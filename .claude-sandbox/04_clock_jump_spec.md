# Case Study: Spurious Disconnection via NTP Clock Jump (Mosquitto ≤ 2.0.21)

## The Bug

Mosquitto ≤ 2.0.21 used `time()` (real-time clock) to evaluate keepalive timeouts.
When the system clock jumps forward — e.g., due to NTP synchronisation or VM clock
adjustment — the broker computes that more time has elapsed than actually has, and
spuriously disconnects a live, well-behaved client.

**Fixed in Mosquitto 2.0.22** (switch to `CLOCK_MONOTONIC` via `mosquitto_time()` wrapper).
GitHub issue: https://github.com/eclipse/mosquitto/issues/3238

### Root cause (code level)

In `src/keepalive.c` (≤ 2.0.21), the timeout check is approximately:

```c
if (time(NULL) - context->last_msg_in > context->keepalive * 3 / 2) {
    // disconnect
}
```

`time(NULL)` returns the wall-clock (real-time) second. A forward NTP jump of `J` seconds
makes `time(NULL)` jump by `J`, instantly aging the client by `J` extra seconds in the
broker's view. If `J > keepalive * 1.5 - (time_since_last_packet)`, the broker fires the
timeout and drops the connection.

The fix replaces `time(NULL)` with `mosquitto_time()` which reads `CLOCK_MONOTONIC`, immune
to NTP adjustments.

---

## TRE Specification

The event alphabet for this experiment:

| Symbol | Meaning |
|---|---|
| `CONNECT` | Client sends MQTT CONNECT (client-side event) |
| `PINGREQ` | Client sends MQTT PINGREQ keepalive |
| `CLOCK_JUMP` | System real-time clock is advanced by J seconds (external event) |
| `DISCONNECT` | Client sends MQTT DISCONNECT |

The bug is triggered by traces of the form:

```
CONNECT · PINGREQ · [gap < K] · CLOCK_JUMP(J) · [PINGREQ within real K] · ...
```

where after `CLOCK_JUMP`, the broker's internal elapsed time exceeds `1.5 · K`.

### TRE spec

```
φ = ⟨ CONNECT
       · ⟨PINGREQ*⟩_[0, K]      -- keepalive pings while active; real time stays < 1.5K
       · CLOCK_JUMP              -- external clock event; broker's apparent gap jumps to > 1.5K
       · ⟨PINGREQ*⟩_[0, K]      -- client continues pinging, unaware of broker disconnect
       · DISCONNECT
     ⟩_[0, T]
```

with K = 10 (keepalive), T = 60 (session budget).

In VolTRE syntax:
```
<CONNECT.<PINGREQ*>_[0,10].CLOCK_JUMP.<PINGREQ*>_[0,10].DISCONNECT>_[0,60]
```

**Why timing is essential here (unlike CVE-2023-28366)**:

The bug only fires when the gap between the last PINGREQ and the CLOCK_JUMP is small
enough that without the jump the client would still be alive, but large enough that
`gap + J > 1.5 · K`. Specifically, if the last PINGREQ arrived at real time `t_last`,
a jump of `J` causes disconnect if:

```
J > 1.5 · K - (t_now - t_last)
```

A trace sampled from `φ` at n = 3 (CONNECT, CLOCK_JUMP, DISCONNECT) has the jump
immediately after CONNECT — trivially disconnects. At n = 4+ (with PINGREQ before the
jump), the window `(t_now - t_last)` is sampled uniformly from `[0, K]`, meaning the
required jump size `J` needed to trigger the bug varies across traces. TRE sampling
covers the full range of pre-jump timing — this is the sensitivity that makes TRE
necessary here.

---

## Implementation Plan

### 1 — Mosquitto version

Need Mosquitto **2.0.21** or earlier. The `.deb` can be fetched from the Debian snapshot
archive in the same way as 2.0.15 (see `SETUP.md`):

```
https://snapshot.debian.org/archive/debian/20230101T000000Z/pool/main/m/mosquitto/mosquitto_2.0.21-1_amd64.deb
```

(adjust snapshot date to one before the 2.0.22 release in late 2023)

### 2 — Clock manipulation without root

We cannot call `settimeofday()` without `CAP_SYS_TIME`. Two alternatives:

**Option A — libfaketime (recommended)**

`libfaketime` intercepts `time()`, `clock_gettime()`, `gettimeofday()` via `LD_PRELOAD`
and lets you set a fixed offset via an environment variable or a file:

```bash
# Install
pip install faketime  # Python wrapper
# or: apt-get install libfaketime (provides /usr/lib/x86_64-linux-gnu/faketime/libfaketime.so.1)

# Run Mosquitto with a +20s clock offset
FAKETIME="+20" LD_PRELOAD=/usr/lib/x86_64-linux-gnu/faketime/libfaketime.so.1 \
    LD_LIBRARY_PATH=... /tmp/mosquitto-pkg/.../mosquitto -c /tmp/mosq_exp.conf
```

To simulate a clock jump mid-run: write the new offset to `FAKETIME_DONT_RESET` file or
use `FAKETIME_TIMESTAMP_FILE` pointing to a temp file that the test harness updates.

**Option B — per-process virtual clock via `clock_settime` in a child namespace**

```bash
# Enter a new time namespace (Linux ≥ 5.6, requires unshare)
unshare --time python3 harness.py
# Inside the namespace, python ctypes can call clock_settime(CLOCK_REALTIME, ...)
# without affecting the host or other processes
```

Check with `unshare --time echo ok` — if it exits 0, this option is available.

### 3 — CLOCK_JUMP event in the harness

The `CLOCK_JUMP` symbol is not an MQTT packet; it is an **out-of-band** harness action.
In `harness.py`, add a handler for it:

```python
elif symbol == "CLOCK_JUMP":
    # Option A: update FAKETIME_TIMESTAMP_FILE with +J seconds
    jump_seconds = 20  # must exceed 1.5 * keepalive - elapsed
    new_offset = f"+{jump_seconds}"
    with open(os.environ['FAKETIME_TIMESTAMP_FILE'], 'w') as fh:
        fh.write(new_offset)
    time.sleep(0.1)   # let broker's next keepalive poll fire
```

The jump size `J = 20` works for keepalive = 10 (threshold = 15 s): any gap < 15 real
seconds + 20 s jump > 15 s.

### 4 — Conformance check

After the CLOCK_JUMP, the client sends the next PINGREQ. The broker's response reveals
the bug:

| Broker version | Response to PINGREQ after jump |
|---|---|
| ≤ 2.0.21 (buggy) | TCP connection reset / no response (broker already dropped it) |
| ≥ 2.0.22 (fixed) | PINGRESP (broker uses monotonic clock, connection still alive) |

Detection in the harness:

```python
try:
    s.sendall(make_pingreq())
    pkt = client.try_recv(timeout=2.0)
    if pkt is None or pkt.ptype != PT_PINGRESP:
        result.conformance_violations.append(
            "PINGREQ after clock jump got no PINGRESP — spurious disconnect (clock-jump bug)"
        )
except ConnectionResetError:
    result.conformance_violations.append("Connection reset after clock jump")
```

### 5 — Expected results

With `FAKETIME` and keepalive = 10 s, a trace like:

```
CONNECT (t=0)  → CONNACK
PINGREQ (t=5)  → PINGRESP
CLOCK_JUMP +20s at t=6  (broker now thinks t=26, last msg was at t=5 → 21s gap > 15s threshold)
PINGREQ (t=7)  → ??? (should be PINGRESP; buggy broker: no response / TCP reset)
DISCONNECT
```

Expected output on ≤ 2.0.21: `conformance_violations = ["Connection reset after clock jump"]`
Expected output on ≥ 2.0.22: `conformance_violations = []`

---

## What VolTRE Adds

Without TRE, you could just send `CONNECT → wait 16s → PINGREQ` (no jump needed) to
trigger a normal timeout — that tests nothing interesting. The clock-jump bug requires
a **specific timing relationship**: the gap before the jump must be within [0, K] (so
the connection is alive), and the jump must be large enough to push the apparent gap
past `1.5 · K`. TRE sampling with `⟨PINGREQ*⟩_[0,K] · CLOCK_JUMP` generates traces
across the full range of pre-jump timing, including the narrow band near `K` where the
required jump size is smallest and the bug is easiest to trigger.

A pure regex sampler (no timing) would either assign zero delays (gap = 0 always, jump
always triggers) or arbitrary fixed delays — neither reflects the uniform distribution
over feasible timing that characterises realistic client behaviour.
