"""Tests for c28_linked_list: LinkedList with append/prepend/delete/reverse/has_cycle/to_list"""
import importlib
import os
import sys
import pytest

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c28_linked_list")
LinkedList = mod.LinkedList


def test_append_and_to_list():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.to_list() == [1, 2, 3]


def test_prepend():
    ll = LinkedList()
    ll.append(2)
    ll.append(3)
    ll.prepend(1)
    assert ll.to_list() == [1, 2, 3]


def test_delete_existing():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.delete(2)
    assert ll.to_list() == [1, 3]


def test_delete_nonexistent_raises():
    ll = LinkedList()
    ll.append(1)
    with pytest.raises(ValueError):
        ll.delete(99)


def test_reverse():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.reverse()
    assert ll.to_list() == [3, 2, 1]


def test_has_cycle_false():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.has_cycle() is False


def test_empty_to_list():
    ll = LinkedList()
    assert ll.to_list() == []
