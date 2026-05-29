import os
import pytest
from parse.quickparse import quickparse
from match.match import match
from sample.TimedWord import TimedWord

SAMPLE_FILE = os.path.join(
    os.path.dirname(__file__), '..', 'experiments', 'paper_experiments', '09_ta_case_study', 'ta_sample_1.txt'
)

PHI1_FILE = os.path.join(
    os.path.dirname(__file__), '..', 'experiments', 'paper_experiments', 'spec_02_subset_A.tre'
)

PHI2_FILE = os.path.join(
    os.path.dirname(__file__), '..', 'experiments', 'paper_experiments', 'spec_02_subset_B.tre'
)


# ── loading ───────────────────────────────────────────────────────────────────

def test_load_returns_list_of_timed_words():
    words = TimedWord.from_wordgen_file(SAMPLE_FILE)
    assert len(words) > 0
    assert all(isinstance(w, TimedWord) for w in words)


def test_symbols_and_delays_match_length():
    words = TimedWord.from_wordgen_file(SAMPLE_FILE)
    for w in words:
        assert len(w.symbols) == len(w.delays)


def test_known_first_word():
    """First line of ta_sample_1.txt has 10 tokens starting with 0.763440[g]."""
    words = TimedWord.from_wordgen_file(SAMPLE_FILE)
    w = words[0]
    assert len(w.symbols) == 10
    assert w.symbols[0] == 'g'
    assert abs(w.delays[0] - 0.763440) < 1e-5


def test_load_ignores_empty_lines(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text("\n1.0[a] 2.0[b]\n\n0.5[c]\n")
    words = TimedWord.from_wordgen_file(str(f))
    assert len(words) == 2
    assert words[0].symbols == ['a', 'b']
    assert words[1].symbols == ['c']


# ── TimedWord properties ──────────────────────────────────────────────────────

def test_all_delays_positive():
    """wordgen only produces positive delays; anything ≤ 0 would be malformed."""
    words = TimedWord.from_wordgen_file(SAMPLE_FILE)
    for w in words:
        assert all(d > 0 for d in w.delays), f"Non-positive delay in {w}"


def test_duration_equals_sum_of_delays():
    words = TimedWord.from_wordgen_file(SAMPLE_FILE)
    for w in words:
        assert abs(w.duration - sum(w.delays)) < 1e-9


def test_length_property():
    words = TimedWord.from_wordgen_file(SAMPLE_FILE)
    for w in words:
        assert w.length == len(w.symbols)


# ── TimedWord operations ──────────────────────────────────────────────────────

def test_timed_word_concat():
    """Concatenation via * should join symbols and delays."""
    w1 = TimedWord(['a', 'b'], [1.0, 2.0])
    w2 = TimedWord(['c'], [0.5])
    w3 = w1 * w2
    assert w3.symbols == ['a', 'b', 'c']
    assert w3.delays == [1.0, 2.0, 0.5]
    assert w3.length == 3
    assert abs(w3.duration - 3.5) < 1e-9


def test_timed_word_slicing():
    """Slicing should return a valid sub-word."""
    w = TimedWord(['a', 'b', 'c', 'd'], [1.0, 2.0, 0.5, 1.5])
    prefix = w[:2]
    assert prefix.symbols == ['a', 'b']
    assert prefix.delays == [1.0, 2.0]
    suffix = w[2:]
    assert suffix.symbols == ['c', 'd']
    assert suffix.delays == [0.5, 1.5]
    # slicing and concat round-trip
    assert (prefix * suffix).symbols == w.symbols


# ── match against phi_1 / phi_2 ───────────────────────────────────────────────

def test_words_can_be_matched_against_phi1():
    """Smoke test: match() runs on all loaded words without error."""
    words = TimedWord.from_wordgen_file(SAMPLE_FILE)
    phi1 = quickparse(PHI1_FILE)
    for w in words:
        result = match(w, phi1)
        assert isinstance(result, int) or isinstance(result, bool)


def test_phi2_subset_of_phi1():
    """Every word accepted by phi_2 should also be accepted by phi_1 (phi_2 ⊆ phi_1)."""
    words = TimedWord.from_wordgen_file(SAMPLE_FILE)
    phi1 = quickparse(PHI1_FILE)
    phi2 = quickparse(PHI2_FILE)
    for w in words:
        if match(w, phi2) > 0:
            assert match(w, phi1) > 0, f"phi_2 ⊆ phi_1 violated for word: {w}"
