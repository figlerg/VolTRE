"""Reproduce Figure 2 (fig:cube): slices of the hypercube language.

Three panels:
  cube_3d.png          3D slices for T in {0.5,1,1.5,2,2.5}   (paper: cubecrop3.png)
  cube_projection.png  the T=1.5 slice projected on (t1,t2)   (paper: outprojsquare.png)
  cube_volume.pdf      the volume function V_3(T)             (paper: bottom TikZ plot)

The two 3D/2D panels are drawn by gnuplot from wordgen samples (Benoit's data,
see PROVENANCE.md). The volume function is computed by VolTRE itself.

Fast mode: use the committed data/*.dat.
Full mode (--resample): regenerate the .dat with wordgen (needs a wordgen
binary, --wordgen or the Docker one).
"""
import argparse
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec_01_hypercube.tre")
CUBE_TXT = os.path.join(HERE, "cube.txt")
DEFAULT_WORDGEN = "/tmp/wordgen_build/_build/default/src/wordgen.exe"

# wordgen commands (regexp, poly, traj, exact expected-duration) per Benoit.
SLICES = [
    ("out05.dat", "0.50001"),
    ("out10.dat", "1.00001"),
    ("out15.dat", "1.50001"),
    ("out20.dat", "2.00001"),
    ("out25.dat", "2.50001"),
]


def find_wordgen(explicit):
    for cand in (explicit, DEFAULT_WORDGEN, shutil.which("wordgen")):
        if cand and os.path.isfile(cand):
            return cand
    sys.exit("[cube] --resample needs a wordgen binary: pass --wordgen PATH, "
             f"put one at {DEFAULT_WORDGEN}, or have 'wordgen' on PATH.")


def resample_with_wordgen(data_dir, wordgen):
    os.makedirs(data_dir, exist_ok=True)
    for fname, dur in SLICES:
        print(f"[cube] wordgen T={dur} -> {fname}")
        subprocess.run(
            [wordgen, "--poly", "3", "--regexp", "<a>_[0,1]*", "--traj", "10000",
             "--exact-duration", "--expected-duration", dur,
             os.path.join(data_dir, fname)],
            check=True,
        )


def run_gnuplot(script, data_dir, outfile, extra=None):
    define = f"datadir='{data_dir}'; outfile='{outfile}'"
    if extra:
        define += "; " + extra
    subprocess.run(["gnuplot", "-e", define, os.path.join(HERE, script)], check=True)


def make_volume_panel(outfile):
    import shutil as _sh
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    usetex = _sh.which("latex") is not None
    plt.rcParams.update({"font.size": 11, "text.usetex": usetex})
    if usetex:
        plt.rcParams.update({"font.family": "serif", "font.serif": ["Latin Modern Roman"]})
    from parse.quickparse import quickparse
    from volume.slice_volume import slice_volume

    ctx = quickparse(SPEC)
    v = slice_volume(ctx, 3)
    plt.figure(figsize=(4.0, 2.2))
    v.plot(no_show=True, plt_title=r"$V_3(T)$", include_zero=True)
    plt.gca().grid(False, which="both")
    plt.savefig(outfile, bbox_inches="tight")
    plt.close("all")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=".", help="output directory")
    ap.add_argument("--resample", action="store_true",
                    help="regenerate the wordgen .dat instead of using committed data")
    ap.add_argument("--wordgen", default=None, help="path to the wordgen binary")
    args = ap.parse_args()

    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)

    if args.resample:
        data_dir = out
        resample_with_wordgen(data_dir, find_wordgen(args.wordgen))
    else:
        data_dir = os.path.join(HERE, "data")

    run_gnuplot("cube_3d.gnu", data_dir, os.path.join(out, "cube_3d.png"),
                extra=f"cubefile='{CUBE_TXT}'")
    print("[cube] cube_3d.png done")
    run_gnuplot("cube_projection.gnu", data_dir, os.path.join(out, "cube_projection.png"))
    print("[cube] cube_projection.png done")
    make_volume_panel(os.path.join(out, "cube_volume.pdf"))
    print("[cube] cube_volume.pdf done")


if __name__ == "__main__":
    main()
