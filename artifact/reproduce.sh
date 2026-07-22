#!/usr/bin/env bash
# Reproduce the replicable figures of the paper by running the real experiment
# scripts under experiments/paper_experiments/ directly (no wrappers). Each run
# writes the script's own output file(s) into artifact/output/, then copies them
# to figN_* names matching the figure numbers in the paper.
#
# Usage:
#   ./reproduce.sh [figure ...] [--full]
#
# Figures (default: all):
#   cube        Fig. 2  fig:cube             -> fig2a/2b/2c
#   stress      Fig. 3  fig:stress           -> fig3
#   sharkfin    Fig. 4  fig:sharkfin         -> fig4
#   ksweep      Fig. 6  fig:exp16            -> fig6
#   maxent      Fig. 7  fig:maxent-triangle  -> fig7
#   deltasigma  Fig. 9  fig:volumeDeltaSigma -> fig9a/9b/9c
#
# Without --full, figures are regenerated from the committed measurement data
# (minutes in total). With --full, all measurements are recomputed from scratch
# (hours; cube and ksweep additionally need a wordgen binary, see README).
#
# Output: artifact/output/  (both the paper-named files and the figN_* copies)
set -eu

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
EXP="$REPO/experiments/paper_experiments"
OUT="$HERE/output"
mkdir -p "$OUT"

# The experiment scripts import the repo-root package `experiments`; export the
# repo root so a non-editable install still finds it. Force a headless backend.
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"
export MPLBACKEND=Agg

FULL=0
FIGS=()
for arg in "$@"; do
  case "$arg" in
    --full) FULL=1 ;;
    cube|stress|sharkfin|ksweep|maxent|deltasigma) FIGS+=("$arg") ;;
    *) echo "Unknown argument: $arg (see header of this script)"; exit 1 ;;
  esac
done
[ ${#FIGS[@]} -eq 0 ] && FIGS=(cube deltasigma maxent sharkfin stress ksweep)

for fig in "${FIGS[@]}"; do
  echo "=== $fig ==="
  case "$fig" in

    cube)  # Fig 2
      if [ "$FULL" = 1 ]; then
        python3 "$EXP/fig2_cube/make_cube_fig.py" --out "$OUT" --resample
      else
        python3 "$EXP/fig2_cube/make_cube_fig.py" --out "$OUT"
      fi
      cp "$OUT/cube_3d.png"         "$OUT/fig2a_cube_3d.png"
      cp "$OUT/cube_projection.png" "$OUT/fig2b_cube_projection.png"
      cp "$OUT/cube_volume.pdf"     "$OUT/fig2c_cube_volume.pdf"
      ;;

    stress)  # Fig 3
      if [ "$FULL" = 1 ]; then
        python3 "$EXP/11_stress_test/stress_compute.py" --out "$OUT"
        python3 "$EXP/11_stress_test/make_combined_plot.py" --results "$OUT" --out "$OUT"
      else
        python3 "$EXP/11_stress_test/make_combined_plot.py" --out "$OUT"
      fi
      cp "$OUT/11_stress_ex123.pdf" "$OUT/fig3_stress.pdf"
      ;;

    sharkfin)  # Fig 4
      if [ "$FULL" = 1 ]; then
        python3 "$EXP/13_nicolas_ambiguity/theorem4.py" --out "$OUT" --resample
      else
        python3 "$EXP/13_nicolas_ambiguity/theorem4.py" --out "$OUT"
      fi
      cp "$OUT/sharkfin.pdf" "$OUT/fig4_sharkfin.pdf"
      ;;

    ksweep)  # Fig 6
      if [ "$FULL" = 1 ]; then
        python3 "$EXP/16_ta_vs_tre_2/exp16_ksweep.py" --results "$OUT" --out "$OUT" --resample
      else
        python3 "$EXP/16_ta_vs_tre_2/exp16_ksweep.py" --out "$OUT"
      fi
      cp "$OUT/exp16_ksweep_v8_k8.pdf" "$OUT/fig6_ksweep.pdf"
      ;;

    maxent)  # Fig 7
      if [ "$FULL" = 1 ]; then
        python3 "$EXP/15_moment_control_qest23_redo/exp15_maxent_triangle.py" --out "$OUT" --resample
      else
        python3 "$EXP/15_moment_control_qest23_redo/exp15_maxent_triangle.py" --out "$OUT"
      fi
      cp "$OUT/exp15_maxent_triangle.pdf" "$OUT/fig7_maxent.pdf"
      ;;

    deltasigma)  # Fig 9 (exact volume, no fast/full distinction)
      python3 "$EXP/make_delta_sigma_fig.py" --out "$OUT"
      cp "$OUT/08_delta_sigma_nicolas_n_10.pdf"           "$OUT/fig9a_deltasigma.pdf"
      cp "$OUT/08b_delta_sigma_nicolas_fat_thin_n_10.pdf" "$OUT/fig9b_deltasigma.pdf"
      cp "$OUT/08c_delta_sigma_thao_n_10.pdf"             "$OUT/fig9c_deltasigma.pdf"
      ;;
  esac
done

echo
echo "Requested figures written to $OUT (paper names + figN_* copies)."
