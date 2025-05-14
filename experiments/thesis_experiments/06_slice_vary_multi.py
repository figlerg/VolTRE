# for now try to generate the multiset of intervals automatically
import pstats
import cProfile
import matplotlib.pyplot as plt
import numpy as np
from os.path import join
from volume.VolumePoly import VolumePoly
from sympy import poly
from sympy.abc import T

# get all settings and constants
from plot_config import *

figname = "06_slice_vary_multi"

def experiment():
    fig, axs = plt.subplots(1, 3, figsize=(fig_width_in, 1/3 * fig_width_in+0.2), sharex=True, sharey=True)

    titles = ["$aa$", "$ba$", "$bb$"]
    slice_levels = [0.25, 0.5, 0.75]

    for i, ax in enumerate(axs):
        ax.set_title(titles[i], fontsize=12)
        ax.set_xlim(0, 2)
        ax.set_ylim(0, 2)
        ax.set_xlabel("$t_1$")
        ax.set_ylabel("$t_2$")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        x = np.linspace(0, 2, 400)
        if i == 0:
            y = -x + 1
        else:
            y = -x + 2

        ax.plot(x, y, color=c1)
        ax.fill_between(x, 0, y, where=(y > 0), interpolate=True, color=c1, alpha=0.2)

        for t in slice_levels:
            y_inscribe = -x + t
            ax.plot(x, y_inscribe, linestyle='--', color=c4, linewidth=1)

        # Arrows pointing away from the t = 0.75 line
        t = 0.75
        for tx in [0.3, 0.6, 0.9]:
            ty = -tx + t
            dx = 0.07
            dy = 0.07
            ax.arrow(tx, ty, dx, dy, head_width=0.03, head_length=0.05, fc=c4, ec=c4)

    plt.subplots_adjust(bottom=0.24)
    plt.savefig(f"{figname}.pdf")

pr = cProfile.Profile()
pr.enable()
experiment()
pr.disable()
pr.dump_stats(f"{figname}.prof")

# # Print the profiling results
p = pstats.Stats(f'{figname}.prof')
p.strip_dirs().sort_stats('cumulative').print_stats(10)
