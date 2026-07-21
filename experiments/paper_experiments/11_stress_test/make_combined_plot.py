"""Standalone script: load CSVs and regenerate 11_stress_ex123.pdf (no sampling)."""
import os, sys, csv
import numpy as np

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
PAPER_EXP = os.path.join(REPO, 'experiments', 'paper_experiments')
for p in [REPO, PAPER_EXP]:
    if p not in sys.path:
        sys.path.insert(0, p)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from experiments.paper_experiments.plot_config import fig_width_in
plt.rcParams.update({"text.usetex": False, "font.family": "sans-serif", "font.serif": []})

# VOLTRE_RESULTS_DIR: read CSVs from there, VOLTRE_OUT_DIR: write the pdf there
RESULTS = os.environ.get('VOLTRE_RESULTS_DIR', os.path.join(os.path.dirname(__file__), 'results'))
OUT_DIR = os.environ.get('VOLTRE_OUT_DIR', RESULTS)
K = 20

COLORS = {
    'volume':        '#F7B7A3',
    'sample':        '#A8D5BA',
    'smart_rej':     '#FDDFA9',
    'intersect_rej': '#C6B8E3',
}

# ── tuneable layout ───────────────────────────────────────────────────────────
PANEL_H  = 1.55  # inches per panel (was 1.9)
HSPACE   = 0.85  # inter-panel gap as fraction of axes height (was 0.9)
YLIM_FAC = 1.48  # headroom above max bar for labels + legend
COL_W    = fig_width_in / 2  # single column width

# ── helpers ───────────────────────────────────────────────────────────────────
def load_results_csv(path):
    xs, results = [], {}
    with open(path, newline='') as f:
        for row in csv.DictReader(f):
            xval = float(row['xval'])
            xs.append(xval)
            results[xval] = {
                't_vol':             float(row['t_vol']),
                't_sample':          float(row['t_sample']),
                'avg_smart_rej':     float(row['avg_smart_rej']),
                'avg_intersect_rej': float(row['avg_intersect_rej']),
                'n_fail':            int(row['n_fail']),
            }
    return xs, results


def stress_bar_plot(ax, xs, results, xlabel, title):
    xs_plotted = [x for x in xs if x in results]
    if not xs_plotted:
        ax.text(0.5, 0.5, 'no data', ha='center', va='center', transform=ax.transAxes)
        return
    has_vol       = any(results[v]['t_vol']             > 0    for v in xs_plotted)
    has_smart     = any(results[v]['avg_smart_rej']     > 0.05 for v in xs_plotted)
    has_intersect = any(results[v]['avg_intersect_rej'] > 0.05 for v in xs_plotted)
    xpos = np.arange(len(xs_plotted))
    t_vols, t_nets, t_srejs, t_irejs = [], [], [], []
    for v in xs_plotted:
        tv = results[v]['t_vol']
        ts = results[v]['t_sample']
        sr = results[v]['avg_smart_rej']
        ir = results[v]['avg_intersect_rej']
        t_net = ts / (1 + sr) if sr > 0 else ts
        t_vols.append(tv)
        t_nets.append(t_net)
        t_srejs.append(ts - t_net)
        t_irejs.append(ir * t_net)
    t_totals  = [tv + tn + tsr + tir
                 for tv, tn, tsr, tir in zip(t_vols, t_nets, t_srejs, t_irejs)]
    max_total = max(t_totals) if t_totals else 1
    bottom = np.zeros(len(xs_plotted))
    if has_vol:
        ax.bar(xpos, t_vols, color=COLORS['volume'],
               label='volume (init.)', width=0.7)
        bottom += np.array(t_vols)
    ax.bar(xpos, t_nets, color=COLORS['sample'],
           label='per sample', bottom=bottom, width=0.7)
    bottom += np.array(t_nets)
    if has_smart:
        ax.bar(xpos, t_srejs, color=COLORS['smart_rej'],
               label='ambiguity corr.', bottom=bottom, width=0.7)
        bottom += np.array(t_srejs)
    if has_intersect:
        ax.bar(xpos, t_irejs, color=COLORS['intersect_rej'],
               label='intersection rej.', bottom=bottom, width=0.7)
    for i, (t, v) in enumerate(zip(t_totals, xs_plotted)):
        nf    = results[v].get('n_fail', 0)
        color = '#d62728' if nf == K else '#333'
        lbl   = f'{t:.1f}s*' if nf else f'{t:.1f}s'
        ax.text(xpos[i], t + max_total * 0.025, lbl,
                ha='center', va='bottom', fontsize=5.5, color=color)
    rot = 45 if len(xs_plotted) > 9 else 0
    ax.set_xticks(xpos)
    ax.set_xticklabels([str(v) for v in xs_plotted],
                       fontsize=6, rotation=rot, ha='right' if rot else 'center')
    ax.set_ylim(0, max_total * YLIM_FAC)
    ax.set_xlabel(xlabel, fontsize=7, labelpad=2)
    ax.set_ylabel('time (s)', fontsize=7)
    ax.set_title(title, fontsize=7.5)
    ax.tick_params(labelsize=6)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    h, lab = ax.get_legend_handles_labels()
    if h:
        ncol = 2 if len(h) >= 3 else 1
        ax.legend(h, lab, loc='upper left', ncol=ncol, frameon=True,
                  handlelength=0.8, fontsize=5.5, borderpad=0.3,
                  labelspacing=0.2, columnspacing=0.8)


# ── load data ─────────────────────────────────────────────────────────────────
N_VALUES_EX1, results_ex1 = load_results_csv(os.path.join(RESULTS, 'results_ex1.csv'))
N_VALUES_EX2, results_ex2 = load_results_csv(os.path.join(RESULTS, 'results_ex2.csv'))
T_VALUES_EX3, results_ex3 = load_results_csv(os.path.join(RESULTS, 'results_ex3.csv'))
N_VALUES_EX1 = [int(v) for v in N_VALUES_EX1]
N_VALUES_EX2 = [int(v) for v in N_VALUES_EX2]
T_EX2 = 2.0

# ── combined 3-panel figure ───────────────────────────────────────────────────
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(COL_W, PANEL_H * 3),
                                     gridspec_kw={'hspace': HSPACE})

stress_bar_plot(ax1, N_VALUES_EX1, results_ex1, r'$n$',
                r'$e_{\mathrm{ex1}}=(\langle a\rangle_{\leq 1})^*$')

stress_bar_plot(ax2, N_VALUES_EX2, results_ex2, r'$n$',
                r'$e_{\mathrm{ex2}}=a^*\!\cdot\!\langle a^*\rangle_{[1,2]}\;(T{=}' + str(T_EX2) + r')$')

stress_bar_plot(ax3, T_VALUES_EX3, results_ex3, r'$T$  ($n=3$)',
                r'$e_{\mathrm{ex3}}=(\langle aa\rangle_{\leq 1}\!\cdot\! a)'
                r'\cap(a\!\cdot\!\langle aa\rangle_{\leq 1})$')

out = os.path.join(OUT_DIR, '11_stress_ex123.pdf')
fig.savefig(out, bbox_inches='tight')
print(f'Saved {out}  (figure size: {COL_W:.2f} x {PANEL_H*3:.2f} in)')
