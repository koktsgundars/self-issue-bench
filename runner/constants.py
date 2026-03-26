"""Shared constants for the self-issue benchmark."""

from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
CHALLENGES_DIR = PROJECT_DIR / "challenges"
RESULTS_DIR = PROJECT_DIR / "results"

CHALLENGE_IDS = [
    "c1_fibonacci",
    "c2_palindrome",
    "c3_word_frequency",
    "c4_array_dedup",
    "c5_deep_clone",
    "c6_csv_parser",
    "c7_retry",
    "c8_token_counter",
    "c9_url_parser",
    "c10_debounce",
    "c11_lru_cache",
    "c12_flatten_array",
    "c13_date_formatter",
    "c14_binary_search",
    "c15_rate_limiter",
    "c16_html_entity_decoder",
    "c17_concurrent_map",
    "c18_iterator",
    "c19_ring_buffer",
    "c20_expression_parser",
    "c21_task_scheduler",
    "c22_markdown_renderer",
    # Expansion set (added 2026-03-25)
    "c23_merge_intervals",
    "c24_topological_sort",
    "c25_edit_distance",
    "c26_trie",
    "c27_min_heap",
    "c28_linked_list",
    "c29_parse_cron",
    "c30_tokenize_sql",
    "c31_glob_match",
    "c32_sanitize_html",
    "c33_escape_shell",
    "c34_diff_objects",
    "c35_throttle",
    "c36_flatten_object",
    "c37_topological_sort",
    "c38_priority_queue",
    "c39_observable",
    "c40_parse_query_string",
    "c41_json_stream",
    "c42_mustache",
    "c43_escape_regexp",
    "c44_validate_email",
    "c45_binary_heap",
    "c46_memoize",
    "c47_typed_event_emitter",
    "c48_result_type",
    "c49_parse_route",
    "c50_parse_ini",
    "c51_deep_merge",
    "c52_retry_ts",
]

# Each challenge prompt file is {id}.md
CHALLENGE_PROMPT_FILES = {cid: f"{cid}.md" for cid in CHALLENGE_IDS}

# Ordered lists for display
CATEGORIES = ["correctness", "edge_case", "security", "style"]
SEVERITIES = ["high", "medium", "low"]

# Sets for validation
ISSUE_TYPES = set(CATEGORIES)
ISSUE_SEVERITIES = set(SEVERITIES)

# Severity weights for weighted scoring
SEVERITY_WEIGHTS = {"high": 3, "medium": 2, "low": 1}

# Aliases that map to canonical type names
_TYPE_ALIASES = {
    "safety": "security",
    "security_safety": "security",
    "smell": "style",
    "style_smell": "style",
}


# Language for each challenge (used by test runner)
CHALLENGE_LANG = {
    "c1_fibonacci": "python",
    "c2_palindrome": "python",
    "c3_word_frequency": "python",
    "c4_array_dedup": "javascript",
    "c5_deep_clone": "javascript",
    "c6_csv_parser": "python",
    "c7_retry": "python",
    "c8_token_counter": "javascript",
    "c9_url_parser": "python",
    "c10_debounce": "javascript",
    "c11_lru_cache": "python",
    "c12_flatten_array": "javascript",
    "c13_date_formatter": "python",
    "c14_binary_search": "typescript",
    "c15_rate_limiter": "python",
    "c16_html_entity_decoder": "javascript",
    "c17_concurrent_map": "go",
    "c18_iterator": "go",
    "c19_ring_buffer": "rust",
    "c20_expression_parser": "rust",
    "c21_task_scheduler": "python",
    "c22_markdown_renderer": "typescript",
    # Expansion set
    "c23_merge_intervals": "python",
    "c24_topological_sort": "python",
    "c25_edit_distance": "python",
    "c26_trie": "python",
    "c27_min_heap": "python",
    "c28_linked_list": "python",
    "c29_parse_cron": "python",
    "c30_tokenize_sql": "python",
    "c31_glob_match": "python",
    "c32_sanitize_html": "python",
    "c33_escape_shell": "python",
    "c34_diff_objects": "python",
    "c35_throttle": "javascript",
    "c36_flatten_object": "javascript",
    "c37_topological_sort": "javascript",
    "c38_priority_queue": "javascript",
    "c39_observable": "javascript",
    "c40_parse_query_string": "javascript",
    "c41_json_stream": "javascript",
    "c42_mustache": "javascript",
    "c43_escape_regexp": "javascript",
    "c44_validate_email": "javascript",
    "c45_binary_heap": "typescript",
    "c46_memoize": "typescript",
    "c47_typed_event_emitter": "typescript",
    "c48_result_type": "typescript",
    "c49_parse_route": "typescript",
    "c50_parse_ini": "typescript",
    "c51_deep_merge": "typescript",
    "c52_retry_ts": "typescript",
}

CHALLENGE_TESTS_DIR = PROJECT_DIR / "challenge_tests"
FIX_PROMPT_FILE = CHALLENGES_DIR / "fix_prompt.md"


def normalize_issue_type(raw: str) -> str | None:
    """Normalize issue type string to canonical form, or None if unrecognized."""
    import re
    itype = re.sub(r"[\s/]+", "_", raw.lower().strip()).strip("_")
    itype = _TYPE_ALIASES.get(itype, itype)
    return itype if itype in ISSUE_TYPES else None
