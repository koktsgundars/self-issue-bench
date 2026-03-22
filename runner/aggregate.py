#!/usr/bin/env python3
"""
Aggregate multiple benchmark runs for the same model.

Groups runs by label, computes mean/stddev/min/max for key metrics.

Usage:
    python runner/aggregate.py results/
    python runner/aggregate.py results/ --label opus-4
"""

import argparse
import re
import sys
from collections import defaultdict
from math import sqrt
from pathlib import Path

from constants import CATEGORIES, CHALLENGE_IDS
from score import load_run, score_run


def parse_run_dir(dirname: str) -> tuple[str, int | None]:
    """Extract label and run number from directory name.

    Examples:
        'opus-4_2026-03-21' -> ('opus-4', None)
        'opus-4_run2_2026-03-21' -> ('opus-4', 2)
    """
    match = re.match(r"^(.+?)(?:_run(\d+))?_(\d{4}-\d{2}-\d{2})$", dirname)
    if not match:
        return dirname, None
    label = match.group(1)
    run_num = int(match.group(2)) if match.group(2) else None
    return label, run_num


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def stddev(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = mean(values)
    return sqrt(sum((x - m) ** 2 for x in values) / (len(values) - 1))


def aggregate_scores(scores: list[dict]) -> dict:
    """Compute aggregate statistics across multiple scored runs."""
    n = len(scores)
    totals = [s["total_issues"] for s in scores]
    rates = [s["self_catch_rate"] for s in scores if s["self_catch_rate"] is not None]

    by_type = {}
    for cat in CATEGORIES:
        vals = [s["by_type"][cat] for s in scores]
        by_type[cat] = {"mean": mean(vals), "stddev": stddev(vals)}

    # Per-challenge: how often each challenge has issues
    per_challenge = {}
    for cid in CHALLENGE_IDS:
        counts = [s["per_challenge"].get(cid, {}).get("issue_count", 0) for s in scores]
        per_challenge[cid] = {
            "mean_issues": mean(counts),
            "has_issues_pct": sum(1 for c in counts if c > 0) / n * 100,
        }

    return {
        "label": scores[0].get("model", "unknown"),
        "n_runs": n,
        "total_issues": {"mean": mean(totals), "stddev": stddev(totals), "min": min(totals), "max": max(totals)},
        "self_catch_rate": {"mean": mean(rates), "stddev": stddev(rates)} if rates else None,
        "by_type": by_type,
        "per_challenge": per_challenge,
    }


def gather_scores(results_dir: Path, label_filter: str | None = None) -> dict[str, list[dict]]:
    """Group and score all runs by label."""
    groups = defaultdict(list)
    for results_file in sorted(results_dir.glob("*/results.yaml")):
        dirname = results_file.parent.name
        label, _ = parse_run_dir(dirname)
        if label_filter and label != label_filter:
            continue
        data = load_run(results_file)
        score = score_run(data)
        groups[label].append(score)
    return dict(groups)


def main():
    parser = argparse.ArgumentParser(description="Aggregate multiple benchmark runs")
    parser.add_argument("results_dir", help="Path to results directory")
    parser.add_argument("--label", default=None, help="Filter to a specific label")
    args = parser.parse_args()

    groups = gather_scores(Path(args.results_dir), args.label)

    if not groups:
        print("No runs found")
        sys.exit(1)

    for label, scores in sorted(groups.items()):
        agg = aggregate_scores(scores)
        n = agg["n_runs"]

        print(f"Label: {label} ({n} run{'s' if n > 1 else ''})")

        ti = agg["total_issues"]
        if n > 1:
            print(f"Total issues: {ti['mean']:.1f} +/- {ti['stddev']:.1f} (range: {ti['min']}-{ti['max']})")
        else:
            print(f"Total issues: {ti['mean']:.0f}")

        print("By type:")
        for cat in CATEGORIES:
            bt = agg["by_type"][cat]
            if n > 1:
                print(f"  {cat:15s} {bt['mean']:.1f} +/- {bt['stddev']:.1f}")
            else:
                print(f"  {cat:15s} {bt['mean']:.0f}")

        scr = agg["self_catch_rate"]
        if scr:
            if n > 1:
                print(f"Self-catch rate: {scr['mean']*100:.0f}% +/- {scr['stddev']*100:.0f}%")
            else:
                print(f"Self-catch rate: {scr['mean']*100:.0f}%")

        # Per-challenge (only show challenges that had issues)
        print("Per-challenge issue frequency:")
        for cid in CHALLENGE_IDS:
            pc = agg["per_challenge"][cid]
            if pc["mean_issues"] > 0 or pc["has_issues_pct"] > 0:
                print(f"  {cid:28s} mean={pc['mean_issues']:.1f}  appeared={pc['has_issues_pct']:.0f}%")

        print()


if __name__ == "__main__":
    main()
