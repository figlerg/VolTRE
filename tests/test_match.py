import os
from match.match import match
from sample.TimedWord import TimedWord
from parse.quickparse import quickparse

EXPERIMENTS = os.path.join(os.path.dirname(__file__), '..', 'experiments')


# ── atom ──────────────────────────────────────────────────────────────────────

def test_atom_match():
    phi = quickparse(os.path.join(EXPERIMENTS, 'spec_13_atom.tre'))  # just 'a'
    assert match(TimedWord(['a'], [0.5]), phi) == 1


def test_atom_wrong_symbol():
    phi = quickparse(os.path.join(EXPERIMENTS, 'spec_13_atom.tre'))
    assert match(TimedWord(['b'], [0.5]), phi) == 0


def test_atom_wrong_length():
    phi = quickparse(os.path.join(EXPERIMENTS, 'spec_13_atom.tre'))
    assert match(TimedWord(['a', 'a'], [0.5, 0.5]), phi) == 0
    assert match(TimedWord([], []), phi) == 0


# ── timed constraint ──────────────────────────────────────────────────────────

def test_timed_in_range():
    # spec_02: <a.b>_[0,1]  — duration 0.7 ∈ [0,1]
    phi = quickparse(os.path.join(EXPERIMENTS, 'spec_02.tre'))
    assert match(TimedWord(['a', 'b'], [0.3, 0.4]), phi) == 1


def test_timed_out_of_range():
    # duration 1.5 ∉ [0,1]
    phi = quickparse(os.path.join(EXPERIMENTS, 'spec_02.tre'))
    assert match(TimedWord(['a', 'b'], [0.7, 0.8]), phi) == 0


# ── union ─────────────────────────────────────────────────────────────────────

def test_union_both_branches():
    # spec_00: (<a>_[0,2] + <b>_[0,1])* — both symbols should be accepted
    phi = quickparse(os.path.join(EXPERIMENTS, 'spec_00.tre'))
    assert match(TimedWord(['a'], [1.0]), phi) > 0
    assert match(TimedWord(['b'], [0.5]), phi) > 0


# ── kleene star ───────────────────────────────────────────────────────────────

def test_kleene_epsilon():
    phi = quickparse(os.path.join(EXPERIMENTS, 'spec_00.tre'))
    assert match(TimedWord([], []), phi) == 1


def test_kleene_multi_letter():
    phi = quickparse(os.path.join(EXPERIMENTS, 'spec_00.tre'))
    assert match(TimedWord(['a', 'b', 'a'], [0.5, 0.3, 1.0]), phi) > 0


def test_kleene_out_of_timed_range():
    # delay 3.0 violates <a>_[0,2], so word is outside the language
    phi = quickparse(os.path.join(EXPERIMENTS, 'spec_00.tre'))
    assert match(TimedWord(['a'], [3.0]), phi) == 0


# ── ambiguous expressions ─────────────────────────────────────────────────────

def test_ambiguous_parse_count():
    # spec_20: <a*.a*>_[0,2]
    # 'aa' splits as ()(aa), (a)(a), (aa)()  →  3 parses
    phi = quickparse(os.path.join(EXPERIMENTS, 'spec_20_ambig.tre'))
    assert match(TimedWord(['a', 'a'], [0.5, 0.5]), phi) == 3


def test_unambiguous_count_is_one():
    phi = quickparse(os.path.join(EXPERIMENTS, 'spec_13_atom.tre'))
    assert match(TimedWord(['a'], [0.7]), phi) == 1
