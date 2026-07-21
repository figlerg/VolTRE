"""Reproduce fig:maxent-triangle.

Paper file: exp15_maxent_triangle_variance_3_cropped.pdf (the "variance sweep"
config, which is the active one in the experiment script; the paper copy was
additionally pdfcrop'ed, the script already saves with a tight bounding box).
Source: experiments/paper_experiments/15_moment_control_qest23_redo/exp15_maxent_triangle.py

Fast mode: plot from the committed sample CSVs (seconds).
Full mode (--full): resample 3x5000 max-entropy words from scratch.
"""
import os
import subprocess
import sys
import time

from common import EXPERIMENTS_DIR, OUTPUT_DIR, full_mode, output_path

SCRIPT = os.path.join(EXPERIMENTS_DIR, "15_moment_control_qest23_redo", "exp15_maxent_triangle.py")


def main():
    env = os.environ.copy()
    env["VOLTRE_OUT_DIR"] = os.path.abspath(OUTPUT_DIR)
    env["MPLBACKEND"] = "Agg"
    if full_mode():
        env["VOLTRE_RESAMPLE"] = "1"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    t0 = time.time()
    subprocess.run([sys.executable, SCRIPT], env=env, check=True)
    print(f"[artifact] exp15_maxent_triangle.pdf done in {time.time() - t0:.1f} s "
          f"({'full resample' if full_mode() else 'fast, from committed CSVs'})")


if __name__ == "__main__":
    main()
