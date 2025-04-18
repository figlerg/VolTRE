# for now try to generate the multiset of intervals automatically
import pstats
import cProfile
import matplotlib.pyplot as plt
from os.path import join
import numpy as np
from volume.VolumePoly import VolumePoly
from sympy import poly
from sympy.abc import T
from matplotlib.patches import Polygon



# get all settings and constants
from plot_config import *


def experiment():
    fig, axs = plt.subplots(6, 1, figsize=(fig_width_in, fig_height_in), sharex=True, sharey=True)  # 2x1 grid layout
    # fig, axs = plt.subplots(6, 1, sharex=True, sharey=True)  # 2x1 grid layout

    # Define plot bounds
    xmin = 0
    xmax = 10
    ymin = 0
    ymax = 1.8

    phi = (1+np.sqrt(5))/2

    # Rectangle configs for 5 subplots
    data = [
        (2, 6, 0.5, 1.5),       # 1) b'-a' < b-a
        (2, 2.6, 0.5, 1.5),       # 2) b-a < b'-a'
        (2, 3, 0.5, 1.5),     # 3) b'-a' < b-a more
        (2, None, 0.5, 1.5),    # 4) b = ∞ (open to the right)
        (2, 3, 0.5, None),    # 5) b' = ∞ (open upwards)
        (2, None, 0.5, None)  # 6) b = ∞ and b' = ∞
    ]

    n_subplots = len(data)

    caption_height_in = 34*inches_per_pt   # 34pt are 2 lines of caption. change if necessary

    fig, axs = plt.subplots(n_subplots, 1, figsize=(fig_width_in, fig_height_in-caption_height_in), sharex=True, sharey=True)


    for j, (ax, (a, b, ap, bp)) in enumerate(zip(axs, data)):
        # Determine b and bp visually if infinite
        b_vis = b if b is not None else xmax
        bp_vis = bp if bp is not None else ymax

        # Rectangle corners
        x_rect = [a, a, b_vis, b_vis, a]
        y_rect = [ap, bp_vis, bp_vis, ap, ap]

        # Adjust linestyle for infinite edges
        draw_edge = [True, True, True, True]
        if b is None:
            draw_edge[2] = False  # skip right edge
        if bp is None:
            draw_edge[1] = False  # skip top edge

        # Draw rectangle with selective edges
        for i in range(4):
            if draw_edge[i]:
                ax.plot([x_rect[i], x_rect[i + 1]], [y_rect[i], y_rect[i + 1]], 'k', linewidth=1)

        if b is None:
            l = np.inf
        else:
            l = b-a
        if bp is None:
            lp = np.inf
        else:
            lp = bp-ap

        alpha = a + ap
        beta = a + ap + min(l,lp)
        gamma = a + ap + max(l,lp)
        # delta = b + bp

        #### DIAGONALS
        # diagonals for plots 2,3,5
        if b is not None and l<=lp:
            x_diag = np.linspace(a, b, 100)
            # from upper left corner
            y_diag1 = -1 * x_diag + beta
            y_diag2 = -1 * x_diag + gamma

            ax.plot(x_diag, y_diag1, 'm-', linewidth=1)
            ax.plot(x_diag, y_diag2, 'm-', linewidth=1)
        # plots 1,4
        if l>lp:
            x_diag = np.linspace(a, a+lp, 100)

            # case 1
            if b:
                x_diag2 = np.linspace(b-lp, b, 100)
                y_diag2 = -1 * x_diag2 + gamma
                ax.plot(x_diag2, y_diag2, 'm-', linewidth=1)

            y_diag1 = -1 * x_diag + beta

            # case 4 doesn't have a line
            if not bp:
                continue


            ax.plot(x_diag, y_diag1, 'm-', linewidth=1)


        # # POLYGONS FOR CASE 1
        # if not (l==lp==np.inf):
        #
        #     # this is a bit trash, why did I not just implement it with b= inf instead of None
        #     try:
        #         b_cut = min(b,a+lp)
        #     except:
        #         b_cut = a+lp
        #     try:
        #         bp_cut = min(bp, ap+l)
        #     except:
        #         bp_cut = ap+l
        #
        #
        #
        #     highlight_points = [(a,ap), (b_cut,ap), (a,bp_cut)]
        #
        # else:
        #     highlight_points = [(a,ap), (a,ymax),(xmax,ymax), (xmax,ap)]


        ### CASE 2 + 3


        # plot 1
        if j == 0:
        # if b and bp and l>lp:
            highlight_points =  np.array(((a,ap), (a,bp), (a+lp, ap)))
            highlight_points2 = np.array(((a,bp), (b-lp, bp), (b,ap), (a+lp, ap)))
            highlight_points3 = np.array(((b-lp, bp), (b,bp), (b,ap)))
            ax.add_patch(Polygon(highlight_points, closed=True, facecolor=c1, edgecolor='none', alpha=0.5))
            ax.add_patch(Polygon(highlight_points2, closed=True, facecolor=c2, edgecolor='none', alpha=0.5))
            ax.add_patch(Polygon(highlight_points3, closed=True, facecolor=c3, edgecolor='none', alpha=0.5))

        if j == 1:
            highlight_points =  np.array(((a,ap), (a,ap+l), (b, ap)))
            highlight_points2 = np.array(((a,ap+l), (a, bp), (b, bp-l),(b,ap)))
            highlight_points3 = np.array(((a, bp), (b,bp-l), (b,bp)))
            ax.add_patch(Polygon(highlight_points, closed=True, facecolor=c1, edgecolor='none', alpha=0.5))
            ax.add_patch(Polygon(highlight_points2, closed=True, facecolor=c4, edgecolor='none', alpha=0.5))
            ax.add_patch(Polygon(highlight_points3, closed=True, facecolor=c3, edgecolor='none', alpha=0.5))

        if j == 2:
            highlight_points =  np.array(((a,ap), (a,ap+l), (b, ap)))
            highlight_points3 = np.array(((a, bp), (b,bp-l), (b,bp)))
            ax.add_patch(Polygon(highlight_points, closed=True, facecolor=c1, edgecolor='none', alpha=0.5))
            ax.add_patch(Polygon(highlight_points3, closed=True, facecolor=c3, edgecolor='none', alpha=0.5))

        if j == 3:
            highlight_points =  np.array(((a,ap), (a,bp), (a+lp, ap)))
            highlight_points2 = np.array(((a,bp), (xmax, bp), (xmax,ap), (a+lp, ap)))
            ax.add_patch(Polygon(highlight_points, closed=True, facecolor=c1, edgecolor='none', alpha=0.5))
            ax.add_patch(Polygon(highlight_points2, closed=True, facecolor=c2, edgecolor='none', alpha=0.5))

        if j == 4:
            highlight_points =  np.array(((a,ap), (a,ap+l), (b, ap)))
            highlight_points2 = np.array(((a,ap+l), (a, ymax), (b, ymax),(b,ap)))
            ax.add_patch(Polygon(highlight_points, closed=True, facecolor=c1, edgecolor='none', alpha=0.5))
            ax.add_patch(Polygon(highlight_points2, closed=True, facecolor=c4, edgecolor='none', alpha=0.5))

        if j == 5:
            highlight_points = np.array(((a,ap), (a,ymax),(xmax, ymax), (xmax, ap)))
            ax.add_patch(Polygon(highlight_points, closed=True, facecolor=c1, edgecolor='none', alpha=0.5))





        # Axis ticks and range
        # ax.axhline(0, color='black', linewidth=0.5)
        # ax.axvline(0, color='black', linewidth=0.5)

        x_offset = -0.2
        y_offset = -0.12

        # CANNOT USE TICKS they are synchronized
        ax.tick_params(axis='x', bottom=False, labelbottom=False)
        ax.text(a, ymin + y_offset, "$a_1$", ha='center', va='top')
        if b is not None:
            ax.text(b, ymin + y_offset, "$b_1$", ha='center', va='top')

        ax.tick_params(axis='y', left=False, labelleft=False)
        ax.text(xmin + x_offset, ap, "$a_2$", ha='right', va='center')
        if bp is not None:
            ax.text(xmin + x_offset, bp, "$b_2$", ha='right', va='center')

        x_offset_line = 0
        y_offset_line = 0

        # Light horizontal guide lines for x-axis symbols
        ax.plot([a, a], [ymin+y_offset_line, ymax], color='gray', linestyle='--', linewidth=0.5, alpha=0.4)
        if b is not None:
            ax.plot([b, b], [ymin+y_offset_line, ymax], color='gray', linestyle='--', linewidth=0.5, alpha=0.4)

        # Light vertical guide lines for y-axis symbols
        ax.plot([xmin+x_offset_line, xmax], [ap, ap], color='gray', linestyle='--', linewidth=0.5, alpha=0.4)
        if bp is not None:
            ax.plot([xmin+x_offset_line, xmax], [bp, bp], color='gray', linestyle='--', linewidth=0.5,
                    alpha=0.4)

        # plt.xlim(xmin,xmax)
        # plt.ylim(ymin,ymax)
        plt.axis([xmin, xmax, ymin, ymax])
        plt.gca().set_aspect('equal', adjustable='box')

        ## CANNOT DO THIS it also forces x and y axes to be equally long
        # ax.set_aspect('equal')
        # ax.set_aspect('equal', adjustable='box')

        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    # plt.tight_layout()  # Adjust layout to fit within the figure size
    axs[-1].set_xlabel("$T_1 := T'$")
    axs[2].set_ylabel("$T_2 := T-T'$",labelpad=30)

    plt.subplots_adjust(left=0.15, right=0.95, top=0.97, bottom=0.05, hspace=0.4)
    # plt.show()


    plt.savefig("02_conv_vis.pdf")

pr = cProfile.Profile()
pr.enable()
experiment()
pr.disable()
pr.dump_stats("02_conv_vis.prof")

# # Print the profiling results
p = pstats.Stats('02_conv_vis.prof')
p.strip_dirs().sort_stats('cumulative').print_stats(10)
