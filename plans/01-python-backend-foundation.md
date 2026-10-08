# Phase 01 — Python Backend Foundation

**Status:** in-progress  
**Last reviewed:** 2026-10-07 (America/Sao_Paulo)  
**Dependencies:** 00  
**Purpose:** Introduce a minimal FastAPI service without disturbing the existing Next.js app.

## Scope and tasks

- [x] **01.01 — Create backend/pyproject.toml and app package**  
  Acceptance: Python dependencies and supported version are pinned/documented.
- [ ] **01.02 — Implement GET /health and GET /api/v1/info**  
  Acceptance: Both endpoints have stable JSON contracts.
- [ ] **01.03 — Implement settings, CORS allowlist and structured logs**  
  Acceptance: No open CORS or secrets in logs.
- [ ] **01.04 — Add pytest health/config tests**  
  Acceptance: Tests run with documented command.
- [ ] **01.05 — Document local startup alongside Next.js**  
  Acceptance: Both servers can run independently.

## Verification and evidence

- Evidence destination: `backend/README.md` (create or update when implementing).
- Record the exact check command, exit result, observed behavior, and any limitations in the Progress log.
- Never invent results or mark work done based on planned output.

## Out of scope

- Do not perform unrelated refactors or upgrade libraries solely to finish this phase.
- Do not make paid model calls without explicit approval.

## Progress log

| Date (UTC or with timezone) | Item | Change / evidence | Result |
|---|---|---|---|
| 2026-10-07 (America/Sao_Paulo) | 01.01 | Added installable `backend/app`, pinned direct/build dependencies in `pyproject.toml`, Python 3.14 baseline, runtime `uv.lock` and local ignores. [Evidence](../backend/README.md): isolated sync, offline sdist/wheel build, lock check, dependency check and imports all exit 0 on Python 3.14.7; wheel content inspected. No endpoints implemented | verified |
