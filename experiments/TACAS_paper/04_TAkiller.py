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


random.seed(42)
np.random.seed(42)

# PAPER

random.seed(42)
np.random.seed(42)

def experiment():
    family_n = 15
    letters_n = 15



    times = []
    sizes = []
    for n in range(1, family_n):

        mode = Subfamily.VANILLA
        expr = generate_expression(n, mode)
        print(expr)

        t_a = time.time()
        v_n = slice_volume(quickparse(expr, string=True), n=letters_n)

        print(v_n)
        t_b = time.time()

        t = t_b - t_a

        times.append(t)
        sizes.append(v_n.size)

    print(times)
    print(sizes)

    # Create subplots: 2 rows and 1 column
    fig, axs = plt.subplots(2, 1, figsize=(10, 10))

    # Plot the execution times in the first subplot
    axs[0].plot(range(1, family_n), times, marker='o', color='b', linestyle='-', label='Execution Time')
    axs[0].set_title('Execution Time for Different Values of n', fontsize=16)
    axs[0].set_xlabel('n (TAkiller Size)', fontsize=14)
    axs[0].set_ylabel('Time (seconds)', fontsize=14)
    axs[0].grid(True)

    # Plot the sizes in the second subplot
    axs[1].plot(range(1, family_n), sizes, marker='s', color='g', linestyle='--', label='Volume Size')
    axs[1].set_title('Poly Size for Different Values of n', fontsize=16)
    axs[1].set_xlabel('n (TAkiller Size)', fontsize=14)
    axs[1].set_ylabel('Volume Size', fontsize=14)
    axs[1].grid(True)

    # Adjust layout for better spacing
    plt.tight_layout()

    # Show the plot
    plt.show()
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
