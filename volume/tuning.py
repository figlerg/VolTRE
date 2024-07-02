from functools import lru_cache

import sympy as sp
import numpy as np
from scipy.integrate import quad
from scipy.optimize import least_squares

from volume.FreePiecewise import FreePiecewise
from volume.VolumePoly import VolumePoly

from sympy import symbols, exp, integrate, oo, Integral, Poly, sympify, solve, solveset, Expr, lambdify
from sympy.abc import T, v

from volume.misc import num_int_evalf

"""
This module is for controlling the properties of the MaxEntSampler.
"""

@lru_cache
def build_exp_term(lambdas) -> Expr:
    # Create the polynomial sum
    polynomial_sum = sum([s * T ** (i + 1) for i, s in enumerate(lambdas)])

    return exp(polynomial_sum)

# TODO move this somewhere more sensible, i just refactored it out as a function cause it is used in multiple places
@lru_cache
def normalising_constant(lambdas, volume) -> float:
    assert lambdas[-1] < 0 or volume.intervals[-1][1] != oo, ("Integral doesn't exist - we either need a "
                                                                        "bounded language or lambda_m < 0.")

    exp_term = build_exp_term(lambdas)

    s = 0
    for (a, b), poly in volume.pairs:
        integrand = exp_term.as_expr() * poly.as_expr()

        # old version - Tested with wolframalpha, same results for bounded intervals.
        # segment_integral = Integral(integrand, (T, a, b))

        # TODO test again with wolfram this version
        s += num_int_evalf(integrand, a, b)

    return s


# mu -> lambda HARD
#
# lambda -> mu EASY
#     -> Euler, gradient descent
#
#
# fixed lambda -> fgenerate mus

def mu(lambdas: np.array, volume: VolumePoly, m = None):

    # Any moment can be computed,
    # but sometimes we are only interested in the first m moments where m is the nr of lambdas.
    if not m:
        m = len(lambdas)


    intervals = volume.intervals.copy()

    # here I take exp(...)*p(T) for all segments
    terms = [(build_exp_term(lambdas).as_expr() * p.as_expr()) for p in volume.polys]

    N = normalising_constant(lambdas, volume)

    # here I just need to integrate from 0 to inf, not create functions for each segment
    out = np.ndarray((m, 1))

    for i in range(m):

        cum_sum = 0
        for (a, b), integrand in zip(intervals, terms):
            integrand: Expr = integrand * T ** (i+1)  # computing the i-th moment, diff gives T^i

            cum_sum += num_int_evalf(integrand, a, b)

        out[i] = cum_sum / N

    return out

def jacobi(lambdas: np.array, volume: VolumePoly, d1 : int):
    """
    Generate the jacobi matrix d mu_i/d lambda_j with dimensions d1 x len(lambdas).
    We have found a nice representation for j <= m, where m is the number of lambdas.

    Formula:
        $$ \frac{d\mu_i}{d \lambda_j}(\lambda) = \mu_{i+j}(\lambda) - \mu_i(\lambda) \cdot \mu_j(\lambda)$$

    :param lambdas:
    :param volume:
    :param m:
    :param n:
    :return:
    """
    d2 = len(lambdas)
    mus = mu(lambdas, volume,d1+d2)  # I need up to m+n to use the nice form nicolas found

    # I will first create a square matrix, and then cut out the ones that reference non-existing lambda_i
    d_max = max(d1, d2)
    M = np.ndarray((d_max, d_max))

    # this is the square matrix with nice representation. TODO can we do this without a loop for speed?
    for i in range(d_max):
        for j in range(d_max):
            M[i,j] = mus[i+j]

    # matrix version of -mu_i*mu_j
    M -= mus[:d_max] @ mus[:d_max].T

    # this is the part that we simply calculate

    # some of these have no meaning because they are basically derivatives for lambdas that we do not have -> cut them
    return M[:d1,:d2]

def hesse(lambdas: np.array, volume: VolumePoly, d1 : int):
    pass

def lambdas(target_mu : np.array, vol : VolumePoly):

    mus = lambda ls: mu(ls, vol,len(target_mu))

    initial_guess = np.random.random([len(target_mu), 1])  # Example initial guess

    result = least_squares(residuals, initial_guess, args=(mu_t,))



def residuals(mu, target_mu):
    return mu - target_mu




