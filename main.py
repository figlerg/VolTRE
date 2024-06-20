# for now try to generate the multiset of intervals automatically
import random
import cProfile
import pstats
import time
import matplotlib.pyplot as plt
from os.path import join, curdir
from parse.quickparse import quickparse
from sample.TimedWord import TimedWord
from visualize_recursion import generate_syntax_tree, highlight_node
from volume.MaxEntDist import MaxEntDist
from volume.slice_volume import slice_volume
from sample.sample import sample, DurationSamplerMode


ctx = quickparse(join('experiments', 'spec_00.tre'))
print(ctx.getText())

# visualizes the tree
# G = generate_syntax_tree(ctx)
# highlight_node(G, str(ctx), comment='')


def experiment():
    random.seed(42)
    n = 3

    V = slice_volume(ctx, n, debug_mode=False)


    lambdas = [1,1,-1]
    max_ent = MaxEntDist(V, lambdas)
    cdf = max_ent.cdf()
    # cdf.plot()

    print('Sampling...')
    nr = 10
    t1 = time.time()
    t = t1
    for _ in range(nr):
        w = sample(ctx,n,mode=DurationSamplerMode.MAX_ENT,lambdas=[1,-1])
        print(f"Sampled {str(w), w.duration} in {time.time() - t}s.")
        t = time.time()

    print(f"Sampled {nr} words in {time.time()-t1}s. Example:{w} with duration {w.duration}.")



    # print(max_ent.normalising_term)

pr = cProfile.Profile()
pr.enable()
experiment()
pr.disable()
pr.dump_stats("main.prof")


# # Profile the function - THIS CAN'T BE USED WITH SNAKEVIZ
# cProfile.run('experiment()', 'main.prof')
#
# # Print the profiling results
p = pstats.Stats('main.prof')
p.strip_dirs().sort_stats('cumulative').print_stats(100)
