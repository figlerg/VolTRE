#!/usr/bin/env bash
# Installation smoke test (about a minute): verifies that VolTRE is importable,
# can parse a TRE, compute a volume, and sample uniformly; also checks for the
# optional wordgen binary.
set -eu

python3 - <<'EOF'
import random
import numpy as np
random.seed(42); np.random.seed(42)

from parse.quickparse import quickparse
from volume.slice_volume import slice_volume
from sample.sample import sample

phi = quickparse('<a>_[0,1] *', string=True)
v = slice_volume(phi, 3)
print('volume V_3 computed:', v)
for _ in range(3):
    print('sampled:', sample(phi, 3))
print('VolTRE smoke test OK')
EOF

WG="${WORDGEN_BIN:-/tmp/wordgen_build/_build/default/src/wordgen.exe}"
if [ -x "$WG" ] || command -v wordgen >/dev/null 2>&1; then
    echo "wordgen binary found (full mode of the ksweep figure available)"
else
    echo "wordgen binary NOT found (optional; only needed for './reproduce.sh ksweep --full')"
fi
echo "Smoke test passed."
