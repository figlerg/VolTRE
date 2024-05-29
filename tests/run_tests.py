# for now try to generate the multiset of intervals automatically
from os.path import join, curdir
from os import listdir

from parse.quickparse import quickparse
from volume.slice_volume import slice_volume

path0 = join('../parse', 'test_spec.txt')
path1 = join('../tests', 'spec_01.txt')
path2 = join('../tests', 'spec_02.txt')
path3 = join('../tests', 'spec_03.txt')
path4 = join('../tests', 'spec_04.txt')

ctx0 = quickparse(path0)  # my original toy example
ctx1 = quickparse(path1)  # here I have a convolution with a c that is not bounded at first. This fails
ctx2 = quickparse(path2)
ctx3 = quickparse(path3)
ctx4 = quickparse(path4)

vol1 = slice_volume(ctx1, n = 2)
vol1.plot()


vol2 = slice_volume(ctx2, n = 2)
vol2.plot()


vol3 = slice_volume(ctx3, n = 2)
vol3.plot()


vol4 = slice_volume(ctx4, n = 8)
vol4.plot()


