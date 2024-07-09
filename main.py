# for now try to generate the multiset of intervals automatically
import random
import cProfile
import pstats
import time
from math import factorial

import matplotlib.pyplot as plt
from os.path import join, curdir

import numpy as np

from parse.quickparse import quickparse
from sample.TimedWord import TimedWord
from visualize_recursion import generate_syntax_tree, highlight_node
from volume.MaxEntDist import MaxEntDist
from volume.slice_volume import slice_volume
from sample.sample import sample, DurationSamplerMode
from volume.tuning import mu, jacobi, lambdas, parameterize_mean_variance

ctx = quickparse(join('experiments', 'spec_00.tre'))
# ctx = quickparse(join('experiments', 'spec_06.tre'))
# ctx = quickparse(join('experiments', 'TAkiller.tre'))
# ctx = quickparse(join('experiments', 'TAkiller_15_gen.tre'))
# ctx = quickparse(join('experiments', 'TAkiller_Subfamily.STAR_3_gen.tre'))
# ctx = quickparse(join('experiments', 'TAkiller_Subfamily.STAR_5_gen.tre'))

print(ctx.getText())

# visualizes the tree
# G = generate_syntax_tree(ctx)
# highlight_node(G, str(ctx), comment='')


def experiment():
    random.seed(42)

    n = 3

    V = slice_volume(ctx, n)
    V.fancy_print()
    # V.plot()

    # target = np.asarray([3, 10])
    # target.resize((len(target),1))

    # optimal_lambda = lambdas(target, v)

    target_mean = 4
    target_variance = 1

    tuned_lambdas = parameterize_mean_variance(target_mean, target_variance, V)

    nr_samples = 1000

    t1 = time.time()
    samples = [sample(ctx, n, mode=DurationSamplerMode.MAX_ENT, lambdas=tuned_lambdas) for i in range(nr_samples)]
    durations = np.asarray([w.duration for w in samples])
    # print(samples)
    # print(durations)

    print(f'Sampled {nr_samples} samples in {time.time()-t1}s. Set for target mean {target_mean} and target variance {target_variance}:')
    print(f"sample mean: {durations.mean()}")
    print(f"sample variance: {durations.var()}")


    # print(float(V.total_volume())- 1/factorial(9))
    # print(float(V.polys[2](2.3)))
    # print(f"Volume is continuous: {V.is_cont_piece()}")
    # V.polys[-1] += 2/6
    # V.plot()
    # print(w1 := sample(ctx, n))


    # lambdas = (1,1,-1)
    # max_ent = MaxEntDist(V, lambdas)
    # max_ent.plot()
    #
    # print(f"The jacobi matrix is: \n{jacobi(lambdas, V, 4)}")
    #
    # pdf = max_ent.pdf
    # cdf = max_ent.cdf
    # pdf.plot()
    # cdf.plot()
    # print(w2 := sample(ctx, n, mode=DurationSamplerMode.MAX_ENT, lambdas=lambdas))




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
