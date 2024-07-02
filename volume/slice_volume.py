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


    if isinstance(node, TREParser.AtomicExprContext):
        if n == 1:
            ints = [(0, inf), ]
            polys = [poly(1, T)]  # the only way I found for representing constant functions
            out = VolumePoly(ints, polys)
        else:
            out = VolumePoly()  # 0 poly if we have more or less letters

    elif isinstance(node, TREParser.ParenExprContext):
        expr = node.expr()
        out = slice_volume(expr, n, vis=vis, debug_mode=debug_mode, debug_container=debug_container)

    elif isinstance(node, TREParser.UnionExprContext):
        # the plus is overloaded: normal addition of piecewise polynomials
        out = slice_volume(node.expr(0), n, vis=vis, debug_mode=debug_mode, debug_container=debug_container) + slice_volume(node.expr(1), n, vis=vis, debug_mode=debug_mode, debug_container=debug_container)

    elif isinstance(node, TREParser.ConcatExprContext):
        out = VolumePoly()  # the zero poly

        # discrete convolution
        for i in range(n + 1):
            # continuous convolution - ** is overloaded with convolution of two piecewise poly objects

            v1 = slice_volume(node.expr(0), i, vis=vis, debug_mode=debug_mode, debug_container=debug_container)
            v2 = slice_volume(node.expr(1), n - i, vis=vis, debug_mode=debug_mode, debug_container=debug_container)

            intermediate_poly = v1 ** v2

            out += intermediate_poly

    elif isinstance(node, TREParser.TimedExprContext):
        child_volume = slice_volume(node.expr(), n, vis=vis, debug_mode=debug_mode, debug_container=debug_container)
        restriction_interval = (int(node.interval().INT(0).getText()), int(node.interval().INT(1).getText()))

        child_volume = child_volume.time_restriction(restriction_interval)

        out = child_volume

    elif isinstance(node, TREParser.KleeneExprContext):
        # TODO there might still be a way to save some computations with something like fast quaring
        expr = node.expr()

        # this is a bit tricky: we don't want to even enter the loop below for n == 0, it is just delta.
        if n == 0:
            out = VolumePoly(delta=1)  # delta distribution
            n = -1 # makes us skip the loop

        # Otherwise it is the zero poly and gets the other stuff added
        else:
            out = VolumePoly()

        for i in range(0, n + 1):

            # this is the case where no intervals survive, since V(e, 0) is 0 everywhere -> skip this.
            # This is due to the assumption that epsilon is not in expr.
            if i == 0:
                continue

            # continuous convolution - unfolding one e from e**. TODO fast squaring would have to happen with two "node" inputs, right? but what is the base case?
            v1 = slice_volume(expr, i, vis=vis, debug_mode=debug_mode, debug_container=debug_container)
            v2 = slice_volume(node, n - i, vis=vis, debug_mode=debug_mode, debug_container=debug_container)

            intermediate_poly = v1 ** v2

            out += intermediate_poly

    else:
        raise Exception("Bad state.")

    out.exp = node.getText()
    out.n = n

    # if cache:
    #     cache[(n,node)] = out

    if debug_mode:
        print(f"n = {n}\t\t node = {node.getText()}\t\t poly = {out}")

        print(f"node = {node_text}, n = {n}")
        highlight_node(vis, str(node), comment=f"n = {n}, p/T) = {out}")

    # cond = isinstance(node, )
    # assert not cond or out.is_cont(), "Encountered a VolumePoly that should be continuous but isn't."

    assert not delta_and_function(out)

    return out


def hybrid_concatenation(node1, node2, n, is_kleene = False):
    pass


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