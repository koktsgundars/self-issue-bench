"""Tests for c27_min_heap: MinHeap class with push/pop/peek/len"""
import importlib
import os
import sys
import pytest

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c27_min_heap")
MinHeap = mod.MinHeap


def test_push_and_peek():
    h = MinHeap()
    h.push(5)
    h.push(3)
    h.push(7)
    assert h.peek() == 3


def test_pop_returns_min():
    h = MinHeap()
    h.push(5)
    h.push(3)
    h.push(7)
    assert h.pop() == 3
    assert h.peek() == 5


def test_pop_in_order():
    h = MinHeap()
    for v in [4, 1, 7, 3, 2]:
        h.push(v)
    result = [h.pop() for _ in range(5)]
    assert result == [1, 2, 3, 4, 7]


def test_pop_empty_raises():
    h = MinHeap()
    with pytest.raises(IndexError):
        h.pop()


def test_peek_empty_raises():
    h = MinHeap()
    with pytest.raises(IndexError):
        h.peek()


def test_len():
    h = MinHeap()
    assert len(h) == 0
    h.push(1)
    h.push(2)
    assert len(h) == 2
    h.pop()
    assert len(h) == 1


def test_duplicate_values():
    h = MinHeap()
    h.push(3)
    h.push(3)
    h.push(3)
    assert h.pop() == 3
    assert h.pop() == 3
    assert len(h) == 1
