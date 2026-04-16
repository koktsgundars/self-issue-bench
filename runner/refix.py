#!/usr/bin/env python3
"""
Re-run the fix step for challenges where the original fix output was not code.

Backfills runs generated before commit 559567a fixed the fix loop's handling
of prose/empty responses. For each affected challenge:
- Replays the conversation through self-review
- Sends the fix prompt with new validation (retry once, then fall back to
  original generated code if the model still fails to emit code)
- Overwrites fixed_code_file and updates fix usage in results.yaml

After running this, re-run test_code.py --fixed to refresh test_results_fixed.

Usage:
    python runner/refix.py results/glm-5_run1_2026-04-01/
    python runner/refix.py results/glm-5_run1_2026-04-01/ --dry-run
"""

import argparse
import sys
import time
from pathlib import Path

import yaml
from constants import CHALLENGE_IDS, CHALLENGE_PROMPT_FILES, CHALLENGES_DIR, FIX_PROMPT_FILE
from providers import check_api_key, create_provider
from run_benchmark import (
    FIX_RETRY_PROMPT,
    REVIEW_PROMPT,
    SECOND_REVIEW_PROMPT,
    _looks_like_code,
)


def reconstruct_messages(run_dir, challenge_id, cdata, double_review):
    """Rebuild the conversation up to (but not including) the fix prompt.

    Returns (messages, generated_code) or None if files are missing.
    """
    prompt_file = CHALLENGE_PROMPT_FILES.get(challenge_id)
    if not prompt_file:
        return None
    prompt_text = (CHALLENGES_DIR / prompt_file).read_text().strip()

    code_file = cdata.get("generated_code_file")
    review_file = cdata.get("review_file")
    if not code_file or not review_file:
        return None

    code_path = run_dir / code_file
    review_path = run_dir / review_file
    if not code_path.exists() or not review_path.exists():
        return None

    generated = code_path.read_text()
    review = review_path.read_text()

    messages = [
        {"role": "user", "content": prompt_text},
        {"role": "assistant", "content": generated},
        {"role": "user", "content": REVIEW_PROMPT},
        {"role": "assistant", "content": review},
    ]

    if double_review:
        review2_file = cdata.get("review2_file")
        if not review2_file:
            return None
        review2_path = run_dir / review2_file
        if not review2_path.exists():
            return None
        review2 = review2_path.read_text()
        messages += [
            {"role": "user", "content": SECOND_REVIEW_PROMPT},
            {"role": "assistant", "content": review2},
        ]

    return messages, generated


def refix_challenge(provider, model, run_dir, challenge_id, cdata, double_review):
    """Re-run fix turn for one challenge. Returns (fixed_code, fix_usage) or None."""
    fix_prompt = FIX_PROMPT_FILE.read_text().strip()
    reconstructed = reconstruct_messages(run_dir, challenge_id, cdata, double_review)
    if reconstructed is None:
        return None
    messages, generated = reconstructed
    messages.append({"role": "user", "content": fix_prompt})

    print(f"  [{challenge_id}] Requesting fix...")
    fixed_code, fix_usage = provider.chat(model, messages)

    if not _looks_like_code(fixed_code):
        print(f"  [{challenge_id}] Fix response is not code, retrying...")
        messages += [
            {"role": "assistant", "content": fixed_code},
            {"role": "user", "content": FIX_RETRY_PROMPT},
        ]
        retry_code, retry_usage = provider.chat(model, messages)
        fix_usage = {
            "input_tokens": fix_usage.get("input_tokens", 0) + retry_usage.get("input_tokens", 0),
            "output_tokens": fix_usage.get("output_tokens", 0) + retry_usage.get("output_tokens", 0),
        }
        if _looks_like_code(retry_code):
            fixed_code = retry_code
        else:
            print(f"  [{challenge_id}] Fix retry failed, using original code")
            fixed_code = generated

    return fixed_code, fix_usage


def find_affected(run_dir, challenges):
    """Return list of challenge_ids whose fixed_code is missing or non-code."""
    affected = []
    for cid in CHALLENGE_IDS:
        cdata = challenges.get(cid)
        if not cdata:
            continue
        fcf = cdata.get("fixed_code_file")
        if not fcf:
            continue
        p = run_dir / fcf
        if not p.exists() or not _looks_like_code(p.read_text()):
            affected.append(cid)
    return affected


def main():
    parser = argparse.ArgumentParser(description="Re-run fix step for bad outputs")
    parser.add_argument("run_dir", help="Path to run directory")
    parser.add_argument("--dry-run", action="store_true", help="List affected challenges without calling API")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    results_path = run_dir / "results.yaml"
    if not results_path.exists():
        print(f"Error: {results_path} not found")
        sys.exit(1)

    with open(results_path) as f:
        data = yaml.safe_load(f)

    if not data.get("fix"):
        print("Run does not have fix=true, nothing to do")
        return

    challenges = data.get("challenges") or {}
    double_review = data.get("double_review", False)
    affected = find_affected(run_dir, challenges)

    print(f"Run dir:        {run_dir}")
    print(f"Provider/model: {data.get('provider')} / {data.get('model')}")
    print(f"Double review:  {double_review}")
    print(f"Affected:       {len(affected)}/{len(challenges)} challenges")

    if not affected:
        return
    if args.dry_run:
        for cid in affected:
            print(f"  {cid}")
        return

    check_api_key(data["provider"])
    provider = create_provider(data["provider"])
    model = data["model"]

    start = time.time()
    for cid in affected:
        cdata = challenges[cid]
        try:
            result = refix_challenge(provider, model, run_dir, cid, cdata, double_review)
        except Exception as e:
            print(f"  [{cid}] ERROR: {type(e).__name__}: {e}")
            continue
        if result is None:
            print(f"  [{cid}] Skipped (could not reconstruct conversation)")
            continue
        fixed_code, fix_usage = result

        fcf = cdata["fixed_code_file"]
        (run_dir / fcf).write_text(fixed_code)

        usage = cdata.setdefault("usage", {})
        usage["fix"] = fix_usage

    with open(results_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    print(f"Done in {time.time() - start:.1f}s")
    print(f"Updated: {results_path}")


if __name__ == "__main__":
    main()
