"""Tests for c1_fibonacci: bigint_multiply(a, b) -> str"""
import importlib
import os
import sys

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c1_fibonacci")
bigint_multiply = mod.bigint_multiply


def test_basic_multiplication():
    assert bigint_multiply("2", "3") == "6"


def test_single_digits():
    assert bigint_multiply("9", "9") == "81"


def test_multiply_by_zero():
    assert bigint_multiply("123", "0") == "0"
    assert bigint_multiply("0", "456") == "0"


def test_multiply_by_one():
    assert bigint_multiply("1", "999") == "999"


def test_negative_times_positive():
    assert bigint_multiply("-3", "4") == "-12"


def test_negative_times_negative():
    assert bigint_multiply("-3", "-4") == "12"


def test_leading_zeros():
    assert bigint_multiply("007", "003") == "21"


def test_large_numbers():
    a = "123456789012345678901234567890"
    b = "987654321098765432109876543210"
    result = bigint_multiply(a, b)
    expected = str(int(a) * int(b))
    assert result == expected


def test_zero_times_zero():
    assert bigint_multiply("0", "0") == "0"


def test_negative_zero():
    # -0 should be "0", not "-0"
    result = bigint_multiply("-0", "5")
    assert result == "0"
