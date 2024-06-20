import random
import warnings
from functools import lru_cache, cached_property

import numpy as np
from matplotlib import pyplot as plt, ticker
from mpmath import findroot
from scipy.integrate import quad
from sympy import Expr
from sympy import lambdify
from sympy import oo, Integral, sympify
from sympy.abc import T, v

from volume.FreePiecewise import FreePiecewise
from volume.VolumePoly import VolumePoly
from volume.misc import cached_lambdify
from volume.tuning import exp_term


# TODO i could have probably include this in volume poly (or inherit from it),
#  but I am worried that things get too complex if I do.
class MaxEntDist:
    """A container class for the maximum entropy solution for given soft constraints. This is essentially a weight
    function for duration T, with which we could implement a different sampler for T (which maximises language
    entropy and can control mean and variance (or any moment))."""

    def __init__(self, volume: VolumePoly, lambdas: list[float]):
        self.volume = volume
        self.lambdas = lambdas

        # compared to VolumePoly we have an additional exp term in the weight function (so integrals change)
        self.exp_term = exp_term(lambdas)

    def __hash__(self):
        return hash((self.volume, self.exp_term))

    def __str__(self):
        return f"{self.exp_term}  *  {self.volume}"

    def __call__(self, val):

        borders = [x for x, _ in self.volume.intervals] + [y for _, y in self.volume.intervals]

        if val in borders:
            warning = f"""
            You are trying to evaluate the function {self} on the point {val} which is on the
            boundary of an interval. It is not clear a priori how to evaluate this, but the 
            sensible thing to do is to add the left and right limit of this point. 
            Be aware that this is not the continuous extension, but it makes more sense for slice 
            volumes. Since these points are a null-set, it doesn't matter when integrating over it.
            """
            warnings.warn(warning, UserWarning)

        return sum([p(val) for (a, b), p in self.volume.pairs if a <= val <= b])

    def __mul__(self, other):
        """
        Basically only works for MaxEntDist * number right now.
        """

        if isinstance(other, MaxEntDist):
            raise NotImplementedError("Multiplication not supported for two MaxEnt functions.")

        if isinstance(other, VolumePoly):
            raise NotImplementedError("Multiplication not supported for MaxEnt and VolumePoly functions.")

        else:
            new_volume = self.volume * other
            return MaxEntDist(new_volume, self.lambdas)

    @cached_property
    def pairs(self):
        """
        This is a little helper which generates callable functions for each segment. Is cached, so it is only computed
        once.
        """
        intervals = self.volume.intervals
        terms = [self.exp_term.subs(T, v) * p(v) for p in self.volume.polys]

        # zip makes a generator, which cannot be cached
        return tuple(zip(intervals, terms))

    @cached_property
    def normalising_term(self):
        """
        Computes the total volume of the maximum entropy solution. An exponential term times a piecewise poly, which are computed
        numerically piece by piece.
        :return: Float (or similar) of total volume.
        """

        assert self.lambdas[-1] < 0 or self.volume.intervals[-1][1] != oo, ("Integral doesn't exist - we either need a "
                                                                            "bounded language or lambda_m < 0.")

        s = 0
        for (a, b), poly in self.volume.pairs:
            integrand = self.exp_term.as_expr() * poly.as_expr()

            # Tested with wolframalpha, same results for bounded intervals.
            # TODO numerical, can't deal with inf. This returns just a big number in cases where it should diverge.
            segment_integral = Integral(integrand, (T, a, b))

            s += segment_integral.evalf()

        return s

    def plot(self, no_show=False):
        """
        Just a modified copy of VolumePoly visualization functions.
        """

        num_points = 400

        # Create a colormap
        cmap = plt.get_cmap('tab10')  # You can choose any colormap you prefer

        last_val = 0
        for i, (function, interval) in enumerate(zip(self.volume.polys, self.volume.intervals)):

            start, end = interval

            inf_flag = False
            if end == oo:
                end = start + 3  # just to see something, I arbitrarily visualize a little bit of the inf interval
                inf_flag = True

            # If function is not callable, convert it to a lambda function
            if not callable(function):
                f = lambda z: function
            else:
                f = function

            # Generate points within the interval
            x = np.linspace(start, end, num_points)

            # Evaluate the function at each point
            y = [float(f(point) * self.exp_term.subs(T, point)) for point in x]

            ## strictly speaking, at the border points we want something like the sum of the two polys.
            ## under the assumption that we get continuous volumes, we can do the below.
            # if self.n not in [0,1]:
            #     plt.scatter(x[-1], 2*y[-1], color = 'black', s = 6)

            # Get color from the colormap TODO - they mix and it looks bad/confusing
            color = cmap(
                i % cmap.N)  # Looping over colors in case the number of functions exceeds the number of colors in the colormap

            plt.plot(x, y, label=f"$V_n^e$ on [{start}, {end}]", color=color)

            # Plot interval boundaries
            plt.axvline(x=start, linestyle='--', color='grey', alpha=0.5)  # Start of interval

            if not inf_flag:
                plt.axvline(x=end, linestyle='--', color='grey', alpha=0.5)  # End of interval
            else:
                plt.axvline(x=end + 1, linestyle='--', color='grey', alpha=0.5)  # End of interval

            # Indicate that the function goes on like this if we have an infinite interval.
            # This is just for visual clarity, there is no real "right" solution to plot an infinite function,
            # but I wanted to make clear in the pictures when we have an interval [c, inf).
            if i == len(self.volume.intervals) - 1 and inf_flag:
                # Add an arrow indicating the function continues to infinity
                plt.annotate('', xy=(x[-1], y[-1]),
                             xytext=(x[-2], y[-2]),
                             arrowprops=dict(arrowstyle='->', color='black'))

                # TODO for some reason arrow is not actually at the end in some examples.
                #  This is not important but annoys me.

                # Retrieve current x-tick positions
                ax = plt.gca()
                current_ticks = ax.get_xticks()

                # Modify x-tick labels to include ellipsis and infinity symbol
                new_labels = [f'{int(tick)}' for tick in current_ticks[:-3]] + [r'$\cdots$', r'$\infty$', '']

                new_ticks = list(current_ticks)
                # Set the x-tick labels
                ax.set_xticks(new_ticks)
                ax.set_xticklabels(new_labels)

        # Ensure that (0, 0) is included in the plot
        plt.xlim(left=min(0, plt.xlim()[0]), right=max(0, plt.xlim()[1]))
        plt.ylim(bottom=min(0, plt.ylim()[0]), top=max(0, plt.ylim()[1]))

        plt.xlabel('T')
        plt.ylabel(r'$e^{\lambda_1 T + ... + \lambda_m T^m}V^e_{n}(T)$       ', rotation=0)
        if self.volume.exp and self.volume.n:
            plt.title(f'MaxEnt Sol.:\ne = {self.volume.exp}, n = {self.volume.n}.')
        # plt.legend()
        plt.grid(False)  # Remove background lattice
        plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        if not no_show:
            plt.show()

    # SAMPLING

    @lru_cache
    def pdf(self):
        """
        Returns a normalized version (pdf) of self. Note: This is not really used anywhere due to numerical instability.
        :return: A normalized MaxEntDist
        """
        div_factor = 1 / self.normalising_term
        return self * div_factor

    @lru_cache
    def cdf(self) -> FreePiecewise:
        """
        Returns a piecewise function that is a cdf of the Maximum Entropy cdf. Note that this is not itself a MaxEntDist
        but instead a FreePiecewise - we have no way of finding a symbolic integral for the expressions here and we
        do not have the nice closedness result as with VolumePolys (that the cdf remains in the class of piecewise
        polys.)
        :return: The cdf as a collection of (interval, sympy term) pairs
        """

        intervals = self.volume.intervals.copy()
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

    def inverse_sampling(self):
        """
        Assumes this is a pdf and simplified.
        :return: A sample of the distribution.
        """

        u = random.uniform(0, 1)

        cdf = self.cdf()
        # cdf.plot()

        # TODO how do i check this here? N is sort of the total volume here, right?
        # assert abs(self.total_volume() -1) < 0.0001, ("Invalid distribution. This is no pdf. "
        #                                               "It is likely this is caused by a bug.")

        for (a, b), term in cdf.pairs:
            # f = lambdify(T, term - u, modules=['scipy', 'numpy'])

            f = lambda x: cached_lambdify(term)(x) - u

            # this is the only case we need to consider, immediately return
            if f(a) <= 0 <= f(b):
                ## NOTE: (term - u).subs(T,1).evalf() computes a number

                ## VANILLA PARAMETERS
                # sol = nsolve(term - u,T, (b+a)/2)

                ## BISECTION, DOCS: "One might safely skip the verification if bounds of the root are known and a
                #                       bisection method is used"
                ## NOTE: this is slower than vanilla
                # sol = nsolve(term - u, (a,b), solver='bisect', verify=False)

                # x0 = (a + b) / 2

                # Use mpmath.findroot to find the root within the specified interval THIS IS FASTEST
                sol = findroot(f, (a, b), solver='anderson')

                if a <= sol <= b:
                    # plt.plot(sol, u, 'ro')
                    # cdf.plot(title = 'cdf')
                    # plt.show()
                    return sol

        # cdf.plot(no_show=True)
        # plt.axhline(y=u, color='r', linestyle='--')
        # plt.show()

        raise Exception("Inverse sampling failed.")
