# Component architecture

Inspect the installed Next.js guides in `node_modules/next/dist/docs/` when available, especially server/client boundaries. Follow the existing router and directory structure rather than introducing a new architecture.

Keep data display server-compatible unless hooks, event handlers, or browser APIs require a client boundary. Put that boundary around the smallest interactive unit. Ordinary callback props cannot cross from a Server Component into a Client Component; use serializable inputs or keep the caller within the client boundary.

Export a typed props contract. Distinguish required identity fields from optional presentation fields; handle missing values deliberately. Prefer composition and ordinary props over speculative configuration systems. Avoid `any`, type suppression, derived state, effects for synchronous computation, and fetching inside reusable display components.

Reuse established class utilities and design tokens. Accept styling extension props when useful, and avoid fixed widths that prevent reuse in grids or sidebars. Long names and unbroken strings must wrap without pushing adjacent controls outside the container.

Validate with the installed TypeScript and ESLint executables. Do not run a package installer to obtain missing checks. Report missing tools and runtime behavior that has not been exercised.
