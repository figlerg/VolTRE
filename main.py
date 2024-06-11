# for now try to generate the multiset of intervals automatically
import random
import cProfile
import pstats

from os.path import join, curdir

import matplotlib.pyplot as plt

from parse.quickparse import quickparse
from sample.TimedWord import TimedWord
from visualize_recursion import generate_syntax_tree, highlight_node
from volume.slice_volume import slice_volume
from sample.sample import sample



# ctx = quickparse(join('experiments', 'working_example.txt'))
ctx = quickparse(join('experiments', 'spec_00.txt'))
print(ctx.getText())

# visualizes the tree
G = generate_syntax_tree(ctx)
highlight_node(G, str(ctx), comment='')


def experiment():
    n = 4

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
p.strip_dirs().sort_stats('cumulative').print_stats(10)
