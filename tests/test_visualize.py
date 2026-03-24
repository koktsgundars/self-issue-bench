"""Tests for heatmap visualization."""

from visualize import generate_heatmap


def _make_aggregate(label, per_challenge=None):
    pc = per_challenge or {}
    return {
        "label": label,
        "n_runs": 1,
        "total_issues": {"mean": 5, "stddev": 0, "min": 5, "max": 5},
        "per_challenge": pc,
    }


def test_heatmap_generates_valid_html():
    aggs = {
        "model-a": _make_aggregate("model-a", {
            "c5_deep_clone": {"mean_issues": 3, "has_issues_pct": 100},
            "c9_url_parser": {"mean_issues": 5, "has_issues_pct": 100},
        }),
        "model-b": _make_aggregate("model-b", {
            "c5_deep_clone": {"mean_issues": 1, "has_issues_pct": 100},
            "c9_url_parser": {"mean_issues": 0, "has_issues_pct": 0},
        }),
    }
    html = generate_heatmap(aggs)
    assert "<!DOCTYPE html>" in html
    assert "<svg" in html
    assert "model-a" in html
    assert "model-b" in html
    assert "deep clone" in html.lower()


def test_heatmap_skips_zero_issue_challenges():
    aggs = {
        "model-a": _make_aggregate("model-a", {
            "c1_fibonacci": {"mean_issues": 0, "has_issues_pct": 0},
            "c5_deep_clone": {"mean_issues": 2, "has_issues_pct": 100},
        }),
    }
    html = generate_heatmap(aggs)
    assert "deep clone" in html.lower()
    assert "fibonacci" not in html.lower()


def test_heatmap_empty_aggregates():
    html = generate_heatmap({})
    assert "<svg" in html
