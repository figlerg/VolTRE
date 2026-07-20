# PLAN — EMSOFT 2026 artifact

Last updated: 2026-07-20 (initial version, derived from .claude/artifact_guidelines_emsoft.md + paper_source).

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
- [ ] Verify README install steps literally in a fresh venv (README install script is Windows-flavored; add/verify Linux path).
- [ ] Verify README CLI examples literally (`python main.py -p experiments/spec_00.tre ...`), `minimal_example.py`, and `tutorial.ipynb` in fresh env.
- [ ] Run pytest suite in fresh env; record expected pass state.
- [ ] Build **Docker image** (required by guidelines for non-trivial tools) containing artifact + all deps; artifact must run end-to-end inside it.
- [ ] Optional: PyPI publication (nice-to-have, not required).

### B. Evaluation loop (definition of done)
- [ ] One documented command (or small set) that reproduces every replicable figure below in a fresh Docker container, no undocumented manual steps.
- [ ] Per-figure runner scripts with seeds; decide fast mode vs full mode (some experiments are hours-long — provide precomputed results + "reproduce from scratch" switch; wordgen budget alone is 3600 s).
- [ ] Smoke test target (< a few minutes) for reviewers to confirm installation works (INSTALL file requirement).

### C. Documentation files (required by guidelines)
- [ ] README — what the artifact does, usage, how to reproduce each paper figure.
- [ ] REQUIREMENTS — hardware/software env, Docker, requirements.txt with versions.
- [ ] STATUS — badges applied for + justification.
- [x] LICENSE — BSD 3-Clause already at repo root (verify it's the intended license).
- [ ] INSTALL — install steps + basic usage example + expected output check.
- [ ] Accepted paper PDF included in artifact: canonical is `paper_source/Unif_Sampling_for_Tre_EMSOFT(61).pdf` (per Felix; the (31)/(37) copies were deleted 2026-07-20). PDF is gitignored — remember to add it explicitly to the artifact archive.

### D. wordgen (exp 16 comparison)
- [ ] wordgen is gitignored, not shipped. Document as optional prerequisite with pointer to its installation instructions.
- DECIDED (Felix 2026-07-20): shipping wordgen inside the Docker image is the optimal outcome — attempt it. Fallback if it doesn't build in time: fig:exp16 partially reproducible (VolTRE bars) + cached wordgen results (`16_ta_vs_tre_2/results/`, `20260616_benoit_results/`).
- [ ] Check wordgen's license permits redistribution inside our image; otherwise install-from-source in Dockerfile.

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
- 2026-07-20 (commit c3bd3ff): committed artifact-prep changes (README, requirements.txt, CLAUDE.md, .claude notes/settings, .gitignore). The previously-unclear .gitignore modification turned out to be Felix's own `paper_source` ignore line — resolved, included. Not pushed (per workflow rules).

## Open questions (for Felix)
1. fig:cube pngs provenance — regenerate or ship as-is with generating scripts marked approximate?
2. fig:sharkfin — exact generation settings to be recovered, deferred until we build that part of the eval loop. Git is a dead end (checked 2026-07-20: theorem4.py has a single commit with NR_SAMPLES=200; the whole `paper_source/` dir is gitignored, so sharkfin.pdf has no history). Felix may check emails; otherwise regenerate with theorem4.py and document the (small) parameter difference.
3. Anonymous repo link in the paper (anonymous.4open.science) vs. the artifact's public GitHub/Zenodo — final camera-ready footnote should point where? (deferred with camera-ready)

## Pending small cleanup
- [ ] Delete `experiments/paper_experiments/Unif_Sampling_for_Tre_EMSOFT/` — approved by Felix (verified: only unique content is an Overleaf zip from 2026-06-18, all superseded by paper_source/). Blocked: root-owned files; Felix must run `rm -rf` himself (command provided in chat).
