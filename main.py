# for now try to generate the multiset of intervals automatically
import random
import cProfile
import pstats
import time

from os.path import join, curdir

import matplotlib.pyplot as plt

from parse.quickparse import quickparse
from sample.TimedWord import TimedWord
from visualize_recursion import generate_syntax_tree, highlight_node
from volume.MaxEntDist import MaxEntDist
from volume.slice_volume import slice_volume
from sample.sample import sample, DurationSamplerMode

# ctx = quickparse(join('experiments', 'working_example.tre'))
ctx = quickparse(join('experiments', 'spec_00.tre'))
print(ctx.getText())

# visualizes the tree
G = generate_syntax_tree(ctx)
highlight_node(G, str(ctx), comment='')


def experiment():
    n = 10

    V = slice_volume(ctx, n, debug_mode=False)

    # V.fancy_print()
    # V.plot()

    T = 0.5

    random.seed(42)

    # s1: TimedWord = sample(ctx, n, T)
    #
    # print(s1, s1.duration)


    lambdas = [1,1,-1]
    max_ent = MaxEntDist(V, lambdas)
    # max_ent.plot()
    # pdf = max_ent.pdf()
    # pdf.plot()
    # print('Arrived at cdf computation.')
    # max_ent.cdf().plot()
    # w = max_ent.inverse_sampling()
    cdf = max_ent.cdf()
    # print('Arrived at plots.')
    # cdf.plot()

    print('Experiments')
    nr = 10
    t1 = time.time()
    t = t1
    for _ in range(nr):
        w = sample(ctx,n,mode=DurationSamplerMode.MAX_ENT,lambdas=[1,-1])
        print(f"Sampled {str(w), w.duration} in {time.time() - t}s.")
        t = time.time()

    print(f"Sampled {n} words in {time.time()-t1}s. Example:{w} with duration {w.duration}.")



    print(max_ent.normalising_term)


# Profile the function
cProfile.run('experiment()', 'profiling_results')

# Print the profiling results
p = pstats.Stats('profiling_results')
p.strip_dirs().sort_stats('cumulative').print_stats(10)
