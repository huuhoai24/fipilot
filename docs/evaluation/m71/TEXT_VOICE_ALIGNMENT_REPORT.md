# M7.1 Text/Voice Production Seam Audit

## Exact field-by-field comparison

| Field | Text | Voice | Same? |
| --- | --- | --- | --- |
| Candidate Profile | Canonical `CandidateProfile` | Same object shape | Yes |
| Interview Question / expected points | Canonical `InterviewQuestion` | Same object shape | Yes |
| Candidate answer | Text | Identical text in M7/M7.1 experiment | Yes |
| Interview Config context | `mode=text` | `mode=voice` | No |
| System instruction | `EVALUATOR_SYSTEM_INSTRUCTION` | Same | Yes |
| User/core prompt | Generic four-criterion rubric | Same plus Voice brevity block | No |
| Score scale | Pydantic 0.0–10.0 | Same | Yes |
| Score anchors | None | None | Yes, both absent |
| Critical-error rule | None | None | Yes, both absent |
| Feedback schema | `AnswerEvaluation` | Same | Yes |
| Model route | `gemini-2.5-pro` (`complex`) | `gemini-2.5-flash` (`simple`) | No |
| Temperature | 0.1 | 0.1 | Yes |
| Thinking | Provider default (`None`) | Disabled (`0`) | No |
| Retry | Vertex service, max 3 | Same | Yes |
| Parsing | `generate_json` + Pydantic | Same | Yes |
| Production post-processing | None | None | Yes |
| M7 reporting tier mapping | <=2.5/<=5/<=7.5/>7.5 | Same | Yes |

## Conclusion

Text and Voice are **not actually evaluating the same thing under the same evaluator configuration**. Input text and schema match, but prompt wording, mode context, model route, and thinking differ. M7.1 will test a shared rubric/core first while preserving model cost/latency differences; a same-model option is conditional on the predeclared budget.

