# MQTT QoS-2 Case Study — Reproduction Setup

This file documents every step needed to reproduce the case study in `10_mqtt_fuzzing.ipynb`
from a fresh Docker container.

## Prerequisites

- Python 3.10+ with the project virtual environment activated (`source .venv/bin/activate`)
- `lief` Python package: `pip install lief`
- Internet access (one-time download of Mosquitto 2.0.15 packages)

## 1 — Extract Mosquitto 2.0.15

Mosquitto 2.0.15 is run without root and without Docker using the Debian package directly.

```bash
mkdir -p /tmp/mosquitto-pkg && cd /tmp/mosquitto-pkg

# Download Mosquitto 2.0.15 and its dependencies from Debian snapshot archive
SNAP=https://snapshot.debian.org/archive/debian/20231015T093922Z/pool/main
wget -q "$SNAP/m/mosquitto/mosquitto_2.0.15-1_amd64.deb"
wget -q "$SNAP/m/mosquitto/libmosquitto1_2.0.15-1_amd64.deb"
wget -q "$SNAP/libn/libnsl/libnsl2_1.3.0-2_amd64.deb"
wget -q "$SNAP/libt/libtirpc/libtirpc3_1.3.3+ds-1_amd64.deb"
wget -q "$SNAP/t/tcp-wrappers/libwrap0_7.6.q-32_amd64.deb"

# Extract all packages
for deb in *.deb; do dpkg -x "$deb" mosquitto-extracted/; done
```

## 2 — Create the libdlt stub

Mosquitto depends on `libdlt.so.2` (DLT — Diagnostic Log and Trace), which is not in
the Debian snapshot. We create a minimal stub using `lief`:

```python
import lief, struct

# Use libcap.so.2 as a template (same ABI style, available system-wide)
lib = lief.parse('/lib/x86_64-linux-gnu/libcap.so.2')
lib.name = 'libdlt.so.2'

# Add the three symbols Mosquitto actually calls
for sym_name in ['dlt_register_app', 'dlt_register_context', 'dlt_unregister_app']:
    sym = lief.ELF.Symbol()
    sym.name = sym_name
    sym.type = lief.ELF.Symbol.TYPE.FUNC
    sym.binding = lief.ELF.Symbol.BINDING.GLOBAL
    sym.value = 0
    lib.add_exported_function(0, sym_name)

lib.write('/tmp/mosquitto-pkg/libdlt.so.2')
```

Save the above as `make_stub.py` and run `python3 make_stub.py`.

## 3 — Write the Mosquitto config

```bash
cat > /tmp/mosq_exp.conf << 'EOF'
listener 18830 127.0.0.1
allow_anonymous true
log_type none
EOF
```

## 4 — Run Mosquitto 2.0.15

```bash
export LD_LIBRARY_PATH=/tmp/mosquitto-pkg/mosquitto-extracted/usr/lib/x86_64-linux-gnu:/tmp/mosquitto-pkg/mosquitto-extracted/lib/x86_64-linux-gnu:/tmp/mosquitto-pkg
/tmp/mosquitto-pkg/mosquitto-extracted/usr/sbin/mosquitto -c /tmp/mosq_exp.conf &
```

Verify: `cat /proc/$!/status | grep VmRSS` should show ~8 MB.

## 5 — Git write workaround

The `.git/objects/` subdirectories are root-owned in this container.
All git commands must use an alternate object store:

```bash
export GIT_OBJECT_DIRECTORY=/workspace/.git/claude-objects
git -c core.alternatesFile=<(echo /workspace/.git/objects) \
    commit -m "..."
```

Or equivalently:

```bash
GIT_OBJECT_DIRECTORY=/workspace/.git/claude-objects git log
```

## 6 — Run the notebook

```bash
cd /workspace
jupyter notebook experiments/paper_experiments/10_mqtt_fuzzing/10_mqtt_fuzzing.ipynb
```

Run all cells in order. Each cell is self-contained; the broker cell (Cell 4) must
complete before the conformance and memory cells.

## Key paths

| Resource | Path |
|---|---|
| Mosquitto 2.0.15 binary | `/tmp/mosquitto-pkg/mosquitto-extracted/usr/sbin/mosquitto` |
| Mosquitto libraries | `/tmp/mosquitto-pkg/mosquitto-extracted/usr/lib/x86_64-linux-gnu/` |
| libdlt stub | `/tmp/mosquitto-pkg/libdlt.so.2` |
| Config file | `/tmp/mosq_exp.conf` |
| Broker port | `18830` (local only) |

## Known issues

- `/tmp/mosquitto.conf` may be root-owned (from a previous session). Use `/tmp/mosq_exp.conf` instead.
- If port 18830 is in use, kill the old process: `pkill -f usr/sbin/mosquitto`
- VolTRE sampling slows significantly for n ≥ 8. The notebook uses n ∈ {4,5,6,7}.
