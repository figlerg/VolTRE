# Generated from C:/Users/giglerf/PycharmProjects/VolTRE/parse/TRE.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .TREParser import TREParser
else:
    from TREParser import TREParser

# This class defines a complete generic visitor for a parse tree produced by TREParser.

class TREVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TREParser#ConcatExpr.
    def visitConcatExpr(self, ctx:TREParser.ConcatExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TREParser#AtomicExpr.
    def visitAtomicExpr(self, ctx:TREParser.AtomicExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TREParser#UnionExpr.
    def visitUnionExpr(self, ctx:TREParser.UnionExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TREParser#KleeneExpr.
    def visitKleeneExpr(self, ctx:TREParser.KleeneExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TREParser#ParenExpr.
    def visitParenExpr(self, ctx:TREParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TREParser#TimedExpr.
    def visitTimedExpr(self, ctx:TREParser.TimedExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TREParser#interval.
    def visitInterval(self, ctx:TREParser.IntervalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TREParser#atomic_expr.
    def visitAtomic_expr(self, ctx:TREParser.Atomic_exprContext):
        return self.visitChildren(ctx)



del TREParser