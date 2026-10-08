<div align="center">

# SkillForge

### Build once. Guide any agent. Measure the outcome.

**An open-source engineering lab for designing, testing, and improving portable AI agent skills.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Status: Early Development](https://img.shields.io/badge/Status-Early%20Development-orange)
![Focus: AI Engineering](https://img.shields.io/badge/Focus-AI%20Engineering-7c3aed)

**Agent Skills · Next.js · TypeScript · shadcn/ui · Evaluation-Driven Development**

[Overview](#overview) · [Architecture](#architecture) · [Getting Started](#getting-started) · [Evaluations](#evaluation-framework) · [Roadmap](#roadmap) · [Contributing](#contributing) · [License](#license)

</div>

> [!NOTE]
> **Project status: early development.** This README describes the target architecture and planned workflows. Features listed in the roadmap are not necessarily implemented. Commands below are scaffolding guidance, not a claim that the entire toolchain is operational.

## Overview

SkillForge explores a practical question:

**Can well-designed, reusable skills help different AI coding agents generate higher-quality frontend code with fewer instructions and less rework?**

The project treats a skill as an engineering artifact rather than just a prompt. Each skill can include instructions, supporting references, templates, validation scripts, and measurable acceptance criteria. The goal is to improve _consistency, maintainability, accessibility, and efficiency_—and to verify improvements through repeatable evaluations.

The initial focus is **building reusable React components with Next.js, TypeScript, Tailwind CSS, and shadcn/ui**. The architecture is designed to support additional domains such as API development, automated testing, and refactoring over time.

SkillForge is **agent-oriented, not agent-exclusive**. Its skills use the open [Agent Skills](https://agentskills.io/specification) directory convention, with agent-specific adapters added where necessary. Compatibility and results depend on the capabilities and configuration of each agent; universal or identical performance is not guaranteed.

## Goals

- **Minimal prompting:** turn a short developer request into a clear, maintainable implementation.
- **Reusable knowledge:** keep conventions and implementation workflows outside one-off conversations.
- **Measurable quality:** test outcomes instead of relying on subjective impressions.
- **Cross-agent evaluation:** compare skills across supported coding agents under controlled conditions.
- **Safety by default:** limit file changes, inspect dependencies, and validate generated code before acceptance.
- **Open collaboration:** make experiments, methodologies, and improvements available to the community.

## Example Use Case

**Developer request**

> Build a responsive customer data table with search, sorting, pagination, loading states, and empty states.

**Intended skill-driven workflow**

1. Inspect the current project structure and available UI components.
2. Reuse existing shadcn/ui primitives instead of recreating them.
3. Generate strongly typed, accessible, responsive components.
4. Add relevant states and tests without changing unrelated files.
5. Run available checks and report failures or limitations accurately.

**Expected deliverable:** working component code and validation evidence—not simply a plausible-looking code snippet.

## Architecture

```text
skillforge/
├── apps/
│   ├── playground/             # Next.js UI validation environment (planned)
│   └── docs/                   # Documentation site (planned)
├── packages/
│   ├── ui/                     # Shared UI primitives (planned)
│   ├── configs/                # Shared lint/TypeScript settings (planned)
│   └── skill-runner/           # Evaluation orchestration (planned)
├── skills/
│   ├── nextjs-component/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   ├── assets/
│   │   └── scripts/
│   ├── nextjs-form/            # Planned
│   ├── nextjs-datatable/       # Planned
│   └── nextjs-layout/          # Planned
├── evals/
│   ├── datasets/               # Reproducible tasks
│   ├── rubrics/                # Scoring criteria
│   ├── baselines/              # Runs without skills
│   └── results/                # Captured evidence
├── tests/
│   ├── integration/
│   └── e2e/
├── scripts/
├── AGENTS.md                   # Repository-wide agent guidance (planned)
├── package.json               # Monorepo workspace (planned)
├── pnpm-workspace.yaml         # Planned
├── turbo.json                  # Planned
├── README.md
└── LICENSE
```

**Separation of concerns**

| Layer                    | Responsibility                                     |
| ------------------------ | -------------------------------------------------- |
| `skills/`                | Describe reusable agent behavior and domain rules. |
| `apps/playground/`       | Run and visually inspect generated components.     |
| `packages/ui/`           | Share approved components and design conventions.  |
| `packages/skill-runner/` | Execute and record repeatable evaluation runs.     |
| `evals/`                 | Store tasks, rubrics, baselines, and results.      |
| `tests/`                 | Validate integration and browser-level behavior.   |

## Technology Stack

| Area                       | Proposed tools                         |
| -------------------------- | -------------------------------------- |
| Monorepo                   | pnpm, Turborepo                        |
| Frontend                   | Next.js App Router, React, TypeScript  |
| UI                         | shadcn/ui, Tailwind CSS                |
| Forms and schemas          | React Hook Form, Zod                   |
| Unit and component testing | Vitest, Testing Library                |
| End-to-end testing         | Playwright                             |
| Code quality               | ESLint, Prettier, Husky                |
| Evaluation                 | Custom runner, structured JSON results |
| Observability (future)     | OpenTelemetry                          |

> Tooling may evolve as the project moves from design to implementation. Dependency versions will be managed in the repository, not pinned in this README.

## Getting Started

For this existing checkout, follow the verified [local development guide](docs/guides/local-development.md)
to run the root Next.js app and Python backend in separate terminals. The bootstrap
sections below describe the planned architecture, not setup required for this checkout.

### Prerequisites

- Git
- A recent Node.js LTS release compatible with the selected Next.js version
- pnpm (via Corepack or your preferred installation method)

### Bootstrap a new workspace

The following commands are intended for **initial project setup**. If the repository already contains the monorepo, clone it and use `pnpm install` instead; do not run the initializer over existing source files.

```bash
pnpm dlx shadcn@latest init -t next --monorepo
```

Follow the CLI prompts, then adapt the generated workspace to the architecture above. The official shadcn/ui monorepo starter generally creates `apps/web` and `packages/ui`; rename `apps/web` to `apps/playground` **only if** you also update relevant workspace configuration and imports.

Once the workspace and package scripts exist, the intended developer workflow is:

```bash
pnpm install
pnpm dev
pnpm lint
pnpm test
pnpm build
```

> [!IMPORTANT]
> These project scripts are **planned conventions**. Only run them after the corresponding `package.json` scripts and packages have been implemented.

## Skill Design

A skill is a folder containing a `SKILL.md` file, optionally supplemented by `references/`, `scripts/`, and `assets/`.

```text
skills/nextjs-component/
├── SKILL.md
├── references/
│   ├── architecture.md
│   ├── shadcn.md
│   └── accessibility.md
├── assets/
│   └── templates/
└── scripts/
```

Example skill metadata:

```yaml
---
name: nextjs-component
description: Create or improve accessible, reusable Next.js React components using TypeScript, Tailwind CSS, and shadcn/ui.
license: MIT
---
```

**Design principles**

1. Keep primary instructions short and actionable.
2. Reference detailed conventions only when relevant.
3. Reuse installed libraries and existing code before introducing abstractions.
4. Favor server-rendered components unless client-side interaction is required.
5. Make accessibility, responsive behavior, and error states explicit.
6. Specify boundaries: avoid unrelated edits and unnecessary dependencies.
7. Require evidence for test and build claims.
8. Record what failed and what remains uncertain.

See the [Agent Skills specification](https://agentskills.io/specification) for the interoperable format. Agent-specific integrations may still be needed.

## Evaluation Framework

SkillForge aims to benchmark the **same task with and without a skill**, using controlled project fixtures and the same agent/model configuration wherever possible.

### Initial evaluation dataset

| ID         | Task                        | Key checks                            |
| ---------- | --------------------------- | ------------------------------------- |
| `EVAL-001` | Button with loading state   | Interaction, accessibility, typing    |
| `EVAL-002` | Form with Zod validation    | Validation, errors, keyboard flow     |
| `EVAL-003` | Responsive data table       | Search, sort, pagination, empty state |
| `EVAL-004` | Editable dialog             | State, focus management, submission   |
| `EVAL-005` | Dashboard with cards        | Reuse, responsive layout, semantics   |
| `EVAL-006` | Existing component refactor | Behavior preserved, minimal diff      |

### Proposed scoring rubric

| Dimension                             |   Weight |
| ------------------------------------- | -------: |
| Functional correctness                |      35% |
| Code quality and maintainability      |      20% |
| Accessibility                         |      15% |
| Project conventions and compatibility |      15% |
| Efficiency and rework                 |      15% |
| **Total**                             | **100%** |

Additional metrics should be reported separately: token usage, latency, estimated API cost, number of attempts, manual fixes, and test pass rate. These weights are **initial hypotheses**, not validated benchmarks.

### Reproducibility standards

- Freeze the task, project fixture, dependency lockfile, and acceptance criteria.
- Record agent, model, skill version, and relevant configuration.
- Run baseline and skill-enhanced tasks in clean, isolated workspaces.
- Repeat evaluations where nondeterministic behavior could distort results.
- Keep functional checks separate from qualitative review.
- Never label an evaluation as passing unless its checks actually ran.
- Publish representative failures alongside successes.

The intended result is a versioned evidence trail, not a leaderboard based on unverified claims.

## Roadmap

- [ ] **Phase 1 — Foundation:** bootstrap monorepo, playground, shared configs, and first `nextjs-component` skill.
- [ ] **Phase 2 — Evaluation:** implement task fixtures, automated checks, run logs, and baseline comparisons.
- [ ] **Phase 3 — Agent compatibility:** test selected agents and document required adapters and limitations.
- [ ] **Phase 4 — Continuous improvement:** version skills, analyze failure patterns, and gate changes on regressions.
- [ ] **Phase 5 — Ecosystem:** publish documented skills, templates, and reproducible community contributions.

## Non-Goals

SkillForge does **not** aim to train a foundation model, guarantee the same output from every AI, or replace code review. Skills guide the behavior of compatible agents; their effectiveness must be measured within each real environment.

## Contributing

Contributions, bug reports, test cases, and proposals are welcome.

1. Open an issue describing the problem or proposed improvement.
2. Fork the repository and create a focused branch.
3. Keep changes small; explain which behavior or evaluation they affect.
4. Add or update tests and documentation when applicable.
5. Open a pull request with reproduction steps and validation evidence.

For skill changes, include a before/after evaluation when a runner is available. Never commit API keys, private prompts, proprietary source code, or personal evaluation data.

A more detailed `CONTRIBUTING.md` and community code of conduct are planned.

## Security

AI-generated code must be reviewed before production deployment. Run evaluation tasks in isolated workspaces with minimal permissions. Do not expose credentials to agents or execute untrusted scripts without inspection.

Until a dedicated vulnerability disclosure policy is published, avoid posting exploitable vulnerabilities or secrets in public issues. Contact the maintainer privately through a contact method listed on the repository profile, if available.

## License

Copyright © 2026 Vitor Prampolin.

This project's original source code, skills, scripts, and documentation are made available under the **MIT License**. See the [LICENSE](LICENSE) file for the full terms.

MIT permits use, modification, distribution, private use, and commercial use, provided the applicable copyright and license notices are retained. It provides the software **as is**, without warranty.

Third-party packages, components, assets, trademarks, and model services remain subject to their **own** licenses and terms. The project license does not relicense upstream dependencies or guarantee that AI-generated outputs are free of third-party obligations.

## Acknowledgments

This project is inspired by the open [Agent Skills specification](https://agentskills.io/specification), [Next.js](https://nextjs.org/), and [shadcn/ui](https://ui.shadcn.com/). These projects are independent and are not affiliated with or endorsing SkillForge.

---

<div align="center">

**SkillForge — Engineering skills, not just prompts.**

Built in the open. Improved through evidence.

</div>
