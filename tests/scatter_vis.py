# for now try to generate the multiset of intervals automatically
import random
from os.path import join, curdir
from os import listdir
from parse.quickparse import quickparse
from sample.TimedWord import TimedWord
from volume.slice_volume import slice_volume
from sample.sample import sample

ctx = quickparse(join('parse', 'test_spec.txt'))
print(ctx.getText())
n = 20

V, cache = slice_volume(ctx, n, debug_mode=False, return_cache = True)  # debug mode generates files in vis_cache

V.fancy_print()
# V.plot()

T = 3.7

seed = random.seed(42)



def experiment():
    # Your code here
    s1: TimedWord = sample(ctx, n, T, cache)