"""Tests for runner/test_code.py."""
from test_code import extract_code, parse_node_test_output, _parse_simple_test_output


def test_extract_code_with_fences():
    raw = "```python\ndef foo():\n    pass\n```"
    assert extract_code(raw) == "def foo():\n    pass"


def test_extract_code_with_language_tag():
    raw = "```javascript\nconst x = 1;\n```"
    assert extract_code(raw) == "const x = 1;"


def test_extract_code_no_fences():
    raw = "def foo():\n    pass"
    assert extract_code(raw) == "def foo():\n    pass"


def test_extract_code_empty():
    assert extract_code("") == ""


def test_extract_code_only_fences():
    raw = "```python\n```"
    assert extract_code(raw) == ""


def test_parse_node_test_output_pass():
    output = "  \u2714 basic test (0.5ms)\n  \u2714 another test (0.3ms)\n"
    details = parse_node_test_output(output)
    assert len(details) == 2
    assert all(d["status"] == "pass" for d in details)
    assert details[0]["name"] == "basic test"


def test_parse_node_test_output_fail():
    output = "  \u2716 broken test (0.5ms)\n"
    details = parse_node_test_output(output)
    assert len(details) == 1
    assert details[0]["status"] == "fail"
    assert details[0]["name"] == "broken test"


def test_parse_node_test_output_mixed():
    output = "  \u2714 good (0.5ms)\n  \u2716 bad (0.3ms)\n"
    details = parse_node_test_output(output)
    assert len(details) == 2
    assert details[0]["status"] == "pass"
    assert details[1]["status"] == "fail"


def test_parse_node_test_output_skips_suite_level():
    output = "\u2714 SuiteName (5ms)\n  \u2714 test inside (0.5ms)\n"
    details = parse_node_test_output(output)
    # Suite-level line (no indent) should be skipped
    assert len(details) == 1
    assert details[0]["name"] == "test inside"


def test_parse_node_test_output_tap_fallback():
    output = "ok 1 - test_one\nnot ok 2 - test_two\n"
    details = parse_node_test_output(output)
    assert len(details) == 2
    assert details[0]["status"] == "pass"
    assert details[1]["status"] == "fail"


def test_parse_simple_test_output():
    output = "PASS test_basic\nFAIL test_edge: expected 1 got 2\nPASS test_another\n"
    details = _parse_simple_test_output(output)
    assert len(details) == 3
    assert details[0]["status"] == "pass"
    assert details[1]["status"] == "fail"
    assert details[1]["message"] == "expected 1 got 2"
    assert details[2]["status"] == "pass"


def test_parse_simple_test_output_error():
    output = "ERROR test_crash: TypeError: undefined\n"
    details = _parse_simple_test_output(output)
    assert len(details) == 1
    assert details[0]["status"] == "error"


def test_parse_simple_test_output_empty():
    assert _parse_simple_test_output("") == []
