from antlr4 import FileStream, CommonTokenStream

from parse.SyntaxError import HardSyntaxErrorStrategy
from parse.TRELexer import TRELexer
from parse.TREParser import TREParser
from os.path import join, curdir


def quickparse(path):
    input_stream = FileStream(path)
    lexer = TRELexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = TREParser(stream)
    parser._errHandler = HardSyntaxErrorStrategy()
    ctx = parser.expr()

    return ctx