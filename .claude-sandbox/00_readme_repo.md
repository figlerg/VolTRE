# VolTRE MQTT Case Study — Project History

This file is the canonical trace of everything tried, what worked, and what failed.
Point a new instance here (and to `experiments/paper_experiments/10_mqtt_fuzzing/`)
to resume without needing the full conversation history.

---

## What this project is

A case study for a **tool paper on VolTRE** — a uniform sampler for Timed Regular
Expressions (TREs). The case study must show that VolTRE finds a real, nontrivial bug in
a real MQTT broker implementation, where the bug has a genuine tie to event ordering
and/or timing.

The repo root is `/workspace`. VolTRE is used via:
```python
from parse.quickparse import quickparse   # parse TRE spec string
from volume.slice_volume import slice_volume  # compute language volume at n
from sample.sample import sample              # draw one uniform timed word at n
```

---

## Files in this directory

| File | What it is |
|---|---|
| `00_readme_repo.md` | This file — project history and state |
| `01_initial_prompt.md` | The original Claude prompt that kicked off this work |
| `02_candidate_bugs.md` | AI-generated list of MQTT bugs suitable for TRE fuzzing |
| `03_mosquitto_setup.md` | Step-by-step instructions to extract and run Mosquitto 2.0.15 without root |
| `04_clock_jump_spec.md` | Full spec for the next case study: NTP clock-jump eviction (Mosquitto ≤ 2.0.21) |

---

## Iteration history

### Attempt 1 — Vibe-coded notebook (abandoned)
**Commit:** `a298c16`  
**What we did:** First pass at the full pipeline — TRE spec, VolTRE sampling, MQTT harness,
broker setup. Used Docker for Mosquitto, then discovered Docker-in-Docker is impossible in
this container (no socket). Pivoted to extracting Mosquitto 2.0.15 directly from the
Debian `.deb` archive using `dpkg -x`. Created a stub `libdlt.so.2` with `lief` to satisfy
a missing shared-library dependency.  
**Why abandoned:** Too much was done at once without a clean structure. User asked to
commit the state and restart from scratch with a clearer, step-by-step notebook.

---

### Attempt 2 — Clean notebook, tailored spec (superseded)
**Commit:** `ba59b21`  
**What we did:** Clean 7-cell notebook demonstrating CVE-2023-28366 in Mosquitto 2.0.15.

TRE spec used:
```
<CONNECT.PUBLISH.<PUBLISH*>_[0,30].PUBREL.DISCONNECT>_[0,60]
```

Confirmed the CVE two ways:
1. **Protocol conformance**: sent 4 consecutive PUBLISH(same msgid) → all got PUBREC (broker
   never disconnected). Fixed version (2.0.16) disconnects after the 2nd duplicate.
2. **Memory growth**: flooded broker with duplicate PUBLISHes, client receive buffer set to
   256 bytes (forces broker buffering). RSS grew at ~78 bytes/PUBLISH after TCP buffers
   saturated (~275K packets). Linear fit confirmed.

**Why superseded — user's 3 critiques:**
1. *Spec too tailored*: `PUBLISH*` looks like we already knew the bug. Spec should model
   legitimate protocol behaviour, not specifically the triggering pattern.
2. *Timing is redundant*: this CVE can be found with regex sampling alone (no timing
   needed). The spec should incorporate timing constraints that are genuinely necessary.
3. *n scaling*: growing n leads to VolTRE slowdowns (n=8 takes ~3 s/sample, n=10 takes
   ~10 s/sample). Must cap n ≤ 7.

---

### Attempt 3 — Redesigned notebook, generic spec (current)
**Commit:** `3710dc7`  
**Notebook:** `experiments/paper_experiments/10_mqtt_fuzzing/10_mqtt_fuzzing.ipynb`

**New TRE spec (derived from MQTT 3.1.1, not from CVE knowledge):**
```
<CONNECT.<PINGREQ*>_[0,10].PUBLISH.<(PUBLISH+PINGREQ)*>_[0,15].PUBREL.<PINGREQ*>_[0,10].DISCONNECT>_[0,60]
```
Parameters:
- K = 10 s — keepalive window (MQTT §3.1.2.10)
- Δ = 15 s — retransmission timeout
- T = 60 s — session budget

**Key design choices:**
- PINGREQs appear in ALL three keepalive positions (before PUBLISH, during retransmission
  window, after PUBREL) — models a real compliant client, not just the retransmission phase
- The `(PUBLISH+PINGREQ)*` retransmission window mixes retransmissions with keepalive pings
- n capped at 7; sampling n uniform in {4,5,6,7} takes ~15 s for 60 traces

**Timing motivation (addresses critique #2):**  
Without the `[0,K]` and `[0,Δ]` bounds, the Kleene-star segments have *infinite* language
volume and cannot be sampled uniformly. The bounds make the language finite and measurable
— this is the fundamental reason TRE is needed (not regex). The bounds themselves encode
real protocol parameters, so they're not arbitrary. The conclusion section also notes that
this approach extends naturally to *timing-sensitive* bugs (the clock-jump case study below)
where timing IS necessary to trigger the bug at all.

**Expected experiment outcome:**
Among 60 uniformly sampled traces, ~8–15% have 3+ PUBLISH events (CVE trigger). These are
replayed against Mosquitto 2.0.15, which returns PUBREC for all duplicates instead of
disconnecting. The direct conformance test (send 4 PUBLISHes, observe 4 PUBRECs) also
confirms the CVE. Memory flood shows ~78 B/PUBLISH linear growth.

**Setup notes:**
- Mosquitto 2.0.15 binary: `/tmp/mosquitto-pkg/mosquitto-extracted/usr/sbin/mosquitto`
- Libraries: `/tmp/mosquitto-pkg/mosquitto-extracted/usr/lib/x86_64-linux-gnu:...:/tmp/mosquitto-pkg`
- Config: `/tmp/mosq_exp.conf` (port 18830, allow_anonymous, no logging)
- Git write workaround (`.git/objects/` is root-owned): `GIT_OBJECT_DIRECTORY=/workspace/.git/claude-objects git <cmd>`
- Full reproduction steps: `03_mosquitto_setup.md`

---

## Next: Attempt 4 — Clock-jump eviction case study (not yet implemented)
**Spec:** `04_clock_jump_spec.md`  
**Target bug:** Mosquitto ≤ 2.0.21 uses real-time clock (`time()`) for keepalive timeouts.
A forward NTP jump of J seconds causes the broker to spuriously disconnect a live client.
Fixed in 2.0.22 by switching to `CLOCK_MONOTONIC`.

**Why this is better for timing motivation:** Unlike CVE-2023-28366, this bug CANNOT be
found by regex sampling alone — the trigger requires a specific timing relationship between
the last keepalive packet and the clock jump. TRE sampling across the full `[0, K]` window
naturally covers the narrow triggering band.

**TRE spec:**
```
<CONNECT.<PINGREQ*>_[0,10].CLOCK_JUMP.<PINGREQ*>_[0,10].DISCONNECT>_[0,60]
```

**Key implementation questions to resolve:**
1. How to manipulate the system clock without root? Options: `libfaketime` via `LD_PRELOAD`,
   or Linux time namespaces (`unshare --time`). See `04_clock_jump_spec.md` §Implementation.
2. Need Mosquitto 2.0.21 `.deb` from Debian snapshot. Same extraction process as 2.0.15.
3. `CLOCK_JUMP` is an out-of-band harness action (not an MQTT packet). The harness needs
   an extension to execute it mid-trace.

---

## Infrastructure notes (for new instances)

### VolTRE performance
| n | approx. time/sample |
|---|---|
| 4 | 0.2 s |
| 5 | 0.3 s |
| 6 | 0.4 s |
| 7 | 0.5 s |
| 8 | ~3 s  |
| 9+ | very slow |

**Hard limit: n ≤ 7** for interactive/notebook use.

### Mosquitto 2.0.15 — CVE trigger logic
- 1 PUBLISH (original): OK
- 2 PUBLISHes (1st dup): OK per spec (allowed retransmission)
- 3+ PUBLISHes (2nd+ dup): CVE trigger — 2.0.15 sends PUBREC; 2.0.16 disconnects

### Git workflow
The `.git/objects/` subdirectories are root-owned. Every git command must use:
```bash
GIT_OBJECT_DIRECTORY=/workspace/.git/claude-objects git <cmd>
```

### Key commits
| Hash | Description |
|---|---|
| `a298c16` | First vibe-coded attempt (abandoned) |
| `ba59b21` | Clean notebook, tailored spec (superseded) |
| `3710dc7` | Redesigned notebook: generic spec + keepalive + bounded n (current) |
