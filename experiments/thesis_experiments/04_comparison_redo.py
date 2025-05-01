# for now try to generate the multiset of intervals automatically
import pstats
import cProfile
import matplotlib.pyplot as plt
import pandas as pd
from os.path import join
import numpy as np
from volume.VolumePoly import VolumePoly
from sympy import poly
from sympy.abc import T

# get all settings and constants
from plot_config import *

figname = "04_comparison_redo"

def experiment():
    fig, axs = plt.subplots(1, 2, figsize=(fig_width_in, fig_height_in*0.32))

    df_benoit_takiller = pd.read_csv("04_benoit_TAKiller.csv", sep=r'\s+')
    df_benoit_thicktwin = pd.read_csv("04_benoit_Thicktwin.csv", sep=r'\s+')
    df_tre_takiller = pd.read_csv("04_tre_TAkiller.csv", sep=r'\s+')
    df_tre_thicktwin = pd.read_csv("04_tre_thicktwin.csv", sep=r'\s+')

    def select_n_and_runtime(df):
        return df.iloc[:, [0, -1]]

    benoit_takiller = select_n_and_runtime(df_benoit_takiller)
    benoit_thicktwin = select_n_and_runtime(df_benoit_thicktwin)
    tre_takiller = select_n_and_runtime(df_tre_takiller)
    tre_thicktwin = select_n_and_runtime(df_tre_thicktwin)

    c_tre = None
    c_ta = None

    # TAKiller
    axs[0].plot(tre_takiller.iloc[:6, 0], tre_takiller.iloc[:6, 1], label="TRE", c=c_tre)
    axs[0].plot(benoit_takiller.iloc[:6, 0], benoit_takiller.iloc[:6, 1], label="TA", c=c_ta)
    axs[0].set_title("Bad-for-TA Family")
    axs[0].set_xlabel("n")
    axs[0].set_ylabel("time (s)")
    axs[0].legend()
    axs[0].grid(True)

    # Thick Twin
    axs[1].plot(tre_thicktwin.iloc[:, 0], tre_thicktwin.iloc[:, 1], label="TRE", c=c_tre)
    axs[1].plot(benoit_thicktwin.iloc[:, 0], benoit_thicktwin.iloc[:, 1], label="TA", c=c_ta)
    axs[1].set_title("$e_\\cap$")
    axs[1].set_xlabel("n")
    axs[1].set_ylabel("time (s)")
    axs[1].legend()
    axs[1].grid(True)

    plt.tight_layout()
    plt.savefig(f"{figname}.pdf")  # Use .pgf if you prefer

pr = cProfile.Profile()
pr.enable()
experiment()
pr.disable()
pr.dump_stats(f"{figname}.prof")

# # Print the profiling results
p = pstats.Stats(f'{figname}.prof')
p.strip_dirs().sort_stats('cumulative').print_stats(10)
