from match.match import match
from parse.TREParser import TREParser
from sample.sample import sample
from math import inf

from volume.slice_volume import slice_volume


def is_subset(node1:TREParser.ExprContext, node2:TREParser.ExprContext,n, eps:float, alpha:float, T = None) -> int:
    """
    This function implements a statistical language inclusion test.
    For a given n, we want to give a counterexample or a confidence interval
    for the language inclusion L_n(node1) < L_n(node2).

    Gives a confidence interval for error bound epsilon and confidence alpha.

        "
        When X is either 0 or N, closed-form expressions for the interval bounds are available.
        When X = 0 the interval is (0, 1 − (α/2)^(1/N)) and when X = N it is ((α/2)^(1/N), 1).
        "
        -Thulin, Måns. "The cost of using exact confidence intervals for a binomial proportion." (2014): 817-840.

    X is here the number of successes, i.e. the number of samples which are also in the second expression.
    If we have one failure, so one word that is in e1 but not in e2, we have a counter example and know for sure the
    inclusion does not hold.

    If we have no failures, so X = N, then we know with some certainty 1-a that
    the success probability is in the interval ((α/2)^(1/N), 1).

    In this case, either we have that the volume of their set difference vol(e1-e2) is small, or that the inclusion holds.
    The volume of the set difference is the deciding factor, since the proba of success is 1 - (vol(e1 - e2) / vol(e1)).

    So our procedure is
        - 1) sample n samples from e1
        - 2a) if one is not in e2, we are done with a counterexample
        - 2b) if all are in e2, we know with certainty 1-alpha that success proba p is in ((α/2)^(1/N), 1).
        - 3) if 2b but there is in fact a volume of counterexamples vol(e1-e2), then with certainty 1-alpha
                 (α/2)^(1/N)                    <   1 - (vol(e1 -e2) / vol(e1))
                 (α/2)^(1/N) - 1                <   -(vol(e1 -e2) / vol(e1))
                 1 - (α/2)^(1/N)                >   vol(e1 -e2) / vol(e1)
                 (1 - (α/2)^(1/N)) * vol(e1)    >   vol(e1 -e2)



    :param node1: parsed expression 1
    :param node2: parsed expression 2
    :param n: word length (i.e. we are comparing L_n(node1) < L_n(node2))
    :param eps: float describing the error bound
    :param theta: float describing the confidence of being TODO being where? -eps, +eps of mean? What is the interval?
    :return: 0 in case that a counterexample is found, otherwise the lower bound of p
    (or the upper bound of failure proba 1-p).
    """

    # TODO reread the theory above and implement. should be relatively straightforward
    v1 = slice_volume(node1,n)

    bound = inf

    N = 0
    while bound > eps:
        w = sample(node1,n, T=T)
        N += 1

        if not match(w,node2):
            print(f"Subset does not hold with counter example w = {w}. \nSampled N = {N} times. "
                  f"Current upper bound for the confidence interval for failure probability would be {bound}.")

            return 0

        print(bound)
        bound = 1 - (alpha/2)**(1/N)

    if not T:
        print(f"No counterexample found after {N} samples."
              f"\nWith confidence {1-alpha} we can say that Vol({node1.getText()} - {node2.getText()}) < {bound * v1.total_volume()}"
              f"\nWith confidence {1-alpha} we can say that the probability of finding a counterexample is < {bound}.")
    else:
        print(f"No counterexample found after {N} samples."
              f"\nWith confidence {1 - alpha} we can say that Vol({node1.getText()} - {node2.getText()}) < {bound * v1(T)}, as opposed to Vol({node1.getText()}(T) = {v1(T)}"
              f"\nWith confidence {1 - alpha} we can say that the probability of finding a counterexample is < {bound}.")

    return bound