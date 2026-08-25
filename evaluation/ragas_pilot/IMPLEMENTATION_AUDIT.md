# FiPilot RAGAS-Style Pilot Implementation Audit

Audit date: 2026-08-15

Audited Git revision: `1249cc50a6995ac0a72465fdfb2d708d2cde5c1c`

This audit records the production seams that the evaluation pilot exercises.
The pilot is evaluation-only: it must not change production retrieval, prompts,
model routing, schemas, or interview behavior.

## Retrieval implementation

| Property | Audited implementation |
| --- | --- |
| Public seam | `KnowledgeRetriever.retrieve_topics(candidate_profile, interview_config) -> list[str]` |
| Active implementation | `LocalKnowledgeRetriever` from `backend/services/interview_knowledge/local.py` |
| Knowledge source | Packaged `backend/services/interview_knowledge/catalog.json` with 10 domains, domain topic metadata, and level guidance |
| Vector database | None |
| Embedding model | None |
| Retrieval method | Deterministic local lexical retrieval |
| Topic Top-K | 8 topics by default (`topic_limit=8`) |
| Query construction | All string values recursively collected from `CandidateProfile`; tokenized profile text is combined implicitly with `InterviewConfig.experience_level` for level guidance |
| Tokenization | Lowercase regex tokens `[a-z0-9+#.]+`; tokens shorter than two characters and configured stop words are removed |
| Domain selection | Exact domain-label occurrence adds 20; overlap with domain terms adds 3 per token; deterministic score/name sort |
| Topic score | Weighted token overlap: tokens of at least five characters add 3, shorter tokens add 1; exact title occurrence adds 12 |
| Similarity metric | No vector similarity. The lexical score is an internal ranking score and is not returned by the public interface |
| Filtering | The selected domain bounds topic candidates; only positive-scoring topics are returned |
| Output structure | Ordered strings: domain context, optional level guidance, then up to eight candidate-aligned topic strings containing catalog path/title and up to five anchors |

The production interface does not expose a topic ID or similarity score. Pilot
records therefore preserve returned context text and rank, use deterministic
evaluation-local context IDs, and store `similarity: null`. They do not infer a
cosine or embedding similarity value.

The retriever augments interview planning. `InterviewPlannerAgent` passes the
returned strings as `curated_knowledge` in its prompt. Calling this component
"vector RAG" would be inaccurate; the precise description is packaged-catalog
lexical retrieval for retrieval-augmented interview planning.

## Question generation implementation

| Property | Audited implementation |
| --- | --- |
| Public seam | `QuestionGeneratorAgent.generate_question(candidate_profile, interview_round, interview_config)` |
| Candidate input | Canonical `CandidateProfile`: role/specialization, skills, skill evidence, projects, experiences, education, and experience signals |
| Plan input | One selected `InterviewRound`, not the whole `InterviewPlan` |
| Retrieved context input | Not passed directly to the Question Generator. Retrieved context first influences `InterviewPlannerAgent`; the selected round is then passed to Question Generator |
| Role | Derived from Candidate Profile evidence; there is no separate role argument |
| Level and language | `InterviewConfig.experience_level` and `InterviewConfig.language` |
| Prompt requirements | Evidence-grounded question, selected round topic/difficulty, one primary question, technical decisions/trade-offs/debugging, language control |
| Output schema | `InterviewQuestion`: question, language, topic, difficulty, reasoning, expected_answer_points, follow_up_questions |
| Production model | `gemini-2.5-flash` through the simple task route |
| Production temperature | 0.2 |
| Thinking budget | 0 |

For the pilot, the actual planner and actual question generator are called so
that retrieved context is mediated through the same plan seam as production.
The sample log preserves the full synthetic Candidate Profile, retrieved
strings, generated plan, selected round, and generated question.

## Answer evaluation implementation

| Property | Audited implementation |
| --- | --- |
| Public seam | `EvaluatorAgent.evaluate_answer(candidate_profile, interview_question, answer, interview_config)` |
| Main rubric | Question `expected_answer_points`, correctness, technical depth, practical experience, and communication |
| Score range | 0.0-10.0 for overall, technical, communication, and correctness scores |
| Evidence available | Candidate Profile, question, expected points, candidate answer, and interview configuration |
| Output | Scores, strengths, weaknesses, missing topics/concepts, feedback, follow-up decision and reason |
| Text model | Configured complex route: `gemini-2.5-pro` |
| Voice model | Simple route: `gemini-2.5-flash` |
| Production temperature | 0.1 |
| Voice thinking budget | 0; text leaves the provider default thinking configuration |

No verified human-labelled answer benchmark was found. The pilot therefore
does not compute human MAE, agreement, or correlation. It uses a **synthetic
controlled evaluation set** with only ordinal quality intent (weak, partial,
good, strong), never fake human scores.

## LLM infrastructure

| Property | Audited implementation |
| --- | --- |
| Provider/API | Google Vertex AI through `google-genai` and `VertexGeminiService` |
| Authentication | Google Application Default Credentials; available during audit |
| Configured project | Present in ADC/environment; not copied into sample logs |
| Vertex location | `us-central1` |
| Simple model | `gemini-2.5-flash` |
| Complex model | `gemini-2.5-pro` |
| JSON validation | Provider JSON schema plus Pydantic validation |
| Default timeout | 60 seconds |
| Default retry attempts | 3 |
| Retry backoff | Exponential from 0.5 seconds, capped at 4 seconds, with up to 0.1 seconds jitter |
| Retryable classes | Timeout, 408/409/429/500/502/503/504, and common transient markers |

Pilot LLM judges are conceptually separate evaluation components and use the
configured Flash model explicitly with `temperature=0` and a versioned rubric.
The production Question Generator remains Flash/0.2 and the production text
Answer Evaluator remains Pro/0.1.

## Ragas package audit

- Installed: no
- Installed version: not installed
- Official Ragas metric used: none

The pilot must not claim custom metrics are official Ragas metrics. Retrieval
judging is named **RAGAS-inspired context precision without reference** and
stores per-context labels and reasons. Question and Answer Evaluator metrics use
FiPilot-specific rubric schemas because classic answer-generation metrics do
not match their semantics.

## Evaluation design decision

- Run all deterministic retrieval calculations on a synthetic controlled set
  derived from actual catalog metadata.
- Start with 10 end-to-end cases because the smoke pilot requires planner,
  question, answer-evaluator, repeatability, and judge calls.
- Preserve every input, generated output, parsed judgment, reason, latency,
  model, and timestamp in JSONL.
- Do not store secrets, tokens, real Resume text, or user data.
- Do not scale to 30 LLM cases until smoke call count, runtime, failure rate,
  and estimated token cost are reported.

## Primary source files

- `backend/services/interview_knowledge/retriever.py`
- `backend/services/interview_knowledge/local.py`
- `backend/services/interview_knowledge/catalog.json`
- `backend/services/interview_planner/agent.py`
- `backend/services/interview_planner/prompts.py`
- `backend/services/question_generator/agent.py`
- `backend/services/question_generator/prompts.py`
- `backend/services/answer_evaluator/agent.py`
- `backend/services/answer_evaluator/prompts.py`
- `backend/infrastructure/llm/base.py`
- `backend/infrastructure/llm/vertex_gemini.py`
- `backend/core/dependencies.py`
- `backend/core/settings.py`
- `backend/shared/schemas/candidate.py`
- `backend/shared/schemas/interview.py`
- `backend/shared/schemas/evaluation.py`
