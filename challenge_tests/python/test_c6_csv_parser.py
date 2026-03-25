"""Tests for c6_csv_parser: parse_csv_row(row) -> list"""
import importlib
import os
import sys

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c6_csv_parser")
parse_csv_row = mod.parse_csv_row


def test_simple_row():
    assert parse_csv_row("a,b,c") == ["a", "b", "c"]


def test_quoted_field_with_comma():
    assert parse_csv_row('a,"b,c",d') == ["a", "b,c", "d"]


def test_whitespace_stripping():
    result = parse_csv_row("  a , b , c  ")
    assert result == ["a", "b", "c"]


def test_empty_fields():
    assert parse_csv_row("a,,c") == ["a", "", "c"]


def test_quoted_field_with_quotes():
    # Escaped double quotes inside quoted field: "" -> "
    assert parse_csv_row('"a""b",c') == ['a"b', "c"]


def test_single_field():
    assert parse_csv_row("hello") == ["hello"]


def test_empty_string():
    result = parse_csv_row("")
    assert result == [""] or result == []


def test_only_quoted():
    assert parse_csv_row('"hello"') == ["hello"]
