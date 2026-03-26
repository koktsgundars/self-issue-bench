"""Tests for c23_merge_intervals: merge_intervals(intervals) -> list"""
import importlib
import os
import sys

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c23_merge_intervals")
merge_intervals = mod.merge_intervals


def test_basic_overlap():
    assert merge_intervals([[1, 3], [2, 6]]) == [[1, 6]]


def test_non_overlapping():
    result = merge_intervals([[1, 2], [4, 5]])
    assert result == [[1, 2], [4, 5]]


def test_unsorted_input():
    result = merge_intervals([[3, 6], [1, 4]])
    assert result == [[1, 6]]


def test_empty_input():
    assert merge_intervals([]) == []


def test_single_interval():
    assert merge_intervals([[1, 5]]) == [[1, 5]]


def test_adjacent_intervals():
    assert merge_intervals([[1, 2], [2, 3]]) == [[1, 3]]


def test_fully_contained():
    result = merge_intervals([[1, 10], [2, 5]])
    assert result == [[1, 10]]


def test_multiple_overlapping():
    result = merge_intervals([[1, 4], [2, 5], [3, 8]])
    assert result == [[1, 8]]
