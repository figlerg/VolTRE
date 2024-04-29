from antlr4 import FileStream, CommonTokenStream

from parse.SyntaxError import HardSyntaxErrorStrategy
from parse.TREParser import TREParser
from math import inf

from parse.misc import intersect, multiset_interval_convolution

"""
The volume of a TRE in terms of overall duration T is always a piecewise polynomial:
p(T) = sum   p_I(T)   1_I(T)

I disliked the antlr visitor, so I simply made a recursion on the syntax tree.
"""






# selfmade recursion skeleton: just the intervals
def generate_intervals(node: TREParser.ExprContext, n):
    assert n >= 0, "Recursion bug."

    if n == 0:
        return []

    elif isinstance(node, TREParser.AtomicExprContext):
        out = [[0, inf], ] if n == 1 else []

    elif isinstance(node, TREParser.ParenExprContext):
        expr = node.expr()
        out = generate_intervals(expr, n)

    elif isinstance(node, TREParser.UnionExprContext):
        out = generate_intervals(node.expr(0), n) + generate_intervals(node.expr(1), n)

    elif isinstance(node, TREParser.ConcatExprContext):
        out = []

        # discrete convolution
        for i in range(n + 1):
            # continuous convolution
            out += multiset_interval_convolution(generate_intervals(node.expr(0), i),
                                                 generate_intervals(node.expr(1), n - i))

    elif isinstance(node, TREParser.TimedExprContext):
        child_intervals = generate_intervals(node.expr(), n)
        restriction_interval = [int(node.interval().INT(0).getText()), int(node.interval().INT(1).getText())]

        out = []

        for interval in child_intervals:
            intersection = intersect(interval, restriction_interval)

            if intersection:
                out.append(intersection)

    elif isinstance(node, TREParser.KleeneExprContext):
        expr = node.expr()

        out = []

        for i in range(0, n + 1):

            # this is the case where no intervals survive, since V(e, i) is 0 everywhere.
            if i == 0:
                continue
            # this is the case where we simply take the expr intervals, since V(e*, 0) is the dirac and works as unit
            if i == n:
                out += generate_intervals(expr, n)

            # continuous convolution - unfolding one e from e*
            out += multiset_interval_convolution(generate_intervals(expr, i), generate_intervals(node, n - i))

            # note that we always return 0 for n==0 above, and mathematically assume that the empty word is not in expr
            #  so we do not have the problematic case with blowup (i == 0 on paper)

    else:
        raise Exception("Bad state.")

    return out


# TODO today:
#  - try out the fast squaring optimization
#  - try to find a way to handle the 2 variable polys
#  - develop the interval shortening method
#  - try to add polys to the code
#  - caching or dynamic programming algo so we don't do work twice


# I represent intervals as 2-value lists for now. As utility, define the intersection:


if __name__ == '__main__':
    from parse.TRELexer import TRELexer
    from parse.TREParser import TREParser

    from os.path import join

    # print("tests:")
    # print(test1 := intersect([0, inf], [1,3]))
    # print(test2 := intersect([2, 3], [0,1]))
    # try:
    #     intersect([2, 3, 1], [0,1])
    # except AssertionError:
    #     print('Failed successfully on [2, 3, 1], [0,1] because of bad interval input.')
    #
    # print(test4 := intersect([1, 3], [2 , 4]))

    input_stream = FileStream(join('parse', 'test.txt'))
    lexer = TRELexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = TREParser(stream)
    parser._errHandler = HardSyntaxErrorStrategy()
    ctx = parser.expr()

    print(generate_intervals(ctx, 2))


