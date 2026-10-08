<!-- BEGIN:nextjs-agent-rules -->

## This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->

## SkillForge mandatory plan tracking

- Before **every** implementation task, read `plan.md` and the relevant detailed checklist in `plans/`. Use these as the progress source of truth; README describes the vision only.
- Inspect the actual repository before treating an item as implemented. Choose the smallest currently available unchecked item; respect dependencies and user scope.
- Before editing, identify phase/task ID, changed files, checks and risks. Do not initiate paid model benchmarks or destructive changes without explicit permission.
- After execution, update `plans/<phase>.md` and `plan.md`: checkbox, phase status, last-reviewed date and progress log with actual verification evidence. If not verified, leave unchecked and record the blocker.
- Do not fabricate check results, token usage, performance, provider compatibility, or completed milestones.
- Preserve existing files and local changes; prefer small, auditable diffs. Use Vim rather than nano in terminal instructions.

## Repository language

- Write all commit messages in English.
- Write all new or modified repository content in English, including code identifiers, comments, docstrings, documentation, tests, logs, error messages, and UI text.
- Conversation with the user may remain in Portuguese.
