


class TimedWord:
    """
    Just a little container for the timed words, with some utility functions.
    """

    def __init__(self, symbols : list, delays : list):
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
        return str(tuple(zip(self.symbols, self.delays)))

    def __iter__(self):
        return zip(self.symbols, self.delays)

    @property
    def length(self):
        assert len(self.symbols) == len(self.delays), "Invalid timed word."
        return len(self.symbols)

    @property
    def duration(self):
        assert len(self.symbols) == len(self.delays), "Invalid timed word."
        return sum(self.delays)



if __name__ == '__main__':
    symbols = ['a', 'a', 'c']
    delays = [1,0.5,7]

    w = TimedWord(symbols, delays)

    print(w)
    print(w.length())
    print(w.duration())