# Deckbuilder UI Scaffold

This folder is a free, isolated Vite + React + TypeScript scaffold for future MTG Workbench UI work.

## Status

- Tooling only.
- Not the finished deckbuilder UI.
- Do not implement deckbuilder features here until the relevant contracts and specs are approved.

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
