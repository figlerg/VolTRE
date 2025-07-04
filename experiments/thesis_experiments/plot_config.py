import matplotlib.pyplot as plt
import numpy as np
import random


# Use the PDF backend which doesn't require LaTeX installed
# plt.rcParams.update({
#     "pgf.texsystem": "pdflatex",  # Use pdflatex (commonly available)
#     "font.family": "serif",       # Use serif fonts (like LaTeX)
#     "text.usetex": True,          # Enable LaTeX rendering
#     "pgf.rcfonts": False,         # Disable font setup for consistency
#     "font.size": 11,              # Same font size as "normal" in my thesis script
#
# })

# Configure matplotlib for LaTeX-like plotting
plt.rcParams.update({
    "pgf.texsystem": "pdflatex",
    "font.family": "serif",
    "font.serif": ["Latin Modern Roman"],
    "font.weight": "bold",
    "font.style": "normal",
    "text.usetex": True,
    "pgf.rcfonts": False,
    "font.size": 11
})

# Set seeds for reproducibility
random.seed(42)
np.random.seed(42)

# Define figure size based on LaTeX textwidth
# 418.25368pt
# 591.5302p

fig_width_pt = 418.25368  # LaTeX textwidth in points
inches_per_pt = 1.0 / 72.27  # Convert points to inches
fig_width_in = fig_width_pt * inches_per_pt  # Width in inches

fig_height_in = 591.5302 * inches_per_pt  # full page height

# fig_height_in = fig_width_in * (2 / 3)  # 2:1 aspect ratio for 2x1 layout
# figsize = (fig_width_in, fig_height_in)  # Exportable figure size


# selfmade
c1 = 'skyblue'
# c2 = 'lightcoral'
c2 = '#EAEFBD'
c3 = 'palegreen'
c4 = 'thistle'

# coolor.co take 1
# c1 = '#dbb1bc'
# c2 = '#d3c4e3'
# c3 = '#8f95d3'
# c4 = '#8cb8e9'
# c5 = '#89daff'

# coolor.co take 2
# c1 = "#cc8b86"  # Old rose
# c2 = "#f9eae1"  # Linen
# c3 = "#aa998f"  # Cinereous
# c4 = "#d1be9c"  # Dun
# c5 = "#e7d9d9"


"""
coolors.co palette:


dbb1bc,d3c4e3,8f95d3,8cb8e9,89daff


"""