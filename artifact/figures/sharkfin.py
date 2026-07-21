"""Reproduce fig:sharkfin (ambiguity / rejection-trials figure, Example 9).

Paper file: sharkfin.pdf. The exact copy in the paper was generated with an
older parameter set (50 samples per T according to the caption); the script
as committed uses NR_SAMPLES=200, which gives a smoother empirical curve with
the same shape. This known, cosmetic difference is documented in the artifact
README.
Source: experiments/paper_experiments/13_nicolas_ambiguity/theorem4.py

Fast mode: volumes are recomputed exactly, the empirical rejection counts are
loaded from the committed CSVs.
Full mode (--full): resample the empirical rejection counts (200 per T value).
"""
import os
import subprocess
import sys
import time

from common import EXPERIMENTS_DIR, OUTPUT_DIR, full_mode

SCRIPT = os.path.join(EXPERIMENTS_DIR, "13_nicolas_ambiguity", "theorem4.py")


def main():
    env = os.environ.copy()
    env["VOLTRE_OUT_DIR"] = os.path.abspath(OUTPUT_DIR)
    env["MPLBACKEND"] = "Agg"
    if full_mode():
        env["VOLTRE_RESAMPLE"] = "1"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    t0 = time.time()
    subprocess.run([sys.executable, SCRIPT], env=env, check=True)
    print(f"[artifact] theorem4_ambiguity.pdf (paper: sharkfin.pdf) done in "
          f"{time.time() - t0:.1f} s "
          f"({'full resample' if full_mode() else 'fast, empirical CSVs'})")


if __name__ == "__main__":
    main()
