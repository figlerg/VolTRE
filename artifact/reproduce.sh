#!/usr/bin/env bash
# Reproduce the replicable figures of the paper.
#
# Usage:
#   ./reproduce.sh [figure ...] [--full]
#
# Figures (default: all):
#   stress      Fig. "stress"            (11_stress_ex123_3.pdf)
#   sharkfin    Fig. "sharkfin"          (sharkfin.pdf)
#   ksweep      Fig. "exp16"             (exp16_ksweep_v8_k8.pdf)
#   maxent      Fig. "maxent-triangle"   (exp15_maxent_triangle_variance_3_cropped.pdf)
#   deltasigma  Fig. "volumeDeltaSigma"  (08*_delta_sigma_*_n_10.pdf, 3 files)
#
# Without --full, figures are regenerated from the committed measurement data
# (minutes in total). With --full, all measurements are recomputed from scratch
# (hours; ksweep additionally needs a wordgen binary, see README).
#
# Output: artifact/output/
set -eu
cd "$(dirname "$0")/figures"

FULL=""
FIGS=()
for arg in "$@"; do
  case "$arg" in
    --full) FULL="--full" ;;
    stress|sharkfin|ksweep|maxent|deltasigma) FIGS+=("$arg") ;;
    *) echo "Unknown argument: $arg (see header of this script)"; exit 1 ;;
  esac
done
[ ${#FIGS[@]} -eq 0 ] && FIGS=(deltasigma maxent sharkfin stress ksweep)

declare -A SCRIPT=(
  [stress]=stress.py
  [sharkfin]=sharkfin.py
  [ksweep]=ksweep_ta_vs_tre.py
  [maxent]=maxent_triangle.py
  [deltasigma]=volume_delta_sigma.py
)

for fig in "${FIGS[@]}"; do
  echo "=== ${fig} ==="
  python3 "${SCRIPT[$fig]}" $FULL
done

echo
echo "All requested figures written to $(cd ../output && pwd)."
