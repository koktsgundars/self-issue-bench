#!/usr/bin/env python3
"""
Validate test suites by running them against known-correct reference implementations.

Every test must pass on reference code. Any failure indicates a bug in the test suite.

Usage:
    python runner/validate_tests.py
    python runner/validate_tests.py --challenges c1_fibonacci c5_deep_clone
"""

import argparse
import sys
from pathlib import Path

from constants import CHALLENGE_IDS, CHALLENGE_LANG, CHALLENGE_TESTS_DIR
from test_code import _LANG_EXT, RUNNERS

PROJECT_DIR = Path(__file__).parent.parent
REFERENCE_DIR = PROJECT_DIR / "reference_implementations"


def validate_challenge(challenge_id: str) -> dict | None:
    """Run tests against a reference implementation. Returns result or None if skipped."""
    lang = CHALLENGE_LANG.get(challenge_id)
    if not lang:
        return None

    runner = RUNNERS.get(lang)
    if not runner:
        return None

    # Find reference implementation
    ref_dir = REFERENCE_DIR / lang
    ext_map = {"python": ".py", "javascript": ".js", "typescript": ".ts"}
    ext = ext_map.get(lang)
    if not ext:
        return None

    ref_file = ref_dir / f"{challenge_id}{ext}"
    if not ref_file.exists():
        return None

    # Find test file
    test_ext = _LANG_EXT.get(lang, ".py")
    test_file = CHALLENGE_TESTS_DIR / lang / f"test_{challenge_id}{test_ext}"
    if not test_file.exists():
        return None

    # Run tests against reference (no markdown extraction needed — raw code)
    return runner(challenge_id, ref_file, test_file, ref_dir)


def main():
    parser = argparse.ArgumentParser(description="Validate test suites against reference implementations")
    parser.add_argument("--challenges", nargs="*", default=None, help="Validate specific challenges")
    args = parser.parse_args()

    challenge_ids = args.challenges or CHALLENGE_IDS

    total_passed = 0
    total_tests = 0
    validated = 0
    skipped = 0
    failures = []

    for cid in challenge_ids:
        if cid not in CHALLENGE_IDS:
            print(f"  [{cid}] Unknown challenge, skipping")
            continue

        result = validate_challenge(cid)

        if result is None:
            skipped += 1
            continue

        validated += 1
        p = result["passed"]
        t = result["total"]
        total_passed += p
        total_tests += t

        if result["compile_error"]:
            print(f"  [{cid}] ERROR: {result['compile_error'][:120]}")
            failures.append(cid)
        elif p == t:
            print(f"  [{cid}] PASS ({p}/{t})")
        else:
            failed_tests = [d["name"] for d in result.get("details", []) if d["status"] != "pass"]
            print(f"  [{cid}] FAIL ({p}/{t}) -- {', '.join(failed_tests)}")
            failures.append(cid)

    print()
    print(f"Validated: {validated} challenges, {skipped} skipped")
    print(f"Tests: {total_passed}/{total_tests} passed")

    if failures:
        print(f"\nFAILURES ({len(failures)}):")
        for cid in failures:
            print(f"  {cid}")
        sys.exit(1)
    else:
        print("\nAll test suites validated against reference implementations.")


if __name__ == "__main__":
    main()
