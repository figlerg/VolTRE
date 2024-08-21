import warnings

from misc.recursion_template import get_interval
from parse.TREParser import TREParser
from parse.quickparse import quickparse


def has_eps(node) -> bool:

    node_type = type(node)


    match node_type:

        case TREParser.EpsExprContext:
            return True

        case TREParser.AtomicExprContext:
            return False

        case TREParser.ParenExprContext:
            node: TREParser.ParenExprContext
            expr = node.expr()

            return has_eps(expr)

        case TREParser.UnionExprContext:
            node: TREParser.UnionExprContext
            e1 = node.expr(0)
            e2 = node.expr(1)

            return has_eps(e1) or has_eps(e2)

        case TREParser.TimedExprContext:
            node: TREParser.TimedExprContext

            a,b = get_interval(node)

            expr: TREParser.ExprContext = node.expr()

            return a <= 0 <= b and has_eps(expr)


        case TREParser.ConcatExprContext:
            node : TREParser.ConcatExprContext

            e1, e2 = node.expr(0), node.expr(1)

            return has_eps(e1) and has_eps(e2)

        case TREParser.KleeneExprContext:
            node : TREParser.KleeneExprContext

            # e* = epsilon + ee*
            # epsilon has 0 volume so we can ignore it in sampling
            e1, e2 = node.expr(), node

            return True

        case TREParser.IntersectionExprContext:
            node: TREParser.IntersectionExprContext
            warnings.warn("Sampling for intersection and renaming is experimental and may not terminate.")

            e1, e2 = node.expr(0), node.expr(1)

            return has_eps(e1) and has_eps(e2)

        case TREParser.RenameExprContext:
            node: TREParser.RenameExprContext
            warnings.warn("Sampling for intersection and renaming is experimental and may not terminate.")

            expr = node.expr()

            return has_eps(expr) # doesn't matter if it's renamed

        case _:
            raise NotImplementedError("Encountered unknown rule in grammar. "
                                      "Probably some recursion function needs an update for the new rule.")


if __name__ == '__main__':
    ctx = quickparse('experiments/spec_12_eps.tre')
    ctx2 = quickparse('experiments/spec_13_atom.tre')
    ctx3 = quickparse('experiments/spec_14_eps.tre')

    print(has_eps(ctx))     # True
    print(has_eps(ctx2))    # False
    print(has_eps(ctx3))    # True
