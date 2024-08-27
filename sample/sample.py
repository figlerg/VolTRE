import warnings
from collections import namedtuple

import numpy as np
import tqdm
from antlr4 import ParserRuleContext

from match.match import match
from misc.disambiguate import disambiguate
from misc.exceptions import UserError
from misc.has_eps import has_eps
from misc.helpers import BudgetExhaustedException
from misc.recursion_template import get_interval
from parse.TREParser import TREParser

import random  # i haven't used numpy anywhere, wo why not (maybe it is imported with sympy though)
from enum import Enum, auto

from sympy.abc import x,y,z

from parse.quickparse import quickparse
from sample.TimedWord import TimedWord
from volume.MaxEntDist import MaxEntDist
from volume.VolumePoly import VolumePoly
from volume.slice_volume import slice_volume
from math import inf

# from volume.tuning import lambdas, parameterize_mean_variance

"""
So at this point we can compute V_n^e(T) and V_n(e). Now we can begin to sample.

The idea here is as follows:
- Compute volume functions for all subexpressions (for all relevant n).

I want to "sample downwards". So we start at top with a specific input (n,T) and invoke child samplers.
- The base case is an atomic a where we return the tuple (a,T) .
-recursion:
    - convolution with input (n,T):
        - discrete: select k in 0...n: Select k with proba Vke1(T)/Vne1(T)
        - we have T time available and know Vne, Vne1, Vne2.
            TODO How do we sample T1 and T2? I think its just 1/(Vne1 ** Vne2)
        - we now have a specific recursion input (k,T') for the sampler of e1 and and (n-k, T-T') for the sampler of e2
    - union with input (n,T):        select one of the children according to volumes: Vne1(T)/Vne(T)
    - kleene star with input (n,T):
        - like convolution for e.e*
"""

# Define the namedtuple
Feedback = namedtuple('SampleFeedback', ['rej'])



class DurationSamplerMode(Enum):
    VANILLA = auto()
    MAX_ENT = auto()

    def __str__(self):
        return self.name
def sample(node: TREParser.ExprContext, n, T=None, mode:DurationSamplerMode = DurationSamplerMode.VANILLA,
           lambdas = None, top = True, feedback=False, budget = 500):
    """
        Here I implement the rejection sampling for the most general set of input expressions:
        I allow any (even ambiguous) expression, with intersection only at top level.

        Let phi be the original spec (node in code) and phi' be the disambiguated phi.
            f(phi') = phi
        and in other words
            w' in phi' => f(w') in phi.
        """

    """
    Explaining some dev choices I made here:
    We need to pay special attention to the combination of top level intersection with the disambiguation method:
        If we naively disambiguate everything, then the variables in the 2nd intersection child will be disjunct from
        the first child. Inside of sample_unambig, we don't currently have the reverse mapping to check membership -
        so the easiest would be to provide this for the sample_unambig - except for rejection sampling
        we need to have the uniformity in each iteration. So in fact we CAN'T do the rejection steps inside
        of the sample_unambig. Thus, we need to do it inside of here (and I also pulled out the smart_sampling as its 
        own function since we need it twice).
    """

    ## TODO the input checks are not really needed in this function, since in any case we do them in all of the calls of unambig

    # create string of phi' from phi. also get f during this process
    # TODO actually I only need to do this once, so I should extract this somewhere.
    #  I don't do it yet, because it complicates calling this function. I will probably do a sample_n wrapper function
    #  somewhere, where I can create f once and reuse it.

    intersection_mode = isinstance(node, TREParser.IntersectionExprContext)
    if intersection_mode:
        assert top, "Intersection only allowed at the top level."
        node:TREParser.IntersectionExprContext

        original_child1 = node.expr(0)
        original_child2 = node.expr(1)
        dis_str, f = disambiguate(original_child1, return_inverse_map=True)  # just pick the 1st one TODO smallest better
        child1_dis = quickparse(dis_str, string=True)  # parse the string again to get the syntax tree of phi'

        for _ in range(budget):
            w,rej = smart_sampling(child1_dis, n, T, mode, lambdas, original_child1, f)
            # w.apply_renaming(f) # we need to go back to the original variables

            if match(w,original_child2):
                if feedback:
                    return w, rej
                return w

        # this has no guarantee to ever finish (depending on intersection volumes)
        raise BudgetExhaustedException(f"Rejection budget {budget} exhausted - "
                                       f"maybe the intersection is empty or small."
                                       f"Try changing the budget parameter.")

    # THE NORMAL FUNCTION WITHOUT INTERSECTION:

    dis_str, f = disambiguate(node, return_inverse_map=True)
    phi_dis = quickparse(dis_str, string=True)  # parse the string again to get the syntax tree of phi'

    # print(f"Transformed phi = {node.getText()} to phi' = {phi_dis.getText()} for russian roulette sampling.")

    w,rej = smart_sampling(phi_dis, n, T, mode, lambdas,node, f)

    if feedback:
        return w, rej
    return w

def smart_sampling(phi_dis:TREParser.ExprContext, n, T,mode, lambdas, origin_node, f):
    rej = 0
    while True:
        # now we pick a regular sample from the disambiguous version with the same sampling parameters
        w = sample_unambig(node=phi_dis, n=n, T=T, mode=mode, lambdas=lambdas, top=True)

        # no renaming necessary if empty word
        if w:
            # use the inverse renaming to get a word in the non renamed language
            w.apply_renaming(rename_map=f)

        # count the number of ways to read the generated word WITH ORIGINAL EXPRESSION
        N = match(w, origin_node)

        # accept with proba 1/#matches of w in phi
        if random.random() < 1 / N:
            out = w
            break
        rej += 1

    return out, Feedback(rej=rej)

def sample_unambig(node: TREParser.ExprContext, n, T=None, mode:DurationSamplerMode = DurationSamplerMode.VANILLA,
                   lambdas = None, top = True):
    """
    TODO streamline the signature of this function. Should I have two functions or is the mode here okay?
        Should I check for illegal combinations, like lambdas and vanilla?
    """


    if mode == DurationSamplerMode.VANILLA and lambdas:
        warnings.warn("Vanilla mode shouldn't be used together with a lambdas input. Lambdas are being ignored.")
    if mode == DurationSamplerMode.MAX_ENT and T:
        warnings.warn("Invalid usage of the sampling function: For fixed T, max_ent and vanilla are equivalent.")
    if mode == DurationSamplerMode.MAX_ENT and not isinstance(lambdas, np.ndarray) and not lambdas:
        raise UserError("Need an input for lambdas in MaxEnt mode.")  # isinstance because otherwise np complains
    if isinstance(node, TREParser.IntersectionExprContext) and (not top or T is None):
        raise UserError("Invalid usage: Intersection can only be used at the top level with a fixed T."
                         "In this case we do not have a volume function for the whole expression, so we can't sample T."
                         "The top level is necessary out of the same reason "
                         "(each volume function depends on its children).")

    # This only concerns the top level call:
    # If no fixed T is provided, we sample either according to volumes, or use MaxEnt distribution.
    # Recursive calls fix a T.

    if T is None:
        # the only possible word for n = 0 is EPS -> we can directly take T=0
        if n == 0 and has_eps(node):

            return TimedWord()
        else:
            match mode:

                case DurationSamplerMode.VANILLA:
                    vol = slice_volume(node, n)
                    pdf = vol.pdf

                    T = pdf.inverse_sampling()

                case DurationSamplerMode.MAX_ENT:
                    # TODO could try to do a vectorized sampling here? Maybe we would get a speedup
                    #  (tried with MaxEntDist.n_inverse_sampling but haven't tested it here yet)
                    vol = slice_volume(node, n)
                    weighted_vol = MaxEntDist(vol, lambdas)

                    T = weighted_vol.inverse_sampling()



    node_type = type(node)


    match node_type:

        case TREParser.AtomicExprContext:
            assert n == 1, f"Problem during parsing: Cannot sample letter {node.getText()} with {n} letters."

            return TimedWord([node.getText(),], [T,])


        case TREParser.ParenExprContext:
            node: TREParser.ParenExprContext
            e0 = node.expr()
            return sample_unambig(e0, n, T, top=False)


        case TREParser.UnionExprContext:
            node: TREParser.UnionExprContext
            e1 = node.expr(0)
            e2 = node.expr(1)

            # these are the full piecewise polynomials. They are callable (in which case they return the Volume for T)
            vol1 = slice_volume(e1, n)
            vol2 = slice_volume(e2, n)

            outcomes = [0,1]
            volumes = [vol1(T), vol2(T)]

            outcome = random.choices(outcomes, volumes)[0]

            assert outcome in [0,1], "This should never happen."

            chosen_expr = node.expr(outcome)

            return sample_unambig(chosen_expr, n, T, top=False)

        case TREParser.TimedExprContext:
            node: TREParser.TimedExprContext

            interval = get_interval(node)

            sub: TREParser.ExprContext = node.expr()

            # TODO unsure whether this means we can run into problems for examples with nonempty volumes...
            #  can the children get illegal delays?
            assert interval[0] <= T <= interval[1], (f"Bad sampling call: The expression {sub.getText()} cannot"
                                                     f" be sampled with T = {T}")

            return sample_unambig(sub, n, T, top=False)


        case TREParser.ConcatExprContext:
            node : TREParser.ConcatExprContext

            e1, e2 = node.expr(0), node.expr(1)

            return concat_sampling(node, e1, e2, n, T)

        case TREParser.KleeneExprContext:
            node : TREParser.KleeneExprContext

            # e* = epsilon + ee*
            # epsilon has 0 volume so we can ignore it in sampling
            e1, e2 = node.expr(), node

            return concat_sampling(node, e1, e2, n, T)

        case TREParser.IntersectionExprContext:
            node: TREParser.IntersectionExprContext
            warnings.warn("Sampling for intersection and renaming is experimental and may not terminate.")

            """
            We cannot use the normal method for intersection, since intersection doesn't work with how we compute 
            volumes. But if the intersection is at the top level only (which is checked above), we can do a trick:
            Simply sample in one of them and do rejection sampling with membership in the other Language.
            """

            raise NotImplementedError("This can't work as it is right now. Need to pull this case out to general sampling function, or the renamings mess with the inclusion checking necessary for intersection sampling.")

            # TODO the below code shall move to the general sampling function

            e1, e2 = node.expr(0), node.expr(1)
            vol1, vol2 = slice_volume(e1, n), slice_volume(e2,n)

            # we do not randomly select the subexpression: instead choose smaller vol and check membership in other
            #  (actually we do not care about the order all that much for sampling, but it might be faster)
            pick1 = vol1(T) < vol2(T)
            if not pick1:
                e1, e2 = e2, e1

            budget = 300  # TODO should probably be a param

            counter = 0  # TODO maybe print rejection rate? with this we can estimate the volume of intersection
            for _ in range(budget):
                w = sample_unambig(node=e1, n=n, T=T, mode=mode, lambdas=lambdas, top=False)

                if match(w, e2):
                    counter += 1
                    return w

            # print(f"ratio is {counter/budget}")
            # return w
            raise BudgetExhaustedException(f"Sampling for intersection failed with budget = {budget} rejections."
                                           f"The intersection might be empty or small.")


        case TREParser.RenameExprContext:
            node: TREParser.RenameExprContext
            warnings.warn("Sampling for intersection and renaming is experimental and may not terminate.")

            expr = node.expr()

            raise NotImplementedError


# TODO this is the function before refactoring. check if the results are the same for unambiguous inputs.
#   should be exactly the same after reseeding.
def old_sample(node: TREParser.ExprContext, n, T=None, mode:DurationSamplerMode = DurationSamplerMode.VANILLA,
                   lambdas = None, top = True):
    """
    TODO streamline the signature of this function. Should I have two functions or is the mode here okay?
        Should I check for illegal combinations, like lambdas and vanilla?
    """

    if mode == DurationSamplerMode.VANILLA and lambdas:
        warnings.warn("Invalid usage of the sampling function: vanilla mode shouldn't be used together with a lambdas "
                      "input. Lambdas are being ignored.")
    if mode == DurationSamplerMode.MAX_ENT and T:
        warnings.warn("Invalid usage of the sampling function: For fixed T, max_ent and vanilla are equivalent.")

    try:
        lambdas_flag = bool(lambdas)
    except ValueError:
        # I also allow np arrays
        lambdas_flag = True

    if mode == DurationSamplerMode.MAX_ENT and not lambdas_flag:
        raise ValueError("Invalid usage of the sampling function: mode MAXENT needs a lambda input.")

    if isinstance(node, (TREParser.IntersectionExprContext, TREParser.RenameExprContext)) and (not top or not T):
        raise ValueError("Invalid use of the sampling funtcion: Intersection and Renaming can only be used at top level"
                         "and with a given duration T, since neither fit in the inductive volume computation.")

    # TODO not sure if my handling of T with the standard value None leads to any problems with sampling

    # This only concerns the top level call:
    # If no fixed T is provided, we sample either according to volumes, or use MaxEnt distribution.
    # Recursive calls fix a T.
    if T is None:
        match mode:

            case DurationSamplerMode.VANILLA:
                vol = slice_volume(node, n)

                pdf = vol.pdf  # this normalizes

                # HERE

                T = pdf.inverse_sampling()

            case DurationSamplerMode.MAX_ENT:
                # TODO could try to do a vectorized sampling here? Maybe we would get a speedup
                #  (tried with MaxEntDist.n_inverse_sampling but haven't tested it here yet)

                vol = slice_volume(node, n)
                weighted_vol = MaxEntDist(vol, lambdas)
                T = weighted_vol.inverse_sampling()

    node_type = type(node)

    match node_type:

        case TREParser.AtomicExprContext:
            assert n == 1, f"Problem during parsing: Cannot sample letter {node.getText()} with {n} letters."

            return TimedWord([node.getText(),], [T,])


        case TREParser.ParenExprContext:
            node: TREParser.ParenExprContext
            e0 = node.expr()
            return sample_unambig(e0, n, T, top=False)


        case TREParser.UnionExprContext:
            node: TREParser.UnionExprContext
            e1 = node.expr(0)
            e2 = node.expr(1)

            # these are the full piecewise polynomials. They are callable (in which case they return the Volume for T)
            vol1 = slice_volume(e1, n)
            vol2 = slice_volume(e2, n)

            outcomes = [0,1]
            volumes = [vol1(T), vol2(T)]

            outcome = random.choices(outcomes, volumes)[0]

            assert outcome in [0,1], "This should never happen."

            chosen_expr = node.expr(outcome)

            return sample_unambig(chosen_expr, n, T, top=False)

        case TREParser.TimedExprContext:
            node: TREParser.TimedExprContext

            interval = get_interval(node)

            sub: TREParser.ExprContext = node.expr()

            # TODO unsure whether this means we can run into problems for examples with nonempty volumes...
            #  can the children get illegal delays?
            assert interval[0] <= T <= interval[1], (f"Bad sampling call: The expression {sub.getText()} cannot"
                                                     f" be sampled with T = {T}")

            return sample_unambig(sub, n, T, top=False)


        case TREParser.ConcatExprContext:
            node : TREParser.ConcatExprContext

            e1, e2 = node.expr(0), node.expr(1)

            return concat_sampling(node, e1, e2, n, T)

        case TREParser.KleeneExprContext:
            node : TREParser.KleeneExprContext

            # e* = epsilon + ee*
            # epsilon has 0 volume so we can ignore it in sampling
            e1, e2 = node.expr(), node

            return concat_sampling(node, e1, e2, n, T)

        case TREParser.IntersectionExprContext:
            node: TREParser.IntersectionExprContext
            warnings.warn("Sampling for intersection and renaming is experimental and may not terminate.")

            """
            We cannot use the normal method for intersection, since intersection doesn't work with how we compute 
            volumes. But if the intersection is at the top level only (which is checked above), we can do a trick:
            Simply sample in one of them and do rejection sampling with membership in the other Language.
            """

            e1, e2 = node.expr(0), node.expr(1)
            vol1, vol2 = slice_volume(e1, n), slice_volume(e2,n)

            # we do not randomly select the subexpression: instead choose smaller vol and check membership in other
            #  (actually we do not care about the order all that much for sampling, but it might be faster)
            pick1 = vol1(T) < vol2(T)
            if not pick1:
                e1, e2 = e2, e1

            budget = 100  # TODO should probably be a param

            counter = 0  # TODO maybe print rejection rate? with this we can estimate the volume of intersection
            for _ in range(budget):
                w = sample_unambig(e1, n, T, mode=mode, lambdas=lambdas, top=False)

                if match(w, e2):
                    counter += 1
                    return w

            # print(f"ratio is {counter/budget}")
            # return w
            raise BudgetExhaustedException(f"Sampling for intersection failed with budget = {budget} rejections."
                                           f"The intersection might be empty or small.")


        case TREParser.RenameExprContext:
            node: TREParser.RenameExprContext
            warnings.warn("Sampling for intersection and renaming is experimental and may not terminate.")

            expr = node.expr()

            raise NotImplementedError

def concat_sampling(node, e1:TREParser.ExprContext, e2:TREParser.ExprContext, n, T):
    """
    Since I use this in both Kleene and concat I extracted it. It samples both the discrete cut k and continuous cut T2.
    :param node: The current node. Could be concat or Kleene.
    :param e1: Left node of concatenation.
    :param e2: Right node of concatenation.
    :param n: Fixed length for the current node.
    :param T: Fixed duration for the current node.
    :param vol_cache: Saved volume results. This ensures that no Volumes are ever recomputed.
    :return: A sample timed word.
    """


    concat_vol = slice_volume(node, n)


    # TODO also include single convolutions in the vol_cache so we don't recompute the subconvolutions often

    # TODO sample k according to fraction of k part over sum of all k parts
    k = sample_k(n, T, concat_vol, e1, e2)

    # this never recomputes anything
    vol1:VolumePoly = slice_volume(e1, k)
    vol2:VolumePoly = slice_volume(e2, n-k)

    V_k = vol1 ** vol2

    # mathematically, we want: pdf(x) = vol1(x) * vol2(T - x) / V_k(T)
    # I implemented the method .convolution_operator to transform vol2(x) to vol2(T-x)

    if not (vol1.delta or vol2.delta):
        # this is the normal case where
        integrand = vol1 * vol2.convolution_operator(T)

    # in the delta case we directly call the sampler for the child that isn't delta
    elif vol1.delta and not vol1.intervals:
        return sample_unambig(e2, n - k, T, top=False)
    elif vol2.delta and not vol2.intervals:
        return sample_unambig(e1, k, T, top=False)

    else:
        # above I excluded the case where delta AND some piecewise polynomials appear in the same function.
        # this should never happen

        raise NotImplementedError("Unexpected state, this is likely a bug in the sampling function.")


    # TODO sample T according to fraction of T' pdf over V(T)
    normalisation_factor = 1/V_k(T)
    pdf = (integrand * normalisation_factor)

    # TODO sample this pdfto get T1, T2 for subexpressions -> should be doable with my integral function
    T1 = pdf.inverse_sampling()
    T2 = T-T1

    return sample_unambig(e1, k, T1, top=False) * sample_unambig(e2, n - k, T2, top=False)  # overloaded for concatenation

def sample_k(n, T, concat_vol, e1, e2) -> int:
    """
    For this we need to compute all the volume parts for a specific cut (k,n-k), then build a discrete distribution.
    :param n:
    :param T:
    :param concat_vol: Top node volume function.
    :param e1: Left node in concatenation.
    :param e2: Right node in concatenation.
    :param vol_cache:
    :return: Sampled integer k, chosen according to the fraction of volumes.
    """

    weights = []

    for k in range(n+1):

        # this is cached by lru_cache and never recomputes anything
        v1 = slice_volume(e1, k)
        v2 = slice_volume(e2, n-k)

        # This function desribes the volumes of words w1w2 where l(w1) = k and l(w2) = n-k.
        V_k = v1 ** v2

        assert concat_vol(T) > 0, (f"Division by zero during concatenation sampling. Is the language empty for this T?"
                                   f"\n volume = {concat_vol}"
                                   f"\n T = {T}")

        # Dividing the part for k by the overall volume (both for input T) gives the right proba to choose k.
        p_k = V_k(T) / concat_vol(T)

        weights.append(p_k)

    # assert abs(np.sum(probas) - 1) < 0.0001, "Problem during sampling of k. Invalid distribution (no pdf)."
    k = random.choices(range(n+1), weights, k=1)[0]

    return k

