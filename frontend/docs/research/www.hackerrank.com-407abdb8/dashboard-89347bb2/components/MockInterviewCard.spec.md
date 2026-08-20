# MockInterviewCard Specification

- **Target file:** `src/components/sites/www.hackerrank.com-407abdb8/dashboard-89347bb2/MockInterviewCard.tsx`
- **Screenshots:** `docs/design-references/www.hackerrank.com-407abdb8/dashboard-89347bb2/desktop-full.png`
- **Interaction model:** static card with hover-only lock button; whole card is clickable (aria button, cursor pointer)
- **Props:** `{ interview: MockInterview }` from `../shared/types` (title, description, duration)
- **Icons:** `ClockIcon`, `LockIcon` from `../shared/icons`

## DOM Structure

```
article/div.card (grid item, width 306px @4-col, height 274px, cursor pointer)
└── div.inner (height 100%, flex column justify-space-between, padding 32px,
              border-radius 16px, border 1px #EBEBF3,
              background linear-gradient(90deg, rgba(174,254,187,.2), transparent))
    ├── div.top (flex column, gap 8px)
    │   ├── h2 (20px/700/32px, #121418)            ← title
    │   ├── p (14px/400/20px, #63646F)             ← description
    │   └── div.duration-pill (flex gap 4px align-center, padding 4px 12px,
    │           border-radius 9999px, background rgba(18,20,24,.05), width fit-content)
    │       ├── ClockIcon (16px, color #63646F)
    │       └── span (14px/400/20px, #63646F)      ← "30 mins"
    └── div.bottom (width fit-content, align-self flex-start)
        └── button.lock-btn (40x40, border 1px #9091A8, border-radius 8px,
                background transparent, display inline-flex center)
            └── LockIcon (20px, color #121418)
```

## Computed Styles

### Card inner
- padding 32px; border-radius 16px; border 1px solid #EBEBF3; background: linear-gradient(90deg, rgba(174,254,187,0.2), transparent); height 100%; display flex; flex-direction column; justify-content space-between; box-sizing border-box.

### Title
- font-family Satoshi; 20px; weight 700; line-height 32px; color #121418; margin 0.

### Description
- 14px; weight 400; line-height 20px; color #63646F; margin 0; max-width 240px.

### Duration pill
- display flex; align-items center; gap 4px; padding 4px 12px; border-radius 9999px; background rgba(18,20,24,0.05); width fit-content.
- ClockIcon 16px color #63646F; span 14px/400/20px color #63646F.

### Lock button
- width/height 40px; border 1px solid #9091A8; border-radius 8px; background transparent; display inline-flex; align-items center; justify-content center; cursor pointer.
- Hover: background → #FBFBFE.
- Transition: color .2s ease-in-out, backgroundColor .2s ease-in-out, borderColor .2s ease-in-out.
- Icon: LockIcon 20px, color #121418 (stroke currentColor).

## States & Behaviors
- Card itself: no visual change on hover (verified).
- Lock button hover: bg transparent → #FBFBFE.
- Card is clickable (navigates to mock interview sign-in in original; in clone, no-op button).

## Content (verbatim, passed via props)
Page 1: Technical Screen / "Practice a recruiter screening to identify gaps in CS fundamentals, role fit, and interview readiness." / 30 mins · Coding / "Solve algorithmic and data structure problems designed to test your problem-solving skills." / 60 mins · System Design / "Improve your ability to design scalable systems and clearly justify architectural decisions." / 60 mins · AI Fluency / "Demonstrate your ability to build with AI and use AI tools to solve problems and improve your workflow." / 30 mins
Page 2: Behavioral / "Practice behavioral questions in a mock setting. Refine your storytelling and STAR method." / 45 mins · Frontend - React JS / "Work on challenges covering React, Javascript, and CSS, testing your core frontend knowledge." / 60 mins · Backend - Node JS / "Work on challenges covering Node.js, JavaScript and Express to test your backend expertise." / 60 mins

## Responsive Behavior
- Width follows grid column (306px @4-col desktop, 296px @3-col, 340px @2-col, 350px @1-col mobile). Height fixed 274px; card padding 32px at all sizes.