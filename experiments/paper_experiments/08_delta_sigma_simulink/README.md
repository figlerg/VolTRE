# Delta-Sigma modulator case study (paper Fig. 8) - MATLAB/Simulink part

This folder holds the MATLAB/Simulink half of the Delta-Sigma falsification
case study. VolTRE samples timed words from the paper's expressions e_A, e_B,
e_C, these words are turned into continuous input signals, and Breach
falsifies a saturation requirement on a Simulink model of the modulator
driven by those signals. This produces the results reported around Fig. 8.

This part is not included in the Docker reproduction loop because it needs a
licensed MATLAB/Simulink installation. It is provided here so that a reader
with MATLAB can re-run the study end to end.

## Requirements

- MATLAB/Simulink R2022a or more recent
- the Breach toolbox (not bundled, see next section)
- only if Breach's precompiled MEX binaries do not cover your platform: a
  supported C/C++ compiler (check with `mex -setup` and `mex -setup C++`
  in MATLAB, see the troubleshooting note below)

## Getting Breach

Breach is developed by Decyphir and distributed under the BSD 3-Clause
license at https://github.com/decyphir/breach. It is not bundled here to
keep the artifact lean. Clone release 1.8.0 into this folder under the name
`breach-dev` (the driver script expects that path):

```bash
git clone --depth 1 --branch 1.8.0 https://github.com/decyphir/breach.git breach-dev
```

The original runs used a development snapshot of Breach that we verified to
be practically identical to release 1.8.0 (the differences on the code path
used here are whitespace and comments).

## Running the study

1. Open MATLAB with this folder as the working directory.
2. Run the main script `testUniform` (it initializes Breach itself via
   `InitBreach`). To plot the falsifiers, set the variable
   `display_option` in `testUniform.m` to a value greater than 0 (it
   ships set to 1).

No compilation step is needed on Windows, Linux, or macOS. Breach 1.8.0
ships precompiled MEX binaries for all three platforms.

Troubleshooting: if MATLAB complains about missing compiled functions,
run `InstallBreach` once from inside `breach-dev`. Be aware that on
recent MATLAB versions (observed with R2026a) `InstallBreach` fails at
the `CompileRobusthom` step with "Unrecognized function or variable".
This failure is harmless on the platforms listed above, since the
functions it would compile are already shipped as binaries.

The script processes the three signal classes in the order exA, exB, exC.
For each class it first regenerates the intermediate files in the `SigExp*`
folders (`clean_s_*` via `data_cleaning.m`, then the continuous signals
`f1cos_clean_s_*.txt` via `continuous_signal_generation.m`), then simulates
the model on each signal at three input scalings and reports falsifiers.
It pauses for ENTER between the three classes.

## What to check against the paper

The claim backed by this study is the caption of Fig. 8: the signals
sampled from e_A and e_B falsify the saturation requirement while the
signals from e_C do not. The requirement is the STL formula
`alw(OutSat[t]<=2 and OutSat[t]>=-2)` in `testUniform.m`, so "Falsified!"
means the quantizer output left the [-2, 2] band for that input.

The check is the console output: the `Number of Falsifiers` printed after
each class should be largest for exA, smaller for exB, and zero for exC.
As a reference, a run with MATLAB R2026a and Breach 1.8.0 gave 33
falsifiers for exA and 17 for exB.

With `display_option > 0` the script also plots each falsifier: the peak
input signal together with the quantizer output escaping the saturation
band.

## Recreating the three panels of Fig. 8

Fig. 8 shows, left to right, the input and quantizer output for the
sample s_050 of e_C (no falsification), s_044 of e_B (falsifies), and
s_099 of e_A (falsifies), rendered at input scaling 5.745e-8. These are
illustrative traces from the campaign that `testUniform.m` re-runs, the
case study's actual claim is the falsifier counts reported there. The script
`make_fig8_panels.m` recreates exactly these three panels. Run it from
this folder after the Breach clone step above (it does not require a
prior `testUniform` run, it regenerates the continuous signals it needs
from the committed timed words). It prints the robustness verdict for
each panel and saves the plots as `fig8_panel*.png` next to the script.

Expected output: no falsification for SigExpC s_050, falsified for
SigExpB s_044 and SigExpA s_099, and three plots matching the panels of
Fig. 8.

## Contents

- `testUniform.m`: the main driver described above
- `data_cleaning.m`, `continuous_signal_generation.m`, `piecewise_cos.m`:
  turn timed words into continuous input signals with peaks of varying width
- `ExampleBand-Pass/`: the Simulink models of the modulator and their
  parameters (`BP2param.m`)
- `Functions/`: auxiliary MATLAB functions used by the models and scripts
- `SigExpA/`, `SigExpB/`, `SigExpC/`: 100 timed words each (`s_000` to
  `s_099`), sampled uniformly by VolTRE from the expressions e_A, e_B, e_C
  of the paper. Files are one `<date> <letter>` pair per line.

## Provenance of the timed words

The `SigExp*` words are the VolTRE samples also committed next to this
folder. e_A is the universal expression (spec file
`../08c_thao_spec.tre`, samples `../08c_thao_spec.tre_10/`), e_B adds the
ordering constraint (`../08b_nicolas_spec_fat_thin.tre`, samples
`../08b_nicolas_spec_fat_thin.tre_10/`), and e_C adds the [5,inf) timed
restriction (`../08a_nicolas_spec_5_inf.tre`, samples
`../08_nicolas_spec.tre_10/`). The `08a/08b/08c` file prefixes are
historical and do not line up with the final paper's A/B/C naming, the
mapping above is the authoritative one. We checked every word in
`SigExpC` against e_C with VolTRE's own matcher (match multiplicity 1)
and verified the folders agree file for file with the committed sample
directories. The sampler that generated them is
`../08s_delta_sigma_nicolas.py`.
