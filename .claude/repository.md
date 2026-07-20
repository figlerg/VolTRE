# Repository notes (VolTRE)

> Status: generated 2026-07-20; **reviewed by Felix 2026-07-20** (corrections incorporated below).

## What the tool is
VolTRE: volume computation and uniform slice sampling for Timed Regular Expressions (TRE). Given a `.tre` file, a length `n` and optionally a duration `T`, it computes the piecewise-polynomial slice-volume function V_n(T) and samples timed words uniformly from the slice.

## Entry points
- `main.py` — CLI. Flags: `-p/--path` (.tre file), `-n/--length`, `-T/--duration`, `--mode {vanilla,max_entropy}`, `--budget` (rejection budget, default 500), `--nr_samples`, `--verbose` (also enables cProfile -> main.prof), `--seed`, `-v/--visualize`, `--total_volume`.
- `minimal_example.py` — programmatic smoke test (parse spec_00.tre, volume plot, slice samples).
- `tutorial.ipynb` — longer programmatic tutorial.

## Package layout
- `parse/` — ANTLR4 grammar `TRE.g4` + generated `TRELexer.py`/`TREParser.py`; `quickparse.py` (parse file or string, `string=True` kwarg); `SyntaxError.py` (hard-error strategy).
  - Grammar: `EPS`, identifiers, `( )`, `*`, `.` concat, `+` union (also postfix `+`), `&` intersection, `<e>_[a,b]` timed restriction (INF/oo/inf), `{a:b,...}e` renaming, `#` comments. Interval bounds are INTs.
- `volume/` — `slice_volume.py` (recursive V_n computation over the syntax tree, `@lru_cache`), `VolumePoly.py` (piecewise polynomial: intervals + sympy polys; `plot()`, `fancy_print()`, `total_volume()`, convolution), `FreePiecewise.py`, `MaxEntDist.py` + `tuning.py` (max-entropy lambda tuning, `parameterize_mean_variance`).
- `sample/` — `sample.py` (recursive sampler = Alg 1; disambiguation rejection = Alg 2; intersection/renaming handling = Alg 3; `DurationSamplerMode.{VANILLA,MAX_ENT}`; `Feedback` namedtuple with rejection counts), `TimedWord.py`.
- `match/` — `match.py` (multiplicity count N(w, phi), used for rejection correction), `intersection_match.py`.
- `misc/` — `disambiguate.py` (renaming trick: index each symbol occurrence), `rename.py`, `first.py`, `has_eps.py`, `is_det.py`, `helpers.py` (`BudgetExhaustedException`), `cached_getText.py`, `recursion_template.py`, `visualize_recursion.py`, `exceptions.py`.
- `probabilistic/` — `subset.py` (statistical language-inclusion test with confidence interval), `volume_estimate.py`.
- `tests/` — pytest suite: parse, volume, match, sampling (vanilla/ambig/maxent), disambiguate, TAkiller, lambda tuning, load-TA-samples.

## Experiments
- `experiments/` root: many `spec_*.tre` files, misc scripts, `thesis_experiments/` (MSc thesis-era).
- `experiments/paper_experiments/` — numbered experiments; `plot_config.py` shared plot styling:
  - `01_hypercube.py` … `08s_delta_sigma_nicolas.py`: flat scripts (hypercube, subset, volume estimation, TAkiller, thicktwin, TRE/TA comparison, delta-sigma volumes). 08-series produces the `08*_n_10.pdf` volume plots used in the paper.
  - `09_ta_case_study/` (notebook, prism TAs), `10_mqtt_fuzzing/` (MQTT broker fuzzing — NOT in final paper), `11_stress_test/` (scalability, notebook + `make_combined_plot.py`), `12_page13_casestudy/` (notebooks, request-grant), `13_nicolas_ambiguity/theorem4.py` (empirical vs theoretical trial counts; sharkfin-style figure), `14_nicolas_samples.py`, `15_moment_control_qest23_redo/exp15_maxent_triangle.py` (max-entropy triangle), `16_ta_vs_tre_2/exp16_ksweep.py` (VolTRE vs wordgen k-sweep; **requires gitignored wordgen/**).
- Paper figure PDFs are copied into `paper_source/fig/`.

## Packaging / environment issues found (relevant to artifact)
- `requirements.txt` was UTF-16 encoded — **converted to UTF-8/LF on 2026-07-20** (pip dry-run OK). Pinned versions incl. antlr4-python3-runtime==4.13.1, sympy==1.12, numpy==1.26.4, matplotlib==3.8.4, scipy, pandas, tqdm, pytest.
- `setup.py` lists only `packages=['misc', 'match']` — missing `parse`, `sample`, `volume`, `probabilistic`. Editable install from repo root masks this; a real (non-editable) install would be broken.
- Version `v0.0.0`, license BSD 3-Clause (LICENSE file at root).
- Python 3.12 per CLAUDE.md; code uses `match`/`case` so needs >= 3.10.

## Paper source
- `paper_source/main.tex` (IEEEtran) inputs: `defs`, `untimed`, `preliminaries`, `TREmain`, `new_inclusion`, `deltasigma`, `appendix`. `comparisonTRETA`, `TAmain`, `samplinggeneral`, `new_ex_req_and_grant`, `factorisation-tree` are commented out (cut from final version).
- Accepted paper PDF: `paper_source/Unif_Sampling_for_Tre_EMSOFT(61).pdf` (canonical, per Felix 2026-07-20; the older (31)/(37) copies in experiments/paper_experiments were deleted). NOTE: the **entire `paper_source/` dir is gitignored** (.gitignore:175) — it exists only on disk, has no git history, and won't be in any branch/archive cut from git. Camera-ready cleanup of main.tex (Anonymous author, revdiff markup) is deferred — not needed for the artifact deadline.
- NOTE: `experiments/paper_experiments/Unif_Sampling_for_Tre_EMSOFT/` is an untracked *directory* duplicating the paper source tree (Overleaf export?) — candidate for cleanup, not touched.

## wordgen
- Local install in gitignored `wordgen/`. Comparison baseline for exp 16 only. Never assume present; artifact docs must list it as optional prerequisite with install pointer.
