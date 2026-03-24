# Self-Issue Benchmark Report

Generated: 2026-03-24 14:08

Models compared: 12
Challenges: 22

## Cross-Model Comparison

| Model | Runs | Total Issues | Weighted | Correctness | Edge Case | Security | Style | Self-Catch Rate |
|-------|------|-------------|---------|-------------|-----------|----------|-------|----------------|
| kimi-k2.5 | 2 | 7.5 +/- 10.6 | 15.0 +/- 21.2 | 4.0 | 3.5 | 0.0 | 0.0 | 33% +/- 0% |
| minimax-m2.5 | 2 | 13.0 +/- 2.8 | 28.0 +/- 1.4 | 7.0 | 5.0 | 0.0 | 1.0 | 54% +/- 1% |
| glm-5 | 2 | 15.0 +/- 7.1 | 36.0 +/- 15.6 | 9.5 | 4.5 | 0.0 | 1.0 | 52% +/- 18% |
| o3-mini | 2 | 15.0 +/- 4.2 | 29.0 +/- 8.5 | 3.0 | 11.0 | 0.0 | 1.0 | 76% +/- 22% |
| opus-4 | 2 | 15.0 +/- 5.7 | 27.5 +/- 10.6 | 4.5 | 10.0 | 0.0 | 0.5 | 72% +/- 27% |
| sonnet-4-strict-2pass | 2 | 15.0 +/- 4.2 | 29.0 +/- 12.7 | 6.0 | 8.5 | 0.0 | 0.5 | 72% +/- 16% |
| qwen-3.5-plus | 2 | 17.0 +/- 0.0 | 34.5 +/- 4.9 | 6.5 | 10.5 | 0.0 | 0.0 | 26% +/- 29% |
| gpt-4o | 2 | 19.0 +/- 12.7 | 41.0 +/- 31.1 | 11.0 | 7.0 | 0.0 | 1.0 | 38% +/- 3% |
| haiku-4.5 | 2 | 20.0 +/- 11.3 | 44.0 +/- 26.9 | 11.5 | 4.5 | 1.5 | 2.5 | 80% +/- 17% |
| gpt-4o-mini | 2 | 21.0 +/- 12.7 | 47.0 +/- 36.8 | 15.5 | 5.0 | 0.0 | 0.5 | 45% +/- 7% |
| gemini-3.1-pro | 2 | 22.0 +/- 2.8 | 56.0 +/- 19.8 | 15.0 | 6.5 | 0.0 | 0.5 | 51% +/- 16% |
| deepseek-v3.2 | 2 | 24.5 +/- 2.1 | 51.0 +/- 9.9 | 12.0 | 11.0 | 0.0 | 1.5 | 54% +/- 22% |

## Per-Challenge Breakdown

| Challenge | deepseek-v3.2 | gemini-3.1-pro | glm-5 | gpt-4o | gpt-4o-mini | haiku-4.5 | kimi-k2.5 | minimax-m2.5 | o3-mini | opus-4 | qwen-3.5-plus | sonnet-4-strict-2pass |
|-----------|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| c1_fibonacci | 1.5 | 1.0 | 0.5 | 1.0 | 0.5 | 0.0 | 0.0 | 0.5 | 1.5 | 0.0 | 1.0 | 0.0 |
| c2_palindrome | 1.5 | 1.0 | 0.0 | 2.5 | 2.5 | 3.0 | 0.0 | 0.0 | 1.5 | 1.5 | 1.0 | 1.5 |
| c3_word_frequency | 1.0 | 0.0 | 0.5 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 | 0.0 | 0.5 |
| c4_array_dedup | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| c5_deep_clone | 3.0 | 2.0 | 2.5 | 1.0 | 1.5 | 1.0 | 1.5 | 0.0 | 1.0 | 0.5 | 3.0 | 1.5 |
| c6_csv_parser | 1.0 | 2.0 | 2.5 | 0.5 | 1.0 | 1.5 | 0.5 | 0.5 | 1.0 | 1.0 | 1.0 | 1.5 |
| c7_retry | 0.5 | 0.5 | 0.5 | 0.5 | 1.0 | 0.0 | 0.5 | 0.5 | 1.0 | 0.0 | 0.5 | 0.0 |
| c8_token_counter | 1.0 | 0.0 | 0.5 | 0.0 | 0.5 | 0.0 | 0.5 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| c9_url_parser | 3.0 | 4.0 | 2.5 | 1.5 | 1.5 | 1.5 | 2.5 | 2.5 | 1.5 | 1.5 | 2.5 | 1.0 |
| c10_debounce | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| c11_lru_cache | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.5 | 0.0 | 0.5 |
| c12_flatten_array | 1.0 | 1.0 | 1.0 | 0.5 | 1.0 | 1.5 | 0.0 | 0.5 | 1.0 | 1.0 | 1.0 | 0.5 |
| c13_date_formatter | 0.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| c14_binary_search | 2.5 | 2.5 | 2.0 | 1.5 | 3.0 | 2.5 | 0.0 | 2.0 | 1.5 | 2.0 | 2.0 | 1.5 |
| c15_rate_limiter | 0.0 | 0.0 | 0.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.5 | 0.0 | 0.5 | 0.0 | 0.5 |
| c16_html_entity_decoder | 1.5 | 1.5 | 0.5 | 0.5 | 0.5 | 0.5 | 1.5 | 1.5 | 0.5 | 0.5 | 1.5 | 0.5 |
| c17_concurrent_map | 0.5 | 0.5 | 0.0 | 1.0 | 1.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| c18_iterator | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 |
| c19_ring_buffer | 1.0 | 0.0 | 0.5 | 1.0 | 1.0 | 1.0 | 0.0 | 1.0 | 1.0 | 1.0 | 0.0 | 1.0 |
| c20_expression_parser | 2.5 | 3.0 | 0.0 | 2.0 | 2.0 | 1.5 | 0.0 | 0.5 | 1.0 | 0.0 | 1.0 | 1.5 |
| c21_task_scheduler | 1.0 | 0.0 | 0.5 | 1.5 | 1.0 | 0.5 | 0.0 | 1.0 | 0.0 | 1.0 | 0.0 | 1.0 |
| c22_markdown_renderer | 1.5 | 3.0 | 0.5 | 3.0 | 2.5 | 3.0 | 0.0 | 0.0 | 1.5 | 2.0 | 2.5 | 2.0 |

## Issue Types by Challenge

Mean issues of each type per model, summed across all models.

| Challenge | Correctness | Edge Case | Security | Style | Total |
|-----------|-------------|-----------|----------|-------|-------|
| c1_fibonacci | 4 | 4 | 0 | 0 | 8 |
| c2_palindrome | 10 | 6 | 0 | 0 | 16 |
| c3_word_frequency | 1 | 4 | 0 | 0 | 5 |
| c4_array_dedup | 0 | 0 | 0 | 0 | 1 |
| c5_deep_clone | 2 | 16 | 0 | 0 | 18 |
| c6_csv_parser | 8 | 6 | 0 | 0 | 14 |
| c7_retry | 4 | 1 | 0 | 1 | 6 |
| c8_token_counter | 2 | 2 | 0 | 0 | 4 |
| c9_url_parser | 10 | 16 | 0 | 0 | 26 |
| c10_debounce | 0 | 0 | 0 | 0 | 0 |
| c11_lru_cache | 0 | 1 | 0 | 0 | 2 |
| c12_flatten_array | 6 | 2 | 0 | 2 | 10 |
| c13_date_formatter | 1 | 0 | 0 | 0 | 1 |
| c14_binary_search | 18 | 5 | 0 | 0 | 23 |
| c15_rate_limiter | 1 | 1 | 0 | 0 | 2 |
| c16_html_entity_decoder | 6 | 5 | 0 | 0 | 11 |
| c17_concurrent_map | 2 | 0 | 0 | 1 | 4 |
| c18_iterator | 2 | 0 | 0 | 0 | 2 |
| c19_ring_buffer | 4 | 4 | 0 | 1 | 8 |
| c20_expression_parser | 10 | 6 | 0 | 0 | 15 |
| c21_task_scheduler | 4 | 2 | 0 | 1 | 8 |
| c22_markdown_renderer | 14 | 7 | 0 | 0 | 22 |

## Challenge Discrimination

Challenges ranked by how many models have issues (higher = more discriminating).

| Challenge | Models with Issues | Total Issues Across Models |
|-----------|-------------------|---------------------------|
| c9_url_parser | 12/12 | 26 |
| c6_csv_parser | 12/12 | 14 |
| c16_html_entity_decoder | 12/12 | 11 |
| c14_binary_search | 11/12 | 23 |
| c5_deep_clone | 11/12 | 18 |
| c12_flatten_array | 11/12 | 10 |
| c22_markdown_renderer | 10/12 | 22 |
| c2_palindrome | 9/12 | 16 |
| c20_expression_parser | 9/12 | 15 |
| c19_ring_buffer | 9/12 | 8 |
| c7_retry | 9/12 | 6 |
| c21_task_scheduler | 8/12 | 8 |
| c1_fibonacci | 8/12 | 8 |
| c3_word_frequency | 6/12 | 5 |
| c8_token_counter | 5/12 | 4 |
| c17_concurrent_map | 4/12 | 4 |
| c15_rate_limiter | 4/12 | 2 |
| c11_lru_cache | 3/12 | 2 |
| c18_iterator | 2/12 | 2 |
| c13_date_formatter | 2/12 | 1 |
| c4_array_dedup | 1/12 | 1 |
| c10_debounce | 1/12 | 0 |

## Self-Catch Analysis

| Model | Self-Catch Rate | Issues Caught | Issues Missed |
|-------|----------------|---------------|---------------|
| haiku-4.5 | 80% | 16 | 4 |
| o3-mini | 76% | 11 | 4 |
| sonnet-4-strict-2pass | 72% | 11 | 4 |
| opus-4 | 72% | 11 | 4 |
| deepseek-v3.2 | 54% | 13 | 11 |
| minimax-m2.5 | 54% | 7 | 6 |
| glm-5 | 52% | 8 | 7 |
| gemini-3.1-pro | 51% | 11 | 11 |
| gpt-4o-mini | 45% | 9 | 12 |
| gpt-4o | 38% | 7 | 12 |
| kimi-k2.5 | 33% | 2 | 5 |
| qwen-3.5-plus | 26% | 4 | 12 |

## Self-Catch Rate by Issue Type

| Model | Correctness | Edge Case | Security | Style |
|-------|-------------|-----------|----------|-------|
| deepseek-v3.2 | 50% (12/24) | 64% (14/22) | - | 0% (0/3) |
| gemini-3.1-pro | 67% (20/30) | 15% (2/13) | - | 100% (1/1) |
| glm-5 | 53% (10/19) | 78% (7/9) | - | 0% (0/2) |
| gpt-4o | 27% (6/22) | 57% (8/14) | - | 0% (0/2) |
| gpt-4o-mini | 42% (13/31) | 50% (5/10) | - | 0% (0/1) |
| haiku-4.5 | 74% (17/23) | 89% (8/9) | 100% (3/3) | 40% (2/5) |
| kimi-k2.5 | 25% (2/8) | 43% (3/7) | - | - |
| minimax-m2.5 | 57% (8/14) | 50% (5/10) | - | 50% (1/2) |
| o3-mini | 67% (4/6) | 77% (17/22) | - | 50% (1/2) |
| opus-4 | 67% (6/9) | 70% (14/20) | - | 0% (0/1) |
| qwen-3.5-plus | 15% (2/13) | 33% (7/21) | - | - |
| sonnet-4-strict-2pass | 58% (7/12) | 82% (14/17) | - | 0% (0/1) |

## Token Efficiency

| Model | Gen Tokens | Review Tokens | Total Tokens | Review Tokens/Issue |
|-------|-----------|--------------|-------------|-------------------|
| gpt-4o | 3,912 | 8,566 | 12,478 | 451 |
| gpt-4o-mini | 3,830 | 9,670 | 13,501 | 460 |
| deepseek-v3.2 | 5,077 | 8,826 | 13,904 | 360 |
| opus-4 | 4,900 | 9,968 | 14,868 | 665 |
| sonnet-4-strict-2pass | 5,178 | 10,885 | 16,063 | 726 |
| haiku-4.5 | 7,092 | 14,322 | 21,414 | 716 |
| o3-mini | 11,876 | 25,910 | 37,786 | 1727 |
| gemini-3.1-pro | 28,564 | 31,222 | 59,786 | 1419 |
| kimi-k2.5 | 34,156 | 41,331 | 75,487 | 5511 |
| minimax-m2.5 | 25,400 | 51,901 | 77,300 | 3992 |
| glm-5 | 33,492 | 48,192 | 81,685 | 3213 |
| qwen-3.5-plus | 61,416 | 96,798 | 158,215 | 5694 |

## Key Findings

- **Fewest issues**: kimi-k2.5 (8 issues)
- **Most issues**: deepseek-v3.2 (24 issues)
- **Best self-catch rate**: haiku-4.5 (80%)
- **Worst self-catch rate**: qwen-3.5-plus (26%)
