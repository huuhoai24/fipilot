# InterviewOS Architecture Documentation

This directory is an evidence-backed architecture snapshot of the checked-out source tree as audited on 2026-08-20. It distinguishes executable behavior from partial implementations, target specifications, offline research, and operational unknowns.

## Start here

- [System Inventory](SYSTEM_INVENTORY.md) — canonical components, runtime entry points, stores, caches, and external dependencies.
- [Diagram Index](DIAGRAM_INDEX.md) — table of all 95 diagrams and standalone Mermaid sources.
- [Architecture Diagram Suite](DIAGRAMS.md) — rendered narrative with purpose, flow, decisions, failures, evidence, and gaps for every diagram.
- [Architecture Gaps](ARCHITECTURE_GAPS.md) — mismatch, risk, missing-test, unused-code, and unknown-state matrix.
- [Research Evidence](RESEARCH_EVIDENCE.md) — detailed source-symbol and primary-document audit notes.

Standalone Mermaid sources live under [`diagrams/`](diagrams/). Their numeric prefixes follow the required topic order.

## Status vocabulary

| Label | Meaning |
|---|---|
| IMPLEMENTED | Present in executable source at the stated scope |
| PARTIAL | Present, but incomplete relative to the documented contract or operational boundary |
| SPEC-PENDING | Described by a binding spec/ADR but absent from active runtime source |
| UNKNOWN | Cannot be established from repository evidence |
| IMPLEMENTED OFFLINE | Implemented in evaluation/research tooling, not the production request path |
| EXTERNAL | A provider or actor outside repository ownership |
| STORAGE | A persistence or packaged-data boundary |

Composite labels such as `IMPLEMENTED/PARTIAL` describe diagrams that intentionally show both complete and incomplete subpaths.

## Reading rules

- Runtime source wins when documentation conflicts with executable behavior; the mismatch is recorded rather than silently reconciled.
- `backend/gateway/main.py` is the active backend. `backend/main.py` is a compatibility re-export, and `backend/app/**` is not a second implementation path.
- Source-controlled deployment assets show deployability, not current live state.
- Offline RAG ablation and M1-M8 evaluation artifacts are not production feature flags or request-path components.
- No secrets or `.env` values are reproduced. The active helper's configuration-file boundary is documented only by path and precedence.

## Validation

Run the documentation validator from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\docs\validate_mermaid.ps1
```

The validator checks the 95-file manifest, recognized Mermaid declaration, balanced delimiters, forbidden embedded fences/HTML, index and narrative coverage, unique titles, required evidence fields, and status labels. It is a deterministic repository check, not a browser screenshot or Mermaid CLI render test.

