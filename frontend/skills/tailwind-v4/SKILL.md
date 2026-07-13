---
name: tailwind-v4
description: "Use when working on Tailwind CSS v4 tasks in this project: setup, migration from v3 syntax, utility/class authoring, theme tokens with @theme, and debugging Tailwind styles."
argument-hint: "<task-or-file>"
---

# Tailwind CSS v4 Skill

Use this skill for implementing or reviewing Tailwind v4 changes in this repo.

## When to Use

- Add Tailwind CSS v4 to Astro pages/components
- Migrate old Tailwind v3 patterns to v4
- Define or update design tokens in CSS
- Fix missing or incorrect Tailwind styles

## Tailwind v4 Defaults

1. Use a CSS entry file with:
   - `@import "tailwindcss";`
2. Prefer CSS-first customization:
   - `@theme` for tokens
   - `@utility` for custom utilities
   - `@variant` for state/selector-based variants
3. Avoid legacy v3 directives unless explicitly required:
   - `@tailwind base;`
   - `@tailwind components;`
   - `@tailwind utilities;`

## Procedure

1. Inspect project setup and identify whether Tailwind v4 is already installed.
2. If missing, add the required Tailwind v4 dependencies and wire them into Astro/Vite config.
3. Ensure a global stylesheet imports Tailwind with `@import "tailwindcss";`.
4. Add/update tokens and utilities in CSS (prefer `@theme` and `@utility`).
5. Apply utility classes in Astro/component markup.
6. Validate by running project build and checking for styling regressions.

## Debug Checklist

- Tailwind import exists in a loaded stylesheet
- The stylesheet is imported by the app layout/page
- Utility classes are valid v4 syntax
- No stale v3-only configuration patterns remain

## References

- [Tailwind v4 quick reference](./references/tailwind-v4-quick-reference.md)
- https://tailwindcss.com/docs
- https://docs.astro.build/en/guides/styling/
