import os
import pytest
from math import inf
from parse.quickparse import quickparse
from volume.slice_volume import slice_volume

EXPERIMENTS = os.path.join(os.path.dirname(__file__), '..', 'experiments')


def spec(name):
    return quickparse(os.path.join(EXPERIMENTS, name))


# ── atom ──────────────────────────────────────────────────────────────────────

def test_atom_volume_n1_is_nonzero():
    # V(a, 1) is constant 1 on [0, inf)
    phi = spec('spec_13_atom.tre')
    V = slice_volume(phi, 1)
    assert V(0.5) == 1
    assert V(10.0) == 1


def test_atom_volume_n2_is_zero():
    # atom at n=2 should be the zero polynomial
    phi = spec('spec_13_atom.tre')
    V = slice_volume(phi, 2)
    assert V(0.5) == 0
    assert V(1.0) == 0


# ── kleene star ───────────────────────────────────────────────────────────────

def test_kleene_n0_has_delta():
    # e* at n=0 is the epsilon/delta distribution
    phi = spec('spec_00.tre')
    V = slice_volume(phi, 0)
    assert V.delta


def test_kleene_n1_nonzero():
    phi = spec('spec_00.tre')
    V = slice_volume(phi, 1)
    # spec_00 inner is <a>_[0,2] + <b>_[0,1], so V(T) > 0 for T in (0,2)
    assert V(0.5) > 0
    assert V(1.5) > 0


# ── timed expression ──────────────────────────────────────────────────────────

def test_timed_total_volume():
    # <a.b>_[0,1] at n=2: ∫_0^1 T dT = 0.5
    phi = spec('spec_02.tre')
    V = slice_volume(phi, 2)
    assert abs(float(V.total_volume()) - 0.5) < 1e-6


def test_timed_volume_outside_interval_is_zero():
    phi = spec('spec_02.tre')
    V = slice_volume(phi, 2)
    assert V(1.5) == 0   # outside [0,1]


# ── union volume is sum ───────────────────────────────────────────────────────

def test_union_volume_is_sum_of_parts():
    # V(<a>_[0,2] + <b>_[0,1], 1) at T=0.5:
    #   <a>_[0,2] contributes 1 (T=0.5 in [0,2])
    #   <b>_[0,1] contributes 1 (T=0.5 in [0,1])
    #   total = 2
    from parse.quickparse import quickparse as qp
    from volume.slice_volume import slice_volume as sv
    # parse just the inner expression without kleene
    from parse.TREParser import TREParser
    phi_full = qp(os.path.join(EXPERIMENTS, 'spec_00.tre'))
    # spec_00 is kleene of the union; get n=1 which equals the inner union at n=1
    V = sv(phi_full, 1)
    assert V(0.5) == 2   # both branches contribute at T=0.5
    assert V(1.5) == 1   # only <a>_[0,2] contributes at T=1.5


# ── intersection raises ───────────────────────────────────────────────────────

def test_intersection_volume_raises():
    phi = spec('spec_07_intersection.tre')
    with pytest.raises((ValueError, NotImplementedError)):
        slice_volume(phi, 2)
