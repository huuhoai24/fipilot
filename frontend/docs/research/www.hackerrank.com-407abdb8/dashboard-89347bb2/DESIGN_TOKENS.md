# DESIGN_TOKENS.md — hackerrank.com dashboard (light theme)

## Fonts
- Family: **Satoshi** (self-hosted via cdn.hackerrank.com). Weights used: 400, 500, 700 (+italic variants exist).
- Fallback: "Open Sans", arial, helvetica, sans-serif.
- Typography scale (computed):
  - hr-title-lg: 24px/700/36px
  - hr-title-md: 20px/700/32px
  - hr-title-sm: 16px/700/24px
  - hr-title-xsm: 14px/700/24px
  - hr-body-lg: 16px/400/24px
  - hr-body-md: 14px/400/20px
  - hr-body-sm: 12px/400/20px

## Neutral scale (--hr-neutral-N)
| Token | Value |
|---|---|
| 0 | #fff |
| 25 | #fbfbfe |
| 50 | #f7f8fd |
| 100 | #ebebf3 |
| 200 | #d6d7e4 |
| 300 | #c1c2d6 |
| 400 | #9091a8 |
| 500 | #797888 |
| 600 | #63646f |
| 700 | #4a4b53 |
| 800 | #35363f |
| 900 | #1f202a |
| 950 | #121418 |
| 1000 | #000 |

## Brand (green)
50 #e9fbef · 100 #def9e7 · 200 #baf3ce · 300 #20d761 · 400 #1dc257 · 500 #1aac4e · 600 #18a149 · 700 #13813a · 800 #0e612c · 900 #0b4b22

## Info (blue)
25 #f6f6ff · 50 #eaecff · 100 #d4ddff · 600 #3568ff · 700 #2358db · 800 #1142af

## Semantic light-theme values (verified computed)
- --color-dashboard-card: #F7F8FD (topic tile bg, footer bg)
- --color-dashboard-card-hover: #EBEBF3
- --color-dashboard-card-border: #EBEBF3
- --color-text-label: #63646F (card desc, pill text)
- --color-mi-card-duration-bg: rgba(18,20,24,.05)
- --color-mi-landing-icon: #18A149 (active dot)
- --color-separator-heavy: #C1C2D6 (inactive dot)
- --color-border: #EBEBF3
- --color-nav-item-default: #9091A8; hover #EBEBF3; active #FFF (dark header)
- Active nav underline: #2EC866

## Component recipes (all computed)
- **Page bg**: #FFFFFF; text #121418.
- **Header**: bg #121418; border-bottom 2px #1F202A; height 60px; padding 0 32px (0 16px @≤768).
- **Nav link**: 14px/400 (700 active), color #FFF, padding 0 24px (0 16px @≤1280, 0 12px @≤1024), line-height 60px. Separator "|": 16px #797888, margin 0 20px.
- **Search input**: height 36px; radius 8px; border 1px #797888 (hover #C1C2D6); bg #121418; color #FFF; padding 10px 12px 10px 40px; 14px. Icon 20px #9091A8.
- **Log In btn**: height 40px; padding 8px 20px; radius 8px; border 1px #63646F; transparent bg; white text; 14/700. Hover bg #63646F.
- **Sign Up btn**: bg #20D761; #121418 text; hover bg #BAF3CE. Same metrics.
- **"New" pill**: bg #F6F6FF; color #1142AF; 14/500; padding 4px 12px; radius 100px.
- **Know More link**: 14/500 #2358DB, no underline, radius 4px.
- **Mock card**: padding 32px; radius 16px; border 1px #EBEBF3; bg gradient linear-gradient(90deg, rgba(174,254,187,.2), transparent); title 20/700; desc 14/400 #63646F; pill bg rgba(18,20,24,.05) padding 4px 12px radius 9999px, ClockIcon 16px #63646F, text 14px; lock btn 40x40 border #9091A8 radius 8px.
- **Dots**: 8x8 #C1C2D6 → active 24x8 #18A149.
- **Pagination buttons**: 40x40 radius 8px; chevrons 20px stroke 1.5; disabled #9091A8 / enabled #121418; hover bg #FFF.
- **Topic tile**: padding 32px; radius 16px; bg #F7F8FD; hover #EBEBF3; icon 24x24; text 16/700.
- **Footer**: bg #F7F8FD; radius 8px; padding 16px 20px; margin 64px auto 32px; gap 16px; link 14/500 #2358DB, hover underline offset 4px.
- **Search dropdown**: top 52px; width 300px; bg #FFF; radius 16px; padding 24px; shadow rgba(37,69,105,.1) 0 1px 4px / 0 3px 12px; section titles 16/700; rows 14px #35363F margin-top 8px; pill 12/500 #121418 bg #EBEBF3 radius 100px padding 4px 12px; separator 1px #63646F.

## Spacing (rem, 1rem = 16px)
0.25=.25rem · 0.5=.5rem · 0.75=.75rem · 1=1rem · 1.5=1.5rem · 2=2rem · 3=3rem · 4=4rem · 5=5rem
Radius: 0.25/0.5/0.75/1rem + full 9999px.
Shadow raised: rgba(37,69,105,.1) 0 1px 4px, 0 3px 12px.