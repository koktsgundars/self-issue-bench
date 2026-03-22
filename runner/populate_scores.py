#!/usr/bin/env python3
"""
One-time script to populate issues into results.yaml files based on
independent review by Claude Opus 4.6.

Run: python runner/populate_scores.py
"""

from pathlib import Path

import yaml

RESULTS_DIR = Path(__file__).parent.parent / "results"


# Issue format: (type, severity, description, self_caught)
# self_caught = True if the model flagged it in pass 1 or pass 2

SCORES = {
    "sonnet-4-strict-2pass_2026-03-21": {
        "c1_fibonacci": [],
        "c2_palindrome": [],
        "c3_word_frequency": [
            ("edge_case", "medium", "Regex [a-zA-Z]+ splits apostrophe words incorrectly (don't -> don, t)", True),
        ],
        "c4_array_dedup": [],
        "c5_deep_clone": [
            ("edge_case", "medium", "No circular reference handling — causes stack overflow", True),
            ("correctness", "low", "Prototype chain not preserved on cloned objects", True),
            ("edge_case", "low", "Symbol keys are ignored (for...in only iterates string keys)", True),
        ],
        "c6_csv_parser": [
            ("correctness", "high", "Quote detection checks startswith('\"') on accumulated field instead of tracking quoted state", True),
            ("edge_case", "medium", "Trailing comma does not produce an empty final field", True),
            ("edge_case", "medium", "Escaped quotes within quoted fields not handled correctly", True),
        ],
        "c7_retry": [],
        "c8_token_counter": [],
    },
    "opus-4_2026-03-21": {
        "c1_fibonacci": [],
        "c2_palindrome": [],
        "c3_word_frequency": [
            ("edge_case", "medium", "Stripping all punctuation turns contractions like don't into dont", True),
            ("edge_case", "low", "Hyphenated words like well-known become wellknown", True),
        ],
        "c4_array_dedup": [],
        "c5_deep_clone": [
            ("edge_case", "medium", "No circular reference handling — causes stack overflow", True),
        ],
        "c6_csv_parser": [
            ("correctness", "high", "Escaped quotes (\"\") inside quoted fields not handled — toggles state instead of producing literal quote", True),
            ("correctness", "medium", "Whitespace stripping logic based on startswith('\"') check that never triggers after quote consumption", True),
        ],
        "c7_retry": [],
        "c8_token_counter": [],
    },
    "haiku-4.5_2026-03-21": {
        "c1_fibonacci": [],
        "c2_palindrome": [],
        "c3_word_frequency": [
            ("edge_case", "medium", "Regex [a-z]+ excludes words with apostrophes, hyphens, and digits", True),
            ("edge_case", "medium", "Regex ignores all non-ASCII/Unicode characters", True),
        ],
        "c4_array_dedup": [],
        "c5_deep_clone": [
            ("edge_case", "medium", "No circular reference handling — causes stack overflow", True),
            ("correctness", "low", "Prototype chain not preserved on cloned objects", True),
        ],
        "c6_csv_parser": [
            ("correctness", "high", "Uses Anthropic API call to parse CSV — non-deterministic, data leakage, unnecessary dependency", True),
            ("security", "high", "Sends CSV data to external API — data exfiltration risk", True),
            ("correctness", "medium", "LLM responses are not guaranteed to be valid JSON", True),
        ],
        "c7_retry": [],
        "c8_token_counter": [],
    },
    "gpt-4o-mini_2026-03-21": {
        "c1_fibonacci": [],
        "c2_palindrome": [],
        "c3_word_frequency": [],
        "c4_array_dedup": [],
        "c5_deep_clone": [
            ("edge_case", "medium", "No circular reference handling — causes stack overflow", True),
            ("edge_case", "medium", "No Date/RegExp/Set/Map support — cloned as plain objects", True),
            ("correctness", "low", "Prototype chain not preserved on cloned objects", False),
        ],
        "c6_csv_parser": [
            ("correctness", "high", "Double-processing: csv.reader already strips quotes but post-processing re-checks for leading quote", False),
            ("correctness", "medium", "Whitespace stripping applied to all fields regardless of quoted state", True),
        ],
        "c7_retry": [
            ("edge_case", "medium", "retries=0 means fn() is never called (range(0) is empty)", True),
            ("style", "low", "Uses raise e instead of bare raise — loses original traceback", False),
        ],
        "c8_token_counter": [
            ("correctness", "medium", "Unescaped [ and ] inside regex character class — may cause unexpected matching", False),
        ],
    },
    "gpt-4o_2026-03-21": {
        "c1_fibonacci": [],
        "c2_palindrome": [],
        "c3_word_frequency": [],
        "c4_array_dedup": [
            ("style", "medium", "O(n^2) performance — indexOf inside filter instead of Set-based O(n)", False),
            ("edge_case", "medium", "NaN values are never found by indexOf (NaN !== NaN) so every NaN kept as unique", False),
        ],
        "c5_deep_clone": [
            ("edge_case", "medium", "No circular reference handling — causes stack overflow", True),
            ("edge_case", "medium", "No Date/RegExp/Set/Map support — cloned as plain objects", True),
        ],
        "c6_csv_parser": [
            ("edge_case", "medium", "Input with newlines causes csv.reader to iterate multiple rows, flattened into one list", False),
        ],
        "c7_retry": [
            ("correctness", "low", "Sleeps after the last failed attempt before raising — unnecessary delay", False),
        ],
        "c8_token_counter": [],
    },
    "o3-mini_2026-03-21": {
        "c1_fibonacci": [],
        "c2_palindrome": [],
        "c3_word_frequency": [
            ("edge_case", "medium", "Contractions like don't split into don and t due to \\w+ pattern", True),
            ("edge_case", "low", "Hyphenated words split into separate words", True),
        ],
        "c4_array_dedup": [],
        "c5_deep_clone": [
            ("correctness", "high", "Functions cloned as non-callable plain objects instead of returned by reference", True),
            ("edge_case", "medium", "Date/RegExp not registered in WeakMap — circular refs involving them cause infinite recursion", False),
        ],
        "c6_csv_parser": [
            ("edge_case", "high", "Missing closing quote silently accepted — malformed input not detected", True),
            ("edge_case", "medium", "Non-whitespace after closing quote silently ignored", True),
        ],
        "c7_retry": [
            ("correctness", "high", "retries=0 causes raise None which throws TypeError", True),
            ("style", "low", "Uses raise last_exception instead of bare raise — loses original traceback", True),
        ],
        "c8_token_counter": [],
        "c9_url_parser": [
            ("edge_case", "medium", "No IPv6 bracket handling", True),
            ("edge_case", "low", "Duplicate query keys silently overwritten", True),
            ("edge_case", "low", "No percent-decoding of query/path values", True),
        ],
        "c10_debounce": [],
        "c11_lru_cache": [],
        "c12_flatten_array": [],
        "c13_date_formatter": [],
        "c14_binary_search": [],
        "c15_rate_limiter": [],
        "c16_html_entity_decoder": [
            ("correctness", "medium", "fromCharCode fails for code points > U+FFFF — should use fromCodePoint", True),
        ],
    },
}

# C9-C16 scores for existing models
C9_C16_SCORES = {
    "opus-4_2026-03-21": {
        "c9_url_parser": [
            ("edge_case", "medium", "IPv6 with colons breaks host:port parsing", True),
            ("edge_case", "low", "No URL-decoding of query/fragment values", True),
            ("edge_case", "low", "No userinfo (user:pass@) handling", True),
        ],
        "c10_debounce": [],
        "c11_lru_cache": [
            ("correctness", "high", "Uses list.remove() making get/put O(n) instead of required O(1)", True),
        ],
        "c12_flatten_array": [],
        "c13_date_formatter": [],
        "c14_binary_search": [],
        "c15_rate_limiter": [
            ("edge_case", "low", "Not thread-safe", True),
        ],
        "c16_html_entity_decoder": [
            ("correctness", "medium", "fromCharCode fails for code points > U+FFFF — should use fromCodePoint", False),
        ],
    },
    "sonnet-4-strict-2pass_2026-03-21": {
        "c9_url_parser": [
            ("edge_case", "medium", "IPv6 with port still breaks bracket parsing", True),
            ("edge_case", "low", "No URL-decoding of query/path values", False),
        ],
        "c10_debounce": [],
        "c11_lru_cache": [
            ("edge_case", "low", "capacity=0 edge case not handled (> vs >=)", True),
        ],
        "c12_flatten_array": [],
        "c13_date_formatter": [],
        "c14_binary_search": [],
        "c15_rate_limiter": [
            ("edge_case", "low", "Not thread-safe", False),
        ],
        "c16_html_entity_decoder": [
            ("correctness", "medium", "fromCharCode fails for code points > U+FFFF — should use fromCodePoint", True),
        ],
    },
    "haiku-4.5_2026-03-21": {
        "c9_url_parser": [
            ("correctness", "medium", "Path defaults to / even when absent", True),
            ("edge_case", "medium", "No IPv6 support", True),
            ("edge_case", "low", "No URL-decoding", False),
        ],
        "c10_debounce": [],
        "c11_lru_cache": [],
        "c12_flatten_array": [],
        "c13_date_formatter": [
            ("correctness", "high", "Calls Anthropic API to format a date — bizarre dependency, dead code", True),
        ],
        "c14_binary_search": [],
        "c15_rate_limiter": [],
        "c16_html_entity_decoder": [
            ("correctness", "medium", "fromCharCode fails for code points > U+FFFF — should use fromCodePoint", True),
        ],
    },
    "gpt-4o_2026-03-21": {
        "c9_url_parser": [
            ("correctness", "high", "Query params in normal URLs silently dropped into path due to split ordering", False),
            ("edge_case", "medium", "No IPv6 support", True),
            ("edge_case", "low", "Path defaults to / even when absent", True),
        ],
        "c10_debounce": [],
        "c11_lru_cache": [],
        "c12_flatten_array": [],
        "c13_date_formatter": [],
        "c14_binary_search": [],
        "c15_rate_limiter": [],
        "c16_html_entity_decoder": [
            ("correctness", "medium", "fromCharCode fails for code points > U+FFFF — should use fromCodePoint", False),
        ],
    },
    "gpt-4o-mini_2026-03-21": {
        "c9_url_parser": [
            ("edge_case", "medium", "Duplicate query keys silently overwritten", True),
            ("edge_case", "low", "No percent-decoding of query values", True),
            ("edge_case", "low", "No userinfo handling", False),
        ],
        "c10_debounce": [],
        "c11_lru_cache": [],
        "c12_flatten_array": [],
        "c13_date_formatter": [],
        "c14_binary_search": [],
        "c15_rate_limiter": [],
        "c16_html_entity_decoder": [
            ("correctness", "medium", "fromCharCode fails for code points > U+FFFF — should use fromCodePoint", False),
        ],
    },
    "o3-mini_2026-03-21": {
        # Already included in main SCORES dict above
    },
}

# Merge C9-C16 into SCORES
for run_name, challenges in C9_C16_SCORES.items():
    if run_name not in SCORES:
        SCORES[run_name] = {}
    SCORES[run_name].update(challenges)


def main():
    for run_name, challenges in SCORES.items():
        results_path = RESULTS_DIR / run_name / "results.yaml"
        if not results_path.exists():
            print(f"SKIP: {results_path} not found")
            continue

        with open(results_path) as f:
            data = yaml.safe_load(f)

        for cid, issues in challenges.items():
            if cid not in data.get("challenges", {}):
                print(f"WARN: {cid} not in {run_name}")
                continue

            data["challenges"][cid]["issues"] = [
                {
                    "type": itype,
                    "severity": severity,
                    "description": desc,
                    "self_caught": self_caught,
                }
                for itype, severity, desc, self_caught in issues
            ]

        with open(results_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

        total = sum(len(issues) for issues in challenges.values())
        caught = sum(
            1 for issues in challenges.values()
            for _, _, _, sc in issues if sc
        )
        print(f"OK: {run_name} — {total} issues, {caught} self-caught")


if __name__ == "__main__":
    main()
