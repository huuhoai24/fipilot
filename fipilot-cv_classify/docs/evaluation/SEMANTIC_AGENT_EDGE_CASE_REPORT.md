# Semantic Agent Edge-Case Report

## Summary

- Date: 2026-08-24
- Scope: Resume → Profile → Readiness → Planner → QGen → Evaluator → Report
- Designed/executed: 72/72 (67 deterministic adversarial cases, 5 live Azure representative cases)
- Result: **39 PASS, 30 FAIL, 3 PARTIAL, 0 BLOCKED**
- Severity: **1 Critical, 28 High, 3 Medium, 1 Low**
- Production code changed: **NO**
- Focused existing regressions: `test_interview_planner.py` + `test_interview_engine.py` **41/41 PASS**

Deterministic QGen failures inject a schema-valid but semantically unsupported model output and verify whether the backend accepts it. They demonstrate an absent system guardrail, not that Azure emits that bad output on every call. All five live representative outputs were grounded.

### Real-CV baseline

| Attribute | Baseline |
|---|---|
| Source | Persisted extraction of `backend/test/CV_hoainh.pdf` |
| Canonical profile keys | `skills`, `workExperience`, `roleMatches` |
| Role | AI Engineer (FACT from role evidence) |
| Level | Intern (requested and supported) |
| Years | UNKNOWN — no canonical years field |
| Experience | 1 Work + 3 Project entries |
| Skills | 31 normalized entries |
| Education | MISSING from runtime extraction contract |
| Plan | 4 grounded rounds; AI Engineer / Intern / easy |
| Existing passed real-E2E question | Grounded project/pipeline implementation question; no duplicate |
| Existing passed evaluation | raw 7/10 → validated 8/10, consistent evidence |
| Existing passed report | 7/10, consistent with evaluated turn |

## Highest-risk findings

1. **STATE-S005 — CRITICAL:** question/session APIs accept caller-supplied `resume_id` and `work_experience` without resolving or checking the latest persisted profile. A stale V1 payload can therefore start a new session after V2 removed an old claim.
2. **QGen semantic acceptance — HIGH:** output validation covers schema and duplicates, but not ownership, production scope, role, seniority, metrics, or candidate-vs-JD/KB provenance.
3. **Evaluator scope grounding — HIGH:** grounding is topic-based. If the topic exists in a project, denial of an unsupported qualifier such as production use, real ownership, or proficiency can still be scored as failure.
4. **Reporter rationale — HIGH:** exact quote/timestamp and score are validated, but the rationale is not checked for entailment. Unsupported tenure, employment, role, or removed skills can remain in per-turn rationale.
5. **Profile data loss — HIGH:** skills/proficiency and education do not reach interview setup; years and education are not represented by the active backend profile contract.

## Detailed Results

| ID | Agent | Status | Severity | Failure type | Key evidence |
|---|---|---:|---:|---|---|
| EXP-001 | Planner | PASS | - | - | Work removed; 3 Project rounds remain. |
| EXP-002 | Planner | PASS | - | - | Internship removed; 3 Project rounds remain. |
| EXP-003 | Planner | PASS | - | - | Converted entry is traced as `Project evidence`. |
| EXP-004 | Planner | PASS | - | - | Missing company/name does not erase title/description evidence. |
| EXP-005 | Planner | PASS | - | - | Project stays interviewable without inventing a team. |
| YEAR-001 | Planner | PASS | - | - | Explicit 5 years supports Senior. |
| YEAR-002 | Planner | PASS | - | - | Numeric years removed; Senior is reduced to Junior. |
| YEAR-003 | Planner | PASS | - | - | Explicit 3 years supports Middle. |
| YEAR-004 | Planner | PASS | - | - | Explicit 1 year does not support Senior. |
| YEAR-005 | Planner | PARTIAL | MEDIUM | CONFLICT_SUPPRESSION | Effective level is Junior, but CV 2 years vs JD 4+ has no explicit conflict signal. |
| YEAR-006 | Planner | PASS | - | - | “Over 2 years” is not rounded up to 3. |
| ROLE-001 | Role inference | FAIL | HIGH | ROLE_CONFUSION | Backend title dominates strongly Frontend task evidence. |
| ROLE-002 | Role inference | FAIL | HIGH | ROLE_CONFUSION | Data Engineer title dominates AI/model task evidence. |
| ROLE-003 | Role inference | PASS | - | - | Mixed frontend/backend evidence remains Full Stack. |
| ROLE-004 | Planner | PASS | - | - | JD-only Data role is an explicit mismatch; round remains Web evidence. |
| SKILL-001 | Profile propagation | PARTIAL | MEDIUM | DATA_LOSS | Skill list changed, but Planner input has no skills; project text may still preserve the concept. |
| SKILL-002 | Profile propagation | FAIL | HIGH | DATA_LOSS | “Familiar with” proficiency never reaches Planner/QGen. |
| SKILL-003 | QGen | FAIL | HIGH | QGEN_GROUNDING_FAILURE | Schema-valid question about a JD/KB-only skill is accepted. |
| SKILL-004 | Role inference | PASS | - | - | NFKC width/case variants preserve the same role share. |
| SKILL-005 | Role inference | PASS | - | - | Duplicate case variants do not change role evidence. |
| SKILL-006 | Planner | PASS | - | - | Niche resume evidence remains usable with zero KB hits. |
| PROJ-001 | Planner | PASS | - | - | Removed flagship project disappears from rounds. |
| PROJ-002 | Planner | PASS | - | - | Replacement business project becomes the selected topic. |
| PROJ-003 | QGen | FAIL | HIGH | QGEN_GROUNDING_FAILURE | Unsupported 99.9% metric survives final acceptance. |
| PROJ-004 | Planner | FAIL | HIGH | ROLE_CONFUSION | Ambiguous typo/no role evidence adopts requested Data Engineer as fact. |
| PROJ-005 | Planner | PASS | - | - | Legacy technology is kept as evidence without being modernized. |
| EDU-001 | Profile→Planner | FAIL | HIGH | DATA_LOSS | Education-only fresher evidence has no backend Planner seam. |
| EDU-002 | Profile→Planner | FAIL | MEDIUM | CONFLICT_SUPPRESSION | Education/work direction conflict is dropped. |
| EDU-003 | Profile→Report | PARTIAL | LOW | DATA_LOSS | GPA is not invented, but education is absent from all agents. |
| NULL-001 | Planner | PASS | - | - | Null position uses name/description without crash. |
| NULL-002 | Planner | PASS | - | - | Null company/name uses title/description without crash. |
| NULL-003 | Planner | PASS | - | - | Empty description produces bounded title-only round, no KB. |
| NULL-004 | Planner | PASS | - | - | String years cause no crash and no seniority invention. |
| QGEN-S001 | QGen | FAIL | HIGH | QGEN_GROUNDING_FAILURE | Fresher project → Senior/other-role question accepted. |
| QGEN-S002 | QGen | FAIL | HIGH | QGEN_GROUNDING_FAILURE | Personal project → company production claim accepted. |
| QGEN-S003 | QGen | FAIL | HIGH | QGEN_GROUNDING_FAILURE | Removed CV skill retained through JD output accepted. |
| QGEN-S004 | QGen | FAIL | HIGH | QGEN_GROUNDING_FAILURE | KB-only technology becomes candidate assumption. |
| QGEN-S005 | QGen | FAIL | HIGH | QGEN_GROUNDING_FAILURE | Beginner evidence → distributed-systems depth accepted. |
| QGEN-S006 | QGen | FAIL | HIGH | QGEN_GROUNDING_FAILURE | Frontend CV → backend data-warehouse assumption accepted. |
| QGEN-S007 | QGen | FAIL | HIGH | QGEN_GROUNDING_FAILURE | Prototype → deployed production scope accepted. |
| QGEN-S008 | QGen | FAIL | HIGH | QGEN_GROUNDING_FAILURE | Vague project → invented metrics/architecture accepted. |
| EVAL-S001 | Evaluator | PASS | - | - | Personal-project correction becomes `NOT_ASSESSED`. |
| EVAL-S002 | Evaluator | PASS | - | - | Unsupported leadership denial becomes `NOT_ASSESSED`. |
| EVAL-S003 | Evaluator | PASS | - | - | Unsupported three-year premise becomes `NOT_ASSESSED`. |
| EVAL-S004 | Evaluator | FAIL | HIGH | UNSUPPORTED_ASSUMPTION | Cache is grounded, so “project, not production” is still scored 2/10. |
| EVAL-S005 | Evaluator | FAIL | HIGH | UNSUPPORTED_ASSUMPTION | Familiarity topic is grounded; denial of implementation is scored 2/10. |
| EVAL-S006 | Evaluator | FAIL | HIGH | UNSUPPORTED_ASSUMPTION | Candidate correction of outdated evidence is scored 2/10. |
| EVAL-S007 | Evaluator | PASS | - | - | Mixed-language equivalent answer: raw 2 → validated 8. |
| EVAL-S008 | Evaluator | PASS | - | - | Concise full answer remains 8/10. |
| EVAL-S009 | Evaluator | PASS | - | - | Technically contradictory answer remains 2/10. |
| EVAL-S010 | Evaluator | PASS | - | - | Partial answer remains 5/10 with focused follow-up. |
| REPORT-S001 | Reporter | FAIL | HIGH | REPORT_HALLUCINATION | Unsupported professional-work rationale survives quote validation. |
| REPORT-S002 | Reporter | FAIL | HIGH | REPORT_HALLUCINATION | Unsupported five-year tenure survives in rationale. |
| REPORT-S003 | Reporter | FAIL | HIGH | REPORT_HALLUCINATION | Removed skill can be reintroduced in rationale. |
| REPORT-S004 | Reporter | PASS | - | - | Strong-Hire text is replaced when validated score is low. |
| REPORT-S005 | Reporter | FAIL | HIGH | ROLE_CONFUSION | Target Data role can be restated as actual employment in rationale. |
| STATE-S001 | Planner | PASS | - | - | V2 plan contains Python evidence and no V1 Java evidence. |
| STATE-S002 | QGen | PASS | - | - | Edited Go description reaches the new question prompt. |
| STATE-S003 | QGen | PASS | - | - | Deleted Java evidence is absent from the V2 prompt. |
| STATE-S004 | Planner | PASS | - | - | Removed project is absent from new rounds. |
| STATE-S005 | API/state | FAIL | CRITICAL | STALE_CONTEXT_REUSE | New question APIs trust stale caller `resume_id` + `work_experience`; no latest-profile consistency check. |
| INFER-001 | QGen | FAIL | HIGH | OVER_INFERENCE | “Assisted with X” → sole designer question accepted. |
| INFER-002 | QGen | FAIL | HIGH | OVER_INFERENCE | “Familiar with X” → production implementation question accepted. |
| INFER-003 | QGen | FAIL | HIGH | OVER_INFERENCE | “Learned X” → customer operation question accepted. |
| INFER-004 | QGen | FAIL | HIGH | OVER_INFERENCE | “Prototype using X” → production user-count question accepted. |
| INFER-005 | QGen | FAIL | HIGH | OVER_INFERENCE | “Contributed to X” → sole architect question accepted. |
| INFER-006 | QGen | FAIL | HIGH | OVER_INFERENCE | “Team project” → individual full-ownership question accepted. |
| LIVE-SEM-01 | Live QGen | PASS | - | - | Work removed; question stays on project model design/training. |
| LIVE-SEM-02 | Live QGen | PASS | - | - | Years removed; question uses an extracted project metric, no tenure/seniority. |
| LIVE-SEM-03 | Live QGen | PASS | - | - | JD-only streaming reference ignored; question stays on candidate HTTP API/testing. |
| LIVE-SEM-04 | Live Evaluator | PASS | - | - | Unsupported leadership correction: raw 10 → final 0 `NOT_ASSESSED`. |
| LIVE-SEM-05 | Live QGen | PASS | - | - | V2 question uses Python/SQL; no V1 Java/Kafka evidence. |

## Failure Propagation

| Mutation class | Resume/Profile | Readiness | Planner | QGen | Evaluator | Report | First wrong stage |
|---|---|---|---|---|---|---|---|
| Work/project removal | Preserved | Accepts remaining meaningful project | Correct | Live correct; deterministic bad output not rejected | Correct for broad unsupported premise | Can restore work claim in rationale | Report rationale |
| Numeric years | No canonical field | Not checked | Free-text years handled conservatively | Receives only selected entry text | No tenure-specific grounding | Can restore tenure in rationale | Profile schema |
| Role/task conflict | Preserved in entry | Not checked | Title can dominate tasks | Bad role leap not rejected | Depends on topic string | Can turn target role into fact | Role inference |
| Skill/proficiency | Skill names exist; proficiency absent | Skills do not make interview setup | Skill list dropped | Uses work/project text only | Receives selected project only | No profile supplied | Profile→setup |
| Education | Frontend type permits it; extraction omits it | Not interviewable alone | Not accepted as evidence | Not supplied | Not supplied | Not supplied | Extraction/profile contract |
| JD/KB-only evidence | Kept separate in Planner query | N/A | Mismatch can be explicit | Prompt says “reference only,” but no output validator | Can penalize if topic appears grounded | No provenance check in rationale | QGen acceptance |
| Resume V1→V2 | V2 can be stored | New frontend setup uses V2 | Correct when passed V2 | Correct when passed V2 | Uses question project snapshot | Uses supplied turns | API trusts stale caller payload |

## Stale-State Analysis

- Cross-candidate and cross-session isolation regressions were not reproduced.
- V2 mutations propagate correctly when V2 `work_experience` is actually supplied.
- The dangerous seam is version consistency: backend question endpoints do not resolve `resume_id` to persisted profile data and do not compare the supplied `work_experience` with that resume. Consequently, a stale client cache can revive removed V1 evidence in a new session.
- Existing session setup is intentionally stored per session, so an already-started interview keeps its original setup. The semantic risk is specifically a **new** session carrying stale V1 data after V2 exists.

## QGen Analysis

- Exact/semantic duplicate handling remains outside this failure set and was not regressed.
- Azure complied in all four live QGen representatives.
- The system boundary still accepts any Pydantic-valid, non-duplicate question. It does not verify entailment against candidate evidence or distinguish `FACT`, `INFERENCE`, `UNKNOWN`, `MISSING`, and `CONTRADICTORY` claims.
- Most dangerous transformations: Project→Work, Prototype→Production, Familiarity→Implementation, Contribution→Ownership, JD/KB reference→Candidate fact, and target role→actual experience.

## Evaluator Analysis

- Semantic language equivalence and score guardrail remain effective.
- Broad unsupported-premise denials work when the topic itself is absent from candidate context.
- Scope qualifiers are fragile. Topic matching treats “Cache,” “System design,” or an outdated skill as grounded even when the unsupported assumption is production use, implementation ownership, proficiency, or continued validity.
- Live unsupported leadership correction passed because the topic was absent and the deterministic guardrail changed raw 10 to final 0 `NOT_ASSESSED`.

## Recommended Fix Order

1. Bind new interview setup to a server-resolved persisted resume/profile version; reject stale/inconsistent payloads.
2. Add a small QGen post-validation seam for evidence provenance and scope entailment before final acceptance, preserving retry/dedup behavior.
3. Replace topic-only evaluator grounding with claim-level premise checks for ownership, environment, proficiency, duration, and negation/correction.
4. Validate report rationale claims against the exact answer and frozen question/profile provenance, not only quote presence.
5. Carry canonical skill scope, years, and education evidence through Profile → Readiness → Planner while preserving unknown/missing states.
6. Make role inference evidence-weighted across title and task descriptions, with an explicit ambiguous/conflict state.

## Evidence Files

- `evaluation/agent_robustness/semantic_edge_results.json`
- `evaluation/agent_robustness/semantic_edge_live_results.json`
- `evaluation/agent_robustness/run_semantic_edge_evaluation.py`
