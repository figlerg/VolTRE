#!/usr/bin/env bash
# Setup script for experiment 10: MQTT protocol fuzzing with VolTRE.
# No root, no Docker required — uses amqtt (pure Python broker).
#
# Run from this directory:
#   bash setup.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

echo "=== VolTRE MQTT Fuzzing — Setup ==="
echo "Repo root: $REPO_ROOT"

# ── Python dependencies ───────────────────────────────────────────────────────
echo
echo "Installing Python dependencies..."
pip install --quiet \
  "antlr4-python3-runtime==4.13.1" \
  sympy numpy scipy matplotlib networkx tqdm \
  paho-mqtt amqtt psutil
echo "Done."

# ── VolTRE self-check ─────────────────────────────────────────────────────────
echo
echo "Checking VolTRE..."
python3 - <<EOF
import sys
sys.path.insert(0, "$REPO_ROOT")
from parse.quickparse import quickparse
from sample.sample import sample
from volume.slice_volume import slice_volume
from match.match import match
print("  imports OK")
EOF

# ── quick sample from the MQTT spec ──────────────────────────────────────────
echo
echo "Quick sample from spec_10_mqtt_qos2.tre..."
python3 - <<EOF
import sys
sys.path.insert(0, "$REPO_ROOT")
sys.path.insert(0, "$SCRIPT_DIR")
import sampler as S
spec = S.load_spec('spec_10_mqtt_qos2.tre')
w = S.sample_word(spec, n=5)
assert S.verify_word(w, spec), "Sampled word not in language!"
print(f"  sample: {w}")
print("  verification: OK")
EOF

echo
echo "=== Setup complete ==="
echo
echo "Run the notebook:"
echo "  jupyter notebook 10_mqtt_fuzzing.ipynb"
echo
echo "Or the command-line fuzzer:"
echo "  python fuzzer.py --traces 50 --spec spec_10_mqtt_qos2.tre"
echo "  python fuzzer.py --traces 50 --spec spec_10_mqtt_qos2_aggressive.tre"
