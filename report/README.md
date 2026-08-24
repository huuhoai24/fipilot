# FiPilot graduation project report

`Final_report.pdf` is the as-built project report for the connected CV-to-interview application. Its organization follows a conventional graduation-project report while its technical claims are restricted to runtime code and current software verification.

## Build

From the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\report\scripts\build_report.ps1
```

The script renders 13 focused Mermaid diagrams, runs XeLaTeX and Biber, repeats XeLaTeX for references, and checks the log for unresolved references and material overflow.

Create the editable Microsoft Word edition with:

```powershell
powershell -ExecutionPolicy Bypass -File .\report\scripts\export_docx.ps1
```

The Word edition uses native headings, paragraphs, tables, inline images, captions, headers, footers, and an updateable Table of Contents field.

## Layout decisions

- US Letter page geometry follows the supplied thesis example closely.
- Short running headers prevent title/header collisions.
- Figures are placed at up to 94% of text width and 70% of text height.
- A float barrier follows every diagram, preventing diagrams from stacking or overlaying later content.
- Diagram sources use compact top-to-bottom layouts and high-resolution rendering so labels remain readable.

## Source structure

- `Final_report.tex`: document entry point.
- `frontmatter.tex`: abstract, acknowledgments, and abbreviations.
- `chapters/`: nine report chapters.
- `appendices/runtime_appendices.tex`: canonical contracts and source index.
- `diagrams/`: Mermaid sources for connected runtime flows.
- `figures/`: generated image assets.
- `references.bib`: cited primary publications and standards.
