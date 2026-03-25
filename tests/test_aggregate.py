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
    label, run_num = parse_run_dir("some-model-with-dashes_run1_2026-03-21")
    assert label == "some-model-with-dashes"
    assert run_num == 1


def _make_score(**overrides):
    """Build a minimal score dict with sensible defaults."""
    base = {
        "model": "test",
        "total_issues": 5,
        "weighted_score": 10,
        "by_type": {"correctness": 2, "edge_case": 3, "security": 0, "style": 0},
        "self_caught": 3,
        "self_caught_by_type": {"correctness": 1, "edge_case": 2, "security": 0, "style": 0},
        "self_catch_rate": 0.6,
        "tokens": {"generation": 500, "review": 1000},
        "per_challenge": {
            "c1_fibonacci": {"issue_count": 0, "by_type": {"correctness": 0, "edge_case": 0, "security": 0, "style": 0}},
            "c5_deep_clone": {"issue_count": 2, "by_type": {"correctness": 1, "edge_case": 1, "security": 0, "style": 0}},
        },
    }
    base.update(overrides)
    return base


def test_aggregate_single_run():
    scores = [_make_score()]
    agg = aggregate_scores(scores)
    assert agg["n_runs"] == 1
    assert agg["total_issues"]["mean"] == 5
    assert agg["total_issues"]["stddev"] == 0.0
    assert agg["weighted_score"]["mean"] == 10
    assert agg["self_catch_rate"]["mean"] == 0.6
    # Token aggregation
    assert agg["tokens"]["generation"]["mean"] == 500
    assert agg["tokens"]["review"]["mean"] == 1000
    assert agg["tokens"]["total"]["mean"] == 1500
    assert agg["tokens"]["review_tokens_per_issue"] == 200.0  # 1000/5
    # Self-catch by type
    assert agg["self_catch_by_type"]["correctness"]["caught"] == 1
    assert agg["self_catch_by_type"]["correctness"]["total"] == 2
    assert agg["self_catch_by_type"]["correctness"]["rate"] == 0.5
    assert agg["self_catch_by_type"]["security"]["rate"] is None
    # Per-challenge type totals
    assert agg["per_challenge"]["c5_deep_clone"]["type_totals"]["correctness"] == 1


def test_aggregate_multiple_runs():
    scores = [
        _make_score(total_issues=4, weighted_score=8,
                    by_type={"correctness": 2, "edge_case": 2, "security": 0, "style": 0},
                    self_caught=4, self_catch_rate=1.0,
                    self_caught_by_type={"correctness": 2, "edge_case": 2, "security": 0, "style": 0},
                    tokens={"generation": 400, "review": 800},
                    per_challenge={"c1_fibonacci": {"issue_count": 1, "by_type": {"correctness": 1, "edge_case": 0, "security": 0, "style": 0}}}),
        _make_score(total_issues=6, weighted_score=14,
                    by_type={"correctness": 3, "edge_case": 3, "security": 0, "style": 0},
                    self_caught=3, self_catch_rate=0.5,
                    self_caught_by_type={"correctness": 1, "edge_case": 2, "security": 0, "style": 0},
                    tokens={"generation": 600, "review": 1200},
                    per_challenge={"c1_fibonacci": {"issue_count": 0, "by_type": {"correctness": 0, "edge_case": 0, "security": 0, "style": 0}}}),
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
    # Token aggregation across runs
    assert agg["tokens"]["generation"]["mean"] == 500
    assert agg["tokens"]["review"]["mean"] == 1000
    # Self-catch by type across runs: 3 caught out of 5 correctness
    assert agg["self_catch_by_type"]["correctness"]["caught"] == 3
    assert agg["self_catch_by_type"]["correctness"]["total"] == 5
    # Per-challenge type totals summed across runs
    assert agg["per_challenge"]["c1_fibonacci"]["type_totals"]["correctness"] == 1
