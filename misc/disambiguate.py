from parse.TREParser import TREParser
import warnings
from misc.recursion_template import get_interval

def disambiguate(node:TREParser.ExprContext, dis_map = None, return_inverse_map = False):
    """
    A renaming trick: We give each occurrence of a symbol a new name
    (its name plus the number of its prior occurences +1).

    The output is a non-ambiguous expression with the same language after renaming, but a distorted
    syntax tree. We can fix the distortion in sampling.
    """


    node_type = type(node)

    if dis_map == None:
        dis_map = dict()

    match node_type:

        case TREParser.EpsExprContext:
            node: TREParser.EpsExprContext
            return node.getText()

        case TREParser.AtomicExprContext:
            node: TREParser.AtomicExprContext
            sym = node.getText()

            try:
                dis_map[sym] += 1
            except KeyError:
                dis_map[sym] = 1

            out = sym + str(dis_map[sym])

        case TREParser.ParenExprContext:
            node: TREParser.ParenExprContext
            expr = node.expr()

            out = f"({disambiguate(expr, dis_map)})"

        case TREParser.UnionExprContext:
            node: TREParser.UnionExprContext
            e1 = node.expr(0)
            e2 = node.expr(1)

            out = f"{disambiguate(e1, dis_map)} + {disambiguate(e2, dis_map)}"

        case TREParser.TimedExprContext:
            node: TREParser.TimedExprContext

            a,b = get_interval(node)

            expr: TREParser.ExprContext = node.expr()

            out = f"<{disambiguate(expr, dis_map)}>_[{a},{b}]"

        case TREParser.ConcatExprContext:
            node: TREParser.ConcatExprContext

            e1, e2 = node.expr(0), node.expr(1)

            out = f"{disambiguate(e1, dis_map)} . {disambiguate(e2, dis_map)}"

        case TREParser.KleeneExprContext:
            node: TREParser.KleeneExprContext

            # e* = epsilon + ee*
            # epsilon has 0 volume so we can ignore it in sampling
            e0 = node.expr()

            out = f"{disambiguate(e0, dis_map)}*"

        case TREParser.IntersectionExprContext:
            node: TREParser.IntersectionExprContext
            warnings.warn("Sampling for intersection and renaming is experimental and may not terminate.")

            e1, e2 = node.expr(0), node.expr(1)

            out = f"{disambiguate(e1, dis_map)} & {disambiguate(e2, dis_map)}"

        case TREParser.RenameExprContext:
            node: TREParser.RenameExprContext
            warnings.warn("Sampling for intersection and renaming is experimental and may not terminate.")

            expr = node.expr()

            tokens = [disambiguate(token, dis_map) for token in node.rename_token()]

            out = f"{','.join(tokens)}{disambiguate(expr, dis_map)}"

        case TREParser.Rename_tokenContext:
            node: TREParser.Rename_tokenContext
            raise ValueError("disambiguate() called on unresolved renaming node. This usage is not intended. "
                             "Fix by apply_renaming first.")
            # TODO this could also be done directly here, but not sure if that isn't more confusing.

        case _:
            raise NotImplementedError("Encountered unknown rule in grammar. "
                                      "Probably some recursion function needs an update for the new rule."
                                      f"Node type: {node_type}")

    # we also need the dictionary as an output in some cases
    if return_inverse_map:
        # print(f"f \t= {dis_map}")
        # print(f"f_inv \t= {invert_dis_map(dis_map)}")

        return out, invert_dis_map(dis_map)

    return out


def invert_dis_map(dis_map: dict):
    inv = dict()

    for key in dis_map:
        for i in range(1, dis_map[key] + 1):
            inv[f"{key}{i}"] = key

    return inv
