from os.path import join
import random
import numpy as np
from parse.quickparse import quickparse
from volume.slice_volume import slice_volume
from sample.sample import sample


# SEED
np.random.seed(42)
random.seed(42)

# PARSE
ctx = quickparse(join('experiments', 'spec_00.tre'))
print(f"Parsed the expression {ctx.getText()}.")

# VOLUMES
n = 5                       # set fixed length n
T = 3.5                     # set fixed duration T

V = slice_volume(ctx, n)    # compute volume function

V.fancy_print()             # prints all segments and their polynomials

V.plot()                    # plot the function

nr_samples = 10             # assume we want to generate 10 samples

# SLICE SAMPLING
for _ in range(nr_samples):

    w = sample(ctx, n, T)      # generates a TimedWord object

    print(f"w = {w}.", f" duration = {w.duration}")  # duration is as specified


print('\nNow sampling all slices:\n')
# SAMPLING ALL SLICES
for _ in range(nr_samples):

    w = sample(ctx, n)      # generates a TimedWord object

    print(f"w = {w}.", f" duration = {w.duration}")  # duration is free but compatible with spec