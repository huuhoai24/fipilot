# BEHAVIORS.md — hackerrank.com/dashboard

All values from getComputedStyle on the live site (light theme).

## Header
- **Nav item hover** (Certify): color #FFF → #EBEBF3, weight stays 400, no underline. Active "Prepare" stays white/700 with 4px #2EC866 bottom border.
- **Log In hover**: bg transparent → #63646F (text stays white). transition color .2s, backgroundColor .2s, borderColor .2s ease-in-out.
- **Sign Up hover**: bg #20D761 → #BAF3CE (text #121418 stays).
- **Search input hover**: border #797888 → #C1C2D6. Focus: 2px outline (--hr-input-outline-color, neutral-900-ish), border stays.
- **Search dropdown** (typing "python"): absolute panel, top 52px, width 300px, bg white, radius 16px, padding 24px, shadow rgba(37,69,105,.1) 0 1px 4px, rgba(37,69,105,.1) 0 3px 12px. Sections (h3 16/700): "challenges", "contests" (rows have "ended" pill bg #EBEBF3 text #121418 12/500 padding 4px 12px radius 100px), "hackers". Row: link 14px/500? color #35363F, flex, margin-top 8px. Separators: hr 1px bg #63646F. Content is server-generated per session → clone uses static mock rows.
- **Mobile hamburger** (<768px): ghost button 40x40 radius 8px, MenuIcon (3 lines). Drawer: absolute top 48px, width 100vw, bg white, padding 24px, shadow raised, transition all .1s ease-in-out, visibility hidden/opacity 0 → visible/1. Items Prepare (active: no bottom border, #121418 bolder), Certify, Compete — links 16px, color #35363F, height 60px, hover bg #F7F8FD + text #121418.
- Header NOT sticky (position static).

## Mock Interviews carousel
- **Track**: transform matrix → translateX(-pageWidth) per page. transition transform .45s cubic-bezier(.2,.7,.2,1).
- **Dots**: active 24x8 bg #18A149; inactive 8x8 bg #C1C2D6. transition width .3s ease, background .3s ease. Also clickable (aria-label "Go to mock interviews page N").
- **Prev/Next buttons**: 40x40 radius 8px. Prev disabled on page 1 → icon color #9091A8. Next enabled → icon #121418, hover bg #FFFFFF.
- Pages: desktop 2 pages (4+3 cards), @≤1280 3 cards/page, ≤768 2/page, ≤650 1/page (7 pages mobile).

## Mock Interview Card
- Hover: card transition all; no visible style change on card body (verified), arrow/lock button hover: bg #FBFBFE (neutral-25).
- Lock button: border 1px #9091A8, radius 8px, icon LockIcon 20px #121418, transition color/backgroundColor/borderColor .2s.

## Practice Skills tiles
- Hover: bg #F7F8FD → #EBEBF3, transition all (no explicit duration).
- Icons: 15 SVGs 24x24 (Algorithm, DataStructure, Mathematics, AI, C, C++, Java, Python, Ruby, SQL, DataBase, LinuxShell, FunctionalProgramming, regex, react) — from hrcdn.net, downloaded to page asset root.

## Footer
- Link hover: textDecoration none → underline, underline-offset 4px, color stays #2358DB.
- Layout: margin 64px auto 32px desktop → 64px 0 0 mobile; wraps.

## Page-level
- No scroll-snap, no Lenis/Locomotive, no parallax, no scroll-triggered header change.
- No autoplay carousel; dots reflect current page only.
- Body: white bg, #121418 text, Satoshi.
- Scrollbar: default.

## Session-specific content (mock in clone)
- Search results are user-scoped → static sample rows.
- Sign-up modal may auto-open for anon users → NOT cloned (page-level modal, out of static scope).