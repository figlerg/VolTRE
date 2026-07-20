# Method notes (paper: "Uniform Sampling for Timed Regular Expressions", accepted at EMSOFT 2026)

> Status: generated 2026-07-20 from paper_source. **Skimmed by Felix: "it's fine as an overview"**.

## Problem
Uniformly sample timed words from a timed regular language given as a TRE, with **exact** prescribed length `n` (number of events) and duration `T` ("slice sampling"), and with that also sampling with free duration (two modes supported). Prior work (wordgen line: QEST16 [BarbotBBK16], [BarbotB23]) only handled *deterministic* TA and could fix only length + *expected* duration. Contributions:
1. First uniform sampler directly on TREs.
2. First *exact-duration* (slice) uniform sampling.
3. A hierarchy of algorithms covering increasingly general classes, up to the full class of timed regular languages = languages of non-deterministic TA (via GTRE with intersection + renaming), see Fig. `fig:potatoes`.

## Core objects
- Timed word `w = t1 a1 t2 a2 ... tn an`; duration θ(w) = Σ ti. A slice `L_{n,T}` = words of length n and duration T, viewed as subsets of R^n (delay vectors) → has a volume.
- **Slice-volume function** `V_n^e(T)`: volume of the n-T-slice as a function of T.
- **Multiset semantics** `M(e)`: counts each timed word with its *multiplicity* N_e(w) = number of distinct parse/derivations of w by e. For unambiguous e, multiset and language semantics coincide. `V_n^{M(e)}` is the multiset volume (computable inductively even when the true language volume isn't).
- **RITRE**: every timed regular language is `rf(∩_k e_k)` — a renaming applied to an intersection of plain TREs (timed Kleene theorem, Asarin-Caspi-Maler).

## Key theorems
- **Thm inductivedef** (inductive characterisation of V_n^{M(e)}): ε and star-at-0 give Dirac(T); atom: V_1 = 1; timed restriction ⟨e⟩_I multiplies by indicator 1_I(T); union = sum; concatenation = Σ_k over length splits of the *convolution* V_k^{M(e1)} * V_{n-k}^{M(e2)}; star via e* ≡ ε + e·e*.
- **Thm polynomials**: V_n^{M(e)}(T) is piecewise polynomial: Σ_I p_I(T)·1_I(T), degree ≤ n−1, interval bounds are integers ≤ n·B(e) (B = max upper bound of timed restrictions) or ∞; ≤ 2nB+2 pieces. Computable in **polynomial time** in n, B(e), |e|. (Appendix lemma: convolution of one-piece polys gives ≤ 3 pieces; Fig `fig:integrals`.)
- **Thm slicesampling**: Alg 1 samples with PDF ∝ multiplicity N_e(w)/V_n^{M(e)}(T). Unambiguous ⇒ this is already uniform. Ambiguous ⇒ Alg 2 is uniform; expected #trials = expected multiplicity V^{M}/V^{lang} (matches empirics, Fig `fig:sharkfin`). Side effect: acceptance rate estimates the true language volume of ambiguous expressions.
- **Thm durationsampling**: for any probability measure depending only on duration with duration-PDF p(T): sample T ~ p (inverse transform), then slice-sample. Enables max-entropy distributions with moment constraints (mean/variance) from [BarbotB23], now actually samplable because V_n(T) is in closed form: p_λ(T) ∝ e^{λ1 T + ... + λm T^m} V_n(T), λ tuned by numerical root-finding. (Fig `fig:maxent-triangle`; code: volume/tuning.py, MaxEntDist.)

## Algorithms (paper ↔ code)
- **Alg 1 `recsample(e,n,T)`** — recursive method lifted to timed setting. Atom → return (T,a); timed restriction → recurse; union → pick branch w.p. proportional to slice volumes; concat/star → sample discrete cut i_cut weighted by convolutions, then continuous cut T_cut from PDF ∝ V_i^{e1}(T')·V_{n-i}^{e2}(T−T'), recurse on both parts. Star treated as e0·e0* with i_min=1 (avoids infinite recursion); n=0 → ε. Code: `sample/sample.py` + `volume/slice_volume.py`.
- **Alg 2 `unifsample(e,n,T)`** — disambiguation rejection: loop { w ← recsample; m ← N_e(w) (computed by `match/match.py`); accept w.p. 1/m }. Uniform on the language for any TRE (no ∩/renaming).
- **Alg `multi` (S_m)** + **Alg 3 General Sampler** — for RITRE rf(∩ e_k): sample w' from e_1 with Alg 1, check membership in the other e_k (`match/intersection_match.py`), apply renaming rf, compute total multiplicity S_m(w) = Σ over preimages in rf^{-1}(w) ∩ ∩ sem(e_k) of N_{e1} (Prop qmst, inductive preimage computation), accept w.p. 1/S_m. Expected cost scales with inverse acceptance ratio (thin intersections are expensive; sampling in an intersection is harder than emptiness, which is PSPACE-hard).

## Why TRE instead of TA
- DTA volume computation is exponential in the number of clocks (split-form blowup in wordgen); nested timed restrictions `e_k` (request-grant family, Eq. eq:ek) need k+1 clocks in a DTA but are polynomial for VolTRE (Fig `fig:exp16`).
- Some unambiguous TREs have no deterministic TA at all (Ex disambiguate: e2 = a*·⟨a*⟩_[1,2], unambiguous equivalent e2' = ⟨a*⟩_[1,2] + a*·⟨a·⟨a*⟩_[1,2]⟩_[2,∞]).

## Applications section (Sec. "Applications and experiments")
1. **Scalability stress test** (Fig `fig:stress`): e1 hypercube (unambiguous, no rejection), e2 ambiguous (per-sample cost grows), e3 intersection (cost explodes near feasibility boundary T→2). One-time volume cost vs per-sample cost decomposition.
2. **Disambiguation trials** (Fig `fig:sharkfin`): empirical vs theoretical expected multiplicity for e2, n=10.
3. **TA-vs-TRE k-sweep** (Fig `fig:exp16`): VolTRE vs wordgen on e_k family, n=10, k=1..8; wordgen OOM at k=7, 3600s budget.
4. **Prescribed duration distribution / max entropy** (Fig `fig:maxent-triangle`): ⟨aa⟩_≤1, n=2, mean 2/3, three variances.
5. **Specification refinement measurement** (Figs `fig:falsifies`, `fig:volumeDeltaSigma`): expressions eA ⊇ eB ⊇ eC over peaks a (width [1,2]) and b (width [3,4]); volume ratios quantify refinement; inclusion-based rejection sampling efficiency.
6. **ΣΔ modulator case study**: 100 timed words (n=10, T=27) from eA/eB/eC turned into peak signals, fed to a Simulink second-order ΣΔ model [Brigati99]; saturation (|quantizer out| > 2) found for eA, eB but not eC at scaling factors μ ∈ [5, 5.745]e-8. Requires MATLAB/Simulink — not reproducible in a pure-Python artifact.

## Notation glossary (defs.tex)
`⟨e⟩_I` timed restriction; `V_n^e(T)` = slice volume (`\vslice`), `\vslicem` = multiset version; N_e(w) multiplicity; B(e)=`\maxbound` max interval bound; GTRE = TRE + intersection + renaming; RITRE = renaming of intersection of TREs.
