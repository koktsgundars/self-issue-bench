"""Tests for c29_parse_cron: next_cron_times(expr, after, count) -> list[datetime]"""
import importlib
import os
import sys
from datetime import datetime

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c29_parse_cron")
next_cron_times = mod.next_cron_times


def test_every_minute():
    after = datetime(2025, 1, 1, 0, 0)
    result = next_cron_times("* * * * *", after, 3)
    assert len(result) == 3
    assert result[0] == datetime(2025, 1, 1, 0, 1)
    assert result[1] == datetime(2025, 1, 1, 0, 2)
    assert result[2] == datetime(2025, 1, 1, 0, 3)


def test_specific_minute():
    after = datetime(2025, 1, 1, 0, 0)
    result = next_cron_times("30 * * * *", after, 2)
    assert result[0] == datetime(2025, 1, 1, 0, 30)
    assert result[1] == datetime(2025, 1, 1, 1, 30)


def test_specific_hour_and_minute():
    after = datetime(2025, 1, 1, 0, 0)
    result = next_cron_times("0 9 * * *", after, 2)
    assert result[0] == datetime(2025, 1, 1, 9, 0)
    assert result[1] == datetime(2025, 1, 2, 9, 0)


def test_step_value():
    after = datetime(2025, 1, 1, 0, 0)
    result = next_cron_times("*/15 * * * *", after, 4)
    assert result[0] == datetime(2025, 1, 1, 0, 15)
    assert result[1] == datetime(2025, 1, 1, 0, 30)
    assert result[2] == datetime(2025, 1, 1, 0, 45)
    assert result[3] == datetime(2025, 1, 1, 1, 0)


def test_returns_correct_count():
    after = datetime(2025, 1, 1, 0, 0)
    result = next_cron_times("* * * * *", after, 5)
    assert len(result) == 5


def test_after_respected():
    after = datetime(2025, 6, 15, 12, 30)
    result = next_cron_times("0 9 * * *", after, 1)
    assert result[0] == datetime(2025, 6, 16, 9, 0)
