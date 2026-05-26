"""
Bug detection: memory-leak analysis, crash detection, and conformance scoring.
"""

import time
import statistics
from dataclasses import dataclass, field
from typing import Optional

import psutil


# ── memory leak ───────────────────────────────────────────────────────────────

@dataclass
class MemoryLeakResult:
    memory_series: list = field(default_factory=list)   # list[(timestamp_s, rss_bytes)]
    slope_bytes_per_rep: float = 0.0
    r_squared: float = 0.0
    is_leak: bool = False
    threshold_bytes: int = 4096     # 4 KB per repetition is suspicious

    def summary(self) -> str:
        status = "LEAK" if self.is_leak else "OK"
        return (f"MemoryLeak({status}  slope={self.slope_bytes_per_rep/1024:.1f} KB/rep  "
                f"R²={self.r_squared:.3f}  n_samples={len(self.memory_series)})")


def check_memory_leak(
    replay_fn,
    timed_word,
    broker,
    repetitions: int = 30,
    poll_fn=None,
) -> MemoryLeakResult:
    """
    Replay *timed_word* *repetitions* times while sampling broker RSS.
    Fits a linear regression y = slope * rep + intercept to the RSS samples.
    Flags as leak if slope > threshold_bytes / rep.

    poll_fn: optional callable() → int for RSS; defaults to broker.memory_rss.
    """
    result = MemoryLeakResult()
    get_mem = poll_fn if poll_fn else (lambda: broker.memory_rss)

    for rep in range(repetitions):
        mem_before = get_mem()
        replay_fn(timed_word)
        mem_after  = get_mem()
        result.memory_series.append((rep, mem_after))

    reps = [r for r, _ in result.memory_series]
    mems = [m for _, m in result.memory_series]

    slope, intercept, r2 = _linear_regression(reps, mems)
    result.slope_bytes_per_rep = slope
    result.r_squared = r2
    result.is_leak = slope > result.threshold_bytes and r2 > 0.7

    return result


def _linear_regression(xs, ys):
    n = len(xs)
    if n < 2:
        return 0.0, 0.0, 0.0
    xm = sum(xs) / n
    ym = sum(ys) / n
    ss_xx = sum((x - xm) ** 2 for x in xs)
    ss_xy = sum((x - xm) * (y - ym) for x, y in zip(xs, ys))
    if ss_xx == 0:
        return 0.0, ym, 0.0
    slope = ss_xy / ss_xx
    intercept = ym - slope * xm
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - ym) ** 2 for y in ys)
    r2 = 1.0 - ss_res / ss_tot if ss_tot else 1.0
    return slope, intercept, r2


# ── conformance scoring ────────────────────────────────────────────────────────

@dataclass
class ConformanceResult:
    violations: list = field(default_factory=list)
    exception: Optional[Exception] = None
    completed: bool = False

    @property
    def is_compliant(self) -> bool:
        return self.completed and not self.violations and self.exception is None

    def summary(self) -> str:
        status = "COMPLIANT" if self.is_compliant else "NON-COMPLIANT"
        viols  = "; ".join(self.violations) if self.violations else "none"
        return f"Conformance({status}  violations=[{viols}])"


def check_conformance(replay_result) -> ConformanceResult:
    """
    Derive a ConformanceResult from a harness ReplayResult.
    """
    r = ConformanceResult(
        violations = list(replay_result.conformance_violations),
        exception  = replay_result.exception,
        completed  = replay_result.completed,
    )
    return r


# ── crash / liveness ──────────────────────────────────────────────────────────

def broker_alive(host: str = "127.0.0.1", port: int = 18830,
                 timeout: float = 2.0) -> bool:
    """
    Check that the broker is still accepting connections.
    Sends a CONNECT and checks for CONNACK.
    """
    import socket
    from mqtt_codec import make_connect, recv_packet, PT_CONNACK
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            s.settimeout(timeout)
            s.sendall(make_connect())
            pkt = recv_packet(s)
            return pkt.ptype == PT_CONNACK
    except Exception:
        return False
