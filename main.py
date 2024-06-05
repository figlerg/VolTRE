# for now try to generate the multiset of intervals automatically
import random
import cProfile
import pstats

from os.path import join, curdir

from parse.quickparse import quickparse
from sample.TimedWord import TimedWord
from volume.slice_volume import slice_volume
from sample.sample import sample



ctx = quickparse(join('parse', 'test_spec.txt'))
print(ctx.getText())



def experiment():
    n = 10

    V = slice_volume(ctx, n, debug_mode=False)

    V.fancy_print()
    V.plot()

    T = 3.7

    random.seed(42)

    s1: TimedWord = sample(ctx, n, T)

    print(s1, s1.duration)

# Profile the function
cProfile.run('experiment()', 'profiling_results')

# Print the profiling results
p = pstats.Stats('profiling_results')
p.strip_dirs().sort_stats('cumulative').print_stats(30)
