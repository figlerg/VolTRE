"""Shared setup for the artifact figure runners.

Replicates the plot style of experiments/paper_experiments/plot_config.py,
with one difference: LaTeX text rendering is enabled only if a `latex`
binary is available (the Docker image ships one). Without LaTeX the figures
are rendered with matplotlib's mathtext; content is identical, fonts differ
slightly from the paper.
"""
import os
import random
import shutil
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
EXPERIMENTS_DIR = os.path.join(REPO_ROOT, "experiments", "paper_experiments")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")

# LaTeX textwidth of the paper, as in plot_config.py
fig_width_pt = 418.25368
inches_per_pt = 1.0 / 72.27
fig_width_in = fig_width_pt * inches_per_pt
fig_height_in = fig_width_in * (2 / 3)


def set_style():
    usetex = shutil.which("latex") is not None
    plt.rcParams.update({
        "pgf.texsystem": "pdflatex",
        "font.family": "serif",
        "font.serif": ["Latin Modern Roman"],
        "font.weight": "bold",
        "font.style": "normal",
        "text.usetex": usetex,
        "pgf.rcfonts": False,
        "font.size": 11,
    })
    if not usetex:
        print("[artifact] LaTeX not found: rendering labels with mathtext "
              "(figure content identical, fonts differ from the paper).")
    return usetex


def seed_all(seed=42):
    random.seed(seed)
    np.random.seed(seed)


def output_path(filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    return os.path.join(OUTPUT_DIR, filename)


def full_mode():
    return "--full" in sys.argv[1:]
