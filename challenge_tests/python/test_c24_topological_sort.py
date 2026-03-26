"""Tests for c24_topological_sort: topological_sort(graph) -> list"""
import importlib
import os
import sys
import pytest

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c24_topological_sort")
topological_sort = mod.topological_sort


def test_linear_chain():
    graph = {"a": ["b"], "b": ["c"], "c": []}
    result = topological_sort(graph)
    assert result.index("a") < result.index("b") < result.index("c")


def test_diamond():
    graph = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
    result = topological_sort(graph)
    assert result.index("a") < result.index("b")
    assert result.index("a") < result.index("c")
    assert result.index("b") < result.index("d")
    assert result.index("c") < result.index("d")


def test_cycle_raises():
    graph = {"a": ["b"], "b": ["c"], "c": ["a"]}
    with pytest.raises(ValueError):
        topological_sort(graph)


def test_single_node():
    graph = {"a": []}
    assert topological_sort(graph) == ["a"]


def test_empty_graph():
    assert topological_sort({}) == []


def test_valid_ordering():
    graph = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": [], "e": ["a"]}
    result = topological_sort(graph)
    for node, deps in graph.items():
        for dep in deps:
            assert result.index(node) < result.index(dep)
