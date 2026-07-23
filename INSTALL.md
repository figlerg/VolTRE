# INSTALL

Two ways to run the artifact. Docker is recommended and was used for vetting.

## Option A: Docker (recommended)

From the repository root:

```bash
docker build -t voltre-artifact .
docker run --rm -it voltre-artifact ./artifact/smoke_test.sh
```

The build takes about 10 minutes. The smoke test (about a minute) parses a
TRE, computes a volume, and draws samples. Expected output ends with:

```
VolTRE smoke test OK
wordgen binary found (full mode of the ksweep figure available)
Smoke test passed.
```

Once the smoke test passes, the image is ready. Reproducing the paper figures is
driven from the walkthrough in README.md (step 3), which also lists the figures,
their runtimes, and the `--full` mode. This file covers only getting VolTRE
installed and verifying the install.

On Apple Silicon Macs the image builds and runs natively as arm64 (both base
images are multi-arch and the wordgen baseline is compiled from source during
the build), so no `--platform` flag is needed. If you ever hit an
architecture-specific problem, you can force the exact x86_64 image we tested by
adding `--platform=linux/amd64` to both the `docker build` and the `docker run`
commands, but note it then runs under emulation and is noticeably slower (the
`--full` suite is already about 1.5 h natively).

## Option B: native install

Requires Python 3.10 to 3.12, see REQUIREMENTS.md. From the repository root:

```bash
python3.12 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate.ps1
pip install -r requirements.txt
pip install .
```

Check the installation:

```bash
./artifact/smoke_test.sh         # as above; "wordgen NOT found" is fine natively
python -m pytest tests           # expected: 162 passed (~2 min), warnings are harmless
```

A first useful run, sampling 20 uniform timed words with 5 events and total
duration 0.5 from the expression in `experiments/spec_00.tre`:

```bash
python main.py -p experiments/spec_00.tre -n 5 -T 0.5 --nr_samples 20
```

More usage examples: README.md (CLI), `minimal_example.py`, `tutorial.ipynb`.
