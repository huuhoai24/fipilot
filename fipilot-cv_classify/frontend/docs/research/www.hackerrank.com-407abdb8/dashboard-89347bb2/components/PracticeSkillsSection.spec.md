# PracticeSkillsSection Specification

- **Target file:** `src/components/sites/www.hackerrank.com-407abdb8/dashboard-89347bb2/PracticeSkillsSection.tsx`
- **Screenshots:** `docs/design-references/www.hackerrank.com-407abdb8/dashboard-89347bb2/desktop-full.png`
- **Interaction model:** hover-only tiles (each navigates to its domain page)
- **Icons/assets:** topic SVGs from `public/sites/www.hackerrank.com-407abdb8/dashboard-89347bb2/icons/<Name>.svg`

## DOM Structure

```
section (width 100%)
├── h2 "Practice Skills" (hr-title-md: 20px/700/32px #121418, margin 0)
└── div.grid (display grid; grid-template-columns repeat(4,1fr); gap 16px; width 100%)
    └── 15 × div.tile (306x88 @4col; flex align-center gap 8px; padding 32px;
            border-radius 16px; background #F7F8FD; cursor pointer; transition all;
            hover background #EBEBF3)
        ├── img (24x24, alt "", src /sites/.../icons/<Name>.svg)
        └── span (hr-title-sm: 16px/700/24px #121418)   ← topic name
```

## Computed Styles

### Grid
- display grid; grid-template-columns repeat(4,1fr); gap 16px; width 100%.
- @≤1280: repeat(3,1fr) · @≤1024: repeat(2,1fr) · @≤650: 1fr.

### Tile
- border-radius 16px; background #F7F8FD; padding 32px; display flex; align-items center; gap 8px; cursor pointer; box-sizing border-box; height 88px; border none; transition all.
- Hover: background → #EBEBF3.
- No box-shadow.

### Icon
- 24x24; display block; object-fit fill (SVG).

### Label
- 16px/700/24px; color #121418.

## Content (verbatim) — name → icon file → href
| Name | Icon file | href |
|---|---|---|
| Algorithms | Algorithm.svg | /domains/algorithms |
| Data Structures | DataStructure.svg | /domains/data-structures |
| Mathematics | Mathematics.svg | /domains/mathematics |
| Artificial Intelligence | AI.svg | /domains/artificial-intelligence |
| C | C.svg | /domains/c |
| C++ | C++.svg | /domains/cpp |
| Java | Java.svg | /domains/java |
| Python | Python.svg | /domains/python |
| Ruby | Ruby.svg | /domains/ruby |
| SQL | SQL.svg | /domains/sql |
| Databases | DataBase.svg | /domains/databases |
| Linux Shell | LinuxShell.svg | /domains/shell |
| Functional Programming | FunctionalProgramming.svg | /domains/functions |
| Regex | regex.svg | /domains/regex |
| React | react.svg | /domains/react |

Icon base URL (through Next Image or plain img): `/sites/www.hackerrank.com-407abdb8/dashboard-89347bb2/icons/<file>`. Use plain `<img>` with width/height 24 (SVGs).

## States & Behaviors
- Hover: background #F7F8FD → #EBEBF3, transition all.
- Click: navigate to href (use <a> wrapper or onClick router.push).

## Responsive Behavior
- 4 cols → 3 (@≤1280) → 2 (@≤1024) → 1 (@≤650). Tile height 88px constant; padding 32px constant.
- At 1 col tiles stretch full width (350px @390 viewport).