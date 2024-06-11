# for now try to generate the multiset of intervals automatically
from os.path import join, curdir
from os import listdir

from matplotlib import pyplot as plt

from parse.quickparse import quickparse
from volume.slice_volume import slice_volume

path0 = join('experiments', 'spec_00.txt')
path1 = join('experiments', 'spec_01.txt')
path2 = join('experiments', 'spec_02.txt')
path3 = join('experiments', 'spec_03.txt')
path4 = join('experiments', 'spec_04.txt')

ctx0 = quickparse(path0)  # my original toy example
ctx1 = quickparse(path1)  # here I have a convolution with a c that is not bounded at first. This fails
ctx2 = quickparse(path2)
ctx3 = quickparse(path3)
ctx4 = quickparse(path4)

vol0 = slice_volume(ctx0, n = 1)
vol0.plot(no_show=True)
plt.tight_layout()
plt.savefig(join('experiments', 'test_out', 'vol_00.png'))
plt.clf()

vol1 = slice_volume(ctx1, n = 2)
vol1.plot(no_show=True)
plt.tight_layout()
plt.savefig(join('experiments', 'test_out', 'vol_01.png'))
plt.clf()

vol2 = slice_volume(ctx2, n = 2)
vol2.plot(no_show=True)
plt.tight_layout()
plt.savefig(join('experiments', 'test_out', 'vol_02.png'))
plt.clf()

vol3 = slice_volume(ctx3, n = 2)
vol3.plot(no_show=True)
plt.tight_layout()
plt.savefig(join('experiments', 'test_out', 'vol_03.png'))
plt.clf()

vol4 = slice_volume(ctx4, n = 8)
vol4.plot(no_show=True)
plt.tight_layout()
plt.savefig(join('experiments', 'test_out', 'vol_04.png'))
plt.clf()


