# Select the Professional Candidate Profile workspace

Direction B, Professional Workspace, is the production design baseline for
Candidate Profile Review. At desktop widths it uses a compact two-column layout:
a narrow Interview Readiness and section-navigation rail beside one continuous
Candidate Profile editor. Readiness issues link directly to affected fields, and
a restrained persistent action area keeps profile persistence separate from text
and speech interview starts. At 768px and below, readiness moves above the
single-column editor and the action area returns to normal document flow.

The prototype validated a flat, information-led treatment: section dividers
instead of a card per section, compact repeatable-entry rows, restrained heading
sizes, no decorative icons, and no routine success banner competing with the
editor. Partial Extraction is an informational warning. `Save corrections` is
primary only while changes are unsaved; both interview actions remain visible
but disabled until the save succeeds. In the default text-entry context,
`Start text interview` is primary and speech remains a separate secondary
action. A stale-version conflict remains visible with local edits intact and
offers `Reload latest profile` as its single primary recovery action.

Direction A, Guided Review, is rejected as the production baseline because its
step-by-step navigation makes long profiles and cross-section correction slower.
Direction C, Progressive Review, is rejected because collapsing saved sections
reduces whole-profile scanability and makes returning-user review less direct.
Both remain useful prototype evidence but do not define production structure.

The throwaway evidence is under
`frontend/prototypes/candidate-profile-review-THROWAWAY/` and is not a production
route or API implementation.
