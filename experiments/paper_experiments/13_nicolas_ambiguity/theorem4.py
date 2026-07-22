import argparse
import os
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings("ignore")

from experiments.paper_experiments.plot_config import *
plt.rcParams.update({
    "text.usetex": False,
    "font.family": "sans-serif",
    "font.serif": [],
})

from parse.quickparse import quickparse
from volume.slice_volume import slice_volume
from sample.sample import sample

_ap = argparse.ArgumentParser(
    description="fig:sharkfin (Fig. 4): number of trials to sample from an ambiguous TRE.")
_ap.add_argument('--out', default=None,
                 help="output directory for the figures (default: this script's results/)")
_ap.add_argument('--resample', action='store_true',
                 help="resample the empirical trial counts instead of loading the committed CSVs")
_args = _ap.parse_args()

RESULTS = os.path.join(os.path.dirname(__file__), 'results')
OUT_DIR = _args.out if _args.out else RESULTS
os.makedirs(RESULTS, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# committed CSVs live in results/; --resample recomputes them into OUT_DIR
LOAD = not _args.resample
if LOAD:
    SAVE_MEAN    = os.path.join(RESULTS, 'theorem4_empirical.csv')
    SAVE_SAMPLES = os.path.join(RESULTS, 'theorem4_samples.csv')
else:
    SAVE_MEAN    = os.path.join(OUT_DIR, 'theorem4_empirical.csv')
    SAVE_SAMPLES = os.path.join(OUT_DIR, 'theorem4_samples.csv')

# ── expressions (Example 9) ──────────────────────────────────────────────────
eex2       = quickparse('a*.<a*>_[1,2]', string=True)
eex2_prime = quickparse('<a*>_[1,2] + a* . <a . <a*>_[1,2] >_[2,INF]', string=True)

n          = 10
NR_SAMPLES = 200
T_MIN, T_MAX = 1.001, 7.0

# ── volumes ───────────────────────────────────────────────────────────────────
V_ex2       = slice_volume(eex2, n)
V_ex2_prime = slice_volume(eex2_prime, n)

T_dense  = np.linspace(0.1, 5.0, 600)
T_sparse = np.linspace(T_MIN, T_MAX, 50)

v2  = np.array([float(V_ex2(T))       for T in T_dense])
v2p = np.array([float(V_ex2_prime(T)) for T in T_dense])

ratio = np.where(v2p > 1e-30, v2 / v2p, np.nan)

# ── empirical: mean(1 + smart_rej) ───────────────────────────────────────────
if LOAD and os.path.exists(SAVE_MEAN):
    data      = np.genfromtxt(SAVE_MEAN, delimiter=',', skip_header=1)
    T_sparse  = data[:, 0]
    empirical = data[:, 1]
else:
    raw = np.array([
        [1 + sample(eex2, n, T=float(T), feedback=True)[1].smart_rej
         for _ in range(NR_SAMPLES)]
        for T in T_sparse
    ])
    empirical = raw.mean(axis=1)
    np.savetxt(SAVE_MEAN, np.column_stack([T_sparse, empirical]),
               delimiter=',', header='T,mean_trials', comments='')
    np.savetxt(SAVE_SAMPLES, np.column_stack([T_sparse, raw]),
               delimiter=',',
               header='T,' + ','.join(f's{i+1}' for i in range(NR_SAMPLES)),
               comments='')

# ── figure ────────────────────────────────────────────────────────────────────
PANEL_H = 1.9
COL_W   = fig_width_in / 2
C1, C2, C3 = '#4C72B0', '#DD8452', '#55A868'

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(COL_W, PANEL_H * 3),
                                     gridspec_kw={'hspace': 0.95})

ZOOM    = True   # set False to let matplotlib auto-scale x
X_LIM_a = 0.9
X_LIM_b = 5

plt.sca(ax1)
V_ex2.plot(no_show=True)
ax1.set_title(r'$e_{ex2} = a^* \cdot \langle a^* \rangle_{[1,2]}$', fontsize=7.5)
ax1.set_ylabel('$V_n(T)$', fontsize=7)
if ZOOM: ax1.set_xlim(X_LIM_a, X_LIM_b)
ax1.grid(axis='y', linestyle='--', alpha=0.3)
ax1.tick_params(labelsize=6)

plt.sca(ax2)
V_ex2_prime.plot(no_show=True)
ax2.set_title(r"$e'_{ex2} = \langle a^* \rangle_{[1,2]} + a^* \cdot \langle a \cdot \langle a^* \rangle_{[1,2]} \rangle_{[2,\infty]}$", fontsize=7.5)
ax2.set_ylabel('$V_n(T)$', fontsize=7)
if ZOOM: ax2.set_xlim(X_LIM_a, X_LIM_b)
ax2.grid(axis='y', linestyle='--', alpha=0.3)
ax2.tick_params(labelsize=6)

ax3.plot(T_dense, ratio, color=C3, lw=1.2,
         label=r"$V_n(e_{ex2})\,/\,V_n(e'_{ex2})$")
ax3.plot(T_sparse, empirical, color=C3, lw=1.0, linestyle='--',
         label=f'empirical #trials')
ax3.set_xlabel('$T$', fontsize=7)
ax3.set_ylabel('trials', fontsize=7)
ax3.set_title('#trials vs. expected #trials', fontsize=7.5)
ax3.legend(loc='upper right', fontsize=5.5, frameon=True,
           handlelength=0.8, borderpad=0.3, labelspacing=0.2)
ax3.grid(axis='y', linestyle='--', alpha=0.3)
ax3.tick_params(labelsize=6)
if ZOOM: ax3.set_xlim(X_LIM_a, X_LIM_b)

save_path = os.path.join(OUT_DIR, 'theorem4_ambiguity.pdf')

fig.savefig(save_path, bbox_inches='tight')

print(f"Saved plot under: {save_path}")

# standalone version of the trials panel, as used in the paper (fig:sharkfin)
fig2, ax = plt.subplots(figsize=(COL_W, COL_W * 0.6))
ax.plot(T_dense, ratio, color=C3, lw=1.8,
        label=r"$V_n(e_{ex2})\,/\,V_n(e'_{ex2})$")
ax.plot(T_sparse, empirical, color=C3, lw=1.5, linestyle='--',
        label='empirical #trials')
ax.set_xlabel('$T$', fontsize=9)
ax.set_ylabel('trials', fontsize=9)
ax.legend(loc='upper right', fontsize=7.5, frameon=True,
          handlelength=1.2, borderpad=0.3, labelspacing=0.2)
ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.tick_params(labelsize=8)
if ZOOM: ax.set_xlim(X_LIM_a, X_LIM_b)
sharkfin_path = os.path.join(OUT_DIR, 'sharkfin.pdf')
fig2.savefig(sharkfin_path, bbox_inches='tight')
print(f"Saved plot under: {sharkfin_path}")