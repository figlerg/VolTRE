import warnings

from parse.TREParser import TREParser
from misc.has_eps import has_eps
from parse.quickparse import quickparse


def first(node)->set:

    node_type = type(node)


    match node_type:

        case TREParser.AtomicExprContext:
            node: TREParser.AtomicExprContext

            sym = node.getText()
            out = {sym}

        case TREParser.ParenExprContext:
            node: TREParser.ParenExprContext
            expr = node.expr()

            out = first(expr)

        case TREParser.UnionExprContext:
            node: TREParser.UnionExprContext
            e1 = node.expr(0)
            e2 = node.expr(1)

            out = first(e1).union(first(e2))

        case TREParser.TimedExprContext:
            node: TREParser.TimedExprContext

            interval = (int(node.interval().INT(0).getText()), int(node.interval().INT(1).getText()))

            expr: TREParser.ExprContext = node.expr()

            out = first(expr)  # TODO can we do better? Time is just ignored

        case TREParser.ConcatExprContext:
            node : TREParser.ConcatExprContext

            e1, e2 = node.expr(0), node.expr(1)

            if has_eps(e1):
                out = first(e1).union(first(e2))
            else:
                out = first(e1)

        case TREParser.KleeneExprContext:
            node : TREParser.KleeneExprContext

            # e* = epsilon + ee*
            # epsilon has 0 volume so we can ignore it in sampling
            e1, e2 = node.expr(), node

            out = first(e1)

        case TREParser.IntersectionExprContext:
            node: TREParser.IntersectionExprContext
            warnings.warn("Sampling for intersection and renaming is experimental and may not terminate.")

            e1, e2 = node.expr(0), node.expr(1)

            return first(e1).intersection(first(e2))

        case TREParser.RenameExprContext:
            node: TREParser.RenameExprContext
            warnings.warn("Sampling for intersection and renaming is experimental and may not terminate.")

            expr = node.expr()

            raise ValueError("You should apply the renaming before running this function.")

        case _:
            raise NotImplementedError("Encountered unknown rule in grammar. "
                                      "Probably some recursion function needs an update for the new rule.")


    return out

if __name__ == '__main__':
    ctx = quickparse('experiments/spec_00.tre')
    ctx2 = quickparse('experiments/spec_17_first.tre')
    ctx3 = quickparse('experiments/spec_14_eps.tre')

    print(ctx.getText())
    print(first(ctx))

    print(ctx2.getText())
    print(first(ctx2))

    print(ctx3.getText())
    print(first(ctx3))