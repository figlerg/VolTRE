# Cognitive Handoff Document — VolTRE EMSOFT Round 2 Experiments

## 1. Core Goal & Tech Stack

**Goal:** Add experimental results to a paper on uniform sampling for Timed Regular
Expressions (TREs) for EMSOFT 2026 Round 2 revision (deadline June 19 AoE).
The paper introduces VolTRE, a tool for slice-uniform sampling of timed words.

**Tech stack:** VolTRE — an existing local Python/OCaml tool (already set up, slightly
dirty state from recent vibe coding, do not push anything without Felix reviewing first).

---

## 2. Current Progress & Key Decisions

**Decided experiments (in priority order):**

1. **Dejan's stress test** — pick expressions from the paper, vary (n, T) on a grid,
   measure wall-clock sampling time, plot as curves. Use at least:
   - `e_ex1 = (<a>_≤1)*`  — clean baseline, no intersection, unambiguous
   - `e_exb = <b>*_[3,4] · (<a>_[1,2] · <b>_[3,4] · <b>*_[3,4])*`  — realistic, constrained
   - optionally one with intersection to stress the rejection path
   Fix n, vary T (unconstrained/random T mode) for the main curve.

2. **Nicolas's rejection rate experiment** — implement parametric request/grant for
   k = 5, 10, 15. Measure total rejections broken into two components:
   - intersection-based rejections
   - ambiguity-based rejections
   Output: bar chart showing totals and fractions per k.
   Prerequisite: Felix needs to read and understand eqs. 20–23 from p.13 draft first.

3. **Train example** — blocked, waiting on Benoit to check if the TRE translation
   is feasible (may require too many intersections).

**Expressions available in the paper** (for reference):
- `e_ex1 = (<a>_≤1)*`
- `e_ex2 = a* · <aa>_≤1 · a*`  (ambiguous)
- `e_ex3 = (<aa>_≤1 · a) ∩ (a · <aa>_≤1)`  (intersection)
- `e_ex4 = [a←a'](a* <a*a'>_[1,2] a* ∩ a* <a'a*>_[1,2] a*)`  (intersection + renaming)
- `e_exa`, `e_exb`, `e_exc`  — Sigma-Delta case study expressions

---

## 3. Exact Next Actionable Step

**Do this first:**

Run Dejan's stress test on `e_ex1` and `e_exb`.
- Fix n ∈ {5, 10, 15, 20}, sample T uniformly from the support of positive volume
- For each (n, T) pair, draw 10 samples and record wall-clock time
- Plot: x-axis = n or T, y-axis = sampling time, one curve per expression
- Save figures to a results folder, do not commit yet

---

## 4. Constraints & Rules

- **Do not push to the VolTRE repo** without Felix explicitly reviewing the diff first.
  The codebase is in a dirty state from recent uncommitted vibe-coded changes.
- **Do not modify the core sampling algorithms** — experiments only, add scripts
  in a separate experiments/ folder or equivalent.
- Figures should be self-contained and reproducible from a script (no notebook
  one-offs that can't be rerun).
- Keep experiment scripts simple and readable — Felix needs to be able to oversee
  and explain them to coauthors.
- The paper has a **2-page budget** (currently 12 pages, max 14). Experiments need
  to earn their space — figures over prose where possible.
- Rejection rate experiment has **two distinct rejection sources** (intersection vs.
  ambiguity) — do not conflate them in the implementation even if the paper
  discusses them together later.