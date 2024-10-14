# for now try to generate the multiset of intervals automatically
import random
import cProfile
import time
import re

import matplotlib.pyplot as plt

import numpy as np

from experiments.generate_TAkiller import Subfamily, generate_expression
from parse.quickparse import quickparse
from volume.slice_volume import slice_volume

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
    family_n = 10
    letters_n = 10

    mode = Subfamily.VANILLA
    expr = generate_expression(family_n, mode)
    print(expr)


    t_a = time.time()
    v_n = slice_volume(quickparse(expr, string=True), n=letters_n)
    t_b = time.time()
    # print(v_n)

    t = t_b - t_a

    expr = expr.replace('<', r'\langle ')
    expr = expr.replace('>', r'\rangle ')
    expr = expr.replace('[', r'{[')
    expr = expr.replace(']', r']}')
    expr = expr.replace('*', '^*')
    expr = '$' + expr + '$'


    # Replace each number with '_{number}'
    pattern = r'(\d+)'
    expr = re.sub(pattern, r'_{\1}', expr)

    print(expr)

    print(f"Volume function with {len(v_n.polys)} pieces.")
    v_n.fancy_print()

    plt.figure(figsize=(6, 3))

    v_n.plot(plt_title=' ', no_show=True)
    print(f"Computation time: {t}s")

    plt.savefig('04_TAkiller.pdf', format='pdf',dpi=300, bbox_inches='tight')


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
