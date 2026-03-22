from constants import (
    CATEGORIES,
    CHALLENGE_IDS,
    CHALLENGE_PROMPT_FILES,
    CHALLENGES_DIR,
    ISSUE_SEVERITIES,
    ISSUE_TYPES,
    SEVERITIES,
    normalize_issue_type,
)


def test_issue_types_match_categories():
    assert ISSUE_TYPES == set(CATEGORIES)


def test_issue_severities_match_severities():
    assert ISSUE_SEVERITIES == set(SEVERITIES)


def test_challenge_prompt_files_match_ids():
    assert set(CHALLENGE_PROMPT_FILES.keys()) == set(CHALLENGE_IDS)
    for cid, filename in CHALLENGE_PROMPT_FILES.items():
        assert filename == f"{cid}.md"


def test_challenge_prompt_files_exist():
    for cid, filename in CHALLENGE_PROMPT_FILES.items():
        path = CHALLENGES_DIR / filename
        assert path.exists(), f"Missing prompt file: {path}"


def test_normalize_known_types():
    assert normalize_issue_type("correctness") == "correctness"
    assert normalize_issue_type("edge_case") == "edge_case"
    assert normalize_issue_type("security") == "security"
    assert normalize_issue_type("style") == "style"


def test_normalize_aliases():
    assert normalize_issue_type("Edge Case") == "edge_case"
    assert normalize_issue_type("safety") == "security"
    assert normalize_issue_type("security/safety") == "security"
    assert normalize_issue_type("smell") == "style"
    assert normalize_issue_type("Style / Smell") == "style"


def test_normalize_unknown_returns_none():
    assert normalize_issue_type("") is None
    assert normalize_issue_type("performance") is None
    assert normalize_issue_type("typo") is None
