---
description: End‑to‑end guarded patch loop with RCA, plan approval, regression shields, and token discipline.
---

# /workflow run

**Usage:** `/workflow run <task>` where `<task>` is a single concise sentence.

When invoked, do the following:

1) Read `context/*.md` and repo docs to initialize working memory.
2) Align: restate goal, constraints, success criteria.
3) RCA: identify the root cause or governing constraint.
4) Plan: list files to edit, minimal changes, tests to run, rollback plan.
5) Regression shield: identify adjacent risk areas and add checks.
6) Scope check: ensure plan aligns with project architecture and guardrails.
7) Execute: apply edits as full files. Keep changes cohesive and small.
8) Deploy repository to live enviornment.
9)  Run all tests; capture outputs in `context/test-log.md`.
10) Summarize results. Do not mark fixed until user verifies in the live environment.

**Token discipline**
- Use `/usage` to monitor spend; if context > ~70%, run `/compact` and move verbose content to `context/`.
- Prefer code over prose; keep responses minimal.

