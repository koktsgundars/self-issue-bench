"""Tests for c34_diff_objects: diff_objects(a, b) -> list of diffs"""
import importlib
import os
import sys

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c34_diff_objects")
diff_objects = mod.diff_objects


def test_identical_dicts():
    assert diff_objects({"a": 1}, {"a": 1}) == []


def test_added_key():
    result = diff_objects({"a": 1}, {"a": 1, "b": 2})
    paths = [d["path"] for d in result]
    assert "b" in paths


def test_removed_key():
    result = diff_objects({"a": 1, "b": 2}, {"a": 1})
    paths = [d["path"] for d in result]
    assert "b" in paths


def test_changed_value():
    result = diff_objects({"a": 1}, {"a": 2})
    assert len(result) == 1
    assert result[0]["path"] == "a"


def test_nested_changes_dot_notation():
    result = diff_objects({"a": {"b": 1}}, {"a": {"b": 2}})
    paths = [d["path"] for d in result]
    assert "a.b" in paths


def test_sorted_by_path():
    result = diff_objects({"c": 1, "a": 1}, {"c": 2, "a": 2})
    paths = [d["path"] for d in result]
    assert paths == sorted(paths)


def test_both_empty():
    assert diff_objects({}, {}) == []
