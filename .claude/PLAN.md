# PLAN — EMSOFT 2026 artifact

Last updated: 2026-07-21 (evaluation loop built and verified in fast mode).

## ▶ NEXT SESSION — start here
1. **Felix: run `docker build -t voltre-artifact .`** (repo root, WSL). Dockerfile is written but unverified (no docker in sandbox). Then run inside the container: `./artifact/smoke_test.sh` and `./artifact/reproduce.sh`. Report errors back.
2. **Full-mode verification**: `./reproduce.sh stress --full` (~1 h) and `./reproduce.sh ksweep --full` (hours) have only been smoke-tested with tiny budgets, never run at full budget. Run at least once, ideally in the container.
3. Artifact doc files (README/REQUIREMENTS/STATUS/INSTALL), section C below.
4. Still open: tutorial.ipynb unverified; Felix to run `rm -rf "/workspace/experiments/paper_experiments/Unif_Sampling_for_Tre_EMSOFT"` (root-owned); commit of 2026-07-21 work pending Felix's confirmation.

## ⚠ Deadline
**Artifact submission deadline 24 July (AoE)** — confirmed by Felix 2026-07-20 ("tight"). Decision notification 24 August.

## Badges to apply for — DECIDED (Felix 2026-07-20)
- Apply for **all three: Available + Reviewed + Reproducible**. Experiments were written with reproducibility in mind; a Docker image reproducing all figures is deemed doable before the deadline. The eval loop is therefore mandatory, not optional.
- ΣΔ case study needs MATLAB/Simulink → those figures are "data provided, not re-runnable"; state this clearly in STATUS/submission form.

## Artifact TODO list

### A. Packaging & install (blockers found 2026-07-20)
- [x] Fix `requirements.txt` encoding: converted UTF-16→UTF-8/LF (2026-07-20, pip dry-run OK). Pins verified in a fresh py3.12 venv 2026-07-20 (full install + run). Docker build will be the final cross-machine check.
- [x] Fix `setup.py` (2026-07-20): root cause was missing `__init__.py` in `parse`, `sample`, `volume`, `probabilistic` (only `match`/`misc` had one, so only those were listed). Added 4 empty `__init__.py`, switched to `find_packages(include=[...])`, version `v0.0.0`→`0.1.0`. Verified: non-editable install in fresh venv, import + slice_volume + sample from outside repo root OK.
- [x] README updated (2026-07-20): venv name → `.venv`, paper title corrected to "Uniform Sampling for Timed Regular Expressions" (EMSOFT 2026).
- [x] Verify README install steps on Windows: done 2026-07-20 by Felix (fresh clone from GitHub, py -3.12 venv, requirements install, non-editable `pip install .`, CLI sampling example all OK). Caveat: plain `py` picked Python 3.14 and failed (see version-constraint item). Still: [ ] Linux path (covered by Docker build).
- [~] Document Python version constraint **3.10–3.12** everywhere: >=3.10 for match/case, <=3.12 because pinned numpy 1.26.4/matplotlib 3.8.4 have no wheels for 3.13+ (found 2026-07-20: Felix's Windows py launcher used a newer Python → pip tried to build numpy from source). README done 2026-07-20. Still: REQUIREMENTS + INSTALL when created; Dockerfile must pin python:3.12.
- [x] Verify README CLI examples + `minimal_example.py`: done on Windows fresh clone 2026-07-20 (sampling example + minimal_example OK, plot shown). Still: [ ] `tutorial.ipynb` unverified.
- [x] Run pytest suite in fresh env (2026-07-20): after fixes, **162 passed, 0 failed, ~86 s** in a fresh non-editable py3.12 venv, run from repo root. Fixed pre-existing suite bugs: (1) cwd-dependent `../experiments` paths in test_sample_maxent/test_lambda_tuning → `__file__`-anchored; (2) test_parse expected old `ParseCancellationException`, now `TREParseError`; (3) test_load_ta_samples pointed at renamed `ta_sample_1.txt` → `ta_sample_old.txt`; (4) added `tests/__init__.py` (suite previously only collected under editable install). Expected-state note for INSTALL: 162 passed, warnings are harmless (TODO warnings + experimental intersection match).
- [ ] Build **Docker image** (required by guidelines for non-trivial tools) containing artifact + all deps; artifact must run end-to-end inside it.
- [ ] Optional: PyPI publication (nice-to-have, not required).

### B. Evaluation loop (definition of done)
- [x] Per-figure runners built 2026-07-21 under `artifact/figures/` (common.py, volume_delta_sigma.py, maxent_triangle.py, sharkfin.py, stress.py, ksweep_ta_vs_tre.py). Entry point `artifact/reproduce.sh [figure ...] [--full]`. Fast mode (default): regenerate plots from committed CSVs, full loop 3m12s, all 5 figures verified visually against the paper (stress even byte-identical data; sharkfin CSVs turned out to BE the paper's data). Full mode (`--full`): recompute measurements with seed 42; CSVs/PDFs go to artifact/output/, repo stays clean. Env plumbing added to the 4 experiment scripts (VOLTRE_RESAMPLE, VOLTRE_OUT_DIR, VOLTRE_RESULTS_DIR, WORDGEN_BIN).
- [x] Smoke test `artifact/smoke_test.sh` (~30 s: parse + volume + 3 samples + wordgen presence check).
- [ ] Full-mode runs at real budgets never executed end to end (only tiny-budget smoke tests). stress full ~1 h, ksweep full up to several hours.
- [ ] Docker run of the loop (blocked on Felix building the image).
- Note: figure runners fall back to mathtext when LaTeX is absent (fonts differ, content identical); Docker image installs texlive for paper-identical fonts.

### C. Documentation files (required by guidelines)
- [ ] README — what the artifact does, usage, how to reproduce each paper figure.
- [ ] REQUIREMENTS — hardware/software env, Docker, requirements.txt with versions.
- [ ] STATUS — badges applied for + justification.
- [x] LICENSE — BSD 3-Clause already at repo root (verify it's the intended license).
- [ ] INSTALL — install steps + basic usage example + expected output check.
- [ ] Accepted paper PDF included in artifact: canonical is `paper_source/Unif_Sampling_for_Tre_EMSOFT(61).pdf` (per Felix; the (31)/(37) copies were deleted 2026-07-20). PDF is gitignored — remember to add it explicitly to the artifact archive.

### D. wordgen (exp 16 comparison)
- [x] License checked 2026-07-21: GPLv3 — redistribution of source + binary in our image is fine (we ship the full source tarball, satisfying GPL source provision).
- [x] Local wordgen matches upstream commit 5502f65b (git.lacl.fr/barbot/wordgen.git, 2026-03-26) exactly (only CRLF noise). Source tarball vendored at `artifact/wordgen-src-5502f65.tar.gz` (4.4 MB, via git archive).
- [x] Clean build proven 2026-07-21 from pristine source: only deps dune + xml-light 2.5 + zarith 1.14 + ppx_deriving 6.1.1 (opam, OCaml 5.3), builds `src/wordgen.exe` in ~2 s, runtime dep only libgmp. Recipe encoded in Dockerfile stage 1.
- [ ] Docker build of stage 1 unverified (no docker in sandbox).
- fig:exp16 fast mode does NOT need wordgen (committed CSVs); only `ksweep --full` does.

### E. Archival & submission
- [ ] Cut artifact branch from `experimental` (frozen after submission). NOTE: do not push/cut without Felix's explicit go-ahead.
- [ ] Zenodo (or similar) deposit with **version-pinned DOI** (not "always latest").
- [ ] Vet on a clean machine before submission.
- [ ] HotCRP submission: DOI link, required skills/environment statement, paper PDF, badge selection.

## Replicable figures in the FINAL paper (main.tex as compiled)

| # | Label | File(s) in fig/ | Source | Reproducible? |
|---|-------|-----------------|--------|---------------|
| 1 | fig:potatoes | (TikZ) | — | N/A (diagram) |
| 2 | fig:cube | cubecrop3.png, outprojsquare.png + TikZ V_3 plot | gnuplot script embedded as comment in main.tex; sample data provenance unclear (01_hypercube.py samples the same language) | ⚠ partially — needs provenance check |
| 3 | fig:stress | 11_stress_ex123_3.pdf | 11_stress_test/ (notebook + make_combined_plot.py, results/ CSVs) | Yes |
| 4 | fig:sharkfin | sharkfin.pdf | 13_nicolas_ambiguity/theorem4.py (produces theorem4_ambiguity.pdf; differs byte-wise from sharkfin.pdf; paper says 50 samples/T, script has NR_SAMPLES=200). Felix authored it; an older version may have been picked for the paper. TODO: recover the exact settings (check git history of theorem4.py; Felix may dig through emails) and use those in the artifact | ⚠ settings recovery pending |
| 5 | fig:takill | (TikZ DTA) | — | N/A (diagram) |
| 6 | fig:exp16 | exp16_ksweep_v8_k8.pdf | 16_ta_vs_tre_2/exp16_ksweep.py | Yes, but needs wordgen (see D) |
| 7 | fig:maxent-triangle | exp15_maxent_triangle_variance_3_cropped.pdf | 15_moment_control_qest23_redo/exp15_maxent_triangle.py (+ cropping step?) | Yes |
| 8 | fig:falsifies | 8new_/8bnew_/8cnew_*.jpg | Simulink ΣΔ model simulation | No (MATLAB/Simulink) — ship data/images |
| 9 | fig:volumeDeltaSigma | 08c_, 08b_, 08_delta_sigma_*_n_10.pdf | 08s_delta_sigma_nicolas.py (+ variants for 08b/08c — confirm one script makes all three) | Yes |
| 10 | fig:integrals (appendix) | (TikZ) | — | N/A (diagram) |

### Figures/sections in paper_source that did NOT make the final version (do not target)
- `comparisonTRETA.tex` (fig/06_TRE_TA_comp.pdf) — `\input` commented out in main.tex.
- `fig/exp16_ksweep_v7_k7.pdf` — superseded by v8_k8 (commented `\includegraphics`).
- `fig/DSfig.pdf` (ΣΔ model overview) — commented in deltasigma.tex.
- Duplicated falsifies/volume figures in deltasigma.tex — inside `\ignore{}`; live copies are in new_inclusion.tex.
- `TAmain.tex`, `samplinggeneral.tex`, `new_ex_req_and_grant.tex`, `factorisation-tree.tex`, `4nextSubmission.tex`, `new_proof_draft.tex` — not input in final main.tex.
- Experiments 09 (TA case study), 10 (MQTT fuzzing), 12 (page13 case study), 14 (Nicolas samples) — no corresponding figure in final paper.

## Hardware/software statement (for HotCRP form)
Pure Python on CPU, no GPU or special hardware. Dev reference machine: Dell Latitude, i7-1265U, 32 GB RAM (WSL Ubuntu). Docker image should be built **multi-arch (linux/amd64 + linux/arm64)** via buildx so it runs natively on Apple Silicon MacBooks too; otherwise document Rosetta/QEMU emulation.

## Progress log
- 2026-07-20: Initial repo/method/plan notes created (read-only pass). Found packaging blockers (UTF-16 requirements.txt, incomplete setup.py packages). Figure inventory extracted from final main.tex.
- 2026-07-20 (later): Felix reviewed repository.md/method.md (fine, with corrections). Deadline 24 July confirmed. Decisions: wordgen-in-Docker is the target; canonical paper PDF = paper_source/Unif_Sampling_for_Tre_EMSOFT(61).pdf (old copies deleted); camera-ready cleanup deferred. Done: requirements.txt → UTF-8; README venv → .venv + title fixed.
- 2026-07-20 (commit c3bd3ff, amended to 437eb89): committed artifact-prep changes (README, requirements.txt, CLAUDE.md, .claude notes/settings, .gitignore). The previously-unclear .gitignore modification turned out to be Felix's own `paper_source` ignore line — resolved, included. Decision: old Co-Authored-By trailers on already-pushed commits stay (no force-push of experimental); no such trailers going forward.
- 2026-07-20 (commits 4f01c38, a200734): setup.py/packaging fixed and test suite fixed, both verified end-to-end on Linux (fresh venv) AND on Felix's Windows machine (fresh GitHub clone, py3.12, non-editable install, CLI + minimal_example + pytest 162/162). Key discovery: Python must be 3.10–3.12 (3.14 tries to build numpy from source).
- 2026-07-20 (commit 9ff8864): README documents the 3.10–3.12 constraint, install script pinned to `py -3.12`. Session ended here. All of section A is done except tutorial.ipynb and the Docker-covered Linux README path. Next block is the eval loop (see NEXT SESSION above).
- 2026-07-21: Eval-loop plan approved by Felix (wordgen-first order; sharkfin regenerated as-is with delta documented). Built: Dockerfile (multi-stage, ocaml/opam debian-12 → python:3.12-slim-bookworm + texlive, both bookworm so glibc matches), .dockerignore, artifact/ with reproduce.sh, smoke_test.sh, 5 figure runners, vendored wordgen source tarball. All 5 figures verified in fast mode (3m12s total). Discoveries: sharkfin committed CSVs are the paper's actual data and paper's sharkfin.pdf is just the bottom panel (added standalone-panel output to theorem4.py); paper's 11_stress_ex123_3.pdf byte-identical to committed results PDF; exp15 paper copy is cropped to drop panel titles. Sweep items resolved: CLAUDE.md edit was already committed (3edb2e5) and pushed. artifact/output/ gitignored.

## Open questions (for Felix)
1. fig:cube pngs provenance — regenerate or ship as-is with generating scripts marked approximate?
2. fig:sharkfin — RESOLVED 2026-07-21 (Felix: regenerate as-is, document delta). Better still: the committed empirical CSVs reproduce the paper curve exactly (wiggle-for-wiggle), so the caption's "50 samples/T" is likely just inaccurate; artifact regenerates a near-identical figure. Delta documented in the runner docstring, to be repeated in artifact README.
3. Anonymous repo link in the paper (anonymous.4open.science) vs. the artifact's public GitHub/Zenodo — final camera-ready footnote should point where? (deferred with camera-ready)

## Pending small cleanup
- [ ] Delete `experiments/paper_experiments/Unif_Sampling_for_Tre_EMSOFT/` — approved by Felix (verified: only unique content is an Overleaf zip from 2026-06-18, all superseded by paper_source/). Blocked: root-owned files; Felix must run `rm -rf` himself (command provided in chat).
