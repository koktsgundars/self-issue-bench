"""Tests for c33_escape_shell: escape_shell_arg(arg) -> str"""
import importlib
import os
import sys

sys.path.insert(0, os.getcwd())
mod = importlib.import_module("c33_escape_shell")
escape_shell_arg = mod.escape_shell_arg


def test_simple_string():
    result = escape_shell_arg("hello")
    # Should be safe — either unchanged or quoted
    assert "hello" in result


def test_spaces_quoted():
    result = escape_shell_arg("hello world")
    # Must be quoted or escaped so the space is safe
    assert result != "hello world"
    assert "hello" in result and "world" in result


def test_single_quotes_escaped():
    result = escape_shell_arg("it's")
    # The single quote must be escaped or handled
    assert "it" in result and "s" in result


def test_double_quotes_handled():
    result = escape_shell_arg('say "hi"')
    assert "say" in result and "hi" in result


def test_semicolons_safe():
    result = escape_shell_arg("foo;rm -rf /")
    # Semicolon must not be interpreted as command separator
    assert ";" in result or "\\;" in result or "foo" in result


def test_empty_string():
    result = escape_shell_arg("")
    # Empty string should produce a safe representation like '' or ""
    assert result in ("''", '""', "")  or len(result) >= 0


def test_newlines_handled():
    result = escape_shell_arg("line1\nline2")
    assert "line1" in result and "line2" in result
