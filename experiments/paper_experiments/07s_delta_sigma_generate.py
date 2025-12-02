# for now try to generate the multiset of intervals automatically
import pstats
import cProfile
import matplotlib.pyplot as plt
from os.path import join
import numpy as np
from volume.VolumePoly import VolumePoly
from sympy import poly
from sympy.abc import T

from parse.quickparse import quickparse
from sample.sample import sample

# get all settings and constants
from plot_config import *
from volume.slice_volume import slice_volume
import pickle
import os

n = 24
case = 'split'

# all of these are equivalent, but they are parsed differently
# experimentally the split works best
match case:
    case 'star':
        figname = f"07_delta_sigma_{n}_star"
        spec = "07a_delta_sigma_star.tre"
    case 'split':
        figname = f"07_delta_sigma_{n}_split"
        spec = "07b_delta_sigma_split.tre"
    case 'four':
        figname = f"07_delta_sigma_{n}_four"
        spec = "07c_delta_sigma_four.tre"



nr_samples = 150
T=None

os.makedirs(figname, exist_ok=True)

def experiment():
    fig, axs = plt.subplots(1, 1, figsize=(fig_width_in, fig_height_in*0.32))  # 2x1 grid layout

    ctx = quickparse(spec)


    v = slice_volume(ctx,n)
    print("Computed volumes.")

    v.plot(no_show=True,plt_title=None)
    # plt.show()

    # plt.ylabel("")
    # plt.subplots_adjust(bottom=0.2)

    for i in range(nr_samples):
        w = sample(ctx, n=n, T=T)
        w_name_pickle = "{:03d}.pkl".format(i)
        with open(os.path.join(figname,w_name_pickle), 'wb') as f:
            pickle.dump(w,f)
        print(w)

    plt.savefig(f"{figname}.pdf")  # Use .pgf if you prefer


pr = cProfile.Profile()
pr.enable()
experiment()
pr.disable()
pr.dump_stats(f"{figname}.prof")

# # Print the profiling results
p = pstats.Stats(f'{figname}.prof')
p.strip_dirs().sort_stats('cumulative').print_stats(10)
