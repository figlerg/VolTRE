# for now try to generate the multiset of intervals automatically
import argparse
import random
import cProfile
import pstats
import time
from math import factorial

import matplotlib.pyplot as plt
from os.path import join, curdir

import numpy as np

from match.match import match
from misc.disambiguate import disambiguate
from parse.quickparse import quickparse
from sample.TimedWord import TimedWord
from visualize_recursion import generate_syntax_tree, highlight_node
from volume.MaxEntDist import MaxEntDist
from volume.slice_volume import slice_volume
from sample.sample import sample, DurationSamplerMode, sample_ambig
from volume.tuning import mu, jacobi, lambdas, parameterize_mean_variance


# TODO this will be the actual way to run it.
# parser = argparse.ArgumentParser(description="Parse a TRE file and generate samples.")
# parser.add_argument('path', type=str, help='Path to the TRE file.')
# args = parser.parse_args()
#
# ctx = quickparse(args.path)


# ctx = quickparse(join('experiments', 'spec_00_test.tre'))
# ctx = quickparse('experiments/spec_08_disambig.tre')
# ctx = quickparse(join('experiments', 'spec_00.tre'))
# ctx = quickparse(join('experiments', 'spec_06.tre'))
# ctx = quickparse(join('experiments', 'TAkiller.tre'))
# ctx = quickparse(join('experiments', 'TAkiller_15_gen.tre'))
# ctx = quickparse(join('experiments', 'TAkiller_Subfamily.STAR_3_gen.tre'))
# ctx = quickparse(join('experiments', 'TAkiller_Subfamily.STAR_5_gen.tre'))
# ctx = quickparse(join('experiments', 'spec_07_intersection.tre'))
# ctx = quickparse(join('experiments', 'spec_08_renaming.tre'))
ctx = quickparse(join('experiments', 'spec_09_ambig.tre'))


print(ctx.getText())

# visualizes the tree
# G = generate_syntax_tree(ctx)
# highlight_node(G, str(ctx), comment='')


def experiment():
    random.seed(42)

    n = 3
    T = 0.7

    # V = slice_volume(ctx, n)
    # V.fancy_print()
    # V.plot()
    #

    for _ in range(10):
        w = sample_ambig(ctx, n)
        print(w)





pr = cProfile.Profile()
pr.enable()
experiment()
pr.disable()
pr.dump_stats("main.prof")


# # Profile the function - THIS CAN'T BE USED WITH SNAKEVIZ
# cProfile.run('experiment()', 'main.prof')
#
# # Print the profiling results
# p = pstats.Stats('main.prof')
# p.strip_dirs().sort_stats('cumulative').print_stats(10)
