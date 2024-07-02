import warnings

import numpy as np
from antlr4 import ParserRuleContext

from parse.TREParser import TREParser

import random  # i haven't used numpy anywhere, wo why not (maybe it is imported with sympy though)
from enum import Enum, auto

from sympy.abc import x,y,z

from sample.TimedWord import TimedWord
from volume.MaxEntDist import MaxEntDist
from volume.VolumePoly import VolumePoly
from volume.slice_volume import slice_volume
from math import inf


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


class DurationSamplerMode(Enum):
    VANILLA = auto()
    MAX_ENT = auto()

    def __str__(self):
        return self.name

def sample(node: TREParser.ExprContext, n, T=None, mode:DurationSamplerMode = DurationSamplerMode.VANILLA, lambdas = None):
    """
    TODO streamline the signature of this function. Should I have two functions or is the mode here okay?
        Should I check for illegal combinations, like lambdas and vanilla?
    :param node:
    :param n:
    :param T:
    :param mode:
    :param lambdas:
    :return:
    """

    if mode == DurationSamplerMode.VANILLA and lambdas:
        warnings.warn("Invalid usage of the sampling function: vanilla mode shouldn't be used together with a lambdas "
                      "input. Lambdas are being ignored.")
    if mode == DurationSamplerMode.MAX_ENT and T:
        warnings.warn("Invalid usage of the sampling function: For fixed T, max_ent and vanilla are equivalent.")

    if mode == DurationSamplerMode.MAX_ENT and not lambdas:
        raise ValueError("Invalid usage of the sampling function: mode MAXENT needs a lambda input.")


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
            assert n == 1, f"Problem during parsing: Cannot sample letter {node_type.getText()} with {n} letters."

            return TimedWord([node.getText(),], [T,])


        case TREParser.ParenExprContext:
            node: TREParser.ParenExprContext
            e0 = node.expr()
            return sample(e0, n, T)


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

            return sample(chosen_expr,n,T)

        case TREParser.TimedExprContext:
            node: TREParser.TimedExprContext

            interval = (int(node.interval().INT(0).getText()), int(node.interval().INT(1).getText()))

            sub: TREParser.ExprContext = node.expr()

            # TODO unsure whether this means we can run into problems for examples with nonempty volumes...
            #  can the children get illegal delays?
            assert interval[0] <= T <= interval[1], (f"Bad sampling call: The expression {sub.getText()} cannot"
                                                     f" be sampled with T = {T}")

            return sample(sub, n, T)


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

def sample_T(pdf):
    """
    Inverse sampling method for a SymPy polynomial.
    :param pdf:
    :return:
    """


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
        return sample(e2, n-k, T)
    elif vol2.delta and not vol2.intervals:
        return sample(e1, k, T)

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

    return sample(e1,k,T1) * sample(e2, n-k, T2)  # overloaded for concatenation

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

    probas = []

    for k in range(n+1):

        # this is cached by lru_cache and never recomputes anything
        v1 = slice_volume(e1, k)
        v2 = slice_volume(e2, n-k)

        # This function desribes the volumes of words w1w2 where l(w1) = k and l(w2) = n-k.
        V_k = v1 ** v2

        assert concat_vol(T) > 0, "Division by zero during concatenation sampling. Is the language empty for this T?"

        # Dividing the part for k by the overall volume (both for input T) gives the right proba to choose k.
        p_k = V_k(T) / concat_vol(T)

        probas.append(p_k)

    assert abs(np.sum(probas) - 1) < 0.0001, "Problem during sampling of k. Invalid distribution (no pdf)."
    k = random.choices(range(n+1), probas, k=1)[0]

    return k



