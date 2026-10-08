# Accessibility and responsive behavior

Choose native semantics before ARIA. Use headings that fit the surrounding page, links for navigation, and buttons for actions. Repeated cards need distinguishable accessible names; associate labels with unique IDs when needed, avoiding duplicate IDs across instances.

Keep all interactions keyboard reachable with visible focus. Do not make a whole card clickable by adding a click handler to a non-interactive container. Do not nest buttons inside links. An icon-only control needs an accessible name; decorative icons and redundant avatars should be hidden from assistive technology.

Represent status with visible text, not color alone. Ensure meaningful images have appropriate alternatives, and missing or broken avatars leave a usable identity. Optional fields should not produce empty labels, broken links, or meaningless placeholders.

Check narrow containers, long unbroken names and emails, zoom, and enlarged text. Prefer wrapping, flexible sizing, and `min-width: 0` where needed. Avoid fixed heights that clip content. Meet WCAG AA contrast targets for text and visible controls using the actual foreground/background combination.

Verification must distinguish code inspection from observed behavior. Exercise keyboard focus and navigation, inspect accessible names, and check layouts at narrow and wide widths when a browser is available. TypeScript and ESLint do not prove accessibility; record manual checks as pending when not performed.
