"""
fig:volumeDeltaSigma (Fig. 9): three volume functions V_10(T) for the
delta-sigma / signal-shaping specs (Nicolas + Thao).

The volume computation is exact and deterministic, so there is no fast/full
distinction: the figure is recomputed from the .tre specs every time.

  --out  output directory for the three PDFs (default: this script's dir)
"""
import argparse, os, sys, shutil, time, warnings
warnings.filterwarnings('ignore')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../..'))
for p in [REPO, HERE]:
    if p not in sys.path:
        sys.path.insert(0, p)

from experiments.paper_experiments.plot_config import fig_width_in, fig_height_in
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


def set_style():
    usetex = shutil.which("latex") is not None
    plt.rcParams.update({"text.usetex": usetex, "font.size": 11})
    if usetex:
        plt.rcParams.update({"font.family": "serif",
                             "font.serif": ["Latin Modern Roman"]})
    else:
        print("[deltasigma] LaTeX not found: labels via mathtext "
              "(content identical, fonts differ from the paper).")


def main():
    ap = argparse.ArgumentParser(
        description="fig:volumeDeltaSigma (Fig. 9): three volume functions V_10(T).")
    ap.add_argument('--out', default=None,
                    help="output directory for the three PDFs (default: this script's dir)")
    args = ap.parse_args()

    out_dir = args.out if args.out else HERE
    os.makedirs(out_dir, exist_ok=True)
    set_style()

    for outname, spec, title in CASES:
        t0 = time.time()
        ctx = quickparse(os.path.join(HERE, spec))
        v = slice_volume(ctx, N)
        plt.figure(figsize=(fig_width_in, fig_height_in * 0.55))
        v.plot(no_show=True, plt_title=title, include_zero=False)
        plt.gca().grid(False, which="both")
        out = os.path.join(out_dir, outname)
        plt.savefig(out, bbox_inches='tight')
        plt.close("all")
        print(f"[deltasigma] {outname} done in {time.time() - t0:.1f} s")


if __name__ == '__main__':
    main()
