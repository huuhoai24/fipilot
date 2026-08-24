# PAGE_TOPOLOGY.md — hackerrank.com/mock-interviews/all-roles/ai-fluency

Source route: `/mock-interviews/all-roles/ai-fluency`.

## Screen and state inventory

1. **Landing** — HackerRank navigation, AI Fluency title, four benefit rows, session duration, and Start Interview CTA. The live logged-out page also exposes an exhausted-credit banner; the clone makes this available from the start screen.
2. **Setup** — microphone/camera readiness checks, privacy reminder, and Continue / Back transitions.
3. **Instructions** — interview format, 30-minute duration, voice-answer guidance, and Begin Interview / Back transitions.
4. **Interview** — timed question view, question progress, text response area, next/previous navigation, submit-answer loading state, and end-interview confirmation modal.
5. **Completion loading** — a short feedback-generation state after the final response.
6. **Results** — score summary, strengths, opportunities, per-question feedback, restart, and Dashboard transition.

## Interaction model

- **Route navigation:** dashboard AI Fluency card links to the preserved source pathname.
- **Client state:** setup, instructions, interview questions, answer submission, confirmation modal, and results are local states because the production runtime is API/session backed.
- **Responsive:** landing columns collapse; setup/instructions cards and interview workspace fit a single mobile column.
