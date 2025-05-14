# VolTRE: Volumetry and Uniform Sampling for Timed Regular Expressions

This repository provides the implementation of **VolTRE**, a tool for volumetry and uniform sampling in timed regular expressions (TRE), based on novel methods (to be published).

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




## Paper: _Slice Sampling for Timed Regular Languages_

This repository is associated with the upcoming paper **"Slice Sampling for Timed Regular Languages"**. 




## Features

- **Uniform Sampling of Timed Words**: Samples timed words of a specified length and duration within a timed regular language, ensuring equal probability for all valid words.
- **Timed Regular Expressions (TRE) Support**: Focuses on uniform sampling exclusively for TRE, addressing a gap in existing research.
- **Exact Duration Control**: Allows sampling with an exact duration, an improvement over prior methods that only controlled expected durations.

More details can be found in our publications. A research paper complementing the diploma thesis is under development.

A selection of experiments can be found in [this folder](./experiments/paper_experiments).

## Quickstart

### Installation
Follow these steps to create a virtual environment and install the tool:
- Install Python 3
- Install Git
- Install pip
- Clone this repository: ````git clone https://github.com/figlerg/VolTRE````
- cd into the top level folder: ````cd VolTRE````
- Create a new venv: ````python3 -m venv venv````
- Activate the venv (choose one): 
  - For Windows Powershell: ````venv\Scripts\activate.ps1````
  - For Windows cmd: ````venv\Scripts\activate.bat````
  - For macOS/Linux: ````source venv/bin/activate````
- Install the required modules: ````pip install -r requirements.txt````
- Install the module using setup.py ````pip install -e .````


Assuming that your platform is Windows Powershell and the prerequisites are installed, you can run this bash script to install 
(note that depending on your installation you may need to substitute "py" with "python", "python3", or the full path of your python executable):
````bash
git clone https://github.com/figlerg/VolTRE
cd VolTRE
py -m venv venv
venv\Scripts\activate.ps1
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





