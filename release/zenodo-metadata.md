# Zenodo metadata for the VolTRE EMSOFT 2026 artifact

Paste-ready field sheet for the manual Zenodo upload. This file is internal
(the `release/` folder is `export-ignore`d), so it does not ship inside the
artifact zip. See `release/ARCHIVING.md` for the full release sequence.

## Fields

- **Upload type:** Software
- **Title:** VolTRE: Uniform Sampling for Timed Regular Expressions (EMSOFT 2026 artifact)
- **Version:** v1.0  (match the git tag, for example v1.0-emsoft26)
- **Language:** English
- **License:** BSD 3-Clause (primary). The bundled wordgen component is GPLv3,
  documented in NOTICE and in the COPYING inside
  artifact/wordgen-src-5502f65.tar.gz.

## Authors and affiliations

Add ORCIDs where available.

1. Felix Gigler - TU Wien, Vienna, Austria; AIT Austrian Institute of Technology, Vienna, Austria - ORCID 0000-0002-6495-9048
2. Dejan Nickovic - AIT Austrian Institute of Technology, Vienna, Austria
3. Nicolas Basset - Univ. Grenoble Alpes, CNRS, Grenoble INP, VERIMAG, Grenoble, France
4. Thao Dang - Univ. Grenoble Alpes, CNRS, Grenoble INP, VERIMAG, Grenoble, France
5. Ezio Bartocci - TU Wien, Vienna, Austria
6. Benoit Barbot - Univ Paris Est Creteil, LACL, Creteil, France

## Keywords

timed regular expressions, uniform sampling, volumetry, timed automata,
falsification, artifact evaluation, EMSOFT 2026

## Related identifiers

- is supplement to: the EMSOFT 2026 paper "Uniform Sampling for Timed Regular
  Expressions" (add its DOI once available)
- is compiled from: https://github.com/figlerg/VolTRE

## Description / abstract

VolTRE is a tool for volumetry and uniform sampling of timed regular expressions
(TRE). Given a TRE together with a target word length and total duration, it
computes the exact volume of the corresponding slice of timed words and draws
samples that are uniformly distributed over that slice, with exact rather than
only expected duration control. This archive is the artifact accompanying the
EMSOFT 2026 paper "Uniform Sampling for Timed Regular Expressions". It contains
the VolTRE implementation, the experiment scripts behind every reproducible
figure of the paper, a Docker environment that pins all dependencies, and a
one-command reproduction script (artifact/reproduce.sh). Fast mode rebuilds the
paper figures from committed measurement data in minutes, while --full recomputes
every measurement from scratch with a fixed seed. The bundled wordgen tool
(GPLv3, see NOTICE) is included only as a comparison baseline for one figure. The
delta-sigma modulator case study (Fig. 8) additionally used a licensed
MATLAB/Simulink toolchain and is provided as data rather than as a re-runnable
step, as documented in STATUS.md.
