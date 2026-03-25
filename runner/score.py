#!/usr/bin/env python3
"""Score a single benchmark run from its YAML results file."""

import sys
from pathlib import Path

import yaml
from constants import CATEGORIES, CHALLENGE_IDS, SEVERITIES, SEVERITY_WEIGHTS, normalize_issue_type


def load_run(path: Path) -> dict:
    results_file = path / "results.yaml" if path.is_dir() else path
    with open(results_file) as f:
        return yaml.safe_load(f)


def score_run(data: dict) -> dict:
    totals = {cat: 0 for cat in CATEGORIES}
    severity_counts = {sev: 0 for sev in SEVERITIES}
    self_caught = 0
    self_caught_by_type = {cat: 0 for cat in CATEGORIES}
    total_issues = 0
    weighted_score = 0
    total_gen_tokens = 0
    total_review_tokens = 0
    per_challenge = {}

    for cid in CHALLENGE_IDS:
        challenge = data.get("challenges", {}).get(cid, {})
        issues = challenge.get("issues") or []
        c_totals = {cat: 0 for cat in CATEGORIES}

        for issue in issues:
            itype = normalize_issue_type(issue.get("type", ""))
            if itype is None:
                continue

            totals[itype] += 1
            c_totals[itype] += 1

            sev = issue.get("severity", "").lower()
            if sev in severity_counts:
                severity_counts[sev] += 1
            weighted_score += SEVERITY_WEIGHTS.get(sev, 1)

            total_issues += 1
            if issue.get("self_caught", False):
                self_caught += 1
                self_caught_by_type[itype] += 1

        # Token usage
        usage = challenge.get("usage", {})
        gen = usage.get("generation", {})
        rev = usage.get("review", {})
        rev2 = usage.get("review_2", {})
        total_gen_tokens += gen.get("input_tokens", 0) + gen.get("output_tokens", 0)
        total_review_tokens += rev.get("input_tokens", 0) + rev.get("output_tokens", 0)
        total_review_tokens += rev2.get("input_tokens", 0) + rev2.get("output_tokens", 0)

        # Test results (if available)
        test_results = challenge.get("test_results")
        c_test = None
        if test_results:
            c_test = {
                "passed": test_results.get("passed", 0),
                "failed": test_results.get("failed", 0),
                "errors": test_results.get("errors", 0),
                "total": test_results.get("total", 0),
                "compile_error": bool(test_results.get("compile_error")),
            }

        # Fixed test results (if available)
        test_results_fixed = challenge.get("test_results_fixed")
        c_test_fixed = None
        if test_results_fixed:
            c_test_fixed = {
                "passed": test_results_fixed.get("passed", 0),
                "failed": test_results_fixed.get("failed", 0),
                "errors": test_results_fixed.get("errors", 0),
                "total": test_results_fixed.get("total", 0),
                "compile_error": bool(test_results_fixed.get("compile_error")),
            }

        per_challenge[cid] = {
            "issue_count": len(issues),
            "by_type": c_totals,
            "tests": c_test,
            "tests_fixed": c_test_fixed,
        }

    self_catch_rate = self_caught / total_issues if total_issues > 0 else None

    # Aggregate test results across challenges
    total_test_passed = 0
    total_test_count = 0
    challenges_tested = 0
    challenges_all_pass = 0
    for cid in CHALLENGE_IDS:
        c = per_challenge.get(cid, {})
        t = c.get("tests")
        if t and t["total"] > 0:
            challenges_tested += 1
            total_test_passed += t["passed"]
            total_test_count += t["total"]
            if t["passed"] == t["total"]:
                challenges_all_pass += 1

    test_pass_rate = total_test_passed / total_test_count if total_test_count > 0 else None

    # Aggregate fixed test results
    total_fixed_passed = 0
    total_fixed_count = 0
    fix_improvement = 0
    fix_regression = 0
    challenges_with_fix = 0
    for cid in CHALLENGE_IDS:
        c = per_challenge.get(cid, {})
        orig = c.get("tests")
        fixed = c.get("tests_fixed")
        if orig and fixed and orig["total"] > 0 and fixed["total"] > 0:
            challenges_with_fix += 1
            total_fixed_passed += fixed["passed"]
            total_fixed_count += fixed["total"]
            fix_improvement += max(0, fixed["passed"] - orig["passed"])
            fix_regression += max(0, orig["passed"] - fixed["passed"])

    fixed_pass_rate = total_fixed_passed / total_fixed_count if total_fixed_count > 0 else None

    return {
        "model": data.get("model", "unknown"),
        "date": data.get("date", ""),
        "total_issues": total_issues,
        "weighted_score": weighted_score,
        "by_type": totals,
        "by_severity": severity_counts,
        "self_caught": self_caught,
        "self_caught_by_type": self_caught_by_type,
        "self_catch_rate": self_catch_rate,
        "tokens": {
            "generation": total_gen_tokens,
            "review": total_review_tokens,
        },
        "per_challenge": per_challenge,
        "test_pass_rate": test_pass_rate,
        "tests": {
            "passed": total_test_passed,
            "total": total_test_count,
            "challenges_tested": challenges_tested,
            "challenges_all_pass": challenges_all_pass,
        },
        "fixed_pass_rate": fixed_pass_rate,
        "fix": {
            "passed": total_fixed_passed,
            "total": total_fixed_count,
            "improvement": fix_improvement,
            "regression": fix_regression,
            "net": fix_improvement - fix_regression,
            "challenges_with_fix": challenges_with_fix,
        } if challenges_with_fix > 0 else None,
    }


def print_scorecard(score: dict) -> None:
    print(f"Model: {score['model']}")
    print(f"Date:  {score['date']}")
    print(f"Total issues: {score['total_issues']}")
    print(f"Weighted score: {score['weighted_score']} (high=3, medium=2, low=1)")
    print()

    print("By type:")
    for cat in CATEGORIES:
        print(f"  {cat:15s} {score['by_type'][cat]}")
    print()

    print("By severity:")
    for sev in SEVERITIES:
        print(f"  {sev:15s} {score['by_severity'][sev]}")
    print()

    if score["self_catch_rate"] is not None:
        pct = score["self_catch_rate"] * 100
        print(f"Self-caught: {score['self_caught']}/{score['total_issues']} ({pct:.0f}%)")
    else:
        print("Self-caught: no issues found")
    print()

    header = f"{'Challenge':20s} {'Total':>6s} " + " ".join(
        f"{c:>12s}" for c in CATEGORIES
    )
    print(header)
    print("-" * len(header))
    for cid in CHALLENGE_IDS:
        c = score["per_challenge"].get(cid, {})
        count = c.get("issue_count", 0)
        by_type = c.get("by_type", {})
        row = f"{cid:20s} {count:>6d} " + " ".join(
            f"{by_type.get(cat, 0):>12d}" for cat in CATEGORIES
        )
        print(row)

    total = score["total_issues"]
    print()
    if total <= 2:
        print("Signal: Excellent output quality on trivial tasks")
    elif total <= 8:
        print("Signal: Expected baseline — review pass adds meaningful value")
    elif total <= 16:
        print("Signal: Notable self-issue rate — systematic review needed")
    else:
        print("Signal: High self-issue rate — review architecture is not optional")


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <run-dir-or-yaml>")
        sys.exit(1)

    path = Path(sys.argv[1])
    data = load_run(path)
    score = score_run(data)
    print_scorecard(score)


if __name__ == "__main__":
    main()
