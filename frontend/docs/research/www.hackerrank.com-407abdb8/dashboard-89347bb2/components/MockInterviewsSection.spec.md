# MockInterviewsSection Specification

- **Target file:** `src/components/sites/www.hackerrank.com-407abdb8/dashboard-89347bb2/MockInterviewsSection.tsx`
- **Screenshots:** `docs/design-references/www.hackerrank.com-407abdb8/dashboard-89347bb2/desktop-full.png`
- **Interaction model:** click-driven carousel (prev/next/dots). NOT scroll-driven, no autoplay.
- **Imports:** `MockInterviewCard` (same dir), `ChevronLeftIcon`, `ChevronRightIcon` from `../shared/icons`, `MockInterview` type from `../shared/types`

## DOM Structure

```
section (width 100%)
├── div.header-row (56px, flex justify-between align-center, width 100%)
│   ├── div.title-col (flex column gap 4px, align-items flex-start)
│   │   ├── div (flex gap 4px align-center)
│   │   │   ├── h2 "AI-powered Mock Interviews" (hr-title-md: 20px/700/32px #121418, margin 0)
│   │   │   └── div "New" pill (14px/500 #1142AF, bg #F6F6FF, padding 4px 12px, radius 100px)
│   │   └── p (14px/400/20px #63646F) "Ace your next job interview by practicing with AI-powered mock interviews."
│   └── a "Know More" (href /mock-interviews; 14px/500 #2358DB, no underline, radius 4px, background transparent)
├── div.body (flex column, gap 16px)
│   ├── div.viewport (overflow hidden, width 100%)
│   │   └── div.track (display flex; transition transform .45s cubic-bezier(.2,.7,.2,1); transform translateX(-N * pageWidth))
│   │       └── N × div.page (flex 0 0 100%; display grid; grid-template-columns repeat(C,1fr); gap 16px; align-items stretch)
│   │           └── C × MockInterviewCard
│   └── div.pagination (40px, flex justify-center align-center gap 16px)
│       ├── button.prev (40x40, radius 8px, ghost, transparent, ChevronLeftIcon 20)
│       ├── div.dots (flex gap 8px align-center)
│       │   └── N × button.dot (8x8, radius 9999px, bg #C1C2D6, border none, cursor pointer, transition width .3s ease background .3s ease; ACTIVE: width 24px, bg #18A149)
│       └── button.next (40x40, radius 8px, ghost, ChevronRightIcon 20)
```

## Computed Styles

### Header row
- 56px tall; flex; justify-content space-between; align-items center; width 100%.

### Title + pill
- h2: hr-title-md (20/700/32px) #121418.
- Pill: font 14px/500; color #1142AF; background #F6F6FF; padding 4px 12px; border-radius 100px; line-height 20px.
- Subtitle: 14px/400/20px; color #63646F; margin 0.

### Know More
- font 14px/500; color #2358DB; background transparent; padding 0; height auto; border-radius 4px; text-decoration none; cursor pointer.

### Track
- display flex; transition transform 0.45s cubic-bezier(0.2, 0.7, 0.2, 1); will-change transform.
- transform: translateX(calc(-1 * var(--page) * 100%)).

### Page
- flex: 0 0 100%; display grid; gap 16px; align-items stretch; grid-template-columns repeat(4,1fr) [@≤1280: repeat(3,1fr); @≤768: repeat(2,1fr); @≤650: repeat(1,1fr)].

### Pagination buttons
- 40x40; border-radius 8px; background transparent; display inline-flex; align-items center; justify-content center; cursor pointer; border none (ghost).
- Prev when page 0: disabled, icon color #9091A8. Enabled: icon #121418, hover background #FFFFFF.

### Dots
- inactive: 8x8 #C1C2D6 radius 9999px border none. Active: width 24px, background #18A149.
- transition: width .3s ease, background .3s ease.

## States & Behaviors

### Carousel paging
- **Trigger:** click prev/next button or dot. Buttons disabled at boundaries (prev disabled on page 0, next disabled on last page).
- Page count recomputed on resize: ceil(totalCards / columnsPerViewport). Breakpoints: >1280: 4, ≤1280: 3, ≤768: 2, ≤650: 1. When page index exceeds new page count after resize, clamp.
- **Implementation:** client component. useState pageIndex, useEffect resize listener (matchMedia or width check). Track transform via inline style translateX(-pageIndex*100%). Cards chunked per page.

## Content (verbatim)
See MockInterviewCard.spec.md (7 cards total).

## Responsive Behavior
- 4-col grid → 3 (@≤1280) → 2 (@≤768) → 1 (@≤650); page count adjusts 2 → 3 → 4 → 7.
- Mobile: title-col flex-direction column (already column) — no change needed; subtitle 14px.
- Pagination stays centered below cards at all widths.