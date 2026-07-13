<!-- copilot:version=1.0 author=Copilot date=2026-07-13 advisory=true -->
# Copilot advisory folder

This folder contains non-authoritative, Copilot-produced drafts, templates, and small verification artifacts.

Purpose
- Provide a safe, lightweight sandbox for Copilot to produce docs-first outputs and templates.
- Keep drafts separate from canonical docs so the primary [codex] agent (or humans) can ignore or merge them.

Policy
- Advisory-only: Nothing in this folder is canonical unless explicitly promoted by the repo owner.
- Promotion: To promote, open a PR that references the copilot file, includes a verification-gate report, and requests human or [codex] agent approval.
- Metadata: Files should include a short HTML comment metadata header, e.g. `<!-- copilot:version=1.0 author=Copilot date=YYYY-MM-DD advisory=true -->`.

See templates/ for reusable templates and agent-alignment/ for a short summary of Copilot behaviour.
