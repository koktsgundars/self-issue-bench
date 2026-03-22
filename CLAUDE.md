# CLAUDE.md

## Project overview

self-issue-bench is a benchmark measuring how many issues coding assistants introduce into their own output on trivial coding challenges. We measure self-generated issue rate and self-catch rate across models.

## Architecture

```
challenges/          # 16 challenge prompts (C1-C16) + review prompts
docs/                # Benchmark spec, trap notes, generated reports
runner/              # All tooling
  constants.py       # Shared constants: challenge IDs, issue types, normalization
  providers.py       # API provider abstraction (Anthropic, OpenAI)
  run_benchmark.py   # Run challenges against a model
  review.py          # Automated independent review of generated code
  score.py           # Score a single run's results.yaml
  compare.py         # Compare runs side-by-side
  aggregate.py       # Aggregate repeated runs, gather_scores()
  report.py          # Generate markdown summary report
  populate_scores.py # Legacy manual scoring (prefer review.py)
results/             # One directory per scored run
```

## Key conventions

- All shared constants (challenge IDs, issue types, paths) live in `runner/constants.py`. Never redefine them elsewhere.
- API providers are in `runner/providers.py`. Use `create_provider()` factory, never instantiate directly.
- Use `score.load_run()` for reading results.yaml, never inline `yaml.safe_load`.
- Use `aggregate.gather_scores()` for grouping runs by label, never re-implement the glob+parse pattern.
- `normalize_issue_type()` returns `None` for unrecognized types — callers must handle this.
- Challenge prompt files are always `{challenge_id}.md` — use `CHALLENGE_PROMPT_FILES` dict.

## Running scripts

All scripts are run from the project root with `python runner/<script>.py`. They use relative imports from `runner/` so the working directory matters.

```bash
# Run benchmark
python runner/run_benchmark.py --model claude-sonnet-4-20250514 --label sonnet-4 --double-review

# Automated independent review
python runner/review.py results/<run-dir>/ --reviewer-model claude-opus-4-20250514

# Score and compare
python runner/score.py results/<run-dir>/
python runner/compare.py results/
python runner/aggregate.py results/

# Generate report
python runner/report.py results/ -o docs/report.md
```

## Quality checks

Always run before committing:

```bash
ruff check runner/
python -m pytest tests/ -q
```

## Style

- No type stubs or annotations beyond what's already present (function signatures only).
- Keep scripts simple — no classes where functions suffice, no abstractions for single use.
- Tests go in `tests/` and use pytest.
