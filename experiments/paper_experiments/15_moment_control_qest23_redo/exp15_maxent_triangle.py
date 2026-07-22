"""
Experiment 15: max-entropy sampling from <a.a>_[0,1] = {t1·a·t2·a | t1+t2 ≤ 1}.
Reproduces the QEST23 cloud-of-points figure using VolTRE machinery.

Three panels with different (mean, variance) targets for the total duration T.
Uniform baseline: E(T) = 2/3, Var(T) = 1/18.
"""
import argparse, os, sys, csv, warnings
warnings.filterwarnings('ignore')

import numpy as np
import matplotlib.pyplot as plt

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
for p in [REPO, os.path.dirname(__file__)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from experiments.paper_experiments.plot_config import fig_width_in
plt.rcParams.update({"text.usetex": False, "font.family": "sans-serif", "font.serif": []})

from parse.quickparse import quickparse
from sample.sample import sample, DurationSamplerMode
from volume.slice_volume import slice_volume
from volume.tuning import parameterize_mean_variance

RESULTS    = os.path.dirname(__file__)
NR_SAMPLES = 5000
N          = 2
_ap = argparse.ArgumentParser(
    description="fig:maxent-triangle (Fig. 7): max-entropy sampling from <a.a>_[0,1].")
_ap.add_argument('--out', default=None,
                 help="output directory for the figure and resampled CSVs (default: this script's dir)")
_ap.add_argument('--resample', action='store_true',
                 help="resample instead of loading the committed CSVs")
_args = _ap.parse_args()
LOAD    = not _args.resample
OUT_DIR = _args.out if _args.out else RESULTS
os.makedirs(OUT_DIR, exist_ok=True)
np.random.seed(42)

phi = quickparse('<a.a>_[0,1]', string=True)
V   = slice_volume(phi, N)

# (target_mean, target_variance, panel_label)
# Uniform baseline: mean=2/3, var=1/18 ≈ 0.056  (lambdas ≈ 0)
# configs = [
#     (0.40, 0.050, r'$E(T)=0.40$'),
#     (2/3,  1/18,  r'$E(T)=2/3$ (uniform)'),
#     (0.85, 0.020, r'$E(T)=0.85$'),
# ]
# configs = [
#     (2/3, 1/36, r'$E(T)=2/3, V(T)=1/36$'),
#     (2/3,  1/18,  r'$E(T)=2/3, V(T)=1/18$'),
#     (2/3, 1/9, r'$E(T)=2/3, V(T)= 1/9$'),
# ]

configs = [
    (2/3, 1/72, r'$E(T)=2/3, V(T)=1/72$'),
    (2/3,  1/18,  r'$E(T)=2/3, V(T)=1/18$'),
    (2/3, 1/9, r'$E(T)=2/3, V(T)= 1/9$'),
]


fig, axes = plt.subplots(1, 3, figsize=(fig_width_in, fig_width_in / 2.8))

for ax, (mean, var, label) in zip(axes, configs):
    csv_dir = RESULTS if LOAD else OUT_DIR
    csv_path = os.path.join(csv_dir, f'exp15_samples_mean{mean:.3f}_var{var:.4f}.csv')

    if LOAD and os.path.exists(csv_path):
        with open(csv_path, newline='') as f:
            rows = list(csv.DictReader(f))
        t1s = [float(r['t1']) for r in rows]
        t2s = [float(r['t2']) for r in rows]
        print(f'  loaded {csv_path} ({len(t1s)} samples)')
    else:
        print(f'\nSolving for mean={mean:.3f}, var={var:.4f} ...')
        lam = parameterize_mean_variance(mean, var, V)
        words = []
        for _ in range(NR_SAMPLES):
            w, _ = sample(phi, n=N, mode=DurationSamplerMode.MAX_ENT,
                          lambdas=lam, feedback=True)
            words.append(w)
        t1s = [w.delays[0] for w in words]
        t2s = [w.delays[1] for w in words]
        with open(csv_path, 'w', newline='') as f:
            csv.writer(f).writerows([['t1', 't2']] + list(zip(t1s, t2s)))
        print(f'  saved {csv_path}')

    ax.scatter(t1s, t2s, s=0.5, alpha=0.25, linewidths=0, color='#2166ac',
               rasterized=True)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.set_xlabel('$t_1$', fontsize=8)
    ax.set_ylabel('$t_2$', fontsize=8)
    ax.set_title(label, fontsize=8)
    ax.tick_params(labelsize=7)

fig.tight_layout()
out = os.path.join(OUT_DIR, 'exp15_maxent_triangle.pdf')
fig.savefig(out, bbox_inches='tight', dpi=300)
print(f'\nSaved {out}')
