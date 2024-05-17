import warnings

from math import inf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker

from sympy import poly
from sympy.polys import Poly
from sympy.abc import T, t, x  # I will treat T as the slice duration, and t as the variable in convolutions.

# this is my code
from misc import intersect, length, interval_convolution, determine_convolution_case, ConvolutionCase


class VolumePoly:
    """
    A wrapper class for the piecewise polynomials.
    Each has the form     sum for I in J, p_I 1_I [+ delta in some cases]
    """

    def __init__(self, intervals: list = None, polys: list = None, delta: int = 0):

        self.intervals = intervals if intervals else list()  # empty intervals is just the zero poly
        self.polys = polys if polys else list()
        self.delta = delta

        # during creating with slice_volumes, these are set
        self.exp = None
        self.n = None

    @property
    def pairs(self):
        return zip(self.intervals, self.polys)

    def check(self):
        # TODO I could do a bunch of sanity checks here.
        assert (len(self.intervals) == len(self.polys)), "Invalid poly!"

    def __str__(self):
        out = ''

        for interval, p in zip(self.intervals, self.polys):
            out += f'1_{interval}(T) * {p} + '

        out = out[0:-3]  # get rid of trailing +

        if self.delta:
            out += f' + {int(self.delta)} delta(T)'

        if not out:
            return '0'
        return out

    def fancy_print(self):
        """
        This prints The polynomial in a simpler form, as pairs of intervals and polys. Useful for debugging.
        :return: None
        """
        for i, inter in enumerate(self.intervals):
            print(inter, self.polys[i].as_expr())

    def __repr__(self):
        return self.__str__()

    def simplify_old(self):
        """
        Deprecated! I keep it here just to compare.
        """

        warnings.warn("This function is deprecated - use the .simplify method.", DeprecationWarning)

        c_max = 0
        for i, (a, b) in enumerate(self.intervals):
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

        self.check()

    def simplify(self):

        events = []
        is_infinite = dict()

        # this loop builds the event queue (unsorted)
        for i, (a, b) in enumerate(self.intervals):
            if a != inf:
                # this tuple has:
                #       i           ... index of the right interval/poly in the lists
                #       a           ... the actual value for sorting in the event queue
                #       True        ... True indicates that it is the left boundary of the interval
                events.append((i, a, True))
            else:
                raise Exception('Invalid interval.')

            if b != inf:
                #       i           ... index of the right interval/poly in the lists
                #       b           ... the actual value for sorting in the event queue
                #       False        ... False indicates that it is the right boundary of the interval
                events.append((i, b, False))
            else:
                is_infinite[i] = True

        events.sort(key=lambda y: y[1])  # I sort for the values (so the border points of the intervals).
        # Python uses Timsort, a hybrid sorting algo with O(n log n), so this influences the complexity.

        current_poly = Poly('0', T)

        current_interval_start = 0

        intervals = []
        polys = []



        for i, val, is_start in events:
            delta_poly = self.polys[i]  # this is either added or subtracted later

            # this flag will signify that we didn't progress in time with this event, leading to some special cases
            simultaneous_events = val == current_interval_start

            # skip 0 after adding poly
            if val == 0:
                current_poly += delta_poly
                continue


            # 1) normal case: the interval of this event is the only event happening at this val.
            #  We also skip val==0 here, since we always start an interval here.
            #  We skip current_poly==0 just to ignore a leading zero poly as it's not necessary
            if not simultaneous_events and current_poly:
                intervals.append((current_interval_start, val))
                polys.append(current_poly)

            # 2) multiple interval borders at same time
            else:
                pass


            # It doesn't matter what case we are in above, the current poly is always updated.
            # Here it is clear, that for finite intervals it will always be zero in the end since we add and subtract
            # each poly once. (Only at t=0 do we not do not enter here, but still add the poly above so the invariant
            # holds.)
            current_interval_start = val
            if is_start:
                current_poly += delta_poly
            else:
                current_poly -= delta_poly


        # Handle case for intervals that extend to infinity
        if current_poly != Poly('0', T):
            intervals.append((current_interval_start, inf))
            polys.append(current_poly)

        self.intervals = intervals
        self.polys = polys

        return None

    def __add__(self, other):
        intervals = self.intervals + other.intervals
        polys = self.polys + other.polys
        delta = int(self.delta) + int(other.delta)
        # TODO this is not nice, because in our fragment it could still be that both have epsilon,
        #  and then we could end up with two diracs... In that case I am not sure what wouldbe the canonical way.

        # assert not (self.delta and other.delta), "Problem with dirac"
        # THIS REALLY HAPPENS! REASON: the way I am aggregating things in the kleene recursion leads to multiple kleene polys being added (discrete convolution).

        out = VolumePoly(intervals, polys, delta=delta)

        out.simplify()  # not strictly necessary, but probably we do this every time? TODO think

        out.check()

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
        """
        scalar multiplication - TODO not sure what the canonical way is. I just want to multiply with ints
        :param other:
        :return:
        """
        assert isinstance(other, int), "For now only poly * int is supported."

        polys = []
        for p in self.polys:
            polys.append(p * other)

        intervals = self.intervals.copy()
        delta = int(self.delta) * other

        out = VolumePoly(intervals, polys, delta)
        out.n = self.n

        out.check()

        return out

    def __pow__(self, other):
        """
        This is the convolution of two functions: int_0^T f(T') g(T-T') dT'
        """

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

                q_x = poly(pI2(x), x)  # basically renaming the variable T to x so I can insert T-t below
                q_eval = q_x(T - t)
                p_prod = poly(pI1(t) * q_eval, t)

                # indef integral for the computation of the definite integrals with symbols below
                integral_p_prod = p_prod.integrate(t)

                a1, b1 = I1  # see calculations in "convolution poly closed form"
                a2, b2 = I2  # see calculations in "convolution poly closed form"
                l1, l2 = length(I1), length(I2)

                # Depending on l1 and l2, I get either 3 or 2 intervals here.
                # The middle part is only added if we get 3 intervals.
                # The integral borders in terms of T can be inferred symbollically calculated by hand.

                case = determine_convolution_case(I1, I2)

                # I always compute the three polys, but in some cases below only some of them are added to the list.
                # For the logic, draw the five pictures of the case distinction! TODO I will provide my notes somewhere in this repo.

                # this poly is always in the first interval, no matter the case.
                p1 = poly(integral_p_prod(T - a2) - integral_p_prod(a1), T)

                # Depending on the case (also the infinite ones) and which length is bigger, this is the 2nd poly.
                if l1 < l2:
                    p2 = poly(integral_p_prod(b1) - integral_p_prod(a1), T)
                elif l1 > l2:
                    p2 = poly(integral_p_prod(b2) - integral_p_prod(a2), T)
                else:
                    p2 = None

                # this is added only in the last case
                p3 = poly(integral_p_prod(b1) - integral_p_prod(T - b2), T)

                match case:
                    case ConvolutionCase.BOTH_INFINITE:
                        polys.append(p1)  # on [0,                      inf)

                    case ConvolutionCase.FIRST_INFINITE:
                        polys.append(p1)  # on [a1 + a2,                a1 + a2 + l2]
                        polys.append(p2)  # on [a1+ a2 + l2,            inf)

                    case ConvolutionCase.SECOND_INFINITE:
                        polys.append(p1)  # on [a1 + a2,                a1 + a2 + l1]
                        polys.append(p2)  # on [a1+ a2 + l1,            inf)

                    case ConvolutionCase.BOTH_FINITE_SAME_LENGTH:
                        polys.append(p1)  # on [a1 + a2,                a1 + a2 + l]
                        polys.append(p3)  # on [a1 + a2 + l,            b1 + b2]

                    case ConvolutionCase.BOTH_FINITE_DIFFERENT_LENGTH:
                        polys.append(p1)  # on [a1 + a2,                a1 + a2 + min(l1,l2)]
                        polys.append(p2)  # on [a1 + a2 + min(l1,l2),   a1 + a2 + max(l1,l2)]
                        polys.append(p3)  # on [a1 + a2 + max(l1,l2),   b1 + b2]

        assert len(intervals) == len(polys), "Convolution bug, invalid VolumePoly created."

        assert not (self.delta and other.delta), (
            "Tried to convolve two deltas - this is not well defined, if this pops "
            "up we might need to think about this more.")

        if self.delta:
            # print(f"Convolution of delta = {self.delta} with {other}")
            intervals += other.intervals
            polys += [int(self.delta) * p for p in other.polys]
            pass

        if other.delta:
            # print(f"Convolution of delta = {other.delta} with {self}")
            intervals += self.intervals
            polys += [int(other.delta) * p for p in self.polys]
            pass

        out = VolumePoly(intervals, polys, delta=False)

        # out.fancy_print()
        out.simplify()
        # out.fancy_print()

        return out

    def __bool__(self):
        return bool(self.polys) or bool(self.delta)

    def __eq__(self, other):
        # TODO I think this doesn't actually work, not sure why.
        alphanum = lambda x: str(x)

        return (sorted(self.intervals, key=alphanum) == sorted(other.intervals, key=alphanum) and
                sorted(self.polys, key=alphanum) == sorted(other.polys, key=alphanum))

    def time_restriction(self, restriction_inter: tuple):
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

    def plot(self, no_show=False):

        num_points = 100

        # Create a colormap
        cmap = plt.get_cmap('tab10')  # You can choose any colormap you prefer

        last_val = 0
        for i, (function, interval) in enumerate(zip(self.polys, self.intervals)):

            start, end = interval

            inf_flag = False
            if end == inf:
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
            y = [float(f(point)) for point in x]

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
            if i == len(self.intervals)-1 and inf_flag:

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
                new_labels = [f'{int(tick)}' for tick in current_ticks[:-3]] + [r'$\cdots$', r'$\infty$','']

                new_ticks = list(current_ticks)
                # Set the x-tick labels
                ax.set_xticks(new_ticks)
                ax.set_xticklabels(new_labels)

        # Ensure that (0, 0) is included in the plot
        plt.xlim(left=min(0, plt.xlim()[0]), right=max(0, plt.xlim()[1]))
        plt.ylim(bottom=min(0, plt.ylim()[0]), top=max(0, plt.ylim()[1]))

        plt.xlabel('T')
        plt.ylabel(r'$V^e_{n}(T)$       ', rotation=0)
        plt.title(f'Slice Volume:\ne = {self.exp}, n = {self.n}.')
        # plt.legend()
        plt.grid(False)  # Remove background lattice
        plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))


        if not no_show:
            plt.show()

    def copy(self):
        """
        Method for deepcopy.
        :return: Deepcopy of self.
        """
        intervals = self.intervals.copy()
        polys = self.polys.copy()

        return VolumePoly(intervals, polys, self.delta)

    def volume(self):

        """
        Evaluates the int _0 ^inf self(x) dx. Admits infinite values.
        :return: Overall volume V_n(e)
        """

        out = 0

        for interval, p in zip(self.intervals, self.polys):
            a,b = interval

            antiderivative = p.integrate(T)
            segment_vol = antiderivative(b) - antiderivative(a)  # this often knows how to deal with inf, it seems.

            out += segment_vol

        return out

    def __call__(self, x):

        assert x >= 0, "VolumePolys are defined on R+."

        out = 0

        # We can assume that the list of intervals is sorted and not overlapping, since we always simplify.
        for i, (a,b) in enumerate(self.intervals):
            cur_p = self.polys[i]

            if a <= x <= b:
                # technically not the optimal solution, but it works also with not simplified polys.
                out += cur_p(x)

            if a == x or b == x:
                warning = f"""
                You are trying to evaluate the function {self} on the point {x} which is on the
                boundary of an interval. It is not clear a priori how to evaluate this, but the 
                sensible thing to do is to add the left and right limit of this point. 
                Be aware that this is not the continuous extension, but it makes more sense for slice 
                volumes. Since these points are a null-set, it doesn't matter when integrating over it.
                """

                warnings.warn(warning, UserWarning)

        return out





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

    # print(f"addition: {vol1 + vol2}")  # checked by hand
    # print(f"Convolution: {vol1 ** vol2}")  # checked by wolfram (assuming my integration intervals are correct)

    vol1.fancy_print()
    print('')
    vol1.simplify() # checked by hand (the new simplify)
    vol1.fancy_print()
    print('')

    """
    test for the integral below checks out
    (3, 4) T
    (4, 5) 2*T + 1
    (5, 7) T
    
    -> T^2 /2       on [3,4]
    -> 2T^2/2 + T   on [4,5]
    -> T^2/2        on [5,7]
    
    checks out with value below
    """

    # integrate from 0 to inf
    print(vol1.volume())

    # eval works too it seems
    print(vol1(4.5))
    try:
        print(vol1(-1))
    except AssertionError:
        print("Successfully caught invalid input.")
