# for now try to generate the multiset of intervals automatically
import random
import time
import warnings
from os.path import join

import numpy as np
from scipy.integrate import IntegrationWarning

from parse.quickparse import quickparse
from sample.sample import sample_unambig, DurationSamplerMode
from volume.slice_volume import slice_volume
from volume.tuning import parameterize_mean_variance

ctx = quickparse(join('experiments', 'spec_11_unbounded.tre'))
# ctx = quickparse(join('experiments', 'spec_00.tre'))
print(ctx.getText())


random.seed(42)
np.random.seed(42)
n = 1

V = slice_volume(ctx, n)
V.fancy_print()
# V.plot()


# np.seterr(all='raise')

## find lambdas for a target
# target = np.asarray([3, 10])
# target.resize((len(target),1))
# optimal_lambda = lambdas(target, v)

## find lambdas for a
target_mean = 30
target_variance = 10


print(f"Set for target mean {target_mean} and target variance {target_variance}.")
with warnings.catch_warnings():
    # Convert IntegrationWarning into an error
    warnings.simplefilter("error", IntegrationWarning)
    tuned_lambdas = parameterize_mean_variance(target_mean, target_variance, V)


    ## statistical test
    nr_samples = 1000

    t1 = time.time()
    samples = [sample_unambig(ctx, n, mode=DurationSamplerMode.MAX_ENT, lambdas=tuned_lambdas) for i in range(nr_samples)]
    durations = np.asarray([w.duration for w in samples])
    # print(samples)
    # print(durations)

print(
    f'Sampled {nr_samples} samples in {time.time() - t1}s.:')
print(f"sample mean: {durations.mean()}")
print(f"sample variance: {durations.var()}")
