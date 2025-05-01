# for now try to generate the multiset of intervals automatically
import pstats
import cProfile
import matplotlib.pyplot as plt
from os.path import join
import numpy as np
from volume.VolumePoly import VolumePoly
from sympy import poly
from sympy.abc import T

# get all settings and constants
from plot_config import *

figname = "03_intro_vis"


def experiment():
    fig, axs = plt.subplots(1, 1, figsize=(fig_width_in, fig_height_in))  # 2x1 grid layout

    plt.savefig(f"{figname}.pdf")  # Use .pgf if you prefer


pr = cProfile.Profile()
pr.enable()
experiment()
pr.disable()
pr.dump_stats(f"{figname}.prof")

# # Print the profiling results
p = pstats.Stats(f'{figname}.prof')
p.strip_dirs().sort_stats('cumulative').print_stats(10)
