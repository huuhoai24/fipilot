# DesktopHeader Specification

## Overview

- Target file: `src/components/sites/www.hackerrank.com-bdd059db/all-roles-ai-fluency-6d460d29/DesktopHeader.tsx`
- Screenshot: `docs/design-references/www.hackerrank.com-bdd059db/all-roles-ai-fluency-6d460d29/desktop-full-1440.png`
- Interaction model: click-driven controls and menu.

## Directly observed structure and styles

- Desktop links: Prepare, Certify, Compete. Their measured outer heights are 60px. Prepare is `14px / 700 / 60px`, white; Certify and Compete are `14px / 400 / 60px`, `rgb(144, 145, 168)`.
- Header icon buttons: measured 40px × 40px; `display: flex` or `inline-flex`; radius 8px; white foreground; transparent background; pointer cursor.
- Avatar trigger: measured 58px × 40px; `display:flex`; radius 8px; transparent background; white foreground.

## States & behaviors

- At 768px the desktop primary links are not exposed.
- Profile trigger opens a menu (see ProfileMenu spec).
- Theme control carries observed `moon-icon` identifier. It was not activated.
- No other header state is asserted.
