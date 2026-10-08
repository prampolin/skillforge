# Phase 01 — Python Backend Foundation

**Status:** done
**Last reviewed:** 2026-10-07 (America/Sao_Paulo)  
**Dependencies:** 00  
**Purpose:** Introduce a minimal FastAPI service without disturbing the existing Next.js app.

## Scope and tasks

- [x] **01.01 — Create backend/pyproject.toml and app package**  
  Acceptance: Python dependencies and supported version are pinned/documented.
- [x] **01.02 — Implement GET /health and GET /api/v1/info**
  Acceptance: Both endpoints have stable JSON contracts.
- [x] **01.03 — Implement settings, CORS allowlist and structured logs**
  Acceptance: No open CORS or secrets in logs.
- [x] **01.04 — Add pytest health/config tests**
  Acceptance: Tests run with documented command.
- [x] **01.05 — Document local startup alongside Next.js**
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
| 2026-10-07 (America/Sao_Paulo) | 01.02 | Added `app.main:app` with typed health/info responses and installed distribution version. [Evidence](../backend/README.md): offline lock/sync exit 0; temporary loopback HTTP harness exit 0 for exact JSON, 200/content type, OpenAPI required fields, version parity, 404 and 405. Pytest remains 01.04 | verified |
| 2026-10-07 (America/Sao_Paulo) | 01.03 | Validated environment settings, explicit GET-only CORS allowlist, JSON logging and loopback launcher. [Evidence](../backend/README.md): four unittest safety checks passed; real launcher HTTP/OpenAPI/JSON-log harness exit 0. Pytest setup remains 01.04 | verified |
| 2026-10-07 (America/Sao_Paulo) | 01.04 | Pinned pytest/httpx2 dev dependencies, configured collection, added HTTP/OpenAPI and environment integration tests plus process-state isolation. [Documented command](../backend/README.md) with `-W error`: 15 passed, 17 subtests passed, exit 0; dependency check exit 0. Existing unittest checks retained | verified |
| 2026-10-07 (America/Sao_Paulo) | 01.05 | [Local startup guide](../docs/guides/local-development.md) and README entry points. Real-process HTTP harness exit 0: concurrent responses, exact CORS origin, each service responds after stopping the other; all created processes stopped. Existing dependency/cache scope documented | verified; phase done |
