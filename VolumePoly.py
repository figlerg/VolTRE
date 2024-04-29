from sympy import poly
from sympy.abc import T, t, \
    x  # I will treat T as the slice duration, and t as the variable in the convolution integrals

from sympy import S
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from math import inf


from parse.misc import intersect, length, interval_convolution


class VolumePoly:
    # a wrapper class for the piecewise polynomials.
    # Each has the form     sum for I in J, p_I 1_I [+ delta in some cases]

    def __init__(self, intervals: list = None, polys: list = None, delta: bool = False):
        # TODO this is bad - I want to use a hashmap, but there might be multiple equal intervals with different polys,
        #  so I either need to make them distinguishable as keys (e.g. numbering multiples), or just treat it as lists.
        #  I chose lists here for simplcity, and because it shouldn't change computation.
        #  However, I will always need to use indices instead of the intervals themselves when matching a poly:interval
        #  pair.


        self.intervals = intervals if intervals else list()  # empty intervals is just the zero poly
        self.polys = polys if polys else list()


        self.delta = delta

        # during creating with slice_volumes, these are set
        self.exp = None
        self.n = None


    @property
    def pairs(self):
        return zip(self.intervals, self.polys)

    def __str__(self):
        out = ''

        for interval, p in zip(self.intervals, self.polys):
            out += f'1_{interval}(T) * {p} + '

        out = out[0:-3]  # get rid of trailing +

        if self.delta:
            out += ' + delta(T)'

        return out

    def __repr__(self):
        return self.__str__()

    def simplify(self):

        c_max = 0
        for a, b in self.intervals:
            c_max = max(c_max, b)  # assumes that the interval is well-ordered, i.e. a < b

        min_int_repr = dict()

        new_intervals = []  # intervals after operation
        new_polys = []  # polys after operation
        last_a = 0  # left border of current interval
        last_poly = 0  # poly at current interval

        # TODO right now intervals [0,inf] don't work well
        #   I will put a heuristic for now, but this should be done better.
        c_max = min(c_max, 200)


        for i in range(c_max + 1):

            # deconstruct the intervals into minimal integer intervals
            min_piece = (i, i + 1)
            min_int_repr[min_piece] = 0  # adding 0 with a sympy poly works as intended (gives a poly)

            for j, inter in enumerate(self.intervals):

                # if the little interval is inside inter, add the inter poly
                if intersect(min_piece, inter) == min_piece:
                    min_int_repr[min_piece] = min_int_repr[min_piece] + self.polys[j]
                    # TODO pretty sure I can make this n times cheaper by remembering the intersected intervals

            if min_int_repr[min_piece] != last_poly:
                if last_poly:  # only add nonzero polynomials (can disregard intervals where the poly is zero)
                    new_intervals.append((last_a, i))  # current interval ends before current mini segment
                    new_polys.append(last_poly)  # current interval has the same poly on (last_a, i)
                last_a = i
                last_poly = min_int_repr[min_piece]

        self.intervals = new_intervals
        self.polys = new_polys

    def __add__(self, other):
        intervals = self.intervals + other.intervals
        polys = self.polys + other.polys
        delta = self.delta or other.delta
        # TODO this is not nice, because in our fragment it could still be that both have epsilon,
        #  and then we could end up with two diracs... In that case I am not sure what wouldbe the canonical way.

        out = VolumePoly(intervals, polys, delta)

        out.simplify()  # not strictly necessary, but probably we do this every time? TODO think

        return out

    def __iadd__(self, other):
        # quality of life for the discrete convolution stuff
        if not self:
            return other
        elif not other:
            return self
        else:
            return other + self

    def __mul__(self, other):
        """This is NOT the multiplication, but the continuous convolution from 0 to T. We never really need the
        multiplication, so I used the operator *.
        TODO maybe use another and put NotImplemented here to make it less confusing."""

        intervals = []
        polys = []

        for I1, pI1 in self.pairs:
            for I2, pI2 in other.pairs:
                new_ints = interval_convolution(I1, I2)
                intervals += new_ints


                """             
                Here we are computing the convolution:
                        int p(T') q(T-T') dT'
                In the original formulation we have something with indicator functions inside, but these can be formed
                into another interval so they basically only influence the borders of the integral.
                """

                # since sympy does not allow constant polynomials to be evaluated, I need to do this distinction.
                try:
                    q_x = poly(pI2(x), x)  # basically renaming the variable T to x so I can insert T-t below
                    q_eval = q_x(T - t)
                except TypeError:
                    q_eval = pI2  # if it isn't a poly, it is a number


                # this is the poly p(T') * q(T-T') in my paper notation (so the poly inside the conv integral)
                try:
                    p_prod = poly(pI1(t) * q_eval, t)
                except:
                    p_prod = poly(pI1 * q_eval, t)


                # indef integral for the computation of the definite integrals with symbols below
                if isinstance(p_prod, float):
                    integral_p_prod = poly(f'{p_prod}*t')  # p_prod can be 0 or 1
                else:
                    integral_p_prod = p_prod.integrate(t)

                    # below I use this indefinite integral as a function. if the value is 0, it will not be callable because sympy
                    if integral_p_prod == 0:
                        integral_p_prod = lambda y : 0

                a, b = I1  # see calculations in "convolution poly closed form"
                a_, b_ = I2  # see calculations in "convolution poly closed form"
                l1, l2 = length(I1), length(I2)

                # Depending on l1 and l2, I get either 3 or 2 intervals here.
                # The middle part is only added if we get 3 intervals.
                # The integral borders in terms of T can be inferred symbollically calculated by hand.
                p1 = poly(integral_p_prod(T- a_) - integral_p_prod(a), T)
                polys.append(p1)

                if len(new_ints) == 3:
                    p2 = poly(integral_p_prod(T) - integral_p_prod(T - min(l1, l2)), T)
                    polys.append(p2)

                p3 = poly(integral_p_prod(b) - integral_p_prod(T - b_), T)
                polys.append(p3)

        assert not (self.delta and other.delta), (
            "Tried to convolve two deltas - this is not well defined, if this pops "
            "up we might need to think about this more.")

        if self.delta:
            intervals += other.intervals
            polys += other.polys

        if other.delta:
            intervals += self.intervals
            polys += self.polys

        out = VolumePoly(intervals, polys, delta=self.delta or other.delta)

        out.simplify()
        return out

    def __bool__(self):
        return bool(self.polys)

    def time_restriction(self, restriction_inter:tuple):
        # intersect all the intervals with the input interval
        delete_indices = []

        for i, interval in enumerate(self.intervals):
            constrained = intersect(interval, restriction_inter)
            if constrained:
                self.intervals[i] = constrained
            else:
                delete_indices.append(i)

        # the reverse is necessary so that the indices don't get disturbed
        for i in reversed(delete_indices):
            del self.intervals[i]
            del self.polys[i]

    # noinspection PyTypeChecker
    def plot(self):

        num_points = 100

        # Create a colormap
        cmap = plt.get_cmap('tab10')  # You can choose any colormap you prefer

        last_val = 0
        for i, (function, interval) in enumerate(zip(self.polys, self.intervals)):
            start, end = interval

            # If function is not callable, convert it to a lambda function
            if not callable(function):
                f = lambda z: function
            else:
                f = function

            # Generate points within the interval
            x = np.linspace(start, end, num_points)

            # Evaluate the function at each point
            y = [f(point) for point in x]

            ## stryictly speaking, at the border points we want something like the sum of the two polys.
            ## under the assumption that we get continuous volumes, we can do the below.
            # if self.n not in [0,1]:
            #     plt.scatter(x[-1], 2*y[-1], color = 'black', s = 6)

            # Get color from the colormap TODO - they mix and it looks bad/confusing
            color = cmap(
                i % cmap.N)  # Looping over colors in case the number of functions exceeds the number of colors in the colormap


            plt.plot(x, y, label=f"$V_n^e$ on [{start}, {end}]", color=color)

            # Plot interval boundaries
            plt.axvline(x=start, linestyle='--', color='grey', alpha=0.5)  # Start of interval
            plt.axvline(x=end, linestyle='--', color='grey', alpha=0.5)  # End of interval

        # Ensure that (0, 0) is included in the plot
        plt.xlim(left=min(0, plt.xlim()[0]), right=max(0, plt.xlim()[1]))
        plt.ylim(bottom=min(0, plt.ylim()[0]), top=max(0, plt.ylim()[1]))


        plt.xlabel('T')
        plt.ylabel(r'$V^e_{n}(T)$       ', rotation = 0)
        plt.title(f'Slice Volume:\ne = {self.exp}, n = {self.n}.')
        # plt.legend()
        plt.grid(False)  # Remove background lattice
        plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        plt.show()


if __name__ == '__main__':
    p = poly("1 + T", T)
    q = poly("T", T)

    ## This appears to work as intended:
    # tmp_poly = poly(q(x), x)
    # p_prod = poly(p(t) * tmp_poly(T - t), t)

    interval_p = (4, 5)
    interval_q = (3, 7)

    vol1 = VolumePoly([interval_p, interval_q], [p, q])

    # vol1.simplify()
    # print(vol1)

    vol2 = VolumePoly([(1, 2), ], [poly('7*T', T)])

    print(vol1 + vol2)

    print(f"addition: {vol1 + vol2}")  # checked by hand
    print(f"Convolution: {vol1 * vol2}")  # checked by wolfram (assuming my integration intervals are correct)