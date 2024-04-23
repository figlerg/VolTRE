from antlr4 import FileStream, CommonTokenStream

from parse.SyntaxError import HardSyntaxErrorStrategy
from parse.TREParser import TREParser
from math import inf, floor, ceil

"""
The volume of a TRE in terms of overall duration T is always a piecewise polynomial:
p(T) = sum   p_I(T)   1_I(T)

This visitor parses a TRE for the intervals on which the volume functions are defined.
I will probably make it into a visitor that directly calculates intervals AND the respective polynomial since it is 
easier than separately.
"""


# selfmade recursion
def generate_intervals(node:TREParser.ExprContext, n):
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
        for i in range(n+1):

            # continuous convolution
            out += multiset_interval_convolution(generate_intervals(node.expr(0), i), generate_intervals(node.expr(1), n-i))

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

        for i in range(0, n+1):

            # this is the case where no intervals survive, since V(e, i) is 0 everywhere.
            if i == 0:
                continue
            # this is the case where we simply take the expr intervals, since V(e*, 0) is the dirac and works as unit
            if i == n:
                out += generate_intervals(expr, n)


            # continuous convolution - unfolding one e from e*
            out += multiset_interval_convolution(generate_intervals(expr, i), generate_intervals(node, n-i))

            # note that we always return 0 for n==0 above, and mathematically assume that the empty word is not in expr
            #  so we do not have the problematic case with blowup (i == 0 on paper)

    else:
        raise Exception("Bad state.")

    return out



def check_int(interval):
    assert len(interval) == 2, "Intervals are not two-valued?"
    assert interval[0] < interval[1], "Intervals are not correctly ordered?"


# I represent intervals as 2-value lists for now. As utility, define the intersection:
def intersect(int1, int2):
    check_int(int1)
    check_int(int2)

    a1, b1 = int1[0], int1[1]
    a2, b2 = int2[0], int2[1]

    if b1 < a2 or b2 < a1:
        return None
    else:
        return [max(a1, a2),  min(b1, b2)]

def length(interval):
    check_int(interval)

    return interval[1] - interval[0]

def interval_convolution(int1, int2):
    check_int(int1)
    check_int(int2)


    a1, b1 = int1[0], int1[1]
    a2, b2 = int2[0], int2[1]
    l1, l2 = length(int1), length(int2)

    if l1 == l2:
        # in this case one of the intervals would be a singleton, so we just need to consider the two intervals with
        # interior points.
        l = l1
        return [[a1 + a2, a1 + a2 + l],
                [a1 + a2 + l, b1 + b2]]

    else:
        return [[a1 + a2, a1 + a2 + min(l1, l2)],
                [a1 + a2, a1 + a2 + max(l1, l2)],
                [a1 + a2 + max(l1, l2), b1 + b2]]


def multiset_interval_convolution(intervals1:list ,intervals2:list):
    # takes to interval lists and returns all the intervals from the convolution of the two

    out = []

    for int1 in intervals1:
        for int2 in intervals2:
            out += interval_convolution(int1, int2)

    return out


if __name__ == '__main__':

    from parse.TRELexer import TRELexer
    from parse.TREParser import TREParser

    from os.path import join, curdir
    from os import listdir

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

    print(generate_intervals(ctx, 5))



    # visitor = IntervalVisitor()
    # intervals = visitor.visit(ctx)
    #
    # print(f"final output: {intervals}")