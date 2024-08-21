import warnings

import numpy as np
from scipy.integrate import IntegrationWarning
from scipy.optimize import root

from parse.quickparse import quickparse
# from sample.sample import sample, DurationSamplerMode
from volume.VolumePoly import VolumePoly

from sympy import exp, oo, Expr
from sympy.abc import T

from misc.helpers import num_int_evalf
from volume.slice_volume import slice_volume

"""
This module is for controlling the properties of the MaxEntSampler.
"""



# @lru_cache
def build_exp_term(lambdas) -> Expr:
    # Create the polynomial sum
    polynomial_sum = sum([s * T ** (i + 1) for i, s in enumerate(lambdas)])

    return exp(polynomial_sum)


# TODO move this somewhere more sensible, i just refactored it out as a function cause it is used in multiple places
# @lru_cache
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

def mu(lambdas: np.array, volume: VolumePoly, m=None):
    # Any moment can be computed,
    # but sometimes we are only interested in the first m moments where m is the nr of lambdas.
    if not m:
        m = len(lambdas)

    intervals = volume.intervals.copy()

    # here I take exp(...)*p(T) for all segments
    terms = [(build_exp_term(lambdas).as_expr() * p.as_expr()) for p in volume.polys]

    # if lambdas[-1] >= 0:
    #     # in this case the integrals will be undefined
    #     return [np.inf,] * m

    try:
        N = normalising_constant(lambdas, volume)
    except AssertionError:
        # TODO fix this atrocity, mu is often evaluated for invalid lambdas. I just fill in high values to penalize
        return np.full((m,), 1000)

    # here I just need to integrate from 0 to inf, not create functions for each segment
    out = np.ndarray((m,))

    for i in range(m):

        cum_sum = 0
        for (a, b), integrand in zip(intervals, terms):

            # The last nonzero lambda is 0 <=> the integral is defined. otherwise it's +inf
            if b == oo and [lam for lam in lambdas if lam != 0][-1] > 0:
                cum_sum += oo
                continue

            integrand: Expr = integrand * T ** (i + 1)  # computing the i-th moment, diff gives T^i

            # Perform the integration
            cum_sum += num_int_evalf(integrand, a, b)

        out[i] = cum_sum / N

    return out


def jacobi(lambdas: np.array, volume: VolumePoly, d1: int):
    r"""
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
    mus = mu(lambdas, volume, d1 + d2)  # I need up to m+n to use the nice form nicolas found

    # I will first create a square matrix, and then cut out the ones that reference non-existing lambda_i
    d_max = max(d1, d2)
    M = np.ndarray((d_max, d_max))

    # this is the square matrix with nice representation. TODO can we do this without a loop for speed?
    for i in range(d_max):
        for j in range(d_max):
            M[i, j] = mus[i + j]

    # matrix version of -mu_i*mu_j
    M -= mus[:d_max] @ mus[:d_max].T

    # this is the part that we simply calculate

    # some of these have no meaning because they are basically derivatives for lambdas that we do not have -> cut them
    return M[:d1, :d2]


def hesse(lambdas: np.array, volume: VolumePoly, d1: int):
    raise NotImplementedError


def lambdas(target_mu: np.array, vol: VolumePoly):
    k = len(target_mu)
    l = k  # this is probably just one of many solutions? I think fixing more moments would make this less free

    x0 = np.random.random(k)  # Example initial guess
    x0[-1] = - np.random.random()  # TODO this needs to be <0 to make the integrals finite

    res = lambda lambda_vector: residuals(mu(lambda_vector, vol, m=k), target_mu)

    # J = lambda lambda_vector: jacobi(lambda_vector, vol, l) @ np.diag(res(mu(lambda_vector, v)))
    #
    # result = least_squares(res, x0, jac=J)

    J = lambda x: jacobi(x, vol, l)
    # result = root(res, x0, jac=J, tol=1e-14)

    # TODO we get many integration warnings. The integrals are expected to misbehave, for now I ignore them
    with warnings.catch_warnings():
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        warnings.filterwarnings("ignore", category=IntegrationWarning)

        J = None  # broyden doesn't need it
        result = root(res, x0,jac = J, method='broyden1', options={'fatol':1e-6}, tol=1e-14)


    # result = root(res, x0,jac = J, method='lm', options={'ftol':1e-10}, tol=1e-14)

    # result2 = root(res, x0)
    # print(result.x - result2.x)
    # print(mu(result2.x,v,k))

    print(f"Target mu is {target_mu}")
    print(f"inferred lambda is {result.x}")
    print(f"mu(inferred_lambda) = {mu(result.x, volume=vol, m=k)}")
    assert loss(mu(result.x, vol), target_mu) < 1e-8, (f"Solver failed to generate acceptable loss: "
                                                       f"final loss is {loss(mu(result.x, vol), target_mu)}")
    print(f"Loss is {loss(mu(result.x, vol), target_mu)}")

    return result.x


def residuals(mu_guess, mu_target):
    return mu_guess - mu_target


def loss(mu_guess, mu_target):
    return (np.square(mu_guess - mu_target)).mean()


def parameterize_mean_variance(target_mean, target_variance, vol):
    # formula: variance = mu_2 - mean^2
    mu_1 = target_mean
    mu_2 = target_variance + target_mean ** 2

    target_moments = np.asarray([mu_1, mu_2])

    assert mu_2 > 0 and mu_1 > 0, ("Invalid mean and variance? Do a sanity check (e.g. use variance = mu_2 - mean^2 "
                                   "and see whether mu_2 <= 0.)")

    return lambdas(target_moments, vol)


if __name__ == '__main__':
    ctx = quickparse("experiments/spec_00.tre")

    n = 3
    v = slice_volume(ctx, n)
    # v.plot()

    target = np.asarray([3, 10])
    # target.resize((len(target),1))

    optimal_lambda = lambdas(target, v)

    tuned_lambdas = parameterize_mean_variance(4, 1, v)

    samples = [sample(ctx, n, mode=DurationSamplerMode.MAX_ENT, lambdas=tuned_lambdas)]

    durations = np.asarray([w.duration for w in samples])

    print(durations.mean())
    print(durations.var())
