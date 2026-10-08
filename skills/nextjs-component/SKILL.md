---
name: nextjs-component
description: Create, refactor, and validate reusable Next.js React components with TypeScript and existing Tailwind or shadcn/ui conventions. Use for component implementation and responsive UI work in an existing Next.js project.
---

# Next.js Component Engineering

Inspect the project, installed packages, nearby components, and local Next.js documentation before choosing APIs. Preserve existing conventions and unrelated functionality; do not install dependencies unless authorized.

Read the relevant references before implementation:

- [Architecture](references/architecture.md): component boundaries, prop APIs, and TypeScript.
- [shadcn/ui](references/shadcn.md): inspect and compose installed primitives, or use semantic HTML when absent.
- [Accessibility](references/accessibility.md): semantics, keyboard behavior, responsive content, and verification.

Keep the implementation focused on the requested behavior. Run configured type and lint checks using installed tools. Report changed files, actual check results, and unverified behavior; never equate lint success with accessibility verification.
