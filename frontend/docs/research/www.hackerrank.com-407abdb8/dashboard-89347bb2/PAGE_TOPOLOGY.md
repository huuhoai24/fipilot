# PAGE_TOPOLOGY.md — hackerrank.com/dashboard

Site: www.hackerrank.com | Page: /dashboard | Viewport basis: 1440x900 desktop

## Page structure (top to bottom)

```
body (bg #fff, Satoshi)
└── header.AppHeader (60px, bg #121418, border-bottom 2px #1F202A, padding 0 32px, flex justify-between align-center)
│   ├── .header-nav-links (desktop: logo + | + Prepare/Certify/Compete)
│   │   ├── ul.NavLinks_desktopOnly (flex, list)
│   │   │   ├── li > a > img(logo-light.svg, 129x14)
│   │   │   ├── li.NavLinks_navSeparator "|" (#797888, margin 0 20px)
│   │   │   ├── li > a.NavItem "Prepare" (ACTIVE: border-bottom 4px #2EC866, 700)
│   │   │   ├── li > a.NavItem "Certify"
│   │   │   └── li > a.NavItem "Compete"
│   │   └── .NavLinks_mobileOnly (hamburger + logo + absolute drawer; hidden ≥768px)
│   └── right cluster (flex gap 8px)
│       ├── .NavGlobalSearch_searchWrapper (200px) input type=search placeholder "Search" + SearchIcon
│       ├── button "Log In" (secondary: transparent, border 1px #63646F, white)
│       └── button "Sign Up" (primary: bg #20D761, text #121418)
├── main content .ContentWrapper (min-height calc(100vh - 60px))
│   └── .hr-container (max-width 1312px, margin auto, padding 0 20px)
│       └── .Dashboard_dashboardContainer (flex col, gap 64px, margin 48px 0)
│           ├── SECTION 1: Mock Interviews (418px tall)
│           │   ├── header row (56px, flex space-between)
│           │   │   ├── left col: h2 "AI-powered Mock Interviews" (20/700) + "New" pill (#F6F6FF/#1142AF) + p subtitle (14px #63646F)
│           │   │   └── a "Know More" (text button, 14/500 #2358DB)
│           │   ├── carousel viewport (overflow hidden)
│           │   │   └── .track (flex, translateX 0 → -pageWidth, transition .45s cubic-bezier(.2,.7,.2,1))
│           │   │       ├── page 1: grid 4 cards (306x274): Technical Screen, Coding, System Design, AI Fluency
│           │   │       └── page 2: grid 3 cards: Behavioral, Frontend - React JS, Backend - Node JS
│           │   └── pagination row (40px, centered, gap 16px)
│           │       ├── button prev (40x40 ghost chevron-left, disabled when page 1: #9091A8)
│           │       ├── dots: active 24x8 #18A149 / inactive 8x8 #C1C2D6 (transition width .3s, background .3s)
│           │       └── button next (40x40 ghost chevron-right, enabled: #121418, hover bg #fff)
│           └── SECTION 2: Practice Skills (464px tall)
│               ├── h2 "Practice Skills" (20/700)
│               └── .Topics_topics (grid 4 cols, gap 16px)
│                   └── 15 tiles (306x88, bg #F7F8FD, radius 16px, padding 32px, flex gap 8px)
│                       ├── img icon 24x24
│                       └── span 16/700
└── footer.AppFooter (margin 64px auto 32px, width fit-content, bg #F7F8FD, radius 8px, padding 16px 20px, flex gap 16px wrap)
    └── 7 links: Environment, FAQ, About Us, Helpdesk, Careers, Terms Of Service, Privacy Policy (14/500 #2358DB, hover underline offset 4px)
```

## Sections

| # | Name | Interaction model | Fixed/sticky |
|---|------|-------------------|--------------|
| 0 | Header | click-driven (search dropdown, mobile drawer) | static (no sticky) |
| 1 | Mock Interviews | click-driven carousel (prev/next/dots), 2 pages desktop | static |
| 2 | Practice Skills | hover-only tiles, links | static |
| 3 | Footer | hover-only links | static |

## Card anatomy (MockInterviewCard)
- wrapper grid item (306x274) → inner card (flex col, space-between, padding 32px, radius 16px, border 1px #EBEBF3, bg linear-gradient(90deg, rgba(174,254,187,.2), transparent))
- top block: h2 (20/700/32px #121418), p desc (14/400/20px #63646F, max-width), duration pill (flex, gap 4px, padding 4px 12px, radius 9999px, bg rgba(18,20,24,.05)): ClockIcon 16px + span 14px #63646F
- bottom: lock button (40x40, border 1px #9091A8, radius 8px, LockIcon 20px #121418)

## Breakpoints
- Topics grid: 4 → 3 (@≤1280) → 2 (@≤1024) → 1 (@≤650)
- Header padding: 32px → 16px (@≤768 via 2rem/1rem rules at ≤1440/≤1024)
- Desktop nav / search: hidden @≤768 (mobile drawer shown <768)
- Carousel page size: 4 cards (desktop) → 3 (@≤1280) → 2 (@≤768ish) → 1 (@≤650)
- Footer margin-bottom 0 @mobile; wraps to full width