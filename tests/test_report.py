"""Smoke tests for report section functions — catch key errors and basic formatting."""

from report import (
    section_challenge_type_profile,
    section_comparison_table,
    section_self_catch_by_type,
    section_token_efficiency,
)


def _make_aggregate(**overrides):
    base = {
        "n_runs": 1,
        "total_issues": {"mean": 5, "stddev": 0, "min": 5, "max": 5},
        "weighted_score": {"mean": 10, "stddev": 0, "min": 10, "max": 10},
        "self_catch_rate": {"mean": 0.6, "stddev": 0},
        "self_catch_by_type": {
            "correctness": {"caught": 1, "total": 2, "rate": 0.5},
            "edge_case": {"caught": 2, "total": 3, "rate": 0.67},
            "security": {"caught": 0, "total": 0, "rate": None},
            "style": {"caught": 0, "total": 0, "rate": None},
        },
        "by_type": {
            "correctness": {"mean": 2, "stddev": 0},
            "edge_case": {"mean": 3, "stddev": 0},
            "security": {"mean": 0, "stddev": 0},
            "style": {"mean": 0, "stddev": 0},
        },
        "per_challenge": {
            "c5_deep_clone": {
                "mean_issues": 2,
                "has_issues_pct": 100,
                "type_totals": {"correctness": 1, "edge_case": 1, "security": 0, "style": 0},
            },
        },
        "tokens": {
            "generation": {"mean": 500},
            "review": {"mean": 1000},
            "total": {"mean": 1500},
            "review_tokens_per_issue": 200,
        },
    }
    base.update(overrides)
    return base


def test_comparison_table_renders():
    aggs = {"model-a": _make_aggregate()}
    groups = {"model-a": [{}]}
    result = section_comparison_table(groups, aggs)
    assert "model-a" in result
    assert "Weighted" in result


def test_challenge_type_profile_renders():
    aggs = {"model-a": _make_aggregate()}
    result = section_challenge_type_profile(aggs)
    assert "c5_deep_clone" in result
    assert "Issue Types by Challenge" in result


def test_self_catch_by_type_renders():
    aggs = {"model-a": _make_aggregate()}
    result = section_self_catch_by_type(aggs)
    assert "50%" in result  # correctness catch rate
    assert "-" in result  # security has no issues


def test_token_efficiency_renders():
    aggs = {"model-a": _make_aggregate()}
    result = section_token_efficiency(aggs)
    assert "500" in result
    assert "1,000" in result
    assert "200" in result
