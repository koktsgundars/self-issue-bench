# self-issue-bench

A benchmark measuring how many issues a coding assistant introduces into its
own output on trivial, clean coding challenges. No pre-injected bugs.
We measure self-generated issue rate + self-catch rate.

## Why open-source the tooling but not the challenges?

Public benchmarks get gamed. If model providers can see the exact prompts, they can
(and do) optimize for them. By keeping challenge prompts private and publishing only
the methodology and tooling, we get:

- **Transparent methodology** — anyone can audit how scoring works
- **Reproducible pipeline** — bring your own challenges and run the same tools
- **Resistance to gaming** — challenge prompts are not in the training data

We publish results periodically. See `docs/benchmark.md` for the full protocol.

## Methodology

1. Send a challenge prompt to the assistant — fresh session, no system prompt, no context
2. After generation, send the standard review prompt (included in `challenges/`)
3. Run independent review with a different model
4. Score by category: correctness, edge case, security, style

See `docs/benchmark.md` for the complete protocol and scoring rubric.

## Key metrics

- **Total issues**: count of distinct bugs/smells introduced by the assistant
- **Self-catch rate** = issues flagged by assistant in review / total issues found

## Challenges

The benchmark uses 16 challenges across Python, JavaScript, and TypeScript, ranging
from easy to medium difficulty. Challenge prompts are **not included** in this
repository to prevent benchmark gaming.

To use your own challenges, add markdown files to `challenges/` following the format
in `challenges/example_challenge.md`. Each prompt should ask for a single function
and end with the constraint to return only a plain code block.

## Running

```bash
# Install dependencies
pip install -e ".[dev]"

# Run benchmark against a model (requires ANTHROPIC_API_KEY or OPENAI_API_KEY)
python runner/run_benchmark.py --model claude-sonnet-4-20250514 --label sonnet-4

# Automated independent review of generated code
python runner/review.py results/<run-dir>/ --reviewer-model claude-opus-4-20250514

# Score a completed run
python runner/score.py results/<run-dir>/

# Compare runs side-by-side
python runner/compare.py results/

# Aggregate repeated runs
python runner/aggregate.py results/

# Generate markdown report
python runner/report.py results/ -o docs/report.md
```

## Project structure

```
challenges/       # Review prompts + example challenge (actual prompts not included)
docs/             # Benchmark spec and methodology
runner/           # Benchmark runner, review, scoring, and reporting tools
results/          # Generated at runtime (gitignored)
```

## Status

- [x] Benchmark doc created
- [x] Project scaffolded
- [x] Run against Claude Code (Sonnet 4.6)
- [x] Run against at least one other model for comparison
- [x] Decide on output format for results
