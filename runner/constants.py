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
]

# Each challenge prompt file is {id}.md
CHALLENGE_PROMPT_FILES = {cid: f"{cid}.md" for cid in CHALLENGE_IDS}

# Ordered lists for display
CATEGORIES = ["correctness", "edge_case", "security", "style"]
SEVERITIES = ["high", "medium", "low"]

# Sets for validation
ISSUE_TYPES = set(CATEGORIES)
ISSUE_SEVERITIES = set(SEVERITIES)

# Aliases that map to canonical type names
_TYPE_ALIASES = {
    "safety": "security",
    "security_safety": "security",
    "smell": "style",
    "style_smell": "style",
}


def normalize_issue_type(raw: str) -> str | None:
    """Normalize issue type string to canonical form, or None if unrecognized."""
    import re
    itype = re.sub(r"[\s/]+", "_", raw.lower().strip()).strip("_")
    itype = _TYPE_ALIASES.get(itype, itype)
    return itype if itype in ISSUE_TYPES else None
