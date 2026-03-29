#!/usr/bin/env python3
"""
Compute inter-reviewer agreement between primary and secondary reviewers.

Usage:
    python runner/validate_reviewers.py results/
    python runner/validate_reviewers.py results/ -o docs/validation.md
"""

import argparse
from math import sqrt
from pathlib import Path

from score import load_run


def find_dual_reviewed_runs(results_dir: Path) -> list[tuple[Path, dict]]:
    """Find runs that have both issues and issues_reviewer_2."""
    runs = []
    for results_file in sorted(results_dir.glob("*/results.yaml")):
        data = load_run(results_file)
        challenges = data.get("challenges", {})
        has_dual = any(
            "issues_reviewer_2" in cdata
            for cdata in challenges.values()
        )
        if has_dual:
            runs.append((results_file.parent, data))
    return runs


def compute_agreement(data: dict) -> dict:
    """Compute agreement metrics between two reviewers for one run."""
    challenges = data.get("challenges", {})

    r1_counts = []
    r2_counts = []
    r1_has = []
    r2_has = []
    r1_types = {"correctness": 0, "edge_case": 0, "security": 0, "style": 0}
    r2_types = {"correctness": 0, "edge_case": 0, "security": 0, "style": 0}

    for cid, cdata in challenges.items():
        issues1 = cdata.get("issues") or []
        issues2 = cdata.get("issues_reviewer_2") or []

        if "issues_reviewer_2" not in cdata:
            continue

        n1 = len(issues1)
        n2 = len(issues2)
        r1_counts.append(n1)
        r2_counts.append(n2)
        r1_has.append(1 if n1 > 0 else 0)
        r2_has.append(1 if n2 > 0 else 0)

        for issue in issues1:
            t = issue.get("type", "")
            if t in r1_types:
                r1_types[t] += 1
        for issue in issues2:
            t = issue.get("type", "")
            if t in r2_types:
                r2_types[t] += 1

    if not r1_counts:
        return {}

    n = len(r1_counts)

    # Issue count correlation (Pearson)
    mean1 = sum(r1_counts) / n
    mean2 = sum(r2_counts) / n
    cov = sum((a - mean1) * (b - mean2) for a, b in zip(r1_counts, r2_counts)) / n
    std1 = sqrt(sum((a - mean1) ** 2 for a in r1_counts) / n)
    std2 = sqrt(sum((b - mean2) ** 2 for b in r2_counts) / n)
    correlation = cov / (std1 * std2) if std1 > 0 and std2 > 0 else 0

    # Binary agreement and Cohen's kappa
    agree = sum(1 for a, b in zip(r1_has, r2_has) if a == b)
    pct_agree = agree / n

    # Cohen's kappa
    p1_yes = sum(r1_has) / n
    p2_yes = sum(r2_has) / n
    pe = p1_yes * p2_yes + (1 - p1_yes) * (1 - p2_yes)
    kappa = (pct_agree - pe) / (1 - pe) if pe < 1 else 1.0

    # Mean issue counts
    mean_r1 = sum(r1_counts) / n
    mean_r2 = sum(r2_counts) / n
    mean_abs_diff = sum(abs(a - b) for a, b in zip(r1_counts, r2_counts)) / n

    return {
        "n_challenges": n,
        "mean_issues_r1": mean_r1,
        "mean_issues_r2": mean_r2,
        "mean_abs_diff": mean_abs_diff,
        "correlation": correlation,
        "pct_agree": pct_agree,
        "kappa": kappa,
        "r1_types": r1_types,
        "r2_types": r2_types,
    }


def generate_report(runs: list[tuple[Path, dict]], all_agreements: list[dict]) -> str:
    """Generate validation report."""
    lines = ["# Inter-Reviewer Validation Report", ""]

    # Get reviewer info from first run
    first_data = runs[0][1]
    r1_info = first_data.get("independent_reviewer", {})
    r2_info = first_data.get("independent_reviewer_2", {})

    lines.append(f"Reviewer 1: {r1_info.get('model', 'unknown')}")
    lines.append(f"Reviewer 2: {r2_info.get('model', 'unknown')}")
    lines.append(f"Runs analyzed: {len(runs)}")
    lines.append("")

    # Per-run table
    lines.append("## Per-Run Agreement")
    lines.append("")
    lines.append("| Run | Challenges | R1 Issues | R2 Issues | Mean Δ | Correlation | Binary Agree | Kappa |")
    lines.append("|-----|-----------|-----------|-----------|--------|-------------|-------------|-------|")

    total_n = 0
    total_agree = 0

    for (run_dir, _), agreement in zip(runs, all_agreements):
        if not agreement:
            continue
        label = run_dir.name
        n = agreement["n_challenges"]
        lines.append(
            f"| {label} | {n} "
            f"| {agreement['mean_issues_r1']:.1f} "
            f"| {agreement['mean_issues_r2']:.1f} "
            f"| {agreement['mean_abs_diff']:.1f} "
            f"| {agreement['correlation']:.2f} "
            f"| {agreement['pct_agree']*100:.0f}% "
            f"| {agreement['kappa']:.2f} |"
        )
        total_n += n
        total_agree += int(agreement["pct_agree"] * n)

    lines.append("")

    # Aggregate summary
    valid = [a for a in all_agreements if a]
    if valid:
        avg_corr = sum(a["correlation"] for a in valid) / len(valid)
        avg_kappa = sum(a["kappa"] for a in valid) / len(valid)
        avg_agree = total_agree / total_n if total_n > 0 else 0
        avg_r1 = sum(a["mean_issues_r1"] for a in valid) / len(valid)
        avg_r2 = sum(a["mean_issues_r2"] for a in valid) / len(valid)

        lines.append("## Summary")
        lines.append("")
        lines.append(f"- **Mean issues (R1)**: {avg_r1:.1f}")
        lines.append(f"- **Mean issues (R2)**: {avg_r2:.1f}")
        lines.append(f"- **Issue count correlation**: {avg_corr:.2f}")
        lines.append(f"- **Binary agreement**: {avg_agree*100:.0f}%")
        lines.append(f"- **Cohen's kappa**: {avg_kappa:.2f}")
        lines.append("")

        # Interpretation
        if avg_kappa >= 0.8:
            interp = "Almost perfect agreement — reviewer scores are highly reliable."
        elif avg_kappa >= 0.6:
            interp = "Substantial agreement — reviewer scores are credible with caveats."
        elif avg_kappa >= 0.4:
            interp = "Moderate agreement — some subjectivity in scoring; results should be interpreted with caution."
        else:
            interp = "Fair/poor agreement — significant subjectivity in scoring; methodology needs revision."
        lines.append(f"**Interpretation**: {interp}")
        lines.append("")

        # Type distribution comparison
        lines.append("## Issue Type Distribution")
        lines.append("")
        lines.append("| Type | R1 Total | R2 Total |")
        lines.append("|------|----------|----------|")
        r1_total = {"correctness": 0, "edge_case": 0, "security": 0, "style": 0}
        r2_total = {"correctness": 0, "edge_case": 0, "security": 0, "style": 0}
        for a in valid:
            for t in r1_total:
                r1_total[t] += a["r1_types"].get(t, 0)
                r2_total[t] += a["r2_types"].get(t, 0)
        for t in ["correctness", "edge_case", "security", "style"]:
            lines.append(f"| {t} | {r1_total[t]} | {r2_total[t]} |")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Compute inter-reviewer agreement")
    parser.add_argument("results_dir", help="Path to results directory")
    parser.add_argument("-o", "--output", default=None, help="Output file (default: stdout)")
    args = parser.parse_args()

    runs = find_dual_reviewed_runs(Path(args.results_dir))

    if not runs:
        print("No runs with dual-reviewer data found.")
        print("Run review.py with --reviewer-number 2 first.")
        return

    print(f"Found {len(runs)} runs with dual-reviewer data")
    print()

    all_agreements = []
    for run_dir, data in runs:
        agreement = compute_agreement(data)
        all_agreements.append(agreement)

    report = generate_report(runs, all_agreements)

    if args.output:
        Path(args.output).write_text(report)
        print(f"Report written to: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
