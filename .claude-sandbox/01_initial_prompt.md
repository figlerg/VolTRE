# MQTT Broker Fuzzing with Timed Regular Expressions — Claude Code Prompt

## Context

This project implements a case study for a tool paper on **uniform sampling of Timed Regular Expressions (TRE)**. The sampler produces `TimedWord` objects — sequences of (delay, symbol) pairs — drawn uniformly at random from the language of a TRE spec. The goal here is to use this sampler as a **timed fuzzing engine** targeting MQTT broker implementations, specifically looking for bugs triggered by the *ordering and timing* of valid protocol messages rather than malformed packet content.

The primary target bug class is **CVE-2023-28366** (Mosquitto ≤2.0.15): sending unacknowledged QoS 2 messages with duplicate message IDs causes a memory leak. This is a sequence/ordering bug, not a content bug — making it a natural fit for TRE-based fuzzing.

---

## TimedWord Interface

The sampler produces `TimedWord` objects. Extend or wrap this as needed. The structure is:

```python
class TimedWord:
    """
    A timed word is a sequence of (delay, symbol) pairs.
    delay: float — time in seconds to wait before sending this symbol
    symbol: str — event name, e.g. "PUBLISH", "PUBREC", etc.
    """
    def __init__(self, pairs: list[tuple[float, str]]):
        self.pairs = pairs  # list of (delay, symbol)

    def __iter__(self):
        return iter(self.pairs)
```

For now, if the sampler is not available, implement a **stub** that generates random timed words over the MQTT alphabet consistent with the TRE spec below. This stub will be replaced with the real sampler later.

---

## TRE Spec

The fuzzing target is the MQTT QoS 2 flow with keepalive interleaving. The informal TRE spec (using the project's syntax) is:

```
CONNECT.
PUBLISH.
(CONNECT + PUBLISH + PUBREC + PUBREL + PUBCOMP + PINGREQ + PINGRESP + DISCONNECT)*_[0,T].
PUBREC.
(CONNECT + PUBLISH + PUBREC + PUBREL + PUBCOMP + PINGREQ + PINGRESP + DISCONNECT)*_[0,T].
PUBREL.
(CONNECT + PUBLISH + PUBREC + PUBREL + PUBCOMP + PINGREQ + PINGRESP + DISCONNECT)*_[0,T].
PUBCOMP.
(CONNECT + PUBLISH + PUBREC + PUBREL + PUBCOMP + PINGREQ + PINGRESP + DISCONNECT)*_[0,T].
DISCONNECT
```

Where T is the keepalive interval (default: 10 seconds). The Sigma* gaps between handshake steps allow arbitrary valid events — including a second PUBLISH with the same message ID before PUBREL, which is the CVE-2023-28366 trigger pattern.

The alphabet is:
- `CONNECT` — open session
- `PUBLISH` — send message (QoS 2, fixed message id=1)
- `PUBREC` — broker acknowledges PUBLISH (client receives this; in replay, simulate it or wait for it)
- `PUBREL` — client releases message
- `PUBCOMP` — broker confirms completion (client receives)
- `PINGREQ` — keepalive ping from client
- `PINGRESP` — broker pong (client receives)
- `DISCONNECT` — close session

Note: PUBREC, PUBCOMP, PINGRESP are broker responses, not client-initiated. In the fuzzing harness, treat them as expected responses and either wait for them with a timeout or skip them depending on mode (see below).

---

## Infrastructure: Docker Setup

Spin up a **vulnerable Mosquitto instance** (version 2.0.15, which has CVE-2023-28366) using Docker:

```bash
docker pull eclipse-mosquitto:2.0.15
```

The harness should:
1. Start the container programmatically (via `subprocess` or `docker` Python SDK)
2. Expose port 1883
3. Be able to **restart the broker cleanly** between fuzzing runs to reset state
4. Expose the broker's **PID** or container stats for memory monitoring

Use a minimal mosquitto config:
```
listener 1883
allow_anonymous true
```

Provide a `docker-compose.yml` or a helper function `start_broker() -> container` and `stop_broker(container)`.

---

## Replay Harness

Implement a function:

```python
def replay(timed_word: TimedWord, host="localhost", port=1883, timeout=5.0) -> ReplayResult:
    ...
```

Using `paho-mqtt` for packet construction. The harness should:

- For each `(delay, symbol)` in the timed word, `time.sleep(delay)` then send the corresponding packet
- Client-initiated symbols (CONNECT, PUBLISH, PUBREL, PINGREQ, DISCONNECT) are sent directly
- Broker-response symbols (PUBREC, PUBCOMP, PINGRESP) in the timed word are treated as "expect this response" — wait up to `timeout` seconds, record whether it arrived
- Use a **fixed message ID** (e.g. id=1) for all QoS 2 packets
- Record the full interaction log with timestamps

```python
@dataclass
class ReplayResult:
    timed_word: TimedWord
    interaction_log: list[tuple[float, str]]  # (timestamp, event)
    broker_responded: bool
    exception: Exception | None
```

---

## Bug Detection

### Memory Leak Detection (CVE-2023-28366)

The key insight: run the *same trace* (or a bug-triggering pattern) **repeatedly** and watch broker memory grow monotonically.

Implement:

```python
def check_memory_leak(
    timed_word: TimedWord,
    repetitions: int = 50,
    poll_interval: float = 1.0
) -> MemoryLeakResult:
    ...
```

- Poll the broker container's memory every `poll_interval` seconds via `docker stats` or `/proc/{pid}/status` (VmRSS)
- Replay the timed word `repetitions` times in a loop
- Fit a linear regression to the memory-over-time series
- Flag as a leak if slope > threshold (e.g. > 100KB/s sustained)
- Return the memory series and the slope

```python
@dataclass  
class MemoryLeakResult:
    timed_word: TimedWord
    memory_series: list[tuple[float, int]]  # (timestamp, bytes)
    slope_bytes_per_second: float
    is_leak: bool
```

### Crash Detection

Wrap every replay in a try/except and also check whether the broker process is still alive after each trace. Flag any trace that causes the broker to exit unexpectedly.

### Hang / Timeout Detection

If the broker stops responding to PINGREQ within keepalive bounds, flag it. This catches denial-of-service type bugs.

### Spec Violation Detection (stretch goal)

After replaying a trace, check whether the broker's responses conform to the MQTT spec. For example: did PUBREC arrive after PUBLISH? Did PUBCOMP arrive after PUBREL? Any deviation is a non-compliance bug. This is what MBFuzzer calls "non-compliance bugs."

---

## Main Fuzzing Loop

```python
def fuzz(
    n_traces: int = 200,
    repetitions_per_trace: int = 50,
    keepalive_T: float = 10.0
):
    results = []
    for i in range(n_traces):
        word = sample_from_tre(keepalive_T)  # stub or real sampler
        replay_result = replay(word)
        leak_result = check_memory_leak(word, repetitions=repetitions_per_trace)
        crash = not broker_alive()
        results.append({
            "trace_id": i,
            "word": word,
            "replay": replay_result,
            "leak": leak_result,
            "crash": crash
        })
        restart_broker()  # clean state for next trace
    report(results)
```

---

## Output / Report

At the end of the fuzzing session, produce:

1. A summary table: trace ID, length, detected bug types
2. For any leaking trace: a memory-over-time plot (matplotlib)
3. The exact `TimedWord` that triggered each bug — this is the "witness trace" for the paper
4. Comparison: which traces contain the CVE-2023-28366 pattern (PUBLISH → PUBREC → PUBLISH before PUBREL) vs which don't — does the leak correlate?

---

## Open Questions (to resolve with domain expert)

These are open questions to discuss with a security/protocol expert before finalizing the case study:

1. **Are there other ordering-based bug patterns in MQTT beyond CVE-2023-28366?** Specifically in QoS 1 flows, session resumption, or retained message handling?

2. **Is the Sigma* between handshake steps the right place to look, or are there other protocol phases with known timing sensitivity?**

3. **How does the broker handle a CONNECT arriving mid-session?** (It appears in Sigma* in our spec — is this a known dangerous pattern?)

4. **Is Mosquitto the right target, or is there a broker with more timing-sensitive bugs?** NanoMQ and EMQX are alternatives.

5. **Is memory leak the most convincing bug class for a tool paper, or would a crash or non-compliance bug be stronger?**

6. **How does this relate to existing MQTT fuzzers (FUME, MBFuzzer)?** Can we show on the same broker versions that those tools miss the timing-triggered bugs?

---

## Dependencies

```
paho-mqtt
docker
matplotlib
scipy  # for linear regression on memory series
dataclasses
```

Mosquitto Docker image: `eclipse-mosquitto:2.0.15`
