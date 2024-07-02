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

    # if n == 0:
    #     # TODO check for deltas? probably by asking whether the node accepts epsilon.
    #     #  THIS IS NOT TRIVIAL! I basically need to check children for whether they allow epsilon?
    #     #  For now I say that only Kleene admits epsilon, since epsilon is not really present elsewhere.
    #     out = VolumePoly([], [])
    #     if isinstance(node, TREParser.KleeneExprContext):
    #         out.delta = True


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

            # if (v1,v2) in debug_container:
            #     raise Exception
            # else:
            #     debug_container.add((v1,v2))
            intermediate_poly = continuous_convolution(v1, v2)
            assert not delta_and_function(intermediate_poly)
            assert not delta_and_function(v1)
            assert not delta_and_function(v2)

            # TODO TODO TODO there is a delta too much here? run main and look at the 5th print paragraph, should look like this:
            """
            b.<d*>_[0,1]
            node b.<d*>_[0,1], 	volume: 1_(0, 1)(T) * Poly(1/6*T**3 + 1, T, domain='QQ') + 1_(1, inf)(T) * Poly(1/2*T**2 - 1/2*T + 7/6, T, domain='QQ') 	n = 4
            subnode b, 	volume: 1_(0, inf)(T) * Poly(1, T, domain='ZZ') 	n = 1
            subnode <d*>_[0,1], 	volume: 1_(0, 1)(T) * Poly(1/2*T**2, T, domain='QQ') + 1 delta(T), 	n = 3
            concat node with n=4
            """

            # if v1 and v2:
                # print(node.getText())
                # debug tests
                # highlight_node(vis,str(node.expr(0)),f"i = {i}")
                # highlight_node(vis,str(node.expr(1)),f"n-i = {n-i}")


                # intermediate_poly = continuous_convolution(v1, v2)
                # print(intermediate_poly)

                # print(f"node {node.getText()}, \tvolume: {intermediate_poly} \tn = {n}")
                # print(f"subnode {node.expr(0).getText()}, \tvolume: {v1} \tn = {i}")
                # print(f"subnode {node.expr(1).getText()}, \tvolume: {v2}, \tn = {n - 1}")
                # print(f"concat node with n={n}\n")
                # test = 2

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
            n = -1

        # Otherwise it is the zero poly and gets the other stuff added
        else:
            out = VolumePoly()

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
            v1 = slice_volume(expr, i, vis=vis, debug_mode=debug_mode, debug_container=debug_container)
            v2 = slice_volume(node, n - i, vis=vis, debug_mode=debug_mode, debug_container=debug_container)

            # v1.fancy_print()
            # v1.plot()
            # v2.fancy_print()
            # v2.plot()

            intermediate_poly = continuous_convolution(v1, v2)


            # this is a bit of a hack - but we need to ensure that in the kleene recursion no delta is added.
            # if n-i == 0:
            #     v2.delta = False



            assert not delta_and_function(intermediate_poly)
            assert not delta_and_function(v1)
            assert not delta_and_function(v2)


            # if v1 and v2:
                # print(node.getText())
                # debug tests
                # highlight_node(vis,str(node.expr(0)),f"i = {i}")
                # highlight_node(vis,str(node.expr(1)),f"n-i = {n-i}")
                # print(intermediate_poly)
                # print(f"node {node.getText()}, \tvolume: {intermediate_poly} \tn = {n}")
                # print(f"subnode {node.expr().getText()}, \tvolume: {v1}, \tn = {i}")
                # print(f"Kleene subnode {node.getText()}, \tvolume: {v2} \tn = {n-i}")
                # print(f"kleene node with n={n}\n")
                # test = 2

            out += intermediate_poly

            assert not delta_and_function(out)

            # note that we always return 0 for n==0 above, and mathematically assume that the empty word is not in expr
            #  so we do not have the problematic case with blowup (i == 0 on paper)

    else:
        raise Exception("Bad state.")

    out.exp = node.getText()
    out.n = n

    # if cache:
    #     cache[(n,node)] = out

    # if debug_mode:
        # print(f"n = {n}\t\t node = {node.getText()}\t\t poly = {out}")
        #
        # print(f"node = {node_text}, n = {n}")
        # highlight_node(vis, str(node), comment=f"n = {n}, p/T) = {out}")

    # cond = isinstance(node, )
    # assert not cond or out.is_cont(), "Encountered a VolumePoly that should be continuous but isn't."

    assert not delta_and_function(out)


    return out # this is the standard output


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