"""Reproduce fig:volumeDeltaSigma (three volume plots, n=10).

Paper files: 08_delta_sigma_nicolas_n_10.pdf,
             08b_delta_sigma_nicolas_fat_thin_n_10.pdf,
             08c_delta_sigma_thao_n_10.pdf
Source: experiments/paper_experiments/08s_delta_sigma_nicolas.py (volume part;
the sampling loop in that script feeds the Simulink case study, not this figure).

The volume computation is exact and deterministic, so fast and full mode are
identical for this figure.
"""
import os
import time

import matplotlib.pyplot as plt

from common import EXPERIMENTS_DIR, fig_width_in, fig_height_in, output_path, seed_all, set_style

from parse.quickparse import quickparse
from volume.slice_volume import slice_volume

N = 10

CASES = [
    ("08_delta_sigma_nicolas_n_10.pdf", "08a_nicolas_spec_5_inf.tre",
     r"$({\langle b\rangle _{[3,4]}}^*) \cdot (\langle  \langle a\rangle _{[1,2]} \cdot ( \langle b\rangle _{[3,4]} . (\langle b\rangle _{[3,4]}^*) ) \rangle _{[5,\infty]})^*$"),
    ("08b_delta_sigma_nicolas_fat_thin_n_10.pdf", "08b_nicolas_spec_fat_thin.tre",
     r"$({\langle b\rangle _{[3,4]}}^*) \cdot (  \langle a\rangle _{[1,2]} \cdot ( \langle b\rangle _{[3,4]} . (\langle b\rangle _{[3,4]}^*) ) )^*$"),
    ("08c_delta_sigma_thao_n_10.pdf", "08c_thao_spec.tre",
     r"$(   \langle a\rangle _{[1,2]}    {\langle b\rangle} _{[3,4]}) ^*  $"),
]


def main():
    set_style()
    os.chdir(EXPERIMENTS_DIR)
    for outname, spec, title in CASES:
        seed_all()
        t0 = time.time()
        ctx = quickparse(spec)
        v = slice_volume(ctx, N)
        plt.figure(figsize=(fig_width_in, fig_height_in * 0.55))
        v.plot(no_show=True, plt_title=title, include_zero=False)
        plt.gca().grid(False, which="both")
        plt.savefig(output_path(outname))
        plt.close("all")
        print(f"[artifact] {outname} done in {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()
