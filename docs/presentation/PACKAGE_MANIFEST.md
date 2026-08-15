# FiPilot Slide Evidence Package Manifest

Generated on 2026-08-14 from repository revision `51fc3b57` on branch
`restore/first-deploy-frontend`.

## Package contents

- `SYSTEM_TRUTH_MAP.md` — implementation, deployment, evaluation, and current
  deck claim boundaries.
- `PROPOSED_SLIDE_PLAN.md` — source-backed 33-slide editing plan.
- `EVALUATION_EVIDENCE_AUDIT.md` — controlling claim gate, exact slide-safe
  wording, primary file-and-line citations, and evaluation provenance audit.
- `PRODUCT_SCREENSHOT_EVIDENCE.md` — capture method, sanitized fixture
  disclosure, route mapping, and PNG hashes.
- `screenshots/01-candidate-profile.png` — real Candidate Profile route.
- `screenshots/02-interview-session.png` — real active text-interview route.
- `screenshots/03-final-report.png` — real saved-report route.
- `screenshots/04-interview-history.png` — real history route.
- `diagrams/01-system-context.svg` through `05-data-model.svg` — existing
  architecture diagrams from `docs/diagrams/`.

The source PPTX is intentionally excluded and was not edited.

## Controlling boundaries

- No LangGraph in the active runtime.
- No vector database or embedding implementation in the audited source.
- Retrieval is local lexical token overlap over a packaged catalog.
- The text workflow has a dated production verification record from
  2026-07-23.
- Voice is implemented in current source and supported by local/private-service
  documentation; production voice deployment is not proven by the available
  deployment record.
- Current empirical AI metrics are N/A / `no_data`. Screenshot scores are
  sanitized demo output, not benchmark evidence.

`EVALUATION_EVIDENCE_AUDIT.md` is authoritative if a shorter document or visual
caption could be read more broadly.
