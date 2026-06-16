import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import random

from parse.quickparse import quickparse
from volume.slice_volume import slice_volume
from volume.VolumePoly import continuous_convolution
from sample.sample import sample
from sample.TimedWord import TimedWord
from sympy.core.cache import clear_cache as clear_sympy_cache


# ─── Plot style ───────────────────────────────────────────────────────────────
# Matches plot_config.py in this folder; set text.usetex=True if LaTeX is available.
import logging
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Latin Modern Roman"],
    "text.usetex": False,
    "font.size": 11,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
})

COLORS = {
    "volume":       "#F7B7A3",  # warm orange — slice_volume (fills lru_cache)
    "sample":       "#A8D5BA",  # cool green  — sample() calls (cache warm)
    "smart_rej":    "#FDDFA9",  # yellow      — time wasted on smart-rejection retries
    "intersect_rej":"#C6B8E3",  # purple      — time wasted on intersection retries
}

DEADLINES_DEMO = [("r1", 1), ("r2", 2), ("r3", 3), ("r4", 4), ("r5", 5), ("r6", 6), ("r7", 7)]


# ─── Expression builders ──────────────────────────────────────────────────────

def build_e_single(r, T):
    # eq 20: r_i always answered by g within T_i.
    s = f"(<{r} . g>_[0,{T}]) *"
    return quickparse(s, string=True), s

def build_e_T(deadlines):
    # eq 21: e_T = intersection of all e_{T_i}.
    # VolTRE can SAMPLE from this (rejection budget) but cannot compute its volume
    # (slice_volume raises ValueError for & subexpressions).
    parts = [f"((<{r} . g>_[0,{T}]) *)" for r, T in deadlines]
    s = " & ".join(parts)
    return quickparse(s, string=True), s

def build_e_prime(deadlines):
    # eq 22: e'_T = e_T & ((EPS + r_Tk) . ... . (EPS + r_T1) . g)*
    # Same optional-request body as e''_T but without nested timing.
    # Timing is enforced by the intersection with e_T.
    # Hard to sample (multiple intersections); no analytic volume.
    #
    # Structured as right-fold: e_T1 & (e_T2 & (... & kleene))
    # so that sample() always sees a plain Kleene as child1 (needed for
    # disambiguate), while match() handles the nested intersections in child2.
    body = " . ".join(f"(EPS + {r})" for r, T in reversed(deadlines))
    s = f"({body} . g) *"
    for r, T in reversed(deadlines):  # wrap from Tk down to T1 so T1 is outermost
        s = f"((<{r} . g>_[0,{T}]) *) & ({s})"
    return quickparse(s, string=True), s


def build_e_dprime(deadlines):
    # eq 23 (old): nested timed, requests optional via EPS, timer starts at cycle/nesting open.
    # (<(EPS+r3).<(EPS+r2).<(EPS+r1).g>_[0,1]>_[0,2]>_[0,3])*
    r1, T1 = deadlines[0]
    inner = f"<(EPS + {r1}) . g>_[0,{T1}]"
    for r_i, T_i in deadlines[1:]:
        inner = f"<(EPS + {r_i}) . {inner}>_[0,{T_i}]"
    s = f"({inner}) *"
    return quickparse(s, string=True), s


def build_e_dprime2(deadlines):
    # Nicolas 1st email: timer starts from request arrival (request outside bracket).
    # Outermost request is mandatory; grant is alternative at every level.
    # (r3.<g+r2.<g+r1.<g>_[0,1]>_[0,2]>_[0,3])*
    out = "g"
    for i, (symb, deadline) in enumerate(deadlines):
        if i != len(deadlines) - 1:
            out = f"g+{symb}.<{out}>_[0,{deadline}]"
        else:
            out = f"({symb}.<{out}>_[0,{deadline}])*"
    return quickparse(out, string=True), out


def build_e_dprime3(deadlines, outer_deadline=None):
    # Nicolas 2nd email: bounded version — outer timed bracket caps the whole cycle.
    # Grant alone (no requests) is possible at any level.
    # (<g+r3.<g+r2.<g+r1.<g>_[0,1]>_[0,2]>_[0,3]>_[0,4])*
    # outer_deadline defaults to last deadline + 1 for arithmetic sequences.
    if outer_deadline is None:
        outer_deadline = deadlines[-1][1] + 1
    out = "g"
    for symb, deadline in deadlines:
        out = f"g+{symb}.<{out}>_[0,{deadline}]"
    out = f"(<{out}>_[0,{outer_deadline}])*"
    return quickparse(out, string=True), out

def build_e_dprime4dummy(deadlines, outer_deadline=None):
    # Like dprime3 but with a* prefixes at each level (dummy junk symbol between events).
    # (<a*.g + a*.r3.<a*.g + a*.r2.<a*.g + a*.r1.<g>_[0,1]>_[0,2]>_[0,3]>_[0,4])*
    if outer_deadline is None:
        outer_deadline = deadlines[-1][1] + 1
    out = "g"
    for symb, deadline in deadlines:
        out = f"a*.g + a*.{symb}.<{out}>_[0,{deadline}]"
    out = f"(<{out}>_[0,{outer_deadline}])*"
    return quickparse(out, string=True), out


def build_e_dprime5(deadlines, outer_deadline=None):
    # Mandatory requests at each level; only the innermost grant may be preceded by junk (a*).
    # Requests are NOT optional — no EPS, no union at request sites.
    # (<rk.<...<r2.<r1.<a*.g>_[0,T1]>_[0,T2]>...>_[0,Tk]>_[0,Tk+1])*
    # For DEADLINES_DEMO[:3]: (<r3.<r2.<r1.<a*.g>_[0,1]>_[0,2]>_[0,3]>_[0,4])*
    if outer_deadline is None:
        outer_deadline = deadlines[-1][1] + 1
    out = "a*.g"
    for symb, deadline in deadlines:
        out = f"{symb}.<{out}>_[0,{deadline}]"
    out = f"(<{out}>_[0,{outer_deadline}])*"
    return quickparse(out, string=True), out


# ─── Timing helpers ───────────────────────────────────────────────────────────
#
# slice_volume is decorated with @lru_cache (keyed on the ANTLR node object + n).
# The first call recursively computes and caches volumes for every sub-expression.
# All subsequent slice_volume calls on those same node objects return instantly.
# sample_unambig calls slice_volume internally — so after the first slice_volume(phi, N)
# call, every sample(phi, N) call only pays for the random choices, not recomputation.
#
# t_vol = first slice_volume call  → fills cache
# t_sample = N_samples sample calls → cache is warm, pure sampling cost

def time_one(phi, N, N_samples):
    """Time volume fill and sampling separately. All relevant caches are cleared
    before the volume call so each measurement starts fully cold:
      - slice_volume      lru_cache (ANTLR node → VolumePoly)
      - continuous_convolution  lru_cache (VolumePoly × VolumePoly)
      - sympy cacheit     polynomial arithmetic results
    Instance-level caches (__add__, __mul__, integral, …) are tied to VolumePoly
    objects and become fresh automatically when slice_volume rebuilds them.

    Returns (t_vol, t_sample_per, avg_smart_rej, avg_intersect_rej):
      t_sample_per      — wall time per accepted sample (total / N_samples)
      avg_smart_rej     — avg rejected attempts per sample (ambiguity correction)
      avg_intersect_rej — avg rejected attempts per sample (intersection loop); 0 if not used"""
    slice_volume.cache_clear()
    continuous_convolution.cache_clear()
    clear_sympy_cache()

    t0 = time.perf_counter()
    slice_volume(phi, N)
    t_vol = time.perf_counter() - t0

    total_smart_rej = 0
    total_intersect_rej = 0
    t0 = time.perf_counter()
    for _ in range(N_samples):
        _, fb = sample(phi, N, feedback=True)
        total_smart_rej += fb.smart_rej
        if fb.intersect_rej is not None:
            total_intersect_rej += fb.intersect_rej
    t_sample = time.perf_counter() - t0

    return (
        t_vol,
        t_sample / N_samples,
        total_smart_rej / N_samples,
        total_intersect_rej / N_samples,
    )


def run_timing(builder_fn, k_values, N, N_samples, label=""):
    results = {}
    for k in k_values:
        phi, expr = builder_fn(DEADLINES_DEMO[:k])
        print(f"  k={k}  {expr}")
        t_vol, t_sample_per, avg_smart_rej, avg_intersect_rej = time_one(phi, N, N_samples)
        results[k] = {
            "t_vol": t_vol,
            "t_sample": t_sample_per,
            "avg_smart_rej": avg_smart_rej,
            "avg_intersect_rej": avg_intersect_rej,
            "expr": expr,
        }
        print(f"    t_vol={t_vol:.3f}s  t_sample/call={t_sample_per:.3f}s  "
              f"s_rej={avg_smart_rej:.2f}  i_rej={avg_intersect_rej:.2f}")
    return results


# ─── Plotting ─────────────────────────────────────────────────────────────────

def plot_timing_breakdown(ax, k_values, results, title, x_label_fn=None):
    """Stacked bar: volume | sample | smart_rej (if any) | intersect_rej (if any).
    t_sample_per already includes rejected attempts; we decompose it:
      net_sample  = t_sample / (1 + sr)
      smart_rej   = sr / (1 + sr) * t_sample"""
    x = np.arange(len(k_values))

    has_smart     = any(results[k]["avg_smart_rej"]     > 0.05 for k in k_values)
    has_intersect = any(results[k]["avg_intersect_rej"] > 0.05 for k in k_values)

    t_vols, t_nets, t_srejs, t_irejs = [], [], [], []
    for k in k_values:
        tv  = results[k]["t_vol"]
        ts  = results[k]["t_sample"]
        sr  = results[k]["avg_smart_rej"]
        ir  = results[k]["avg_intersect_rej"]
        t_net  = ts / (1 + sr) if sr > 0 else ts
        t_vols.append(tv)
        t_nets.append(t_net)
        t_srejs.append(ts - t_net)
        t_irejs.append(ir * t_net)

    t_totals  = [tv + tn + tsr + tir
                 for tv, tn, tsr, tir in zip(t_vols, t_nets, t_srejs, t_irejs)]
    max_total = max(t_totals) if t_totals else 1

    bottom = np.zeros(len(k_values))
    ax.bar(x, t_vols, color=COLORS["volume"], label="volume computation (init.)", width=0.6)
    bottom += np.array(t_vols)
    ax.bar(x, t_nets, color=COLORS["sample"], label="time per sample", bottom=bottom, width=0.6)
    bottom += np.array(t_nets)
    if has_smart:
        ax.bar(x, t_srejs, color=COLORS["smart_rej"], label="ambiguity rejection time (per sample)",
               bottom=bottom, width=0.6)
        bottom += np.array(t_srejs)
    if has_intersect:
        ax.bar(x, t_irejs, color=COLORS["intersect_rej"], label="intersection rejection time (per sample)",
               bottom=bottom, width=0.6)

    for i, t in enumerate(t_totals):
        ax.text(i, t + max_total * 0.02, f"{t:.2f}s",
                ha="center", va="bottom", fontsize=7, color="#333")

    ax.set_xticks(x)
    labels = [x_label_fn(k) for k in k_values] if x_label_fn else [f"k={k}" for k in k_values]
    ax.set_xticklabels(labels)
    ax.set_ylim(0, max_total * 1.55)
    ax.set_ylabel("time (s)")
    if title:
        ax.set_title(title, fontsize=8, pad=6)
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    h, lab = ax.get_legend_handles_labels()
    ax.legend(h, lab, loc="upper left", ncol=1, frameon=True,
              handlelength=0.8, fontsize=7, borderpad=0.3, labelspacing=0.2)


# ─── Main ─────────────────────────────────────────────────────────────────────
#
# Experiment: e_{4,k} timing — how sampling cost scales with the number of
# request types k.
#
# Expression structure (arithmetic deadlines T_i = i, outer deadline k+1):
#
#   e_{4,k} = (<nested timed cycle with k request levels>)^*
#
# Two candidate definitions are compared (pick one for the paper):
#
#   MODE 2 — mandatory requests (dprime5):
#     Every cycle must contain all k requests in strict nesting order.
#     The innermost core allows arbitrary junk before the grant (a*.g).
#       (<r_k . <... r_1 . <a*.g>_{<=1} ...>_{<=k}>_{<=k+1})*
#
#   MODE 5 — optional requests, grant at any level (dprime3):
#     At each nesting level the cycle may end with a bare grant, making
#     all intermediate requests optional.
#       (<g + r_k . <... g + r_1 . <g>_{<=1} ...>_{<=k}>_{<=k+1})*
#
# Both are plotted under the name e_{4,k} with their recursive formula
# shown in the title, so you can compare and choose one for the paper.
#
# Parameters: k in {1,...,6},  n = 10 symbols,  10 samples per k,  T_i = i.
# Each stacked bar shows:
#   orange  — volume computation (one-time slice_volume call, cold cache)
#   green   — time per sample (cache warm, pure sampling cost)
#   yellow  — ambiguity rejection time per sample (if any)
#   purple  — intersection rejection time per sample (if any)
#
# Run:    python expressions_12_requests.py   (set MODE = 2, 5, or 6)
# Output: 12_page13_casestudy/results/
#
#  MODE 1 — quick sanity: k=3, n=10, 3 samples; prints timing + words, saves volume PDF
#  MODE 3 — k-scaling for dprime4dummy (slow!): same plot, stops early if budget exceeded
#  MODE 4 — probe: two reps per k + reverse pass to diagnose t_vol behaviour
#  MODE 6 — (n,k) grid sweep: heatmap of per-sample time; set SANITY=True first

if __name__ == "__main__":
    np.random.seed(42)
    random.seed(42)

    MODE = 6   # ← change this

    RESULTS = os.path.join(os.path.dirname(__file__), "12_page13_casestudy", "results")
    os.makedirs(RESULTS, exist_ok=True)

    # ── Mode 1: quick check ───────────────────────────────────────────────────
    if MODE == 1:
        K = 3
        N = 10
        N_SAMPLES = 3

        phi, expr = build_e_dprime5(DEADLINES_DEMO[:K])
        print(f"expr: {expr}")

        t_vol, t_sample_per, avg_smart_rej, avg_intersect_rej = time_one(phi, N, N_SAMPLES)
        print(f"t_vol={t_vol:.3f}s   t_sample/call={t_sample_per:.3f}s ({N_SAMPLES} samples)  "
              f"s_rej={avg_smart_rej:.2f}  i_rej={avg_intersect_rej:.2f}")

        V = slice_volume(phi, N)   # instant — cache already warm from time_one
        out_path = os.path.join(RESULTS, f"expr12_dprime5_volume_k{K}_n{N}.pdf")
        V.plot(no_show=True, plt_title=f"e = {expr},  n = {N}")
        plt.savefig(out_path, bbox_inches="tight")
        plt.close()
        print(f"saved: {out_path}")

        for i in range(N_SAMPLES):
            print(f"  [{i}] {sample(phi, N)}")

    # ── Mode 2: k-scaling, dprime5 ───────────────────────────────────────────
    elif MODE == 2:
        K_VALUES = [1, 2, 3, 4, 5, 6]
        N = 10
        N_SAMPLES = 10

        print(f"=== k-scaling: dprime5  (n={N}, {N_SAMPLES} samples/k) ===")
        results = run_timing(build_e_dprime5, K_VALUES, N, N_SAMPLES)

        title = (
            r"$e_{4,k}=(\langle r_k\cdot\langle\cdots r_1"
            r"\cdot\langle a^*g\rangle_{\leq 1}\cdots\rangle_{\leq k}\rangle_{\leq k{+}1})^*$"
            "\n"
            f"$k$-scaling,  $n={N}$,  $T_i=i$,  {N_SAMPLES} samples per $k$"
        )
        fig, ax = plt.subplots(figsize=(5, 3.5))
        plot_timing_breakdown(ax, K_VALUES, results, title)
        plt.tight_layout(pad=0.8)

        out_path = os.path.join(RESULTS, f"timing_dprime5_k_sweep_n{N}.pdf")
        plt.savefig(out_path, bbox_inches="tight")
        plt.close()
        print(f"\nSaved: {out_path}")

    # ── Mode 3: k-scaling, dprime4dummy (slow — budget guard) ─────────────────
    elif MODE == 3:
        K_VALUES = [1, 2, 3, 4, 5]
        N = 10
        N_SAMPLES = 1
        BUDGET_S = 200   # stop before the next k if previous total exceeded this

        print(f"=== k-scaling: dprime4dummy  (n={N}, {N_SAMPLES} sample/k, budget={BUDGET_S}s) ===")
        results = {}
        for k in K_VALUES:
            phi, expr = build_e_dprime4dummy(DEADLINES_DEMO[:k])
            print(f"  k={k}  {expr}")
            t_vol, t_sample_per, avg_smart_rej, avg_intersect_rej = time_one(phi, N, N_SAMPLES)
            results[k] = {
                "t_vol": t_vol,
                "t_sample": t_sample_per,
                "avg_smart_rej": avg_smart_rej,
                "avg_intersect_rej": avg_intersect_rej,
                "expr": expr,
            }
            print(f"    t_vol={t_vol:.3f}s  t_sample/call={t_sample_per:.3f}s  "
                  f"s_rej={avg_smart_rej:.2f}  i_rej={avg_intersect_rej:.2f}")
            if t_vol + t_sample_per * N_SAMPLES > BUDGET_S:
                print(f"  -> budget exceeded at k={k}, stopping early.")
                break
        done_k = list(results.keys())

        fig, ax = plt.subplots(figsize=(5, 3.5))
        plot_timing_breakdown(ax, done_k, results, "dprime4dummy: a* at each level")
        fig.suptitle(f"dprime4dummy — scaling in k  (n={N}, {N_SAMPLES} sample/k)", fontsize=10)
        plt.tight_layout(pad=0.8)

        out_path = os.path.join(RESULTS, f"timing_dprime4dummy_k_sweep_n{N}.pdf")
        plt.savefig(out_path, bbox_inches="tight")
        plt.close()
        print(f"\nSaved: {out_path}")




    # ── Mode 4: probe why t_vol shrinks with k ────────────────────────────────
    # Two competing hypotheses:
    #   (A) Python warmup — the first slice_volume call in a process is slow
    #       due to module/JIT startup cost, regardless of which k it times.
    #   (B) Expression structure — larger k means more mandatory symbols per
    #       Kleene cycle, so fewer valid partitions of n symbols into cycles,
    #       so the volume sum is cheaper to compute even though the expression is bigger.
    #
    # Test for (A): run each k twice with cache_clear between.
    #   If warmup is the cause, rep2 should be noticeably faster than rep1.
    # Test for (B): run k in reverse order (5→1).
    #   If structure is the cause, k=5 (now first in the loop) should still
    #   be fast and k=1 (now last) should still be slow.
    # Also print total_volume per k — if it decreases with k, that confirms
    # the Kleene partition count shrinks (structural explanation).
    elif MODE == 4:
        N = 10
        N_SAMPLES = 3

        print("=== Probe: forward pass k=1..5, two reps each ===")
        for k in [1, 2, 3, 4, 5]:
            phi, expr = build_e_dprime5(DEADLINES_DEMO[:k])

            t1_vol, t1_sper, t1_sr, _ = time_one(phi, N, N_SAMPLES)
            t2_vol, t2_sper, t2_sr, _ = time_one(phi, N, N_SAMPLES)

            V = slice_volume(phi, N)   # cache warm after time_one
            print(f"  k={k}  total_volume={float(V.total_volume()):.3e}")
            print(f"    rep1: t_vol={t1_vol:.3f}s  t_sample/call={t1_sper:.3f}s  s_rej={t1_sr:.2f}")
            print(f"    rep2: t_vol={t2_vol:.3f}s  t_sample/call={t2_sper:.3f}s  s_rej={t2_sr:.2f}")

        print()
        print("=== Probe: reverse pass k=5..1, single rep each ===")
        for k in [5, 4, 3, 2, 1]:
            phi, expr = build_e_dprime5(DEADLINES_DEMO[:k])
            t_vol, t_sper, avg_sr, _ = time_one(phi, N, N_SAMPLES)
            V = slice_volume(phi, N)
            print(f"  k={k}  t_vol={t_vol:.3f}s  t_sample/call={t_sper:.3f}s  s_rej={avg_sr:.2f}  "
                  f"total_volume={float(V.total_volume()):.3e}")


    # ── Mode 5: k-scaling, dprime3 ───────────────────────────────────────────
    elif MODE == 5:
        K_VALUES  = [1, 2, 3, 4, 5, 6]
        N         = 10
        N_SAMPLES = 10

        print(f"=== k-scaling: dprime3  (n={N}, {N_SAMPLES} samples/k) ===")
        results = run_timing(build_e_dprime3, K_VALUES, N, N_SAMPLES)

        title = (
            r"$e_{4,k}=(\langle g+r_k\cdot\langle\cdots g+r_1"
            r"\cdot\langle g\rangle_{\leq 1}\cdots\rangle_{\leq k}\rangle_{\leq k{+}1})^*$"
            "\n"
            f"$k$-scaling,  $n={N}$,  $T_i=i$,  {N_SAMPLES} samples per $k$"
        )
        fig, ax = plt.subplots(figsize=(5, 3.5))
        plot_timing_breakdown(ax, K_VALUES, results, title)
        plt.tight_layout(pad=0.8)

        out_path = os.path.join(RESULTS, f"timing_dprime3_k_sweep_n{N}.pdf")
        plt.savefig(out_path, bbox_inches="tight")
        plt.close()
        print(f"\nSaved: {out_path}")
    # ── Mode 6: (n,k) grid sweep — VolTRE timing heatmap ─────────────────────
    #
    # Outputs (12_page13_casestudy/results/):
    #   nk_grid_voltre.csv          — n, k, init_time, per_sample_time, status
    #   nk_grid_heatmap_voltre.pdf  — per-sample-time heatmap; T.O. cells grey
    #
    # TA comparison: place a CSV with columns (n, k, per_sample_time, status) at
    #   12_page13_casestudy/results/nk_grid_ta.csv
    # and re-run to get side-by-side panels.
    #
    # Set SANITY = True (default) for a quick 3×3 corner check first.
    elif MODE == 6:
        import signal
        import csv
        import matplotlib.colors as mcolors

        # ── Tunable parameters ───────────────────────────────────────────────
        SANITY           = False   # ← set False for full grid
        SAMPLE_TIMEOUT_S = 200    # ← per-sample (and per-init) wall-clock limit (s)
        N_SAMPLES        = 10     # ← samples averaged per cell

        # Grid ranges — shrink if numbers get excessive
        N_GRID = list(range(1, 4  if SANITY else 11))   # word lengths
        K_GRID = list(range(1, 4  if SANITY else 11))   # request-type counts
        # ─────────────────────────────────────────────────────────────────────

        FIG_W  = 5.787   # matches plot_config fig_width_in

        class _Timeout(Exception):
            pass

        def _alarm(signum, frame):
            raise _Timeout()

        def fmt_t(t):
            if t is None:
                return "   —  "
            if t < 0.01:
                return f"{t:.4f}s"
            if t < 10:
                return f"{t:.3f}s"
            return f"{t:.1f}s"

        def cell_label(t):
            if t is None:
                return "T.O."
            if t < 0.01:
                return f"{t:.3f}"
            if t < 10:
                return f"{t:.2f}"
            return f"{t:.0f}s"

        def time_cell(phi, n):
            signal.signal(signal.SIGALRM, _alarm)
            # ── init: volume computation ──────────────────────────────────
            signal.alarm(int(SAMPLE_TIMEOUT_S))
            try:
                slice_volume.cache_clear()
                continuous_convolution.cache_clear()
                clear_sympy_cache()
                t0 = time.perf_counter()
                slice_volume(phi, n)
                t_vol = time.perf_counter() - t0
            except _Timeout:
                return None, None, "timeout:init"
            except Exception as e:
                return None, None, f"error:init:{type(e).__name__}"
            finally:
                signal.alarm(0)
            # ── sampling: one timeout per sample() call ───────────────────
            t_acc = 0.0
            for _ in range(N_SAMPLES):
                signal.alarm(int(SAMPLE_TIMEOUT_S))
                try:
                    t0 = time.perf_counter()
                    sample(phi, n)
                    t_acc += time.perf_counter() - t0
                except _Timeout:
                    return t_vol, None, "timeout:sample"
                except Exception as e:
                    return t_vol, None, f"error:sample:{type(e).__name__}"
                finally:
                    signal.alarm(0)
            return t_vol, t_acc / N_SAMPLES, "ok"

        tag = "SANITY (3x3)" if SANITY else f"FULL ({len(N_GRID)}x{len(K_GRID)})"
        print(f"=== MODE 6 — (n,k) grid  [{tag}] ===")
        print(f"    n={N_GRID}  k={K_GRID}  "
              f"{N_SAMPLES} samples/cell  timeout={SAMPLE_TIMEOUT_S}s/operation")
        print(f"    expression: e_{{4,k}} = build_e_dprime3\n")

        rows = []
        for k in K_GRID:
            phi, expr = build_e_dprime3(DEADLINES_DEMO[:k])
            short = expr if len(expr) <= 72 else expr[:69] + "..."
            print(f"k={k}  {short}")
            for n in N_GRID:
                t_vol, t_sper, status = time_cell(phi, n)
                rows.append({
                    "n": n, "k": k,
                    "init_time":       f"{t_vol:.6f}"  if t_vol  is not None else "",
                    "per_sample_time": f"{t_sper:.6f}" if t_sper is not None else "",
                    "status": status,
                })
                print(f"  n={n:2d}  init={fmt_t(t_vol)}  sample={fmt_t(t_sper)}  [{status}]")
            print()

        prefix = "sanity" if SANITY else "nk_grid"
        out_csv = os.path.join(RESULTS, f"{prefix}_voltre.csv")
        with open(out_csv, "w", newline="") as f:
            w = csv.DictWriter(
                f, fieldnames=["n", "k", "init_time", "per_sample_time", "status"])
            w.writeheader()
            w.writerows(rows)
        print(f"CSV: {out_csv}")

        # ── heatmap ──────────────────────────────────────────────────────────
        mat_sper = np.full((len(K_GRID), len(N_GRID)), np.nan)
        mat_vol  = np.full((len(K_GRID), len(N_GRID)), np.nan)
        for r in rows:
            ni = int(r["n"]) - N_GRID[0]
            ki = int(r["k"]) - K_GRID[0]
            if r["status"] == "ok":
                mat_sper[ki, ni] = float(r["per_sample_time"])
                mat_vol[ki, ni]  = float(r["init_time"])

        cmap = plt.cm.YlOrRd.copy()
        cmap.set_bad("#555555")

        valid = mat_sper[~np.isnan(mat_sper)]
        if len(valid) > 1 and valid.max() > valid.min() * 10:
            norm = mcolors.LogNorm(
                vmin=max(valid.min(), 1e-5), vmax=valid.max())
        else:
            norm = mcolors.Normalize(
                vmin=valid.min() if len(valid) else 0,
                vmax=valid.max() if len(valid) else 1)

        fig, axes = plt.subplots(1, 2, figsize=(FIG_W, FIG_W * 0.52))

        for ax, mat, col_label, subplot_title in [
            (axes[0], mat_vol,  "init time (s)",       "volume init"),
            (axes[1], mat_sper, "per-sample time (s)", "per-sample"),
        ]:
            valid_m = mat[~np.isnan(mat)]
            if len(valid_m) > 1 and valid_m.max() > valid_m.min() * 10:
                n_m = mcolors.LogNorm(
                    vmin=max(valid_m.min(), 1e-5), vmax=valid_m.max())
            else:
                n_m = mcolors.Normalize(
                    vmin=valid_m.min() if len(valid_m) else 0,
                    vmax=valid_m.max() if len(valid_m) else 1)

            im = ax.imshow(mat, aspect="auto", norm=n_m,
                           cmap=cmap, origin="lower")
            plt.colorbar(im, ax=ax, label=col_label,
                         fraction=0.046, pad=0.04)

            for ki in range(len(K_GRID)):
                for ni in range(len(N_GRID)):
                    val = mat[ki, ni]
                    lbl = cell_label(val) if not np.isnan(val) else "T.O."
                    fc  = "white" if np.isnan(val) else "black"
                    ax.text(ni, ki, lbl, ha="center", va="center",
                            fontsize=5, color=fc)

            ax.set_xticks(range(len(N_GRID)))
            ax.set_xticklabels(N_GRID, fontsize=6)
            ax.set_yticks(range(len(K_GRID)))
            ax.set_yticklabels(K_GRID, fontsize=6)
            ax.set_xlabel("$n$", fontsize=7)
            ax.set_ylabel("$k$", fontsize=7)
            ax.set_title(
                f"$e_{{4,k}}$ — VolTRE {subplot_title}", fontsize=7, pad=4)

        plt.tight_layout(pad=0.6)
        out_fig = os.path.join(RESULTS, f"{prefix}_heatmap_voltre.pdf")
        plt.savefig(out_fig, bbox_inches="tight")
        plt.close()
        print(f"Heatmap: {out_fig}")
        if SANITY:
            print("\n[Sanity passed? Set SANITY=False and re-run for full 10x10 grid.]")
