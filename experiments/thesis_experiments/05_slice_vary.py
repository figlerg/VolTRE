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

figname = "05_slice_vary"

def experiment():
    fig, ax = plt.subplots(1, 1, figsize=(0.5 * fig_width_in, 0.5 * fig_width_in))

    ax.set_title("$ba$", fontsize=12)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_xlabel("$t_1$")
    ax.set_ylabel("$t_2$")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    x = np.linspace(0, 2, 400)
    y = -x + 2
    ax.plot(x, y, color=c1)
    ax.fill_between(x, 0, y, where=(y > 0), interpolate=True, color=c1, alpha=0.2)

    slice_levels = [0.25, 0.5, 0.75]
    for t in slice_levels:
        y_inscribe = -x + t
        ax.plot(x, y_inscribe, linestyle='--', color=c4, linewidth=1)
        # if t == 0.5:
        #     ax.text(0.001, 0.01, "$t_1 + t_2 = \\frac{1}{2}$", fontsize=10, color=c4, rotation=-48, ha='left', va='bottom')

    # Add arrows pointing away from the t = 0.75 line
    t = 0.75
    for tx in [0.3, 0.6, 0.9]:
        ty = -tx + t
        dx = 0.1
        dy = 0.1
        ax.arrow(tx, ty, dx, dy, head_width=0.03, head_length=0.05, fc=c4, ec=c4)

    plt.subplots_adjust(bottom=0.2, left=0.2)
    plt.savefig(f"{figname}.pdf")

pr = cProfile.Profile()
pr.enable()
experiment()
pr.disable()
pr.dump_stats(f"{figname}.prof")

# # Print the profiling results
p = pstats.Stats(f'{figname}.prof')
p.strip_dirs().sort_stats('cumulative').print_stats(10)
