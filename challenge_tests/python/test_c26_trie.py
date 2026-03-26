"""Tests for c26_trie: Trie class with insert/search/starts_with/delete"""
import importlib
import os
import sys
import pytest

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c26_trie")
Trie = mod.Trie


def test_insert_and_search():
    t = Trie()
    t.insert("apple")
    assert t.search("apple") is True


def test_search_missing():
    t = Trie()
    t.insert("apple")
    assert t.search("app") is False


def test_starts_with():
    t = Trie()
    t.insert("apple")
    assert t.starts_with("app") is True
    assert t.starts_with("xyz") is False


def test_delete_existing():
    t = Trie()
    t.insert("apple")
    t.delete("apple")
    assert t.search("apple") is False


def test_delete_nonexistent_raises():
    t = Trie()
    with pytest.raises(KeyError):
        t.delete("ghost")


def test_prefix_search_after_deletion():
    t = Trie()
    t.insert("apple")
    t.insert("app")
    t.delete("apple")
    assert t.search("app") is True
    assert t.starts_with("app") is True


def test_insert_prefix_of_existing():
    t = Trie()
    t.insert("apple")
    t.insert("app")
    assert t.search("app") is True
    assert t.search("apple") is True
