from review import check_self_caught, parse_issues


def test_parse_valid_json_lines():
    response = (
        '{"type": "correctness", "severity": "high", "description": "Off by one"}\n'
        '{"type": "edge_case", "severity": "low", "description": "No null check"}\n'
    )
    issues = parse_issues(response)
    assert len(issues) == 2
    assert issues[0]["type"] == "correctness"
    assert issues[1]["type"] == "edge_case"


def test_parse_empty_response():
    assert parse_issues("") == []
    assert parse_issues("[]") == []


def test_parse_skips_unknown_type():
    response = '{"type": "performance", "severity": "high", "description": "Slow"}\n'
    issues = parse_issues(response)
    assert len(issues) == 0


def test_parse_normalizes_types():
    response = '{"type": "Edge Case", "severity": "medium", "description": "Missing check"}\n'
    issues = parse_issues(response)
    assert len(issues) == 1
    assert issues[0]["type"] == "edge_case"


def test_parse_skips_malformed_lines():
    response = (
        "This is not JSON\n"
        '{"type": "correctness", "severity": "high", "description": "Real issue"}\n'
        "Also not JSON\n"
    )
    issues = parse_issues(response)
    assert len(issues) == 1


def test_parse_handles_markdown_list_markers():
    response = '- {"type": "correctness", "severity": "high", "description": "Bug"}\n'
    issues = parse_issues(response)
    assert len(issues) == 1


def test_check_self_caught_positive():
    desc = "No circular reference handling causes stack overflow"
    review = "the function does not handle circular references and will cause a stack overflow"
    assert check_self_caught(desc, review) is True


def test_check_self_caught_negative():
    desc = "No circular reference handling causes stack overflow"
    review = "The code looks correct. No issues found."
    assert check_self_caught(desc, review) is False


def test_check_self_caught_empty_review():
    desc = "Some issue description"
    assert check_self_caught(desc, "") is False
