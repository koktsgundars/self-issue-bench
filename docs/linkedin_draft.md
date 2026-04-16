I added four more LLMs to my coding benchmark. Two of my earlier claims didn't survive.

Benchmark: 14 models, 52 well-specified single-function tasks, 5 runs each, 345 validated tests, dual evaluation (LLM review + real execution). No tools, no agents, no IDE — just the raw quality of what each model emits on first ask.

New finding #1: Writing good code and catching your own bugs are partially independent skills.

Qwen 3.5 Plus passes 98% of tests — statistically tied with Opus 4, Sonnet 4, and o3-mini at the top. But when asked to find its own bugs, it catches only 33%. GPT-4o is worse at 27%. Meanwhile Haiku 4.5 catches 65% of its issues while passing just 73% of tests. The "best coders are best self-reviewers" story has meaningful counterexamples at the top, the middle, and the bottom. Pick for workflow, not for a clean narrative.

New finding #2: The self-review-and-fix loop is for models that need help — not polish for models that don't.

Haiku 4.5 goes from 73% → 95% after one fix step (+22pp). GLM-5 goes 73% → 89%. Kimi K2.5 goes 75% → 87%. MiniMax M2.5 goes 84% → 95%.

Top-tier models? Opus, Sonnet, o3-mini, Qwen, DeepSeek: flat or worse. Nemotron 3 Super drops from 91% to 81% — a ten-point regression from "fixing" things that weren't broken.

Seven of thirteen models pass fewer tests after self-review and fix than they did on first try. The fix loop is a reliability amplifier for mid-tier models and a liability for top-tier ones.

Also worth noting:
→ Open-weights has closed the gap on trivial code. Qwen 3.5 Plus and Gemma 4 31B match or beat every proprietary model below Opus/Sonnet.
→ Every one of the 14 models produces defects on URL parsing, HTML sanitization, CSV parsing, cron parsing, and SQL tokenization. No exceptions. Don't trust single-shot LLM output for parsers.
→ LLM review and test execution agree only 43-65% of the time across models. Run the code. Don't trust the review.

Full writeup, methodology, and heatmaps: [link to Substack]

Benchmark tooling is open source: github.com/koktsgundars/self-issue-bench
