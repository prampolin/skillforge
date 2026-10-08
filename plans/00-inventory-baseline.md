# Phase 00 — Inventory & Baseline

**Status:** done  
**Last reviewed:** 2026-10-07 (America/Sao_Paulo)  
**Dependencies:** None  
**Purpose:** Inventory the existing Next.js 16 project and skills before changing architecture.

## Scope and tasks

- [x] **00.01 — Record the current file tree, package scripts, lockfile and Git status**  
  Acceptance: Baseline report includes versions and current commands.
- [x] **00.02 — Inspect AGENTS.md, skills and EVAL-001 artifacts**  
  Acceptance: Existing work is catalogued without overwriting files.
- [x] **00.03 — Run existing safe typecheck/lint/test commands where available**  
  Acceptance: Actual pass/fail/not-configured evidence is recorded.
- [x] **00.04 — Document architectural decisions in docs/decisions/**  
  Acceptance: Decisions for local-first, orchestration and data storage are recorded.

## Verification and evidence

- Evidence destination: `docs/architecture/current-state.md` (create or update when implementing).
- Record the exact check command, exit result, observed behavior, and any limitations in the Progress log.
- Never invent results or mark work done based on planned output.

## Out of scope

- Do not perform unrelated refactors or upgrade libraries solely to finish this phase.
- Do not make paid model calls without explicit approval.

## Progress log

| Date (UTC or with timezone) | Item | Change / evidence | Result |
|---|---|---|---|
| 2026-10-07 (America/Sao_Paulo) | 00.01 | [Baseline inventory](../docs/architecture/current-state.md): file and empty-directory inventory, package scripts, installed versions, npm lockfile v3, HEAD and initial dirty Git status recorded | verified |
| 2026-10-07 (America/Sao_Paulo) | 00.02 | AGENTS, skill/references, EVAL-001 source and two ignored manifests inspected; both prepared/not_run, usage null; zero-byte placeholders identified | verified inventory; benchmark not run |
| 2026-10-07 (America/Sao_Paulo) | 00.03 | `npm run lint`, `./node_modules/.bin/tsc --noEmit --incremental false`, `bash -n scripts/run-eval-001.sh`, Python AST/structural checks: exit 0. Tests not configured; build/browser not run. See audit for limits | verified |
| 2026-10-07 (America/Sao_Paulo) | 00.04 | [Decision record](../docs/decisions/0001-local-first-architecture.md) consolidates existing local-first, FastAPI, SQLite and host-executor decisions; no runtime changes | documented |
