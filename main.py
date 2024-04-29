# for now try to generate the multiset of intervals automatically
from antlr4 import FileStream, CommonTokenStream

from parse.IntervalVisitor import generate_intervals
from parse.SyntaxError import HardSyntaxErrorStrategy
from parse.TRELexer import TRELexer
from parse.TREParser import TREParser

from os.path import join, curdir
from os import listdir



input_stream = FileStream(join('parse', 'test.txt'))
lexer = TRELexer(input_stream)
stream = CommonTokenStream(lexer)
parser = TREParser(stream)
parser._errHandler = HardSyntaxErrorStrategy()
ctx = parser.expr()

print(generate_intervals(ctx, 2))
