import warnings

from misc.first import first
from misc.has_eps import has_eps
from parse.TREParser import TREParser


# NOT NEEDED? JUST ALWAYS RENAME?

def is_det(node)->bool:

    node_type = type(node)


    match node_type:

        case TREParser.EpsExprContext:
            raise NotImplementedError

        case TREParser.AtomicExprContext:
            node:TREParser.AtomicExprContext
            return True


        case TREParser.ParenExprContext:
            node: TREParser.ParenExprContext
            expr = node.expr()

            return is_det(expr)

        case TREParser.UnionExprContext:
            node: TREParser.UnionExprContext
            e1 = node.expr(0)
            e2 = node.expr(1)

            return (not bool(first(e1).intersection(first(e2)))) and is_det(e1) and is_det(e2)


        case TREParser.TimedExprContext:
            node: TREParser.TimedExprContext

            interval = (int(node.interval().INT(0).getText()), int(node.interval().INT(1).getText()))

            expr: TREParser.ExprContext = node.expr()

            return is_det(expr)


        case TREParser.ConcatExprContext:
            node : TREParser.ConcatExprContext

            e1, e2 = node.expr(0), node.expr(1)

            if has_eps(e1):
                return (not bool(first(e1).intersection(first(e2)))) and is_det(e1) and is_det(e2)
            else:
                return is_det(e1) and is_det(e2)

        case TREParser.KleeneExprContext:
            node : TREParser.KleeneExprContext

            # e* = epsilon + ee*
            # epsilon has 0 volume so we can ignore it in sampling
            e0, e0_star = node.expr(), node



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