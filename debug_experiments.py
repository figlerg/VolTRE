import time

from antlr4 import FileStream, CommonTokenStream
from matplotlib import pyplot as plt

from parse.SyntaxError import HardSyntaxErrorStrategy
from slice_volume import slice_volume
from parse.TRELexer import TRELexer
from parse.TREParser import TREParser
from os.path import join

from visualize_recursion import generate_syntax_tree


## PARSING

input_stream = FileStream(join('parse', 'test_spec.txt'))
print(f'input: {input_stream}')

lexer = TRELexer(input_stream)
stream = CommonTokenStream(lexer)
parser = TREParser(stream)
parser._errHandler = HardSyntaxErrorStrategy()
ctx = parser.expr()

### SUBEXPERIMENT

case = 1


# fixed n
if case == 0:
    n = 1

    a = time.time()
    test = slice_volume(ctx, n)
    b = time.time()

    print(f"Computation complete for n = {n} and exp = {ctx.getText()}.\n"
          f"Elapsed time = {b - a}s")

    test.plot()


# VARY n
if case == 1:
    n_max = 30

    ts = []
    for n in range(n_max):
        a = time.time()
        test = slice_volume(ctx, n)
        b = time.time()

        print(f"Computation complete for n = {n} and exp = {ctx.getText()}.\n"
              f"Elapsed time = {b - a}s")
        ts.append(b - a)

        print(test)

        test.plot()

    # this goes up to ~20s with the cache, so we got a huge speedup by remembering the results
    plt.plot(ts)
    plt.show()


