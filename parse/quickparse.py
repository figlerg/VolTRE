from antlr4 import FileStream, CommonTokenStream, InputStream

from parse.SyntaxError import HardSyntaxErrorStrategy
from parse.TRELexer import TRELexer
from parse.TREParser import TREParser


def quickparse(parse_input, string=False) -> TREParser.ExprContext:
    """
    Generates the syntax tree from a string. The standard usage is
        quickparse(path),
    but you can also use the string directly like this:
        quickparse(input_string, string=True).
    :param parse_input: Path or string.
    :param string: Flag for string mode.
    :return: ANTLR4 syntax tree (a TREParser.ExprContext object).
    """

    if not string:
        input_stream = FileStream(parse_input)
    else:
        input_stream = InputStream(parse_input)

    lexer = TRELexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = TREParser(stream)
    parser._errHandler = HardSyntaxErrorStrategy()
    ctx = parser.expr()

    return ctx

