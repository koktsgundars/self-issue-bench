"""Tests for c32_sanitize_html: sanitize_html(html) -> str"""
import importlib
import os
import sys

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c32_sanitize_html")
sanitize_html = mod.sanitize_html


def test_preserves_allowed_tags():
    result = sanitize_html("<p>hello</p>")
    assert "<p>" in result and "hello" in result


def test_strips_script_tags():
    result = sanitize_html("<script>alert(1)</script>")
    assert "<script>" not in result
    assert "alert" not in result


def test_preserves_text_of_stripped_tags():
    result = sanitize_html("<div>hello</div>")
    assert "hello" in result


def test_allows_href_on_a():
    html = '<a href="http://example.com">link</a>'
    result = sanitize_html(html)
    assert "http://example.com" in result
    assert "link" in result


def test_strips_javascript_urls():
    html = '<a href="javascript:alert(1)">click</a>'
    result = sanitize_html(html)
    assert "javascript:" not in result


def test_strips_disallowed_attributes():
    html = '<p style="color:red">text</p>'
    result = sanitize_html(html)
    assert "style" not in result
    assert "text" in result
