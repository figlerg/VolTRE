import warnings

from parse.TREParser import TREParser




node = 0


node_type = type(node)


match node_type:

    case TREParser.AtomicExprContext:
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

        interval = (int(node.interval().INT(0).getText()), int(node.interval().INT(1).getText()))

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