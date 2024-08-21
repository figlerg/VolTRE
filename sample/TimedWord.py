import math
import numpy as np


class TimedWord:
    """
    Just a little container for the timed words, with some utility functions.
    """

    def __init__(self, symbols : list, delays : list):
        assert len(symbols) == len(delays), ("Tried to instantiate an invalid timed word. "
                                             "Symbols and delays need to have same length.")
        self.symbols = symbols
        self.delays = delays

    def __mul__(self, other):
        """
        Concatenation of two timed words.
        :param other: TimedWord object.
        :return: TimedWord object for the concatenation.
        """
        return TimedWord(self.symbols + other.symbols, self.delays + other.delays)

    def __str__(self):
        if self:
            # return str(tuple(zip(self.symbols, self.delays)))
            pairs = zip(self.delays, self.symbols)
            # I switch the order here on purpose... Nicolas says I should print delay, sym
            out = ','.join([f"({float(delay):.3f}, {symbol})" for delay, symbol in pairs])
            return out


        else:
            return 'EPS'

    def __iter__(self):
        return zip(self.symbols, self.delays)

    def __bool__(self):
        return bool(self.symbols)

    def __getitem__(self, item):

        if isinstance(item, slice):
            # Get the start, stop, and step from the slice
            return TimedWord(self.symbols[item], self.delays[item])

        return tuple(self.__iter__())[item]

    @property
    def length(self):
        assert len(self.symbols) == len(self.delays), "Invalid timed word."
        return len(self.symbols)

    @property
    def duration(self):
        assert len(self.symbols) == len(self.delays), "Invalid timed word."
        return sum(self.delays)

    def is_epsilon(self):
        return not bool(self.symbols)

    @property
    def dates(self):
        return np.cumsum(self.delays)

    def iota_k(self):
        """
        For testing we want iota and k of the sample.
        :return: integer iota and k
        """

        tau, iota = math.modf(self.dates[-1])  # fractional part, integer part
        iota = int(iota)
        k = len([t % 1 for t in self.dates[:-1] if t % 1 < tau])  # count the nr of lower fractional parts for rank

        return iota, k

    def region_index(self) -> tuple:
        """
        Just computes the vector (iota1, ..., iotan, k1,...,kn), i.e. the index of the region.
        :return: Tuple (iota1, ..., iotan, k1,...,kn)
        """

        dates = self.dates

        index = []

        for t in dates:
            index.append(int(t - t % 1))

        frac_parts = [t % 1 for t in dates]
        sigma = infer_permutation(frac_parts, sorted(frac_parts))

        sigma_inv = {sigma[i]:i for i in range(len(sigma))}

        for i in range(len(frac_parts)):
            # just so it matches the math on paper, we start at 1
            index.append(sigma_inv[i] + 1)

        return tuple(index)

    def apply_renaming(self, rename_map:dict):
        for i, s in enumerate(self.symbols):
            self.symbols[i] = rename_map[s]


# helper to infer the permutation
def infer_permutation(a, b):
    if sorted(a) != sorted(b):
        raise ValueError("b is not a permutation of a")

    # Create a mapping from value to index for b
    b_index_map = {value: idx for idx, value in enumerate(b)}

    # Find the permutation by mapping the indices of a to the indices of b
    permutation = [b_index_map[value] for value in a]

    return permutation


if __name__ == '__main__':
    symbols = ['a', 'a', 'c']
    delays = [1,0.5,7]

    w = TimedWord(symbols, delays)

    print(w)