#!/usr/bin/env bash
# Reproduce the replicable figures of the paper by running the real experiment
# scripts under experiments/paper_experiments/ directly (no wrappers). Every
# script writes its raw output into artifact/output/intermediates/. Only the
# final deliverables are copied up into artifact/output/ under figN_* names
# matching the figure numbers in the paper, so `ls artifact/output/` shows just
# those figures plus the intermediates/ folder.
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
# Output: artifact/output/  (figN_* deliverables + an intermediates/ subfolder)
set -eu

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
EXP="$REPO/experiments/paper_experiments"
OUT="$HERE/output"
mkdir -p "$OUT"

# Each script writes its own paper-named PDFs/CSVs/.dat into $WORK, a persistent
# subfolder of $OUT that a curious reviewer can inspect (the fresh measurement
# CSVs from --full live here). Only the figN_* deliverables are copied up into
# $OUT itself, so `ls $OUT` shows just the ten figures plus this one folder.
# $WORK is wiped at the start of every run so it always reflects the latest run.
WORK="$OUT/intermediates"
rm -rf "$WORK"
mkdir -p "$WORK"

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
        python3 "$EXP/fig2_cube/make_cube_fig.py" --out "$WORK" --resample
      else
        python3 "$EXP/fig2_cube/make_cube_fig.py" --out "$WORK"
      fi
      cp "$WORK/cube_3d.png"         "$OUT/fig2a_cube_3d.png"
      cp "$WORK/cube_projection.png" "$OUT/fig2b_cube_projection.png"
      cp "$WORK/cube_volume.pdf"     "$OUT/fig2c_cube_volume.pdf"
      ;;

    stress)  # Fig 3
      if [ "$FULL" = 1 ]; then
        python3 "$EXP/11_stress_test/stress_compute.py" --out "$WORK"
        python3 "$EXP/11_stress_test/make_combined_plot.py" --results "$WORK" --out "$WORK"
      else
        python3 "$EXP/11_stress_test/make_combined_plot.py" --out "$WORK"
      fi
      cp "$WORK/11_stress_ex123.pdf" "$OUT/fig3_stress.pdf"
      ;;

    sharkfin)  # Fig 4
      if [ "$FULL" = 1 ]; then
        python3 "$EXP/13_nicolas_ambiguity/theorem4.py" --out "$WORK" --resample
      else
        python3 "$EXP/13_nicolas_ambiguity/theorem4.py" --out "$WORK"
      fi
      cp "$WORK/sharkfin.pdf" "$OUT/fig4_sharkfin.pdf"
      ;;

    ksweep)  # Fig 6
      if [ "$FULL" = 1 ]; then
        python3 "$EXP/16_ta_vs_tre_2/exp16_ksweep.py" --results "$WORK" --out "$WORK" --resample
      else
        python3 "$EXP/16_ta_vs_tre_2/exp16_ksweep.py" --out "$WORK"
      fi
      cp "$WORK/exp16_ksweep_v8_k8.pdf" "$OUT/fig6_ksweep.pdf"
      ;;

    maxent)  # Fig 7
      if [ "$FULL" = 1 ]; then
        python3 "$EXP/15_moment_control_qest23_redo/exp15_maxent_triangle.py" --out "$WORK" --resample
      else
        python3 "$EXP/15_moment_control_qest23_redo/exp15_maxent_triangle.py" --out "$WORK"
      fi
      cp "$WORK/exp15_maxent_triangle.pdf" "$OUT/fig7_maxent.pdf"
      ;;

    deltasigma)  # Fig 9 (exact volume, no fast/full distinction)
      python3 "$EXP/make_delta_sigma_fig.py" --out "$WORK"
      cp "$WORK/08_delta_sigma_nicolas_n_10.pdf"           "$OUT/fig9a_deltasigma.pdf"
      cp "$WORK/08b_delta_sigma_nicolas_fat_thin_n_10.pdf" "$OUT/fig9b_deltasigma.pdf"
      cp "$WORK/08c_delta_sigma_thao_n_10.pdf"             "$OUT/fig9c_deltasigma.pdf"
      ;;
  esac
done

echo
echo "Figures written to $OUT (figN_* deliverables; raw output in $WORK)."
