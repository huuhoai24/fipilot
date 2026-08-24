# AudioCameraSettings Specification

## Overview

- Target file: `src/components/sites/www.hackerrank.com-bdd059db/all-roles-ai-fluency-6d460d29/AudioCameraSettings.tsx`
- Screenshot: `docs/design-references/www.hackerrank.com-bdd059db/all-roles-ai-fluency-6d460d29/interview-entry-1440.png`
- Interaction model: click-driven device-settings gate.

## Directly observed structure

- Heading: `Audio & Camera Settings`.
- Microphone shown: `Built-in Audio Analog Stereo`, with a combobox and 0–100 meter. Meter value at observation: `46.1484375`.
- Speaker shown: `Built-in Audio Analog Stereo`, with a combobox and `Test Speakers` button.
- Camera shown: `Integrated Webcam`, with a combobox.
- Footer buttons: Cancel and Start Interview.

## Computed styles

- Fixed dialog: 640px wide; 24px padding; white background; 12px radius; foreground `rgb(18, 20, 24)`; `16px / 400 / 18.4px`.
- Test Speakers: `14px / 700 / 20px`; transparent background; 8px radius; 16px 12px padding.
- Cancel: `14px / 700 / 20px`; transparent background; 8px radius; 8px 20px padding.
- Start Interview: `14px / 700 / 20px`; white foreground; `rgb(19, 129, 58)` background; 8px radius; 8px 20px padding.

## States & boundary

- The device-option lists could not be opened through the connected browser because their focusable input measured about 0.01px wide. No options are inferred.
- Start Interview was issued with user authorization. The connected browser did not return a subsequent accessible snapshot or tab list within 30 seconds; no subsequent screen is documented.
