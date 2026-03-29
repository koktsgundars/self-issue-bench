# Inter-Reviewer Validation Report

Reviewer 1: claude-opus-4-20250514
Reviewer 2: gpt-4o
Runs analyzed: 10

## Per-Run Agreement

| Run | Challenges | R1 Issues | R2 Issues | Mean Δ | Correlation | Binary Agree | Kappa |
|-----|-----------|-----------|-----------|--------|-------------|-------------|-------|
| deepseek-v3.2_run1_2026-03-25 | 52 | 1.7 | 1.4 | 1.1 | 0.69 | 71% | 0.43 |
| gemini-3.1-pro_run1_2026-03-27 | 52 | 1.7 | 1.4 | 1.0 | 0.71 | 79% | 0.58 |
| gpt-4o-mini_run1_2026-03-25 | 52 | 2.5 | 1.7 | 1.2 | 0.73 | 73% | 0.45 |
| gpt-4o_run1_2026-03-25 | 52 | 2.2 | 1.5 | 1.1 | 0.78 | 71% | 0.40 |
| haiku-4.5_run1_2026-03-25 | 52 | 3.1 | 1.8 | 2.0 | 0.53 | 71% | 0.33 |
| minimax-m2.5_run1_2026-03-26 | 52 | 0.9 | 0.5 | 0.8 | 0.40 | 63% | 0.22 |
| nemotron-3-super_run1_2026-03-26 | 52 | 2.0 | 1.2 | 1.3 | 0.54 | 75% | 0.50 |
| o3-mini_run1_2026-03-25 | 52 | 1.5 | 1.0 | 1.2 | 0.53 | 65% | 0.33 |
| opus-4_run1_2026-03-25 | 52 | 1.5 | 1.6 | 1.0 | 0.64 | 69% | 0.36 |
| sonnet-4_run1_2026-03-25 | 52 | 1.7 | 1.6 | 1.3 | 0.65 | 71% | 0.41 |

## Summary

- **Mean issues (R1)**: 1.9
- **Mean issues (R2)**: 1.4
- **Issue count correlation**: 0.62
- **Binary agreement**: 71%
- **Cohen's kappa**: 0.40

**Interpretation**: Moderate agreement — some subjectivity in scoring; results should be interpreted with caution.

## Issue Type Distribution

| Type | R1 Total | R2 Total |
|------|----------|----------|
| correctness | 550 | 579 |
| edge_case | 353 | 98 |
| security | 29 | 16 |
| style | 38 | 21 |
