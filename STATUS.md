# STATUS

Artifact for the EMSOFT 2026 paper "Uniform Sampling for Timed Regular
Expressions". We apply for all three badges.

## Available

The artifact is archived on Zenodo with a version-pinned DOI
([10.5281/zenodo.21512672](https://doi.org/10.5281/zenodo.21512672)) under the
BSD 3-Clause license (see LICENSE). Development continues at
https://github.com/figlerg/VolTRE, which does not replace the archived copy.

## Reviewed

The artifact is complete and documented (README.md, INSTALL.md,
REQUIREMENTS.md). A reviewer can check the installation in about a minute
with `./artifact/smoke_test.sh` and regenerate all replicable paper figures
in a few minutes with `./artifact/reproduce.sh`, or recompute all
measurements from scratch in about 1.5 h (measured in the container on the
reference machine, see README.md for details) with
`./artifact/reproduce.sh --full` (expected outputs are stated in INSTALL.md
and README.md). A Dockerfile provides the exact environment,
including the wordgen comparison baseline built from vendored source.

## Reproducible

Every figure of the paper that rests on VolTRE's own computation is regenerated
by `./artifact/reproduce.sh`. That covers figures 2, 3, 4, 6, 7, and 9. Figure
8 is also reproducible, but through MATLAB rather than the Docker loop (see
below). The remaining figures (1, 5, 10) are hand-drawn diagrams.

The code behind each reproducible figure is the real experiment code under
`experiments/paper_experiments/`. `reproduce.sh` runs these scripts directly and
copies each result to a `figN_*` file in `artifact/output/`:

- Figure 2 (hypercube slices and volume function): `fig2_cube/make_cube_fig.py`
- Figure 3 (scaling stress test): `11_stress_test/stress_compute.py` and
  `11_stress_test/make_combined_plot.py`
- Figure 4 (ambiguity trials): `13_nicolas_ambiguity/theorem4.py`
- Figure 6 (VolTRE vs. wordgen k-sweep): `16_ta_vs_tre_2/exp16_ksweep.py`
- Figure 7 (max-entropy triangle): `15_moment_control_qest23_redo/exp15_maxent_triangle.py`
- Figure 8 (ΣΔ falsification panels): `08_delta_sigma_simulink/make_fig8_panels.m`
  and `08_delta_sigma_simulink/testUniform.m` (MATLAB, see below)
- Figure 9 (ΣΔ volume functions): `make_delta_sigma_fig.py`

`./artifact/reproduce.sh` regenerates all of them except Figure 8 in two
modes:

- `--full`: every measurement is recomputed from scratch with a fixed seed
  (42), so VolTRE's sampling and volume computation run end to end (about
  1.5 h). This is the reproduction that matters. The sampling-based figures
  come out identical to the paper, while the two timing figures (stress,
  ksweep) show the reviewer's own hardware timings, so absolute numbers
  differ while the qualitative result (scaling behavior, wordgen's blow-up
  for k >= 6) is reproduced.
- fast (default when `--full` is omitted): the plots are rebuilt from the
  committed measurement data in minutes. This reproduces the paper figures
  exactly but does not re-run the methods, so it is a quick look rather than
  a full reproduction.

Figure 8 (the ΣΔ falsification case study) is the one reproducible figure
outside the Docker loop, because it needs a licensed MATLAB/Simulink
installation. The artifact ships everything else required: the Simulink
models, the driver scripts, and the VolTRE-sampled input words, with full
instructions in
`experiments/paper_experiments/08_delta_sigma_simulink/README.md`.
`testUniform.m` reproduces the falsifier counts behind the figure's claim
(more falsifiers for e_A than e_B, none for e_C) and `make_fig8_panels.m`
recreates the three panels themselves. The run was verified with MATLAB
R2026a and Breach 1.8.0 (cloned per the instructions, not bundled).
