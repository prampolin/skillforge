# Phase 06 — Docker Local Development

**Status:** not-started  
**Last reviewed:** 2026-10-07  
**Dependencies:** 05  
**Purpose:** Make frontend and API reproducible with Compose.

## Scope and tasks

- [ ] **06.01 — Create Dockerfile for Next.js and FastAPI**  
  Acceptance: Images build with documented commands.
- [ ] **06.02 — Add compose.yaml with ports 3000/8000 and healthchecks**  
  Acceptance: Docker startup works without API keys.
- [ ] **06.03 — Add .dockerignore and environment template**  
  Acceptance: Secrets excluded and no credentials mounted by default.
- [ ] **06.04 — Document host executor vs containers network design**  
  Acceptance: Authenticated CLI remains on trusted host for MVP.
- [ ] **06.05 — Verify compose build/up/down and persistence**  
  Acceptance: Runbook includes actual verification results.

## Verification and evidence

- Evidence destination: `docs/guides/docker.md` (create or update when implementing).
- Record the exact check command, exit result, observed behavior, and any limitations in the Progress log.
- Never invent results or mark work done based on planned output.

## Out of scope

- Do not perform unrelated refactors or upgrade libraries solely to finish this phase.
- Do not make paid model calls without explicit approval.

## Progress log

| Date (UTC or with timezone) | Item | Change / evidence | Result |
|---|---|---|---|
| — | — | No execution recorded yet | not-started |
