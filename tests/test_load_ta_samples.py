import os
import pytest
from sample.TimedWord import TimedWord

SAMPLE_FILE = os.path.join(
    os.path.dirname(__file__), '..', 'experiments', 'paper_experiments', '09_ta_case_study', 'ta_sample_1.txt'
)


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
