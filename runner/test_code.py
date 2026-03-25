#!/usr/bin/env python3
"""
Run test suites against generated code from benchmark results.

Usage:
    python runner/test_code.py results/opus-4_2026-03-23/
    python runner/test_code.py results/opus-4_2026-03-23/ --challenges c1_fibonacci c5_deep_clone
    python runner/test_code.py results/opus-4_2026-03-23/ --dry-run
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from constants import CHALLENGE_IDS, CHALLENGE_LANG, CHALLENGE_TESTS_DIR
from score import load_run


def extract_code(raw: str) -> str:
    """Strip markdown code fences if present."""
    lines = raw.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines)


def parse_pytest_json(output: str) -> list[dict]:
    """Parse pytest --tb=line output into test details."""
    details = []
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return details

    for test in data.get("tests", []):
        name = test.get("nodeid", "").split("::")[-1]
        outcome = test.get("outcome", "unknown")
        message = None
        if outcome == "failed":
            call = test.get("call", {})
            message = call.get("crash", {}).get("message", "")
            if not message:
                message = call.get("longrepr", "")
        status = {"passed": "pass", "failed": "fail", "error": "error"}.get(
            outcome, "error"
        )
        details.append({"name": name, "status": status, "message": message})

    return details


_TIMEOUT_RESULT = {
    "passed": 0, "failed": 0, "errors": 1, "total": 1,
    "compile_error": "Timed out (30s)",
    "details": [],
}

# Map language to test file extension
_LANG_EXT = {
    "python": ".py",
    "javascript": ".js",
    "typescript": ".ts",
    "go": "_test.go",
    "rust": ".rs",
}


def run_python_test(challenge_id, code_path, test_path, run_dir):
    """Run a Python test suite against generated code."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Write extracted code as importable module
        raw = code_path.read_text()
        code = extract_code(raw)
        module_name = challenge_id
        (tmpdir / f"{module_name}.py").write_text(code)

        # Copy test file
        shutil.copy(test_path, tmpdir / f"test_{challenge_id}.py")

        # Run pytest with JSON report
        try:
            result = subprocess.run(
                [
                    sys.executable, "-m", "pytest",
                    f"test_{challenge_id}.py",
                    "--tb=short", "-q",
                    "--json-report", "--json-report-file=report.json",
                ],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=30,
                env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )
        except subprocess.TimeoutExpired:
            return _TIMEOUT_RESULT

        # Parse results
        report_path = tmpdir / "report.json"
        if report_path.exists():
            details = parse_pytest_json(report_path.read_text())
        else:
            # Fallback: treat as compile/import error
            return {
                "passed": 0,
                "failed": 0,
                "errors": 1,
                "total": 1,
                "compile_error": result.stderr[:500] if result.stderr else result.stdout[:500],
                "details": [],
            }

        passed = sum(1 for d in details if d["status"] == "pass")
        failed = sum(1 for d in details if d["status"] == "fail")
        errors = sum(1 for d in details if d["status"] == "error")

        return {
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "total": passed + failed + errors,
            "compile_error": None,
            "details": details,
        }



def parse_node_test_output(stdout: str) -> list[dict]:
    """Parse node:test output into test details.

    Node's test runner uses Unicode symbols:
      ✔ test name (pass)
      ✖ test name (fail)
    And summary lines like:
      ℹ pass N / ℹ fail N
    """
    details = []
    for line in stdout.splitlines():
        stripped = line.strip()
        # Unicode format: "✔ name" or "✖ name"
        # Indented lines are individual tests; non-indented are suite summaries.
        is_indented = line != line.lstrip()
        if stripped.startswith("✔ ") or stripped.startswith("✓ "):
            if is_indented:
                name = stripped[2:].split(" (")[0].strip()
                details.append({"name": name, "status": "pass", "message": None})
        elif stripped.startswith("✖ ") or stripped.startswith("✗ "):
            if is_indented:
                name = stripped[2:].split(" (")[0].strip()
                details.append({"name": name, "status": "fail", "message": "test failed"})
        # TAP format fallback: "ok N - name" / "not ok N - name"
        elif stripped.startswith("ok ") or stripped.startswith("not ok "):
            is_pass = stripped.startswith("ok ")
            parts = stripped.split(" - ", 1)
            name = parts[1].strip() if len(parts) > 1 else stripped
            details.append({
                "name": name,
                "status": "pass" if is_pass else "fail",
                "message": None if is_pass else "test failed",
            })
    return details


def run_javascript_test(challenge_id, code_path, test_path, run_dir):
    """Run a JavaScript test suite against generated code."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Write extracted code wrapped to export via global
        raw = code_path.read_text()
        code = extract_code(raw)
        # Wrap code so declarations are accessible: use indirect eval via Function
        # or write as a module that the test file requires
        code_file = tmpdir / f"{challenge_id}.js"
        code_file.write_text(code)

        # Copy test file
        shutil.copy(test_path, tmpdir / f"test_{challenge_id}.js")

        # Run with node
        try:
            result = subprocess.run(
                ["node", "--test", f"test_{challenge_id}.js"],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=30,
                env={**__import__("os").environ, "CODE_FILE": str(code_file)},
            )
        except subprocess.TimeoutExpired:
            return _TIMEOUT_RESULT

        # Check for syntax/compile errors
        if result.returncode != 0 and "SyntaxError" in result.stderr:
            return {
                "passed": 0,
                "failed": 0,
                "errors": 1,
                "total": 1,
                "compile_error": result.stderr[:500],
                "details": [],
            }

        details = parse_node_test_output(result.stdout)
        if not details:
            # Try stderr for TAP output
            details = parse_node_test_output(result.stderr)

        passed = sum(1 for d in details if d["status"] == "pass")
        failed = sum(1 for d in details if d["status"] == "fail")
        errors = sum(1 for d in details if d["status"] == "error")

        # If no details parsed but there was an error, report it
        if not details and result.returncode != 0:
            return {
                "passed": 0,
                "failed": 0,
                "errors": 1,
                "total": 1,
                "compile_error": (result.stderr or result.stdout)[:500],
                "details": [],
            }

        return {
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "total": passed + failed + errors,
            "compile_error": None,
            "details": details,
        }


def run_typescript_test(challenge_id, code_path, test_path, run_dir):
    """Run a TypeScript test suite by transpiling to JS first."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Write extracted code
        raw = code_path.read_text()
        code = extract_code(raw)
        code_file = tmpdir / f"{challenge_id}.ts"
        code_file.write_text(code)

        # Copy test file
        shutil.copy(test_path, tmpdir / f"test_{challenge_id}.ts")

        # Use tsx to run TypeScript test directly
        try:
            result = subprocess.run(
                ["npx", "tsx", f"test_{challenge_id}.ts"],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=60,
                env={**__import__("os").environ, "CODE_FILE": str(code_file)},
            )
        except subprocess.TimeoutExpired:
            return _TIMEOUT_RESULT

        # Parse simple pass/fail output from test file
        details = _parse_simple_test_output(result.stdout)

        if not details and result.returncode != 0:
            return {
                "passed": 0,
                "failed": 0,
                "errors": 1,
                "total": 1,
                "compile_error": (result.stderr or result.stdout)[:500],
                "details": [],
            }

        passed = sum(1 for d in details if d["status"] == "pass")
        failed = sum(1 for d in details if d["status"] == "fail")
        errors = sum(1 for d in details if d["status"] == "error")

        return {
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "total": passed + failed + errors,
            "compile_error": None,
            "details": details,
        }


def _parse_simple_test_output(stdout: str) -> list[dict]:
    """Parse simple PASS/FAIL output lines."""
    details = []
    for line in stdout.splitlines():
        line = line.strip()
        if line.startswith("PASS "):
            details.append({"name": line[5:], "status": "pass", "message": None})
        elif line.startswith("FAIL "):
            parts = line[5:].split(": ", 1)
            name = parts[0]
            message = parts[1] if len(parts) > 1 else "test failed"
            details.append({"name": name, "status": "fail", "message": message})
        elif line.startswith("ERROR "):
            parts = line[6:].split(": ", 1)
            name = parts[0]
            message = parts[1] if len(parts) > 1 else "error"
            details.append({"name": name, "status": "error", "message": message})
    return details


RUNNERS = {
    "python": run_python_test,
    "javascript": run_javascript_test,
    "typescript": run_typescript_test,
    # "go": run_go_test,      # Requires Go toolchain
    # "rust": run_rust_test,   # Requires Rust toolchain
}


def test_challenge(run_dir, challenge_id, challenge_data, use_fixed=False):
    """Run tests for a single challenge."""
    lang = CHALLENGE_LANG.get(challenge_id)
    if not lang:
        return None

    runner = RUNNERS.get(lang)
    if not runner:
        return None

    file_key = "fixed_code_file" if use_fixed else "generated_code_file"
    code_file = challenge_data.get(file_key)
    if not code_file:
        return None

    code_path = run_dir / code_file
    if not code_path.exists():
        return {
            "passed": 0, "failed": 0, "errors": 1, "total": 1,
            "compile_error": f"Code file not found: {code_file}",
            "details": [],
        }

    # Find test file
    test_dir = CHALLENGE_TESTS_DIR / lang
    ext = _LANG_EXT.get(lang, ".py")
    test_file = test_dir / f"test_{challenge_id}{ext}"

    if not test_file.exists():
        return None  # No test suite yet

    return runner(challenge_id, code_path, test_file, run_dir)


def main():
    parser = argparse.ArgumentParser(description="Run test suites against generated code")
    parser.add_argument("run_dir", help="Path to run directory")
    parser.add_argument("--challenges", nargs="*", default=None, help="Test only specific challenges")
    parser.add_argument("--fixed", action="store_true", help="Test fixed code instead of original")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be tested")
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
        print(f"Run dir:    {run_dir}")
        print(f"Model:      {data.get('model', 'unknown')}")
        print(f"Challenges: {len(challenges)}")
        for cid in challenges:
            lang = CHALLENGE_LANG.get(cid, "?")
            runner = "available" if lang in RUNNERS else "skipped (no toolchain)"
            print(f"  {cid} ({lang}): {runner}")
        return

    version = "fixed" if args.fixed else "original"
    results_key = "test_results_fixed" if args.fixed else "test_results"

    print(f"Run dir:    {run_dir}")
    print(f"Model:      {data.get('model', 'unknown')}")
    print(f"Version:    {version}")
    print()

    total_passed = 0
    total_tests = 0
    tested = 0
    skipped = 0

    for cid in CHALLENGE_IDS:
        if cid not in challenges:
            continue

        cdata = challenges[cid]
        result = test_challenge(run_dir, cid, cdata, use_fixed=args.fixed)

        if result is None:
            skipped += 1
            continue

        tested += 1
        data["challenges"][cid][results_key] = result

        p = result["passed"]
        t = result["total"]
        total_passed += p
        total_tests += t

        status = "PASS" if p == t else "FAIL"
        err = " (compile error)" if result["compile_error"] else ""
        print(f"  [{cid}] {status} {p}/{t}{err}")

        if result["compile_error"]:
            print(f"    {result['compile_error'][:120]}")

    # Write updated results
    with open(results_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    print()
    if total_tests > 0:
        rate = total_passed / total_tests * 100
        print(f"Tested: {tested} challenges, {skipped} skipped")
        print(f"Total: {total_passed}/{total_tests} tests passed ({rate:.0f}%)")
    else:
        print(f"No tests run ({skipped} skipped)")
    print(f"Results written to: {results_path}")


if __name__ == "__main__":
    main()
