# I Added Four More Models To My Coding Benchmark. Two Of My Findings Didn't Survive.

*Part 3 of [I Benchmarked Whether AI Coding Assistants Know When They Screw Up](https://gundarskokts.substack.com/p/i-benchmarked-whether-ai-coding-assistants). [Part 2 is here](https://gundarskokts.substack.com/p/your-coding-assistant-knows-its-code).*

Last post, I made two confident claims about self-issue rates in coding assistants:

1. **The best models are the best self-reviewers.** Opus 4 had the highest test pass rate (98%) and the highest self-catch rate (79%). The pattern held down the rankings.
2. **The fix loop is mostly pointless for top-tier models.** I called it "mixed/preliminary" and moved on.

Then I added four more models: Qwen 3.5 Plus, Gemma 4 31B, Kimi K2.5, and GLM-5. The benchmark is now **14 models × 52 challenges × 5 runs**, with the same dual evaluation (LLM review + real test execution).

The new data weakens the first claim and outright inverts the second. Here's what I got wrong.

## Finding #1: Qwen 3.5 Plus broke my self-catch story

Last post, the cleanest finding was a positive correlation: models that pass more tests also catch more of their own bugs. Opus at 98%/79%, Sonnet at 98%/71%, DeepSeek at 96%/67%. Haiku was the exception at the bottom (73%/65%) and I handwaved it.

Qwen 3.5 Plus does not fit.

| Model | Test Pass | Self-Catch |
|---|---|---|
| Opus 4 | 98% | **79%** |
| Qwen 3.5 Plus | 98% | **33%** |
| Sonnet 4 | 98% | 71% |
| o3-mini | 97% | 40% |
| Gemma 4 31B | 96% | 71% |

Qwen writes code at the top tier — statistically indistinguishable from Opus, Sonnet, and o3-mini at 98% test pass (pairwise bootstrap p > 0.9 across the four). But when asked to find its own bugs, it catches 33% of them. That's bottom-quartile territory, sitting next to GPT-4o (27%) and GLM-5 (23%).

GPT-4o was already a crack in the story (94% test pass, 27% self-catch). Qwen widens it enough that the narrative "best coders are best self-reviewers" is no longer something I'd put my name on. The softer version survives — there *is* a positive correlation across the 14 models — but it has meaningful counterexamples at both the top (Qwen) and the mid (GPT-4o).

**The real finding is quieter:** writing good code and catching your own bugs appear to be partially independent capabilities. Opus and Sonnet get both. Qwen and GPT-4o get the first without the second. Haiku gets the second without the first. Which of those profiles is most useful depends entirely on your workflow.

## Finding #2: The fix loop is for models that need help, not models that don't

I made test_results_fixed data comparable across models and tallied what actually happens when a model is shown its own review and asked to fix the issues. The result was the opposite of what I expected.

| Model | Original → Fixed | Net change |
|---|---|---|
| Haiku 4.5 | 73% → 95% | **+22pp** |
| GLM-5 | 73% → 89% | **+16pp** |
| MiniMax M2.5 | 84% → 95% | **+11pp** |
| Kimi K2.5 | 75% → 87% | **+12pp** |
| Opus 4 | 98% → 98% | ±0 |
| o3-mini | 97% → 97% | ±0 |
| Sonnet 4 | 98% → 97% | −1pp |
| DeepSeek V3.2 | 96% → 94% | −2pp |
| GPT-4o-mini | 92% → 91% | −1pp |
| Gemini 3.1 Pro | 93% → 91% | −2pp |
| GPT-4o | 94% → 94% | 0 |
| Nemotron 3 Super | 91% → 81% | **−10pp** |
| Qwen 3.5 Plus | 98% → 94% | **−4pp** |

Read this carefully. The models with the most to gain from the fix loop are the ones at 73-84% — Haiku, GLM-5, Kimi, MiniMax. Haiku goes from 73% to 95%. That's not polish; that's transformation.

The top tier gets nothing, or regresses. Opus, Sonnet, o3-mini, Qwen, DeepSeek — all flat or worse after the fix step. **Seven of thirteen models pass fewer tests after self-review and fix than they did on first-try.**

The Nemotron 3 Super result is the sharpest. It starts at 91%, is shown a review, attempts a fix, and ends at 81%. A ten-percentage-point regression driven by the model "fixing" things that weren't broken.

Last post I called the fix loop "mixed and preliminary." That wasn't wrong, but it hid the real shape of the result. The actual finding is:

**The fix loop is a reliability amplifier for mid-tier models. It is not polish for top-tier models — for the top tier, it's a liability.**

If you're using a model that's already at 97-98% on trivial tasks, adding a self-review-and-fix step costs you tests. If you're using a model that sits at 73-85%, it's the cheapest quality gain you'll find.

## Bonus finding: Open-weights caught up

Not the headline, but worth noting. Two of the four new models are open-weights:

- **Qwen 3.5 Plus: 98% test pass** — tied with Opus 4, Sonnet 4, and o3-mini (p > 0.9 across all pairwise comparisons). No statistically significant difference.
- **Gemma 4 31B: 96% test pass** — tied with DeepSeek V3.2, ahead of GPT-4o (94%), Gemini 3.1 Pro (93%), GPT-4o-mini (92%), and Nemotron 3 Super (91%).

For the narrow question of "how many issues does this model introduce into trivial, single-function code," open-weights is not a compromise anymore. The gap I assumed existed doesn't, at least not on this task class.

Note the limitation: this measures only trivial, well-specified tasks with deterministic outputs. It says nothing about agentic workflows, long-context work, tool use, or anything that involves planning. It's one narrow axis.

## Bonus finding: Ten challenges where every model fails

Across all 14 models, there are ten challenges where **not one** manages a clean run:

- URL parser
- HTML sanitizer
- Deep clone
- Binary search
- Cron parser
- Result type (TypeScript)
- SQL tokenizer
- Markdown renderer
- Palindrome (yes, really — always a variant issue)
- CSV parser

Eight of the ten are parsers or spec-heavy utilities. The pattern from the previous post — "parsing is where models fail" — held up with three times the models. If your workflow involves generating parsers, sanitizers, or format converters with an LLM, assume there is a bug in the output and plan accordingly.

## What I'd say differently now

Revised takeaways:

1. **Run the code.** Still true, more so. With 14 models now, review-vs-test agreement is 43-65% — barely above chance for the middle of the distribution. Reviews are supplementary, not substitute.
2. **Writing good code and finding your own bugs are partially independent skills.** Opus, Sonnet, Gemma, and Haiku are strong at both. Qwen, o3-mini, GPT-4o, and GLM-5 are asymmetric. The correlation is real but noisy.
3. **The fix loop helps weak models, not strong ones.** If you're pairing an LLM with self-review for quality, do it on Haiku/Kimi/GLM-5/MiniMax — not on Opus or Qwen. For top-tier models, skip it.
4. **Open-weights is no longer a quality compromise for trivial code.** Qwen 3.5 Plus and Gemma 4 31B match or beat most proprietary models.
5. **Parsers are where every model fails.** Fourteen for fourteen. Don't trust single-shot LLM output for format parsing, period.

## Caveats

14 models, 52 challenges, 5 runs, 345 validated tests (with a 100% kill rate on mutation tests of the reference implementations — the tests catch every bug I could plant). The independent reviewer is still Claude Opus 4, cross-validated against GPT-4o with Cohen's κ = 0.40 (moderate agreement). Kimi K2.5, GLM-5, and Qwen 3.5 Plus had provider-side reliability problems during the initial fix-step runs, which I backfilled with a separate tool that replays the fix step against the new validation logic. That backfill completed this week and is reflected in the numbers above.

Tasks are canonical and some overlap with any plausible training set. I'm not publishing the challenge prompts to reduce future contamination, but the tasks themselves (URL parser, CSV parser, etc.) are fundamentally well-known. This benchmark measures how cleanly a model handles problems it has almost certainly seen versions of — which is exactly the scenario most practitioners care about.

All tooling is [open source](https://github.com/koktsgundars/self-issue-bench).
