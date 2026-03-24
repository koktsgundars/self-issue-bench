from score import score_run


def _make_run(challenges: dict) -> dict:
    return {"model": "test-model", "date": "2026-01-01", "challenges": challenges}


def test_empty_run():
    score = score_run(_make_run({}))
    assert score["total_issues"] == 0
    assert score["self_catch_rate"] is None
    assert score["model"] == "test-model"


def test_single_issue():
    run = _make_run({
        "c1_fibonacci": {
            "issues": [
                {"type": "correctness", "severity": "high", "description": "bug", "self_caught": True},
            ]
        }
    })
    score = score_run(run)
    assert score["total_issues"] == 1
    assert score["weighted_score"] == 3  # high=3
    assert score["by_type"]["correctness"] == 1
    assert score["by_severity"]["high"] == 1
    assert score["self_caught"] == 1
    assert score["self_catch_rate"] == 1.0


def test_multiple_issues_across_challenges():
    run = _make_run({
        "c1_fibonacci": {
            "issues": [
                {"type": "correctness", "severity": "high", "self_caught": True},
            ]
        },
        "c5_deep_clone": {
            "issues": [
                {"type": "edge_case", "severity": "medium", "self_caught": True},
                {"type": "edge_case", "severity": "low", "self_caught": False},
            ]
        },
    })
    score = score_run(run)
    assert score["total_issues"] == 3
    assert score["by_type"]["correctness"] == 1
    assert score["by_type"]["edge_case"] == 2
    assert score["self_caught"] == 2
    assert score["self_catch_rate"] == 2 / 3


def test_unknown_type_skipped():
    run = _make_run({
        "c1_fibonacci": {
            "issues": [
                {"type": "performance", "severity": "high", "self_caught": False},
                {"type": "correctness", "severity": "low", "self_caught": False},
            ]
        }
    })
    score = score_run(run)
    assert score["total_issues"] == 1  # "performance" skipped
    assert score["by_type"]["correctness"] == 1


def test_type_normalization_in_scoring():
    run = _make_run({
        "c1_fibonacci": {
            "issues": [
                {"type": "Edge Case", "severity": "medium", "self_caught": False},
                {"type": "safety", "severity": "high", "self_caught": True},
            ]
        }
    })
    score = score_run(run)
    assert score["total_issues"] == 2
    assert score["by_type"]["edge_case"] == 1
    assert score["by_type"]["security"] == 1


def test_weighted_score_mixed_severities():
    run = _make_run({
        "c1_fibonacci": {
            "issues": [
                {"type": "correctness", "severity": "high", "self_caught": False},
                {"type": "edge_case", "severity": "medium", "self_caught": False},
                {"type": "style", "severity": "low", "self_caught": False},
            ]
        }
    })
    score = score_run(run)
    assert score["total_issues"] == 3
    assert score["weighted_score"] == 6  # 3 + 2 + 1


def test_weighted_score_empty_run():
    score = score_run(_make_run({}))
    assert score["weighted_score"] == 0


def test_self_caught_by_type():
    run = _make_run({
        "c1_fibonacci": {
            "issues": [
                {"type": "correctness", "severity": "high", "self_caught": True},
                {"type": "correctness", "severity": "medium", "self_caught": False},
                {"type": "edge_case", "severity": "low", "self_caught": True},
            ]
        }
    })
    score = score_run(run)
    assert score["self_caught_by_type"]["correctness"] == 1
    assert score["self_caught_by_type"]["edge_case"] == 1
    assert score["self_caught_by_type"]["security"] == 0


def test_token_usage_extraction():
    run = _make_run({
        "c1_fibonacci": {
            "issues": [],
            "usage": {
                "generation": {"input_tokens": 50, "output_tokens": 100},
                "review": {"input_tokens": 200, "output_tokens": 80},
            },
        },
        "c5_deep_clone": {
            "issues": [{"type": "correctness", "severity": "high", "self_caught": False}],
            "usage": {
                "generation": {"input_tokens": 60, "output_tokens": 120},
                "review": {"input_tokens": 300, "output_tokens": 90},
            },
        },
    })
    score = score_run(run)
    assert score["total_gen_tokens"] == 330  # 50+100+60+120
    assert score["total_review_tokens"] == 670  # 200+80+300+90


def test_per_challenge_counts():
    run = _make_run({
        "c1_fibonacci": {"issues": []},
        "c5_deep_clone": {
            "issues": [
                {"type": "correctness", "severity": "high", "self_caught": False},
            ]
        },
    })
    score = score_run(run)
    assert score["per_challenge"]["c1_fibonacci"]["issue_count"] == 0
    assert score["per_challenge"]["c5_deep_clone"]["issue_count"] == 1
