"""Tests for c13_date_formatter: format_date(date_str, input_format, output_format)"""
import importlib
import os
import sys

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c13_date_formatter")
format_date = mod.format_date


def test_basic_conversion():
    result = format_date("2026-03-24", "%Y-%m-%d", "%d/%m/%Y")
    assert result == "24/03/2026"


def test_us_format():
    result = format_date("03/24/2026", "%m/%d/%Y", "%Y-%m-%d")
    assert result == "2026-03-24"


def test_with_time():
    result = format_date("2026-03-24 14:30:00", "%Y-%m-%d %H:%M:%S", "%H:%M on %d %b %Y")
    assert "14:30" in result


def test_invalid_date():
    try:
        format_date("2026-02-30", "%Y-%m-%d", "%d/%m/%Y")
        assert False, "Should raise ValueError for invalid date"
    except ValueError:
        pass


def test_identity_format():
    result = format_date("2026-01-15", "%Y-%m-%d", "%Y-%m-%d")
    assert result == "2026-01-15"
