import math
import random
import warnings
from functools import cached_property

import mpmath
import numpy as np
from matplotlib import pyplot as plt, ticker
from mpmath import findroot
from scipy.integrate import IntegrationWarning
from sympy import Expr
from sympy import lambdify
from sympy import oo, Integral, sympify
from sympy.abc import T, v

from volume.FreePiecewise import FreePiecewise
from volume.VolumePoly import VolumePoly
from misc.helpers import cached_lambdify, num_int_evalf
from volume.tuning import build_exp_term, normalising_constant
from typing import Iterable


class MaxEntDist:
    """A container class for the maximum entropy solution for given soft constraints. This is essentially a weight
    function for duration T, with which we could implement a different sampler for T (which maximises language
    entropy and can control mean and variance (or any moment))."""

    def __init__(self, volume: VolumePoly, lambdas: Iterable[float]):
        self.volume = volume
        self.lambdas = tuple(lambdas)  # we want this hashable

        # compared to VolumePoly we have an additional exp term in the weight function (so integrals change)
        self.exp_term = build_exp_term(self.lambdas)

        self.normalised = False

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

    def __bool__(self):
        return self.exp_term and bool(self.volume.polys)

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

        return normalising_constant(self.lambdas, self.volume)

    def plot(self, no_show=False):
        """
        Just a modified copy of VolumePoly visualization functions.
        """

        num_points = 400

        # Create a colormap
        cmap = plt.get_cmap('tab10')  # You can choose any colormap you prefer

        for i, ((a, b), term) in enumerate(self.pairs):
            f = lambdify(v, term, modules=['scipy', 'numpy'])

            inf_flag = False
            if b == oo:
                b = a + 3  # just to see something, I arbitrarily visualize a little bit of the inf interval
                inf_flag = True

            # Generate points within the interval
            x = np.linspace(a, b, num_points)

            # Evaluate the function at each point
            y = [f(point) for point in x]

            # Get color from the colormap TODO - they mix and it looks bad/confusing
            color = cmap(
                i % cmap.N)  # Looping over colors in case the number of functions exceeds the number of colors in the colormap

            plt.plot(x, y, label=f"$V_n^e$ on [{a}, {b}]", color=color)

            # Plot interval boundaries
            plt.axvline(x=a, linestyle='--', color='grey', alpha=0.5)  # Start of interval

            if not inf_flag:
                plt.axvline(x=b, linestyle='--', color='grey', alpha=0.5)  # End of interval
            else:
                plt.axvline(x=b + 1, linestyle='--', color='grey', alpha=0.5)  # End of interval

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

        if not self.normalised:
            plt.ylabel(r'$e^{\lambda_1 T + ... + \lambda_m T^m}V^e_{n}(T)$       ', rotation=90)
        # I give an option to fix the label for an actual pdf
        else:
            plt.ylabel(r'$\frac{e^{\lambda_1 T + ... + \lambda_m T^m}V^e_{n}(T)} '
                       r'{\int_0^\infty e^{\lambda_1 T_1 + ... + \lambda_m T_1^m}V^e_{n}(T_1 dT_1)}$       ', rotation=90)

        if self.volume.exp and self.volume.n:
            plt.title(f'MaxEnt Solution\ne = {self.volume.exp}, n = {self.volume.n}.')
        # plt.legend()
        plt.grid(False)  # Remove background lattice
        plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        if not no_show:
            plt.show()

    def eval_plot(self, no_show=False):
        """
        For debugging it is useful to lambdify the whole function and plot that. Basically a check for .plot().
        """
        num_points = 400

        # Create a colormap
        cmap = plt.get_cmap('tab10')  # You can choose any colormap you prefer

        # basically lambdified piecewise function
        def f(val):
            for (a,b), p in self.volume.pairs:
                if a <= val < b:
                    fun = lambdify(v, p(v)*self.exp_term.subs(T,v), modules=['scipy', 'numpy'])
                    return fun(val)

            return 0

        self.volume.plot()
        x = np.linspace(0, self.volume.intervals[-1][1], num_points)

        # Evaluate the function at each point
        y = [f(point) for point in x]


        plt.plot(x,y)
        plt.title(f'Lambdified $V_n^{self.volume.exp}')
        plt.show()



        p1 = tuple(self.volume.pairs)[2][1]
        y = [p1(point) for point in x]

        plt.plot(x,y)
        plt.title(f'Left poly {p1}')
        plt.show()

        p2 = tuple(self.volume.pairs)[3][1]
        y = [p2(point) for point in x]

        plt.plot(x,y)
        plt.title(f'Right poly {p2}')
        plt.show()

        g = lambda t: self.exp_term.subs(T,t).evalf()
        y = [g(point) for point in x]

        plt.plot(x,y)
        plt.title(f'Exp term {self.exp_term}')

        if not no_show:
            plt.show()



    # SAMPLING

    @cached_property
    def pdf(self):
        """
        Returns a normalized version (pdf) of self. Note: This is not really used anywhere due to numerical instability.
        :return: A normalized MaxEntDist
        """
        div_factor = 1 / self.normalising_term
        pdf = self * div_factor
        pdf.normalised = True
        return pdf

    @cached_property
    def cdf(self) -> FreePiecewise:
        """
        Returns a piecewise function that is a cdf of the Maximum Entropy cdf. Note that this is not itself a MaxEntDist
        but instead a FreePiecewise - we have no way of finding a symbolic integral for the expressions here and we
        do not have the nice closedness result as with VolumePolys (that the cdf remains in the class of piecewise
        polys.)
        :return: The cdf as a collection of (interval, sympy term) pairs
        """

        assert self, "The zero function has no pdf. Is the language empty?"

        intervals = self.volume.intervals.copy()
        terms = []

        c = 0
        for (a, b), integrand in self.pairs:
            integrand: Expr  # this is already p(T)*exp_term(T)

            # ## THIS IS SLOW
            # # create antiderivative of the poly, with variable T as endpoint.
            # # This is an unevaluated integral (which we can approximate later)
            sub_antideriv = Integral(integrand, (v, a, T))
            sub_antideriv += c
            terms.append(sub_antideriv)

            # tmp = c
            # c = num_int_evalf(integrand, a, b)
            # c += tmp
            c += num_int_evalf(integrand, a, b, var=v)  # this is the same, no?

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

        cdf = self.cdf
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
                # TODO we have some numerical instability, it seems.
                #      u = 0.999706564107641 can't find a solution for precision 1e-32, even though f(a) <= 0 <= f(b)
                if b == math.inf:
                    b = 10000

                # TODO right now I just ignore the integration warnings.
                #  I should figure out a way to handle these differently
                with warnings.catch_warnings():
                    # warnings.filterwarnings("ignore", category=RuntimeWarning)
                    warnings.filterwarnings("ignore", category=IntegrationWarning)
                    try:
                        sol = findroot(f, (a, b), solver='anderson')
                    except (ValueError, ZeroDivisionError):
                        # warnings.warn(f"Inverse sampling problem: Anderson solver failed for u = {u}.\n"
                        #               f"f(a) = {f(a)}, f(b) = {f(b)}. Falling back to bisection.")
                        sol = findroot(f, (a, b), solver='bisect')
                        # print(sol)
                        # print("Plotting cdf...")
                        # plt.axhline(y=u, color='r', linestyle='--')
                        # cdf.plot(title = 'Sampling error - cdf')
                        # plt.show()

                if a <= sol <= b:
                    # plt.plot(sol, u, 'ro')
                    # cdf.plot(title = 'cdf')
                    # plt.show()
                    return sol

        # cdf.plot(no_show=True)
        # plt.axhline(y=u, color='r', linestyle='--')
        # plt.show()

        raise Exception("Inverse sampling failed.")
