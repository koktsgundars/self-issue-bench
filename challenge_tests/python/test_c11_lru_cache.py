"""Tests for c11_lru_cache: LRUCache(capacity) with get/put"""
import importlib
import os
import sys

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c11_lru_cache")
LRUCache = mod.LRUCache


def test_basic_put_get():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1


def test_missing_key():
    cache = LRUCache(2)
    assert cache.get(99) == -1


def test_eviction():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)  # evicts key 1
    assert cache.get(1) == -1
    assert cache.get(3) == 3


def test_get_refreshes_order():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.get(1)      # refreshes key 1
    cache.put(3, 3)   # should evict key 2, not key 1
    assert cache.get(2) == -1
    assert cache.get(1) == 1


def test_update_existing_key():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(1, 10)
    assert cache.get(1) == 10


def test_capacity_one():
    cache = LRUCache(1)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == -1
    assert cache.get(2) == 2


def test_put_updates_refresh_order():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(1, 10)   # update refreshes key 1
    cache.put(3, 3)    # should evict key 2
    assert cache.get(2) == -1
    assert cache.get(1) == 10
