# VolTRE artifact image (EMSOFT 2026, "Uniform Sampling for Timed Regular Expressions")
#
# Stage 1 builds wordgen (comparison baseline for Fig. exp16) from the vendored
# source tarball artifact/wordgen-src-5502f65.tar.gz
# (upstream: https://git.lacl.fr/barbot/wordgen.git, commit 5502f65b, GPLv3).
# Stage 2 is the Python 3.12 environment with VolTRE installed.
# Both stages are Debian 12 (bookworm) so the wordgen binary's glibc matches.
#
# Build:  docker build -t voltre-artifact .
# Run:    docker run -it voltre-artifact

FROM ocaml/opam:debian-12-ocaml-5.3 AS wordgen-build
RUN sudo apt-get update \
 && sudo apt-get install -y --no-install-recommends libgmp-dev pkg-config \
 && sudo apt-get clean
# yojson is required by wordgen's src/dune but missing from its dune-project depends.
RUN opam install -y dune.3.23.1 xml-light.2.5 zarith.1.14 ppx_deriving.6.1.1 yojson.3.0.0
COPY --chown=opam:opam artifact/wordgen-src-5502f65.tar.gz /home/opam/
RUN mkdir wordgen \
 && tar -xzf wordgen-src-5502f65.tar.gz -C wordgen \
 && cd wordgen \
 && opam exec -- dune build src/wordgen.exe

FROM python:3.12-slim-bookworm
# libgmp10: wordgen runtime dependency.
# texlive + lmodern: the paper figures use matplotlib with text.usetex and
# Latin Modern fonts; without LaTeX the runners fall back to mathtext.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      libgmp10 \
      texlive-latex-base texlive-latex-extra texlive-fonts-recommended \
      lmodern cm-super dvipng ghostscript \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /voltre
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./
RUN pip install --no-cache-dir .
COPY --from=wordgen-build /home/opam/wordgen/_build/default/src/wordgen.exe /usr/local/bin/wordgen
ENV WORDGEN_BIN=/usr/local/bin/wordgen
ENV MPLBACKEND=Agg
CMD ["bash"]
