# Phase 04 — Benchmark Orchestrator & Scoring

**Status:** not-started  
**Last reviewed:** 2026-10-07  
**Dependencies:** 03  
**Purpose:** Run baseline vs skill consistently and save verifiable results.

## Scope and tasks

- [ ] **04.01 — Define baseline/skill variant preparation and instruction isolation policy**  
  Acceptance: Contamination limits documented in run manifest.
- [ ] **04.02 — Create isolated workspaces per variant with no source overwrite**  
  Acceptance: Working tree remains unchanged.
- [ ] **04.03 — Persist immutable run manifest and JSONL event logs**  
  Acceptance: Each run is traceable by ID and timestamp.
- [ ] **04.04 — Run configured typecheck/lint/test on generated output**  
  Acceptance: Scoring uses actual results; missing checks are N/A.
- [ ] **04.05 — Implement initial rubric score and repeat-run comparison**  
  Acceptance: Subscores, weights, and uncertainty visible.
- [ ] **04.06 — Add tests for failures, timeouts and partial results**  
  Acceptance: Failures are stored, not hidden.

## Verification and evidence

- Evidence destination: `docs/architecture/evaluation-methodology.md` (create or update when implementing).
- Record the exact check command, exit result, observed behavior, and any limitations in the Progress log.
- Never invent results or mark work done based on planned output.

## Out of scope

- Do not perform unrelated refactors or upgrade libraries solely to finish this phase.
- Do not make paid model calls without explicit approval.

## Progress log

| Date (UTC or with timezone) | Item | Change / evidence | Result |
|---|---|---|---|
| — | — | No execution recorded yet | not-started |
