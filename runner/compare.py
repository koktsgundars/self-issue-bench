#!/usr/bin/env python3
"""Compare scored runs across multiple models."""

import sys
from pathlib import Path

from constants import CATEGORIES
from score import load_run, score_run


def find_runs(results_dir: Path) -> list[Path]:
    """Find all results.yaml files under the results directory."""
    return sorted(results_dir.glob("*/results.yaml"))


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <results-dir>")
        sys.exit(1)

    results_dir = Path(sys.argv[1])
    run_files = find_runs(results_dir)

    if not run_files:
        print(f"No results.yaml files found under {results_dir}")
        sys.exit(1)

    scores = []
    for rf in run_files:
        data = load_run(rf)
        scores.append(score_run(data))

    # Summary table
    model_col = max(len(s["model"]) for s in scores)
    model_col = max(model_col, 5)  # min width

    header = f"{'Model':<{model_col}s}  {'Total':>5s}  " + "  ".join(
        f"{c[:4]:>4s}" for c in CATEGORIES
    ) + f"  {'Caught':>6s}  {'Rate':>5s}"
    print(header)
    print("-" * len(header))

    for s in scores:
        rate = f"{s['self_catch_rate'] * 100:.0f}%" if s["self_catch_rate"] is not None else "n/a"
        row = (
            f"{s['model']:<{model_col}s}  {s['total_issues']:>5d}  "
            + "  ".join(f"{s['by_type'][c]:>4d}" for c in CATEGORIES)
            + f"  {s['self_caught']:>6d}  {rate:>5s}"
        )
        print(row)


if __name__ == "__main__":
    main()
