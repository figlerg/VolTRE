from parse.TREParser import TREParser


"""
So at this point we can compute V_n^e(T) and V_n(e). Now we can begin to sample.

The idea here is as follows:
- Compute volume functions for all subexpressions (for all relevant n).

I want to "sample downwards". So we start at top with a specific input (n,T) and invoke child samplers.
- The base case is an atomic a where we return the tuple (a,T) .
-recursion:
    - convolution with input (n,T):
        - discrete: select k in 0...n: Select k with proba Vke1(T)/Vne1(T)
        - we have T time available and know Vne, Vne1, Vne2.
            TODO How do we sample T1 and T2? I think its just 1/(Vne1 ** Vne2)
        - we now have a specific recursion input (k,T') for the sampler of e1 and and (n-k, T-T') for the sampler of e2
    - union with input (n,T):        select one of the children according to volumes: Vne1(T)/Vne(T)
    - kleene star with input (n,T):
        - like convolution for e.e*
"""

def sample(ctx: TREParser.ExprContext, n, T, vol_cache):

    node_type = type(ctx)

    match node_type:

        case TREParser.AtomicExprContext:
            assert n == 1, f"Problem during parsing: Cannot sample letter {node_type.getText()} with {n} letters."
            return ctx.getText()

        case TREParser.ParenExprContext:
            pass

        case TREParser.UnionExprContext:
            pass

        case TREParser.ConcatExprContext:
            pass

        case TREParser.KleeneExprContext:
            pass

        case TREParser.TimedExprContext:
            pass





