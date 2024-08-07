# Generated from C:/Users/Felix/PycharmProjects/VolTRE/parse/TRE.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,20,72,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,1,0,1,0,1,0,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,5,1,31,8,1,10,1,12,1,34,9,1,1,1,1,1,1,1,1,1,3,1,40,8,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,1,55,8,1,10,1,12,1,
        58,9,1,1,2,1,2,1,2,1,2,1,2,1,2,1,3,1,3,1,4,1,4,1,4,1,4,1,4,0,1,2,
        5,0,2,4,6,8,0,0,76,0,10,1,0,0,0,2,39,1,0,0,0,4,59,1,0,0,0,6,65,1,
        0,0,0,8,67,1,0,0,0,10,11,3,2,1,0,11,12,5,0,0,1,12,1,1,0,0,0,13,14,
        6,1,-1,0,14,40,5,16,0,0,15,40,3,6,3,0,16,17,5,1,0,0,17,18,3,2,1,
        0,18,19,5,2,0,0,19,40,1,0,0,0,20,21,5,7,0,0,21,22,3,2,1,0,22,23,
        5,8,0,0,23,24,5,9,0,0,24,25,3,4,2,0,25,40,1,0,0,0,26,32,5,10,0,0,
        27,28,3,8,4,0,28,29,5,11,0,0,29,31,1,0,0,0,30,27,1,0,0,0,31,34,1,
        0,0,0,32,30,1,0,0,0,32,33,1,0,0,0,33,35,1,0,0,0,34,32,1,0,0,0,35,
        36,3,8,4,0,36,37,5,12,0,0,37,38,3,2,1,1,38,40,1,0,0,0,39,13,1,0,
        0,0,39,15,1,0,0,0,39,16,1,0,0,0,39,20,1,0,0,0,39,26,1,0,0,0,40,56,
        1,0,0,0,41,42,10,6,0,0,42,43,5,4,0,0,43,55,3,2,1,7,44,45,10,4,0,
        0,45,46,5,5,0,0,46,55,3,2,1,5,47,48,10,3,0,0,48,49,5,6,0,0,49,55,
        3,2,1,4,50,51,10,7,0,0,51,55,5,3,0,0,52,53,10,5,0,0,53,55,5,5,0,
        0,54,41,1,0,0,0,54,44,1,0,0,0,54,47,1,0,0,0,54,50,1,0,0,0,54,52,
        1,0,0,0,55,58,1,0,0,0,56,54,1,0,0,0,56,57,1,0,0,0,57,3,1,0,0,0,58,
        56,1,0,0,0,59,60,5,13,0,0,60,61,5,18,0,0,61,62,5,11,0,0,62,63,5,
        18,0,0,63,64,5,14,0,0,64,5,1,0,0,0,65,66,5,17,0,0,66,7,1,0,0,0,67,
        68,3,6,3,0,68,69,5,15,0,0,69,70,3,6,3,0,70,9,1,0,0,0,4,32,39,54,
        56
    ]

class TREParser ( Parser ):

    grammarFileName = "TRE.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'*'", "'.'", "'+'", "'&'", 
                     "'<'", "'>'", "'_'", "'{'", "','", "'}'", "'['", "']'", 
                     "':'", "'EPS'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "EPS", "IDENTIFIER", "INT", "WS", "COMMENT" ]

    RULE_file = 0
    RULE_expr = 1
    RULE_interval = 2
    RULE_atomic_expr = 3
    RULE_rename_token = 4

    ruleNames =  [ "file", "expr", "interval", "atomic_expr", "rename_token" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    EPS=16
    IDENTIFIER=17
    INT=18
    WS=19
    COMMENT=20

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class FileContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(TREParser.ExprContext,0)


        def EOF(self):
            return self.getToken(TREParser.EOF, 0)

        def getRuleIndex(self):
            return TREParser.RULE_file




    def file_(self):

        localctx = TREParser.FileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_file)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 10
            self.expr(0)
            self.state = 11
            self.match(TREParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return TREParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class ConcatExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TREParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TREParser.ExprContext)
            else:
                return self.getTypedRuleContext(TREParser.ExprContext,i)



    class AtomicExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TREParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def atomic_expr(self):
            return self.getTypedRuleContext(TREParser.Atomic_exprContext,0)



    class PlusExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TREParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(TREParser.ExprContext,0)



    class UnionExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TREParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TREParser.ExprContext)
            else:
                return self.getTypedRuleContext(TREParser.ExprContext,i)



    class RenameExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TREParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def rename_token(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TREParser.Rename_tokenContext)
            else:
                return self.getTypedRuleContext(TREParser.Rename_tokenContext,i)

        def expr(self):
            return self.getTypedRuleContext(TREParser.ExprContext,0)



    class IntersectionExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TREParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TREParser.ExprContext)
            else:
                return self.getTypedRuleContext(TREParser.ExprContext,i)



    class KleeneExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TREParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(TREParser.ExprContext,0)



    class ParenExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TREParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(TREParser.ExprContext,0)



    class TimedExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TREParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(TREParser.ExprContext,0)

        def interval(self):
            return self.getTypedRuleContext(TREParser.IntervalContext,0)



    class EpsExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TREParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def EPS(self):
            return self.getToken(TREParser.EPS, 0)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = TREParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_expr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 39
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [16]:
                localctx = TREParser.EpsExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 14
                self.match(TREParser.EPS)
                pass
            elif token in [17]:
                localctx = TREParser.AtomicExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 15
                self.atomic_expr()
                pass
            elif token in [1]:
                localctx = TREParser.ParenExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 16
                self.match(TREParser.T__0)
                self.state = 17
                self.expr(0)
                self.state = 18
                self.match(TREParser.T__1)
                pass
            elif token in [7]:
                localctx = TREParser.TimedExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 20
                self.match(TREParser.T__6)
                self.state = 21
                self.expr(0)
                self.state = 22
                self.match(TREParser.T__7)
                self.state = 23
                self.match(TREParser.T__8)
                self.state = 24
                self.interval()
                pass
            elif token in [10]:
                localctx = TREParser.RenameExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 26
                self.match(TREParser.T__9)
                self.state = 32
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 27
                        self.rename_token()
                        self.state = 28
                        self.match(TREParser.T__10) 
                    self.state = 34
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

                self.state = 35
                self.rename_token()
                self.state = 36
                self.match(TREParser.T__11)
                self.state = 37
                self.expr(1)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 56
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,3,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 54
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
                    if la_ == 1:
                        localctx = TREParser.ConcatExprContext(self, TREParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 41
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 42
                        self.match(TREParser.T__3)
                        self.state = 43
                        self.expr(7)
                        pass

                    elif la_ == 2:
                        localctx = TREParser.UnionExprContext(self, TREParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 44
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 45
                        self.match(TREParser.T__4)
                        self.state = 46
                        self.expr(5)
                        pass

                    elif la_ == 3:
                        localctx = TREParser.IntersectionExprContext(self, TREParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 47
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 48
                        self.match(TREParser.T__5)
                        self.state = 49
                        self.expr(4)
                        pass

                    elif la_ == 4:
                        localctx = TREParser.KleeneExprContext(self, TREParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 50
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 51
                        self.match(TREParser.T__2)
                        pass

                    elif la_ == 5:
                        localctx = TREParser.PlusExprContext(self, TREParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 52
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 53
                        self.match(TREParser.T__4)
                        pass

             
                self.state = 58
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class IntervalContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self, i:int=None):
            if i is None:
                return self.getTokens(TREParser.INT)
            else:
                return self.getToken(TREParser.INT, i)

        def getRuleIndex(self):
            return TREParser.RULE_interval




    def interval(self):

        localctx = TREParser.IntervalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_interval)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 59
            self.match(TREParser.T__12)
            self.state = 60
            self.match(TREParser.INT)
            self.state = 61
            self.match(TREParser.T__10)
            self.state = 62
            self.match(TREParser.INT)
            self.state = 63
            self.match(TREParser.T__13)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Atomic_exprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(TREParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return TREParser.RULE_atomic_expr




    def atomic_expr(self):

        localctx = TREParser.Atomic_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_atomic_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 65
            self.match(TREParser.IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Rename_tokenContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def atomic_expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TREParser.Atomic_exprContext)
            else:
                return self.getTypedRuleContext(TREParser.Atomic_exprContext,i)


        def getRuleIndex(self):
            return TREParser.RULE_rename_token




    def rename_token(self):

        localctx = TREParser.Rename_tokenContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_rename_token)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 67
            self.atomic_expr()
            self.state = 68
            self.match(TREParser.T__14)
            self.state = 69
            self.atomic_expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 5)
         




