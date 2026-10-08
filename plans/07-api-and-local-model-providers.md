# Phase 07 — API and Local Model Providers

**Status:** not-started  
**Last reviewed:** 2026-10-07  
**Dependencies:** 04,05  
**Purpose:** Support DeepSeek, OpenRouter, Ollama and future backends.

## Scope and tasks

- [ ] **07.01 — Add configurable API provider adapter, initially LiteLLM-compatible**  
  Acceptance: Provider choices are configuration-driven.
- [ ] **07.02 — Add local Ollama adapter and health/status checks**  
  Acceptance: No network key required for local option.
- [ ] **07.03 — Implement tool-capability declarations for raw APIs**  
  Acceptance: Raw model vs agent comparisons are labeled distinctly.
- [ ] **07.04 — Add usage/cost reports with unknown cost as unavailable**  
  Acceptance: No fabricated token/cost readings.
- [ ] **07.05 — Add secret handling and network safety tests**  
  Acceptance: Credentials redacted from logs.

## Verification and evidence

- Evidence destination: `docs/architecture/api-providers.md` (create or update when implementing).
- Record the exact check command, exit result, observed behavior, and any limitations in the Progress log.
- Never invent results or mark work done based on planned output.

## Out of scope

- Do not perform unrelated refactors or upgrade libraries solely to finish this phase.
- Do not make paid model calls without explicit approval.

## Progress log

| Date (UTC or with timezone) | Item | Change / evidence | Result |
|---|---|---|---|
| — | — | No execution recorded yet | not-started |
