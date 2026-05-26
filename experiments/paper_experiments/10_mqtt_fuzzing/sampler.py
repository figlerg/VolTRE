"""
VolTRE sampler interface for the MQTT fuzzing case study.

Wraps parse + sample so the fuzzer can call sample_from_spec(n) and get a
TimedWord drawn uniformly at random from the TRE language.
"""

import os
import sys

# make VolTRE importable regardless of working directory
_REPO = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

from parse.quickparse import quickparse
from sample.sample import sample, DurationSamplerMode
from match.match import match


# spec files live alongside the other experiment specs, one level up
_SPEC_DIR = os.path.join(os.path.dirname(__file__), "..")


def load_spec(name: str):
    """Load and parse a .tre file.  Pass the bare filename (e.g.
    'spec_10_mqtt_qos2.tre') or a full path."""
    if os.path.isabs(name) or os.sep in name:
        path = name
    else:
        path = os.path.join(_SPEC_DIR, name)
    return quickparse(path)


def sample_word(spec, n: int, seed: int = None):
    """
    Draw one timed word of length n from the TRE spec.
    Uses vanilla (uniform) mode.
    """
    import random
    if seed is not None:
        random.seed(seed)
    return sample(spec, n=n, mode=DurationSamplerMode.VANILLA)


def verify_word(word, spec) -> bool:
    """Return True if the word is in the language of spec."""
    return match(word, spec) > 0


def contains_pattern(word, *symbols) -> bool:
    """
    Return True if the word contains a sub-sequence matching the given symbols
    (in order, not necessarily contiguous).
    """
    syms = list(symbols)
    idx  = 0
    for s in word.symbols:
        if idx < len(syms) and s == syms[idx]:
            idx += 1
    return idx == len(syms)


def has_duplicate_publish(word) -> bool:
    """
    Return True if PUBLISH appears at least twice before any PUBREL.
    This is the structural pattern that can trigger CVE-2023-28366.
    """
    publish_count = 0
    for s in word.symbols:
        if s == "PUBLISH":
            publish_count += 1
        if s == "PUBREL":
            break
    return publish_count >= 2
