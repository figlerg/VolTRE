# from antlr4 import *
# from antlr4.error.ErrorStrategy import BailErrorStrategy
#
#
#
# # this actually throws if parser encounters invalid syntax and gives some error message.
# # inspired by https://stackoverflow.com/questions/60263601/how-can-i-fail-on-first-syntax-error-in-a-python-antlr-generated-parser-while-ke
# class HardSyntaxErrorStrategy(BailErrorStrategy):
#     def recover(self, recognizer: Parser, e: RecognitionException):
#         recognizer._errHandler.reportError(recognizer, e)
#         super().recover(recognizer, e)





# parse/SyntaxError.py

from antlr4 import Parser, RecognitionException, Token
from antlr4.error.ErrorStrategy import BailErrorStrategy
from antlr4.error.Errors import InputMismatchException


# parse/SyntaxError.py
import os
from antlr4 import Parser, RecognitionException, Token
from antlr4.error.ErrorStrategy import BailErrorStrategy
from antlr4.error.Errors import InputMismatchException

class TREParseError(Exception):
    pass

class HardSyntaxErrorStrategy(BailErrorStrategy):

    def _get_source_name(self, recognizer: Parser, token: Token) -> str:
        # wie vorher:
        if token is not None and hasattr(token, "source") and token.source:
            _, input_stream = token.source
            if input_stream is not None:
                name = getattr(input_stream, "name", None) or getattr(input_stream, "sourceName", None)
                if name:
                    # NEU: relative → absolut
                    if not os.path.isabs(name):
                        name = os.path.abspath(name)
                    return name

        stream = recognizer.getInputStream()
        name = getattr(stream, "name", None) or getattr(stream, "sourceName", None)
        if name:
            if not os.path.isabs(name):
                name = os.path.abspath(name)
            return name

        return "<input>"

    # Rest wie gehabt ...
    def _format_message(self, recognizer: Parser, e: Exception, token: Token) -> str:
        if isinstance(e, InputMismatchException):
            expected = e.getExpectedTokens().toString(
                recognizer.literalNames, recognizer.symbolicNames
            )
            text = token.text
            if text is None:
                text = "<EOF>" if token.type == Token.EOF else "<no text>"
            return f"mismatched input {text!r} expecting {expected}"
        if e.args:
            return str(e.args[0])
        return e.__class__.__name__

    def _raise(self, recognizer: Parser, e: Exception):
        token = getattr(e, "offendingToken", None) or recognizer.getCurrentToken()
        line = getattr(token, "line", 0)
        col = getattr(token, "column", 0)
        source = self._get_source_name(recognizer, token)
        msg = self._format_message(recognizer, e, token)
        pretty_msg = f'\n  File "{source}", line {line}\n    {msg} (col {col})'
        raise TREParseError(pretty_msg) from e

    def recover(self, recognizer: Parser, e: RecognitionException):
        self._raise(recognizer, e)

    def recoverInline(self, recognizer: Parser):
        e = InputMismatchException(recognizer)
        self._raise(recognizer, e)

    def sync(self, recognizer: Parser):
        return
