from antlr4 import FileStream, CommonTokenStream

from TREVisitor import TREVisitor
from parse.SyntaxError import HardSyntaxErrorStrategy
from parse.TREParser import TREParser
from math import inf


"""
The volume of a TRE in terms of overall duration T is always a piecewise polynomial:
p(T) = sum   p_I(T)   1_I(T)

This visitor parses a TRE for the intervals on which the volume functions are defined.
I will probably make it into a visitor that directly calculates intervals AND the respective polynomial since it is 
easier than separately.
"""




class IntervalVisitor(TREVisitor):
    """
    - Intervals are 2-valued lists
    - Visitor returns list of lists... basically a multiset of intervals
    """


    def generate_intervals(self, n):


    def visitAtomicExpr(self, ctx:TREParser.AtomicExprContext):
        return [[0, inf], ]

    def visitParenExpr(self, ctx:TREParser.ParenExprContext):
        return self.visit(ctx.expr())

    def visitInterval(self, ctx:TREParser.IntervalContext):

        a = int(ctx.INT(0).getText()) # surely not the canonical way to get this
        b = int(ctx.INT(1).getText()) # surely not the canonical way to get this

        return [a,b]

    def visitUnionExpr(self, ctx:TREParser.UnionExprContext):
        return self.visit(ctx.expr(0)) + self.visit(ctx.expr(1))

    def visitConcatExpr(self, ctx:TREParser.ConcatExprContext):
        child_intervals1 = self.visit(ctx.expr(0))  # this is the list of intervals we get from left expression
        child_intervals2 = self.visit(ctx.expr(1))  # this is the list of intervals we get from right expression



        return multiset_interval_convolution(child_intervals1, child_intervals2)

    def visitTimedExpr(self, ctx:TREParser.TimedExprContext):
        child_intervals = self.visit(ctx.expr())  # this is the list of intervals we get from the expression
        restriction_interval = self.visit(ctx.interval())

        intervals = []

        for interval in child_intervals:
            intersection = intersect(interval, restriction_interval)

            if intersection:
                intervals.append(intersection)

        return intervals

    def visitKleeneExpr(self, ctx:TREParser.KleeneExprContext):
        # return self.BoundedKleene(self.visit(ctx.expr()), self.n)

        # TODO TODO TODO something here is not right... the intervals only make sense when the word length is taken
        #  into account... n = 2 means "a" has volume 0, no intervals needed. So basically we should bake the n into
        #  the visitor, decrease it accordingly in concat and kleene, and then recombine it.

    def BoundedKleene(self, exp_intervals, n):
        return multiset_interval_convolution(exp_intervals, self.BoundedKleene(exp_intervals, self.n - 1))








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

    return interval[1] - interval[2]

def interval_convolution(int1, int2):

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

    print("tests:")
    print(test1 := intersect([0, inf], [1,3]))
    print(test2 := intersect([2, 3], [0,1]))
    try:
        intersect([2, 3, 1], [0,1])
    except AssertionError:
        print('Failed successfully on [2, 3, 1], [0,1] because of bad interval input.')

    print(test4 := intersect([1, 3], [2 , 4]))


    input_stream = FileStream(join('parse', 'test.txt'))
    lexer = TRELexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = TREParser(stream)
    parser._errHandler = HardSyntaxErrorStrategy()
    ctx = parser.expr()

    visitor = IntervalVisitor()
    intervals = visitor.visit(ctx)

    print(f"final output: {intervals}")