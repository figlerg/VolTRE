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

from experiments.generate_TAkiller import Subfamily, generate_expression
from parse.TREParser import TREParser
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


# Use the PDF backend which doesn't require LaTeX installed
plt.rcParams.update({
    "pgf.texsystem": "pdflatex",  # Use pdflatex (commonly available)
    "font.family": "serif",       # Use serif fonts (like LaTeX)
    "text.usetex": True,          # Enable LaTeX rendering
    "pgf.rcfonts": False,         # Disable font setup for consistency
})


ctx : TREParser.IntersectionExprContext = quickparse('spec_05_thicktwin.tre')

# PAPER

random.seed(0)
np.random.seed(0)

def experiment():
    ns = [5,15,25]
    alphas = [0.1, 0.5, 0.9]

    nr_samples = 10  # just for getting an empirical mean

    def T_maker(n, alpha):
        return alpha*n/2

    times = {}
    piece_counts = {}

    rej_means = np.zeros((len(ns), len(alphas)))

    for i, n in enumerate(ns):
        for j, alpha in enumerate(alphas):
            print(n,alpha)

            if n == 15 and alpha == 0.9:
                print(T_maker(n,alpha))
                v1 = slice_volume(ctx.expr(0), n)
                v1.plot()

                print('---')
                v2 = slice_volume(ctx.expr(1), n)
                v2.plot()

            for _ in range(nr_samples):

                t_a = time.time()


                try:
                    w, rej = sample(ctx, n, T_maker(n, alpha), feedback=True,budget=1500)
                    print(rej)
                except AssertionError:
                    print(slice_volume(ctx.children[0], n))
                    raise Exception



                t_b = time.time()

                t = t_b - t_a

                rej_means[i,j] += rej.intersect_rej

                # times.append(t)
                # sizes.append(v_n.size)

    rej_means /= nr_samples

    # print(times)
    # print(sizes)

    print(rej_means)

pr = cProfile.Profile()
pr.enable()
experiment()
pr.disable()
pr.dump_stats("05thicktwin.prof")

# # Profile the function - THIS CAN'T BE USED WITH SNAKEVIZ
# cProfile.run('experiment()', 'main.prof')
#
# Print the profiling results
p = pstats.Stats("05thicktwin.prof")
p.strip_dirs().sort_stats('cumulative').print_stats(10)
