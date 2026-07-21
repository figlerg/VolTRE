"""Reproduce fig:stress (3-panel stress test, ex1/ex2/ex3).

Paper file: 11_stress_ex123_3.pdf. The committed CSVs in
experiments/paper_experiments/11_stress_test/results/ are the paper's data:
make_combined_plot.py on those CSVs regenerates the paper PDF byte-identically
(verified 2026-07-21).
Source: experiments/paper_experiments/11_stress_test/ (notebook + make_combined_plot.py)

Fast mode: regenerate the figure from the committed CSVs (seconds).
Full mode (--full): rerun the timing sweeps by executing the notebook's
compute cells headlessly (seed 42, budget 1200 s per example, up to ~1 h;
fresh CSVs and figure go to artifact/output/). Timing bars will differ from
the paper depending on your hardware; the qualitative shape is the result.
"""
import json
import os
import subprocess
import sys
import time

from common import EXPERIMENTS_DIR, OUTPUT_DIR, full_mode

STRESS_DIR = os.path.join(EXPERIMENTS_DIR, "11_stress_test")
NOTEBOOK = os.path.join(STRESS_DIR, "11_stress_test.ipynb")
PLOT_SCRIPT = os.path.join(STRESS_DIR, "make_combined_plot.py")


def run_compute_cells(out_dir):
    with open(NOTEBOOK) as f:
        nb = json.load(f)
    code_cells = [''.join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
    setup, helpers = code_cells[0], code_cells[1]
    setup = setup.replace('matplotlib.use("module://matplotlib_inline.backend_inline")',
                          'matplotlib.use("Agg")')
    compute = [c for c in code_cells
               if "= collect_timed(" in c and ("results_ex1" in c or "results_ex2" in c
                                               or "results_ex3" in c)]
    assert len(compute) == 3, f"expected 3 compute cells, found {len(compute)}"
    ns = {}
    exec(setup, ns)
    exec(helpers, ns)
    ns["RESULTS"] = out_dir  # redirect CSVs and per-panel PDFs, keep the repo clean
    if os.environ.get("VOLTRE_STRESS_BUDGET"):
        ns["BUDGET_S"] = float(os.environ["VOLTRE_STRESS_BUDGET"])
    for cell in compute:
        exec(cell, ns)


def main():
    out_dir = os.path.abspath(OUTPUT_DIR)
    os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()
    env = os.environ.copy()
    env["VOLTRE_OUT_DIR"] = out_dir
    env["MPLBACKEND"] = "Agg"
    if full_mode():
        print("[artifact] full mode: rerunning stress sweeps (up to ~1 h) ...")
        run_compute_cells(out_dir)
        env["VOLTRE_RESULTS_DIR"] = out_dir
    subprocess.run([sys.executable, PLOT_SCRIPT], env=env, check=True)
    print(f"[artifact] 11_stress_ex123.pdf (paper: 11_stress_ex123_3.pdf) done in "
          f"{time.time() - t0:.1f} s "
          f"({'full rerun' if full_mode() else 'fast, from committed CSVs'})")


if __name__ == "__main__":
    main()
