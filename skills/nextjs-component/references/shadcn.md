# shadcn/ui composition

Inspect `components.json`, path aliases, and actual component source before importing a primitive. shadcn/ui components are project-owned source: upstream examples do not establish the local API. Check supported variants, slot behavior, forwarded props, and class merging.

Reuse installed Card, Avatar, Button, and related primitives when they fit the task. If absent, use semantic HTML and existing styling utilities; do not invent imports, install a component library, or add form dependencies for a display component.

Use the project's Tailwind version, tokens, and existing dark-mode conventions. Preserve focus styling and readable contrast when composing variants. Check the final rendered element: a navigation action should remain a link, and a command should remain a button. Avoid nested interactive elements when using slots or `asChild` APIs.

For avatars, distinguish missing images from failed image loads. Reuse an existing fallback mechanism when available. Avoid duplicate announcements when the adjacent text already identifies the person. Do not assume initials alone communicate identity.
