import pstats
import cProfile
import matplotlib.pyplot as plt
from os.path import join
import numpy as np
from matplotlib.patches import Polygon
from plot_config import *  # Make sure this contains fig_width_in, inches_per_pt, and colors c1, c2, c3, etc.

def experiment():
    # Only one case to show (case i)
    data = [
        (2, 6, 0.5, 1.5),
    ]

    xmin, xmax = 0, 10
    ymin, ymax = 0, 1.8

    caption_height_in = 34 * inches_per_pt
    full_height = fig_height_in - caption_height_in
    scaled_height = full_height / 6

    fig, ax = plt.subplots(1, 1, figsize=(fig_width_in, scaled_height), sharex=True, sharey=True)
    axs = [ax]  # Ensure it's iterable

    for j, (ax, (a, b, ap, bp)) in enumerate(zip(axs, data)):
        b_vis = b if b is not None else xmax
        bp_vis = bp if bp is not None else ymax

        x_rect = [a, a, b_vis, b_vis, a]
        y_rect = [ap, bp_vis, bp_vis, ap, ap]

        draw_edge = [True, True, True, True]
        if b is None: draw_edge[2] = False
        if bp is None: draw_edge[1] = False

        for i in range(4):
            if draw_edge[i]:
                ax.plot([x_rect[i], x_rect[i + 1]], [y_rect[i], y_rect[i + 1]], 'k', linewidth=1)

        l = np.inf if b is None else b - a
        lp = np.inf if bp is None else bp - ap

        beta = a + ap + min(l, lp)
        gamma = a + ap + max(l, lp)

        x_diag = np.linspace(a, a + lp, 10)
        if b:
            x_diag2 = np.linspace(b - lp, b, 10)
            y_diag2 = -1 * x_diag2 + gamma
            ax.plot(x_diag2, y_diag2, 'm-', linewidth=1)
        y_diag1 = -1 * x_diag + beta
        if bp:
            ax.plot(x_diag, y_diag1, 'm-', linewidth=1)

        testlen = lp/2
        x_test1 = np.linspace(a,a+testlen, 10)
        y_test1 = -1*x_test1 + beta - testlen
        ax.plot(x_test1, y_test1, 'm-', linewidth=1,c=c1)

        # Highlight polygons for case i
        highlight_points = np.array(((a, ap), (a, bp), (a + lp, ap)))
        highlight_points2 = np.array(((a, bp), (b - lp, bp), (b, ap), (a + lp, ap)))
        highlight_points3 = np.array(((b - lp, bp), (b, bp), (b, ap)))

        ax.add_patch(Polygon(highlight_points, closed=True, facecolor=c1, edgecolor='none', alpha=0.5))
        ax.add_patch(Polygon(highlight_points2, closed=True, facecolor=c2, edgecolor='none', alpha=0.5))
        ax.add_patch(Polygon(highlight_points3, closed=True, facecolor=c3, edgecolor='none', alpha=0.5))

        x_offset = -0.2
        y_offset = -0.12

        ax.tick_params(axis='x', bottom=False, labelbottom=False)
        ax.text(a, ymin + y_offset, "$a_1$", ha='center', va='top')
        if b is not None:
            ax.text(b, ymin + y_offset, "$b_1$", ha='center', va='top')

        ax.tick_params(axis='y', left=False, labelleft=False)
        ax.text(xmin + x_offset, ap, "$a_2$", ha='right', va='center')
        if bp is not None:
            ax.text(xmin + x_offset, bp, "$b_2$", ha='right', va='center')

        ax.plot([a, a], [ymin, ymax], color='gray', linestyle='--', linewidth=0.5, alpha=0.4)
        if b is not None:
            ax.plot([b, b], [ymin, ymax], color='gray', linestyle='--', linewidth=0.5, alpha=0.4)
        ax.plot([xmin, xmax], [ap, ap], color='gray', linestyle='--', linewidth=0.5, alpha=0.4)
        if bp is not None:
            ax.plot([xmin, xmax], [bp, bp], color='gray', linestyle='--', linewidth=0.5, alpha=0.4)

        plt.axis([xmin, xmax, ymin, ymax])
        ax.set_aspect('equal', adjustable='box')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    ax.set_xlabel("$T_1 := T'$")
    ax.set_ylabel("$T_2 := T-T'$", labelpad=30)

    plt.subplots_adjust(left=0.15, right=0.95, top=0.97, bottom=0.15)
    plt.savefig("02b_conv_vis2.pdf")

# Run and profile
pr = cProfile.Profile()
pr.enable()
experiment()
pr.disable()
pr.dump_stats("02b_conv_vis2.prof")

p = pstats.Stats('02b_conv_vis2.prof')
p.strip_dirs().sort_stats('cumulative').print_stats(10)
