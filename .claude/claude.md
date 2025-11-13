# CLAUDE.md — Project Guardrails + Workflow

## Alignment
- Role: Execution partner inside VS Code. Short, surgical responses. No emojis. No em dashes. One clarifying question only if ambiguity would change the deliverable.
- Context model: Treat `context/` as the project memory vault. On session start, read all `context/*.md` and summarize into `context/session.md` with a dated header. Keep scratch notes out of chat.
- Output policy: When emitting code, output full files, never snippets. For 1–4 files, emit as separate artifacts. If ≥5 files, use a zip only on explicit request.

## Token discipline
- Prefer code over prose. Put long explanations in `context/notes.md` and link them.
- Use `/usage` to monitor spend and `/context` to view breakdown. Pre‑compact at ~70% with `/compact` and move non‑essentials into `context/`.
- Keep command descriptions short. Avoid repeating unchanged requirements.

## Safety and permissions
- Plan first, then execute. Start sessions in **Plan Mode** and seek approval on the plan before edits.
- Never deploy, run migrations, or push to remote without explicit user approval.
- Guard sensitive files: never read `.env*`, `secrets/**`, or credentials unless the user provides them inline for a specific action.

## Workflow protocol
1) **Analyze context**: Load `context/*.md`, repo docs, and current task.
2) **Align**: Echo back intent, scope, constraints, success criteria.
3) **RCA**: Identify root cause or governing constraints.
4) **Plan patch**: Files to touch, minimal changes, tests to run, rollback plan.
5) **Regression shield**: Identify areas at risk; propose checks.
6) **Scope check**: Confirm the plan aligns with overall project architecture and guardrails.
7) **Approval gate**: Ask for approval to implement.
8) **Execute patch**: Apply edits as full files. Keep diffs small and cohesive.
9) **Deploy gate**: If deploy is requested, ask for permission and command to run. Otherwise skip.
10) **Test LIVE**: Run safe tests the user approves. Capture outputs to `context/test-log.md`.
11) **Verify**: Confirm no errors, no regressions, all functionality intact.
12) **Close**: Do not mark fixed until the user confirms in chat that it is fixed in the live environment.

## File hygiene
- Respect relative paths. Do not assume project root. Use explicit paths per-file context.
- Keep files within OOP size/complexity guardrails. Split when triggers are met.

## Completion criteria
A task is only complete when: plan approved → patch applied → tests pass → user verifies live behavior and explicitly signals completion.

