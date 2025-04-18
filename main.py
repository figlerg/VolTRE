# for now try to generate the multiset of intervals automatically
import argparse
import os.path
import pstats
import random
import cProfile
import matplotlib.pyplot as plt
from os.path import join
import numpy as np
from misc.rename import rename
from parse.quickparse import quickparse
from sample.sample import sample

# TODO make the cmd params a bit nicer, add descriptions
parser = argparse.ArgumentParser(description="Parse a TRE file and generate samples. UNDER CONSTRUCTION")
parser.add_argument('-path', nargs='?', type=str, help='Path to the TRE file.',default=os.path.join('experiments','spec_00.tre'))
parser.add_argument('-n', nargs='?', type=int, default=2, help='Length of words.')
parser.add_argument('-T', nargs='?', type=float, default=None, help='Duration of words.')

args = parser.parse_args()

path = args.path
n = args.n
T = args.T

ctx = quickparse(args.path)
print(ctx.getText())


# apply renamings
ctx_tmp = rename(ctx)
if ctx.getText() != ctx_tmp.getText():
    ctx = ctx_tmp
    print(f"Applied renaming and got:\n{ctx.getText()}")

# visualize the tree
# G = generate_syntax_tree(ctx)
# highlight_node(G, str(ctx), comment='')


def experiment():
    random.seed(42)
    np.random.seed(42)

    # TODO nr_samples as input param
    for _ in range(50):
        w = sample(ctx, n=n, T=T)
        print(w)

    plt.show()


pr = cProfile.Profile()
pr.enable()
experiment()
pr.disable()
pr.dump_stats("main.prof")

# Print the profiling results
p = pstats.Stats('main.prof')
p.strip_dirs().sort_stats('cumulative').print_stats(10)
