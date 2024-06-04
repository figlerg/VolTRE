# for now try to generate the multiset of intervals automatically
import random
import cProfile
import pstats

from antlr4 import FileStream, CommonTokenStream

from parse.SyntaxError import HardSyntaxErrorStrategy
from parse.TRELexer import TRELexer
from parse.TREParser import TREParser

from os.path import join, curdir
from os import listdir

from parse.quickparse import quickparse
from sample.TimedWord import TimedWord
from volume.slice_volume import slice_volume
from sample.sample import sample

ctx = quickparse(join('parse', 'test_spec.txt'))
print(ctx.getText())
n = 10

V, cache = slice_volume(ctx, n, debug_mode=False, return_cache = True)  # debug mode generates files in vis_cache

V.fancy_print()
# V.plot()

T = 3.7

seed = random.seed(42)



def experiment():
    # Your code here
    s: TimedWord = sample(ctx, n, T, cache)
    print(s)

# Profile the function
cProfile.run('experiment()', 'profiling_results')

# Print the profiling results
p = pstats.Stats('profiling_results')
p.strip_dirs().sort_stats('cumulative').print_stats(10)



# print(s)

# a_count = 0
# b_count = 0
#
# n_samples = 100
#
# points = []
# for i in range(n_samples):
#     s:TimedWord = sample(ctx, n, T, cache)
#
#
#
#     for letter, delay in s:
#         if letter == 'a':
#             a_count +=1
#         if letter == 'b':
#             b_count +=1
#
#         # if letter == 'a':
#         #     point = ()
#         # elif letter == 'b':
#
#     # print(s)
#     # print(s.get_duration())
#
# print(a_count / n_samples)
# print(b_count / n_samples)
# print(a_count / b_count)

