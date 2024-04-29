from math import inf

from antlr4 import FileStream, CommonTokenStream
from sympy import Piecewise

from VolumePoly import VolumePoly
from parse.SyntaxError import HardSyntaxErrorStrategy
from parse.TREParser import TREParser


def slice_volume(node: TREParser.ExprContext, n):
    assert n >= 0, "Recursion bug."

    if n == 0:
        # TODO check for deltas? probably by asking whether the node accepts epsilon
        out = VolumePoly([], [])

    elif isinstance(node, TREParser.AtomicExprContext):
        ints = [(0, inf), ] if n == 1 else []
        polys = [Piecewise((1, True)), ]  # the only way I found for representing constant functions
        out = VolumePoly(ints, polys)

    elif isinstance(node, TREParser.ParenExprContext):
        expr = node.expr()
        out = slice_volume(expr, n)

    elif isinstance(node, TREParser.UnionExprContext):
        # the plus is overloaded: normal addition of piecewise polynomials
        out = slice_volume(node.expr(0), n) + slice_volume(node.expr(1), n)

    elif isinstance(node, TREParser.ConcatExprContext):
        out = VolumePoly()  # the zero poly

        # discrete convolution
        for i in range(n + 1):
            # continuous convolution - * is overloaded with convolution of two piecewise poly objects
            out += slice_volume(node.expr(0), i) * slice_volume(node.expr(1), n - i)

    elif isinstance(node, TREParser.TimedExprContext):
        child_volume = slice_volume(node.expr(), n)
        restriction_interval = (int(node.interval().INT(0).getText()), int(node.interval().INT(1).getText()))

        child_volume.time_restriction(restriction_interval)  # does the interval intersection in place for all intervals

        out = child_volume

    elif isinstance(node, TREParser.KleeneExprContext):
        expr = node.expr()

        out = VolumePoly()  # the zero poly

        for i in range(0, n + 1):

            # this is the case where no intervals survive, since V(e, i) is 0 everywhere.
            if i == 0:
                continue
            # this is the case where we simply take the expr intervals, since V(e*, 0) is the dirac and works as unit
            if i == n:
                out += slice_volume(expr, n)

            # continuous convolution - unfolding one e from e*
            out += slice_volume(expr, i) * slice_volume(node, n - i)

            # note that we always return 0 for n==0 above, and mathematically assume that the empty word is not in expr
            #  so we do not have the problematic case with blowup (i == 0 on paper)

    else:
        raise Exception("Bad state.")

    out.exp = ctx.getText()
    out.n = n

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

    n = 1
    test = slice_volume(ctx, n)

    print(test)

    test.plot(n)
