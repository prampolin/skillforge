# Phase 03 — Local CLI Provider Adapters

**Status:** not-started  
**Last reviewed:** 2026-10-07  
**Dependencies:** 02  
**Purpose:** Make Codex and Claude available through an interchangeable runner interface.

## Scope and tasks

- [ ] **03.01 — Design ProviderAdapter protocol with capability detection**  
  Acceptance: Unsupported features are reported, never guessed.
- [ ] **03.02 — Implement Codex CLI adapter using authenticated local installation**  
  Acceptance: No private credential files are copied.
- [ ] **03.03 — Implement Claude Code adapter, optionally unavailable**  
  Acceptance: Absent CLI/login produces clear inactive state.
- [ ] **03.04 — Add subprocess timeout, cancellation and restricted cwd**  
  Acceptance: Commands and writes are constrained to run workspace.
- [ ] **03.05 — Unit-test adapters with mocked process output**  
  Acceptance: Tests do not require paid calls.

## Verification and evidence

- Evidence destination: `docs/architecture/provider-adapters.md` (create or update when implementing).
- Record the exact check command, exit result, observed behavior, and any limitations in the Progress log.
- Never invent results or mark work done based on planned output.

## Out of scope

- Do not perform unrelated refactors or upgrade libraries solely to finish this phase.
- Do not make paid model calls without explicit approval.

## Progress log

| Date (UTC or with timezone) | Item | Change / evidence | Result |
|---|---|---|---|
| — | — | No execution recorded yet | not-started |
