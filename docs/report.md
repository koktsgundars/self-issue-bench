# Self-Issue Benchmark Report

Generated: 2026-03-21 17:55

Models compared: 6
Challenges: 16

## Cross-Model Comparison

| Model | Runs | Total Issues | Correctness | Edge Case | Security | Style | Self-Catch Rate |
|-------|------|-------------|-------------|-----------|----------|-------|----------------|
| gpt-4o | 1 | 10 | 3 | 6 | 0 | 1 | 40% |
| opus-4 | 1 | 11 | 4 | 7 | 0 | 0 | 91% |
| gpt-4o-mini | 1 | 12 | 5 | 6 | 0 | 1 | 50% |
| haiku-4.5 | 1 | 12 | 6 | 5 | 1 | 0 | 92% |
| o3-mini | 1 | 12 | 3 | 8 | 0 | 1 | 92% |
| sonnet-4-strict-2pass | 1 | 12 | 3 | 9 | 0 | 0 | 83% |

## Per-Challenge Breakdown

| Challenge | gpt-4o | gpt-4o-mini | haiku-4.5 | o3-mini | opus-4 | sonnet-4-strict-2pass |
|-----------|---:|---:|---:|---:|---:|---:|
| c1_fibonacci | - | - | - | - | - | - |
| c2_palindrome | - | - | - | - | - | - |
| c3_word_frequency | - | - | 2 | 2 | 2 | 1 |
| c4_array_dedup | 2 | - | - | - | - | - |
| c5_deep_clone | 2 | 3 | 2 | 2 | 1 | 3 |
| c6_csv_parser | 1 | 2 | 3 | 2 | 2 | 3 |
| c7_retry | 1 | 2 | - | 2 | - | - |
| c8_token_counter | - | 1 | - | - | - | - |
| c9_url_parser | 3 | 3 | 3 | 3 | 3 | 2 |
| c10_debounce | - | - | - | - | - | - |
| c11_lru_cache | - | - | - | - | 1 | 1 |
| c12_flatten_array | - | - | - | - | - | - |
| c13_date_formatter | - | - | 1 | - | - | - |
| c14_binary_search | - | - | - | - | - | - |
| c15_rate_limiter | - | - | - | - | 1 | 1 |
| c16_html_entity_decoder | 1 | 1 | 1 | 1 | 1 | 1 |

## Challenge Discrimination

Challenges ranked by how many models have issues (higher = more discriminating).

| Challenge | Models with Issues | Total Issues Across Models |
|-----------|-------------------|---------------------------|
| c9_url_parser | 6/6 | 17 |
| c6_csv_parser | 6/6 | 13 |
| c5_deep_clone | 6/6 | 13 |
| c16_html_entity_decoder | 6/6 | 6 |
| c3_word_frequency | 4/6 | 7 |
| c7_retry | 3/6 | 5 |
| c15_rate_limiter | 2/6 | 2 |
| c11_lru_cache | 2/6 | 2 |
| c4_array_dedup | 1/6 | 2 |
| c8_token_counter | 1/6 | 1 |
| c13_date_formatter | 1/6 | 1 |

**Trivial challenges** (no issues across any model): c1_fibonacci, c2_palindrome, c10_debounce, c12_flatten_array, c14_binary_search

## Self-Catch Analysis

| Model | Self-Catch Rate | Issues Caught | Issues Missed |
|-------|----------------|---------------|---------------|
| o3-mini | 92% | 11 | 1 |
| haiku-4.5 | 92% | 11 | 1 |
| opus-4 | 91% | 10 | 1 |
| sonnet-4-strict-2pass | 83% | 10 | 2 |
| gpt-4o-mini | 50% | 6 | 6 |
| gpt-4o | 40% | 4 | 6 |

## Common Failure Modes

Issues present across 3+ models on the same challenge:

*(Run `python runner/compare.py results/` for the latest comparison table)*

## Key Findings

- **Fewest issues**: gpt-4o (10 issues)
- **Most issues**: sonnet-4-strict-2pass (12 issues)
- **Best self-catch rate**: o3-mini (92%)
- **Worst self-catch rate**: gpt-4o (40%)
