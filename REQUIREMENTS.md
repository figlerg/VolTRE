# REQUIREMENTS

## Hardware

- Commodity x86-64 machine, CPU only (no GPU, no special peripherals).
  Reference machine: laptop, Intel i7-1265U, 32 GB RAM.
- RAM: ~10 GB should be enough.
- Disk: about 5 GB for the Docker image, about 1 GB for a native install.

## Software

- Recommended: **Docker**. The image contains everything: VolTRE, its pinned
  Python dependencies, a wordgen binary (comparison baseline), and LaTeX for
  paper-identical figure fonts. See INSTALL.md.
- Native alternative: Python **3.10 to 3.12** (3.13+ is not supported by the
  pinned dependency versions) with the exact package versions in
  `requirements.txt`. Optional extras, only needed natively:
  - a LaTeX installation (figure fonts match the paper, otherwise matplotlib
    falls back to mathtext and only the fonts differ),
  - wordgen (https://git.lacl.fr/barbot/wordgen.git), only for
    `ksweep --full`. The vendored source we build in Docker is at
    `artifact/wordgen-src-5502f65.tar.gz`.
- The ΣΔ modulator case study additionally used MATLAB/Simulink. It is not
  part of the reproduction loop, see STATUS.md.
