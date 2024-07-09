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
        4,1,19,54,2,0,7,0,2,1,7,1,2,2,7,2,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,
        0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,3,0,26,8,0,1,0,1,0,
        1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,5,0,41,8,0,10,0,12,0,
        44,9,0,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,2,0,1,0,3,0,2,4,0,0,58,
        0,25,1,0,0,0,2,45,1,0,0,0,4,51,1,0,0,0,6,7,6,0,-1,0,7,26,3,4,2,0,
        8,9,5,1,0,0,9,10,3,0,0,0,10,11,5,2,0,0,11,26,1,0,0,0,12,13,5,7,0,
        0,13,14,3,0,0,0,14,15,5,8,0,0,15,16,5,9,0,0,16,17,3,2,1,0,17,26,
        1,0,0,0,18,19,5,10,0,0,19,20,3,4,2,0,20,21,5,11,0,0,21,22,3,4,2,
        0,22,23,5,12,0,0,23,24,3,0,0,1,24,26,1,0,0,0,25,6,1,0,0,0,25,8,1,
        0,0,0,25,12,1,0,0,0,25,18,1,0,0,0,26,42,1,0,0,0,27,28,10,6,0,0,28,
        29,5,4,0,0,29,41,3,0,0,7,30,31,10,4,0,0,31,32,5,5,0,0,32,41,3,0,
        0,5,33,34,10,3,0,0,34,35,5,6,0,0,35,41,3,0,0,4,36,37,10,7,0,0,37,
        41,5,3,0,0,38,39,10,5,0,0,39,41,5,5,0,0,40,27,1,0,0,0,40,30,1,0,
        0,0,40,33,1,0,0,0,40,36,1,0,0,0,40,38,1,0,0,0,41,44,1,0,0,0,42,40,
        1,0,0,0,42,43,1,0,0,0,43,1,1,0,0,0,44,42,1,0,0,0,45,46,5,13,0,0,
        46,47,5,17,0,0,47,48,5,14,0,0,48,49,5,17,0,0,49,50,5,15,0,0,50,3,
        1,0,0,0,51,52,5,16,0,0,52,5,1,0,0,0,3,25,40,42
    ]

class TREParser ( Parser ):

    grammarFileName = "TRE.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'*'", "'.'", "'+'", "'&'", 
                     "'<'", "'>'", "'_'", "'{'", "':'", "'}'", "'['", "','", 
                     "']'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "IDENTIFIER", "INT", "WS", "COMMENT" ]

    RULE_expr = 0
    RULE_interval = 1
    RULE_atomic_expr = 2

    ruleNames =  [ "expr", "interval", "atomic_expr" ]

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
    IDENTIFIER=16
    INT=17
    WS=18
    COMMENT=19

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




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


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConcatExpr" ):
                return visitor.visitConcatExpr(self)
            else:
                return visitor.visitChildren(self)


    class AtomicExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TREParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def atomic_expr(self):
            return self.getTypedRuleContext(TREParser.Atomic_exprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtomicExpr" ):
                return visitor.visitAtomicExpr(self)
            else:
                return visitor.visitChildren(self)


    class PlusExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TREParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(TREParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPlusExpr" ):
                return visitor.visitPlusExpr(self)
            else:
                return visitor.visitChildren(self)


    class UnionExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TREParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TREParser.ExprContext)
            else:
                return self.getTypedRuleContext(TREParser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnionExpr" ):
                return visitor.visitUnionExpr(self)
            else:
                return visitor.visitChildren(self)


    class RenameExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TREParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def atomic_expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TREParser.Atomic_exprContext)
            else:
                return self.getTypedRuleContext(TREParser.Atomic_exprContext,i)

        def expr(self):
            return self.getTypedRuleContext(TREParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRenameExpr" ):
                return visitor.visitRenameExpr(self)
            else:
                return visitor.visitChildren(self)


    class IntersectionExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TREParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TREParser.ExprContext)
            else:
                return self.getTypedRuleContext(TREParser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIntersectionExpr" ):
                return visitor.visitIntersectionExpr(self)
            else:
                return visitor.visitChildren(self)


    class KleeneExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TREParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(TREParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitKleeneExpr" ):
                return visitor.visitKleeneExpr(self)
            else:
                return visitor.visitChildren(self)


    class ParenExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TREParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(TREParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenExpr" ):
                return visitor.visitParenExpr(self)
            else:
                return visitor.visitChildren(self)


    class TimedExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TREParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(TREParser.ExprContext,0)

        def interval(self):
            return self.getTypedRuleContext(TREParser.IntervalContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTimedExpr" ):
                return visitor.visitTimedExpr(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = TREParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 0
        self.enterRecursionRule(localctx, 0, self.RULE_expr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 25
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [16]:
                localctx = TREParser.AtomicExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 7
                self.atomic_expr()
                pass
            elif token in [1]:
                localctx = TREParser.ParenExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 8
                self.match(TREParser.T__0)
                self.state = 9
                self.expr(0)
                self.state = 10
                self.match(TREParser.T__1)
                pass
            elif token in [7]:
                localctx = TREParser.TimedExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 12
                self.match(TREParser.T__6)
                self.state = 13
                self.expr(0)
                self.state = 14
                self.match(TREParser.T__7)
                self.state = 15
                self.match(TREParser.T__8)
                self.state = 16
                self.interval()
                pass
            elif token in [10]:
                localctx = TREParser.RenameExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 18
                self.match(TREParser.T__9)
                self.state = 19
                self.atomic_expr()
                self.state = 20
                self.match(TREParser.T__10)
                self.state = 21
                self.atomic_expr()
                self.state = 22
                self.match(TREParser.T__11)
                self.state = 23
                self.expr(1)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 42
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 40
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = TREParser.ConcatExprContext(self, TREParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 27
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 28
                        self.match(TREParser.T__3)
                        self.state = 29
                        self.expr(7)
                        pass

                    elif la_ == 2:
                        localctx = TREParser.UnionExprContext(self, TREParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 30
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 31
                        self.match(TREParser.T__4)
                        self.state = 32
                        self.expr(5)
                        pass

                    elif la_ == 3:
                        localctx = TREParser.IntersectionExprContext(self, TREParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 33
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 34
                        self.match(TREParser.T__5)
                        self.state = 35
                        self.expr(4)
                        pass

                    elif la_ == 4:
                        localctx = TREParser.KleeneExprContext(self, TREParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 36
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 37
                        self.match(TREParser.T__2)
                        pass

                    elif la_ == 5:
                        localctx = TREParser.PlusExprContext(self, TREParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 38
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 39
                        self.match(TREParser.T__4)
                        pass

             
                self.state = 44
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInterval" ):
                return visitor.visitInterval(self)
            else:
                return visitor.visitChildren(self)




    def interval(self):

        localctx = TREParser.IntervalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_interval)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 45
            self.match(TREParser.T__12)
            self.state = 46
            self.match(TREParser.INT)
            self.state = 47
            self.match(TREParser.T__13)
            self.state = 48
            self.match(TREParser.INT)
            self.state = 49
            self.match(TREParser.T__14)
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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtomic_expr" ):
                return visitor.visitAtomic_expr(self)
            else:
                return visitor.visitChildren(self)




    def atomic_expr(self):

        localctx = TREParser.Atomic_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_atomic_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 51
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
        self._predicates[0] = self.expr_sempred
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
         




