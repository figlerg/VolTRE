"""Reproduce fig:exp16 (VolTRE vs wordgen scalability, k-sweep, mode 8).

Paper file: exp16_ksweep_v8_k8.pdf.
Source: experiments/paper_experiments/16_ta_vs_tre_2/exp16_ksweep.py

Fast mode: regenerate the plot from the committed timing CSVs (seconds,
wordgen not needed).
Full mode (--full): rerun the VolTRE timing sweep (k=1..9) and the local
wordgen runs (k=1..9, 1 h timeout and 8 GB memory cap per k, so worst case
several hours). Requires a wordgen binary: set WORDGEN_BIN, or rely on the
Docker image which ships one. Timings differ with hardware; the qualitative
result is wordgen's blow-up at k>=6 while VolTRE keeps scaling.
"""
import os
import shutil
import subprocess
import sys
import time

from common import EXPERIMENTS_DIR, OUTPUT_DIR, full_mode

SCRIPT = os.path.join(EXPERIMENTS_DIR, "16_ta_vs_tre_2", "exp16_ksweep.py")
DEFAULT_WORDGEN = "/tmp/wordgen_build/_build/default/src/wordgen.exe"


def wordgen_available(env):
    candidate = env.get("WORDGEN_BIN", DEFAULT_WORDGEN)
    if os.path.isfile(candidate):
        return candidate
    on_path = shutil.which("wordgen")
    if on_path:
        env["WORDGEN_BIN"] = on_path
        return on_path
    return None


def main():
    out_dir = os.path.abspath(OUTPUT_DIR)
    os.makedirs(out_dir, exist_ok=True)
    env = os.environ.copy()
    env["VOLTRE_OUT_DIR"] = out_dir
    env["MPLBACKEND"] = "Agg"
    if full_mode():
        wg = wordgen_available(env)
        if wg is None:
            sys.exit("[artifact] full mode needs a wordgen binary: none found at "
                     f"WORDGEN_BIN, {DEFAULT_WORDGEN}, or on PATH. Use the Docker "
                     "image or install wordgen (see README).")
        print(f"[artifact] full mode: rerunning VolTRE + wordgen ({wg}), "
              "worst case several hours ...")
        env["VOLTRE_RESAMPLE"] = "1"
        env["VOLTRE_RESULTS_DIR"] = out_dir
    t0 = time.time()
    subprocess.run([sys.executable, SCRIPT], env=env, check=True)
    print(f"[artifact] exp16_ksweep_v8_k*.pdf (paper: exp16_ksweep_v8_k8.pdf) done "
          f"in {time.time() - t0:.1f} s "
          f"({'full rerun' if full_mode() else 'fast, from committed CSVs'})")


if __name__ == "__main__":
    main()
