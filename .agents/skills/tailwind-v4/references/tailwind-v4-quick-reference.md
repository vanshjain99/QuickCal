# Tailwind CSS v4 Quick Reference

## Core import

```css
@import "tailwindcss";
```

## Theme tokens

```css
@theme {
  --color-brand-500: oklch(62% 0.2 255);
  --radius-card: 1rem;
}
```

## Custom utility

```css
@utility content-auto {
  content-visibility: auto;
}
```

## Custom variant

```css
@variant hocus (&:hover, &:focus);
```

## Migration notes from v3

- Replace `@tailwind base/components/utilities` with `@import "tailwindcss";`
- Prefer CSS-first customization with `@theme` instead of relying only on JS config
- Re-check any plugin or config assumptions that were v3-specific
