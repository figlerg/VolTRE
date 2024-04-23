# for now try to generate the multiset of intervals automatically
from antlr4 import FileStream, CommonTokenStream

from parse.IntervalVisitor import generate_intervals
from parse.SyntaxError import HardSyntaxErrorStrategy
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

print(generate_intervals(ctx, 1))
