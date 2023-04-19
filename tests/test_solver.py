import pytest
from app.solver import Solver


@pytest.fixture
def all_words():
    words = [
        "agave",
        "abate",
        "argue",
        "biker",
        "baker",
        "caper",
        "czars",
        "tests",
        "solve",
    ]
    return [[l for l in word] for word in words]


def test_all_words(all_words):
    assert len(all_words) == 9
    solver = Solver(word=None, words=all_words)
    assert len(solver.available_words) == 9


def test_available_words(all_words):
    solver = Solver(word="solve", words=all_words)
    assert len(solver.available_words) == 9
    direct_hits = {}
    hits = {}
    misses = {"a"}
    aw = solver.get_available_words(direct_hits, hits, misses)
    assert len(solver.available_words) == 3
    direct_hits = {("v", 3)}
    aw = solver.get_available_words(direct_hits, hits, misses)
    assert len(solver.available_words) == 1


def test_get_stats(all_words):
    solver = Solver(word="solve", words=all_words)
    best_chars = solver.get_stats(solver.available_words)
    assert len(best_chars) == 5
    assert best_chars == ["a", "a", "a", "e", "e"]


def test_best_guess(all_words):
    solver = Solver(word="solve", words=all_words)
    direct_hits = {("e", 3)}
    hits = {"k": {1, 4}}
    misses = {"a"}
    aw = solver.get_available_words(direct_hits, hits, misses)
    s = solver.get_stats(aw)
    g = solver.get_best_guess(s, aw)
    assert g == ["b", "i", "k", "e", "r"]
