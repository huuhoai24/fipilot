# InterviewPreview Specification

## Overview

- Target file: `src/components/sites/www.hackerrank.com-bdd059db/all-roles-ai-fluency-6d460d29/InterviewPreview.tsx`
- Screenshot: `docs/design-references/www.hackerrank.com-bdd059db/all-roles-ai-fluency-6d460d29/desktop-full-1440.png`
- Interaction model: static preview with untested media controls.

## Directly observed content and styles

- Background: `linear-gradient(135deg, rgb(35, 88, 219) 0px, rgb(74, 115, 254) 50%, rgb(102, 135, 255) 100%)`.
- Displayed text includes `30:00` and `LISTENING...`.
- Buttons: `Mute microphone` and `Disable video`; each measured 36px × 36px; `display:flex`; background `rgb(235, 235, 243)`; foreground `rgb(53, 54, 63)`; radius `20%`; transition `0.1s ease-in-out`.

## Responsive behavior

- Exposed at desktop 1440px.
- Not exposed in the 768px or 390px accessibility snapshots. No inference is made about whether it is hidden, moved, or otherwise represented.
