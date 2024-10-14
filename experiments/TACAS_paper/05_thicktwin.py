# for now try to generate the multiset of intervals automatically
import argparse
import random
import cProfile
import pstats
import time
import warnings
from math import factorial, inf

import matplotlib.pyplot as plt
from os.path import join, curdir

import numpy as np

from experiments.generate_TAkiller import Subfamily, generate_expression
from misc.helpers import BudgetExhaustedException, InverseSamplingException
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
import pandas as pd


# Use the PDF backend which doesn't require LaTeX installed
plt.rcParams.update({
    "pgf.texsystem": "pdflatex",  # Use pdflatex (commonly available)
    "font.family": "serif",       # Use serif fonts (like LaTeX)
    "text.usetex": True,          # Enable LaTeX rendering
    "pgf.rcfonts": False,         # Disable font setup for consistency
})


ctx : TREParser.IntersectionExprContext = quickparse('spec_05_thicktwin.tre')

# PAPER

random.seed(42)
np.random.seed(42)


"""
BENOIT:
Thick twin
 
n alpha T "execution time"
1 0.66 .6 0.01  
3 0.66 1.3 0.01  
5 0.66 1.9 0.01  
7 0.66 2.6 0.03  
9 0.66 3.3 0.07  
11 0.66 3.9 0.18  
13 0.66 4.6 0.44  
15 0.66 5.2 0.98  
17 0.66 5.9 2.10  
19 0.66 6.6 4.28  
21 0.66 7.2 8.32 
timeword of length n numerically unstable for n> 21

(n+1)/2 is the maximum time
(n+1)/2*alpha
"""


def experiment():
    # ns = [5,15,25]
    # alphas = [0.1, 0.5, 0.9]
    # Ts = []

    ns = np.asarray(range(1,23,2))
    Ts = 0.66*(ns+1)/2

    print(Ts)

    # nTs= [(1, 0.6),]
    # nTs= [(1, 0.6), (3, 1.3), (5, 1.9), (7, 2.6), (9, 3.3), (11, 3.9), (13, 4.6), (15, 5.2), (17, 5.9), (19, 6.6), (21, 7.2)]
    nTs = zip(ns, Ts)

    nr_samples = 10  # just for getting an empirical mean

    # def T_maker(n, alpha):
    #     return alpha*n/2

    # execution_time = {}
    # piece_counts = {}

    # df = pd.DataFrame(columns=['n', 'T', 'execution time'])
    df = pd.DataFrame({
        'n': pd.Series(dtype='int'),  # First column is integer
        'T': pd.Series(dtype='float'),  # Second column is float
        'execution time': pd.Series(dtype='float')  # Third column is float
    })




    problem_intersection = set()
    problem_empty = set()
    problem_inverse = set()

    for n,T in nTs:
        print(n,T)

        aggregate = 0

        for _ in range(nr_samples):
            try:
                t_a = time.time()
                w, rej = sample(ctx, n, T, feedback=True,budget=300)
                # print(rej)
                t_b = time.time()
                t = t_b - t_a
            except BudgetExhaustedException:
                print(slice_volume(ctx.children[0], n))
                t = inf
                problem_empty.add((n,T))
                print(f"n={n}, T={T} FAILED (out of budget)")
            except AssertionError:
                t = inf
                problem_intersection.add((n,T))
                print(f"n={n}, T={T} FAILED (empty slice)")
            except InverseSamplingException:
                t = inf
                problem_inverse.add((n, T))
                print(f"n={n}, T={T} FAILED (numerical instability)")

            aggregate += t

        new_triplet = {'n': n, 'T': T, 'execution time': aggregate}
        df = df._append(new_triplet, ignore_index=True)

    # Ensure that the 'n' column is treated as an integer
    df['n'] = df['n'].astype(int)

    # Save to CSV, specifying no decimal points for floats
    df.to_csv('05_thicktwin.csv', sep=' ', index=False, float_format='%.2f')

    # # Save the empty DataFrame to CSV with space as delimiter
    # df.to_csv('04_TAkiller.csv', sep=' ', index=False)

    print(f"Problem tuples:"
          f"\n intersection budget: {problem_intersection}"
          f"\n empty slice        : {problem_empty}"
          f"\n inverse        : {problem_inverse}")

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
