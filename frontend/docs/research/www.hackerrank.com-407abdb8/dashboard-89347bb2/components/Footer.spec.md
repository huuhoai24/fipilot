# Footer Specification

- **Target file:** `src/components/sites/www.hackerrank.com-407abdb8/dashboard-89347bb2/Footer.tsx`
- **Screenshots:** `docs/design-references/www.hackerrank.com-407abdb8/dashboard-89347bb2/desktop-full.png`
- **Interaction model:** hover-only links

## DOM Structure

```
footer (margin 64px auto 32px; width fit-content; background #F7F8FD; border-radius 8px;
        padding 16px 20px; display flex; flex-wrap wrap; gap 16px; justify-content center;
        align-items center)
└── 7 × a (14px/500, color #2358DB, text-decoration none, text-underline-offset 4px,
           hover: text-decoration underline)
```

## Computed Styles

### Footer container
- margin: 64px auto 32px (desktop); margin-bottom 0 @mobile (≤768: margin 64px 0 0).
- width fit-content (content-sized); max-width 100%.
- background #F7F8FD; border-radius 8px; padding 16px 20px.
- display flex; flex-wrap wrap; justify-content center; align-items center; gap 16px.
- position static.

### Links
- font 14px; weight 500; color #2358DB; text-decoration none; text-underline-offset 4px.
- Hover: text-decoration underline (color unchanged).
- Transitions: none observed (instant underline).

## Content (verbatim) — label → href
Environment → https://www.hackerrank.com/environment
FAQ → https://www.hackerrank.com/faq
About Us → https://www.hackerrank.com/about-us
Helpdesk → https://help.hackerrank.com/
Careers → https://www.hackerrank.com/careers
Terms Of Service → https://www.hackerrank.com/about-us/terms-of-service
Privacy Policy → https://www.hackerrank.com/privacy

## States & Behaviors
- Hover: underline appears, offset 4px.
- Links are real <a> elements (target _blank not used on original).

## Responsive Behavior
- Desktop: single row, centered under content (width fits 7 links, margin auto centers it).
- ≤768: wraps to available width (full width at 390), margin 64px 0 0.