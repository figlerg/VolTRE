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
falsification, artifact evaluation, EMSOFT

## Related identifiers

- is supplement to: the EMSOFT 2026 paper "Uniform Sampling for Timed Regular
  Expressions" (add its DOI once available)
- is compiled from: https://github.com/figlerg/VolTRE

## Description / abstract

This is the artifact accompanying the paper "Uniform Sampling for Timed Regular
Expressions", submitted for artifact evaluation at EMSOFT 2026.

The paper introduces the first method to uniformly sample timed words directly
from timed regular expressions (TREs). Given a desired length and duration as
input, the method guarantees that all words of that length and duration in the
language have the same chance of being drawn. It also introduces the first
technique for treating the full class of timed regular languages recognized by
non-deterministic timed automata (excluding those that require silent
transitions), whereas previous work handled only deterministic timed automata.
The approach is implemented in VolTRE, an open-source prototype tool.

This archive packages VolTRE together with the experiment scripts, data, and a
Docker environment needed to reproduce the paper's figures. The bundled wordgen
tool (GPLv3, see NOTICE) is included only as a comparison baseline.
