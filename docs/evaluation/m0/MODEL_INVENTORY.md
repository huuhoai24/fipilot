# M0 Model Inventory

## Production/runtime models

The table records code defaults and the repository's configured local launch
baseline. LLM calls use Google Vertex AI through `google-genai` and Application
Default Credentials.

| Component | Provider | Exact model | Temperature | Timeout | Retry | Source |
| --- | --- | --- | ---: | ---: | ---: | --- |
| Resume extraction | Vertex AI Gemini | `gemini-2.5-flash-lite` | 0.1 | 60 s | 1 attempt | `core/dependencies.py:101-119`; `profile_scanner/agent.py:20-29` |
| Interview planner | Vertex AI Gemini | `gemini-2.5-flash` | 0.1 | 60 s | 3 attempts | `interview_planner/agent.py:53-62`; `core/settings.py:266` |
| Question generation | Vertex AI Gemini | `gemini-2.5-flash` | 0.2 | 60 s | 3 attempts | `question_generator/agent.py:41-50` |
| Voice question streaming | Vertex AI Gemini | `gemini-2.5-flash` | 0.2 | 60 s for stream | Up to 3 attempts before emission; interrupted emitted stream is not replayed | `question_generator/streaming_service.py:132-156`; `vertex_gemini.py:115-163` |
| Text answer evaluation | Vertex AI Gemini | `gemini-2.5-pro` | 0.1 | 60 s | 3 attempts | `answer_evaluator/agent.py:19-63`; `.env.local`/settings complex route |
| Voice answer evaluation | Vertex AI Gemini | `gemini-2.5-flash` | 0.1 | 60 s | 3 attempts | `answer_evaluator/agent.py:32-63` |
| Final report | Vertex AI Gemini | `gemini-2.5-pro` | 0.1 | 60 s | 3 attempts | `report_generator/agent.py:21-29` |
| Optional query/document embedding | Vertex AI | `gemini-embedding-001`, 768 dimensions | N/A | No application timeout | 3 attempts, 0.5/1.0 s backoff (max 4 s) | `infrastructure/interview_knowledge/firestore_vector.py:18-93`; disabled by local config |
| STT (configured separate speech service) | Local faster-whisper/CTranslate2 | `large-v3-turbo` | N/A | No application inference timeout | None | `backend/.env.speech`; `speech/stt/faster_whisper.py:46-124` |
| STT code default | Local faster-whisper/CTranslate2 | `large-v3` | N/A | None | None | `core/settings.py:92-98` |
| STT container-baked artifact | Local faster-whisper/CTranslate2 | `large-v3` path under `/opt/fipilot/models/` | N/A | None | None | `backend/Dockerfile` |
| Voice activity detection | Silero VAD ONNX | Package-provided Silero VAD model; no versioned model ID in app config | N/A | None | None | `services/voice_session/audio_pipeline.py:68-83` |
| TTS | Local VieNeu | Mode `v3turbo`; package/model artifact not pinned by an exact model ID | N/A | No application synthesis timeout | None | `core/settings.py:124-131`; `speech/tts/vieneu.py:31-154` |

## Shared LLM policy

- Default retry policy: 3 attempts, 0.5 s initial exponential backoff, 4 s cap,
  up to 0.1 s jitter (`vertex_gemini.py:39-44`).
- Retryable conditions: timeout; 408, 409, 429, 500, 502, 503, 504; or common
  transient text markers (`vertex_gemini.py:618-625`).
- Default timeout: 60 seconds (`vertex_gemini.py:55-68`).
- Structured calls request `application/json`, provide a Pydantic JSON schema,
  extract one JSON object, and validate it (`vertex_gemini.py:165-354`).
- There is no provider/model failover. Resume uses an isolated service with
  exactly one attempt.

## Evaluation-only models

| Component | Provider | Model | Temperature | Timeout/retry | Status |
| --- | --- | --- | ---: | --- | --- |
| System evaluation question judge | Vertex AI Gemini | Complex route, currently `gemini-2.5-pro` | 0.0 | Shared 60 s / 3 attempts | Code exists; public manifest contains zero cases |
| RAGAS-style pilot judge | Vertex AI Gemini | `gemini-2.5-flash` | 0.0 | Shared 60 s / 3 attempts | Historical run artifacts at commit `1249cc50…`; synthetic cases |

Evaluation judges are not called by production interview routes.

## Requested provider/type presence

| Type | Status | Evidence |
| --- | --- | --- |
| Gemini | PRESENT | All production LLM agents use Gemini through the shared adapter |
| Vertex AI | PRESENT | Client is created with `vertexai=True` |
| OpenAI-compatible production LLM | **NOT PRESENT** | Only obsolete documentation describes it; no active gateway dependency constructs one |
| Alternate hosted LLM provider | **NOT PRESENT** | No production provider fallback is wired |
| Local general-purpose LLM | **NOT PRESENT** | Local models are speech/VAD only |
| STT | PRESENT | faster-whisper |
| TTS | PRESENT | VieNeu |
| Embedding model | IMPLEMENTED, NOT ACTIVE IN LOCAL BASELINE | Optional `gemini-embedding-001` adapter; `INTERVIEW_KNOWLEDGE_BACKEND=local` |
| Reranker | **NOT PRESENT** | No reranking model or stage |
| Production judge model | **NOT PRESENT** | Judges exist only in evaluation code |

## Configuration caveats

Model identity is not persisted with Candidate Profiles, interview sessions, or
reports. Environment files can override every Gemini/STT/embedding model. The
latest tracked deployment command sets only simple/complex Gemini models and
does not prove which uncommitted vector configuration, if any, is deployed.
