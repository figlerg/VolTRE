# for now try to generate the multiset of intervals automatically
import argparse
import random
import cProfile
import pstats
import time
import warnings
from math import factorial
import pandas as pd

import matplotlib.pyplot as plt
from os.path import join, curdir

import numpy as np

from experiments.generate_TAkiller import Subfamily, generate_expression
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


# PAPER

random.seed(42)
np.random.seed(42)

"""
BENOIT:
TA Killer

n TRE T "execution time"
2 <a<b+>_[0,1]>_[0,2] 1.0 0.01  
3 <a<b<c+>_[0,1]>_[0,2]>_[0,3] 1.5 0.01  
4 <a<b<c<d+>_[0,1]>_[0,2]>_[0,3]>_[0,4] 2.0 0.06  
5 <a<b<c<d<e+>_[0,1]>_[0,2]>_[0,3]>_[0,4]>_[0,5] 2.5 1.45  
6 <a<b<c<d<e<f+>_[0,1]>_[0,2]>_[0,3]>_[0,4]>_[0,5]>_[0,6] 3.0 24.93 
7 <a<b<c<d<e<f<g+>_[0,1]>_[0,2]>_[0,3]>_[0,4]>_[0,5]>_[0,6]>_[0,7] Out of memory > 30GB
timeword of length n, alpha= 0.5
"""



def experiment():
    family_n = 10
    alpha = 0.5
    # letters_n = 15
    nr_samples = 10
    df = pd.DataFrame({
        'n': pd.Series(dtype='int'),                  # First column 'n' is integer
        'TRE': pd.Series(dtype='float'),              # Second column 'TRE' is float
        'T': pd.Series(dtype='float'),                # Third column 'T' is float
        'execution time': pd.Series(dtype='float')    # Fourth column 'execution time' is float
    })

    for n in range(2, family_n):

        mode = Subfamily.VANILLA
        expr = generate_expression(n, mode)
        print(expr)

        T = alpha*n

        t_a = time.time()
        for _ in range(nr_samples):
            # v_n = slice_volume(quickparse(expr, string=True), n=family_n)
            # print(v_n)
            w = sample(quickparse(expr, string=True),n=n, T=T)
        t_b = time.time()

        comp_t = t_b - t_a

        new_tuple = {'n': n, 'TRE': expr, 'T': T, 'execution time': comp_t}
        df = df._append(new_tuple, ignore_index=True)

    # Ensure that the 'n' column is treated as an integer
    df['n'] = df['n'].astype(int)

    # Save to CSV, specifying no decimal points for floats
    df.to_csv('04_TAkiller.csv', sep=' ', index=False, float_format='%.2f')


pr = cProfile.Profile()
pr.enable()
experiment()
pr.disable()
pr.dump_stats("04_TAkiller.prof")

# # Profile the function - THIS CAN'T BE USED WITH SNAKEVIZ
# cProfile.run('experiment()', 'main.prof')
#
# # Print the profiling results
# p = pstats.Stats('main.prof')
# p.strip_dirs().sort_stats('cumulative').print_stats(10)
