# M0 Interview Data Flow

## Active end-to-end flow

```text
UploadFile
  -> temporary PDF/DOCX + SHA-256
  -> extracted Resume text
  -> ResumeExtractionResult
  -> CandidateProfile / PersistedCandidateProfile
  -> retrieved planner context strings
  -> InterviewPlan
  -> InterviewQuestion / InterviewTurn
  -> InterviewSessionState persisted in session.state_payload
  -> candidate answer (or STT final transcript)
  -> AnswerEvaluation
  -> deterministic decision + next/follow-up InterviewTurn
  -> completed InterviewSessionState
  -> InterviewReport
```

This is in-process orchestration. `orchestrator/workflow.py` explicitly states
that LangGraph is not used.

## Upload and profile creation

| Arrow | Object/schema | Source | Destination |
| --- | --- | --- | --- |
| Browser → API | Multipart `UploadFile` | Frontend `uploadResume`; `POST /api/v2/resume/upload` | `gateway.api.resume.upload_resume` |
| API → parser | Temporary path + original filename | `upload_resume` | `DocumentService.extract_text` |
| Parser → API | Plain `str` | `extract_pdf_text_direct` or `extract_docx_text_direct` | 50-character gate and extraction cache |
| API → extractor | `resume_text: str` | Cache/artifact miss in `upload_resume` | `ResumeAgent.extract_profile` |
| Extractor → Gemini | Prompt containing JSON-encoded `resume_text[:12000]` + `ResumeExtractionResult` JSON schema | `build_resume_extraction_prompt`; `VertexGeminiService.generate_json` | Vertex AI `gemini-2.5-flash-lite` |
| Gemini → extractor | Validated `ResumeExtractionResult` | Provider JSON + Pydantic | `ResumeExtractionResult.to_candidate_profile` |
| Extractor → repository | `CandidateProfile` | `ResumeAgent` | `create_candidate`, raw text save, profile save, cache/artifact save |
| Repository → client | `candidate_id`, persisted profile, confidence | SQLite or Firestore repository | Upload JSON response |

The cache key is SHA-256 of extraction version, authenticated user ID, and file
content hash. The in-memory cache lasts one hour; the repository extraction
artifact has no expiry in this route. A cache hit still creates a new Candidate
resource and saves the same extracted profile.

## Profile read

`GET /api/v2/candidates/{candidate_id}/profile` performs an owned repository
lookup, returns `CandidateProfileReadResponse`, computes
`InterviewReadiness` with `evaluate_interview_readiness`, and sets a strong
ETag from `profile_version`.

There is no active Profile PATCH or Replacement Upload route, so the documented
review/correction flow does not continue beyond GET in the backend.

## Interview preparation and start

| Arrow | Object/schema | Source | Destination |
| --- | --- | --- | --- |
| Client → prepare/start | `InterviewStartRequest(candidate_id, interview_config)` | `/api/v2/interview/prepare` or `/start` | Owned profile lookup |
| Profile → cache key | `PersistedCandidateProfile`, config, user ID | `InterviewPreparationCache.key_for` | In-memory/persistent blueprint cache |
| Profile → retriever | `CandidateProfile`, `InterviewConfig` | `InterviewPlannerAgent.create_plan` | Active `LocalKnowledgeRetriever.retrieve_topics` |
| Retriever → planner prompt | Ordered `list[str]` | Domain, level guidance, up to 8 topic strings | `build_interview_planner_prompt` as `curated_knowledge` |
| Planner prompt → Gemini | Profile + config + curated context + `InterviewPlan` schema | `InterviewPlannerAgent` | Vertex `gemini-2.5-flash` |
| Gemini → blueprint | `InterviewPlan` | Pydantic validation | Memory cache + repository blueprint artifact |
| Plan round → question model | Profile + first `InterviewRound` + config | `InterviewOrchestrator.start_interview` | `QuestionGeneratorAgent.generate_question` |
| Question model → state | `InterviewQuestion` | Vertex `gemini-2.5-flash` | `InterviewTurn` inside `InterviewSessionState` |
| State → repository | JSON-serialized `InterviewSessionState` | `start_interview` route | Session `state_payload` plus turn record |

For text mode, `begin_text_conversation` temporarily makes a deterministic
introduction the current turn and preserves the generated technical question as
`pending_turn`. For voice mode the generated question remains current.

The state contains a copy of the profile, but the start route does not invoke
the shared readiness validator and repository creation is not an atomic
profile-version snapshot transaction.

## Text answer loop

1. `POST /api/v2/interview/{session_id}/answer` loads and validates
   `InterviewSessionState` from the owned session.
2. If phase is `opening`, `answer_opening` records the introduction and reveals
   the already generated pending question; no evaluator is called.
3. Otherwise `InterviewOrchestrator.submit_answer` copies the answer into the
   current `InterviewTurn`.
4. For a normal text next-topic branch, the next question may be speculatively
   generated concurrently while the current answer is evaluated.
5. `EvaluatorAgent.evaluate_answer` sends profile + question + expected points
   + answer + config to Gemini Pro and returns `AnswerEvaluation`.
6. `InterviewDecisionService.decide` chooses:

   - `follow_up` when the model sets `follow_up_needed`;
   - `increase_difficulty` at overall score ≥ 8;
   - otherwise `next_question`.

7. Follow-up uses an existing probe if available. Voice ranks probes by lexical
   overlap with weaknesses/missing concepts; text uses the first remaining
   probe. If none remains, the normal Question Generator is called with memory
   and “do not ask again” directions.
8. The updated state and current turn are persisted. When question count or
   plan rounds are exhausted, `current_turn` becomes null and status becomes
   completed.

## Voice answer loop

```text
Browser PCM16 frames
  -> WebSocket /api/v2/voice/interview/{session_id}
  -> bounded audio queue
  -> Silero VAD speech boundaries
  -> faster-whisper partial/final TranscriptEvent
  -> reviewed/confirmed transcript string
  -> VoiceAnswerSubmissionService
  -> the same InterviewOrchestrator/Evaluator path
  -> streamed next-question JSON text
  -> question deltas + sentence/phrase chunks
  -> VieNeu TTS
  -> 24 kHz PCM frames to browser
```

With `SPEECH_SERVICE_URL` configured, gateway speech calls go over a private
WebSocket to `speech_service.main`. Without it, the same faster-whisper,
Silero, and VieNeu adapters are constructed in the gateway process. This is a
configuration choice, not an automatic runtime fallback: failure of the remote
service does not switch to embedded models.

The voice evaluator uses Flash with thinking disabled. The next question uses
the streaming Flash path. If the streamed JSON metadata is invalid after the
candidate has heard the question, the application retains the spoken text and
rebuilds topic/difficulty/expected points from the selected round.

## Report flow

| Arrow | Object/schema | Source | Destination |
| --- | --- | --- | --- |
| Client → report service | Owned completed `session_id` | `POST /api/v2/interview/{session_id}/report` | `ReportService.generate_for_session` |
| Repository → service | `InterviewSessionRecord` + parsed `InterviewSessionState` | `get_session` | Completion/current-turn checks |
| Repository → generator | **Current** `PersistedCandidateProfile` + stored state | `get_candidate_profile(session.candidate_id)` | `ReportGeneratorAgent.generate_report` |
| Generator → Gemini | Profile, config, plan, all completed turns/evaluations | `build_report_prompt` | Vertex `gemini-2.5-pro` |
| Gemini → repository | `InterviewReport` with app-assigned ID/session/time | Pydantic validation | Save report and mark session `report_generated` |

The report service reloads the current Candidate Profile instead of using only
`state.candidate_profile`. This conflicts with the documented immutable
snapshot contract if profile mutation is later implemented.

## Persistence objects

- Candidate/Profile: SQLite `users` row JSON or Firestore candidate document.
- Resume text: stored with the candidate in repository-specific form.
- Extraction artifact: profile JSON keyed by version/user/content fingerprint.
- Interview blueprint: `InterviewPlan` keyed by candidate and preparation key.
- Session: status/config metadata plus serialized `InterviewSessionState`.
- Turn/evaluation: repository records plus copies embedded in session state.
- Report: serialized `InterviewReport` attached to the session/document.

No session field named `candidate_profile_version` exists in the active shared
schema. The profile copy in state is the only snapshot-shaped object.
