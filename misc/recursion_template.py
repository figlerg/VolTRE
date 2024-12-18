import warnings

from parse.TREParser import TREParser
from math import inf



def generic_function(node):


    node_type = type(node)


    match node_type:

        case TREParser.EpsExprContext:
            raise NotImplementedError

        case TREParser.AtomicExprContext:
                node:TREParser.AtomicExprContext
                raise NotImplementedError

        case TREParser.ParenExprContext:
            node: TREParser.ParenExprContext
            expr = node.expr()

            raise NotImplementedError

        case TREParser.UnionExprContext:
            node: TREParser.UnionExprContext
            e1 = node.expr(0)
            e2 = node.expr(1)

            raise NotImplementedError

        case TREParser.TimedExprContext:
            node: TREParser.TimedExprContext

            a,b = get_interval(node)

            expr: TREParser.ExprContext = node.expr()

            raise NotImplementedError


        case TREParser.ConcatExprContext:
            node : TREParser.ConcatExprContext

            e1, e2 = node.expr(0), node.expr(1)

            raise NotImplementedError

        case TREParser.KleeneExprContext:
            node : TREParser.KleeneExprContext

            # e* = epsilon + ee*
            # epsilon has 0 volume so we can ignore it in sampling
            e1, e2 = node.expr(), node

            raise NotImplementedError

        case TREParser.IntersectionExprContext:
            node: TREParser.IntersectionExprContext
            warnings.warn("Sampling for intersection and renaming is experimental and may not terminate.")

            e1, e2 = node.expr(0), node.expr(1)

            raise NotImplementedError

        case TREParser.RenameExprContext:
            node: TREParser.RenameExprContext
            warnings.warn("Sampling for intersection and renaming is experimental and may not terminate.")

            expr = node.expr()

            raise NotImplementedError

        case _:
            raise NotImplementedError("Encountered unknown rule in grammar. "
                                      "Probably some recursion function needs an update for the new rule.")


def get_interval(node:TREParser.TimedExprContext):
    a = int(node.interval().INT(0).getText())
    # we allow [INT, INF] or [INT, oo] intervals. Then INT() has len 1
    if len(node.interval().INT()) == 2:
        b = int(node.interval().INT(1).getText())
    else:
        b = inf
    return a, b