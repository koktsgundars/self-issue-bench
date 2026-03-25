"""Tests for c15_rate_limiter: RateLimiter(max_calls, period) with allow()"""
import importlib
import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c15_rate_limiter")
RateLimiter = mod.RateLimiter


def test_allows_within_limit():
    with patch("c15_rate_limiter.time.time", return_value=1000.0):
        limiter = RateLimiter(3, 10.0)
        assert limiter.allow() is True
        assert limiter.allow() is True
        assert limiter.allow() is True


def test_denies_over_limit():
    with patch("c15_rate_limiter.time.time", return_value=1000.0):
        limiter = RateLimiter(2, 10.0)
        assert limiter.allow() is True
        assert limiter.allow() is True
        assert limiter.allow() is False


def test_sliding_window_allows_after_period():
    t = 1000.0
    with patch("c15_rate_limiter.time.time") as mock_time:
        mock_time.return_value = t
        limiter = RateLimiter(2, 10.0)
        assert limiter.allow() is True
        assert limiter.allow() is True
        assert limiter.allow() is False

        # Advance past the window
        mock_time.return_value = t + 11.0
        assert limiter.allow() is True


def test_single_call_limit():
    with patch("c15_rate_limiter.time.time", return_value=1000.0):
        limiter = RateLimiter(1, 5.0)
        assert limiter.allow() is True
        assert limiter.allow() is False
