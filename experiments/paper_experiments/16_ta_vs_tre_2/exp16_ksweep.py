"""
Experiment 16: VolTRE vs wordgen (TA) scalability — k-sweep.

Expression family (dprime5 / Benoit's outreg2):
  e_k = (<r_k.<...<r_1.<a*.g>_[0,1]>_[0,k]>_[0,k+1])*
  k = number of nested request levels, n = 10 (fixed word length)

VolTRE: k=1..K_TRE_MAX, averaged over N_SAMPLES calls.
  t_vol    = one-time slice_volume init (cold cache)
  t_sample = average per-sample time (cache warm, ambiguity-free so no smart_rej)

wordgen (TA, Benoit): parsed from outfelix file (outreg2 = dprime5 equivalent).
  t_split  = splitting reachability graph (TA construction / init)
  t_sample = distribution time / 10 (per-sample cost)
  k=6: run was interrupted due to memory exhaustion (>1h wall time).

Output (in results/):
  exp16_voltre_timing.csv   — VolTRE k-sweep
  exp16_ta_timing.csv       — parsed wordgen results
  exp16_ksweep_m<N>_k<K>.pdf — plot (mode N, K_TRE_SHOW=K)

Plot modes (PLOT_MODE):
  3 — [archived] two panels, log y, lines + markers, T.O. annotation
  4 — [archived] two subplots (init | per-sample), grouped bars, log y, T.O. grey bar
  5 — [current]  two panels (VolTRE | TA), stacked bars, log y, T.O. bars + hatch
  6 — [current]  single panel, paired total-time bars (VolTRE | TA per k), log y,
                 T.O. hatched TA bars; best for showing catastrophic TA scaling
  7 — [current]  same as mode 6 but bars stacked: init (darker) / sample (lighter)
  8 — [local-TA]  run wordgen locally via subprocess; real 1-h timeout + 8 GB memory
                  cap per k; saves exp16_local_ta_timing.csv; generates mode-7-style plot
"""
import os, sys, re, csv, time, warnings
from misc.exceptions import EmptyLanguageError
warnings.filterwarnings('ignore')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
PAPER_EXP = os.path.join(REPO, 'experiments', 'paper_experiments')
for p in [REPO, PAPER_EXP]:
    if p not in sys.path:
        sys.path.insert(0, p)

from experiments.paper_experiments.plot_config import fig_width_in
plt.rcParams.update({"text.usetex": False, "font.family": "sans-serif", "font.serif": []})

from experiments.paper_experiments.expressions_12_requests import (
    build_e_dprime5, time_one,
)

# ── experiment parameters ─────────────────────────────────────────────────────
LOAD_TRE  = True    # set False to rerun VolTRE timing
LOAD_TA   = True    # set False to reparse outfelix / rerun local wordgen

K_TRE_MAX    = 9    # k=10 is empty for n=10 (min cycle needs k+1=11 symbols)
K_TA_TIMEOUT = 6    # first k where TA failed (shown as T.O.)
N            = 10
N_SAMPLES    = 10

# ── plot configuration ────────────────────────────────────────────────────────
PLOT_MODE   = 8     # see mode descriptions in docstring above

# K values for VolTRE panel:
#   6 → same x-range as TA — most direct comparison
#   7 → one point past TA's failure — shows VolTRE keeps working
#   9 → full data — shows complete scaling curve
K_TRE_SHOW  = 7

TIMEOUT_S   = 3600  # T.O. bar height in mode 5 (seconds, 1h)

# ── paths ─────────────────────────────────────────────────────────────────────
OUTFELIX = os.path.join(os.path.dirname(__file__),
                         '20260616_benoit_results', 'outfelix')
RESULTS  = os.path.join(os.path.dirname(__file__), 'results')
os.makedirs(RESULTS, exist_ok=True)

CSV_TRE      = os.path.join(RESULTS, 'exp16_voltre_timing.csv')
CSV_TA       = os.path.join(RESULTS, 'exp16_ta_timing.csv')
CSV_TA_LOCAL = os.path.join(RESULTS, 'exp16_local_ta_timing.csv')

# wordgen binary built from /workspace/wordgen into /tmp/wordgen_build
WORDGEN_BIN  = '/tmp/wordgen_build/_build/default/src/wordgen.exe'
# memory cap per wordgen subprocess (bytes) — protects container from OOM
WORDGEN_MEM_LIMIT = 8 * 1024 ** 3   # 8 GB virtual address space
# k values to attempt for the local TA run (beyond k=5 is expected to OOM/timeout)
K_LOCAL_MAX  = 9

DEADLINES = [(f'r{i}', i) for i in range(1, K_TRE_MAX + 1)]

COLORS = {
    'init':   '#F7B7A3',   # warm orange — vol init / TA split
    'sample': '#A8D5BA',   # cool green  — per-sample time
}

EXPR_TITLE = (r'$e_k=(\langle r_k\cdot\langle\cdots\langle a^*g'
              r'\rangle_{\leq 1}\cdots\rangle_{\leq k}\rangle_{\leq k{+}1})^*$')

PANEL_H  = 1.9
YLIM_FAC = 1.48


# ── VolTRE timing ─────────────────────────────────────────────────────────────
def run_voltre_timing():
    rows = []
    np.random.seed(42)
    fieldnames = ['k', 't_vol', 't_sample', 'avg_smart_rej', 'expr']
    with open(CSV_TRE, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for k in range(1, K_TRE_MAX + 1):
            phi, expr = build_e_dprime5(DEADLINES[:k])
            print(f'  VolTRE k={k}: {expr[:80]}')
            try:
                t_vol, t_sper, avg_sr, avg_ir = time_one(phi, N, N_SAMPLES)
            except EmptyLanguageError:
                print(f'    k={k}: empty language for n={N} — stopping.')
                break
            row = {'k': k, 't_vol': t_vol, 't_sample': t_sper,
                   'avg_smart_rej': avg_sr, 'expr': expr}
            rows.append(row); w.writerow(row); f.flush()
            print(f'    t_vol={t_vol:.3f}s  t_sample={t_sper:.3f}s')
    print(f'  saved {CSV_TRE}')
    return rows


def load_voltre_timing():
    with open(CSV_TRE, newline='') as f:
        return [{'k': int(r['k']), 't_vol': float(r['t_vol']),
                 't_sample': float(r['t_sample']),
                 'avg_smart_rej': float(r['avg_smart_rej']),
                 'expr': r['expr']}
                for r in csv.DictReader(f)]


# ── wordgen (TA) timing — parse outfelix ──────────────────────────────────────
# outfelix alternates: outreg1 result, outreg2 result, outreg1, outreg2, ...
# k=5 is duplicated; k=6 is truncated (memory exhaustion).
# outreg2 (= dprime5): positions 1,3,5,7,9 (0-indexed) → k=1..5.
_RE_SPLIT = re.compile(r'Splitting reachability graph.*?\[(\d+(?:\.\d+)?)s\]')
_RE_DIST  = re.compile(r'Computing Distribution\[.*?\]\s*\[(\d+(?:\.\d+)?)s\]')
_RE_VOL   = re.compile(r'Volume in initial state:([\d.]+)')
_RE_FWD   = re.compile(r'Computing forward reachability graph')


def parse_outfelix():
    with open(OUTFELIX) as f:
        text = f.read()
    blocks = _RE_FWD.split(text)[1:]
    parsed = []
    for blk in blocks:
        t_split = float(_RE_SPLIT.search(blk).group(1)) if _RE_SPLIT.search(blk) else None
        t_dist  = float(_RE_DIST.search(blk).group(1))  if _RE_DIST.search(blk)  else None
        m_vol   = _RE_VOL.search(blk)
        volume  = float(m_vol.group(1)) if m_vol else None
        parsed.append({'t_split': t_split, 't_dist': t_dist,
                       'ok': (volume is not None) and (volume > 0)})
    rows = []
    for k, idx in enumerate([1, 3, 5, 7, 9], start=1):
        if idx >= len(parsed):
            break
        blk = parsed[idx]
        rows.append({'k': k,
                     't_split':  blk['t_split'] or 0.0,
                     't_sample': (blk['t_dist'] or 0.0) / N_SAMPLES,
                     'status':   'ok' if blk['ok'] else 'fail'})
        print(f'  wordgen k={k}: split={rows[-1]["t_split"]:.3f}s  '
              f'sample={rows[-1]["t_sample"]:.4f}s  [{rows[-1]["status"]}]')
    with open(CSV_TA, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['k', 't_split', 't_sample', 'status'])
        w.writeheader(); w.writerows(rows)
    print(f'  saved {CSV_TA}')
    return rows


def load_ta_timing():
    with open(CSV_TA, newline='') as f:
        return [{'k': int(r['k']), 't_split': float(r['t_split']),
                 't_sample': float(r['t_sample']), 'status': r['status']}
                for r in csv.DictReader(f)]


# ── shared helpers ────────────────────────────────────────────────────────────
def _fmt(t):
    if t < 0.001: return '<0.001s'
    if t < 10:    return f'{t:.2f}s'
    return f'{t:.1f}s'


def _bar_labels(ax, xpos, totals, max_t, pad_frac=0.025, fontsize=5.5, colors=None,
                log_y=False):
    for i, t in enumerate(totals):
        if t <= 0:
            continue
        c = colors[i] if colors else '#333'
        y = t * (1 + pad_frac) if log_y else (t + (max_t or 1) * pad_frac)
        ax.text(xpos[i], y, _fmt(t), ha='center', va='bottom', fontsize=fontsize, color=c)


def _finish_ax(ax, xpos, xlabels, ylim_top, xlabel, ylabel, title,
               legend_loc='upper left', log_y=False, show_legend=True):
    ax.set_xticks(xpos)
    ax.set_xticklabels(xlabels, fontsize=6)
    if log_y:
        ax.set_yscale('log')
        if ylim_top is not None:
            ax.set_ylim(top=ylim_top)
    else:
        ax.set_ylim(0, ylim_top)
    ax.set_xlabel(xlabel, fontsize=7, labelpad=2)
    ax.set_ylabel(ylabel, fontsize=7)
    ax.set_title(title, fontsize=6.8)
    ax.tick_params(labelsize=6)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    if show_legend:
        h, lab = ax.get_legend_handles_labels()
        if h:
            ax.legend(h, lab, loc=legend_loc, fontsize=5.5, frameon=True,
                      handlelength=0.8, borderpad=0.3, labelspacing=0.2)


# ── Mode 3 [archived]: log-scale lines, two panels ───────────────────────────
def plot_m3(tre_rows, ta_rows, k_tre_show, ta_timeout_k, out_path):
    C_TRE, C_TA = '#2166ac', '#d6604d'
    tr = [r for r in tre_rows if r['k'] <= k_tre_show]
    ta = [r for r in ta_rows  if r['status'] == 'ok']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(fig_width_in, PANEL_H),
                                    gridspec_kw={'wspace': 0.52})
    for ax, rows, color, lbl, to_k in [
        (ax1, tr, C_TRE, 'VolTRE',                     None),
        (ax2, ta, C_TA,  'wordgen (equivalent automaton)', ta_timeout_k),
    ]:
        ks   = [r['k']        for r in rows]
        inits = [r.get('t_vol', r.get('t_split', 0)) for r in rows]
        smps  = [r['t_sample'] for r in rows]
        tots  = [i + s for i, s in zip(inits, smps)]
        ax.semilogy(ks, inits, 'o--', color=color, lw=0.9, ms=3.5, alpha=0.7, label='init')
        ax.semilogy(ks, smps,  's-',  color=color, lw=1.2, ms=3.5,            label='per sample')
        ax.semilogy(ks, tots,  '^-',  color=color, lw=1.4, ms=4,   alpha=0.4,
                    label=f'total (×{N_SAMPLES})')
        if to_k:
            ax.axvline(to_k - 0.5, color='#aaa', lw=0.8, ls='--')
            ax.annotate(f'k={to_k}: T.O.', xytext=(0.97, 0.92),
                        textcoords='axes fraction', xy=(to_k, 1), xycoords=('data','axes fraction'),
                        fontsize=6, color='#d62728', ha='right',
                        arrowprops=dict(arrowstyle='->', color='#d62728', lw=0.8))
        ax.set_xlabel('$k$', fontsize=7); ax.set_ylabel('time (s)', fontsize=7)
        ax.set_title(f'{lbl}\n{EXPR_TITLE}', fontsize=6.5)
        ax.set_xticks(range(1, (to_k or max(ks)) + 1))
        ax.tick_params(labelsize=6)
        ax.grid(axis='both', linestyle='--', alpha=0.25)
        ax.legend(loc='upper left', fontsize=5.5, frameon=True,
                  handlelength=1.0, borderpad=0.3, labelspacing=0.2)
    fig.savefig(out_path, bbox_inches='tight')
    print(f'  saved {out_path}')


# ── Mode 4 [archived]: grouped bars, log y, two sub-panels ───────────────────
def plot_m4(tre_rows, ta_rows, k_tre_show, ta_timeout_k, out_path):
    C_TRE, C_TA, C_TO = '#2166ac', '#d6604d', '#aaaaaa'
    all_k   = list(range(1, max(k_tre_show, ta_timeout_k) + 1))
    xpos    = np.arange(len(all_k))
    w       = 0.38
    tre_map = {r['k']: r for r in tre_rows}
    ta_map  = {r['k']: r for r in ta_rows if r['status'] == 'ok'}
    eps     = 1e-4

    fig, (ax_i, ax_s) = plt.subplots(2, 1, figsize=(fig_width_in / 2, PANEL_H * 2),
                                      gridspec_kw={'hspace': 0.55})
    for ax, key_t, key_a, ylabel, sfx in [
        (ax_i, 't_vol',    't_split',  'init time (s)',       'init'),
        (ax_s, 't_sample', 't_sample', 'per-sample time (s)', 'per sample'),
    ]:
        tv = [max(tre_map[k][key_t], eps) if k in tre_map else np.nan for k in all_k]
        ta = [max(ta_map[k][key_a],  eps) if k in ta_map  else np.nan for k in all_k]
        ax.bar(xpos - w/2, tv, w, color=C_TRE, alpha=0.85, label='VolTRE (TRE)')
        ax.bar(xpos + w/2, ta, w, color=C_TA,  alpha=0.85, label='Wordgen (TA)', zorder=3)
        to_i = all_k.index(ta_timeout_k)
        ymax = np.nanmax([v for v in ta + tv if not np.isnan(v)])
        ax.bar(to_i + w/2, ymax * 2, w, color=C_TO, hatch='//', alpha=0.7, zorder=2,
               label='T.O.' if sfx == 'init' else '')
        ax.text(to_i + w/2, ymax * 2.2, 'T.O.', ha='center', va='bottom',
                fontsize=5.5, color='#d62728')
        ax.set_yscale('log')
        _finish_ax(ax, xpos, [str(k) for k in all_k], None,
                   '$k$', ylabel, f'{EXPR_TITLE}\n{sfx}')
    fig.savefig(out_path, bbox_inches='tight')
    print(f'  saved {out_path}')


# ── Mode 6 [current]: single panel, paired total-time bars, log y ─────────────
#
# For each k: two side-by-side bars (VolTRE total | TA total), log y.
# TA T.O. bars (k >= ta_timeout_k) use same TA colour + hatch — no legend entry.
# Best for showing TA's catastrophic scaling vs VolTRE's near-flat curve.
def plot_m6(tre_rows, ta_rows, k_tre_show, ta_timeout_k, timeout_s, out_path):
    C_TRE = '#2166ac'
    C_TA  = '#d6604d'

    tre_map = {r['k']: r for r in tre_rows}
    ta_map  = {r['k']: r for r in ta_rows if r['status'] == 'ok'}

    all_k = list(range(1, k_tre_show + 1))
    xpos  = np.arange(len(all_k))
    w     = 0.38

    tre_tots = [tre_map[k]['t_vol'] + tre_map[k]['t_sample'] if k in tre_map else np.nan
                for k in all_k]
    ta_tots  = [max(ta_map[k]['t_split'] + ta_map[k]['t_sample'], LOG_EPS)
                if k in ta_map and k < ta_timeout_k else 0.0
                for k in all_k]

    fig, ax = plt.subplots(1, 1, figsize=(fig_width_in * 0.75, PANEL_H * 1.3))

    ax.bar(xpos - w/2, tre_tots, w, color=C_TRE, label='VolTRE (TRE)', alpha=0.85)
    ax.bar(xpos + w/2, ta_tots,  w, color=C_TA,  label='Wordgen (TA)',  alpha=0.85)

    # T.O. bars — same TA colour + hatch, no legend entry
    to_ks = [k for k in all_k if k >= ta_timeout_k]
    for k in to_ks:
        xi = xpos[all_k.index(k)]
        ax.bar(xi + w/2, timeout_s, w, color=C_TA, alpha=0.85,
               hatch='//', edgecolor='#a03020')
    if to_ks:
        ax.text((xpos[0] + xpos[-1]) / 2, timeout_s * 2, 'T.O. (>1 h)',
                ha='center', va='center', fontsize=5.5, color='#d62728')

    # horizontal cutoff line
    ax.axhline(timeout_s, color='#d62728', linewidth=0.8, linestyle='--', alpha=0.7,
               zorder=5)

    ax.set_yscale('log')
    ax.set_ylim(bottom=LOG_EPS * 0.5, top=timeout_s * 4)
    ax.set_xticks(xpos)
    ax.set_xticklabels([str(k) for k in all_k], fontsize=6)
    ax.set_xlabel('$k$', fontsize=7, labelpad=2)
    ax.set_ylabel('total time (s)', fontsize=7)
    ax.set_title(EXPR_TITLE, fontsize=6.8)
    ax.tick_params(labelsize=6)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.legend(loc='upper left', fontsize=5.5, frameon=True,
              handlelength=0.8, borderpad=0.3, labelspacing=0.2)
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')
    print(f'  saved {out_path}')


# ── Mode 7 [current]: same as mode 6, stacked init (darker) / sample (lighter) ─
def plot_m7(tre_rows, ta_rows, k_tre_show, ta_timeout_k, timeout_s, out_path):
    C_TRE_INIT   = '#2166ac'   # dark blue  — VolTRE init
    C_TRE_SAMPLE = '#92c5de'   # light blue — VolTRE sample
    C_TA_INIT    = '#d6604d'   # dark red   — TA init
    C_TA_SAMPLE  = '#f4a582'   # light salmon — TA sample

    tre_map = {r['k']: r for r in tre_rows}
    ta_map  = {r['k']: r for r in ta_rows if r['status'] == 'ok'}

    all_k = list(range(1, k_tre_show + 1))
    xpos  = np.arange(len(all_k))
    w     = 0.38

    tre_inits   = [max(tre_map[k]['t_vol'],    LOG_EPS) if k in tre_map else np.nan for k in all_k]
    tre_samples = [max(tre_map[k]['t_sample'], LOG_EPS) if k in tre_map else np.nan for k in all_k]
    ta_inits    = [max(ta_map[k]['t_split'],   LOG_EPS) if k in ta_map and k < ta_timeout_k else 0.0 for k in all_k]
    ta_samples  = [max(ta_map[k]['t_sample'],  LOG_EPS) if k in ta_map and k < ta_timeout_k else 0.0 for k in all_k]

    fig, ax = plt.subplots(1, 1, figsize=(fig_width_in * 0.75, PANEL_H * 1.3))

    ax.bar(xpos - w/2, tre_inits,   w, color=C_TRE_INIT,   alpha=0.9, label='VolTRE — init')
    ax.bar(xpos - w/2, tre_samples, w, color=C_TRE_SAMPLE, alpha=0.9, label='VolTRE — sample',
           bottom=tre_inits)
    ax.bar(xpos + w/2, ta_inits,    w, color=C_TA_INIT,    alpha=0.9, label='Wordgen — init')
    ax.bar(xpos + w/2, ta_samples,  w, color=C_TA_SAMPLE,  alpha=0.9, label='Wordgen — sample',
           bottom=ta_inits)

    # T.O. bars — TA init colour + hatch
    to_ks = [k for k in all_k if k >= ta_timeout_k]
    for k in to_ks:
        xi = xpos[all_k.index(k)]
        ax.bar(xi + w/2, timeout_s, w, color=C_TA_INIT, alpha=0.85,
               hatch='//', edgecolor='#a03020')
    if to_ks:
        ax.text((xpos[0] + xpos[-1]) / 2, timeout_s * 2, 'T.O. (>1 h)',
                ha='center', va='center', fontsize=5.5, color='#d62728')

    ax.axhline(timeout_s, color='#d62728', linewidth=0.8, linestyle='--', alpha=0.7, zorder=5)

    ax.set_yscale('log')
    ax.set_ylim(bottom=LOG_EPS * 0.5, top=timeout_s * 4)
    ax.set_xticks(xpos)
    ax.set_xticklabels([str(k) for k in all_k], fontsize=6)
    ax.set_xlabel('$k$', fontsize=7, labelpad=2)
    ax.set_ylabel('total time (s)', fontsize=7)
    ax.set_title(EXPR_TITLE, fontsize=6.8)
    ax.tick_params(labelsize=6)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.legend(loc='upper left', fontsize=5.5, frameon=True,
              handlelength=0.8, borderpad=0.3, labelspacing=0.2)
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')
    print(f'  saved {out_path}')


# ── Mode 5 [current]: stress-test style stacked bars, log y, T.O. bars ───────
#
# Two panels side by side (VolTRE | wordgen), log y per panel.
# VolTRE k=1..k_tre_show; TA k=1..k_tre_show, with T.O. bars for k>=ta_timeout_k.
# T.O. bars use TA orange + hatch; NO legend entry, just a 'T.O.' text label.
# Legend only in VolTRE panel to avoid overlap and confusion with T.O. bars.
LOG_EPS = 1e-3   # floor for log-scale bars so zero-height bars don't collapse


def plot_m5(tre_rows, ta_rows, k_tre_show, ta_timeout_k, timeout_s, out_path):
    tre   = [r for r in tre_rows if r['k'] <= k_tre_show]
    ta_map = {r['k']: r for r in ta_rows if r['status'] == 'ok'}

    TIMEOUT_DISPLAY = timeout_s          # bar height = actual timeout (1 h, where Benoit cut it)
    TA_YLIM         = timeout_s * 1.8   # headroom above bar for T.O. label

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(fig_width_in, PANEL_H),
                                    gridspec_kw={'wspace': 0.52})

    # ── left panel: VolTRE ────────────────────────────────────────────────────
    tre_k  = [r['k'] for r in tre]
    t_vols = [max(r['t_vol'],    LOG_EPS) for r in tre]
    t_smps = [max(r['t_sample'], LOG_EPS) for r in tre]
    t_tots = [r['t_vol'] + r['t_sample']  for r in tre]
    max_tre = max(t_tots)
    xp1    = np.arange(len(tre_k))

    ax1.bar(xp1, t_vols, color=COLORS['init'],   label='init',       width=0.65)
    ax1.bar(xp1, t_smps, color=COLORS['sample'], label='per sample', width=0.65,
            bottom=t_vols)
    _bar_labels(ax1, xp1, t_tots, None, pad_frac=0.20, log_y=True)
    _finish_ax(ax1, xp1, [str(k) for k in tre_k],
               max_tre * 6, '$k$', 'time (s)',
               f'VolTRE\n{EXPR_TITLE}', legend_loc='upper left', log_y=True)

    # ── right panel: wordgen (TA) ─────────────────────────────────────────────
    # x-axis mirrors VolTRE: k=1..k_tre_show
    all_k2  = list(range(1, k_tre_show + 1))
    xp2     = np.arange(len(all_k2))
    real_ks = [k for k in all_k2 if k < ta_timeout_k and k in ta_map]
    real_xi = [xp2[all_k2.index(k)] for k in real_ks]

    # real TA bars (no labels — legend lives in left panel only)
    if real_ks:
        ta_spl = [max(ta_map[k]['t_split'],  LOG_EPS) for k in real_ks]
        ta_smp = [max(ta_map[k]['t_sample'], LOG_EPS) for k in real_ks]
        ta_tots_raw = [ta_map[k]['t_split'] + ta_map[k]['t_sample'] for k in real_ks]
        ax2.bar(real_xi, ta_spl, color=COLORS['init'],   width=0.65)
        ax2.bar(real_xi, ta_smp, color=COLORS['sample'], width=0.65, bottom=ta_spl)
        lbl_mask = [t > LOG_EPS * 5 for t in ta_tots_raw]
        _bar_labels(ax2, [x for x, m in zip(real_xi, lbl_mask) if m],
                    [t for t, m in zip(ta_tots_raw, lbl_mask) if m],
                    None, pad_frac=0.20, log_y=True)

    # T.O. bars for all k >= ta_timeout_k — same orange colour + hatch, no label
    to_ks = [k for k in all_k2 if k >= ta_timeout_k]
    to_xi = [xp2[all_k2.index(k)] for k in to_ks]
    for xi in to_xi:
        ax2.bar(xi, TIMEOUT_DISPLAY, color=COLORS['init'], width=0.65,
                hatch='//', edgecolor='#c08060')
    # single "T.O." annotation above the first T.O. bar
    if to_xi:
        ax2.text(to_xi[0], TIMEOUT_DISPLAY * 1.12, 'T.O. (>1 h)',
                 ha='center', va='bottom', fontsize=5.5, color='#d62728', linespacing=1.2)

    _finish_ax(ax2, xp2, [str(k) for k in all_k2],
               TA_YLIM, '$k$', 'time (s)',
               f'wordgen (equivalent automaton)\n{EXPR_TITLE}',
               log_y=True, show_legend=False)

    fig.savefig(out_path, bbox_inches='tight')
    print(f'  saved {out_path}')


# ── Mode 8: run wordgen locally, real timeout + memory cap ────────────────────
#
# Builds the same e_k regexp family, runs wordgen as a subprocess for each k.
# Per-process memory capped at WORDGEN_MEM_LIMIT (virtual address space).
# Timeout = TIMEOUT_S (3600 s). Results saved to CSV_TA_LOCAL; never overwrites
# existing CSVs from Benoit's run or VolTRE data.

import subprocess, signal, resource as _resource

_RE_SPLIT_L = re.compile(r'Splitting reachability graph.*?\[(\d+(?:\.\d+)?)s\]')
_RE_DIST_L  = re.compile(r'Computing Distribution\[.*?\]\s*\[(\d+(?:\.\d+)?)s\]')


def _wordgen_regexp(k):
    """Single-char wordgen regexp for e_k (dprime5 family).
    r_i → chr(ord('r') + i - 1):  r1='r', r2='s', r3='t', ...
    Innermost: a*g  (a = wildcard before grant g).
    """
    inner = 'a*g'
    for i in range(k):          # i=0 → r1, deadline 1
        c = chr(ord('r') + i)
        inner = f'{c}<{inner}>_[0,{i + 1}]'
    return f'(<{inner}>_[0,{k + 1}])*'


def _run_wordgen(regexp, n, n_traj, timeout_s, mem_limit):
    """Run wordgen subprocess. Returns (t_split, t_dist_total, status, log).
    t_dist_total is the total distribution time for all n_traj samples.
    status: 'ok' | 'timeout' | 'oom' | 'error:<code>'
    """
    if not os.path.isfile(WORDGEN_BIN):
        return None, None, 'no_binary', 'wordgen binary not found'

    def _set_limits():
        _resource.setrlimit(_resource.RLIMIT_AS, (mem_limit, mem_limit))

    cmd = [WORDGEN_BIN, '--regexp', regexp, '--poly', str(n), '--traj', str(n_traj)]
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            preexec_fn=_set_limits, text=True,
        )
        try:
            stdout, _ = proc.communicate(timeout=timeout_s)
        except subprocess.TimeoutExpired:
            proc.kill()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                pass
            return None, None, 'timeout', '(killed after timeout)'

        if proc.returncode not in (0, None):
            # SIGKILL (−9 or 137) typically means OOM from setrlimit or kernel OOM
            code = proc.returncode
            if code in (-9, 137, -signal.SIGKILL):
                return None, None, 'oom', stdout[:500]
            return None, None, f'error:{code}', stdout[:500]

        m_split = _RE_SPLIT_L.search(stdout)
        m_dist  = _RE_DIST_L.search(stdout)
        t_split = float(m_split.group(1)) if m_split else None
        t_dist  = float(m_dist.group(1))  if m_dist  else None
        return t_split, t_dist, 'ok', stdout
    except Exception as e:
        return None, None, f'exception:{type(e).__name__}', str(e)


def run_local_ta(k_max, n, n_traj, timeout_s, mem_limit):
    """Run wordgen for k=1..k_max. Returns list of row dicts."""
    rows = []
    fieldnames = ['k', 't_split', 't_sample', 't_dist_total', 'status', 'regexp', 'n', 'n_traj']
    with open(CSV_TA_LOCAL, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for k in range(1, k_max + 1):
            regexp = _wordgen_regexp(k)
            print(f'  k={k}  regexp={regexp}')
            t0_wall = time.perf_counter()
            t_split, t_dist_total, status, log = _run_wordgen(
                regexp, n, n_traj, timeout_s, mem_limit)
            elapsed = time.perf_counter() - t0_wall
            t_sample = (t_dist_total / n_traj) if (t_dist_total is not None) else None
            print(f'    status={status}  t_split={t_split}  '
                  f't_dist_total={t_dist_total}  wall={elapsed:.1f}s')
            if status != 'ok':
                print(f'    log: {log[:200]}')
            row = {
                'k':            k,
                't_split':      t_split,
                't_sample':     t_sample,
                't_dist_total': t_dist_total,
                'status':       status,
                'regexp':       regexp,
                'n':            n,
                'n_traj':       n_traj,
            }
            rows.append(row)
            csv_row = {
                'k':            k,
                't_split':      f'{t_split:.6f}'      if t_split      is not None else '',
                't_sample':     f'{t_sample:.6f}'     if t_sample     is not None else '',
                't_dist_total': f'{t_dist_total:.6f}' if t_dist_total is not None else '',
                'status':       status,
                'regexp':       regexp,
                'n':            n,
                'n_traj':       n_traj,
            }
            w.writerow(csv_row)
            f.flush()
            # stop early if two consecutive non-ok (timeout or oom cascade)
            if len(rows) >= 2 and all(r['status'] not in ('ok',) for r in rows[-2:]):
                print(f'  Two consecutive failures — stopping at k={k}.')
                break
    print(f'  saved {CSV_TA_LOCAL}')
    return rows


def load_local_ta():
    with open(CSV_TA_LOCAL, newline='') as f:
        out = []
        for r in csv.DictReader(f):
            out.append({
                'k':            int(r['k']),
                't_split':      float(r['t_split'])      if r['t_split']      else None,
                't_sample':     float(r['t_sample'])     if r['t_sample']     else None,
                't_dist_total': float(r['t_dist_total']) if r['t_dist_total'] else None,
                'status':       r['status'],
            })
        return out


def plot_m8(tre_rows, local_ta_rows, k_tre_show, timeout_s, out_path):
    """Mode-7-style stacked bars using locally-measured TA data."""
    C_TRE_INIT   = '#2166ac'
    C_TRE_SAMPLE = '#92c5de'
    C_TA_INIT    = '#d6604d'
    C_TA_SAMPLE  = '#f4a582'

    tre_map    = {r['k']: r for r in tre_rows}
    ta_map     = {r['k']: r for r in local_ta_rows if r['status'] == 'ok'}
    ta_fail    = {r['k']: r['status'] for r in local_ta_rows if r['status'] != 'ok'}

    k_ta_max   = max((r['k'] for r in local_ta_rows), default=0)
    all_k      = list(range(1, max(k_tre_show, k_ta_max) + 1))
    xpos       = np.arange(len(all_k), dtype=float)
    w          = 0.38

    # Use LOG_EPS as floor everywhere — set_yscale('log') must come BEFORE bar()
    # calls; setting it after corrupts bar transforms when any bottom=0 exists.
    tre_inits   = np.array([max(tre_map[k]['t_vol'],    LOG_EPS) if k in tre_map else np.nan for k in all_k])
    tre_samples = np.array([max(tre_map[k]['t_sample'], LOG_EPS) if k in tre_map else np.nan for k in all_k])
    ta_inits    = np.array([max(ta_map[k]['t_split'],   LOG_EPS) if k in ta_map else LOG_EPS for k in all_k])
    ta_samples  = np.array([max(ta_map[k]['t_sample'],  LOG_EPS) if k in ta_map else LOG_EPS for k in all_k])

    fig, ax = plt.subplots(1, 1, figsize=(fig_width_in * 0.75, PANEL_H * 1.3))

    # Set log scale BEFORE drawing bars so all bar artists are created in log space
    ax.set_yscale('log')
    ax.set_ylim(bottom=LOG_EPS * 0.5, top=timeout_s * 4)

    ax.bar(xpos - w/2, tre_inits,   w, color=C_TRE_INIT,   alpha=0.9, label='VolTRE — init')
    ax.bar(xpos - w/2, tre_samples, w, color=C_TRE_SAMPLE, alpha=0.9, label='VolTRE — sample',
           bottom=tre_inits)
    ax.bar(xpos + w/2, ta_inits,    w, color=C_TA_INIT,    alpha=0.9, label='Wordgen — init')
    ax.bar(xpos + w/2, ta_samples,  w, color=C_TA_SAMPLE,  alpha=0.9, label='Wordgen — sample',
           bottom=ta_inits)

    # T.O. / OOM bars for failed TA ks
    to_ks = [k for k in all_k if k in ta_fail]
    for k in to_ks:
        xi = xpos[all_k.index(k)]
        hatch = '//' if 'timeout' in ta_fail[k] else 'xx'
        ax.bar(xi + w/2, timeout_s, w, color=C_TA_INIT, alpha=0.85,
               hatch=hatch, edgecolor='#a03020')
        short = 'T.O.' if 'timeout' in ta_fail[k] else 'OOM'
        ax.text(xi + w/2, timeout_s * 1.15, short,
                ha='center', va='bottom', fontsize=5, color='#d62728')

    ax.axhline(timeout_s, color='#d62728', linewidth=0.8, linestyle='--', alpha=0.7, zorder=5)
    ax.set_xticks(xpos)
    ax.set_xticklabels([str(k) for k in all_k], fontsize=6)
    ax.set_xlabel('$k$', fontsize=7, labelpad=2)
    ax.set_ylabel('total time (s)', fontsize=7)
    ax.set_title(EXPR_TITLE, fontsize=6.5)
    ax.tick_params(labelsize=6)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.legend(loc='upper left', fontsize=5.5, frameon=True,
              handlelength=0.8, borderpad=0.3, labelspacing=0.2)
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')
    print(f'  saved {out_path}')


# ── main ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print(f'=== Exp 16: VolTRE vs wordgen  '
          f'[mode={PLOT_MODE}  K_TRE_SHOW={K_TRE_SHOW}  n={N}  samples={N_SAMPLES}] ===')

    if PLOT_MODE == 8:
        # ── Mode 8: run wordgen locally and plot ─────────────────────────────
        print('\n--- VolTRE (from csv) ---')
        tre_rows = load_voltre_timing() if (LOAD_TRE and os.path.exists(CSV_TRE)) \
                   else run_voltre_timing()

        print(f'\n--- wordgen LOCAL run (k=1..{K_LOCAL_MAX}, timeout={TIMEOUT_S}s, '
              f'mem_limit={WORDGEN_MEM_LIMIT // 1024**3}GB) ---')
        if LOAD_TA and os.path.exists(CSV_TA_LOCAL):
            print('  loading existing local TA csv ...')
            local_ta_rows = load_local_ta()
        else:
            local_ta_rows = run_local_ta(K_LOCAL_MAX, N, N_SAMPLES, TIMEOUT_S, WORDGEN_MEM_LIMIT)

        k_ta_max = max((r['k'] for r in local_ta_rows), default=K_TRE_SHOW)
        k_show   = max(K_TRE_SHOW, k_ta_max)
        path     = os.path.join(RESULTS, f'exp16_ksweep_v8_k{k_show}.pdf')
        print(f'\n  mode=8  k_show={k_show} ...')
        plot_m8(tre_rows, local_ta_rows, k_show, TIMEOUT_S, path)

    else:
        print('\n--- VolTRE ---')
        tre_rows = load_voltre_timing() if (LOAD_TRE and os.path.exists(CSV_TRE)) \
                   else run_voltre_timing()

        print('\n--- wordgen (TA, from outfelix) ---')
        ta_rows  = load_ta_timing()    if (LOAD_TA  and os.path.exists(CSV_TA))  \
                   else parse_outfelix()

        for k_show in [6, 7, 9]:
            path = os.path.join(RESULTS, f'exp16_ksweep_v{PLOT_MODE}_k{k_show}.pdf')
            print(f'\n  mode={PLOT_MODE}  K_TRE_SHOW={k_show} ...')
            if PLOT_MODE == 3:
                plot_m3(tre_rows, ta_rows, k_show, K_TA_TIMEOUT, path)
            elif PLOT_MODE == 4:
                plot_m4(tre_rows, ta_rows, k_show, K_TA_TIMEOUT, path)
            elif PLOT_MODE == 5:
                plot_m5(tre_rows, ta_rows, k_show, K_TA_TIMEOUT, TIMEOUT_S, path)
            elif PLOT_MODE == 6:
                plot_m6(tre_rows, ta_rows, k_show, K_TA_TIMEOUT, TIMEOUT_S, path)
            elif PLOT_MODE == 7:
                plot_m7(tre_rows, ta_rows, k_show, K_TA_TIMEOUT, TIMEOUT_S, path)

    print('\nDone.')
