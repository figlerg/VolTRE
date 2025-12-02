# for now try to generate the multiset of intervals automatically
import os
import pickle
import pstats
import cProfile
import matplotlib.pyplot as plt
from os.path import join
import numpy as np
import random


from parse.quickparse import quickparse
from sample.sample import sample
from volume.VolumePoly import VolumePoly

# get all settings and constants
from plot_config import *
from volume.slice_volume import slice_volume

r"""
Hi Felix,
with Thao we have a new way of generating signals.
Can you provide 100 samples of size n=20 and duration T=42 for the following 
Denote by 
s=<a>_[1,2] and f=<b>_[3,4]
the expression is
f* . (< s . ( f . f* ) >_\geq 5)*
The idea is two have two kind of peaks slim and fat.
The formula says between two slims there should be at least one fat and at least 5 time unit. This can also be an example that we could use earlier in the paper...

We can augment the density of s by reducing the T.

Best,
Nicolas

THE ACTUAL HARDCODED SPEC: (<b>_[3,4]*) . (< <a>_[1,2] . ( <b>_[3,4] . (<b>_[3,4]*) ) >_[5,\infty])*
"""

random.seed(42)
np.random.seed(42)

figname = "08_delta_sigma_nicolas"

spec = "08_nicolas_spec.tre"
n = 15
folder = spec + f'_{n}'
T = 43
# T = 27
nr_samples = 100


os.makedirs(folder, exist_ok=True)

def experiment():
    fig, axs = plt.subplots(1, 1, figsize=(fig_width_in, fig_height_in*0.5))  # 2x1 grid layout
    ctx = quickparse(spec)

    case = 'compute'
    match case:
        case 'compute':
            v:VolumePoly = slice_volume(ctx,n)
            print("Computed volumes.")

            with open(join(folder, f'volume_{n}.pkl'), 'wb') as f:
                pickle.dump(v, f)
        case 'load':
            path = join(folder, f'volume_{n}.pkl')
            with open(path, "rb") as f:
                v = pickle.load(f)
            print('Loaded volume.')

    title = r"$({\langle b\rangle _{[3,4]}}^*) \cdot (\langle  \langle a\rangle _{[1,2]} \cdot ( \langle b\rangle _{[3,4]} . (\langle b\rangle _{[3,4]}^*) ) \rangle _{[5,\infty]})^*$"
    v.plot(no_show=True,plt_title=title, include_zero=False)

    ax = plt.gca()
    ax.grid(False, which='both')
    # plt.show()

    plt.savefig(f"{figname}_n_{n}.pdf")

    # plt.ylabel("")
    # plt.subplots_adjust(bottom=0.2)

    for i in range(nr_samples):
        try:
            w = sample(ctx, n=n, T=T)
            w_name_pickle = "{:03d}.pkl".format(i)
            with open(join(folder,w_name_pickle), 'wb') as f:
                pickle.dump(w,f)
            print(w)
        except Exception as e:
            print(f'Skipped because of exception: {e}.')



pr = cProfile.Profile()
pr.enable()
experiment()
pr.disable()
pr.dump_stats(f"{figname}_n_{n}.prof")

# # Print the profiling results
p = pstats.Stats(f'{figname}_n_{n}.prof')
p.strip_dirs().sort_stats('cumulative').print_stats(10)
