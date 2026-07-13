---
name: tailwind-v4-astro-setup
description: "Use when setting up Tailwind CSS v4 in Astro projects: install dependencies, add the CSS import, wire global styles, and verify build output."
argument-hint: "<optional-path-or-task>"
---

# Tailwind v4 + Astro Setup

Use this skill to perform or validate Tailwind CSS v4 setup in Astro projects.

## When to Use

- Tailwind is not installed in an Astro project
- A project needs migration to Tailwind v4 setup conventions
- Styles are not loading because Tailwind import or global CSS wiring is missing

## Procedure

1. Verify Astro project structure and locate style entry points.
2. Install required dependency:
   - `tailwindcss`
3. Create or update the global stylesheet to include:
   - `@import "tailwindcss";`
4. Ensure that stylesheet is imported from layout/page entry used by the app.
5. Remove or migrate stale v3 directives if present (`@tailwind base/components/utilities`).
6. Run build to verify configuration is valid.

## Validation Checklist

- `tailwindcss` exists in dependencies
- Global CSS file with `@import "tailwindcss";` is loaded by the app
- No broken build after setup

## References

- [Astro styling guide](https://docs.astro.build/en/guides/styling/)
- [Tailwind installation docs](https://tailwindcss.com/docs/installation)
- [Project Tailwind v4 quick reference](../tailwind-v4/references/tailwind-v4-quick-reference.md)
