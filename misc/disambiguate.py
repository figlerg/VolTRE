from functools import lru_cache

from parse.TREParser import TREParser
import warnings


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

            a,b = (int(node.interval().INT(0).getText()), int(node.interval().INT(1).getText()))
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
            warnings.warn("Sampling for intersection and renaming is experimental and may not terminate.")
            raise NotImplementedError

        case _:
            raise NotImplementedError("Encountered unknown rule in grammar. "
                                      "Probably some recursion function needs an update for the new rule.")

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
