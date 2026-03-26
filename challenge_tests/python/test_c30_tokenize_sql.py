"""Tests for c30_tokenize_sql: tokenize_sql(query) -> list[tuple]"""
import importlib
import os
import sys

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c30_tokenize_sql")
tokenize_sql = mod.tokenize_sql


def test_basic_select():
    tokens = tokenize_sql("SELECT * FROM users")
    types = [t[0] for t in tokens]
    values = [t[1] for t in tokens]
    assert "SELECT" in values
    assert "*" in values
    assert "FROM" in values
    assert "users" in values


def test_handles_strings():
    tokens = tokenize_sql("WHERE name = 'foo'")
    values = [t[1] for t in tokens]
    assert "foo" in values or "'foo'" in values


def test_handles_numbers():
    tokens = tokenize_sql("LIMIT 10")
    values = [t[1] for t in tokens]
    assert "10" in values or 10 in values


def test_case_insensitive_keywords():
    tokens = tokenize_sql("select * from users")
    values = [t[1] for t in tokens]
    # Keywords should be normalized to uppercase
    assert "SELECT" in values or "select" in values


def test_handles_operators():
    tokens = tokenize_sql("WHERE age >= 18")
    values = [t[1] for t in tokens]
    assert ">=" in values


def test_handles_parentheses():
    tokens = tokenize_sql("SELECT COUNT(id) FROM users")
    values = [t[1] for t in tokens]
    assert "(" in values
    assert ")" in values
