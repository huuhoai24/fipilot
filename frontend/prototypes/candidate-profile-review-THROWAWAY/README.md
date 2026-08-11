# THROWAWAY: Candidate Profile Review prototype

This isolated prototype compares three UI directions for the durable Candidate
Profile Review workspace. It is not imported by the production router, calls no
backend, and uses deterministic local data. Delete the entire
`candidate-profile-review-THROWAWAY` directory after the production design has
been implemented.

## Run

From `frontend`:

```powershell
npm run dev -- --config prototypes/candidate-profile-review-THROWAWAY/vite.config.ts
```

Open:

```text
http://127.0.0.1:4173/prototype/candidate-profile-review/?variant=B&state=ready
```

Use the fixed prototype controls to switch directions and contract states.
Left and right arrow keys also change direction when focus is not in a control.
The query string makes each direction and scenario directly shareable.

## Direction A: Guided Review

- Intended user: first-time candidates who need a clear sequence.
- Information hierarchy: extraction outcome, readiness, five-step progress,
  current section, one forward action.
- UX tradeoff: strongest guidance and lowest immediate complexity, but long
  profiles require more navigation and cross-section comparison is slower.
- Component structure: `GuidedReview` -> `ReadinessSummary` -> `GuidedSteps` ->
  one `ProfileSection` -> `PrimaryWorkflowAction`.
- URL: `?variant=A&state=ready`

## Direction B: Professional Workspace

- Intended user: returning candidates and candidates with long profiles.
- Information hierarchy: workspace purpose, readiness navigation, extraction
  or save state, full Candidate Profile editor, restrained persistent actions.
- UX tradeoff: fastest scanning and correction across sections, but the dense
  desktop layout asks more of first-time users.
- Component structure: `ProfessionalWorkspace` -> `ReadinessRail` plus
  `CandidateProfileEditor` -> ordered `ProfileSection` instances -> `ActionArea`.
- URL: `?variant=B&state=ready`

## Direction C: Progressive Review

- Intended user: candidates who want to focus only on unresolved information.
- Information hierarchy: current outcome, readiness requirements, unresolved
  sections expanded first, completed sections collapsed but available, actions.
- UX tradeoff: reduces cognitive load and page length, but collapsed sections
  make broad profile comparison and reordering less immediate.
- Component structure: `ProgressiveReview` -> `ReadinessSummary` ->
  `ProgressiveSections` using native disclosure controls -> `ActionArea`.
- URL: `?variant=C&state=incomplete`

## Deterministic scenarios

The scenario selector covers accepted complete extraction, Partial Extraction,
incomplete and interview-ready saved profiles, unsaved and saving corrections,
save success, field validation, stale-version conflict, save failure,
replacement upload selection/processing/rejection, temporary upload failure,
authentication required, and legacy/structured education.

No action persists data. Choosing, retrying, saving, and starting an interview
are prototype-only state demonstrations.

## Selected baseline

Direction B is selected as the production design baseline. The rendered
anti-slop review validated these corrections in the prototype:

- removed card framing from the desktop readiness and upload rail;
- replaced rounded nested-entry containers with compact divided rows;
- removed repeated `Back to top` links where the readiness rail already
  provides persistent navigation;
- made text interview the default ready-state primary action while retaining a
  separate speech action;
- reserved space so the throwaway switcher does not obscure workflow actions;
- moved readiness above the editor at 768px and narrower;
- kept Partial Extraction informational and made routine saved confirmation
  quieter;
- kept stale-version recovery visible without discarding local edits or
  repeating its primary action.

Directions A and C remain runnable comparison evidence, but ADR 0012 records why
they are not the production baseline.
