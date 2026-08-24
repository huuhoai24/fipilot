# StartInterviewCta Specification

## Overview

- Target file: `src/components/sites/www.hackerrank.com-bdd059db/all-roles-ai-fluency-6d460d29/StartInterviewCta.tsx`
- Screenshot: `docs/design-references/www.hackerrank.com-bdd059db/all-roles-ai-fluency-6d460d29/desktop-full-1440.png`
- Interaction model: click-driven; activation opens the Audio & Camera Settings modal.

## Computed styles and text

- Text: `Try for free`.
- Measured desktop size: 112px × 48px.
- `display:flex`; `14px / 700 / 20px`; white foreground; `rgb(19, 129, 58)` background; radius 8px; pointer cursor.
- Transition: `color 0.2s ease-in-out, backgroundColor 0.2s ease-in-out, borderColor 0.2s ease-in-out`.

## Behavior boundary

The observed analytics interaction is `start_interview_clicked`. With explicit user authorization, activating the button opened Audio & Camera Settings. The Start Interview action from that modal was then issued, but no subsequent state was available from the browser connection.
