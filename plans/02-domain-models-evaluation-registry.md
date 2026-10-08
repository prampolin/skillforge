# Phase 02 — Domain Models & Evaluation Registry

**Status:** in-progress
**Last reviewed:** 2026-10-07 (America/Sao_Paulo)
**Dependencies:** 01  
**Purpose:** Standardize skills, models, benchmarks and execution results.

## Scope and tasks

- [x] **02.01 — Define Pydantic schemas for provider, model, skill, eval and run**
  Acceptance: Schemas have explicit identifiers and versions.
- [ ] **02.02 — Load and validate evals/datasets and skills metadata**  
  Acceptance: Malformed metadata yields actionable validation errors.
- [ ] **02.03 — Implement read-only discovery endpoints**  
  Acceptance: UI can list skills, benchmarks and provider capabilities.
- [ ] **02.04 — Add schema/registry tests and stable fixture**  
  Acceptance: Versioned fixture loads consistently.

## Verification and evidence

- Evidence destination: `docs/architecture/contracts.md` (create or update when implementing).
- Record the exact check command, exit result, observed behavior, and any limitations in the Progress log.
- Never invent results or mark work done based on planned output.

## Out of scope

- Do not perform unrelated refactors or upgrade libraries solely to finish this phase.
- Do not make paid model calls without explicit approval.

## Progress log

| Date (UTC or with timezone) | Item | Change / evidence | Result |
|---|---|---|---|
| 2026-10-07 (America/Sao_Paulo) | 02.01 | Added five versioned domain schemas, revision references, unknown capability/usage semantics and run consistency validation. [Contracts and evidence](../docs/architecture/contracts.md): pytest with `-W error` exit 0, 59 tests and 17 subtests passed. Registry, metadata loading and stable registry fixture remain pending | verified |
