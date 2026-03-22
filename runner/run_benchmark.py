#!/usr/bin/env python3
"""
Run the self-issue benchmark against a model.

Usage:
    # Anthropic (default)
    python runner/run_benchmark.py --model claude-opus-4-20250514 --label opus-4

    # OpenAI
    python runner/run_benchmark.py --provider openai --model gpt-5.3-codex --label gpt-5.3-codex

    # Other providers (direct)
    python runner/run_benchmark.py --provider deepseek --model deepseek-chat --label deepseek-v3.2
    python runner/run_benchmark.py --provider gemini --model gemini-3.1-pro --label gemini-3.1-pro

    # OpenRouter (single key for all models)
    python runner/run_benchmark.py --provider openrouter --model deepseek/deepseek-v3.2 --label deepseek-v3.2
    python runner/run_benchmark.py --provider openrouter --model google/gemini-3.1-pro-preview --label gemini-3.1-pro

Requires:
    Set the appropriate API key environment variable for your provider.
    pip install anthropic openai pyyaml
"""

import argparse
import sys
import time
from datetime import date

import yaml
from constants import CHALLENGE_IDS, CHALLENGE_PROMPT_FILES, CHALLENGES_DIR, RESULTS_DIR
from providers import ALL_PROVIDER_NAMES, check_api_key, create_provider

REVIEW_PROMPT = (CHALLENGES_DIR / "review_prompt.md").read_text().strip()

SECOND_REVIEW_PROMPT = (
    "Look again. Are there any issues you missed in your first review? "
    "Focus on correctness and edge cases, not style. "
    "Use the same output format. If you have nothing to add, say so explicitly."
)

def run_challenge(
    provider,
    model: str,
    challenge_id: str,
    prompt_text: str,
    double_review: bool = False,
) -> dict:
    """Run a single challenge: generate code, then ask for self-review."""
    print(f"  [{challenge_id}] Generating code...")

    # Turn 1: generate code
    messages = [{"role": "user", "content": prompt_text}]
    generated, gen_usage = provider.chat(model, messages)

    print(f"  [{challenge_id}] Requesting self-review (pass 1)...")

    # Turn 2: self-review (same conversation context)
    messages = [
        {"role": "user", "content": prompt_text},
        {"role": "assistant", "content": generated},
        {"role": "user", "content": REVIEW_PROMPT},
    ]
    review, review_usage = provider.chat(model, messages)

    result = {
        "generated_code": generated,
        "self_review": review,
        "usage": {
            "generation": gen_usage,
            "review": review_usage,
        },
    }

    # Optional turn 3: second review pass
    if double_review:
        print(f"  [{challenge_id}] Requesting self-review (pass 2)...")

        messages += [
            {"role": "assistant", "content": review},
            {"role": "user", "content": SECOND_REVIEW_PROMPT},
        ]
        review2, review2_usage = provider.chat(model, messages)

        result["self_review_2"] = review2
        result["usage"]["review_2"] = review2_usage

    return result


def main():
    parser = argparse.ArgumentParser(description="Run self-issue benchmark")
    parser.add_argument(
        "--provider",
        choices=ALL_PROVIDER_NAMES,
        default="anthropic",
        help=f"API provider (default: anthropic). Available: {', '.join(ALL_PROVIDER_NAMES)}",
    )
    parser.add_argument(
        "--model",
        required=True,
        help="Model ID (e.g. claude-sonnet-4-20250514, gpt-4o, o3)",
    )
    parser.add_argument(
        "--label",
        default=None,
        help="Short label for the run directory (default: derived from model name)",
    )
    parser.add_argument(
        "--challenges",
        nargs="*",
        default=None,
        help="Run only specific challenges (e.g. c1_fibonacci c3_word_frequency)",
    )
    parser.add_argument(
        "--double-review",
        action="store_true",
        help="Run a second review pass after the first",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=1,
        help="Number of independent runs (default: 1)",
    )
    parser.add_argument(
        "--run-offset",
        type=int,
        default=1,
        help="Starting run number (default: 1, useful for resuming)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be run without calling the API",
    )
    args = parser.parse_args()

    label = args.label or args.model
    run_date = date.today().isoformat()

    # Filter challenges if requested
    challenge_ids = CHALLENGE_IDS
    if args.challenges:
        challenge_ids = [cid for cid in CHALLENGE_IDS if cid in args.challenges]
        if not challenge_ids:
            print(f"No matching challenges for: {args.challenges}")
            sys.exit(1)

    # Build list of run numbers
    run_numbers = list(range(args.run_offset, args.run_offset + args.runs))

    def make_run_dir(run_num):
        if args.runs == 1 and args.run_offset == 1:
            return RESULTS_DIR / f"{label}_{run_date}"
        return RESULTS_DIR / f"{label}_run{run_num}_{run_date}"

    if args.dry_run:
        print(f"Provider:      {args.provider}")
        print(f"Model:         {args.model}")
        print(f"Label:         {label}")
        print(f"Runs:          {args.runs} (starting at {args.run_offset})")
        for rn in run_numbers:
            print(f"  Output dir:  {make_run_dir(rn)}")
        print(f"Double review: {args.double_review}")
        print(f"Challenges:    {challenge_ids}")
        return

    check_api_key(args.provider)
    provider = create_provider(args.provider)

    for run_num in run_numbers:
        run_dir = make_run_dir(run_num)

        # Create output directory
        run_dir.mkdir(parents=True, exist_ok=True)
        code_dir = run_dir / "code"
        code_dir.mkdir(exist_ok=True)

        if args.runs > 1:
            print(f"=== Run {run_num} of {args.run_offset + args.runs - 1} ===")
        print(f"Provider:   {args.provider}")
        print(f"Model:      {args.model}")
        print(f"Output dir: {run_dir}")
        if args.double_review:
            print("Mode:       double-review")
        print(f"Challenges: {len(challenge_ids)}")
        print()

        # Load existing results if present (to support incremental runs)
        results_path = run_dir / "results.yaml"
        if results_path.exists():
            with open(results_path) as f:
                results = yaml.safe_load(f)
            print(f"(Merging into existing results with {len(results.get('challenges', {}))} challenges)")
            print()
        else:
            results = {
                "provider": args.provider,
                "model": args.model,
                "label": label,
                "date": run_date,
                "double_review": args.double_review,
                "run_number": run_num if args.runs > 1 else None,
                "notes": "",
                "challenges": {},
            }

        total_start = time.time()

        for challenge_id in challenge_ids:
            prompt_file = CHALLENGE_PROMPT_FILES[challenge_id]
            prompt_text = (CHALLENGES_DIR / prompt_file).read_text().strip()

            result = run_challenge(
                provider, args.model, challenge_id, prompt_text,
                double_review=args.double_review,
            )

            # Determine file extension from challenge content
            if "TypeScript" in prompt_text:
                ext = ".ts"
            elif "JavaScript" in prompt_text:
                ext = ".js"
            else:
                ext = ".py"
            code_filename = f"{challenge_id}{ext}"

            # Save generated code to file
            code_path = code_dir / code_filename
            code_path.write_text(result["generated_code"])

            # Save self-review to file
            review_path = run_dir / f"{challenge_id}_review.md"
            review_path.write_text(result["self_review"])

            # Add to results (issues left empty for scoring)
            challenge_result = {
                "generated_code_file": f"code/{code_filename}",
                "review_file": f"{challenge_id}_review.md",
                "usage": result["usage"],
                "issues": [],
            }

            # Save second review if present
            if "self_review_2" in result:
                review2_path = run_dir / f"{challenge_id}_review2.md"
                review2_path.write_text(result["self_review_2"])
                challenge_result["review2_file"] = f"{challenge_id}_review2.md"

            results["challenges"][challenge_id] = challenge_result

            print(f"  [{challenge_id}] Done.")
            print()

        elapsed = time.time() - total_start

        # Write results.yaml
        with open(results_path, "w") as f:
            yaml.dump(results, f, default_flow_style=False, sort_keys=False)

        print(f"Finished run in {elapsed:.1f}s")
        print(f"Results saved to: {run_dir}")
        print()


if __name__ == "__main__":
    main()
