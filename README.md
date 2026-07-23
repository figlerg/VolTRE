# VolTRE: Volumetry and Uniform Sampling for Timed Regular Expressions

This repository provides the implementation of **VolTRE**, a tool for volumetry and uniform sampling in timed regular expressions (TRE), based on novel methods (to be published).

## EMSOFT 2026 Artifact

This repository is the EMSOFT 2026 artifact for the paper *"Uniform Sampling for Timed Regular Expressions"* (accepted at EMSOFT 2026). **Reviewers start here.** The suggested path through the artifact:

1. **Set up the environment.** Check the hardware and software prerequisites in [REQUIREMENTS.md](REQUIREMENTS.md), then follow [INSTALL.md](INSTALL.md). Docker is recommended, and with it the build is just:
   ```bash
   docker build -t voltre-artifact .
   ```
2. **Check the installation** with the smoke test (about a minute: it parses a TRE, computes a volume, and draws samples):
   ```bash
   docker run --rm -it voltre-artifact ./artifact/smoke_test.sh
   ```
3. **Reproduce the paper figures.** For a genuine reproduction use `--full`: it re-runs VolTRE's sampling and volume computations from scratch (fixed seed 42) and rebuilds every figure from those fresh results (about 1.5 h):
   ```bash
   docker run --rm -v "$PWD/artifact/output:/voltre/artifact/output" voltre-artifact ./artifact/reproduce.sh --full
   ```
   Omitting `--full` instead rebuilds the plots from the committed measurement data in a few minutes. That is only a quick look at the plotting step, not a re-run of the methods.
4. **Check the figures** in `artifact/output/`: ten `figN_*` files whose numbers match the paper, plus an `intermediates/` folder holding the underlying PDFs, CSVs, and `.dat` files for anyone who wants to dig deeper.
5. **Reproducibility and badges.** [STATUS.md](STATUS.md) maps every paper figure to the code that produces it and lays out our case for the three badges.

The figures produced by `reproduce.sh`, the scripts behind them, and their fast and `--full` runtimes:

| `reproduce.sh` name | paper fig. | output (`figN_*`) | paper figure (PDF name) | fast | `--full` |
|---|---|---|---|---|---|
| `cube` | 2 | `fig2a/2b/2c` | `cubecrop3.png`, `outprojsquare.png`, TikZ `V_3(T)` | ~1 min | ~5 min, needs wordgen |
| `stress` | 3 | `fig3` | `11_stress_ex123_3.pdf` | seconds | ~10 min |
| `sharkfin` | 4 | `fig4` | `sharkfin.pdf` | seconds | ~40 min |
| `ksweep` | 6 | `fig6` | `exp16_ksweep_v8_k8.pdf` | seconds | ~30 min, needs wordgen |
| `maxent` | 7 | `fig7` | `exp15_maxent_triangle_variance_3_cropped.pdf` | seconds | ~3 min |
| `deltasigma` | 9 | `fig9a/9b/9c` | `08*_delta_sigma_*_n_10.pdf` (3 files) | ~1 min | same (always computed live) |

Full-mode times measured in the Docker container on the reference machine (see REQUIREMENTS.md), ~1.5 h in total. `cube --full` and `ksweep --full` need a wordgen binary (the Docker image ships one). `ksweep --full` can take up to several hours on machines where wordgen runs into the 1 h timeout instead of failing fast on memory.

Note on `ksweep --full`: at the larger nesting depths wordgen prints errors and eventually crashes (`error:-6`, `Fatal error: exception Out of memory`), and the run reports "Two consecutive failures — stopping at k=8." This is the expected result, not an artifact bug. The whole point of Fig. 6 is that wordgen blows up in states and memory as the nesting depth grows while VolTRE stays fast, so the script deliberately catches these failures and records them as the baseline giving up.

`--full` recomputes all measurements from scratch (fixed seed 42), so it exercises the sampling and volume methods end to end. The sampling-based figures come out identical to the paper, while for the two timing figures (`stress`, `ksweep`) the absolute numbers depend on your hardware and only the qualitative result is reproduced. Fast mode (the default when you omit `--full`) instead rebuilds the plots from the committed measurement data, reproducing the paper figures exactly but without re-running the methods. Without a LaTeX installation the figures fall back to matplotlib's mathtext (content identical, fonts differ). The Docker image ships LaTeX, gnuplot (used for the `cube` 3D/projection panels), and the wordgen baseline needed for `cube --full` and `ksweep --full`.

---

## Repository documentation

Everything above is the EMSOFT 2026 artifact. The sections below are the general project documentation for using VolTRE.

## Contributors

- **Felix Gigler** (TU Wien, Vienna, Austria; AIT Austrian Institute of Technology, Vienna, Austria)
- Dejan Nickovic (AIT Austrian Institute of Technology, Vienna, Austria)
- Nicolas Basset (Univ. Grenoble Alpes, CNRS, Grenoble INP, VERIMAG, 38000 Grenoble, France)
- Thao Dang (Univ. Grenoble Alpes, CNRS, Grenoble INP, VERIMAG, 38000 Grenoble, France)
- Ezio Bartocci (TU Wien, Vienna, Austria)
- Benoît Barbot (Univ Paris Est Creteil, LACL, F-94010 Creteil, France)

This repository was developed and maintained by **Felix Gigler**.


## Master's Thesis: _Uniform Sampling of Timed Regular Expressions_
This repository accompanies the Diplomarbeit (Master's thesis) *"Uniform Sampling of Timed Regular Expressions"*, submitted as part of the Logic and Computation program at TU Wien. The work was carried out under the supervision of Dejan Nickovic (main supervisor), with additional guidance and support from Nicolas Basset, Thao Dang, and Ezio Bartocci.




## Paper: _Uniform Sampling for Timed Regular Expressions_

This repository is associated with the paper **"Uniform Sampling for Timed Regular Expressions"** (accepted at EMSOFT 2026). 


## Features

- **Uniform Sampling of Timed Words**: Samples timed words of a specified length and duration within a timed regular language, ensuring equal probability for all valid words.
- **Timed Regular Expressions (TRE) Support**: Focuses on uniform sampling exclusively for TRE, addressing a gap in existing research.
- **Exact Duration Control**: Allows sampling with an exact duration, an improvement over prior methods that only controlled expected durations.

More details can be found in our publications. A research paper complementing the diploma thesis is under development.

A selection of experiments can be found in [this folder](./experiments/paper_experiments).

## Quickstart

### Installation
Follow these steps to create a virtual environment and install the tool:
- Install Python, **version 3.10 to 3.12** (3.10+ is needed for the syntax we use, and 3.13+ is not supported by the pinned dependency versions in requirements.txt: pip would try to build numpy/matplotlib from source)
- Install Git
- Install pip
- Clone this repository: ````git clone https://github.com/figlerg/VolTRE````
- cd into the top level folder: ````cd VolTRE````
- Create a new venv with a supported Python version: ````python3 -m venv .venv```` (if your default Python is newer than 3.12, use e.g. ````python3.12 -m venv .venv```` on Linux/macOS or ````py -3.12 -m venv .venv```` on Windows)
- Activate the venv (choose one): 
  - For Windows Powershell: ````.venv\Scripts\activate.ps1````
  - For Windows cmd: ````.venv\Scripts\activate.bat````
  - For macOS/Linux: ````source .venv/bin/activate````
- Install the required modules: ````pip install -r requirements.txt````
- Install the module using setup.py ````pip install -e .````


Assuming that your platform is Windows Powershell and the prerequisites are installed, you can run this bash script to install 
(note that depending on your installation you may need to substitute "py -3.12" with "python", "python3.12", or the full path of your python executable):
````bash
git clone https://github.com/figlerg/VolTRE
cd VolTRE
py -3.12 -m venv .venv
.venv\Scripts\activate.ps1
pip install -r requirements.txt
python -m pip install -e .

````

To check whether the installation works, run the example below.

### 🔧 CLI Examples

**Minimal sampling:**
```bash
python main.py -p experiments/spec_00.tre -n 5 -T 0.5 --nr_samples 20
```
- Samples 20 timed words
- Each word has 5 events and total duration 0.5
- Default mode = `vanilla`
- No profiling, no seed

**With profiling and fixed seed:**
```bash
python main.py -p experiments/spec_00.tre -n 8 --budget 1000 --nr_samples 30 --verbose --seed 123
```
- Enables profiling and fixed randomness
- Useful for reproducibility and performance measurement
- Profiling data saved to `main.prof`

**Only visualize the slice volume (no sampling):**
```bash
python main.py -p experiments/spec_00.tre -n 6 --visualize
```
- Computes and plots the slice volume
- If `--verbose` is used, prints the piecewise volume function
- ⚠️ Assumes no ambiguity or top-level intersection — warning shown if needed

**Print only the total volume (no sampling):**
```bash
python main.py -p experiments/spec_00.tre -n 6 --total_volume
```
- Computes and prints the total volume (area) of the slice
- Can be combined with `--verbose` for extra details


### Minimal Example - Programmatic
Test your installation by running the [minimal example](./minimal_example.py) in the top level _VolTRE_ folder (with the activated venv). You should see the graph of a volume function, and upon closing it some samples in the terminal.

````python minimal_example.py````

This is the code in the example, with comment explanations:
````python
from os.path import join
import random
import numpy as np
from parse.quickparse import quickparse
from volume.slice_volume import slice_volume
from sample.sample import sample


# SEED
np.random.seed(42)
random.seed(42)

# PARSE
ctx = quickparse(join('experiments', 'spec_00.tre'))
print(f"Parsed the expression {ctx.getText()}.")

# VOLUMES
n = 5                       # set fixed length n
T = 3.5                     # set fixed duration T

V = slice_volume(ctx, n)    # compute volume function

V.fancy_print()             # prints all segments and their polynomials

V.plot()                    # plot the function

nr_samples = 10             # assume we want to generate 10 samples

# SLICE SAMPLING
for _ in range(nr_samples):

    w = sample(ctx, n, T)      # generates a TimedWord object

    print(f"w = {w}.", f" duration = {w.duration}")  # duration is as specified


print('\nNow sampling all slices:\n')
# SAMPLING ALL SLICES
for _ in range(nr_samples):

    w = sample(ctx, n)      # generates a TimedWord object

    print(f"w = {w}.", f" duration = {w.duration}")  # duration is free but compatible with spec

````

For a more in-depth tutorial refer to our [Tutorial JuPyter Notebook](tutorial.ipynb).





