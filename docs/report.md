# Self-Issue Benchmark Report

Generated: 2026-03-29 17:33

Models compared: 11
Challenges: 52

## Model Summary

| Model | Test Pass Rate | First-Try Pass | Self-Catch Rate | Issues | Clean Challenges | Review-Test Agreement |
|-------|---------------|----------------|-----------------|--------|-----------------|----------------------|
| opus-4 | 98% [97-98%] | 88% | 79% [76-82%] | 79 | 22/52 | 46% |
| sonnet-4 | 98% [97-98%] | 90% | 71% [69-73%] | 86 | 20/52 | 43% |
| o3-mini | 97% [96-98%] | 88% | 40% [36-44%] | 80 | 22/52 | 50% |
| deepseek-v3.2 | 96% [95-97%] | 84% | 67% [64-70%] | 102 | 17/52 | 46% |
| gpt-4o | 94% [92-95%] | 79% | 27% [23-31%] | 111 | 13/52 | 44% |
| gemini-3.1-pro | 93% [89-96%] | 79% | 40% [35-46%] | 88 | 22/52 | 58% |
| gpt-4o-mini | 92% [90-93%] | 73% | 50% [46-54%] | 123 | 12/52 | 47% |
| nemotron-3-super | 91% [87-94%] | 69% | 52% [48-57%] | 116 | 15/52 | 56% |
| minimax-m2.5 | 84% [81-87%] | 79% | 43% [37-48%] | 51 | 30/52 | 57% |
| haiku-4.5 | 73% [71-76%] | 55% | 65% [61-67%] | 142 | 11/52 | 63% |
| kimi-k2.5 | - | - | - | 0 | 52/52 | - |

## Statistical Significance (Test Pass Rate)

Pairwise bootstrap test (p < 0.05 = significant difference).

| | deepseek-v3.2 | gemini-3.1-pro | gpt-4o | gpt-4o-mini | haiku-4.5 | minimax-m2.5 | nemotron-3-super | o3-mini | opus-4 | sonnet-4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| deepseek-v3.2 | — | 0.11 | **0.014** | **0.000** | **0.000** | **0.000** | **0.002** | 0.17 | **0.010** | **0.019** |
| gemini-3.1-pro |  | — | 0.69 | 0.52 | **0.000** | **0.001** | 0.39 | **0.032** | **0.006** | **0.009** |
| gpt-4o |  |  | — | **0.034** | **0.000** | **0.000** | 0.12 | **0.000** | **0.000** | **0.000** |
| gpt-4o-mini |  |  |  | — | **0.000** | **0.000** | 0.64 | **0.000** | **0.000** | **0.000** |
| haiku-4.5 |  |  |  |  | — | **0.000** | **0.000** | **0.000** | **0.000** | **0.000** |
| minimax-m2.5 |  |  |  |  |  | — | **0.004** | **0.000** | **0.000** | **0.000** |
| nemotron-3-super |  |  |  |  |  |  | — | **0.000** | **0.000** | **0.000** |
| o3-mini |  |  |  |  |  |  |  | — | 0.53 | 0.58 |
| opus-4 |  |  |  |  |  |  |  |  | — | 0.94 |
| sonnet-4 |  |  |  |  |  |  |  |  |  | — |

Bold = statistically significant (p < 0.05). Upper triangle only.

## Cross-Model Comparison

| Model | Runs | Total Issues | Weighted | Correctness | Edge Case | Security | Style | Self-Catch Rate |
|-------|------|-------------|---------|-------------|-----------|----------|-------|----------------|
| kimi-k2.5 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | n/a |
| minimax-m2.5 | 5 | 51.0 +/- 30.9 | 109.6 +/- 66.0 | 27.2 | 21.6 | 0.6 | 1.6 | 43% +/- 7% |
| opus-4 | 5 | 78.6 +/- 4.2 | 158.8 +/- 8.6 | 35.2 | 39.6 | 2.0 | 1.8 | 79% +/- 4% |
| o3-mini | 5 | 80.2 +/- 2.4 | 151.4 +/- 5.9 | 31.8 | 44.0 | 2.6 | 1.8 | 40% +/- 5% |
| sonnet-4 | 5 | 86.4 +/- 5.1 | 174.4 +/- 17.0 | 44.4 | 38.6 | 1.6 | 1.8 | 71% +/- 2% |
| gemini-3.1-pro | 4 | 88.5 +/- 10.8 | 218.0 +/- 29.9 | 64.8 | 23.0 | 0.2 | 0.5 | 40% +/- 7% |
| deepseek-v3.2 | 5 | 102.0 +/- 11.0 | 215.8 +/- 21.6 | 56.2 | 41.4 | 1.4 | 3.0 | 67% +/- 4% |
| gpt-4o | 5 | 110.8 +/- 3.2 | 246.6 +/- 5.1 | 62.6 | 44.0 | 1.6 | 2.6 | 27% +/- 5% |
| nemotron-3-super | 5 | 115.6 +/- 14.9 | 260.2 +/- 40.0 | 76.4 | 31.0 | 3.0 | 5.2 | 52% +/- 6% |
| gpt-4o-mini | 5 | 122.8 +/- 4.8 | 287.8 +/- 8.0 | 80.4 | 39.2 | 1.6 | 1.6 | 50% +/- 5% |
| haiku-4.5 | 5 | 142.4 +/- 11.3 | 325.4 +/- 30.5 | 88.2 | 20.4 | 12.6 | 21.2 | 65% +/- 4% |

## Per-Challenge Breakdown

| Challenge | deepseek-v3.2 | gemini-3.1-pro | gpt-4o | gpt-4o-mini | haiku-4.5 | kimi-k2.5 | minimax-m2.5 | nemotron-3-super | o3-mini | opus-4 | sonnet-4 |
|-----------|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| c1_fibonacci | 2.0 | 1.5 | 2.4 | 3.0 | 0.0 | - | 0.6 | 0.6 | 1.2 | 0.2 | 0.8 |
| c2_palindrome | 3.8 | 3.2 | 4.4 | 4.0 | 4.2 | - | 2.0 | 4.0 | 3.0 | 2.8 | 3.2 |
| c3_word_frequency | 0.0 | 0.5 | 0.4 | 0.0 | 3.0 | - | 0.0 | 0.4 | 0.8 | 0.0 | 0.0 |
| c4_array_dedup | 0.0 | 0.0 | 0.4 | 0.0 | 0.0 | - | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| c5_deep_clone | 5.4 | 1.2 | 5.2 | 6.0 | 5.6 | - | 4.2 | 4.8 | 4.8 | 3.4 | 5.0 |
| c6_csv_parser | 2.8 | 3.5 | 2.2 | 3.6 | 5.6 | - | 1.0 | 3.2 | 2.6 | 3.4 | 3.4 |
| c7_retry | 0.8 | 1.0 | 0.4 | 0.6 | 2.8 | - | 0.4 | 2.0 | 1.0 | 0.0 | 1.0 |
| c8_token_counter | 0.0 | 0.5 | 1.6 | 1.4 | 0.0 | - | 0.0 | 1.2 | 1.8 | 0.6 | 1.4 |
| c9_url_parser | 5.2 | 6.0 | 6.6 | 5.2 | 5.4 | - | 3.2 | 4.6 | 4.8 | 4.8 | 4.6 |
| c10_debounce | 0.2 | 0.5 | 1.0 | 1.8 | 0.6 | - | 0.0 | 0.6 | 0.4 | 0.0 | 0.8 |
| c11_lru_cache | 0.4 | 0.8 | 0.0 | 0.2 | 1.0 | - | 0.0 | 0.2 | 0.0 | 0.2 | 0.0 |
| c12_flatten_array | 2.4 | 2.5 | 1.6 | 1.2 | 1.8 | - | 1.0 | 2.4 | 1.8 | 1.4 | 1.4 |
| c13_date_formatter | 0.6 | 0.2 | 0.2 | 0.0 | 4.4 | - | 0.0 | 0.4 | 0.0 | 0.0 | 0.0 |
| c14_binary_search | 3.8 | 4.8 | 4.6 | 5.0 | 6.0 | - | 2.0 | 5.0 | 3.6 | 3.4 | 3.8 |
| c15_rate_limiter | 0.0 | 0.0 | 0.4 | 0.4 | 0.0 | - | 0.8 | 0.8 | 0.6 | 0.0 | 0.8 |
| c16_html_entity_decoder | 1.2 | 2.0 | 2.0 | 2.6 | 4.2 | - | 1.4 | 2.6 | 2.0 | 1.0 | 2.2 |
| c17_concurrent_map | 1.0 | 1.0 | 2.0 | 2.0 | 0.0 | - | 1.0 | 0.8 | 0.0 | 0.0 | 0.0 |
| c18_iterator | 0.4 | 0.0 | 0.8 | 0.0 | 2.2 | - | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| c19_ring_buffer | 1.0 | 0.0 | 2.4 | 2.2 | 1.8 | - | 0.4 | 3.8 | 2.4 | 0.4 | 1.6 |
| c20_expression_parser | 3.0 | 5.2 | 3.4 | 4.6 | 3.6 | - | 0.4 | 4.6 | 1.8 | 0.4 | 2.8 |
| c21_task_scheduler | 2.6 | 0.5 | 2.6 | 2.8 | 4.6 | - | 1.4 | 3.6 | 0.8 | 1.4 | 0.6 |
| c22_markdown_renderer | 3.2 | 3.5 | 5.0 | 4.4 | 5.2 | - | 1.0 | 4.0 | 3.4 | 3.2 | 3.6 |
| c23_merge_intervals | 0.8 | 0.8 | 0.6 | 1.0 | 0.4 | - | 0.8 | 0.4 | 0.2 | 0.6 | 0.0 |
| c24_topological_sort | 1.6 | 0.2 | 1.8 | 1.6 | 2.2 | - | 0.4 | 0.6 | 0.4 | 1.6 | 0.0 |
| c25_edit_distance | 0.0 | 0.5 | 0.0 | 0.0 | 0.4 | - | 0.2 | 1.0 | 0.0 | 0.0 | 0.0 |
| c26_trie | 0.2 | 0.2 | 1.8 | 1.6 | 1.2 | - | 0.0 | 1.0 | 0.0 | 0.8 | 0.8 |
| c27_min_heap | 0.0 | 0.0 | 0.6 | 0.0 | 0.0 | - | 0.0 | 0.2 | 0.0 | 0.0 | 0.0 |
| c28_linked_list | 2.0 | 0.0 | 0.4 | 0.8 | 0.8 | - | 1.2 | 2.2 | 0.4 | 0.0 | 0.4 |
| c29_parse_cron | 5.0 | 4.8 | 4.0 | 5.0 | 5.0 | - | 1.4 | 3.0 | 4.2 | 4.4 | 4.4 |
| c30_tokenize_sql | 3.4 | 3.8 | 3.4 | 4.0 | 5.2 | - | 1.8 | 4.6 | 3.4 | 3.4 | 3.6 |
| c31_glob_match | 1.4 | 1.0 | 0.8 | 0.8 | 5.0 | - | 1.4 | 0.4 | 0.0 | 0.0 | 1.2 |
| c32_sanitize_html | 5.0 | 3.2 | 5.6 | 7.6 | 5.4 | - | 2.0 | 4.6 | 4.2 | 6.2 | 6.4 |
| c33_escape_shell | 1.6 | 0.5 | 1.6 | 1.8 | 1.8 | - | 1.0 | 1.8 | 1.4 | 0.6 | 1.4 |
| c34_diff_objects | 2.4 | 3.8 | 3.0 | 2.6 | 5.4 | - | 2.6 | 2.6 | 2.8 | 2.4 | 2.2 |
| c35_throttle | 2.2 | 0.5 | 2.6 | 2.0 | 2.6 | - | 1.0 | 1.6 | 1.0 | 1.8 | 0.8 |
| c36_flatten_object | 2.2 | 2.8 | 2.6 | 2.6 | 1.6 | - | 1.6 | 3.0 | 2.4 | 2.0 | 1.8 |
| c37_topological_sort | 1.8 | 1.2 | 1.8 | 2.0 | 2.0 | - | 0.4 | 1.2 | 1.0 | 0.8 | 0.8 |
| c38_priority_queue | 1.2 | 0.0 | 0.4 | 0.8 | 1.8 | - | 0.4 | 0.2 | 0.0 | 1.4 | 0.4 |
| c39_observable | 2.0 | 0.8 | 2.6 | 2.8 | 1.8 | - | 1.2 | 2.8 | 0.2 | 1.2 | 2.2 |
| c40_parse_query_string | 1.4 | 0.0 | 2.2 | 2.8 | 1.6 | - | 0.8 | 1.0 | 1.2 | 2.0 | 1.6 |
| c41_json_stream | 3.8 | 4.2 | 3.0 | 3.4 | 3.8 | - | 1.8 | 2.8 | 2.2 | 2.8 | 2.0 |
| c42_mustache | 5.6 | 3.5 | 5.2 | 4.8 | 5.2 | - | 0.6 | 5.2 | 3.4 | 4.6 | 3.8 |
| c43_escape_regexp | 0.4 | 0.5 | 1.0 | 1.2 | 0.8 | - | 0.6 | 0.8 | 1.0 | 1.0 | 1.0 |
| c44_validate_email | 1.4 | 2.8 | 2.2 | 4.0 | 3.2 | - | 1.2 | 1.4 | 1.2 | 1.0 | 1.4 |
| c45_binary_heap | 0.0 | 0.0 | 0.0 | 0.4 | 0.2 | - | 0.0 | 1.2 | 0.0 | 0.2 | 0.0 |
| c46_memoize | 0.2 | 0.0 | 0.2 | 1.0 | 2.0 | - | 0.6 | 1.6 | 0.0 | 0.4 | 0.0 |
| c47_typed_event_emitter | 2.4 | 2.0 | 0.8 | 1.2 | 2.6 | - | 1.4 | 3.4 | 1.0 | 2.0 | 2.0 |
| c48_result_type | 3.8 | 3.2 | 3.4 | 4.4 | 5.6 | - | 1.6 | 6.8 | 3.6 | 2.8 | 3.6 |
| c49_parse_route | 2.6 | 3.5 | 2.0 | 3.0 | 4.4 | - | 0.8 | 2.4 | 1.4 | 1.8 | 1.8 |
| c50_parse_ini | 2.2 | 0.0 | 2.0 | 1.6 | 3.4 | - | 0.6 | 1.2 | 1.4 | 1.0 | 0.0 |
| c51_deep_merge | 3.4 | 3.0 | 3.0 | 3.2 | 3.0 | - | 1.6 | 3.4 | 2.8 | 3.0 | 3.0 |
| c52_retry_ts | 2.2 | 3.2 | 2.6 | 3.8 | 2.0 | - | 1.2 | 3.6 | 2.6 | 2.2 | 2.8 |

## Issue Types by Challenge

Mean issues of each type per model, summed across all models.

| Challenge | Correctness | Edge Case | Security | Style | Total |
|-----------|-------------|-----------|----------|-------|-------|
| c1_fibonacci | 5 | 7 | 0 | 0 | 12 |
| c2_palindrome | 22 | 12 | 1 | 1 | 35 |
| c3_word_frequency | 2 | 2 | 0 | 1 | 5 |
| c4_array_dedup | 0 | 0 | 0 | 0 | 0 |
| c5_deep_clone | 2 | 42 | 0 | 1 | 46 |
| c6_csv_parser | 19 | 10 | 1 | 1 | 31 |
| c7_retry | 7 | 2 | 0 | 2 | 10 |
| c8_token_counter | 2 | 6 | 0 | 1 | 8 |
| c9_url_parser | 20 | 30 | 0 | 0 | 50 |
| c10_debounce | 3 | 2 | 0 | 0 | 6 |
| c11_lru_cache | 2 | 0 | 0 | 0 | 3 |
| c12_flatten_array | 12 | 4 | 0 | 1 | 18 |
| c13_date_formatter | 3 | 0 | 1 | 2 | 6 |
| c14_binary_search | 25 | 15 | 1 | 1 | 42 |
| c15_rate_limiter | 1 | 2 | 0 | 0 | 4 |
| c16_html_entity_decoder | 10 | 10 | 1 | 0 | 21 |
| c17_concurrent_map | 6 | 0 | 0 | 1 | 8 |
| c18_iterator | 1 | 0 | 0 | 2 | 3 |
| c19_ring_buffer | 7 | 7 | 0 | 2 | 16 |
| c20_expression_parser | 18 | 12 | 0 | 0 | 30 |
| c21_task_scheduler | 15 | 3 | 0 | 2 | 21 |
| c22_markdown_renderer | 23 | 11 | 2 | 0 | 36 |
| c23_merge_intervals | 4 | 1 | 0 | 0 | 6 |
| c24_topological_sort | 4 | 5 | 0 | 1 | 10 |
| c25_edit_distance | 1 | 1 | 0 | 0 | 2 |
| c26_trie | 4 | 3 | 0 | 0 | 8 |
| c27_min_heap | 0 | 1 | 0 | 0 | 1 |
| c28_linked_list | 3 | 5 | 0 | 0 | 8 |
| c29_parse_cron | 30 | 11 | 0 | 0 | 41 |
| c30_tokenize_sql | 23 | 11 | 1 | 1 | 37 |
| c31_glob_match | 7 | 3 | 1 | 1 | 12 |
| c32_sanitize_html | 28 | 11 | 11 | 0 | 50 |
| c33_escape_shell | 5 | 6 | 3 | 0 | 14 |
| c34_diff_objects | 17 | 10 | 1 | 1 | 30 |
| c35_throttle | 14 | 1 | 0 | 1 | 16 |
| c36_flatten_object | 9 | 13 | 0 | 1 | 23 |
| c37_topological_sort | 6 | 6 | 0 | 1 | 13 |
| c38_priority_queue | 4 | 1 | 0 | 2 | 7 |
| c39_observable | 13 | 4 | 0 | 1 | 18 |
| c40_parse_query_string | 6 | 8 | 0 | 1 | 15 |
| c41_json_stream | 19 | 10 | 0 | 0 | 30 |
| c42_mustache | 37 | 4 | 1 | 0 | 42 |
| c43_escape_regexp | 8 | 0 | 0 | 0 | 8 |
| c44_validate_email | 10 | 9 | 0 | 1 | 20 |
| c45_binary_heap | 1 | 0 | 0 | 1 | 2 |
| c46_memoize | 4 | 1 | 0 | 1 | 6 |
| c47_typed_event_emitter | 12 | 4 | 0 | 2 | 19 |
| c48_result_type | 38 | 0 | 0 | 1 | 39 |
| c49_parse_route | 11 | 12 | 1 | 0 | 24 |
| c50_parse_ini | 5 | 7 | 0 | 0 | 13 |
| c51_deep_merge | 21 | 7 | 0 | 1 | 29 |
| c52_retry_ts | 16 | 8 | 0 | 1 | 26 |

## Challenge Discrimination

Challenges ranked by how many models have issues (higher = more discriminating).

| Challenge | Models with Issues | Total Issues Across Models |
|-----------|-------------------|---------------------------|
| c9_url_parser | 10/11 | 50 |
| c32_sanitize_html | 10/11 | 50 |
| c5_deep_clone | 10/11 | 46 |
| c14_binary_search | 10/11 | 42 |
| c42_mustache | 10/11 | 42 |
| c29_parse_cron | 10/11 | 41 |
| c48_result_type | 10/11 | 39 |
| c30_tokenize_sql | 10/11 | 37 |
| c22_markdown_renderer | 10/11 | 36 |
| c2_palindrome | 10/11 | 35 |
| c6_csv_parser | 10/11 | 31 |
| c41_json_stream | 10/11 | 30 |
| c20_expression_parser | 10/11 | 30 |
| c34_diff_objects | 10/11 | 30 |
| c51_deep_merge | 10/11 | 29 |
| c52_retry_ts | 10/11 | 26 |
| c49_parse_route | 10/11 | 24 |
| c36_flatten_object | 10/11 | 23 |
| c16_html_entity_decoder | 10/11 | 21 |
| c21_task_scheduler | 10/11 | 21 |
| c44_validate_email | 10/11 | 20 |
| c47_typed_event_emitter | 10/11 | 19 |
| c39_observable | 10/11 | 18 |
| c12_flatten_array | 10/11 | 18 |
| c35_throttle | 10/11 | 16 |
| c33_escape_shell | 10/11 | 14 |
| c37_topological_sort | 10/11 | 13 |
| c43_escape_regexp | 10/11 | 8 |
| c19_ring_buffer | 9/11 | 16 |
| c40_parse_query_string | 9/11 | 15 |
| c1_fibonacci | 9/11 | 12 |
| c24_topological_sort | 9/11 | 10 |
| c7_retry | 9/11 | 10 |
| c23_merge_intervals | 9/11 | 6 |
| c50_parse_ini | 8/11 | 13 |
| c31_glob_match | 8/11 | 12 |
| c28_linked_list | 8/11 | 8 |
| c26_trie | 8/11 | 8 |
| c38_priority_queue | 8/11 | 7 |
| c10_debounce | 8/11 | 6 |
| c8_token_counter | 7/11 | 8 |
| c46_memoize | 7/11 | 6 |
| c17_concurrent_map | 6/11 | 8 |
| c15_rate_limiter | 6/11 | 4 |
| c11_lru_cache | 6/11 | 3 |
| c13_date_formatter | 5/11 | 6 |
| c3_word_frequency | 5/11 | 5 |
| c25_edit_distance | 4/11 | 2 |
| c45_binary_heap | 4/11 | 2 |
| c18_iterator | 3/11 | 3 |
| c27_min_heap | 2/11 | 1 |
| c4_array_dedup | 1/11 | 0 |

## Difficulty Tiers

Based on empirical failure rates across 11 models.

### Hard (34 challenges)

| Challenge | Models with Issues | Mean Issues |
|-----------|-------------------|-------------|
| c32_sanitize_html | 10/11 | 5.0 |
| c9_url_parser | 10/11 | 4.9 |
| c5_deep_clone | 10/11 | 4.5 |
| c42_mustache | 10/11 | 4.1 |
| c14_binary_search | 10/11 | 4.1 |
| c29_parse_cron | 10/11 | 4.0 |
| c48_result_type | 10/11 | 3.8 |
| c30_tokenize_sql | 10/11 | 3.6 |
| c22_markdown_renderer | 10/11 | 3.6 |
| c2_palindrome | 10/11 | 3.4 |
| c6_csv_parser | 10/11 | 3.1 |
| c41_json_stream | 10/11 | 2.9 |
| c34_diff_objects | 10/11 | 2.9 |
| c51_deep_merge | 10/11 | 2.9 |
| c20_expression_parser | 10/11 | 2.9 |
| c52_retry_ts | 10/11 | 2.6 |
| c49_parse_route | 10/11 | 2.3 |
| c36_flatten_object | 10/11 | 2.2 |
| c21_task_scheduler | 10/11 | 2.1 |
| c16_html_entity_decoder | 10/11 | 2.1 |
| c44_validate_email | 10/11 | 1.9 |
| c47_typed_event_emitter | 10/11 | 1.8 |
| c39_observable | 10/11 | 1.7 |
| c12_flatten_array | 10/11 | 1.7 |
| c35_throttle | 10/11 | 1.6 |
| c33_escape_shell | 10/11 | 1.3 |
| c37_topological_sort | 10/11 | 1.3 |
| c43_escape_regexp | 10/11 | 0.8 |
| c19_ring_buffer | 9/11 | 1.6 |
| c40_parse_query_string | 9/11 | 1.5 |
| c1_fibonacci | 9/11 | 1.2 |
| c24_topological_sort | 9/11 | 1.0 |
| c7_retry | 9/11 | 1.0 |
| c23_merge_intervals | 9/11 | 0.5 |

### Medium (13 challenges)

| Challenge | Models with Issues | Mean Issues |
|-----------|-------------------|-------------|
| c50_parse_ini | 8/11 | 1.3 |
| c31_glob_match | 8/11 | 1.2 |
| c28_linked_list | 8/11 | 0.8 |
| c26_trie | 8/11 | 0.8 |
| c38_priority_queue | 8/11 | 0.7 |
| c10_debounce | 8/11 | 0.6 |
| c8_token_counter | 7/11 | 0.8 |
| c46_memoize | 7/11 | 0.6 |
| c17_concurrent_map | 6/11 | 0.8 |
| c15_rate_limiter | 6/11 | 0.4 |
| c11_lru_cache | 6/11 | 0.3 |
| c13_date_formatter | 5/11 | 0.6 |
| c3_word_frequency | 5/11 | 0.5 |

### Easy (5 challenges)

| Challenge | Models with Issues | Mean Issues |
|-----------|-------------------|-------------|
| c45_binary_heap | 4/11 | 0.2 |
| c25_edit_distance | 4/11 | 0.2 |
| c18_iterator | 3/11 | 0.3 |
| c27_min_heap | 2/11 | 0.1 |
| c4_array_dedup | 1/11 | 0.0 |

**Distribution**: 34 hard, 13 medium, 5 easy, 0 trivial

## Cost-Effectiveness

| Model | Cost/Run | Cost/Issue | Issues/$ | Test Pass Rate |
|-------|---------|-----------|---------|---------------|
| gpt-4o-mini | $0.02 | $0.000 | 6241 | 92% |
| deepseek-v3.2 | $0.04 | $0.000 | 2384 | 96% |
| nemotron-3-super | $0.05 | $0.000 | 2171 | 91% |
| haiku-4.5 | $0.24 | $0.002 | 582 | 73% |
| gpt-4o | $0.29 | $0.003 | 385 | 94% |
| minimax-m2.5 | $0.22 | $0.004 | 231 | 84% |
| o3-mini | $0.49 | $0.006 | 163 | 97% |
| sonnet-4 | $0.60 | $0.007 | 144 | 98% |
| gemini-3.1-pro | $1.38 | $0.016 | 64 | 93% |
| opus-4 | $2.76 | $0.035 | 28 | 98% |
| kimi-k2.5 | $0.31 | $0.000 | 0 | - |

## Self-Catch Analysis

| Model | Self-Catch Rate | Issues Caught | Issues Missed |
|-------|----------------|---------------|---------------|
| kimi-k2.5 | 100% | - | - |
| opus-4 | 79% | 62 | 17 |
| sonnet-4 | 71% | 61 | 25 |
| deepseek-v3.2 | 67% | 69 | 33 |
| haiku-4.5 | 65% | 92 | 50 |
| nemotron-3-super | 52% | 60 | 55 |
| gpt-4o-mini | 50% | 61 | 62 |
| minimax-m2.5 | 43% | 22 | 29 |
| gemini-3.1-pro | 40% | 36 | 53 |
| o3-mini | 40% | 32 | 48 |
| gpt-4o | 27% | 30 | 81 |

## Self-Catch Rate by Issue Type

| Model | Correctness | Edge Case | Security | Style |
|-------|-------------|-----------|----------|-------|
| deepseek-v3.2 | 70% (198/281) | 65% (134/207) | 43% (3/7) | 60% (9/15) |
| gemini-3.1-pro | 41% (106/259) | 40% (37/92) | 0% (0/1) | 50% (1/2) |
| gpt-4o | 26% (81/313) | 28% (62/220) | 25% (2/8) | 23% (3/13) |
| gpt-4o-mini | 49% (195/402) | 51% (100/196) | 88% (7/8) | 25% (2/8) |
| haiku-4.5 | 68% (301/441) | 78% (80/102) | 59% (37/63) | 41% (43/106) |
| kimi-k2.5 | - | - | - | - |
| minimax-m2.5 | 38% (52/136) | 51% (55/108) | 33% (1/3) | 50% (4/8) |
| nemotron-3-super | 55% (210/382) | 48% (75/155) | 80% (12/15) | 23% (6/26) |
| o3-mini | 40% (63/159) | 41% (90/220) | 46% (6/13) | 22% (2/9) |
| opus-4 | 84% (147/176) | 76% (150/198) | 80% (8/10) | 56% (5/9) |
| sonnet-4 | 67% (149/222) | 77% (149/193) | 62% (5/8) | 44% (4/9) |

## Token Efficiency

| Model | Gen Tokens | Review Tokens | Total Tokens | Review Tokens/Issue |
|-------|-----------|--------------|-------------|-------------------|
| gpt-4o | 20,479 | 31,955 | 52,434 | 288 |
| gpt-4o-mini | 19,696 | 36,161 | 55,857 | 294 |
| deepseek-v3.2 | 24,666 | 41,143 | 65,809 | 403 |
| opus-4 | 26,662 | 40,902 | 67,564 | 520 |
| sonnet-4 | 27,882 | 43,755 | 71,637 | 506 |
| haiku-4.5 | 40,667 | 62,420 | 103,086 | 438 |
| o3-mini | 51,529 | 86,569 | 138,098 | 1079 |
| nemotron-3-super | 63,088 | 137,903 | 200,991 | 1193 |
| minimax-m2.5 | 131,518 | 96,276 | 227,794 | 1888 |
| gemini-3.1-pro | 138,088 | 160,334 | 298,422 | 1812 |
| kimi-k2.5 | 156,823 | 210,196 | 367,019 | - |

## Test Pass Rates

| Model | Tests Passed | Total Tests | Pass Rate |
|-------|-------------|-------------|-----------|
| opus-4 | 331 | 338 | 98% |
| sonnet-4 | 330 | 338 | 98% |
| o3-mini | 328 | 337 | 97% |
| deepseek-v3.2 | 316 | 329 | 96% |
| gpt-4o | 313 | 334 | 94% |
| gemini-3.1-pro | 262 | 282 | 93% |
| gpt-4o-mini | 310 | 338 | 92% |
| nemotron-3-super | 261 | 288 | 91% |
| minimax-m2.5 | 250 | 296 | 84% |
| haiku-4.5 | 188 | 257 | 73% |

## Fix Effectiveness

| Model | Original Pass Rate | Fixed Pass Rate | Improvement | Regressions |
|-------|--------------------|-----------------|-------------|-------------|
| haiku-4.5 | 73% | 95% | +99.0 | -4.0 |
| minimax-m2.5 | 84% | 94% | +27.4 | -9.0 |
| opus-4 | 98% | 98% | +3.0 | -2.2 |
| gpt-4o | 94% | 94% | +3.4 | -8.4 |
| o3-mini | 97% | 97% | +3.2 | -3.0 |
| gpt-4o-mini | 92% | 91% | +8.0 | -12.4 |
| sonnet-4 | 98% | 97% | +2.8 | -7.0 |
| deepseek-v3.2 | 96% | 94% | +6.5 | -14.2 |
| gemini-3.1-pro | 93% | 90% | +29.0 | -40.2 |
| nemotron-3-super | 91% | 81% | +23.6 | -46.4 |

## Score History

Models with runs on multiple dates, showing key metrics per date.

### deepseek-v3.2

| Date | Issues | Self-Catch | Test Pass | First-Try Pass |
|------|--------|------------|-----------|---------------|
| 2026-03-22 | 23 | 70% | - | - |
| 2026-03-23 | 26 | 38% | 98% | 83% |
| 2026-03-25 | 102 | 67% | 96% | 84% |

### gemini-3.1-pro

| Date | Issues | Self-Catch | Test Pass | First-Try Pass |
|------|--------|------------|-----------|---------------|
| 2026-03-22 | 20 | 40% | - | - |
| 2026-03-23 | 24 | 62% | 86% | 40% |
| 2026-03-26 | 102 | 47% | 97% | 82% |
| 2026-03-27 | 81 | 39% | 90% | 78% |
| 2026-03-28 | 90 | 37% | 95% | 80% |

### glm-5

| Date | Issues | Self-Catch | Test Pass | First-Try Pass |
|------|--------|------------|-----------|---------------|
| 2026-03-22 | 20 | 65% | - | - |
| 2026-03-23 | 10 | 40% | 40% | 33% |

### gpt-4o

| Date | Issues | Self-Catch | Test Pass | First-Try Pass |
|------|--------|------------|-----------|---------------|
| 2026-03-21 | 10 | 40% | - | - |
| 2026-03-23 | 28 | 36% | 97% | 67% |
| 2026-03-25 | 111 | 27% | 94% | 79% |

### gpt-4o-mini

| Date | Issues | Self-Catch | Test Pass | First-Try Pass |
|------|--------|------------|-----------|---------------|
| 2026-03-21 | 12 | 50% | - | - |
| 2026-03-23 | 30 | 40% | 87% | 67% |
| 2026-03-25 | 123 | 50% | 92% | 73% |

### haiku-4.5

| Date | Issues | Self-Catch | Test Pass | First-Try Pass |
|------|--------|------------|-----------|---------------|
| 2026-03-21 | 12 | 92% | - | - |
| 2026-03-23 | 28 | 68% | 68% | 50% |
| 2026-03-25 | 142 | 65% | 73% | 55% |

### kimi-k2.5

| Date | Issues | Self-Catch | Test Pass | First-Try Pass |
|------|--------|------------|-----------|---------------|
| 2026-03-22 | 15 | 33% | - | - |
| 2026-03-23 | 5 | 40% | 25% | 33% |
| 2026-03-29 | 0 | - | - | - |

### minimax-m2.5

| Date | Issues | Self-Catch | Test Pass | First-Try Pass |
|------|--------|------------|-----------|---------------|
| 2026-03-22 | 15 | 53% | - | - |
| 2026-03-23 | 11 | 55% | 72% | 75% |
| 2026-03-26 | 46 | 35% | 81% | 77% |
| 2026-03-27 | 44 | 45% | 85% | 79% |
| 2026-03-28 | 76 | 46% | 86% | 84% |

### nemotron-3-super

| Date | Issues | Self-Catch | Test Pass | First-Try Pass |
|------|--------|------------|-----------|---------------|
| 2026-03-25 | 40 | 42% | 96% | 83% |
| 2026-03-26 | 109 | 51% | 93% | 74% |
| 2026-03-27 | 126 | 54% | 88% | 61% |

### o3-mini

| Date | Issues | Self-Catch | Test Pass | First-Try Pass |
|------|--------|------------|-----------|---------------|
| 2026-03-21 | 12 | 92% | - | - |
| 2026-03-23 | 18 | 61% | 100% | 100% |
| 2026-03-25 | 80 | 40% | 97% | 88% |
| 2026-03-26 | 82 | 40% | 98% | 90% |

### opus-4

| Date | Issues | Self-Catch | Test Pass | First-Try Pass |
|------|--------|------------|-----------|---------------|
| 2026-03-21 | 11 | 91% | - | - |
| 2026-03-23 | 19 | 53% | - | - |
| 2026-03-25 | 80 | 80% | 98% | 88% |
| 2026-03-26 | 72 | 74% | 98% | 88% |

### qwen-3.5-plus

| Date | Issues | Self-Catch | Test Pass | First-Try Pass |
|------|--------|------------|-----------|---------------|
| 2026-03-22 | 17 | 47% | - | - |
| 2026-03-23 | 17 | 6% | 95% | 67% |

### sonnet-4

| Date | Issues | Self-Catch | Test Pass | First-Try Pass |
|------|--------|------------|-----------|---------------|
| 2026-03-21 | 12 | 83% | - | - |
| 2026-03-23 | 18 | 61% | 100% | 100% |
| 2026-03-25 | 86 | 71% | 98% | 90% |

## Key Findings

- **Fewest issues**: kimi-k2.5 (0 issues)
- **Most issues**: haiku-4.5 (142 issues)
- **Best self-catch rate**: opus-4 (79%)
- **Worst self-catch rate**: gpt-4o (27%)
