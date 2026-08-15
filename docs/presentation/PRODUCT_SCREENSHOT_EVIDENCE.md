# Product Screenshot Evidence

Capture date: 2026-08-14
Purpose: source-backed visual evidence for the Capstone presentation's
**End-to-End Product Flow** slide.

## Capture decision

The application could run locally. The screenshots therefore use the real
React routes and real FastAPI response contracts rather than recreated mockups.
The backend used an isolated SQLite database seeded with explicitly synthetic
content. Local development authentication was enabled through FiPilot's
documented backend bypass and a capture-only frontend auth adapter; no personal
Firebase account, production Firestore data, Resume, transcript, or answer was
used.

These captures demonstrate implemented product surfaces and end-to-end data
rendering. They are **not** production-deployment proof and are **not** AI
evaluation results. In particular, report scores visible in the UI are
synthetic demonstration values.

## Captured routes and assets

| Stage | Real route | Screenshot | Slide use |
| --- | --- | --- | --- |
| Candidate Profile | `/candidate-profile/101` | `screenshots/01-candidate-profile.png` | Main slide panel 1 |
| Active text interview | `/text-interview/201` | `screenshots/02-interview-session.png` | Main slide panel 2 |
| Final coaching report | `/text-interview/202/report` | `screenshots/03-final-report.png` | Main slide panel 3 |
| Interview history | `/interview-history` | `screenshots/04-interview-history.png` | Backup/supporting evidence |

All four captures are 1440 × 900 PNG files in the repository's current
blue/white UI.

## Sanitized fixture

- Candidate identity: `Demo Candidate`
- Account label: `FiPilot Demo`
- Organization and education names explicitly contain `Demo`
- Questions and answers were written for this capture and contain no real
  person, employer, project, or interview response
- SQLite owner: `product-flow-demo-user`
- Candidate/session identifiers: `101`, `201`, and `202`
- The report and its scores are deterministic sample product output

The active session was seeded at question 3 of 5 so the screenshot visibly
demonstrates persisted conversation history, current-question state, progress,
and answer input. The report session was separately seeded as
`report_generated` so the GET path loaded a saved report without calling Gemini.

## Commands and verification

The isolated seed and capture helpers are under ignored `.scratch` storage.
The effective commands were:

```powershell
backend\.venv\Scripts\python.exe .scratch\seed_product_flow.py

$env:BACKEND_ENV_FILE=(Resolve-Path .scratch\product-flow-backend.env).Path
powershell -ExecutionPolicy Bypass -File scripts\run_backend.ps1

# From the repository root; native config loading avoids path bundling issues.
node frontend/node_modules/vite/bin/vite.js `
  --config .scratch/vite.product-flow.config.mjs `
  --configLoader native `
  --host localhost

node .scratch\capture_product_flow.mjs
```

Verification completed before capture:

- `GET /health` returned `{"status":"ok"}`.
- Candidate Profile, active session, saved report, and history endpoints returned
  the seeded records through the running FastAPI application.
- Playwright completed all four captures with exit code `0`.
- The final evidence-package recapture on 2026-08-14 returned backend
  `status=ok` and frontend HTTP `200`; the four hashes below remained unchanged.
- Visual inspection confirmed Tailwind styling, readable content, no loading or
  error state, and no personal identifiers.
- Both local services were stopped after capture.

## File hashes

| File | SHA-256 |
| --- | --- |
| `01-candidate-profile.png` | `85A7A7C6B5A32A8AC18731C35A872F06D95C94ADBFB3C5663813F02ABE0AC8DD` |
| `02-interview-session.png` | `D10365D5EF70802757606F3B6C4F2EFAABD29B4E02A85DBF67B874233BDBDB06` |
| `03-final-report.png` | `BF850FADFEA812DA2B5387577E54D7AC169FF93F567A1F66CE4B1116DDD3AB7B` |
| `04-interview-history.png` | `49B3B521D7FC0DA0D8385B7FF5CD9F049A3D5FB048EE19D10FF20238B955ED39` |

## Slide composition

Slide 31 will use three numbered screenshot panels with a left-to-right flow:

1. **Profile evidence** — persisted Candidate Profile and readiness
2. **Adaptive session** — prior answers, current question, and progress
3. **Coaching report** — saved scores, strengths, gaps, and next actions

The interview panel should be the visual anchor, with the Profile and Report
panels slightly narrower. Use native PowerPoint captions and arrows rather than
adding text to the screenshots. The footer disclosure should read:

> Real local FiPilot UI captured with sanitized demo data. Displayed scores are
> sample product output, not benchmark or evaluation evidence.
