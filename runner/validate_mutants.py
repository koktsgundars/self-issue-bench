#!/usr/bin/env python3
"""
Mutation testing: run test suites against intentionally buggy code.

Every mutant should be caught by at least one test. A surviving mutant
indicates a gap in the test suite.

Usage:
    python runner/validate_mutants.py
    python runner/validate_mutants.py --challenges c1_fibonacci c5_deep_clone
"""

import argparse
import sys
from pathlib import Path

from constants import CHALLENGE_IDS, CHALLENGE_LANG, CHALLENGE_TESTS_DIR
from test_code import _LANG_EXT, RUNNERS

PROJECT_DIR = Path(__file__).parent.parent
REFERENCE_DIR = PROJECT_DIR / "reference_implementations"


def find_mutants(challenge_id: str, lang: str) -> list[Path]:
    """Find all mutant files for a challenge."""
    ext_map = {"python": ".py", "javascript": ".js", "typescript": ".ts"}
    ext = ext_map.get(lang, "")
    mutant_dir = REFERENCE_DIR / lang / "mutants"
    if not mutant_dir.exists():
        return []
    return sorted(mutant_dir.glob(f"{challenge_id}_m*{ext}"))


def test_mutant(challenge_id: str, mutant_path: Path, lang: str) -> dict | None:
    """Run tests against a mutant. Returns test result or None if skipped."""
    runner = RUNNERS.get(lang)
    if not runner:
        return None

    test_ext = _LANG_EXT.get(lang, ".py")
    test_file = CHALLENGE_TESTS_DIR / lang / f"test_{challenge_id}{test_ext}"
    if not test_file.exists():
        return None

    return runner(challenge_id, mutant_path, test_file, mutant_path.parent)


def main():
    parser = argparse.ArgumentParser(description="Mutation testing for test suites")
    parser.add_argument("--challenges", nargs="*", default=None, help="Test specific challenges")
    args = parser.parse_args()

    challenge_ids = args.challenges or CHALLENGE_IDS

    total_mutants = 0
    total_killed = 0
    total_survived = 0
    survivors = []

    for cid in challenge_ids:
        if cid not in CHALLENGE_IDS:
            continue

        lang = CHALLENGE_LANG.get(cid)
        if not lang:
            continue

        mutants = find_mutants(cid, lang)
        if not mutants:
            continue

        killed = 0
        survived = []

        for mutant_path in mutants:
            mutant_name = mutant_path.stem  # e.g. c1_fibonacci_m1
            result = test_mutant(cid, mutant_path, lang)

            if result is None:
                continue

            total_mutants += 1

            if result["compile_error"] or result["passed"] < result["total"]:
                killed += 1
                total_killed += 1
            else:
                survived.append(mutant_name)
                total_survived += 1
                survivors.append((cid, mutant_name))

        if survived:
            print(f"  [{cid}] {killed}/{killed + len(survived)} killed -- SURVIVED: {', '.join(survived)}")
        else:
            print(f"  [{cid}] {killed}/{killed} killed")

    print()
    print(f"Mutants: {total_mutants} tested, {total_killed} killed, {total_survived} survived")
    if total_mutants > 0:
        rate = total_killed / total_mutants * 100
        print(f"Kill rate: {rate:.0f}%")

    if survivors:
        print(f"\nSURVIVORS ({len(survivors)}) — test gaps to investigate:")
        for cid, name in survivors:
            print(f"  {cid}: {name}")
        sys.exit(1)
    else:
        print("\nAll mutants killed. Test suites have no false-negative gaps.")


if __name__ == "__main__":
    main()
