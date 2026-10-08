# 0001 — Local-first architecture

Recorded: 2026-10-07 (America/Sao_Paulo)  
Status: accepted direction already stated in `plan.md`; implementation pending  
Source: `plan.md`, Decisions and change control / Current position. Audit item: 00.04.

## Context

The repository currently contains a root Next.js scaffold, an authored component skill and a dedicated Python EVAL-001 script. README describes a future monorepo; it is not the implementation baseline. The existing plan chooses a local-first benchmark application.

## Decisions

1. Keep Next.js at the repository root until a migration has documented value. Do not introduce a monorepo simply to match the README illustration.
2. Use Python/FastAPI for orchestration: Next.js UI → FastAPI → benchmark orchestrator → CLI/API/local adapters → reports. Never expose arbitrary host command execution to untrusted web clients.
3. Start with SQLite for local run metadata. Retain JSONL event logs and immutable run manifests as target evidence artifacts. The current experimental script rewrites its manifest; it does not implement that immutable storage contract.
4. Initially execute authenticated local CLIs on the trusted host. Use Docker for reproducible web/API services without mounting host credentials into containers.
5. Label execution type for comparisons. Raw API models require a controlled tool executor for fair comparison with CLI agents.

## Consequences and verification

Backend, storage contracts, adapters and container/host communication still need implementation and tests in subsequent phases. These decisions do not establish provider compatibility, isolation guarantees or benchmark results. This record consolidates existing plan decisions without selecting new frameworks, installing dependencies or changing runtime behavior.

Verified by inspecting `plan.md`, the phase checklists, root application and runner source on the recorded date; see [current-state audit](../architecture/current-state.md).
