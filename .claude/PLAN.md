# PLAN — EMSOFT 2026 artifact

Last updated: 2026-07-21 (Docker image verified end to end in fast mode on Felix's machine).

## ▶ NEXT SESSION — start here
IN PROGRESS (2026-07-22): reviewer-facing rework of the eval loop, decided with Felix:
1. [DONE] fig:cube (Figure 2) added — new source folder experiments/paper_experiments/fig2_cube/ (Benoit's wordgen data + gnuplot 3D/projection + VolTRE volume). Runs fast (committed .dat) and full (--resample via wordgen). All 3 panels verified in the sandbox. Adds gnuplot as a dependency (needs gnuplot-nox in Docker).
2. [NEXT, RISKY] figN naming + "full uniform rewrite" of the runners (Felix chose the deepest option): every reproducible figure = one real script taking plain CLI flags (--out/--resample, +--wordgen for ksweep), reproduce.sh becomes a flat list of direct script calls + `cp` to figN names (fig2a/2b/2c, fig3, fig4, fig6, fig7, fig9a/9b/9c). Retrofit argparse into theorem4.py, exp15_maxent_triangle.py, exp16_ksweep.py, make_combined_plot.py (replaces the VOLTRE_* env-var contract). Stress needs a committed stress_compute.py to kill the notebook-cell-surgery in the current stress.py. deltasigma keeps its clean inlined runner. Remove artifact/figures/*.py wrappers. TOUCHES PAPER-PRODUCING CODE — verify each script against its committed output; full Docker re-verify at the end (~85 min).
3. Reproducibility map table in STATUS.md (paper figN -> output file -> script -> fast/full) as the reviewer's manual-verification checklist and Reproducible-badge justification.
4. THEN archival (section E): cut emsoft26-artifact branch + tag, Zenodo DOI (then fill STATUS placeholder), paper PDF into archive, clean-machine vetting, HotCRP form. Watch the ΣΔ Simulink discussion.

Compiled figure numbering — CONFIRMED against the PDF 2026-07-22 (PyMuPDF caption extraction, since poppler/pdftoppm is not installed): 1 potatoes(diagram), 2 cube(repro,3p), 3 stress(repro), 4 sharkfin(repro), 5 takill/DTA(diagram), 6 exp16(repro,wordgen), 7 maxent(repro), 8 falsifies(Simulink,data-only), 9 volumeDeltaSigma(repro,3p), 10 integrals(appendix diagram). Reproducible = 2,3,4,6,7,9 (10 output files): fig2a/2b/2c, fig3, fig4, fig6, fig7, fig9a/9b/9c.

Still open: multi-arch buildx; INSTALL only documents the bash `-v "$PWD/..."` mount form, consider adding the PowerShell `${PWD}` variant; Felix to run `rm -rf "/workspace/experiments/paper_experiments/Unif_Sampling_for_Tre_EMSOFT"` (root-owned); optional dev-venv repin (numpy drifted to 2.2.6).

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
- [x] Verify README CLI examples + `minimal_example.py`: done on Windows fresh clone 2026-07-20 (sampling example + minimal_example OK, plot shown). `tutorial.ipynb` verified 2026-07-21: runs end to end headlessly (nbconvert --execute) in a fresh pinned venv. NOTE: it fails under numpy 2.x (dev venv drifted to 2.2.6; sympy can't parse numpy-2 repr in VolumePoly.plot:362), irrelevant for the pinned artifact env. Optional dev follow-ups: repin .venv, one-line float() cast fix.
- [x] Run pytest suite in fresh env (2026-07-20): after fixes, **162 passed, 0 failed, ~86 s** in a fresh non-editable py3.12 venv, run from repo root. Fixed pre-existing suite bugs: (1) cwd-dependent `../experiments` paths in test_sample_maxent/test_lambda_tuning → `__file__`-anchored; (2) test_parse expected old `ParseCancellationException`, now `TREParseError`; (3) test_load_ta_samples pointed at renamed `ta_sample_1.txt` → `ta_sample_old.txt`; (4) added `tests/__init__.py` (suite previously only collected under editable install). Expected-state note for INSTALL: 162 passed, warnings are harmless (TODO warnings + experimental intersection match).
- [x] Build **Docker image**: built and verified on Felix's Windows machine 2026-07-21. Two fixes needed: (1) wordgen's src/dune requires yojson, undeclared in its dune-project → pinned yojson.3.0.0 in Dockerfile stage 1; (2) `experiments` package not importable under non-editable install → common.py exports REPO_ROOT on sys.path/PYTHONPATH. In-container: smoke_test.sh OK (wordgen found), full fast reproduce loop OK (all 8 PDFs, ~3.5 min).
- [ ] Optional: PyPI publication (nice-to-have, not required).

### B. Evaluation loop (definition of done)
- [x] Per-figure runners built 2026-07-21 under `artifact/figures/` (common.py, volume_delta_sigma.py, maxent_triangle.py, sharkfin.py, stress.py, ksweep_ta_vs_tre.py). Entry point `artifact/reproduce.sh [figure ...] [--full]`. Fast mode (default): regenerate plots from committed CSVs, full loop 3m12s, all 5 figures verified visually against the paper (stress even byte-identical data; sharkfin CSVs turned out to BE the paper's data). Full mode (`--full`): recompute measurements with seed 42; CSVs/PDFs go to artifact/output/, repo stays clean. Env plumbing added to the 4 experiment scripts (VOLTRE_RESAMPLE, VOLTRE_OUT_DIR, VOLTRE_RESULTS_DIR, WORDGEN_BIN).
- [x] Smoke test `artifact/smoke_test.sh` (~30 s: parse + volume + 3 samples + wordgen presence check).
- [x] Full-mode run at real budgets: Felix ran `reproduce.sh --full` in the container 2026-07-21, completed cleanly in ~85 min (deltasigma 35 s, maxent 159 s, sharkfin 2334 s, stress 644 s, ksweep 1716 s). Much faster than the ~6 h worst case because wordgen failed fast on memory (k=7 SIGABRT after 8 min, k=8 explicit OOM after 14 min, then two-consecutive-failures stop, k=9 never attempted) instead of burning 1 h timeouts, and the stress sweeps finished under budget. Qualitative results match the paper: VolTRE scales through k=9, wordgen dies at k>=7 locally (paper's committed data: k>=7 OOM too). ksweep + stress PDFs visually checked against the paper. Log oddities, all cosmetic: interleaved print ordering from block buffering, "(from csv)" header hardcoded in exp16_ksweep.py:688 despite fresh computation, mojibake em dash in PowerShell log encoding.
- [x] Docker run of the loop: fast mode verified in-container 2026-07-21 (see section A).
- Note: figure runners fall back to mathtext when LaTeX is absent (fonts differ, content identical); Docker image installs texlive for paper-identical fonts.

### C. Documentation files (required by guidelines)
- [~] Drafted 2026-07-21, uncommitted, pending Felix's diff review:
- [x] README — added "EMSOFT 2026 Artifact" section: reproduce.sh usage, per-figure table (fast/full runtimes), pointers to the other doc files.
- [x] REQUIREMENTS.md — hardware (commodity CPU, RAM note for ksweep --full), Docker vs native, Python 3.10–3.12, optional LaTeX/wordgen/MATLAB notes.
- [x] STATUS.md — all three badges with justifications; ΣΔ MATLAB figures declared data-only. TODO inside: insert Zenodo DOI before submission.
- [x] LICENSE — BSD 3-Clause already at repo root (verify it's the intended license).
- [x] INSTALL.md — Docker + native paths, smoke-test expected output, pytest expectation. All reviewer-typed commands tested literally 2026-07-21 in the sandbox (smoke test, CLI example, pytest: 162 passed in pinned venv, tutorial nbconvert). Docker commands match what Felix ran on Windows (bash `"$PWD"` form documented).
- [ ] Accepted paper PDF included in artifact: canonical is `paper_source/Unif_Sampling_for_Tre_EMSOFT(61).pdf` (per Felix; the (31)/(37) copies were deleted 2026-07-20). PDF is gitignored — remember to add it explicitly to the artifact archive.

### D. wordgen (exp 16 comparison)
- [x] License checked 2026-07-21: GPLv3 — redistribution of source + binary in our image is fine (we ship the full source tarball, satisfying GPL source provision).
- [x] Local wordgen matches upstream commit 5502f65b (git.lacl.fr/barbot/wordgen.git, 2026-03-26) exactly (only CRLF noise). Source tarball vendored at `artifact/wordgen-src-5502f65.tar.gz` (4.4 MB, via git archive).
- [x] Clean build proven 2026-07-21 from pristine source: only deps dune + xml-light 2.5 + zarith 1.14 + ppx_deriving 6.1.1 (opam, OCaml 5.3), builds `src/wordgen.exe` in ~2 s, runtime dep only libgmp. Recipe encoded in Dockerfile stage 1.
- [x] Docker build of stage 1 verified 2026-07-21 (after adding yojson.3.0.0, undeclared dep of wordgen's src/dune; local build had only passed because the sandbox opam switch already had yojson).
- fig:exp16 fast mode does NOT need wordgen (committed CSVs); only `ksweep --full` does.

### Camera-ready + open questions (NOT part of the artifact, deadline ~3 weeks, mid-August)
- [ ] Paper plots have vastly different font sizes across figures; unify for the camera-ready. Noted 2026-07-21, explicitly deferred, do not touch now.
- [ ] ΣΔ Simulink question (open, colleagues discussing as of 2026-07-21): apparently the Simulink software/models can't be shipped directly without asking MathWorks. Decide what the artifact/camera-ready ships for the ΣΔ case study. Current artifact stance (STATUS.md): data provided, not re-runnable. Revisit once the discussion concludes.

### E. Archival & submission
- [ ] Cut artifact branch from `experimental` (frozen after submission). NOTE: do not push/cut without Felix's explicit go-ahead.
- [ ] Zenodo (or similar) deposit with **version-pinned DOI** (not "always latest").
- [ ] Vet on a clean machine before submission.
- [ ] HotCRP submission: DOI link, required skills/environment statement, paper PDF, badge selection.

## Replicable figures in the FINAL paper (main.tex as compiled)

| # | Label | File(s) in fig/ | Source | Reproducible? |
|---|-------|-----------------|--------|---------------|
| 1 | fig:potatoes | (TikZ) | — | N/A (diagram) |
| 2 | fig:cube | cubecrop3.png, outprojsquare.png + TikZ V_3 plot | experiments/paper_experiments/fig2_cube/make_cube_fig.py (built 2026-07-22). Benoit's wordgen data (out05..25.dat) + gnuplot for the 3D + projection panels; VolTRE slice_volume for V_3(T). Provenance in fig2_cube/PROVENANCE.md | ✅ Yes (3 panels) |
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
- 2026-07-21 (later): Docker image verified on Felix's Windows machine. Build failed once (yojson undeclared by wordgen upstream → pinned yojson.3.0.0 in stage 1), container reproduce failed once (`experiments` package unimportable under non-editable install → common.py now exports repo root on sys.path/PYTHONPATH, verified locally and in-container). Smoke test + full fast loop pass inside the container, all 8 PDFs written to the mounted artifact/output/. RAM decision: no .wslconfig/docker --memory tweaks, the artifact's own setrlimit 8 GB cap governs wordgen. Overnight full-mode container run planned for tonight.
- 2026-07-21 (lunch block): committed Docker fixes (8dc766a). Drafted section C doc files (README artifact section, REQUIREMENTS.md, STATUS.md, INSTALL.md), uncommitted for Felix's review. Verified tutorial.ipynb headlessly in a fresh pinned venv (passes; fails only under numpy 2.x, dev venv has drifted to 2.2.6). Pinned-venv pytest: 162 passed, 54 s. Dev-venv pytest: 4 failures, all numpy-drift, not artifact-relevant.
- 2026-07-21 (session end): Felix reviewed REQUIREMENTS/STATUS/INSTALL, made minor edits (RAM simplified to ~10 GB; runtime wording). One inconsistency fixed: his 6 h figure was attached to the default (fast) reproduce.sh call, moved to --full. All reviewer-typed doc commands verified run: smoke test, CLI example, native install path + pytest (162 passed) + tutorial nbconvert in fresh pinned venv, fast reproduce loop in sandbox and container. Docker doc commands match Felix's Windows runs modulo bash vs PowerShell $PWD quoting. Doc files remain uncommitted. Tonight: Felix's overnight full-mode container run (command in NEXT SESSION item 1; no rebuild needed, his image was built after both fixes and equals 8dc766a).
- 2026-07-21 (afternoon): Felix ran the full-mode container run immediately instead of overnight. Completed cleanly in ~85 min, all figures qualitatively verified (details in section B). README table and STATUS updated with measured runtimes. Section B is now fully done; the eval loop is verified fast + full, native + container.
- 2026-07-21 (end of day): Felix approved the README artifact section, all doc files committed. New notes from Felix: camera-ready font-size unification and the ΣΔ Simulink/MathWorks question (see camera-ready section above).
- 2026-07-22: Felix reopened the artifact with more work. (a) Benoit supplied fig2_files_benoit.zip for Figure 2 (fig:cube): 5 wordgen .dat (regexp <a>_[0,1]*, poly 3, 10^4 exact-duration traj per T) + gnuplot4_3d.gnu; original plotting script was lost, Benoit reconstructed the commands. Built experiments/paper_experiments/fig2_cube/ with data, cube.txt wireframe (regenerated, missing from the zip), PROVENANCE.md, parametrized gnuplot scripts, and make_cube_fig.py (CLI: --out/--resample/--wordgen). Produces all 3 panels; verified fast + full in the sandbox (gnuplot 6.0 installed by Felix as root). 3D slices, T=1.5 hexagon projection, and V_3(T) peaking at 0.75 all match the paper. (b) Felix asked for reviewer-facing figN naming of every reproducible output, a reasoning/mapping list in STATUS, and to make the runners "less logic-ey" — chose the full uniform rewrite (real scripts + CLI flags, flat reproduce.sh, drop the env-var contract). Triage table done (see figure table + NEXT SESSION numbering). Paused after fig:cube for Felix's diff review before touching the committed experiment scripts.

## Open questions (for Felix)
1. fig:cube pngs provenance — regenerate or ship as-is with generating scripts marked approximate?
2. fig:sharkfin — RESOLVED 2026-07-21 (Felix: regenerate as-is, document delta). Better still: the committed empirical CSVs reproduce the paper curve exactly (wiggle-for-wiggle), so the caption's "50 samples/T" is likely just inaccurate; artifact regenerates a near-identical figure. Delta documented in the runner docstring, to be repeated in artifact README.
3. Anonymous repo link in the paper (anonymous.4open.science) vs. the artifact's public GitHub/Zenodo — final camera-ready footnote should point where? (deferred with camera-ready)

## Pending small cleanup
- [ ] Delete `experiments/paper_experiments/Unif_Sampling_for_Tre_EMSOFT/` — approved by Felix (verified: only unique content is an Overleaf zip from 2026-06-18, all superseded by paper_source/). Blocked: root-owned files; Felix must run `rm -rf` himself (command provided in chat).
