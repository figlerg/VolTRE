# helpers and similar
import math
from enum import Enum
from functools import lru_cache

import sympy as sp
from scipy.integrate import quad
from sympy import lambdify, Expr
from sympy.abc import T


def check_int(interval):
    assert len(interval) == 2, "Intervals are not two-valued?"
    assert interval[0] < interval[1] or interval[0] == math.inf == interval[1], "Intervals are not correctly ordered?"


def intersect(int1, int2):
    check_int(int1)
    check_int(int2)

    a1, b1 = int1[0], int1[1]
    a2, b2 = int2[0], int2[1]

    # TODO: take care with that last part. I basically decree that we don't care about point intervals.
    if b1 < a2 or b2 < a1 or max(a1, a2) == min(b1, b2):
        return None
    else:
        return max(a1, a2), min(b1, b2)


def length(interval):
    check_int(interval)
    out = interval[1] - interval[0]
    return out


class ConvolutionCase(Enum):
    BOTH_INFINITE = 1
    FIRST_INFINITE = 2
    SECOND_INFINITE = 3
    BOTH_FINITE_SAME_LENGTH = 4
    BOTH_FINITE_DIFFERENT_LENGTH = 5


def determine_convolution_case(interval1, interval2) -> ConvolutionCase:
    a1, b1 = interval1
    a2, b2 = interval2

    if b1 == math.inf and b2 == math.inf:
        return ConvolutionCase.BOTH_INFINITE
    elif b1 == math.inf:
        return ConvolutionCase.FIRST_INFINITE
    elif b2 == math.inf:
        return ConvolutionCase.SECOND_INFINITE
    elif (b1 - a1) == (b2 - a2):
        return ConvolutionCase.BOTH_FINITE_SAME_LENGTH
    else:
        return ConvolutionCase.BOTH_FINITE_DIFFERENT_LENGTH


def interval_convolution(int1, int2):
    """
    The convolution of piecewise polynomials gives us several different cases, which all define separate intervals.
    Here the intervals and a case enum is returned, to be used in the convolution function of the VolumePoly class
    (This is the overloaded ** operator __pow__).
    :param int1: An interval of 1st volume function.
    :param int2: An interval of 2nd volume function.
    :return: list of intervals, case number for later processing
    """
    check_int(int1)
    check_int(int2)

    a1, b1 = int1[0], int1[1]
    a2, b2 = int2[0], int2[1]
    l1, l2 = length(int1), length(int2)

    case = determine_convolution_case(int1, int2)

    new_ints = None  # just so linter doesn't complain below
    match case:
        case ConvolutionCase.BOTH_INFINITE:
            new_ints = [(a1 + a2, math.inf),]
        case ConvolutionCase.FIRST_INFINITE:
            new_ints = [(a1 + a2, a1 + a2 + l2),
                        (a1 + a2 + l2, math.inf)]
        case ConvolutionCase.SECOND_INFINITE:
            new_ints = [(a1 + a2, a1 + a2 + l1),
                        (a1 + a2 + l1, math.inf)]
        case ConvolutionCase.BOTH_FINITE_SAME_LENGTH:
            new_ints = [(a1 + a2, a1 + a2 + l1),
                        (a1 + a2 + l1, b1 + b2)]
        case ConvolutionCase.BOTH_FINITE_DIFFERENT_LENGTH:
            new_ints = [(a1 + a2, a1 + a2 + min(l1, l2)),
                        (a1 + a2 + min(l1, l2), a1 + a2 + max(l1, l2)),
                        (a1 + a2 + max(l1, l2), b1 + b2)]

    return new_ints


def multiset_interval_convolution(intervals1: list, intervals2: list):
    # takes to interval lists and returns all the intervals from the convolution of the two

    out = []

    for int1 in intervals1:
        for int2 in intervals2:
            out += interval_convolution(int1, int2)

    return out

def num_int_evalf(integrand:Expr, a, b, var = T):
    """This is just so I don't use 5 different procedures for evaluating integrals."""

    integrand_func = lambdify(var, integrand, modules=['scipy', 'numpy'])
    # noinspection PyTupleAssignmentBalance
    s, err = quad(integrand_func, a, b)
    return s

@lru_cache
def my_eval(expr):
    return expr.evalf()

@lru_cache
def cached_lambdify(expr):
    return lambdify(T, expr, modules=['scipy', 'numpy'])