import time

from antlr4 import FileStream, CommonTokenStream
from matplotlib import pyplot as plt

from parse.SyntaxError import HardSyntaxErrorStrategy
from slice_volume import slice_volume
from parse.TRELexer import TRELexer
from parse.TREParser import TREParser
from os.path import join



## PARSING

input_stream = FileStream(join('parse', 'test.txt'))
print(f'input: {input_stream}')

lexer = TRELexer(input_stream)
stream = CommonTokenStream(lexer)
parser = TREParser(stream)
parser._errHandler = HardSyntaxErrorStrategy()
ctx = parser.expr()





### SUBEXPERIMENT

case = 0






# VARY N
if case == 0:
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

# SUSPICIOUS TEST
if case == 1:
    n = 6
    a = time.time()
    test = slice_volume(ctx, n)
    b = time.time()

    print(f"Computation complete for n = {n} and exp = {ctx.getText()}.\n"
          f"Elapsed time = {b - a}s")

    test.plot()

    a = time.time()
    n1 = 5
    n2 = 1
    testa = slice_volume(ctx, n1)
    testb = slice_volume(ctx, n2)
    testa.delta = False
    test2 = testa ** testb
    test2.n = f'{n1} + {n2}'
    test2.exp = ctx.expr().getText() + '.' + ctx.getText()
    b = time.time()

    print(f"Computation 2 complete for n = {n1} + {n2} and exp = {test2.exp}.\n"
          f"Elapsed time = {b - a}s")

    test2.plot()

    a = time.time()
    n1 = 2
    n2 = 4
    testa = slice_volume(ctx, n1)
    testa.delta = False
    testb = slice_volume(ctx, n2)
    test3 = testa ** testb
    test3.n = f'{n1} + {n2}'
    test3.exp = ctx.expr().getText() + '.' + ctx.getText()
    b = time.time()

    print(f"Computation 3 complete for n = {n1} + {n2} and exp = {test3.exp}.\n"
          f"Elapsed time = {b - a}s")

    print(f"test2 == test3: {test2 == test3}")

    test3.plot()

    a = time.time()
    n1 = 1
    n2 = 5
    testa = slice_volume(ctx, n1)
    testb = slice_volume(ctx, n2)
    testa.delta = False
    test3 = testa ** testb
    test3.n = f'{n1} + {n2}'
    test3.exp = ctx.expr().getText() + '.' + ctx.getText()
    b = time.time()

    print(f"Computation 3 complete for n = {n1} + {n2} and exp = {test3.exp}.\n"
          f"Elapsed time = {b - a}s")

    print(f"test2 == test3: {test2 == test3}")

    test3.plot()


# SUSPICIOUS TEST
if case == 2:
    n = 6
    a = time.time()
    test = slice_volume(ctx, n)
    b = time.time()

    print(f"Computation complete for n = {n} and exp = {ctx.getText()}.\n"
          f"Elapsed time = {b - a}s")

    test.plot()
