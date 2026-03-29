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

from aggregate import aggregate_scores, gather_scores, gather_scores_by_date
from constants import CATEGORIES, CHALLENGE_IDS
from stats import bootstrap_diff_test


def section_model_summary(aggregates: dict) -> str:
    """Top-level summary with the metrics that matter most."""
    lines = ["## Model Summary", ""]
    lines.append("| Model | Test Pass Rate | First-Try Pass | Self-Catch Rate | Issues | Clean Challenges | Review-Test Agreement |")
    lines.append("|-------|---------------|----------------|-----------------|--------|-----------------|----------------------|")

    rows = []
    for label, agg in aggregates.items():
        tpr = agg.get("test_pass_rate")
        ftp = agg.get("first_try_pass_rate")
        scr = agg.get("self_catch_rate")
        ti = agg["total_issues"]["mean"]
        czi = agg.get("challenges_zero_issues")
        tra = agg.get("test_review_agreement")

        if tpr and tpr.get("ci_95"):
            ci = tpr["ci_95"]
            tpr_str = f"{tpr['mean']*100:.0f}% [{ci[0]*100:.0f}-{ci[1]*100:.0f}%]"
        elif tpr:
            tpr_str = f"{tpr['mean']*100:.0f}%"
        else:
            tpr_str = "-"

        ftp_str = f"{ftp['mean']*100:.0f}%" if ftp else "-"

        if scr and scr.get("ci_95"):
            ci = scr["ci_95"]
            scr_str = f"{scr['mean']*100:.0f}% [{ci[0]*100:.0f}-{ci[1]*100:.0f}%]"
        elif scr:
            scr_str = f"{scr['mean']*100:.0f}%"
        else:
            scr_str = "-"
        czi_str = f"{czi['mean']:.0f}/{len(CHALLENGE_IDS)}" if czi else "-"
        tra_str = f"{tra['mean']*100:.0f}%" if tra else "-"

        sort_key = tpr["mean"] if tpr else 0
        rows.append((sort_key, label, tpr_str, ftp_str, scr_str, f"{ti:.0f}", czi_str, tra_str))

    for _, label, tpr_str, ftp_str, scr_str, ti_str, czi_str, tra_str in sorted(rows, reverse=True):
        lines.append(f"| {label} | {tpr_str} | {ftp_str} | {scr_str} | {ti_str} | {czi_str} | {tra_str} |")

    lines.append("")
    return "\n".join(lines)


def section_significance_matrix(aggregates: dict) -> str:
    """Pairwise significance tests for test pass rate."""
    # Only include models with raw test pass rate values
    models = []
    for label, agg in sorted(aggregates.items()):
        vals = agg.get("test_pass_rate_values")
        if vals and len(vals) >= 3:
            models.append((label, vals))

    if len(models) < 2:
        return ""

    lines = ["## Statistical Significance (Test Pass Rate)", ""]
    lines.append("Pairwise bootstrap test (p < 0.05 = significant difference).")
    lines.append("")

    # Header
    labels = [m[0] for m in models]
    header = "| | " + " | ".join(labels) + " |"
    sep = "|---|" + "|".join(["---:" for _ in labels]) + "|"
    lines.append(header)
    lines.append(sep)

    for i, (label_a, vals_a) in enumerate(models):
        cells = []
        for j, (label_b, vals_b) in enumerate(models):
            if i == j:
                cells.append("—")
            elif i < j:
                p = bootstrap_diff_test(vals_a, vals_b)
                if p is not None and p < 0.05:
                    cells.append(f"**{p:.3f}**")
                elif p is not None:
                    cells.append(f"{p:.2f}")
                else:
                    cells.append("-")
            else:
                cells.append("")  # lower triangle left empty
        lines.append(f"| {label_a} | " + " | ".join(cells) + " |")

    lines.append("")
    lines.append("Bold = statistically significant (p < 0.05). Upper triangle only.")
    lines.append("")
    return "\n".join(lines)


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


def section_difficulty_tiers(groups: dict, aggregates: dict) -> str:
    """Classify challenges into difficulty tiers."""
    n_models = len(aggregates)
    challenge_stats = []

    for cid in CHALLENGE_IDS:
        models_with_issues = 0
        total_issues = 0
        for label, scores in groups.items():
            for s in scores:
                pc = s["per_challenge"].get(cid, {})
                if pc.get("issue_count", 0) > 0:
                    models_with_issues += 1
                    break
            for s in scores:
                pc = s["per_challenge"].get(cid, {})
                total_issues += pc.get("issue_count", 0)
        mean_issues = total_issues / sum(len(v) for v in groups.values()) if groups else 0
        challenge_stats.append((models_with_issues, mean_issues, cid))

    # Classify
    hard = [(m, i, c) for m, i, c in challenge_stats if m >= n_models * 0.75]
    medium = [(m, i, c) for m, i, c in challenge_stats if n_models * 0.38 <= m < n_models * 0.75]
    easy = [(m, i, c) for m, i, c in challenge_stats if 0 < m < n_models * 0.38]
    trivial = [(m, i, c) for m, i, c in challenge_stats if m == 0]

    lines = ["## Difficulty Tiers", ""]
    lines.append(f"Based on empirical failure rates across {n_models} models.")
    lines.append("")

    for tier_name, tier_data in [("Hard", hard), ("Medium", medium), ("Easy", easy), ("Trivial", trivial)]:
        if not tier_data:
            continue
        lines.append(f"### {tier_name} ({len(tier_data)} challenges)")
        lines.append("")
        lines.append("| Challenge | Models with Issues | Mean Issues |")
        lines.append("|-----------|-------------------|-------------|")
        for m, i, c in sorted(tier_data, reverse=True):
            lines.append(f"| {c} | {m}/{n_models} | {i:.1f} |")
        lines.append("")

    lines.append(f"**Distribution**: {len(hard)} hard, {len(medium)} medium, {len(easy)} easy, {len(trivial)} trivial")
    lines.append("")
    return "\n".join(lines)


def section_cost_effectiveness(aggregates: dict) -> str:
    """Cost-effectiveness analysis."""
    # Check if any model has cost data
    has_cost = any(
        agg.get("cost") and agg["cost"].get("mean") is not None
        for agg in aggregates.values()
    )
    if not has_cost:
        return ""

    lines = ["## Cost-Effectiveness", ""]
    lines.append("| Model | Cost/Run | Cost/Issue | Issues/$ | Test Pass Rate |")
    lines.append("|-------|---------|-----------|---------|---------------|")

    rows = []
    for label, agg in aggregates.items():
        cost = agg.get("cost")
        ti = agg["total_issues"]["mean"]
        tpr = agg.get("test_pass_rate")

        if not cost or cost.get("mean") is None:
            continue

        cost_val = cost["mean"]
        cost_per_issue = cost_val / ti if ti > 0 else 0
        issues_per_dollar = ti / cost_val if cost_val > 0 else 0
        tpr_str = f"{tpr['mean']*100:.0f}%" if tpr else "-"

        rows.append((issues_per_dollar, label, cost_val, cost_per_issue, issues_per_dollar, tpr_str))

    for _, label, cost, cpi, ipd, tpr_str in sorted(rows, reverse=True):
        lines.append(f"| {label} | ${cost:.2f} | ${cpi:.3f} | {ipd:.0f} | {tpr_str} |")

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


def section_test_results(aggregates: dict) -> str:
    """Test pass rates per model."""
    # Check if any model has test data
    has_tests = any(agg.get("test_pass_rate") for agg in aggregates.values())
    if not has_tests:
        return ""

    lines = ["## Test Pass Rates", ""]
    lines.append("| Model | Tests Passed | Total Tests | Pass Rate |")
    lines.append("|-------|-------------|-------------|-----------|")

    rows = []
    for label, agg in aggregates.items():
        tpr = agg.get("test_pass_rate")
        tr = agg.get("test_results")
        if tpr and tr:
            rate = tpr["mean"] * 100
            passed = tr["passed"]["mean"]
            total = tr["total"]["mean"]
            rows.append((rate, label, passed, total))

    for rate, label, passed, total in sorted(rows, reverse=True):
        lines.append(f"| {label} | {passed:.0f} | {total:.0f} | {rate:.0f}% |")

    lines.append("")
    return "\n".join(lines)


def section_fix_effectiveness(aggregates: dict) -> str:
    """Fix loop effectiveness per model."""
    has_fix = any(agg.get("fix") for agg in aggregates.values())
    if not has_fix:
        return ""

    lines = ["## Fix Effectiveness", ""]
    lines.append("| Model | Original Pass Rate | Fixed Pass Rate | Improvement | Regressions |")
    lines.append("|-------|--------------------|-----------------|-------------|-------------|")

    rows = []
    for label, agg in aggregates.items():
        tpr = agg.get("test_pass_rate")
        fpr = agg.get("fixed_pass_rate")
        fix = agg.get("fix")
        if tpr and fpr and fix:
            rows.append((
                fpr["mean"] * 100 - tpr["mean"] * 100,  # sort by improvement
                label,
                tpr["mean"] * 100,
                fpr["mean"] * 100,
                fix["improvement"]["mean"],
                fix["regression"]["mean"],
            ))

    for _, label, orig, fixed, imp, reg in sorted(rows, reverse=True):
        lines.append(f"| {label} | {orig:.0f}% | {fixed:.0f}% | +{imp:.1f} | -{reg:.1f} |")

    lines.append("")
    return "\n".join(lines)


def section_drift(results_dir: Path) -> str:
    """Show how model scores change over time."""
    by_date = gather_scores_by_date(results_dir)

    # Only include models with runs on multiple dates
    multi_date_models = {
        label: dates for label, dates in by_date.items()
        if len(dates) > 1
    }

    if not multi_date_models:
        return ""

    lines = ["## Score History", ""]
    lines.append("Models with runs on multiple dates, showing key metrics per date.")
    lines.append("")

    for label in sorted(multi_date_models):
        dates = multi_date_models[label]
        lines.append(f"### {label}")
        lines.append("")
        lines.append("| Date | Issues | Self-Catch | Test Pass | First-Try Pass |")
        lines.append("|------|--------|------------|-----------|---------------|")

        for run_date in sorted(dates):
            agg = aggregate_scores(dates[run_date])
            ti = agg["total_issues"]["mean"]
            scr = agg.get("self_catch_rate")
            tpr = agg.get("test_pass_rate")
            ftp = agg.get("first_try_pass_rate")

            scr_str = f"{scr['mean']*100:.0f}%" if scr else "-"
            tpr_str = f"{tpr['mean']*100:.0f}%" if tpr else "-"
            ftp_str = f"{ftp['mean']*100:.0f}%" if ftp else "-"

            lines.append(f"| {run_date} | {ti:.0f} | {scr_str} | {tpr_str} | {ftp_str} |")

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
        section_model_summary(aggregates),
        section_significance_matrix(aggregates),
        section_comparison_table(groups, aggregates),
        section_per_challenge(aggregates),
        section_challenge_type_profile(aggregates),
        section_discrimination(aggregates),
        section_difficulty_tiers(groups, aggregates),
        section_cost_effectiveness(aggregates),
        section_self_catch(aggregates),
        section_self_catch_by_type(aggregates),
        section_token_efficiency(aggregates),
        section_test_results(aggregates),
        section_fix_effectiveness(aggregates),
        section_drift(results_dir),
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
