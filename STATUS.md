# STATUS

Artifact for the EMSOFT 2026 paper "Uniform Sampling for Timed Regular
Expressions". We apply for all three badges.

## Available

The artifact is archived on Zenodo with a version-pinned DOI
(**TODO: insert DOI before submission**) under the BSD 3-Clause license
(see LICENSE). Development continues at https://github.com/figlerg/VolTRE,
which does not replace the archived copy.

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

`./artifact/reproduce.sh` regenerates every replicable figure of the paper,
in two modes:

- fast (default): plots are rebuilt from the committed measurement data,
  minutes in total. This reproduces the paper figures exactly.
- `--full`: all measurements are recomputed from scratch with a fixed seed
  (42), taking hours. Sampling-based figures reproduce exactly; the two
  timing figures (stress, ksweep) show the reviewer's hardware timings, so
  absolute numbers differ while the qualitative result (scaling behavior,
  wordgen's blow-up for k >= 6) is reproduced.

Exception, stated for transparency: the ΣΔ modulator case-study figures were
produced with a licensed MATLAB/Simulink toolchain. For these we provide the
data, but they are not re-runnable within this artifact.
