# Header Specification

- **Target file:** `src/components/sites/www.hackerrank.com-407abdb8/dashboard-89347bb2/Header.tsx`
- **Screenshots:** `docs/design-references/www.hackerrank.com-407abdb8/dashboard-89347bb2/desktop-full.png`
- **Interaction model:** click-driven (search dropdown, mobile drawer); no scroll behavior
- **Data types:** `src/components/sites/www.hackerrank.com-407abdb8/shared/types.ts` (none needed)
- **Icons:** `SearchIcon`, `MenuIcon` from `../shared/icons`
- **Logo:** `public/sites/www.hackerrank.com-407abdb8/dashboard-89347bb2/logo-light.svg` (natural 300x33, rendered 129x14 desktop)

## DOM Structure

```
header (60px, bg #121418, border-bottom 2px #1F202A, padding 0 32px desktop / 0 16px @≤768,
        flex justify-between align-center, position static)
├── div.header-nav-links (flex-1? no — natural width)
│   ├── ul (desktop only, flex row, list none, items center)  [hidden @≤768]
│   │   ├── li > a(href /dashboard) > img(logo, alt "HackerRank Home")
│   │   ├── li.sep "|" (color #797888, font 16px, margin 0 20px)
│   │   ├── li > a "Prepare" (ACTIVE: border-bottom 4px #2EC866, weight 700, color #FFF)
│   │   ├── li > a "Certify" (href /skills-verification)
│   │   └── li > a "Compete" (href /contests)
│   └── div.mobile-nav (flex gap 8px align-center, hidden ≥768, position relative)
│       ├── button (40x40, radius 8px, ghost/transparent, white) > MenuIcon size 20
│       ├── a > img(logo, width 124px mobile)
│       └── div.drawer (absolute, top 48px, left -16px, width 100vw, bg #FFF, padding 24px,
│           box-shadow raised, visibility hidden opacity 0 → visible/1, transition all .1s ease-in-out,
│           z-index 999)
│           └── ul (flex col gap 8px)
│               ├── li > a "Prepare" (active: color #121418, font-weight bolder, no border)
│               └── li > a "Certify" / "Compete" (16px, color #35363F, height 60px, hover bg #F7F8FD + color #121418)
└── div.right (flex gap 8px align-center)
    ├── div.search-wrapper (width 200px @1440, 240px base, 180px @≤1440, display none @≤768)
    │   └── div.relative
    │       ├── input type=search placeholder "Search"
    │       ├── SearchIcon (absolute left, 20px, color #9091A8, margin-left 12px)
    │       └── (dropdown when typing, see below)
    ├── button "Log In"
    └── button "Sign Up"
```

## Computed Styles (exact)

### Header
- height: 60px; background: #121418; border-bottom: 2px solid #1F202A; padding: 0 32px (0 16px @≤768); display flex; justify-content: space-between; align-items: center; position: static; font-family Satoshi.

### Nav links (a.NavItem)
- font-size 14px; line-height 60px; height 60px; display inline-block; padding 0 24px (@≤1280: 0 16px; @≤1024: 0 12px); color #FFF; text-decoration none; font-weight 400 (700 when active).
- Active: border-bottom 4px solid #2EC866; font-weight 700; color #FFF.
- Hover: color → #EBEBF3.
- Separator: color #797888; font-size 16px; margin 0 20px.

### Search input
- height 36px; border-radius 8px; border 1px #797888 (hover → #C1C2D6); background #121418; color #FFF; padding 10px 12px 10px 40px; font-size 14px; width 100%. Placeholder color: #9091A8 (neutral-400), 14px.
- Focus: outline 2px solid rgba(18,20,24,.5)-ish; background stays #121418.

### Log In button
- height 40px; border-radius 8px; padding 8px 20px; border 1px solid #63646F; background transparent; color #FFF; font 14px/700; cursor pointer.
- Hover: background → #63646F. Transition: color .2s ease-in-out, backgroundColor .2s ease-in-out, borderColor .2s ease-in-out.

### Sign Up button
- Same metrics; background #20D761; color #121418; border none.
- Hover: background → #BAF3CE. Same transition.

### Search dropdown (rendered when input has focus+value, or on click of search area)
- position absolute; top 52px; width 300px; background #FFF; border-radius 16px; padding 24px; box-shadow: rgba(37,69,105,.1) 0 1px 4px 0, rgba(37,69,105,.1) 0 3px 12px 0; z-index high.
- Section title h3: 16px/700 #121418 ("challenges", "contests", "hackers").
- Rows (flex justify-between align-center, margin-top 8px): link 14px #35363F; contest rows get "ended" pill (12px/500 #121418, bg #EBEBF3, radius 100px, padding 4px 12px).
- Separators between sections: hr 1px solid #63646F, margin-bottom 12px.
- Static demo rows (server content is session-specific):
  - challenges: Say "Hello, World!" With Python (py-hello-world), Python: Division (python-division), Python Evaluation (python-eval), Python If-Else (py-if-else)
  - contests: Pythonista Practice Session [ended], Pythonist [ended], Pythonist 2 [ended], Pythonist 3 [ended]
  - hackers: python, python1231, python1111118881

### Mobile drawer item
- 16px (mobile), color #35363F, height 60px, width 100%; hover: background #F7F8FD, color #121418. Active item: color #121418, font-weight bolder, no border-bottom.

## States & Behaviors

### Search dropdown
- **Trigger:** typing in input (or click on input area). Closes on Escape / outside click.
- Content is static demo data (mock).
- **Implementation:** local state `query`; show dropdown when `focused && query.length > 0`.

### Mobile drawer
- **Trigger:** hamburger click. visibility hidden/opacity 0 → visible/1, transition all .1s ease-in-out.
- Items: Prepare (active), Certify, Compete.

## Text Content (verbatim)
Prepare | Certify | Compete | Search | Log In | Sign Up

## Responsive Behavior
- **Desktop (1440px):** full nav + logo + separator + search (200px) + buttons.
- **≤1280:** nav link padding 0 16px.
- **≤1024:** nav link padding 0 12px; search 180px.
- **≤768:** desktop nav hidden; search hidden; hamburger + logo left (logo 124x14), Log In/Sign Up right; header padding 0 16px; drawer width 100vw.
- Mobile drawer nav item font-size 16px.