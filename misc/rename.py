"""
Apply all the renamings in the expression.
"""
import math
import warnings

from parse.TREParser import TREParser
from parse.quickparse import quickparse
from misc.recursion_template import get_interval


def rename(node:TREParser.ExprContext, ren_map = None) -> TREParser.ExprContext:
    """
    Applies all the renaming nodes in the tree, returns a tree that has no renaming nodes.
    """


    node_type = type(node)

    top = ren_map == None
    if top:
        ren_map = dict()

    match node_type:

        case TREParser.AtomicExprContext:
            node: TREParser.AtomicExprContext

            try:
                return ren_map[node.getText()]
            except KeyError:
                return node.getText()



        case TREParser.ParenExprContext:
            node: TREParser.ParenExprContext
            expr = node.expr()

            out = f"({rename(expr, ren_map)})"

        case TREParser.UnionExprContext:
            node: TREParser.UnionExprContext
            e1 = node.expr(0)
            e2 = node.expr(1)

            out = f"{rename(e1, ren_map)} + {rename(e2, ren_map)}"

        case TREParser.TimedExprContext:
            node: TREParser.TimedExprContext

            a,b = get_interval(node)
            if b == math.inf:
                b = node.interval().INF().getText()

            expr: TREParser.ExprContext = node.expr()

            out = f"<{rename(expr, ren_map)}>_[{a},{b}]"

        case TREParser.ConcatExprContext:
            node: TREParser.ConcatExprContext

            e1, e2 = node.expr(0), node.expr(1)

            out = f"{rename(e1, ren_map)} . {rename(e2, ren_map)}"

        case TREParser.KleeneExprContext:
            node: TREParser.KleeneExprContext

            # e* = epsilon + ee*
            # epsilon has 0 volume so we can ignore it in sampling
            e0 = node.expr()

            out = f"{rename(e0, ren_map)}*"

        case TREParser.IntersectionExprContext:
            node: TREParser.IntersectionExprContext

            e1, e2 = node.expr(0), node.expr(1)

            out = f"{rename(e1, ren_map)} & {rename(e2, ren_map)}"

        case TREParser.RenameExprContext:
            node: TREParser.RenameExprContext

            sub_ren_map = get_renaming_dict(node)

            # first fetch the renamings from the subexpressions and apply them
            sub_str = rename(node.expr(), ren_map = sub_ren_map)
            sub = quickparse(sub_str, string=True)

            # finally apply the input map to the new node without renamings
            out = rename(sub,ren_map = ren_map)

        case _:
            raise NotImplementedError("Encountered unknown rule in grammar. "
                                      "Probably some recursion function needs an update for the new rule.")

    # TODO this is not as clean as it could be: I am creating strings and parsing multiple times during renaming
    if top:
        # only in this case do I return a ctx object
        return quickparse(out, string=True)
    return out

def get_renaming_dict(node):
    assert isinstance(node, TREParser.RenameExprContext)


    return {tok.atomic_expr(0).getText():tok.atomic_expr(1).getText() for tok in node.rename_token()}


if __name__ == '__main__':
    ctx = quickparse(parse_input="../experiments/spec_08_renaming.tre")
    print(ctx.getText())
    print(rename(ctx).getText())