"""Tests for c21_task_scheduler: Task dataclass + TaskScheduler class"""
import importlib
import os
import sys

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c21_task_scheduler")
Task = mod.Task
TaskScheduler = mod.TaskScheduler


def test_basic_add_and_run():
    s = TaskScheduler()
    ran = []
    s.add_task(Task(id="a", priority=1, action=lambda: ran.append("a")))
    result = s.run_next()
    assert result == "a"
    assert ran == ["a"]


def test_priority_order():
    s = TaskScheduler()
    ran = []
    s.add_task(Task(id="low", priority=10, action=lambda: ran.append("low")))
    s.add_task(Task(id="high", priority=1, action=lambda: ran.append("high")))
    result = s.run_next()
    assert result == "high"


def test_fifo_equal_priority():
    s = TaskScheduler()
    ran = []
    s.add_task(Task(id="first", priority=1, action=lambda: ran.append("first")))
    s.add_task(Task(id="second", priority=1, action=lambda: ran.append("second")))
    ids = s.run_all()
    assert ids == ["first", "second"]
    assert ran == ["first", "second"]


def test_cancel_task():
    s = TaskScheduler()
    s.add_task(Task(id="a", priority=1, action=lambda: None))
    s.cancel_task("a")
    try:
        s.run_next()
        assert False, "Should raise IndexError on empty"
    except IndexError:
        pass


def test_duplicate_id_raises():
    s = TaskScheduler()
    s.add_task(Task(id="a", priority=1, action=lambda: None))
    try:
        s.add_task(Task(id="a", priority=2, action=lambda: None))
        assert False, "Should raise ValueError for duplicate id"
    except ValueError:
        pass


def test_cancel_missing_raises():
    s = TaskScheduler()
    try:
        s.cancel_task("nonexistent")
        assert False, "Should raise KeyError"
    except KeyError:
        pass


def test_run_next_empty_raises():
    s = TaskScheduler()
    try:
        s.run_next()
        assert False, "Should raise IndexError"
    except IndexError:
        pass


def test_run_all():
    s = TaskScheduler()
    ran = []
    s.add_task(Task(id="c", priority=3, action=lambda: ran.append("c")))
    s.add_task(Task(id="a", priority=1, action=lambda: ran.append("a")))
    s.add_task(Task(id="b", priority=2, action=lambda: ran.append("b")))
    ids = s.run_all()
    assert ids == ["a", "b", "c"]
    assert ran == ["a", "b", "c"]
