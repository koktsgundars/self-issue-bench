"""Tests for c25_edit_distance: edit_distance(s1, s2) -> int"""
import importlib
import os
import sys

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c25_edit_distance")
edit_distance = mod.edit_distance


def test_identical_strings():
    assert edit_distance("abc", "abc") == 0


def test_empty_to_nonempty():
    assert edit_distance("", "hello") == 5


def test_nonempty_to_empty():
    assert edit_distance("hello", "") == 5


def test_single_char_difference():
    assert edit_distance("cat", "bat") == 1


def test_kitten_sitting():
    assert edit_distance("kitten", "sitting") == 3


def test_completely_different():
    assert edit_distance("abc", "xyz") == 3


def test_both_empty():
    assert edit_distance("", "") == 0


def test_insertion_needed():
    assert edit_distance("ab", "abc") == 1
