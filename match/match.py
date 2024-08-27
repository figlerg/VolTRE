from misc.recursion_template import get_interval
from parse.TREParser import TREParser
from parse.quickparse import quickparse
from sample.TimedWord import TimedWord
import warnings


def match(w:TimedWord, phi: TREParser.ExprContext) -> int:

    node_type = type(phi)
    phi_text = phi.getText()

    match node_type:

        case TREParser.AtomicExprContext:
            atom = phi.getText()

            if w:
                sym = w[0][0]
            else:
                sym = ''

            if w.length == 1 and sym == atom:
                N = 1
            else:
                N = 0

        case TREParser.ParenExprContext:
            phi: TREParser.ParenExprContext
            expr = phi.expr()

            N = match(w, expr)

        case TREParser.UnionExprContext:
            phi: TREParser.UnionExprContext
            e1 = phi.expr(0)
            e2 = phi.expr(1)

            N1 = match(w,e1)
            N2 = match(w,e2)

            N = N1 + N2

        case TREParser.TimedExprContext:
            phi: TREParser.TimedExprContext

            a,b = get_interval(phi)
            expr: TREParser.ExprContext = phi.expr()

            if a <= w.duration <= b:
                N = match(w, expr)
            else:
                N = 0

        case TREParser.ConcatExprContext:
            phi: TREParser.ConcatExprContext

            e1, e2 = phi.expr(0), phi.expr(1)

            matches = [match(w[:k], e1) * match(w[k:],e2) for k in range(w.length+1)]
            N = sum(matches)

        case TREParser.KleeneExprContext:
            phi: TREParser.KleeneExprContext

            e1, e2 = phi.expr(), phi

            """
            Case: word is 1 letter long. 
                We have w[:0]*w[0:] == w. 
                Further w[0:] == w.
                In kleene we evaluate match(w[0],e) and concatenate with match(EPS,e*).

            """

            # need to check for epsilon
            if w.is_epsilon():
                N = 1
            else:
                N = 0
                for k in range(w.length+1):
                    N1 = match(w[:k], e1)

                    # this guards against infinite recursion: if N1 is 0 we do not need to look at the other factor
                    if N1:
                        N2 = match(w[k:], e2)
                    else:
                        continue

                    N_sub = N1 * N2
                    N+=N_sub

        case TREParser.IntersectionExprContext:
            phi:TREParser.IntersectionExprContext
            warnings.warn("Ihe match() function for intersection is experimental at this point."
                          "Also, it does not count the syntax trees, but just checks that the word is at least "
                          "in both child languages.")

            return match(w, phi.expr(0)) and match(w,phi.expr(1))

        case TREParser.RenameExprContext:
            warnings.warn("Sampling for intersection and renaming is experimental and may not terminate.")
            raise NotImplementedError

        case _:
            raise NotImplementedError('Was a new grammar rule added?')

    # if isinstance(phi, TREParser.TimedExprContext):
    #     print(f"N({phi.getText()}\t,\t{w})= {N}")
    #     print(w.dates)
    #     print('')

    return N

