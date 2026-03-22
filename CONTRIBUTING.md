# Contributing to self-issue-bench

Thanks for your interest in contributing! Here's how to get started.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Writing your own challenges

The benchmark's challenge prompts are kept private to prevent gaming. To run the
pipeline with your own challenges, add markdown files to `challenges/` named
`c<n>_<name>.md` (e.g., `c1_fibonacci.md`). See `challenges/example_challenge.md`
for the expected format. Each challenge should be:

- Self-contained (no external dependencies beyond the standard library)
- Solvable in a single file / function
- Clear enough that a correct solution is unambiguous
- End with: "Return only a single implementation as a plain code block."

Update `CHALLENGE_IDS` in `runner/constants.py` to match your challenge filenames.

## Adding providers

Provider implementations live in `runner/providers.py`. Use the `create_provider()` factory — see existing providers for the pattern.

## Code quality

Before submitting a PR, run:

```bash
ruff check runner/
python -m pytest tests/ -q
```

All checks must pass.

## Style guidelines

- Keep scripts simple — functions over classes, no premature abstractions.
- Shared constants go in `runner/constants.py`, never redefined elsewhere.
- No type annotations beyond what's already present in function signatures.

## Submitting changes

1. Fork the repo and create a branch from `main`.
2. Make your changes and ensure checks pass.
3. Open a pull request with a clear description of what and why.
