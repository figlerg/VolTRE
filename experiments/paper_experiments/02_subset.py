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


# Use the PDF backend which doesn't require LaTeX installed
plt.rcParams.update({
    "pgf.texsystem": "pdflatex",  # Use pdflatex (commonly available)
    "font.family": "serif",       # Use serif fonts (like LaTeX)
    "text.usetex": True,          # Enable LaTeX rendering
    "pgf.rcfonts": False,         # Disable font setup for consistency
})

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


random.seed(42)
np.random.seed(42)

# PAPER
ctx1 = quickparse(join('spec_02_subset_A.tre'))
ctx2 = quickparse(join('spec_02_subset_B.tre'))
# B refines A, so A subset B

# visualizes the tree
# G = generate_syntax_tree(ctx)
# highlight_node(G, str(ctx), comment='')



def experiment():
    random.seed(42)
    np.random.seed(42)

    # print(disambiguate(ctx, return_inverse_map=True))

    n = 10

    # order is misleading: set B refines set A
    is_subset(ctx2, ctx1, n, eps=0.1, alpha=0.1, T=30)

pr = cProfile.Profile()
pr.enable()
experiment()
pr.disable()
pr.dump_stats("02_subset.prof")

# # Profile the function - THIS CAN'T BE USED WITH SNAKEVIZ
# cProfile.run('experiment()', 'main.prof')
#
# # Print the profiling results
# p = pstats.Stats('main.prof')
# p.strip_dirs().sort_stats('cumulative').print_stats(10)
