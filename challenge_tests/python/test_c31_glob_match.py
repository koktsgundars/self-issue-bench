"""Tests for c31_glob_match: glob_match(pattern, text) -> bool"""
import importlib
import os
import sys

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c31_glob_match")
glob_match = mod.glob_match


def test_exact_match():
    assert glob_match("hello", "hello") is True


def test_star_matches_any():
    assert glob_match("h*o", "hello") is True


def test_question_mark_single():
    assert glob_match("h?llo", "hello") is True


def test_star_matches_empty():
    assert glob_match("h*llo", "hllo") is True


def test_no_match():
    assert glob_match("hello", "world") is False


def test_star_matches_everything():
    assert glob_match("*", "anything") is True
    assert glob_match("*", "") is True


def test_question_no_empty():
    assert glob_match("h?llo", "hllo") is False


def test_multiple_stars():
    assert glob_match("*a*b*", "xayzb") is True
    assert glob_match("*a*b*", "xyz") is False
