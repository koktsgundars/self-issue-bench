#!/usr/bin/env python3
"""
Generate a markdown summary report from benchmark results.

Usage:
    python runner/report.py results/
    python runner/report.py results/ -o docs/report.md
"""

import argparse
from datetime import datetime
from pathlib import Path

from aggregate import aggregate_scores, gather_scores
from constants import CATEGORIES, CHALLENGE_IDS


def section_comparison_table(groups: dict, aggregates: dict) -> str:
    """Cross-model comparison table."""
    lines = ["## Cross-Model Comparison", ""]

    lines.append("| Model | Runs | Total Issues | Weighted | Correctness | Edge Case | Security | Style | Self-Catch Rate |")
    lines.append("|-------|------|-------------|---------|-------------|-----------|----------|-------|----------------|")

    rows = []
    for label in sorted(groups):
        agg = aggregates[label]
        n = agg["n_runs"]
        ti = agg["total_issues"]
        scr = agg["self_catch_rate"]

        ws = agg["weighted_score"]
        if n > 1:
            total_str = f"{ti['mean']:.1f} +/- {ti['stddev']:.1f}"
            ws_str = f"{ws['mean']:.1f} +/- {ws['stddev']:.1f}"
            rate_str = f"{scr['mean']*100:.0f}% +/- {scr['stddev']*100:.0f}%" if scr else "n/a"
            type_strs = [f"{agg['by_type'][c]['mean']:.1f}" for c in CATEGORIES]
        else:
            total_str = f"{ti['mean']:.0f}"
            ws_str = f"{ws['mean']:.0f}"
            rate_str = f"{scr['mean']*100:.0f}%" if scr else "n/a"
            type_strs = [f"{agg['by_type'][c]['mean']:.0f}" for c in CATEGORIES]

        rows.append((ti["mean"], label, n, total_str, ws_str, type_strs, rate_str))

    for _, label, n, total_str, ws_str, type_strs, rate_str in sorted(rows):
        lines.append(
            f"| {label} | {n} | {total_str} | {ws_str} | "
            + " | ".join(type_strs)
            + f" | {rate_str} |"
        )

    lines.append("")
    return "\n".join(lines)


def section_per_challenge(aggregates: dict) -> str:
    """Per-challenge breakdown across models."""
    lines = ["## Per-Challenge Breakdown", ""]
    labels = sorted(aggregates.keys())

    header = "| Challenge | " + " | ".join(labels) + " |"
    sep = "|-----------|" + "|".join(["---:" for _ in labels]) + "|"
    lines.append(header)
    lines.append(sep)

    for cid in CHALLENGE_IDS:
        cells = []
        for label in labels:
            agg = aggregates[label]
            avg = agg["per_challenge"].get(cid, {}).get("mean_issues", 0)
            if agg["n_runs"] > 1:
                cells.append(f"{avg:.1f}")
            else:
                cells.append(f"{int(avg)}" if avg > 0 else "-")
        lines.append(f"| {cid} | " + " | ".join(cells) + " |")

    lines.append("")
    return "\n".join(lines)


def section_challenge_type_profile(aggregates: dict) -> str:
    """Issue type breakdown per challenge, averaged per model then summed."""
    lines = ["## Issue Types by Challenge", ""]
    lines.append("Mean issues of each type per model, summed across all models.")
    lines.append("")
    lines.append("| Challenge | Correctness | Edge Case | Security | Style | Total |")
    lines.append("|-----------|-------------|-----------|----------|-------|-------|")

    for cid in CHALLENGE_IDS:
        type_totals = {cat: 0.0 for cat in CATEGORIES}
        for agg in aggregates.values():
            tt = agg["per_challenge"].get(cid, {}).get("type_totals", {})
            n = agg["n_runs"]
            for cat in CATEGORIES:
                type_totals[cat] += tt.get(cat, 0) / n
        total = sum(type_totals.values())
        if total == 0:
            continue
        cells = [f"{type_totals[c]:.0f}" for c in CATEGORIES]
        lines.append(f"| {cid} | " + " | ".join(cells) + f" | {total:.0f} |")

    lines.append("")
    return "\n".join(lines)


def section_discrimination(aggregates: dict) -> str:
    """Which challenges best separate models."""
    lines = ["## Challenge Discrimination", ""]
    lines.append("Challenges ranked by how many models have issues (higher = more discriminating).")
    lines.append("")
    lines.append("| Challenge | Models with Issues | Total Issues Across Models |")
    lines.append("|-----------|-------------------|---------------------------|")

    challenge_stats = []
    for cid in CHALLENGE_IDS:
        models_with_issues = 0
        total = 0
        for label, agg in aggregates.items():
            avg = agg["per_challenge"].get(cid, {}).get("mean_issues", 0)
            if avg > 0:
                models_with_issues += 1
                total += avg
        challenge_stats.append((models_with_issues, total, cid))

    for models, total, cid in sorted(challenge_stats, reverse=True):
        if models > 0:
            lines.append(f"| {cid} | {models}/{len(aggregates)} | {total:.0f} |")

    trivial = [cid for m, _, cid in challenge_stats if m == 0]
    if trivial:
        lines.append("")
        lines.append(f"**Trivial challenges** (no issues across any model): {', '.join(trivial)}")

    lines.append("")
    return "\n".join(lines)


def section_self_catch(aggregates: dict) -> str:
    """Self-catch rate analysis."""
    lines = ["## Self-Catch Analysis", ""]
    lines.append("| Model | Self-Catch Rate | Issues Caught | Issues Missed |")
    lines.append("|-------|----------------|---------------|---------------|")

    rows = []
    for label, agg in sorted(aggregates.items()):
        scr = agg["self_catch_rate"]
        ti = agg["total_issues"]["mean"]
        if scr and ti > 0:
            rate = scr["mean"] * 100
            caught = ti * scr["mean"]
            missed = ti - caught
            rows.append((rate, label, f"{caught:.0f}", f"{missed:.0f}"))
        else:
            rows.append((100.0, label, "-", "-"))

    for rate, label, caught, missed in sorted(rows, reverse=True):
        lines.append(f"| {label} | {rate:.0f}% | {caught} | {missed} |")

    lines.append("")
    return "\n".join(lines)


def section_self_catch_by_type(aggregates: dict) -> str:
    """Self-catch rate broken down by issue type across models."""
    lines = ["## Self-Catch Rate by Issue Type", ""]
    lines.append("| Model | Correctness | Edge Case | Security | Style |")
    lines.append("|-------|-------------|-----------|----------|-------|")

    for label in sorted(aggregates):
        agg = aggregates[label]
        scbt = agg.get("self_catch_by_type", {})
        cells = []
        for cat in CATEGORIES:
            info = scbt.get(cat, {})
            if info.get("total", 0) > 0:
                cells.append(f"{info['rate']*100:.0f}% ({info['caught']}/{info['total']})")
            else:
                cells.append("-")
        lines.append(f"| {label} | " + " | ".join(cells) + " |")

    lines.append("")
    return "\n".join(lines)


def section_token_efficiency(aggregates: dict) -> str:
    """Token usage and efficiency analysis."""
    lines = ["## Token Efficiency", ""]
    lines.append("| Model | Gen Tokens | Review Tokens | Total Tokens | Review Tokens/Issue |")
    lines.append("|-------|-----------|--------------|-------------|-------------------|")

    rows = []
    for label, agg in aggregates.items():
        tok = agg.get("tokens", {})
        gen = tok.get("generation", {}).get("mean", 0)
        rev = tok.get("review", {}).get("mean", 0)
        total = tok.get("total", {}).get("mean", 0)
        rpi = tok.get("review_tokens_per_issue")
        rpi_str = f"{rpi:.0f}" if rpi is not None else "-"
        rows.append((total, label, gen, rev, rpi_str))

    for total, label, gen, rev, rpi_str in sorted(rows):
        lines.append(f"| {label} | {gen:,.0f} | {rev:,.0f} | {total:,.0f} | {rpi_str} |")

    lines.append("")
    return "\n".join(lines)


def section_findings(aggregates: dict) -> str:
    """Auto-generated key findings."""
    lines = ["## Key Findings", ""]

    by_issues = []
    by_catch = []
    for label, agg in aggregates.items():
        by_issues.append((agg["total_issues"]["mean"], label))
        if agg["self_catch_rate"]:
            by_catch.append((agg["self_catch_rate"]["mean"], label))

    by_issues.sort()
    by_catch.sort(reverse=True)

    if by_issues:
        best = by_issues[0]
        worst = by_issues[-1]
        lines.append(f"- **Fewest issues**: {best[1]} ({best[0]:.0f} issues)")
        lines.append(f"- **Most issues**: {worst[1]} ({worst[0]:.0f} issues)")

    if by_catch:
        best_c = by_catch[0]
        worst_c = by_catch[-1]
        lines.append(f"- **Best self-catch rate**: {best_c[1]} ({best_c[0]*100:.0f}%)")
        lines.append(f"- **Worst self-catch rate**: {worst_c[1]} ({worst_c[0]*100:.0f}%)")

    lines.append("")
    return "\n".join(lines)


def generate_report(results_dir: Path) -> str:
    """Generate full markdown report."""
    groups = gather_scores(results_dir)

    if not groups:
        return "No results found."

    # Compute aggregates once, pass to all sections
    aggregates = {label: aggregate_scores(scores) for label, scores in groups.items()}

    sections = [
        "# Self-Issue Benchmark Report",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"Models compared: {len(groups)}",
        f"Challenges: {len(CHALLENGE_IDS)}",
        "",
        section_comparison_table(groups, aggregates),
        section_per_challenge(aggregates),
        section_challenge_type_profile(aggregates),
        section_discrimination(aggregates),
        section_self_catch(aggregates),
        section_self_catch_by_type(aggregates),
        section_token_efficiency(aggregates),
        section_findings(aggregates),
    ]

    return "\n".join(sections)


def main():
    parser = argparse.ArgumentParser(description="Generate benchmark summary report")
    parser.add_argument("results_dir", help="Path to results directory")
    parser.add_argument("-o", "--output", default=None, help="Output file (default: stdout)")
    args = parser.parse_args()

    report = generate_report(Path(args.results_dir))

    if args.output:
        Path(args.output).write_text(report)
        print(f"Report written to: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
