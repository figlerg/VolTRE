from math import inf

import matplotlib.pyplot as plt
from antlr4 import FileStream, CommonTokenStream
from sympy import Piecewise, poly
from sympy.abc import T, t

from volume.VolumePoly import VolumePoly, continuous_convolution
from parse.SyntaxError import HardSyntaxErrorStrategy
from parse.TREParser import TREParser
from visualize_recursion import generate_syntax_tree, highlight_node

from functools import lru_cache

@lru_cache
def slice_volume(node: TREParser.ExprContext, n, vis=None, debug_mode=False, debug_container = None) -> VolumePoly:

    node_text = node.getText()  # just for debugging

    # if not debug_container:
    #     debug_container = set()

    if not vis and debug_mode:
        vis = generate_syntax_tree(node)

    rule = type(node)

    match rule:

        case TREParser.AtomicExprContext:
            node:TREParser.AtomicExprContext
            if n == 1:
                ints = [(0, inf), ]
                polys = [poly(1, T)]  # the only way I found for representing constant functions
                out = VolumePoly(ints, polys)
            else:
                out = VolumePoly()  # 0 poly if we have more or less letters

        case TREParser.ParenExprContext:
            node: TREParser.ParenExprContext
            expr = node.expr()
            out = slice_volume(expr, n, vis=vis, debug_mode=debug_mode, debug_container=debug_container)

        case TREParser.UnionExprContext:
            node: TREParser.UnionExprContext
            # the plus is overloaded: normal addition of piecewise polynomials
            out = slice_volume(node.expr(0), n, vis=vis, debug_mode=debug_mode, debug_container=debug_container) + slice_volume(node.expr(1), n, vis=vis, debug_mode=debug_mode, debug_container=debug_container)

        case TREParser.ConcatExprContext:
            node: TREParser.ConcatExprContext
            out = hybrid_conv(node.expr(0), node.expr(1),n,vis, debug_mode, debug_container)

        case TREParser.TimedExprContext:
            node: TREParser.TimedExprContext
            child_volume = slice_volume(node.expr(), n, vis=vis, debug_mode=debug_mode, debug_container=debug_container)

            a, b = parse_interval(node)

            restriction_interval = (a,b)

            child_volume = child_volume.time_restriction(restriction_interval)

            out = child_volume

        case TREParser.KleeneExprContext:
            node: TREParser.KleeneExprContext
            expr = node.expr()

            # this is a bit tricky: we don't want to even enter the loop below for n == 0, it is just delta.
            if n == 0:
                out = VolumePoly(delta=1)  # delta distribution
                n = -1 # makes us skip the loop

            # Otherwise it is the zero poly and gets the other stuff added
            else:
                out = hybrid_conv(expr, node,n,vis, debug_mode, debug_container, is_kleene=True)

        case TREParser.PlusExprContext:
            node: TREParser.PlusExprContext
            raise NotImplementedError('exp+ is not supported yet.')
            # TODO the below is wrong! In the levels below we can't use this node. We would need a kleene node
            # expr = node.expr()
            # if n == 0:
            #     out = VolumePoly()
            # else:
            #     out = hybrid_conv(expr, node, n, vis, debug_mode, debug_container, is_kleene=True)

        case TREParser.IntersectionExprContext:
            node: TREParser.IntersectionExprContext
            raise ValueError(f'Volume computation for intersection operator & is not supported. '
                                      f'Problematic subexpression: {node.getText()}')

        case TREParser.RenameExprContext:
            node: TREParser.RenameExprContext
            raise ValueError(f'Volume computation for renaming operator is not supported. '
                                      f'Problematic subexpression: {node.getText()}')

        case _:
            raise NotImplementedError("Bad rule in volume generation.")

    out.exp = node.getText()
    out.n = n

    if debug_mode:
        print(f"n = {n}\t\t node = {node.getText()}\t\t poly = {out}")

        print(f"node = {node_text}, n = {n}")
        highlight_node(vis, str(node), comment=f"n = {n}, p/T) = {out}")

    # cond = isinstance(node, ) TODO maybe create a check here to catch bad polys
    # assert not cond or out.is_cont(), "Encountered a VolumePoly that should be continuous but isn't."

    assert not delta_and_function(out)

    return out


def parse_interval(node):
    a = int(node.interval().INT(0).getText())
    # we allow [INT, INF] or [INT, oo] intervals. Then INT() has len 1
    if len(node.interval().INT()) == 2:
        b = int(node.interval().INT(1).getText())
    else:
        b = inf
    return a, b


def hybrid_conv(node1, node2, n, vis=None, debug_mode=False, debug_container = None, is_kleene = False):
    out = VolumePoly()  # the zero poly



    # there is a weird case when concatenating two expressions which admit epsilon, and n = 0. Just return delta here.
    v1_0 = slice_volume(node1, 0, vis=vis, debug_mode=debug_mode, debug_container=debug_container)
    v2_0 = slice_volume(node2, 0, vis=vis, debug_mode=debug_mode, debug_container=debug_container)

    if n == 0 and v1_0.delta and v2_0.delta:
        return VolumePoly(delta=True)

    # discrete convolution
    for i in range(n + 1):
        # continuous convolution - ** is overloaded with convolution of two piecewise poly objects

        # For kleene, this is the case where no intervals survive, since V(e, 0) is 0 everywhere -> skip this.
        # This is due to the assumption that epsilon is not in expr.
        if is_kleene and i == 0:
            continue

        v1 = slice_volume(node1, i, vis=vis, debug_mode=debug_mode, debug_container=debug_container)
        v2 = slice_volume(node2, n - i, vis=vis, debug_mode=debug_mode, debug_container=debug_container)

        intermediate_poly = v1 ** v2

        out += intermediate_poly

    return out


# some debugging checks
def delta_and_function(v:VolumePoly):
    return v.polys and v.delta



# easy test case
if __name__ == '__main__':
    from parse.TRELexer import TRELexer
    from parse.TREParser import TREParser

    from os.path import join


    input_stream = FileStream(join('parse', 'test_spec.txt'))
    print(f'input: {input_stream}')

    lexer = TRELexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = TREParser(stream)
    parser._errHandler = HardSyntaxErrorStrategy()
    ctx = parser.expr()


    f = slice_volume(ctx,2)

    f.plot()