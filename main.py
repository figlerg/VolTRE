# for now try to generate the multiset of intervals automatically
from antlr4 import FileStream, CommonTokenStream

from parse.SyntaxError import HardSyntaxErrorStrategy
from parse.TRELexer import TRELexer
from parse.TREParser import TREParser

from os.path import join, curdir
from os import listdir

from slice_volume import slice_volume

input_stream = FileStream(join('parse', 'test_spec.txt'))
lexer = TRELexer(input_stream)
stream = CommonTokenStream(lexer)
parser = TREParser(stream)
parser._errHandler = HardSyntaxErrorStrategy()
ctx = parser.expr()

n = 6

V = slice_volume(ctx, n, debug_mode=False)  # debug mode generates files in vis_cache

print(V)
V.plot()