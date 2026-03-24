from aggregate import aggregate_scores, parse_run_dir


def test_parse_run_dir_simple():
    label, run_num = parse_run_dir("opus-4_2026-03-21")
    assert label == "opus-4"
    assert run_num is None


def test_parse_run_dir_with_run_number():
    label, run_num = parse_run_dir("opus-4_run2_2026-03-21")
    assert label == "opus-4"
    assert run_num == 2


def test_parse_run_dir_complex_label():
    label, run_num = parse_run_dir("sonnet-4-strict-2pass_run1_2026-03-21")
    assert label == "sonnet-4-strict-2pass"
    assert run_num == 1


def test_aggregate_single_run():
    scores = [{
        "model": "test",
        "total_issues": 5,
        "weighted_score": 12,
        "by_type": {"correctness": 2, "edge_case": 3, "security": 0, "style": 0},
        "self_caught": 4,
        "self_catch_rate": 0.8,
        "per_challenge": {
            "c1_fibonacci": {"issue_count": 0, "by_type": {}},
            "c5_deep_clone": {"issue_count": 2, "by_type": {}},
        },
    }]
    agg = aggregate_scores(scores)
    assert agg["n_runs"] == 1
    assert agg["total_issues"]["mean"] == 5
    assert agg["total_issues"]["stddev"] == 0.0
    assert agg["weighted_score"]["mean"] == 12
    assert agg["self_catch_rate"]["mean"] == 0.8


def test_aggregate_multiple_runs():
    scores = [
        {
            "model": "test",
            "total_issues": 4,
            "weighted_score": 8,
            "by_type": {"correctness": 2, "edge_case": 2, "security": 0, "style": 0},
            "self_caught": 4,
            "self_catch_rate": 1.0,
            "per_challenge": {"c1_fibonacci": {"issue_count": 1, "by_type": {}}},
        },
        {
            "model": "test",
            "total_issues": 6,
            "weighted_score": 14,
            "by_type": {"correctness": 3, "edge_case": 3, "security": 0, "style": 0},
            "self_caught": 3,
            "self_catch_rate": 0.5,
            "per_challenge": {"c1_fibonacci": {"issue_count": 0, "by_type": {}}},
        },
    ]
    agg = aggregate_scores(scores)
    assert agg["n_runs"] == 2
    assert agg["total_issues"]["mean"] == 5.0
    assert agg["total_issues"]["min"] == 4
    assert agg["total_issues"]["max"] == 6
    assert agg["weighted_score"]["mean"] == 11.0
    assert agg["weighted_score"]["min"] == 8
    assert agg["weighted_score"]["max"] == 14
    assert agg["self_catch_rate"]["mean"] == 0.75
    assert agg["per_challenge"]["c1_fibonacci"]["has_issues_pct"] == 50.0
