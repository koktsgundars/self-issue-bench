# Your Coding Assistant Knows Its Code Has Bugs. It Just Doesn't Check.

*Part 2 of [I Benchmarked Whether AI Coding Assistants Know When They Screw Up](https://gundarskokts.substack.com/p/i-benchmarked-whether-ai-coding-assistants)*

Last week I [ran a small experiment](https://gundarskokts.substack.com/p/i-benchmarked-whether-ai-coding-assistants): give a coding assistant 8 trivial tasks, count the bugs, then ask it to review its own code. The first results — ~6 issues per run, 70-80% self-catch rate — were interesting enough that I kept going.

This is what happened when I scaled it to 52 challenges, 13 models, and 5 runs each — and then actually *ran* the code.

## The expanded benchmark

Same protocol as before — generate in a fresh session, self-review, independent review by Claude Opus 4 — but much bigger. 52 challenges across Python, JavaScript, and TypeScript covering algorithms, data structures, parsing, security, and utility functions. Things like topological sort, Mustache template rendering, SQL tokenization, email validation, and HTML sanitization.

The big addition: **test suites**. I wrote tests for each challenge (5-10 per challenge, ~350 total) and ran every model's generated code against them. This gives us an objective pass/fail signal alongside the subjective LLM review.

Five runs per model to get tighter confidence intervals. 13 models across Anthropic, OpenAI, and OpenRouter providers.

## The headline numbers

| Model | Test Pass Rate | Issues | Self-Catch Rate | Cost/Run |
|-------|---------------|--------|----------------|----------|
| Sonnet 4 | 98% | 66 | 68% | $0.46 |
| Opus 4 | 98% | 60 | 77% | $2.13 |
| o3-mini | 98% | 61 | 69% | $0.42 |
| DeepSeek V3.2 | 96% | 73 | 53% | $0.03 |
| Qwen 3.5 Plus | 95% | 17 | 25% | $0.18 |
| GPT-4o | 94% | 85 | 30% | $0.25 |
| Gemini 3.1 Pro | 92% | 66 | 42% | $1.01 |
| Nemotron 3 Super | 92% | 103 | 42% | $0.05 |
| GPT-4o-mini | 91% | 94 | 37% | $0.02 |
| MiniMax M2.5 | 82% | 40 | 52% | $0.17 |
| Haiku 4.5 | 72% | 107 | 69% | $0.21 |

Sorted by test pass rate — the metric that matters most.

## Tests and reviews tell different stories

This is the most interesting finding. When we just did LLM review (Part 1), Kimi K2.5 looked like the best model — fewest issues. When we actually ran the code, it had a 25% test pass rate. The "fewest issues" model produced code that mostly didn't work.

Why? The reviewer was too lenient on Kimi's simple-but-broken code, and too aggressive on models that wrote more ambitious implementations with more surface area for edge cases.

We validated this by running a second reviewer (GPT-4o) on a subset. The two reviewers agreed on only 71% of binary "has issues" decisions, with a Cohen's kappa of 0.40 — moderate agreement. They're measuring real things, but different things.

**The practical takeaway: if you're evaluating code quality, run it. Review is supplementary — useful for catching edge cases tests don't cover, but not a substitute for execution.**

## The cost story

This is the chart I wish I'd had when picking models for my own projects.

DeepSeek V3.2 costs $0.03 per run and passes 96% of tests. Opus 4 costs $2.13 per run and passes 98%. That's a **70x price difference for 2% more quality**. Unless that 2% matters for your use case, DeepSeek is the rational choice.

GPT-4o-mini is even cheaper ($0.02) at 91% — and if you add a self-review step, the marginal cost is negligible. For batch code generation where you'll review the output anyway, the cheapest models that clear ~90% are likely good enough.

The expensive models (Opus 4, Gemini 3.1 Pro) only make sense when you need the absolute highest first-pass quality and can't afford a review loop.

## What's hard, what's easy

I classified all 52 challenges by empirical failure rate:

- **Hard (32 challenges)**: 75%+ of models have issues. URL parsing, CSV parsing, HTML sanitization, Mustache templates, cron parsing. The pattern: tasks with a long tail of edge cases.
- **Medium (9 challenges)**: 38-69% failure rate. Linked list, trie, deep merge, INI parsing.
- **Easy (7 challenges)**: Under 38% failure rate. Date formatter, iterator, concurrent map.
- **Trivial (4 challenges)**: Zero or near-zero failures. Edit distance, binary heap, min heap.

Parsing and security tasks are consistently hard. Classic data structures are consistently easy. This matches intuition — edge-case-heavy tasks require the kind of exhaustive thinking that single-shot generation doesn't do.

## Self-review: still useful, still uneven

The self-catch rates widened with more data. Opus 4 catches 77% of its own issues. GPT-4o catches 30%. Qwen 3.5 Plus catches 25%.

But here's the nuance with 52 challenges: self-catch rate doesn't predict test pass rate. Haiku 4.5 has one of the highest self-catch rates (69%) but one of the lowest test pass rates (72%). It knows what's wrong but the code was too far gone to begin with.

The models where self-review is most valuable are the ones that write *almost* correct code and can catch the last few issues: Sonnet 4, Opus 4, o3-mini. For models that generate fundamentally broken code, self-review is rearranging deck chairs.

## The fix loop

I added a third step: after reviewing its code, ask the model to fix the issues it found. Results are mixed.

For the top-tier models (Sonnet, Opus, o3-mini), the fix step has minimal impact — the original code was already 98% passing. For mid-tier models, it sometimes helps and sometimes makes things *worse* — the model returns prose instead of code, or "fixes" things that weren't broken.

The fix loop needs more work. But the preliminary signal is: it's not the silver bullet. A model that can't write good code in the first place doesn't reliably fix it either.

## What I take away

**Run the code.** Review is useful but not sufficient. Our two independent reviewers (Opus 4 and GPT-4o) agreed on only 71% of findings. Test suites agreed with themselves 100% of the time.

**Cost efficiency matters more than marginal quality.** DeepSeek at $0.03/run with 96% pass rate is better value than Opus 4 at $2.13/run with 98%. For most workflows, the cheapest model above 90% is the right choice.

**The top three models are interchangeable on quality.** Sonnet 4, Opus 4, and o3-mini all hit 98%. Pick based on cost and latency, not quality — they're within noise of each other.

**Parsing tasks are where models consistently fail.** If you're generating parsers, validators, or anything that handles structured input, don't trust single-shot output. Test it.

**Self-review helps the models that need it least.** The models that write the best code are also the best at catching their own mistakes. The models that write the worst code can't reliably improve it. This is a fundamental limitation of same-model self-review.

## Caveats

52 challenges and 5 runs per model is a much larger sample than Part 1, but individual challenge results still have variance. The independent reviewer (Opus 4) is systematically stricter than GPT-4o — kappa of 0.40 on the cross-validation. Test suites are hand-written and cover basics + edge cases, not exhaustive. Go and Rust challenges (4 of 52) don't have execution tests. Three models (Kimi K2.5, GLM-5, Qwen 3.5 Plus) have limited run data due to unreliable API providers.

The scoring tooling and methodology are [open source](https://github.com/koktsgundars/self-issue-bench). The challenge prompts are not published to avoid contaminating future model training data.
