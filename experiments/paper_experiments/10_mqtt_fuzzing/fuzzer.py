"""
Main fuzzing loop.

Usage:
    python fuzzer.py [--traces N] [--reps R] [--n-min M] [--n-max X]
                     [--spec SPECFILE] [--port PORT] [--seed SEED]
"""

import argparse
import json
import os
import sys
import time
import random

# ── path setup ────────────────────────────────────────────────────────────────
_REPO = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

import sampler as S
from broker  import managed_broker, BrokerThread
from harness import replay, ReplayResult
from detect  import check_conformance, broker_alive, check_memory_leak


# ── fuzz result ───────────────────────────────────────────────────────────────

class FuzzResult:
    def __init__(self, trace_id, word, replay_result, conformance, memory,
                 broker_alive_after):
        self.trace_id          = trace_id
        self.word              = word
        self.replay_result     = replay_result
        self.conformance       = conformance
        self.memory            = memory
        self.broker_alive_after = broker_alive_after

    @property
    def has_bug(self) -> bool:
        return (not self.conformance.is_compliant or
                self.memory.is_leak or
                not self.broker_alive_after)

    def to_dict(self) -> dict:
        return {
            "trace_id":     self.trace_id,
            "n":            self.word.length,
            "word":         str(self.word),
            "dup_publish":  S.has_duplicate_publish(self.word),
            "violations":   self.conformance.violations,
            "exception":    repr(self.conformance.exception) if self.conformance.exception else None,
            "completed":    self.conformance.completed,
            "memory_slope": round(self.memory.slope_bytes_per_rep, 1),
            "memory_r2":    round(self.memory.r_squared, 3),
            "is_leak":      self.memory.is_leak,
            "broker_alive": self.broker_alive_after,
            "has_bug":      self.has_bug,
        }


# ── main fuzz loop ────────────────────────────────────────────────────────────

def fuzz(
    spec_name:   str   = "mqtt_qos2.tre",
    n_traces:    int   = 50,
    reps:        int   = 20,
    n_min:       int   = 4,
    n_max:       int   = 7,
    port:        int   = 18830,
    seed:        int   = None,
    output_json: str   = None,
    verbose:     bool  = True,
) -> list:

    if seed is not None:
        random.seed(seed)

    spec = S.load_spec(spec_name)

    results = []

    with managed_broker(port=port) as broker:
        time.sleep(0.5)   # give broker a moment to fully initialise

        for i in range(n_traces):
            n = random.randint(n_min, n_max)

            # ── sample ────────────────────────────────────────────────────────
            try:
                word = S.sample_word(spec, n=n)
            except Exception as exc:
                if verbose:
                    print(f"[{i:3d}] SAMPLE ERROR: {exc}")
                continue

            if not S.verify_word(word, spec):
                if verbose:
                    print(f"[{i:3d}] SAMPLER BUG: word not in language: {word}")
                # record as finding but continue
                results.append(FuzzResult(
                    i, word,
                    ReplayResult(timed_word=word),
                    type("C", (), {"is_compliant": False,
                                   "violations": ["SAMPLER_BUG: word not in language"],
                                   "exception": None, "completed": False})(),
                    type("M", (), {"is_leak": False,
                                   "slope_bytes_per_rep": 0,
                                   "r_squared": 0})(),
                    True,
                ))
                continue

            dup = S.has_duplicate_publish(word)
            if verbose:
                tag = " [DUP-PUBLISH]" if dup else ""
                print(f"[{i:3d}] n={n}{tag}  {word}")

            # ── single replay for conformance ─────────────────────────────────
            rr = replay(word, port=port)
            conf = check_conformance(rr)

            # ── memory leak check (repeated replay) ───────────────────────────
            def do_replay(w):
                replay(w, port=port)

            mem = check_memory_leak(do_replay, word, broker, repetitions=reps)

            alive = broker_alive(port=port)

            fr = FuzzResult(i, word, rr, conf, mem, alive)
            results.append(fr)

            if verbose:
                status = "BUG" if fr.has_bug else "ok"
                print(f"       {status}  conf={conf.summary()}  {mem.summary()}")

            if not alive:
                if verbose:
                    print("       BROKER CRASHED — restarting")
                broker.restart()
                time.sleep(0.5)

    return results


# ── report ────────────────────────────────────────────────────────────────────

def report(results: list) -> None:
    bugs = [r for r in results if r.has_bug]
    leaks = [r for r in results if r.memory.is_leak]
    viols = [r for r in results if r.conformance.violations]
    crashes = [r for r in results if not r.broker_alive_after]
    dup_pub = [r for r in results if S.has_duplicate_publish(r.word)]

    print()
    print("═" * 60)
    print(f"  Fuzzing report — {len(results)} traces")
    print("═" * 60)
    print(f"  Bugs found:            {len(bugs)}")
    print(f"  Conformance violations:{len(viols)}")
    print(f"  Memory leaks:          {len(leaks)}")
    print(f"  Broker crashes:        {len(crashes)}")
    print(f"  Traces with dup PUBLISH before PUBREL: {len(dup_pub)}")
    print()

    if bugs:
        print("  ── Witness traces ──")
        for r in bugs[:10]:
            print(f"    [{r.trace_id:3d}] n={r.word.length}  {r.word}")
            if r.conformance.violations:
                for v in r.conformance.violations:
                    print(f"         violation: {v}")
            if r.memory.is_leak:
                print(f"         leak: slope={r.memory.slope_bytes_per_rep/1024:.1f} KB/rep  R²={r.memory.r_squared:.3f}")

    print("═" * 60)


# ── CLI ───────────────────────────────────────────────────────────────────────

def _parse_args():
    p = argparse.ArgumentParser(description="VolTRE MQTT fuzzer")
    p.add_argument("--traces", type=int, default=50)
    p.add_argument("--reps",   type=int, default=20,
                   help="repetitions per trace for leak detection")
    p.add_argument("--n-min",  type=int, default=4)
    p.add_argument("--n-max",  type=int, default=7)
    p.add_argument("--spec",   type=str, default="mqtt_qos2.tre")
    p.add_argument("--port",   type=int, default=18830)
    p.add_argument("--seed",   type=int, default=42)
    p.add_argument("--output", type=str, default=None,
                   help="Write results to JSON file")
    return p.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    results = fuzz(
        spec_name=args.spec,
        n_traces=args.traces,
        reps=args.reps,
        n_min=args.n_min,
        n_max=args.n_max,
        port=args.port,
        seed=args.seed,
    )
    report(results)

    if args.output:
        with open(args.output, "w") as f:
            json.dump([r.to_dict() for r in results], f, indent=2)
        print(f"  Results saved to {args.output}")
