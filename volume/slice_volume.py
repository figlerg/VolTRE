from math import inf

import matplotlib.pyplot as plt
from antlr4 import FileStream, CommonTokenStream
from sympy import Piecewise, poly
from sympy.abc import T, t

from volume.VolumePoly import VolumePoly
from parse.SyntaxError import HardSyntaxErrorStrategy
from parse.TREParser import TREParser
from visualize_recursion import generate_syntax_tree, highlight_node

from functools import lru_cache

@lru_cache
def slice_volume(node: TREParser.ExprContext, n, cache=None, vis=None, debug_mode=False, return_cache=False):

    node_text = node.getText()  # just for debugging

    if not vis and debug_mode:
        vis = generate_syntax_tree(node)

    ## moved this to end so it also captures cached calls
    # if debug_mode:
        # highlight_node(vis, str(node), comment=f"n = {n}")
        # print(f"node = {node_text}, n = {n}")
        # highlight_node(vis, str(node), comment=f"n = {n}")


    # if cache is None:
    #     cache = {}
    # assert n >= 0, "Recursion bug."


    # # memoizer: i ask this first in the elif, in case we already computed the poly we just jump right to return
    # if (n,node) in cache:
    #     if debug_mode:
    #         print(f"n = {n}\t node = {node.getText()}\t poly = {cache[(n,node)]} \t (cached)")
    #
    #     out =  cache[(n,node)]

    if n == 0:
        # TODO check for deltas? probably by asking whether the node accepts epsilon.
        #  THIS IS NOT TRIVIAL! I basically need to check children for whether they allow epsilon?
        #  For now I say that only Kleene admits epsilon, since epsilon is not really present elsewhere.
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
        out = slice_volume(expr, n, cache=cache, vis=vis, debug_mode=debug_mode)

    elif isinstance(node, TREParser.UnionExprContext):
        # the plus is overloaded: normal addition of piecewise polynomials
        out = slice_volume(node.expr(0), n, cache=cache, vis=vis, debug_mode=debug_mode) + slice_volume(node.expr(1), n, cache=cache, vis=vis, debug_mode=debug_mode)

    elif isinstance(node, TREParser.ConcatExprContext):
        out = VolumePoly()  # the zero poly

        # discrete convolution
        for i in range(n + 1):
            # continuous convolution - ** is overloaded with convolution of two piecewise poly objects
            out += slice_volume(node.expr(0), i, cache=cache, vis=vis, debug_mode=debug_mode) ** slice_volume(node.expr(1), n - i, cache=cache, vis=vis, debug_mode=debug_mode)

    elif isinstance(node, TREParser.TimedExprContext):
        child_volume = slice_volume(node.expr(), n, cache=cache, vis=vis, debug_mode=debug_mode)
        restriction_interval = (int(node.interval().INT(0).getText()), int(node.interval().INT(1).getText()))

        child_volume.time_restriction(restriction_interval)  # does the interval intersection in place for all intervals

        out = child_volume

    elif isinstance(node, TREParser.KleeneExprContext):
        # TODO there might still be a way to save some computations with something like fast quaring
        expr = node.expr()
        out = VolumePoly()  # the zero poly

        for i in range(0, n + 1):

            # this is the case where no intervals survive, since V(e, 0) is 0 everywhere -> skip this.
            # This is due to the assumption that epsilon is not in expr.
            if i == 0:
                continue

            # # this is the case where we simply take the expr intervals, since V(e**, 0) is the dirac and works as unit
            # if i == n:
            #     out += slice_volume(expr, n, cache=cache, vis=vis, debug_mode=debug_mode)
            #     pass
            ## Note: the dirac is now handled in the convolution in __pow__

            # continuous convolution - unfolding one e from e**. TODO fast squaring would have to happen with two "node" inputs, right? but what is the base case?
            intermediate_poly = (slice_volume(expr, i, cache=cache, vis=vis, debug_mode=debug_mode) **
                                 slice_volume(node, n - i, cache=cache, vis=vis, debug_mode=debug_mode))

            out += intermediate_poly

            # note that we always return 0 for n==0 above, and mathematically assume that the empty word is not in expr
            #  so we do not have the problematic case with blowup (i == 0 on paper)

    else:
        raise Exception("Bad state.")

    out.exp = node.getText()
    out.n = n

    # if cache:
    #     cache[(n,node)] = out

    if debug_mode:
        print(f"n = {n}\t node = {node.getText()}\t poly = {out}")

        print(f"node = {node_text}, n = {n}")
        highlight_node(vis, str(node), comment=f"n = {n}, p/T) = {out}")

    # in some cases we want to reuse the cache
    if return_cache:
        return out, cache



    return out # this is the standard output


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