# Coding Assistant Self-Issue Benchmark

**How many bugs does the assistant inject into trivial code?**

v1.0 | March 2026

## Purpose

This benchmark measures how many issues a coding assistant introduces into its
own output when given clean, simple, unambiguous coding challenges. No issues
are pre-injected. The only bugs present are ones the assistant created.

This is explicitly **not** a test of:
- How well the assistant reviews externally-authored code
- How it handles complex or ambiguous requirements
- PR-level or cross-file reasoning

It **is** a test of: given a trivial, well-specified task, how clean is the output?

## Protocol

### Step 1 — Generate

For each challenge, paste only the prompt text into the assistant with no
additional context. No system prompt. No CLAUDE.md. No prior conversation.
Fresh session.

Each prompt includes the constraint: "Return only a single implementation as a
plain code block. No alternatives, no examples, no explanation." This ensures
we measure single-shot codegen quality, not the model's ability to hedge with
multiple implementations.

Record the generated code verbatim.

### Step 2 — Review

After the code is generated, send the following review prompt in the same session:

> Review the code you just wrote. For each issue you find, output:
> - Issue type: [correctness | edge case | security | style]
> - Severity: [high | medium | low]
> - Description: one sentence
> - Line(s): if applicable
>
> Be critical. Do not defend the code. If there are no issues, say so explicitly.

This prompt is intentionally minimal. The point is to test what the assistant
surfaces with a low-friction ask, not what it surfaces under adversarial pressure.

### Step 3 — Verify (independent review)

Independently review the generated code using a different reviewer — either a
human or a different model. The key requirement is that the reviewer is not the
same model that generated the code and performed the self-review. This ensures
the issue count reflects ground truth, not just what the model under test is
willing to flag about its own output.

In our runs, independent review is performed by Claude Opus 4.6 reviewing the
generated code and self-reviews from all models (including other Claude models).

Add any issues the independent reviewer finds to the score. Mark missed issues
(ones the model did not catch in its self-review) in the notes column.

### Step 4 — Score

Log each issue in the scorecard by type. Count only distinct issues — if the
assistant flags the same issue twice, count it once.

## Scoring rubric

### Issue categories

| Category | Definition | Examples |
|----------|-----------|----------|
| Correctness | Code that produces wrong output on valid inputs | Off-by-one, wrong algorithm, broken base case, logic inversion |
| Edge case | Code that fails on valid but non-obvious inputs | Empty input, None/null, zero, negative numbers, Unicode, very large values |
| Security / safety | Code that introduces a vulnerability or unsafe pattern | SQL injection, unhashed credentials, arbitrary code execution, resource leak |
| Style / smell | Code that works but is unnecessarily fragile, obscure, or unmaintainable | Magic numbers, mutable defaults, shadowed variables, no type hints on public API |

### Severity

- **High** — incorrect output on common inputs, or a serious security vulnerability
- **Medium** — fails on plausible but non-obvious inputs
- **Low** — style issues, minor fragility, suboptimal but not wrong

### Self-catch rate

For each issue found, note whether the assistant caught it in the review step or
whether it was identified independently.

**Self-catch rate = issues flagged by assistant / total issues found**

## Interpreting results

| Total issues | Signal | Implication |
|-------------|--------|-------------|
| 0–2 | Excellent output quality on trivial tasks | Model is reliable for simple work with no review |
| 3–8 | Expected baseline for current models | Review pass adds meaningful value even on simple code |
| 9–16 | Notable self-issue rate | Default output needs systematic review |
| 17+ | High self-issue rate | Review agent or second-pass architecture is not optional |

The self-catch rate is in some ways more interesting than the raw issue count. A
model that introduces 6 issues and catches 5 of them on a simple review prompt
is a very different story from one that introduces 6 and catches 1.
