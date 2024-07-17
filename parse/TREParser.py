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
        4,1,19,71,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,1,0,1,0,1,0,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,
        1,30,8,1,10,1,12,1,33,9,1,1,1,1,1,1,1,1,1,3,1,39,8,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,1,54,8,1,10,1,12,1,57,
        9,1,1,2,1,2,1,2,1,2,1,2,1,2,1,3,1,3,1,4,1,4,1,4,1,4,1,4,0,1,2,5,
        0,2,4,6,8,0,0,74,0,10,1,0,0,0,2,38,1,0,0,0,4,58,1,0,0,0,6,64,1,0,
        0,0,8,66,1,0,0,0,10,11,3,2,1,0,11,12,5,0,0,1,12,1,1,0,0,0,13,14,
        6,1,-1,0,14,39,3,6,3,0,15,16,5,1,0,0,16,17,3,2,1,0,17,18,5,2,0,0,
        18,39,1,0,0,0,19,20,5,7,0,0,20,21,3,2,1,0,21,22,5,8,0,0,22,23,5,
        9,0,0,23,24,3,4,2,0,24,39,1,0,0,0,25,31,5,10,0,0,26,27,3,8,4,0,27,
        28,5,11,0,0,28,30,1,0,0,0,29,26,1,0,0,0,30,33,1,0,0,0,31,29,1,0,
        0,0,31,32,1,0,0,0,32,34,1,0,0,0,33,31,1,0,0,0,34,35,3,8,4,0,35,36,
        5,12,0,0,36,37,3,2,1,1,37,39,1,0,0,0,38,13,1,0,0,0,38,15,1,0,0,0,
        38,19,1,0,0,0,38,25,1,0,0,0,39,55,1,0,0,0,40,41,10,6,0,0,41,42,5,
        4,0,0,42,54,3,2,1,7,43,44,10,4,0,0,44,45,5,5,0,0,45,54,3,2,1,5,46,
        47,10,3,0,0,47,48,5,6,0,0,48,54,3,2,1,4,49,50,10,7,0,0,50,54,5,3,
        0,0,51,52,10,5,0,0,52,54,5,5,0,0,53,40,1,0,0,0,53,43,1,0,0,0,53,
        46,1,0,0,0,53,49,1,0,0,0,53,51,1,0,0,0,54,57,1,0,0,0,55,53,1,0,0,
        0,55,56,1,0,0,0,56,3,1,0,0,0,57,55,1,0,0,0,58,59,5,13,0,0,59,60,
        5,17,0,0,60,61,5,11,0,0,61,62,5,17,0,0,62,63,5,14,0,0,63,5,1,0,0,
        0,64,65,5,16,0,0,65,7,1,0,0,0,66,67,3,6,3,0,67,68,5,15,0,0,68,69,
        3,6,3,0,69,9,1,0,0,0,4,31,38,53,55
    ]

class TREParser ( Parser ):

    grammarFileName = "TRE.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'*'", "'.'", "'+'", "'&'", 
                     "'<'", "'>'", "'_'", "'{'", "','", "'}'", "'['", "']'", 
                     "':'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "IDENTIFIER", "INT", "WS", "COMMENT" ]

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
    IDENTIFIER=16
    INT=17
    WS=18
    COMMENT=19

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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFile" ):
                return visitor.visitFile(self)
            else:
                return visitor.visitChildren(self)




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

        def rename_token(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TREParser.Rename_tokenContext)
            else:
                return self.getTypedRuleContext(TREParser.Rename_tokenContext,i)

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
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_expr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 38
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [16]:
                localctx = TREParser.AtomicExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 14
                self.atomic_expr()
                pass
            elif token in [1]:
                localctx = TREParser.ParenExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 15
                self.match(TREParser.T__0)
                self.state = 16
                self.expr(0)
                self.state = 17
                self.match(TREParser.T__1)
                pass
            elif token in [7]:
                localctx = TREParser.TimedExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 19
                self.match(TREParser.T__6)
                self.state = 20
                self.expr(0)
                self.state = 21
                self.match(TREParser.T__7)
                self.state = 22
                self.match(TREParser.T__8)
                self.state = 23
                self.interval()
                pass
            elif token in [10]:
                localctx = TREParser.RenameExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 25
                self.match(TREParser.T__9)
                self.state = 31
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 26
                        self.rename_token()
                        self.state = 27
                        self.match(TREParser.T__10) 
                    self.state = 33
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

                self.state = 34
                self.rename_token()
                self.state = 35
                self.match(TREParser.T__11)
                self.state = 36
                self.expr(1)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 55
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,3,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 53
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
                    if la_ == 1:
                        localctx = TREParser.ConcatExprContext(self, TREParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 40
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 41
                        self.match(TREParser.T__3)
                        self.state = 42
                        self.expr(7)
                        pass

                    elif la_ == 2:
                        localctx = TREParser.UnionExprContext(self, TREParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 43
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 44
                        self.match(TREParser.T__4)
                        self.state = 45
                        self.expr(5)
                        pass

                    elif la_ == 3:
                        localctx = TREParser.IntersectionExprContext(self, TREParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 46
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 47
                        self.match(TREParser.T__5)
                        self.state = 48
                        self.expr(4)
                        pass

                    elif la_ == 4:
                        localctx = TREParser.KleeneExprContext(self, TREParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 49
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 50
                        self.match(TREParser.T__2)
                        pass

                    elif la_ == 5:
                        localctx = TREParser.PlusExprContext(self, TREParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 51
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 52
                        self.match(TREParser.T__4)
                        pass

             
                self.state = 57
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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInterval" ):
                return visitor.visitInterval(self)
            else:
                return visitor.visitChildren(self)




    def interval(self):

        localctx = TREParser.IntervalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_interval)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 58
            self.match(TREParser.T__12)
            self.state = 59
            self.match(TREParser.INT)
            self.state = 60
            self.match(TREParser.T__10)
            self.state = 61
            self.match(TREParser.INT)
            self.state = 62
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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtomic_expr" ):
                return visitor.visitAtomic_expr(self)
            else:
                return visitor.visitChildren(self)




    def atomic_expr(self):

        localctx = TREParser.Atomic_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_atomic_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 64
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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRename_token" ):
                return visitor.visitRename_token(self)
            else:
                return visitor.visitChildren(self)




    def rename_token(self):

        localctx = TREParser.Rename_tokenContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_rename_token)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.atomic_expr()
            self.state = 67
            self.match(TREParser.T__14)
            self.state = 68
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
         




