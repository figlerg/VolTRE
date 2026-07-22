"""
Stress test compute for fig:stress (Fig. 3): time the sampler on three TREs and
write the timing CSVs (results_ex1.csv, results_ex2.csv, results_ex3.csv) that
make_combined_plot.py turns into the paper figure.

This is the same measurement code as 11_stress_test.ipynb, as a plain script so
the artifact does not have to execute notebook cells. Timing bars depend on the
hardware; the qualitative shape (super-polynomial growth in ex2, intersection
rejection growth in ex3) is the result.

  --out     directory for the CSVs (default: this script's results/)
  --budget  wall-clock budget per expression in seconds (default: 1200)
  --k       samples per data point (default: 20)
"""
import argparse, os, sys, csv, time, random, warnings
warnings.filterwarnings('ignore')

import numpy as np

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
PAPER_EXP = os.path.join(REPO, 'experiments', 'paper_experiments')
for p in [REPO, PAPER_EXP]:
    if p not in sys.path:
        sys.path.insert(0, p)

from parse.quickparse import quickparse
from sample.sample import sample
from volume.slice_volume import slice_volume
from volume.VolumePoly import continuous_convolution
from sympy.core.cache import clear_cache as clear_sympy_cache


def save_results_csv(path, xs, results):
    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['xval', 't_vol', 't_sample', 'avg_smart_rej',
                    'avg_intersect_rej', 'n_fail'])
        for xval in xs:
            if xval in results:
                r = results[xval]
                w.writerow([xval, r['t_vol'], r['t_sample'],
                            r['avg_smart_rej'], r['avg_intersect_rej'], r['n_fail']])


def collect_timed(phi, xs, n_of, T_of, label, K, budget_s, is_intersection=False):
    results = {}
    t_start = time.perf_counter()
    print(f"=== {label} ===")
    for xval in xs:
        elapsed = time.perf_counter() - t_start
        if elapsed > budget_s:
            print(f"  budget hit after {elapsed:.0f}s, stopping")
            break
        n = n_of(xval)
        T = T_of(xval)
        print(f"  n={n}  T={T}  elapsed={elapsed:.0f}s", flush=True)
        slice_volume.cache_clear()
        continuous_convolution.cache_clear()
        clear_sympy_cache()
        if is_intersection:
            # Intersection raises in slice_volume at the top level, but volumes ARE
            # computed for both arms inside each sample() call. Precompute them here
            # on the original children so t_vol reflects the real init cost.
            t0 = time.perf_counter()
            try:
                child0, child1 = phi.expr(0), phi.expr(1)
                for k in range(n + 1):
                    slice_volume(child0, k)
                    slice_volume(child1, k)
                t_vol = time.perf_counter() - t0
            except Exception as e:
                print(f"    sub-volume precompute failed: {type(e).__name__}, skipping")
                t_vol = 0.0
        else:
            t0 = time.perf_counter()
            try:
                slice_volume(phi, n)
                t_vol = time.perf_counter() - t0
            except Exception as e:
                print(f"    slice_volume failed: {type(e).__name__}, skipping")
                continue
        total_sr, total_ir, n_ok = 0, 0, 0
        t0 = time.perf_counter()
        for _ in range(K):
            try:
                kw = {'n': n, 'feedback': True}
                if T is not None:
                    kw['T'] = T
                _, fb = sample(phi, **kw)
                total_sr += fb.smart_rej
                if fb.intersect_rej is not None:
                    total_ir += fb.intersect_rej
                n_ok += 1
            except Exception:
                pass
        t_sample_total = time.perf_counter() - t0
        n_fail = K - n_ok
        if n_ok > 0:
            t_sper = t_sample_total / n_ok
            results[xval] = {
                't_vol': t_vol, 't_sample': t_sper,
                'avg_smart_rej': total_sr / n_ok,
                'avg_intersect_rej': total_ir / n_ok,
                'n_fail': n_fail}
            print(f"    t_vol={t_vol:.2f}s  t_sample/call={t_sper:.3f}s  "
                  f"s_rej={total_sr/n_ok:.1f}  i_rej={total_ir/n_ok:.1f}  ok={n_ok}/{K}")
        else:
            results[xval] = {
                't_vol': t_vol, 't_sample': 0,
                'avg_smart_rej': 0, 'avg_intersect_rej': 0, 'n_fail': K}
            print(f"    all {K} samples failed  t_vol={t_vol:.2f}s")
    return results


def main():
    ap = argparse.ArgumentParser(
        description="fig:stress (Fig. 3): compute the timing CSVs for the stress test.")
    ap.add_argument('--out', default=None,
                    help="directory for the CSVs (default: this script's results/)")
    ap.add_argument('--budget', type=float, default=1200,
                    help="wall-clock budget per expression in seconds (default: 1200)")
    ap.add_argument('--k', type=int, default=20,
                    help="samples per data point (default: 20)")
    args = ap.parse_args()

    out_dir = args.out if args.out else os.path.join(os.path.dirname(__file__), 'results')
    os.makedirs(out_dir, exist_ok=True)

    phi_ex1 = quickparse('<a>_[0,1] *', string=True)
    phi_ex2 = quickparse('a*.<a*>_[1,2]', string=True)
    phi_ex3 = quickparse('(<a . a>_[0,1] . a) & (a . <a . a>_[0,1])', string=True)

    N_VALUES_EX1 = list(range(3, 31, 3))
    N_VALUES_EX2 = list(range(2, 21, 2))
    T_EX2        = 2.0
    T_VALUES_EX3 = [0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 1.8, 1.85, 1.9]

    print(f"Config: K={args.k}  budget={args.budget}s  out={out_dir}")

    random.seed(42); np.random.seed(42)
    results_ex1 = collect_timed(phi_ex1, N_VALUES_EX1,
                                n_of=lambda n: n, T_of=lambda n: None,
                                label='ex1', K=args.k, budget_s=args.budget)
    save_results_csv(os.path.join(out_dir, 'results_ex1.csv'), N_VALUES_EX1, results_ex1)

    random.seed(42); np.random.seed(42)
    results_ex2 = collect_timed(phi_ex2, N_VALUES_EX2,
                                n_of=lambda n: n, T_of=lambda n: T_EX2,
                                label='ex2', K=args.k, budget_s=args.budget)
    save_results_csv(os.path.join(out_dir, 'results_ex2.csv'), N_VALUES_EX2, results_ex2)

    random.seed(42); np.random.seed(42)
    results_ex3 = collect_timed(phi_ex3, T_VALUES_EX3,
                                n_of=lambda T: 3, T_of=lambda T: T,
                                label='ex3', K=args.k, budget_s=args.budget,
                                is_intersection=True)
    save_results_csv(os.path.join(out_dir, 'results_ex3.csv'), T_VALUES_EX3, results_ex3)

    print(f"Saved results_ex1/ex2/ex3.csv to {out_dir}")


if __name__ == '__main__':
    main()
