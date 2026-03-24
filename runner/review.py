#!/usr/bin/env python3
"""
Automated independent review of benchmark results.

Sends generated code to a reviewer model and parses structured issue output.
Replaces manual populate_scores.py workflow.

Usage:
    python runner/review.py results/opus-4_2026-03-21/
    python runner/review.py results/opus-4_2026-03-21/ --reviewer-model claude-opus-4-20250514
    python runner/review.py results/opus-4_2026-03-21/ --challenges c1_fibonacci c5_deep_clone
    python runner/review.py results/opus-4_2026-03-21/ --dry-run

Requires:
    ANTHROPIC_API_KEY or OPENAI_API_KEY environment variable
    pip install anthropic openai pyyaml
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import yaml
from constants import CHALLENGE_PROMPT_FILES, CHALLENGES_DIR, ISSUE_SEVERITIES, normalize_issue_type
from providers import ALL_PROVIDER_NAMES, check_api_key, create_provider
from score import load_run

_RAW_TEMPLATE = (CHALLENGES_DIR / "independent_review_prompt.md").read_text()


def build_review_prompt(challenge_prompt: str, generated_code: str) -> str:
    """Build review prompt using simple replacement to avoid .format() brace issues."""
    return _RAW_TEMPLATE.replace(
        "{challenge_prompt}", challenge_prompt
    ).replace(
        "{generated_code}", generated_code
    )


def parse_issues(response_text: str) -> list[dict]:
    """Parse JSON-lines response into issue objects."""
    issues = []

    # Handle explicit empty response
    stripped = response_text.strip()
    if stripped == "[]" or stripped == "":
        return []

    for line in response_text.strip().splitlines():
        line = line.strip()
        if not line or line == "[]":
            continue

        # Strip leading list markers like "- " or "1. "
        line = re.sub(r"^[\-\d.)\s]+", "", line).strip()
        if not line:
            continue

        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            # Try to extract JSON from the line
            match = re.search(r"\{.*\}", line)
            if match:
                try:
                    obj = json.loads(match.group())
                except json.JSONDecodeError:
                    print(f"    WARN: Could not parse line: {line[:80]}")
                    continue
            else:
                continue

        itype = normalize_issue_type(obj.get("type", ""))
        if itype is None:
            print(f"    WARN: Unknown type '{obj.get('type', '')}', skipping")
            continue

        severity = obj.get("severity", "").lower()
        if severity not in ISSUE_SEVERITIES:
            print(f"    WARN: Unknown severity '{severity}', skipping")
            continue

        description = obj.get("description", "").strip()
        if not description:
            continue

        issues.append({
            "type": itype,
            "severity": severity,
            "description": description,
        })

    return issues


def check_self_caught(issue_desc: str, review_text_lower: str) -> bool:
    """Check if the model's self-review caught an issue by keyword matching.

    review_text_lower should be pre-lowercased by the caller.
    """
    terms = [w.lower() for w in re.findall(r"\w{3,}", issue_desc)]
    if not terms:
        return False
    matches = sum(1 for t in terms if t in review_text_lower)
    return matches / len(terms) > 0.5


def review_challenge(
    provider,
    reviewer_model: str,
    run_dir: Path,
    challenge_id: str,
    challenge_data: dict,
) -> tuple[list[dict], str]:
    """Review a single challenge's generated code."""
    # Read generated code
    code_path = run_dir / challenge_data["generated_code_file"]
    generated_code = code_path.read_text()

    # Read challenge prompt
    prompt_file = CHALLENGE_PROMPT_FILES.get(challenge_id)
    if not prompt_file:
        print(f"    WARN: No prompt file for {challenge_id}")
        return [], ""

    challenge_prompt = (CHALLENGES_DIR / prompt_file).read_text().strip()

    # Build review prompt
    review_prompt = build_review_prompt(challenge_prompt, generated_code)

    # Call reviewer model
    response_text, _ = provider.chat(
        reviewer_model,
        [{"role": "user", "content": review_prompt}],
    )

    # Parse issues
    issues = parse_issues(response_text)

    # Determine self_caught for each issue
    review_file = challenge_data.get("review_file", "")
    review2_file = challenge_data.get("review2_file", "")
    self_review_text = ""
    if review_file:
        review_path = run_dir / review_file
        if review_path.exists():
            self_review_text += review_path.read_text()
    if review2_file:
        review2_path = run_dir / review2_file
        if review2_path.exists():
            self_review_text += "\n" + review2_path.read_text()

    review_lower = self_review_text.lower()
    for issue in issues:
        issue["self_caught"] = check_self_caught(issue["description"], review_lower)

    return issues, response_text


def main():
    parser = argparse.ArgumentParser(description="Automated independent review")
    parser.add_argument(
        "run_dir",
        help="Path to run directory (e.g. results/opus-4_2026-03-21/)",
    )
    parser.add_argument(
        "--reviewer-provider",
        choices=ALL_PROVIDER_NAMES,
        default="anthropic",
        help="API provider for reviewer (default: anthropic)",
    )
    parser.add_argument(
        "--reviewer-model",
        default="claude-opus-4-20250514",
        help="Model to use as independent reviewer (default: claude-opus-4-20250514)",
    )
    parser.add_argument(
        "--challenges",
        nargs="*",
        default=None,
        help="Review only specific challenges",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print prompts without calling API",
    )
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    results_path = run_dir / "results.yaml"

    if not results_path.exists():
        print(f"Error: {results_path} not found")
        sys.exit(1)

    data = load_run(results_path)

    challenges = data.get("challenges", {})
    if args.challenges:
        challenges = {k: v for k, v in challenges.items() if k in args.challenges}

    if args.dry_run:
        print(f"Run dir:         {run_dir}")
        print(f"Reviewer:        {args.reviewer_provider}/{args.reviewer_model}")
        print(f"Challenges:      {list(challenges.keys())}")
        print()
        # Show one example prompt
        cid = next(iter(challenges))
        cdata = challenges[cid]
        code_path = run_dir / cdata["generated_code_file"]
        prompt_file = CHALLENGE_PROMPT_FILES.get(cid, "")
        if prompt_file:
            challenge_prompt = (CHALLENGES_DIR / prompt_file).read_text().strip()
            generated_code = code_path.read_text() if code_path.exists() else "(code not found)"
            print(f"Example prompt for {cid}:")
            print("---")
            print(build_review_prompt(challenge_prompt, generated_code)[:500] + "...")
        return

    # Check API key
    check_api_key(args.reviewer_provider)
    provider = create_provider(args.reviewer_provider)

    print(f"Run dir:    {run_dir}")
    print(f"Model:      {data.get('model', 'unknown')}")
    print(f"Reviewer:   {args.reviewer_model}")
    print(f"Challenges: {len(challenges)}")
    print()

    total_issues = 0
    total_caught = 0

    for cid, cdata in challenges.items():
        print(f"  [{cid}] Reviewing...")

        issues, raw_response = review_challenge(
            provider, args.reviewer_model, run_dir, cid, cdata,
        )

        # Save raw response
        review_path = run_dir / f"{cid}_independent_review.md"
        review_path.write_text(raw_response)

        # Update results
        data["challenges"][cid]["issues"] = issues
        data["challenges"][cid]["independent_review_file"] = f"{cid}_independent_review.md"

        caught = sum(1 for i in issues if i.get("self_caught"))
        total_issues += len(issues)
        total_caught += caught

        print(f"  [{cid}] {len(issues)} issues ({caught} self-caught)")

    # Add reviewer metadata
    data["independent_reviewer"] = {
        "model": args.reviewer_model,
        "provider": args.reviewer_provider,
        "date": date.today().isoformat(),
    }

    # Write updated results
    with open(results_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    print()
    if total_issues > 0:
        rate = total_caught / total_issues * 100
        print(f"Total: {total_issues} issues, {total_caught} self-caught ({rate:.0f}%)")
    else:
        print("Total: 0 issues found")
    print(f"Results written to: {results_path}")


if __name__ == "__main__":
    main()
