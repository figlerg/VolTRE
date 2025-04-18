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
fig_width_pt = 418.25368  # LaTeX textwidth in points
inches_per_pt = 1.0 / 72.27  # Convert points to inches
fig_width_in = fig_width_pt * inches_per_pt  # Width in inches
# fig_height_in = fig_width_in * (2 / 3)  # 2:1 aspect ratio for 2x1 layout
# figsize = (fig_width_in, fig_height_in)  # Exportable figure size
