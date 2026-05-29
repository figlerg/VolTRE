import os
import pytest
from parse.quickparse import quickparse
from sample.sample import sample, DurationSamplerMode
from volume.slice_volume import slice_volume
from match.match import match

EXPERIMENTS = os.path.join(os.path.dirname(__file__), '..', 'experiments')

TAKILLER      = os.path.join(EXPERIMENTS, 'TAkiller.tre')
TAKILLER_15   = os.path.join(EXPERIMENTS, 'TAkiller_15_gen.tre')


# ── volume ────────────────────────────────────────────────────────────────────

def test_takiller_volume_n1_is_empty():
    # TAkiller requires at least a + b + c = 3 events; n=1 is empty.
    phi = quickparse(TAKILLER)
    V = slice_volume(phi, 1)
    assert V.total_volume() == 0


def test_takiller_volume_n3_nonzero():
    # n=3: a, b, c with d*=epsilon. Should have positive volume.
    phi = quickparse(TAKILLER)
    V = slice_volume(phi, 3)
    assert V.total_volume() > 0


# ── sampling ──────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("n", [3, 5])
def test_takiller_sampled_words_in_language(n):
    phi = quickparse(TAKILLER)
    w = sample(phi, n=n, mode=DurationSamplerMode.VANILLA)
    assert match(w, phi) > 0, f"Sampled word not in TAkiller language: {w}"


@pytest.mark.parametrize("n", [3, 5])
def test_takiller_15_sampled_words_in_language(n):
    phi = quickparse(TAKILLER_15)
    w = sample(phi, n=n, mode=DurationSamplerMode.VANILLA)
    assert match(w, phi) > 0, f"Sampled word not in TAkiller_15 language: {w}"
