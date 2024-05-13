from math import inf

import matplotlib.pyplot as plt
from antlr4 import FileStream, CommonTokenStream
from sympy import Piecewise, poly
from sympy.abc import T, t

from VolumePoly import VolumePoly
from parse.SyntaxError import HardSyntaxErrorStrategy
from parse.TREParser import TREParser
from visualize_recursion import generate_syntax_tree, highlight_node


def slice_volume(node: TREParser.ExprContext, n, cache=None, vis=None):

    node_text = node.getText()  # just for debugging

    if not vis and DEBUG_MODE:
        vis = generate_syntax_tree(node)

    if DEBUG_MODE:
        highlight_node(vis, str(node), n)

    if cache is None:
        cache = {}
    assert n >= 0, "Recursion bug."


    # memoizer
    if (n,node) in cache:
        if DEBUG_MODE:
            print(f"n = {n}\t node = {node.getText()}\t poly = {cache[(n,node)]} \t (cached)")

        return cache[(n,node)]

    if n == 0:
        # TODO check for deltas? probably by asking whether the node accepts epsilon. THIS IS NOT TRIVIAL! I basically need to check children for whether they allow epsilon?
        out = VolumePoly([], [])
        if isinstance(node, TREParser.KleeneExprContext):
            out.delta = True



    elif isinstance(node, TREParser.AtomicExprContext):
        if n == 1:
            ints = [(0, inf), ]
            polys = [poly(1, T)]  # the only way I found for representing constant functions
            out = VolumePoly(ints, polys)
        else:
            out = VolumePoly()  # 0 poly if we have more or less letters

    elif isinstance(node, TREParser.ParenExprContext):
        expr = node.expr()
        out = slice_volume(expr, n, cache=cache, vis=vis)

    elif isinstance(node, TREParser.UnionExprContext):
        # the plus is overloaded: normal addition of piecewise polynomials
        out = slice_volume(node.expr(0), n, cache=cache, vis=vis) + slice_volume(node.expr(1), n, cache=cache, vis=vis)

    elif isinstance(node, TREParser.ConcatExprContext):
        out = VolumePoly()  # the zero poly

        # discrete convolution
        for i in range(n + 1):
            # continuous convolution - ** is overloaded with convolution of two piecewise poly objects
            out += slice_volume(node.expr(0), i, cache=cache, vis=vis) ** slice_volume(node.expr(1), n - i, cache=cache, vis=vis)

    elif isinstance(node, TREParser.TimedExprContext):
        child_volume = slice_volume(node.expr(), n, cache=cache, vis=vis)
        restriction_interval = (int(node.interval().INT(0).getText()), int(node.interval().INT(1).getText()))

        child_volume.time_restriction(restriction_interval)  # does the interval intersection in place for all intervals

        out = child_volume

    elif isinstance(node, TREParser.KleeneExprContext):
        # TODO there might still be a way to save some computations with something like fast quaring
        expr = node.expr()
        out = VolumePoly()  # the zero poly

        for i in range(0, n + 1):

            # this is the case where no intervals survive, since V(e, i) is 0 everywhere.
            if i == 0:
                continue

            # # this is the case where we simply take the expr intervals, since V(e**, 0) is the dirac and works as unit
            # if i == n:
            #     out += slice_volume(expr, n, cache=cache, vis=vis)
            #     pass

            intermediate_poly = slice_volume(expr, i, cache=cache, vis=vis) ** slice_volume(node, n - i, cache=cache, vis=vis) # TODO visualize these together with the syntax tree

            # continuous convolution - unfolding one e from e**. TODO fast squaring would have to happen with two "node" inputs, right? but what is the base case?
            out += intermediate_poly

            # note that we always return 0 for n==0 above, and mathematically assume that the empty word is not in expr
            #  so we do not have the problematic case with blowup (i == 0 on paper)

    else:
        raise Exception("Bad state.")

    out.exp = node.getText()
    out.n = n

    cache[(n,node)] = out

    if DEBUG_MODE:
        print(f"n = {n}\t node = {node.getText()}\t poly = {out}")

    return out


### FLAG FOR THE CURRENT DEBUG MODE
DEBUG_MODE = False

if __name__ == '__main__':
    from parse.TRELexer import TRELexer
    from parse.TREParser import TREParser

    from os.path import join


    input_stream = FileStream(join('parse', 'test.txt'))
    print(f'input: {input_stream}')

    lexer = TRELexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = TREParser(stream)
    parser._errHandler = HardSyntaxErrorStrategy()
    ctx = parser.expr()


    f = slice_volume(ctx,2)

    f.plot()