# Generated from C:/Users/giglerf/PycharmProjects/VolTRE/parse/TRE.g4 by ANTLR 4.13.1
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
        4,1,21,68,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,1,0,1,0,1,0,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,1,29,
        8,1,10,1,12,1,32,9,1,1,1,1,1,1,1,1,1,3,1,38,8,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,1,53,8,1,10,1,12,1,56,9,1,
        1,2,1,2,1,2,1,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,0,1,2,4,0,2,4,6,0,1,
        2,0,17,17,19,19,73,0,8,1,0,0,0,2,37,1,0,0,0,4,57,1,0,0,0,6,63,1,
        0,0,0,8,9,3,2,1,0,9,10,5,0,0,1,10,1,1,0,0,0,11,12,6,1,-1,0,12,38,
        5,16,0,0,13,38,5,18,0,0,14,15,5,1,0,0,15,16,3,2,1,0,16,17,5,2,0,
        0,17,38,1,0,0,0,18,19,5,7,0,0,19,20,3,2,1,0,20,21,5,8,0,0,21,22,
        5,9,0,0,22,23,3,4,2,0,23,38,1,0,0,0,24,30,5,10,0,0,25,26,3,6,3,0,
        26,27,5,11,0,0,27,29,1,0,0,0,28,25,1,0,0,0,29,32,1,0,0,0,30,28,1,
        0,0,0,30,31,1,0,0,0,31,33,1,0,0,0,32,30,1,0,0,0,33,34,3,6,3,0,34,
        35,5,12,0,0,35,36,3,2,1,1,36,38,1,0,0,0,37,11,1,0,0,0,37,13,1,0,
        0,0,37,14,1,0,0,0,37,18,1,0,0,0,37,24,1,0,0,0,38,54,1,0,0,0,39,40,
        10,6,0,0,40,41,5,4,0,0,41,53,3,2,1,7,42,43,10,4,0,0,43,44,5,5,0,
        0,44,53,3,2,1,5,45,46,10,3,0,0,46,47,5,6,0,0,47,53,3,2,1,4,48,49,
        10,7,0,0,49,53,5,3,0,0,50,51,10,5,0,0,51,53,5,5,0,0,52,39,1,0,0,
        0,52,42,1,0,0,0,52,45,1,0,0,0,52,48,1,0,0,0,52,50,1,0,0,0,53,56,
        1,0,0,0,54,52,1,0,0,0,54,55,1,0,0,0,55,3,1,0,0,0,56,54,1,0,0,0,57,
        58,5,13,0,0,58,59,5,19,0,0,59,60,5,11,0,0,60,61,7,0,0,0,61,62,5,
        14,0,0,62,5,1,0,0,0,63,64,5,18,0,0,64,65,5,15,0,0,65,66,5,18,0,0,
        66,7,1,0,0,0,4,30,37,52,54
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
                      "EPS", "INF", "IDENTIFIER", "INT", "WS", "COMMENT" ]

    RULE_file = 0
    RULE_expr = 1
    RULE_interval = 2
    RULE_rename_token = 3

    ruleNames =  [ "file", "expr", "interval", "rename_token" ]

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
    INF=17
    IDENTIFIER=18
    INT=19
    WS=20
    COMMENT=21

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
            self.state = 8
            self.expr(0)
            self.state = 9
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

        def IDENTIFIER(self):
            return self.getToken(TREParser.IDENTIFIER, 0)


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
            self.state = 37
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [16]:
                localctx = TREParser.EpsExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 12
                self.match(TREParser.EPS)
                pass
            elif token in [18]:
                localctx = TREParser.AtomicExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 13
                self.match(TREParser.IDENTIFIER)
                pass
            elif token in [1]:
                localctx = TREParser.ParenExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 14
                self.match(TREParser.T__0)
                self.state = 15
                self.expr(0)
                self.state = 16
                self.match(TREParser.T__1)
                pass
            elif token in [7]:
                localctx = TREParser.TimedExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 18
                self.match(TREParser.T__6)
                self.state = 19
                self.expr(0)
                self.state = 20
                self.match(TREParser.T__7)
                self.state = 21
                self.match(TREParser.T__8)
                self.state = 22
                self.interval()
                pass
            elif token in [10]:
                localctx = TREParser.RenameExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 24
                self.match(TREParser.T__9)
                self.state = 30
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 25
                        self.rename_token()
                        self.state = 26
                        self.match(TREParser.T__10) 
                    self.state = 32
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

                self.state = 33
                self.rename_token()
                self.state = 34
                self.match(TREParser.T__11)
                self.state = 35
                self.expr(1)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 54
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,3,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 52
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
                    if la_ == 1:
                        localctx = TREParser.ConcatExprContext(self, TREParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 39
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 40
                        self.match(TREParser.T__3)
                        self.state = 41
                        self.expr(7)
                        pass

                    elif la_ == 2:
                        localctx = TREParser.UnionExprContext(self, TREParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 42
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 43
                        self.match(TREParser.T__4)
                        self.state = 44
                        self.expr(5)
                        pass

                    elif la_ == 3:
                        localctx = TREParser.IntersectionExprContext(self, TREParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 45
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 46
                        self.match(TREParser.T__5)
                        self.state = 47
                        self.expr(4)
                        pass

                    elif la_ == 4:
                        localctx = TREParser.KleeneExprContext(self, TREParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 48
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 49
                        self.match(TREParser.T__2)
                        pass

                    elif la_ == 5:
                        localctx = TREParser.PlusExprContext(self, TREParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 50
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 51
                        self.match(TREParser.T__4)
                        pass

             
                self.state = 56
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

        def INF(self):
            return self.getToken(TREParser.INF, 0)

        def getRuleIndex(self):
            return TREParser.RULE_interval




    def interval(self):

        localctx = TREParser.IntervalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_interval)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 57
            self.match(TREParser.T__12)
            self.state = 58
            self.match(TREParser.INT)
            self.state = 59
            self.match(TREParser.T__10)
            self.state = 60
            _la = self._input.LA(1)
            if not(_la==17 or _la==19):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 61
            self.match(TREParser.T__13)
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

        def IDENTIFIER(self, i:int=None):
            if i is None:
                return self.getTokens(TREParser.IDENTIFIER)
            else:
                return self.getToken(TREParser.IDENTIFIER, i)

        def getRuleIndex(self):
            return TREParser.RULE_rename_token




    def rename_token(self):

        localctx = TREParser.Rename_tokenContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_rename_token)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 63
            self.match(TREParser.IDENTIFIER)
            self.state = 64
            self.match(TREParser.T__14)
            self.state = 65
            self.match(TREParser.IDENTIFIER)
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
         




