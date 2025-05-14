# for now try to generate the multiset of intervals automatically
import pstats
import cProfile
import matplotlib.pyplot as plt
from os.path import join
import numpy as np

from parse.quickparse import quickparse
from volume.VolumePoly import VolumePoly
from sympy import poly
from sympy.abc import T

# get all settings and constants
from plot_config import *
from volume.slice_volume import slice_volume

figname = "08_intro_slicevolume"


def experiment():
    fig, axs = plt.subplots(1, 1, figsize=(fig_width_in, fig_height_in*0.32))  # 2x1 grid layout

    ctx = quickparse('03_intro_vis.tre')

    v = slice_volume(ctx,2)

    v.plot(no_show=True,plt_title=r"$V_n^{\langle a\cdot a \rangle_{[0,1]} + \langle a\cdot (a+b) \rangle_{[0,2]}}(T)$")

    plt.ylabel("")

    plt.subplots_adjust(bottom=0.2)

    plt.savefig(f"{figname}.pdf")  # Use .pgf if you prefer


pr = cProfile.Profile()
pr.enable()
experiment()
pr.disable()
pr.dump_stats(f"{figname}.prof")

# # Print the profiling results
p = pstats.Stats(f'{figname}.prof')
p.strip_dirs().sort_stats('cumulative').print_stats(10)
