# for now try to generate the multiset of intervals automatically
import pstats
import random
import cProfile

import matplotlib.pyplot as plt
from os.path import join

import numpy as np

from misc.rename import rename
from parse.quickparse import quickparse
from volume.slice_volume import slice_volume
from sample.sample import sample



TODO = None

# this gets all the settings I use for latex styles, fonts, etc for the plots
from plot_config import *


def experiment():


    fig_height_in = TODO
    fig, axs = plt.subplots(2, 1, figsize=(fig_width_in, fig_height_in))  # 2x1 grid layout

    # Example plots (replace with actual data)
    x = np.linspace(0, 10, 100)
    axs[0].plot(x, np.sin(x), label="sin(x)")
    axs[1].plot(x, np.cos(x), label="cos(x)")

    # Customize the axes and labels
    for ax in axs:
        ax.legend()
        ax.set_xlabel("X-axis label")
        ax.set_ylabel("Y-axis label")

    plt.tight_layout()  # Adjust layout to fit within the figure size

    plt.show()
    # plt.savefig("01_hypercube.pdf"TODO)  # Use .pgf if you prefer
    plt.savefig(TODO)

pr = cProfile.Profile()
pr.enable()
experiment()
pr.disable()

# pr.dump_stats("01_simplify_vis.prof"TODO)
pr.dump_stats(TODO)

# # Print the profiling results
# p = pstats.Stats('01_simplify_vis.prof'TODO)
p = pstats.Stats(TODO)
p.strip_dirs().sort_stats('cumulative').print_stats(10)
