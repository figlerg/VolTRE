# for now try to generate the multiset of intervals automatically
import random
import cProfile

from os.path import join

import numpy as np

from misc.disambiguate import disambiguate
from misc.rename import rename
from parse.quickparse import quickparse
from probabilistic.volume_estimate import volume_estimate
from volume.slice_volume import slice_volume

ctx = quickparse(join('..', 'spec_09_ambig.tre'))

print(ctx.getText())
ctx2 = rename(ctx)
if ctx.getText() != ctx2.getText():
    ctx = ctx2
    print(f"Applied renaming and got:\n{ctx.getText()}")  # TODO might put this into the sampling itself.

# visualizes the tree
# G = generate_syntax_tree(ctx)
# highlight_node(G, str(ctx), comment='')


def experiment():
    random.seed(42)
    np.random.seed(42)


    # print(disambiguate(ctx, return_inverse_map=True))


    n = 1
    # T = 1.7
    nr_samples = 1000
    conf = 0.95

    # print("This volume is not real! We can't compute it with ambiguity.")
    V = slice_volume(quickparse(disambiguate(ctx), string=True), n)
    V.fancy_print()
    # V.plot()

    v_est, (a,b) = volume_estimate(node=ctx, n=n, nr_samples=nr_samples, gamma=conf, mode='pearson')


pr = cProfile.Profile()
pr.enable()
experiment()
pr.disable()
pr.dump_stats("03_volume.prof")


# # Profile the function - THIS CAN'T BE USED WITH SNAKEVIZ
# cProfile.run('experiment()', 'main.prof')
#
# # Print the profiling results
# p = pstats.Stats('main.prof')
# p.strip_dirs().sort_stats('cumulative').print_stats(10)
