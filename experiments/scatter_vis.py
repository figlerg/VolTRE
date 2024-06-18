# for now try to generate the multiset of intervals automatically
import random
import time
from os.path import join, curdir
from os import listdir

import numpy as np
from matplotlib import pyplot as plt

from parse.quickparse import quickparse
from sample.TimedWord import TimedWord
from volume.slice_volume import slice_volume
from sample.sample import sample

seed = random.seed(42)

start = time.time()

ctx = quickparse(join('experiments', 'spec_00.tre'))
print(ctx.getText())
t1 = time.time()
print(f'Successfully parsed expression in {t1 - start}s.')

nr_exp = 5000
n = 3
# T = 3.7


V = slice_volume(ctx, n)
t2 = time.time()
print(f'Successfully generated volume function in {t2 - t1}s.')
# V.fancy_print()
# V.plot()

# BUILDING SCATTERPLOT
pts = []

for i in range(nr_exp):
    s: TimedWord = sample(ctx, n)

    pt = []
    for symbol, delay in s:
        if symbol == 'b':
            delay += 2
        pt.append(delay)

    pts.append(pt)

pts = np.asarray(pts)

t3 = time.time()
print(f'Successfully sampled {nr_exp} times in {t3-t2}s.')


# Create a figure and an axis
fig, ax = plt.subplots()

# Set the limits for the plot
ax.set_xlim(0, 3)
ax.set_ylim(0, 3)

# Set the ticks on both axes
ax.set_xticks([0, 2, 3])
ax.set_yticks([0, 2, 3])

# Draw the vertical and horizontal lines
ax.plot([2, 2], [0, 3], color='black')
ax.plot([0, 3], [2, 2], color='black')

# Draw the box borders
ax.plot([0, 3], [0, 0], color='black')
ax.plot([0, 3], [3, 3], color='black')
ax.plot([0, 0], [0, 3], color='black')
ax.plot([3, 3], [0, 3], color='black')

# Set the aspect of the plot to be equal
ax.set_aspect('equal')

# # # Optional: add labels for better clarity
# ax.text(1, 2.5, '[0,2] x [2,3]', horizontalalignment='center')
# ax.text(1, 1, '[0,2] x [0,2]', horizontalalignment='center')
# ax.text(2.5, 2.5, '[2,3] x [2,3]', horizontalalignment='center')
# ax.text(2.5, 1, '[2,3] x [0,2]', horizontalalignment='center')

# Add labels just outside the box
# For [0,2] intervals
ax.text(-0.1, 1, 'a', horizontalalignment='right', verticalalignment='center', fontsize=12, c = 'blue')
ax.text(1, -0.1, 'a', horizontalalignment='center', verticalalignment='top', fontsize=12, c = 'blue')

# For [2,3] intervals
ax.text(2.5, -0.1, 'b', horizontalalignment='center', verticalalignment='top', fontsize=12, c = 'blue')
ax.text(-0.1, 2.5, 'b', horizontalalignment='right', verticalalignment='center', fontsize=12, c = 'blue')


plt.scatter(pts[:,0], pts[:,1], s=2)
# plt.show()

plt.tight_layout()
plt.savefig(join('experiments', 'test_out', 'scatter_vis.png'))