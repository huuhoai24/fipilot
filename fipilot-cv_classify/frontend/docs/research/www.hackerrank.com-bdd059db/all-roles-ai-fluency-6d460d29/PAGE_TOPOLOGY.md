# Page Topology

Observed at `https://www.hackerrank.com/mock-interviews/all-roles/ai-fluency` while authenticated.

1. Header — dark horizontal navigation at desktop: HackerRank logo, Prepare, Certify, Compete, search, navigation controls, theme control, app drawer control, and profile menu. At 768px the primary links are absent. At 390px a separate leading menu button and logo are present.
2. Intro — `AI Fluency`, followed by `Practice with AI-powered voice interviews`.
3. Availability banner — `You have 1 mock interview available`.
4. Four benefit rows — each contains a title, explanatory sentence, and separator.
5. Call to action — `Try for free`.
6. Interview-preview panel — blue gradient panel on desktop containing a `30:00` display, listening status, and microphone/video controls. It was not exposed in the 768px or 390px accessibility snapshots.
7. Audio & Camera Settings modal — fixed device gate shown after Try for free. Measured 640px wide, 650px high at x=400/y=175 in the 1440px viewport.

## Layout and interaction model

- Page height equalled the 1000px desktop viewport in the inspected session; no additional scroll state was directly observed.
- Header and page content are in normal flow in the observed initial state.
- Profile menu is click-driven. The mobile leading menu button was clicked but no additional accessible state was observed after one second.
- The CTA starts a real interview according to its observed `start_interview_clicked` analytics attribute; with explicit user authorization, it opened the Audio & Camera Settings modal.
- The audio/camera modal is click-driven. Its Start Interview action was issued, but the browser connection did not return an inspectable post-start state.
