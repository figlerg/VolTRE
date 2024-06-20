
import sympy as sp
import numpy as np

from volume.FreePiecewise import FreePiecewise
from volume.VolumePoly import VolumePoly

from sympy import symbols, exp, integrate, oo, Integral, Poly, sympify, solve, solveset, Expr

"""
This module is for controlling the properties of the MaxEntSampler.
"""


def exp_term(lambdas) -> Expr:

    T = symbols('T')

    # Create the polynomial sum
    polynomial_sum = sum([s * T ** (i + 1) for i, s in enumerate(lambdas)])

    return exp(polynomial_sum)




def mu(lambdas: np.array, volume: VolumePoly):
    intervals = volume.intervals.copy()
    terms = []

    c = 0
    c2 = 0
    for (a, b), integrand in self.pairs:
        integrand: Expr  # this is already p(T)*exp_term(T)

        # ## THIS IS SLOW
        # # create antiderivative of the poly, with variable T as endpoint.
        # # This is an unevaluated integral (which we can approximate later)
        sub_antideriv = Integral(integrand, (v, a, T))

        sub_antideriv += c2  # move by the current cumulative sum divided by N (we saved this before in self.__cs)
        terms.append(sub_antideriv)
        #
        # c = sub_antideriv.subs(T,b).evalf()

        ## HOPE THIS IS FAST
        integrand_func = lambdify(v, integrand, modules=['scipy', 'numpy'])
        # noinspection PyTupleAssignmentBalance
        tmp_c2 = c2
        c2, err = quad(integrand_func, a, b)

        c2 += tmp_c2

        # assert abs(c2 - c) < 0.001

    # test = FreePiecewise(intervals, terms)

    N = terms[-1].subs(T, b)

    terms = [p / N for p in terms]

    a, b = intervals[-1]
    if b != oo:
        intervals.append((b, oo))
        terms.append(sympify(1))

    return FreePiecewise(intervals, expressions=terms)

def jacobi():
    # this should be a mapping of lambdas to a matrix?
    raise NotImplementedError

def lambdas(mu : np.array, vol : VolumePoly):
    # this will need some optimization algo
    pass