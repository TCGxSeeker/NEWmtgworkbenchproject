# Tooling Plan

## Purpose

Record free project tooling needed for future deckbuilder UI work without starting product implementation.

## Approved Tooling Scope

- Install free runtime/tooling only.
- Prefer project-local dependencies and scaffolding.
- Keep frontend work isolated from the Python CLI.
- Do not add paid services, account-based tools, secrets, telemetry, Electron, Tauri, Rust, or production deployment tooling without a human checkpoint.

## Frontend Tooling Baseline

Target scaffold:

```text
apps/deckbuilder-ui/
```

Recommended free stack:

- Node.js LTS.
- Vite.
- React.
- TypeScript.
- Radix UI primitives for accessible menus, tabs, dialogs, popovers, and tooltips.
- `lucide-react` for icons.
- Recharts for future stats/probability views.

## Glass / Liquid UI Notes

Glassmorphism does not require a paid UI kit or special library. Use CSS selectively with:

- `backdrop-filter`.
- Translucent surfaces.
- Subtle borders.
- Soft shadows.
- Strong whitespace.
- High-contrast readable text.

The main deckbuilder workspace must stay calm and readable. Glass effects should support panels, drawers, modals, and command/search surfaces, not turn the whole app into a cluttered showcase.

## Deferred Tooling

- Playwright browser downloads until visual UI verification is needed.
- Electron/Tauri until desktop packaging is explicitly chosen.
- Any paid or account-gated design assets.

## Verification

After setup:

```powershell
node --version
npm --version
cd apps/deckbuilder-ui
npm install
npm run build
npm run lint
```
