<!-- copilot:version=1.0 author=Copilot date=2026-07-13 advisory=true -->
# Copilot Skills Examples — gotcha-capture

This file is an example of how Copilot will apply the gotcha-capture workflow when the user corrects or rejects an output.

Example workflow
1. User: "Don't recommend Sol Ring for this deck — it's intentional policy."
2. Copilot: record gotcha with scope=repo, symptom="incorrect recommendation: Sol Ring", cause="recommendation engine defaulted to popularity", fix="exclude Sol Ring for decks with policy X", prevention="add rule in docs/rules to prefer user-owned-only staples"
3. Copilot appends an entry to docs/codex/GOTCHAS.md and writes a short replica here under copilot/gotchas for review.

Mirroring policy
- Copilot will not promote this change to canonical docs without a promotion PR and verification evidence.
