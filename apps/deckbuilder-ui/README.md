# Deckbuilder UI Scaffold

This folder is a free, isolated Vite + React + TypeScript app for MTG Workbench UI work.

## Status

- `See The Deck v0` is implemented as the first narrow visible deck screen.
- It uses tiny local fixture data shaped like `deck_workspace_view_projection.v0`.
- It is not the finished deckbuilder UI or generic deckbuilder parity.
- Do not add more deckbuilder features here until the relevant contracts and specs are approved.

## Installed Free Tooling

- Vite
- React
- TypeScript
- Radix UI primitives
- `lucide-react`
- Recharts

## Commands

Use `npm.cmd` in PowerShell if `npm.ps1` is blocked by local script policy:

```powershell
$env:Path = 'C:\Program Files\nodejs;' + $env:Path
& 'C:\Program Files\nodejs\npm.cmd' run dev
& 'C:\Program Files\nodejs\npm.cmd' run build
& 'C:\Program Files\nodejs\npm.cmd' run lint
```

## UI Direction

Glass or liquid styling should be calm, readable, and selective. The main deckbuilder workspace remains the priority, with progressive disclosure instead of a dense feature collage.
