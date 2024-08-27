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
ctx = quickparse(join('experiments', 'spec_07_intersection.tre'))
# ctx = quickparse(join('experiments', 'spec_08_renaming.tre'))
# ctx = quickparse(join('experiments', 'spec_09_ambig.tre'))
# ctx = quickparse(join('experiments', 'spec_10_noparse.tre'))
# ctx = quickparse("experiments/spec_08_disambig.tre")
# ctx = quickparse("experiments/spec_19_qest_subset.tre")
# ctx = quickparse("experiments/spec_20_ambig.tre")
# ctx = quickparse("experiments/spec_21_infint.tre")

print(ctx.getText())
ctx2 = rename(ctx)
if ctx.getText() != ctx2.getText():
    ctx = ctx2
    print(f"Applied renaming and got:\n{ctx.getText()}")

# visualizes the tree
# G = generate_syntax_tree(ctx)
# highlight_node(G, str(ctx), comment='')


def experiment():
    random.seed(42)
    np.random.seed(42)


    # print(disambiguate(ctx, return_inverse_map=True))


    n = 1
    # T = 1.7
    nr_samples = 500

    V = slice_volume(ctx, n)
    V.fancy_print()
    V.plot()

    counts = []

    with warnings.catch_warnings():
        warnings.filterwarnings("error", category=UserWarning)

        for i in range(nr_samples):
            # w, feedback = sample(ctx, n, T=T, feedback=True)
            w, feedback = sample(ctx, n=n, feedback=True, mode=DurationSamplerMode.MAX_ENT, lambdas=[-1,])

            counts.append(feedback.rej)  # the rejections of the smart rej sampling

            # print(w)

    # V_e/V_e' = nr_acc/nr_rej
    v_est = V.total_volume()* (nr_samples/(sum(counts)+nr_samples))
    print(f"V(e') =       \t{V.total_volume()}")
    print(f"Accepted...   \t{nr_samples}")
    print(f"Rejections... \t{sum(counts)}")
    print(f"Volume estimate for {ctx.getText()}. n={n} is {v_est}.")



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
