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

figname = "07_samplesketch"

def experiment():
    fig, ax = plt.subplots(1, 1, figsize=(0.5 * fig_width_in, 0.5 * fig_width_in))

    ax.set_title("$aa$", fontsize=12)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_xlabel("$t_1$")
    ax.set_ylabel("$t_2$")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    x = np.linspace(0, 2, 400)
    y = -x + 1
    ax.plot(x, y, color=c1)
    ax.fill_between(x, 0, y, where=(y > 0), interpolate=True, color=c1, alpha=0.2)

    # Only one slice line
    t = 0.5
    y_inscribe = -x + t
    ax.plot(x, y_inscribe, linestyle='--', color=c4, linewidth=1)

    # # Arrows with slope 1 pointing TOWARDS the line from bottom left
    # for tx in [0.1, 0.3, 0.5]:
    #     ty = 0.1 * tx
    #     dx = 0.07
    #     dy = 0.07
    #     ax.arrow(tx, ty, dx, dy, head_width=0.03, head_length=0.05, fc=c4, ec=c4)
    head_length=0.05
    ax.arrow(0, 0, 1/4-0.05, 1/4-0.05, head_width=0.03, head_length=0.05, fc=c4, ec=c4)

    # Arrow with slope -1 from start of the line segment (top-left)
    start_tx = 0.0
    start_ty = t
    dx = 0.1
    dy = -0.1
    ax.arrow(start_tx, start_ty, dx, dy, head_width=0.03, head_length=0.05, fc=c4, ec=c4)

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