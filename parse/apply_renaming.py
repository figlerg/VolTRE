import warnings

from parse.TREParser import TREParser


def apply_renaming(node:TREParser.ExprContext, renaming:dict=None):

    node_type = type(node)

    match node_type:

        case TREParser.AtomicExprContext:
            node: TREParser.AtomicExprContext
            sym = node.getText()

            if sym in renaming.keys():
                out = renaming[sym]
            else:
                out = sym

        case TREParser.ParenExprContext:
            node: TREParser.ParenExprContext
            expr = node.expr()

            out = f"({apply_renaming(expr, renaming)})"

        case TREParser.UnionExprContext:
            node: TREParser.UnionExprContext
            e1 = node.expr(0)
            e2 = node.expr(1)

            out = f"{apply_renaming(e1, renaming)} + {apply_renaming(e2, renaming)}"

        case TREParser.TimedExprContext:
            node: TREParser.TimedExprContext

            a,b = (int(node.interval().INT(0).getText()), int(node.interval().INT(1).getText()))
            expr: TREParser.ExprContext = node.expr()

            out = f"<{apply_renaming(expr, renaming)}>_[{a},{b}]"

        case TREParser.ConcatExprContext:
            node: TREParser.ConcatExprContext

            e1, e2 = node.expr(0), node.expr(1)

            out = f"{apply_renaming(e1, renaming)} . {apply_renaming(e2, renaming)}"

        case TREParser.KleeneExprContext:
            node: TREParser.KleeneExprContext

            # e* = epsilon + ee*
            # epsilon has 0 volume so we can ignore it in sampling
            e0 = node.expr()

            out = f"{apply_renaming(e0, renaming)}*"

        case TREParser.IntersectionExprContext:
            node: TREParser.IntersectionExprContext
            warnings.warn("Sampling for intersection and renaming is experimental and may not terminate.")

            e1, e2 = node.expr(0), node.expr(1)

            out = f"{apply_renaming(e1, renaming)} & {apply_renaming(e2, renaming)}"

        case TREParser.RenameExprContext:
            node: TREParser.RenameExprContext
            warnings.warn("Sampling for intersection and renaming is experimental and may not terminate.")

            expr = node.expr()

            rename_tokens = node.rename_token()
            renaming = {ren_token.atomic_expr(0):ren_token.atomic_expr(1) for ren_token in rename_tokens}

            out = apply_renaming(expr, renaming)

        case _:
            raise NotImplementedError("Encountered unknown rule in grammar. "
                                      "Probably some recursion function needs an update for the new rule.")


    return out