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

# Run benchmark (set the appropriate API key env var for your provider)
python runner/run_benchmark.py --model claude-opus-4-20250514 --label opus-4
python runner/run_benchmark.py --provider openai --model gpt-5.3-codex --label gpt-5.3-codex
python runner/run_benchmark.py --provider deepseek --model deepseek-chat --label deepseek-v3.2
python runner/run_benchmark.py --provider gemini --model gemini-3.1-pro --label gemini-3.1-pro

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

## Supported providers

| Provider | `--provider` | API key env var | Example models |
|----------|-------------|-----------------|----------------|
| Anthropic | `anthropic` (default) | `ANTHROPIC_API_KEY` | `claude-opus-4-20250514` |
| OpenAI | `openai` | `OPENAI_API_KEY` | `gpt-5.3-codex`, `o3` |
| DeepSeek | `deepseek` | `DEEPSEEK_API_KEY` | `deepseek-chat` |
| Google Gemini | `gemini` | `GEMINI_API_KEY` | `gemini-3.1-pro` |
| Alibaba Qwen | `qwen` | `DASHSCOPE_API_KEY` | `qwen-plus` |
| Moonshot (Kimi) | `moonshot` | `MOONSHOT_API_KEY` | `kimi-k2.5` |
| Zhipu (GLM) | `zhipu` | `ZHIPU_API_KEY` | `glm-5` |
| MiniMax | `minimax` | `MINIMAX_API_KEY` | `MiniMax-M2.5` |
| **OpenRouter** | `openrouter` | `OPENROUTER_API_KEY` | Any model — use `vendor/model` format |

OpenRouter (openrouter.ai) gives you access to all of the above through a single API key.
Use the `vendor/model` format for model IDs, e.g. `deepseek/deepseek-v3.2`, `google/gemini-3.1-pro-preview`.

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
