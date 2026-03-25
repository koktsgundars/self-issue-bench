"""Tests for c7_retry: retry(fn, retries=3, delay=1.0)"""
import importlib
import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c7_retry")
retry = mod.retry


def test_immediate_success():
    result = retry(lambda: 42)
    assert result == 42


@patch("c7_retry.time.sleep")
def test_success_after_failures(mock_sleep):
    call_count = 0

    def flaky():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("fail")
        return "ok"

    result = retry(flaky, retries=3, delay=0.1)
    assert result == "ok"
    assert call_count == 3


@patch("c7_retry.time.sleep")
def test_all_retries_exhausted(mock_sleep):
    def always_fail():
        raise RuntimeError("always fails")

    try:
        retry(always_fail, retries=3, delay=0.1)
        assert False, "Should have raised"
    except RuntimeError as e:
        assert "always fails" in str(e)


@patch("c7_retry.time.sleep")
def test_retries_zero(mock_sleep):
    """With retries=0, should call fn once and raise on failure."""
    def fail():
        raise ValueError("fail")

    try:
        retry(fail, retries=0, delay=0.1)
        assert False, "Should have raised"
    except ValueError:
        pass


def test_returns_value():
    result = retry(lambda: {"key": "value"})
    assert result == {"key": "value"}
