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

figname = "03_intro_vis"

def experiment():
    # Ensure square aspect ratio with enough horizontal space for two plots
    fig, axs = plt.subplots(1, 3, figsize=(fig_width_in, 1/3 * fig_width_in), sharex=True, sharey=True)

    # titles = [
    #     "$\\langle a \\cdot a \\rangle_{[0,1]}$",
    #     "$\\langle b \\cdot (a \\cup b) \\rangle_{[0,2]}$"
    # ]
    titles = [
        "$aa$% in $\\langle a \\cdot a \\rangle_{[0,1]}$",
        "$ba$% in $\\langle b \\cdot (a \\cup b) \\rangle_{[0,2]}$",
        "$bb$% in $\\langle b \\cdot (a \\cup b) \\rangle_{[0,2]}$"
    ]

    # fig.suptitle("Area of delays in subexpresions of $e_t$", fontsize=14, y=1.05)

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

        # new inscribed line for a slice
        y_inscribe = -x + 0.5
        ax.plot(x, y_inscribe, linestyle='--', color=c4, linewidth=1)
        ax.text(0.001, 0.01, "$t_1 + t_2 = \\frac{1}{2}$", fontsize=10, color=c4, rotation=-48, ha='left', va='bottom')


        ax.fill_between(x, 0, y, where=(y > 0), interpolate=True, color=c1, alpha=0.2)

    # plt.tight_layout()
    # plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.savefig(f"{figname}.pdf")

pr = cProfile.Profile()
pr.enable()
experiment()
pr.disable()
pr.dump_stats(f"{figname}.prof")

# # Print the profiling results
p = pstats.Stats(f'{figname}.prof')
p.strip_dirs().sort_stats('cumulative').print_stats(10)
