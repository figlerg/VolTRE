# for now try to generate the multiset of intervals automatically
import argparse
import random
import cProfile
import pstats
import time
import warnings
from math import factorial

import matplotlib.pyplot as plt
from os.path import join, curdir

import numpy as np

from probabilistic.subset import is_subset
from match.intersection_match import intersection_match
from match.match import match
from misc.disambiguate import disambiguate
from misc.rename import rename
from parse.quickparse import quickparse
from sample.TimedWord import TimedWord
from visualize_recursion import generate_syntax_tree, highlight_node
from volume.MaxEntDist import MaxEntDist
from volume.slice_volume import slice_volume
from sample.sample import sample_unambig, DurationSamplerMode, sample
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
# ctx = quickparse(join('experiments', 'spec_08_renaming.tre'))
# ctx = quickparse(join('experiments', 'spec_09_ambig.tre'))
# ctx = quickparse(join('experiments', 'spec_10_noparse.tre'))
# ctx = quickparse("experiments/spec_08_disambig.tre")
# ctx = quickparse("experiments/spec_19_qest_subset.tre")
# ctx = quickparse("experiments/spec_20_ambig.tre")
# ctx = quickparse("experiments/spec_21_infint.tre")
# ctx = quickparse(join('experiments', 'spec_21_no_subset_A.tre'))

# PAPER
ctx = quickparse(join('experiments','paper_experiments', 'spec_01_hypercube.tre'))

print(ctx.getText())
ctx_tmp = rename(ctx)
if ctx.getText() != ctx_tmp.getText():
    ctx = ctx_tmp
    print(f"Applied renaming and got:\n{ctx.getText()}")

# visualizes the tree
# G = generate_syntax_tree(ctx)
# highlight_node(G, str(ctx), comment='')

# ctx2 = quickparse(join('experiments', 'spec_21_no_subset_B.tre'))



def experiment():
    random.seed(42)
    np.random.seed(42)


    # print(disambiguate(ctx, return_inverse_map=True))

    n = 3
    # T = 1.7

    delays = []

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    for _ in range(50):
        w = sample(ctx, n, T = 0.5)
        # delays += list(w.delays)

    # plt.eventplot(delays)
    # plt.show()

    # print(w.wordgen_format())

    # print(intersection_match(w,phi=ctx))

    # print(is_subset(ctx, ctx2,n,0.01,0.05))


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
