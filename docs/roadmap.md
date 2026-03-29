# Roadmap to Arxiv Submission

## Critical (must-have for submission)

- [ ] **Cross-reviewer validation** — re-run independent review with a second reviewer model (e.g. GPT-4o) on ~20% of runs. Report inter-reviewer agreement. If <60%, address subjectivity in methodology.
- [ ] **Test suite validation** — write reference implementations for each challenge. Verify all tests pass on reference code and fail on intentionally buggy variants.
- [ ] **Statistical significance** — add confidence intervals and pairwise significance tests (bootstrap or paired t-test) to scoring pipeline. No model-to-model claims without p-values.
- [ ] **Prompt contamination argument** — address in paper: challenges are standard tasks by design; we measure execution quality, not capability.

## Important (strengthens the paper)

- [ ] **Difficulty calibration** — tier challenges into easy/medium/hard based on empirical failure rates. Report results per tier.
- [ ] **Comparison to existing benchmarks** — correlate our rankings with HumanEval/SWE-bench/LiveCodeBench. Divergence = novelty story.
- [ ] **Cost-effectiveness analysis** — quality per dollar using token counts + public API pricing.
- [ ] **Go/Rust execution** — install toolchains or drop 4 challenges.
- [ ] **Complete missing models** — Kimi K2.5, GLM-5, Qwen 3.5 Plus with 5 runs each.

## Nice to have

- [ ] More models (Llama, Mistral, Codestral, etc.)
- [ ] Prompt sensitivity analysis (bare prompt vs "be careful about edge cases")
- [ ] Website / leaderboard (GitHub Pages)
- [ ] Fix loop analysis (deeper dive into when self-fix helps vs hurts)

## Paper structure

- [ ] Abstract
- [ ] Introduction (the gap between what models produce and what they know)
- [ ] Related work (HumanEval, SWE-bench, LiveCodeBench, CodeContests — how we differ)
- [ ] Methodology (protocol, challenges, scoring, metrics)
- [ ] Results (rankings, self-catch analysis, test-review agreement, fix effectiveness)
- [ ] Discussion (what the metrics mean for practitioners)
- [ ] Limitations
- [ ] Conclusion
