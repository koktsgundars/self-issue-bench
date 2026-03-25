"""Tests for c2_palindrome: json_path(data, path) -> list"""
import importlib
import os
import sys

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c2_palindrome")
json_path = mod.json_path

STORE_DATA = {
    "store": {
        "name": "Books Inc",
        "books": [
            {"title": "A", "price": 10},
            {"title": "B", "price": 20},
        ],
    }
}


def test_root():
    assert json_path(STORE_DATA, "$") == [STORE_DATA]


def test_dot_notation():
    assert json_path(STORE_DATA, "$.store.name") == ["Books Inc"]


def test_bracket_notation():
    assert json_path(STORE_DATA, "$['store']['name']") == ["Books Inc"]


def test_array_index():
    assert json_path(STORE_DATA, "$.store.books[0]") == [{"title": "A", "price": 10}]


def test_array_index_nested():
    assert json_path(STORE_DATA, "$.store.books[0].title") == ["A"]


def test_wildcard():
    result = json_path(STORE_DATA, "$.store.books[*].title")
    assert result == ["A", "B"]


def test_missing_path():
    assert json_path(STORE_DATA, "$.nonexistent") == []


def test_missing_nested():
    assert json_path(STORE_DATA, "$.store.nothing.deep") == []


def test_simple_dict():
    assert json_path({"a": 1}, "$.a") == [1]


def test_double_quoted_brackets():
    data = {"key with spaces": 42}
    assert json_path(data, '$["key with spaces"]') == [42]
