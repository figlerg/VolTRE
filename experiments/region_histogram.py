# for now try to generate the multiset of intervals automatically
import math
import random
import time
from os.path import join, curdir
from os import listdir
import pandas as pd

import numpy as np
from matplotlib import pyplot as plt

from parse.quickparse import quickparse
from sample.TimedWord import TimedWord
from volume.slice_volume import slice_volume
from sample.sample import sample

seed = random.seed(42)

start = time.time()

# ctx = quickparse(join('parse', 'test_spec.txt'))
ctx = quickparse(join('experiments', 'working_example.tre'))
print(ctx.getText())
t1 = time.time()
print(f'Successfully parsed expression in {t1 - start}s.')

nr_exp = 2000
n = 4


V = slice_volume(ctx, n)
t2 = time.time()
print(f'Successfully generated volume function in {t2 - t1}s.')
V.fancy_print()
# V.plot()

# BUILDING SCATTERPLOT
pts = []
words = []

for i in range(nr_exp):
    s: TimedWord = sample(ctx, n)
    words.append(s)


t3 = time.time()
print(f'Successfully sampled {nr_exp} times in {t3-t2}s.')


n1 = 5
n2 = 4

# Initialize a DataFrame with zeros for counts
k_range = range(n1)
i_range = range(n2)
df = pd.DataFrame(0, index=i_range, columns=k_range)

# Name the index and columns
df.index.name = 'i'
df.columns.name = 'k'

# Example loop to increment counts for encountered tuples (j1, j2)
for word in words:
    iota, k = word.iota_k()
    df.at[iota, k] += 1

# Print the DataFrame to verify counts
print(df)

normalized_df = df.divide(nr_exp)
print(normalized_df)

scaled_df = normalized_df.multiply((math.factorial(n) * V.total_volume()))
print(scaled_df)

hist = {}
for word in words:
    key = word.region_index()

    try:
        hist[key] += 1
    except KeyError:
        hist[key] = 0

for key in sorted(hist.keys()):
    hist[key] *= float(math.factorial(n) * V.total_volume() / nr_exp)

for pair in sorted(hist.items()):
    print(pair)