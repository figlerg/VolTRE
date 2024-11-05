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


def experiment():
    fig, axs = plt.subplots(1, 2, figsize=(fig_width_in, 0.3*fig_width_in))  # 2x1 grid layout

    f = VolumePoly(intervals=[(0,1), (0,2), (1,2)], polys=[2,poly("(T-1)^2",T),3])

    f.fancy_print()

    plt.sca(axs[0])
    f.plot(no_show=True)

    plt.sca(axs[1])
    f.simplify()
    f.plot(no_show=True)

    for ax in axs:
        ax.set_yticks([])

    axs[0].set_xlabel("$T$")
    axs[0].set_ylabel(r"$f$",  labelpad=7)

    axs[1].set_xlabel("$T$")
    axs[1].set_ylabel(r"$f'$",  labelpad=7)

    plt.tight_layout()  # Adjust layout to fit within the figure size

    # plt.show()
    plt.savefig("01_simplify_vis.pdf")  # Use .pgf if you prefer

pr = cProfile.Profile()
pr.enable()
experiment()
pr.disable()
pr.dump_stats("01_simplify_vis.prof")

# # Print the profiling results
p = pstats.Stats('01_simplify_vis.prof')
p.strip_dirs().sort_stats('cumulative').print_stats(10)
