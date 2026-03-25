"""Tests for c9_url_parser: parse_url(url) -> dict"""
import importlib
import os
import sys

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c9_url_parser")
parse_url = mod.parse_url


def test_full_url():
    result = parse_url("https://example.com:8080/path?key=value#frag")
    assert result["scheme"] == "https"
    assert result["host"] == "example.com"
    assert result["port"] == 8080
    assert result["path"] == "/path"
    assert result["query"] == {"key": "value"}
    assert result["fragment"] == "frag"


def test_no_port():
    result = parse_url("https://example.com/path")
    assert result["host"] == "example.com"
    assert result["port"] is None


def test_no_path():
    result = parse_url("https://example.com")
    assert result["host"] == "example.com"
    assert result["path"] == "" or result["path"] == "/"


def test_query_multiple_params():
    result = parse_url("http://example.com?a=1&b=2")
    assert result["query"]["a"] == "1"
    assert result["query"]["b"] == "2"


def test_no_query():
    result = parse_url("http://example.com/path")
    assert result["query"] == {}


def test_fragment_only():
    result = parse_url("http://example.com#section")
    assert result["fragment"] == "section"


def test_no_fragment():
    result = parse_url("http://example.com/path")
    assert result["fragment"] == "" or result["fragment"] is None


def test_http_scheme():
    result = parse_url("http://example.com")
    assert result["scheme"] == "http"
