# for now try to generate the multiset of intervals automatically
import random
import cProfile
import pstats
import time
from math import factorial

import matplotlib.pyplot as plt
from os.path import join, curdir
from parse.quickparse import quickparse
from sample.TimedWord import TimedWord
from visualize_recursion import generate_syntax_tree, highlight_node
from volume.MaxEntDist import MaxEntDist
from volume.slice_volume import slice_volume
from sample.sample import sample, DurationSamplerMode
from volume.tuning import mu, jacobi

# ctx = quickparse(join('experiments', 'spec_00.tre'))
# ctx = quickparse(join('experiments', 'spec_06.tre'))
ctx = quickparse(join('experiments', 'TAkiller.tre'))
# ctx = quickparse(join('experiments', 'TAkiller_15_gen.tre'))
print(ctx.getText())

# visualizes the tree
# G = generate_syntax_tree(ctx)
# highlight_node(G, str(ctx), comment='')


def experiment():
    random.seed(42)
    n = 4

    V = slice_volume(ctx, n)
    V.fancy_print()
    # print(float(V.total_volume())- 1/factorial(9))
    # print(float(V.polys[2](2.3)))
    print(f"Volume is continuous: {V.is_cont_piece()}")
    # V.polys[-1] += 2/6
    V.plot()
    # print(w1 := sample(ctx, n))


    # lambdas = (1,1,-1)
    # max_ent = MaxEntDist(V, lambdas)
    # # max_ent.plot()
    #
    # print(f"The jacobi matrix is: \n{jacobi(lambdas, V, 4)}")
    #
    # pdf = max_ent.pdf
    # cdf = max_ent.cdf
    # # pdf.plot()
    # # cdf.plot()
    # print(w2 := sample(ctx, n, mode=DurationSamplerMode.MAX_ENT, lambdas=lambdas))
    #
    # # test = w2[-1]
    # exjskyjsaio= 1



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
