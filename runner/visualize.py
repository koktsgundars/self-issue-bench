#!/usr/bin/env python3
"""
Generate an HTML heatmap visualization of benchmark results.

Usage:
    python runner/visualize.py results/ -o docs/heatmap.html
"""

import argparse
from pathlib import Path

from aggregate import aggregate_scores, gather_scores
from constants import CHALLENGE_IDS


def _color(value, max_value):
    """Map a value to a green-yellow-red color. 0=green, max=red."""
    if max_value == 0 or value == 0:
        return "#22c55e"  # green
    ratio = min(value / max_value, 1.0)
    if ratio < 0.5:
        # green to yellow
        r = int(34 + (250 - 34) * (ratio * 2))
        g = int(197 - (197 - 204) * (ratio * 2))
        b = int(94 - (94 - 0) * (ratio * 2))
    else:
        # yellow to red
        t = (ratio - 0.5) * 2
        r = int(250 + (239 - 250) * t)
        g = int(204 - (204 - 68) * t)
        b = int(0 + (68 - 0) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


def generate_heatmap(aggregates: dict) -> str:
    """Generate a self-contained HTML heatmap."""
    labels = sorted(aggregates.keys(), key=lambda lab: aggregates[lab]["total_issues"]["mean"])

    # Build data matrix
    matrix = {}
    max_val = 0
    for label in labels:
        agg = aggregates[label]
        for cid in CHALLENGE_IDS:
            val = agg["per_challenge"].get(cid, {}).get("mean_issues", 0)
            matrix[(label, cid)] = val
            if val > max_val:
                max_val = val

    # Filter to challenges that have at least one issue
    active_challenges = [cid for cid in CHALLENGE_IDS
                         if any(matrix.get((lab, cid), 0) > 0 for lab in labels)]

    cell_w, cell_h = 48, 32
    label_w = 200
    header_h = 140
    w = label_w + len(active_challenges) * cell_w + 20
    h = header_h + len(labels) * cell_h + 60

    svg_parts = []
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
                     f'font-family="system-ui, sans-serif" font-size="12">')

    # Column headers (rotated challenge names)
    for i, cid in enumerate(active_challenges):
        x = label_w + i * cell_w + cell_w // 2
        short = cid.replace("c", "C").replace("_", " ").split(" ", 1)[-1]
        svg_parts.append(
            f'<text x="{x}" y="{header_h - 8}" '
            f'transform="rotate(-45 {x} {header_h - 8})" '
            f'text-anchor="end" font-size="11" fill="#374151">{short}</text>'
        )

    # Rows
    for j, label in enumerate(labels):
        y = header_h + j * cell_h

        # Model label
        svg_parts.append(
            f'<text x="{label_w - 8}" y="{y + cell_h // 2 + 4}" '
            f'text-anchor="end" font-size="12" fill="#1f2937">{label}</text>'
        )

        # Cells
        for i, cid in enumerate(active_challenges):
            x = label_w + i * cell_w
            val = matrix.get((label, cid), 0)
            color = _color(val, max_val)
            svg_parts.append(
                f'<rect x="{x}" y="{y}" width="{cell_w - 2}" height="{cell_h - 2}" '
                f'rx="4" fill="{color}"/>'
            )
            if val > 0:
                text_color = "#fff" if val > max_val * 0.4 else "#1f2937"
                display = f"{val:.1f}" if val != int(val) else str(int(val))
                svg_parts.append(
                    f'<text x="{x + cell_w // 2 - 1}" y="{y + cell_h // 2 + 4}" '
                    f'text-anchor="middle" font-size="11" fill="{text_color}">{display}</text>'
                )

    # Legend
    legend_y = header_h + len(labels) * cell_h + 20
    svg_parts.append(f'<text x="{label_w}" y="{legend_y}" font-size="11" fill="#6b7280">'
                     f'Color: green (0 issues) → yellow → red ({max_val:.0f} issues)</text>')

    svg_parts.append('</svg>')
    svg = "\n".join(svg_parts)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Self-Issue Benchmark Heatmap</title>
<style>
  body {{ margin: 2rem; background: #f9fafb; font-family: system-ui, sans-serif; }}
  h1 {{ color: #1f2937; font-size: 1.5rem; }}
  p {{ color: #6b7280; font-size: 0.9rem; }}
</style>
</head>
<body>
<h1>Challenge × Model Heatmap</h1>
<p>Issue count per challenge per model. Models sorted by total issues (fewest first).</p>
{svg}
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Generate benchmark heatmap visualization")
    parser.add_argument("results_dir", help="Path to results directory")
    parser.add_argument("-o", "--output", default="docs/heatmap.html", help="Output HTML file")
    args = parser.parse_args()

    groups = gather_scores(Path(args.results_dir))
    if not groups:
        print("No results found.")
        return

    aggregates = {label: aggregate_scores(scores) for label, scores in groups.items()}
    html = generate_heatmap(aggregates)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(html)
    print(f"Heatmap written to: {args.output}")


if __name__ == "__main__":
    main()
