"""Tests for c3_word_frequency: word_frequency(text) -> dict"""
import importlib
import os
import sys

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c3_word_frequency")
word_frequency = mod.word_frequency


def test_basic():
    result = word_frequency("hello world hello")
    assert result["hello"] == 2
    assert result["world"] == 1


def test_case_insensitive():
    result = word_frequency("Hello hello HELLO")
    assert result["hello"] == 3


def test_punctuation_ignored():
    result = word_frequency("hello, world! hello.")
    assert result["hello"] == 2
    assert result["world"] == 1


def test_empty_string():
    result = word_frequency("")
    assert result == {}


def test_single_word():
    result = word_frequency("test")
    assert result["test"] == 1


def test_multiple_spaces():
    result = word_frequency("hello   world")
    assert result["hello"] == 1
    assert result["world"] == 1
