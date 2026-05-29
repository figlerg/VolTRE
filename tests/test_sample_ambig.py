import os
import pytest
from parse.quickparse import quickparse
from sample.sample import sample, DurationSamplerMode
from match.match import match
from misc.disambiguate import disambiguate

EXPERIMENTS = os.path.join(os.path.dirname(__file__), '..', 'experiments')

AMBIG_09 = os.path.join(EXPERIMENTS, 'spec_09_ambig.tre')   # <a*>_[0,3] + (<a + b>_[0,1])*
AMBIG_20 = os.path.join(EXPERIMENTS, 'spec_20_ambig.tre')   # <a*.a*>_[0,2]


# ── sampling from ambiguous specs ─────────────────────────────────────────────

@pytest.mark.parametrize("n", [1, 2, 3])
def test_ambig_09_sampled_words_in_language(n):
    phi = quickparse(AMBIG_09)
    w = sample(phi, n=n, mode=DurationSamplerMode.VANILLA)
    assert match(w, phi) > 0, f"Sampled word not in language: {w}"


@pytest.mark.parametrize("n", [1, 2, 3])
def test_ambig_20_sampled_words_in_language(n):
    phi = quickparse(AMBIG_20)
    w = sample(phi, n=n, mode=DurationSamplerMode.VANILLA)
    assert match(w, phi) > 0, f"Sampled word not in language: {w}"


# ── ambiguity: words have multiple parses ─────────────────────────────────────

def test_ambig_20_word_has_multiple_parses():
    # <a*.a*>_[0,2]: 'aa' has 3 parses (see test_match.py for derivation)
    phi = quickparse(AMBIG_20)
    from sample.TimedWord import TimedWord
    w = TimedWord(['a', 'a'], [0.5, 0.5])
    assert match(w, phi) > 1


# ── disambiguate reduces to unambiguous ───────────────────────────────────────

def test_disambiguate_renames_symbols():
    # disambiguate() should rename repeated symbols so each occurrence gets a unique name
    phi = quickparse(AMBIG_09)   # <a*>_[0,3] + (<a + b>_[0,1])* — 'a' appears twice
    result = disambiguate(phi)
    assert 'a1' in result and 'a2' in result, "Expected renamed symbols a1, a2 in disambiguated string"


def test_sample_ambig_via_sample_function():
    # sample() internally handles disambiguation; the returned word uses original symbols
    phi = quickparse(AMBIG_09)
    w = sample(phi, n=2, mode=DurationSamplerMode.VANILLA)
    assert match(w, phi) > 0
