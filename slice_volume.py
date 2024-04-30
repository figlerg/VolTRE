from math import inf

import matplotlib.pyplot as plt
from antlr4 import FileStream, CommonTokenStream
from sympy import Piecewise, poly
from sympy.abc import T, t

from VolumePoly import VolumePoly
from parse.SyntaxError import HardSyntaxErrorStrategy
from parse.TREParser import TREParser


def slice_volume(node: TREParser.ExprContext, n, cache:dict=None):
    assert n >= 0, "Recursion bug."

    if not cache:
        cache = dict()

    if cache and (n,node) in cache:
        return cache[(n,node)]

    if n == 0:
        # TODO check for deltas? probably by asking whether the node accepts epsilon
        out = VolumePoly([], [])

    elif isinstance(node, TREParser.AtomicExprContext):
        if n == 1:
            ints = [(0, inf), ]
            polys = [poly(1, T)]  # the only way I found for representing constant functions
            out = VolumePoly(ints, polys)
        else:
            out = VolumePoly()  # 0 poly if we have more or less letters

    elif isinstance(node, TREParser.ParenExprContext):
        expr = node.expr()
        out = slice_volume(expr, n, cache=cache)

    elif isinstance(node, TREParser.UnionExprContext):
        # the plus is overloaded: normal addition of piecewise polynomials
        out = slice_volume(node.expr(0), n, cache=cache) + slice_volume(node.expr(1), n, cache=cache)

    elif isinstance(node, TREParser.ConcatExprContext):
        out = VolumePoly()  # the zero poly

        # discrete convolution
        for i in range(n + 1):
            # continuous convolution - * is overloaded with convolution of two piecewise poly objects
            out += slice_volume(node.expr(0), i, cache=cache) * slice_volume(node.expr(1), n - i, cache=cache)

    elif isinstance(node, TREParser.TimedExprContext):
        child_volume = slice_volume(node.expr(), n, cache=cache)
        restriction_interval = (int(node.interval().INT(0).getText()), int(node.interval().INT(1).getText()))

        child_volume.time_restriction(restriction_interval)  # does the interval intersection in place for all intervals

        out = child_volume

    elif isinstance(node, TREParser.KleeneExprContext):
        expr = node.expr()

        # TODO here i have a problem to do the fast squaring recursion method...
        #   I never really know how how many letters exp can have, so the base case depends on that.
        #   For example, if i take <aa>_[0,1]* and if I look at V_1 here, it will be zero.
        #   One solution would be to look how deep the tree goes (how many letters to expect here),
        #   but that only works if there is no kleene below...

        out = VolumePoly()  # the zero poly

        for i in range(0, n + 1):

            # this is the case where no intervals survive, since V(e, i) is 0 everywhere.
            if i == 0:
                continue
            # this is the case where we simply take the expr intervals, since V(e*, 0) is the dirac and works as unit
            if i == n:
                out += slice_volume(expr, n, cache=cache)

            intermediate_poly = slice_volume(expr, i, cache=cache) * slice_volume(node, n - i, cache=cache) # TODO visualize these together with the syntax tree

            # continuous convolution - unfolding one e from e*. TODO fast squaring would have to happen with two "node" inputs, right? but what is the base case?
            out += intermediate_poly

            # note that we always return 0 for n==0 above, and mathematically assume that the empty word is not in expr
            #  so we do not have the problematic case with blowup (i == 0 on paper)

    else:
        raise Exception("Bad state.")

    out.exp = ctx.getText()
    out.n = n

    cache[(n,node)] = out

    return out



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

    import time


    case = 1

    # here i try to profile the computation for varying n
    if case == 0:
        n_max = 12

        ts = []
        for n in range(n_max):
            a = time.time()
            test = slice_volume(ctx, n)
            b = time.time()

            print(f"Computation complete for n = {n} and exp = {ctx.getText()}.\n"
              f"Elapsed time = {b-a}s")
            ts.append(b-a)

            print(test)

            test.plot()

        plt.plot(ts)
        plt.show()

    # TODO here I look at suspicious case with discontinuity. Is it a bug? Very likely, since it only happens for
    #  rec(1)*rec(5). maybe something like overflow?
    if case == 1:
        n = 6
        a = time.time()
        test = slice_volume(ctx, n)
        b = time.time()

        print(f"Computation complete for n = {n} and exp = {ctx.getText()}.\n"
              f"Elapsed time = {b - a}s")

        test.plot()

        a = time.time()
        n1 = 3
        n2 = 3
        test1 = slice_volume(ctx, n1)
        test2 = slice_volume(ctx, n2)
        test2 = test1 * test2
        test2.n = f'{n1} + {n2}'
        test2.exp = ctx.expr().getText() + '.' + ctx.getText()
        b = time.time()

        print(f"Computation 2 complete for n = {n1} + {n2} and exp = {test2.exp}.\n"
                      f"Elapsed time = {b - a}s")

        test2.plot()


        a = time.time()
        n1 = 2
        n2 = 4
        testa = slice_volume(ctx, n1)
        testb = slice_volume(ctx, n2)
        test3 = testa * testb
        test3.n = f'{n1} + {n2}'
        test3.exp = ctx.expr().getText() + '.' + ctx.getText()
        b = time.time()

        print(f"Computation 3 complete for n = {n1} + {n2} and exp = {test3.exp}.\n"
                      f"Elapsed time = {b - a}s")

        print(f"test2 == test3: {test2 == test3}")

        test3.plot()