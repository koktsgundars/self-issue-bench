# Self-Issue Benchmark Report

Generated: 2026-03-23 18:53

Models compared: 12
Challenges: 16

## Cross-Model Comparison

| Model | Runs | Total Issues | Weighted | Correctness | Edge Case | Security | Style | Self-Catch Rate |
|-------|------|-------------|---------|-------------|-----------|----------|-------|----------------|
| gpt-4o | 1 | 10 | 19 | 3 | 6 | 0 | 1 | 40% |
| opus-4 | 1 | 11 | 20 | 4 | 7 | 0 | 0 | 91% |
| gpt-4o-mini | 1 | 12 | 21 | 5 | 6 | 0 | 1 | 50% |
| haiku-4.5 | 1 | 12 | 25 | 6 | 5 | 1 | 0 | 92% |
| o3-mini | 1 | 12 | 23 | 3 | 8 | 0 | 1 | 92% |
| sonnet-4-strict-2pass | 1 | 12 | 20 | 3 | 9 | 0 | 0 | 83% |
| kimi-k2.5 | 1 | 15 | 30 | 8 | 7 | 0 | 0 | 33% |
| minimax-m2.5 | 1 | 15 | 29 | 5 | 8 | 0 | 2 | 53% |
| qwen-3.5-plus | 1 | 17 | 38 | 4 | 13 | 0 | 0 | 47% |
| gemini-3.1-pro | 1 | 20 | 42 | 8 | 12 | 0 | 0 | 40% |
| glm-5 | 1 | 20 | 47 | 11 | 8 | 0 | 1 | 65% |
| deepseek-v3.2 | 1 | 23 | 44 | 9 | 14 | 0 | 0 | 70% |

## Per-Challenge Breakdown

| Challenge | deepseek-v3.2 | gemini-3.1-pro | glm-5 | gpt-4o | gpt-4o-mini | haiku-4.5 | kimi-k2.5 | minimax-m2.5 | o3-mini | opus-4 | qwen-3.5-plus | sonnet-4-strict-2pass |
|-----------|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| c1_fibonacci | - | - | - | - | - | - | - | - | - | - | - | - |
| c2_palindrome | - | - | - | - | - | - | - | - | - | - | - | - |
| c3_word_frequency | 2 | - | 1 | - | - | 2 | - | - | 2 | 2 | - | 1 |
| c4_array_dedup | - | - | - | 2 | - | - | - | - | - | - | - | - |
| c5_deep_clone | 6 | 4 | 5 | 2 | 3 | 2 | 3 | - | 2 | 1 | 6 | 3 |
| c6_csv_parser | 2 | 4 | 5 | 1 | 2 | 3 | 1 | 1 | 2 | 2 | 2 | 3 |
| c7_retry | 1 | 1 | 1 | 1 | 2 | - | 1 | 1 | 2 | - | 1 | - |
| c8_token_counter | 2 | - | 1 | - | 1 | - | 1 | 2 | - | - | - | - |
| c9_url_parser | 6 | 8 | 5 | 3 | 3 | 3 | 5 | 5 | 3 | 3 | 5 | 2 |
| c10_debounce | - | - | - | - | - | - | 1 | - | - | - | - | - |
| c11_lru_cache | - | - | - | - | - | - | - | 2 | - | 1 | - | 1 |
| c12_flatten_array | - | - | - | - | - | - | - | - | - | - | - | - |
| c13_date_formatter | 1 | - | - | - | - | 1 | - | - | - | - | - | - |
| c14_binary_search | - | - | - | - | - | - | - | - | - | - | - | - |
| c15_rate_limiter | - | - | 1 | - | - | - | - | 1 | - | 1 | - | 1 |
| c16_html_entity_decoder | 3 | 3 | 1 | 1 | 1 | 1 | 3 | 3 | 1 | 1 | 3 | 1 |

## Challenge Discrimination

Challenges ranked by how many models have issues (higher = more discriminating).

| Challenge | Models with Issues | Total Issues Across Models |
|-----------|-------------------|---------------------------|
| c9_url_parser | 12/12 | 51 |
| c6_csv_parser | 12/12 | 28 |
| c16_html_entity_decoder | 12/12 | 22 |
| c5_deep_clone | 11/12 | 37 |
| c7_retry | 9/12 | 11 |
| c3_word_frequency | 6/12 | 10 |
| c8_token_counter | 5/12 | 7 |
| c15_rate_limiter | 4/12 | 4 |
| c11_lru_cache | 3/12 | 4 |
| c13_date_formatter | 2/12 | 2 |
| c4_array_dedup | 1/12 | 2 |
| c10_debounce | 1/12 | 1 |

**Trivial challenges** (no issues across any model): c1_fibonacci, c2_palindrome, c12_flatten_array, c14_binary_search

## Self-Catch Analysis

| Model | Self-Catch Rate | Issues Caught | Issues Missed |
|-------|----------------|---------------|---------------|
| o3-mini | 92% | 11 | 1 |
| haiku-4.5 | 92% | 11 | 1 |
| opus-4 | 91% | 10 | 1 |
| sonnet-4-strict-2pass | 83% | 10 | 2 |
| deepseek-v3.2 | 70% | 16 | 7 |
| glm-5 | 65% | 13 | 7 |
| minimax-m2.5 | 53% | 8 | 7 |
| gpt-4o-mini | 50% | 6 | 6 |
| qwen-3.5-plus | 47% | 8 | 9 |
| gpt-4o | 40% | 4 | 6 |
| gemini-3.1-pro | 40% | 8 | 12 |
| kimi-k2.5 | 33% | 5 | 10 |

## Key Findings

- **Fewest issues**: gpt-4o (10 issues)
- **Most issues**: deepseek-v3.2 (23 issues)
- **Best self-catch rate**: o3-mini (92%)
- **Worst self-catch rate**: kimi-k2.5 (33%)
