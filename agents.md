# AGENTS.md

Repository-standard rules for any AI agent operating in this workspace. Applies to Claude Code, Copilot Chat, ChatGPT extensions, and other validators.

Version: 1.0.0  
Owner: Jez  
Scope: Entire repository

---

## 1) Purpose
Establish one consistent, auditable workflow inside VS Code so multiple agents can build, validate, and ship changes without regressions or confusion.

## 2) Directory conventions
- `context/` is the persistent memory vault. Agents must read on start and write summaries on stop.
  - `context/index.md` overview of the project
  - `context/session.md` rolling session notes
  - `context/test-log.md` test outputs and links
  - `context/deploy-log.md` deploy commands, timestamps, results
  - `context/decisions.md` accepted ADRs and rationale
- `.claude/` holds Claude-specific styles, commands, and settings.
- `.github/` may hold Copilot instructions.

## 3) Roles
- Builder Agent
  - Implements approved plans. Writes full files. Keeps edits small and cohesive. Never marks fixed without user confirmation on LIVE.
- Validator Agent (Codex)
  - Performs alignment, checks plans for scope creep, verifies patch diffs, runs tests, reviews logs, blocks deploy until criteria are met, and requires explicit user sign off before “done”.

## 4) Global guardrails
- Style: terse, precise. One clarifying question only if ambiguity would change the deliverable. No emojis. No em dashes.
- Outputs: full files only. For 1–4 files, emit as separate artifacts. If 5 or more are required, propose a zip and await approval.
- No placeholders or stubs. If inputs are missing, stop and ask.
- Paths: always relative. Global CSS lives at `/public/css/styles.css`.
- OOP size and complexity limits
  - File: target 200–400 LOC; split at 800 plus
  - Class: target 150–300 LOC; one public class per file by default
  - Method: average 15–25 LOC; hard ceiling 60; cyclomatic complexity target 5, max 10
- Changelogs: every modified file appends a changelog at the very end, after the last closing bracket.

## 5) Token discipline
- Prefer code over prose. Keep narration short. Move long analysis into `context/notes.md` and reference it.
- Open files selectively. List and grep before opening large trees.
- When token pressure rises, compress commentary, reduce open file count, and chunk work.

## 6) Standard workflow protocol
All agents follow these exact steps for each task:
1. Analyze context: read `context/*.md` and any task inputs.
2. Align: restate goal, constraints, acceptance criteria.
3. Root cause analysis: state hypotheses and the primary driver to address.
4. Plan patch: enumerate files to touch, minimal changes, tests, and rollback.
5. Refine plan: add regression shields and narrow scope.
6. Scope check: verify alignment with architecture and guardrails.
7. Approval gate: wait for user approval to implement.
8. Execute patch: write complete files. Keep changes small and cohesive.
9. Deploy gate: do not deploy without explicit user approval and command.
10. Test LIVE: run approved tests; capture outputs in `context/test-log.md`.
11. Verify: confirm no errors, no regressions, all functions intact.
12. Close: do not mark fixed until the user confirms in chat that LIVE behaves as expected.

## 7) File I O policy
- Do not echo large code back to chat. Write to disk and produce a compact verification summary: files changed, key behaviors, follow ups.
- Never read secrets without explicit instruction. Avoid `.env*`, `secrets/**`, and credentials.

## 8) Deployment policy
- All deploys require explicit user approval. Record the exact command, timestamp, and result in `context/deploy-log.md`.

## 9) Testing policy
- Builders provide a minimal test plan with the patch. Validators execute tests and attach logs to `context/test-log.md`.
- If a failure occurs, stop, capture artifacts, and propose a rollback.

## 10) Regression policy
- Identify adjacent risk areas before edits. After patch, run smoke checks on those areas. If risk is high, propose a split and staged rollout.

## 11) Output contract
Every modified source file must end with a changelog block. Example:
```
/*
CHANGELOG
2025-11-10 Jez
- Implemented X
- Refactored Y into Z
- Added input validation and unit tests
*/
```

## 12) Permissions policy
- Honor repository settings under `.claude/settings.json` and equivalent tool settings. If a command is not explicitly allowed, ask.
- Dangerous operations like `git push`, deploy, or database migrations require user consent and a recorded log entry.

## 13) Tool mappings
- Claude Code: obey `CLAUDE.md`, `.claude/output-styles/`, `.claude/commands/`, and `.claude/settings.json`.
- Copilot Chat: if present, mirror these rules in `.github/copilot-instructions.md` and reference this file.
- ChatGPT extensions: set this file as the system message or pinned context where supported.

## 14) Checklists
- Builder pre-commit
  - [ ] Plan approved
  - [ ] Files listed and scoped
  - [ ] Tests defined
  - [ ] Risk areas noted
  - [ ] Full files written
  - [ ] Changelogs appended
- Validator gate
  - [ ] Plan matches scope and guardrails
  - [ ] Tests executed and attached
  - [ ] No errors or regressions in logs
  - [ ] User has confirmed LIVE works

## 15) Incident protocol
- On failure: stop, capture logs, write a brief RCA in `context/session.md`, propose fix plan and rollback.

## 16) Versioning
- Bump this file’s version when rules change. Keep an entry in `context/decisions.md` linking the commit.

End of file.