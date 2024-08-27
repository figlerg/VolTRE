from typing import Set

from misc.recursion_template import get_interval
from parse.TREParser import TREParser
from parse.quickparse import quickparse
from sample.TimedWord import TimedWord
import warnings

from itertools import product

# TODO this is harder than expected? What are the sets that I combine?

# IDEA: The match witnesses are subtrees: Each subtree must have len(w) leafs exactly.
#   NO! We can get multiple letters from *, so it isn't necessarily a subtree?

# IDEA2: The match witnesses are itself trees.
#   However, they are not like the syntax trees anymore.
#   Instead, they record exactly how many phi_0 we get out of any kleene node, and only ever get one of the union node children.
#   Each node has an integer for how many letters it consumes.
# e.g.


# TODO ask dejan/nicolas if this makes sense. I remember the witnesses to be "runs" in other automata paper?
class WitnessNode:
    def __init__(self, exp_ref=None, children=None):
        self.exp_ref = exp_ref
        # Convert children to a tuple to make it immutable
        self.children = tuple(children) if children is not None else tuple()

    def __hash__(self):
        # Combine the hash of exp_ref and the tuple of children
        return hash((self.exp_ref, self.children))

    def __eq__(self, other):
        if not isinstance(other, WitnessNode):
            return False
        # Check both exp_ref and children for equality
        return self.exp_ref == other.exp_ref and self.children == other.children

    def is_leaf(self):
        return not self.children

    def add_child(self, child):
        # Create a new tuple with the additional child and reassign
        self.children += (child,)


"""
My idea for the algorithm: Create a specififc witness for each match, then combine them and add them to a set.
The question is whether this approach (and my assumptions) is sound, and what the witness should be. 


"""


def intersection_match(w:TimedWord, phi: TREParser.ExprContext) -> Set[WitnessNode]:

    node_type = type(phi)
    print(node_type)
    phi_text = phi.getText()
    phi_ref = repr(phi)

    match node_type:

        case TREParser.AtomicExprContext:
            atom = phi.getText()

            if w.length == 1 and w[0][0] == atom:
                s = {WitnessNode(exp_ref=phi_ref)}
            else:
                s = set()

        case TREParser.ParenExprContext:
            phi: TREParser.ParenExprContext
            expr = phi.expr()

            s = intersection_match(w, expr)

        case TREParser.UnionExprContext:
            phi: TREParser.UnionExprContext
            e1 = phi.expr(0)
            e2 = phi.expr(1)

            s1 = intersection_match(w,e1)
            s2 = intersection_match(w,e2)

            s = s1.union(s2)

        case TREParser.TimedExprContext:
            phi: TREParser.TimedExprContext

            a,b = get_interval(phi)
            expr: TREParser.ExprContext = phi.expr()

            if a <= w.duration <= b:
                s = intersection_match(w, expr)
            else:
                s = set()

        case TREParser.ConcatExprContext:
            phi: TREParser.ConcatExprContext

            e1, e2 = phi.expr(0), phi.expr(1)

            s = set()
            for k in range(w.length+1):
                s1 = intersection_match(w[:k], e1)
                s2 = intersection_match(w[k:],e2)

                s.update(combine(s1,s2,phi))

        case TREParser.KleeneExprContext:
            phi: TREParser.KleeneExprContext

            e1, e2 = phi.expr(), phi

            """
            Case: word is 1 letter long. 
                We have w[:0]*w[0:] == w. 
                Further w[0:] == w.
                In kleene we evaluate match(w[0],e) and concatenate with match(EPS,e*).

            """

            # need to check for epsilon
            if w.is_epsilon():
                s = {WitnessNode(exp_ref=phi_ref)}
            else:
                s = set()
                for k in range(w.length+1):
                    s1 = intersection_match(w[:k], e1)

                    # this guards against infinite recursion: if N1 is 0 we do not need to look at the other factor
                    if s1:
                        s2 = intersection_match(w[k:], e2)
                    else:
                        continue

                    s.update(combine(s1,s2,phi))

        case TREParser.IntersectionExprContext:
            phi:TREParser.IntersectionExprContext
            warnings.warn("Sampling for intersection and renaming is experimental and may not terminate.")
            s1 = intersection_match(w,phi.expr(0))
            s2 = intersection_match(w,phi.expr(1))

            return s1.intersection(s2)

        case TREParser.RenameExprContext:
            warnings.warn("Sampling for intersection and renaming is experimental and may not terminate.")
            raise NotImplementedError

        case _:
            raise NotImplementedError('Was a new grammar rule added?')

    # if isinstance(phi, TREParser.TimedExprContext):
    #     print(f"N({phi.getText()}\t,\t{w})= {N}")
    #     print(w.dates)
    #     print('')

    return s


def combine(s1, s2, parent):
    out = set()

    k_cut_matches = product(s1, s2)


    for a, b in k_cut_matches:
        witness = WitnessNode(exp_ref=repr(parent))
        witness.add_child(a)
        witness.add_child(b)

        out.add(witness)
    return out