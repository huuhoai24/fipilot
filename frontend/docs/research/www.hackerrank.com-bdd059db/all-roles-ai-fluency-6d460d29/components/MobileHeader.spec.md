# MobileHeader Specification

## Overview

- Target file: `src/components/sites/www.hackerrank.com-bdd059db/all-roles-ai-fluency-6d460d29/MobileHeader.tsx`
- Screenshot: `docs/design-references/www.hackerrank.com-bdd059db/all-roles-ai-fluency-6d460d29/mobile-full-390.png`
- Interaction model: click-driven leading menu control and profile menu.

## Direct observation

- At 390px, the accessibility tree exposes a leading button followed by a HackerRank Home link/logo.
- Compact header controls and profile trigger remain exposed.
- Clicking the leading button produced no additional accessible state after one second; no drawer content is asserted.
