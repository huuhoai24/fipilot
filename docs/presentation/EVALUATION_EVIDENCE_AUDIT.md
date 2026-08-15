# Evaluation Evidence Audit

Audit date: 2026-08-14
Scope: the current working tree, ignored local project artifacts, and all locally
available Git history/branches. Dependency-package sample data was inventoried
only to exclude it from FiPilot evidence.

Audited revision: `51fc3b57` on branch `restore/first-deploy-frontend`.

## Presentation claim gate

This section is the controlling evidence gate for slide editing. “Not found”
means not found in the active source, first-party dependency manifests, tracked
deployment evidence, or the additional working-tree/history searches recorded
below. It is a scoped repository finding, not a proof about every untracked
machine, external service, or future revision.

| Required claim | Verdict for slides | Primary repository evidence |
| --- | --- | --- |
| No LangGraph | **Supported for the active application.** Describe the workflow as an in-process orchestrator, not a LangGraph graph. | The active workflow boundary says the project intentionally does not use LangGraph and exports `InterviewOrchestrator` (`backend/orchestrator/workflow.py:1-9`). The similarly named graph-state schemas are explicitly compatibility contracts, while `orchestrator.state` is active (`backend/shared/schemas/graph_state.py:1-5`). `backend/app/graph/__init__.py:1` is a placeholder, not an implementation. |
| No vector DB / embeddings | **Supported as a scoped implementation finding.** Do not put a vector store, embedding model, semantic search, or semantic reranker in the architecture. | The active retriever reads packaged JSON into memory (`backend/services/interview_knowledge/local.py:82-86`) and scores token overlap (`backend/services/interview_knowledge/local.py:106-121`). The active backend dependency list contains Firestore but no embedding/vector client (`backend/requirements.txt:1-13`). The negative source/dependency search is documented below. |
| Lexical retrieval only | **Supported.** Call it deterministic local lexical retrieval, bounded to eight topics by default. Do not call the implemented mechanism vector RAG or semantic retrieval. | Tokens are produced by a regular expression and stop-word filtering (`backend/services/interview_knowledge/local.py:40-61`); domain selection uses label matches and token-set intersection (`backend/services/interview_knowledge/local.py:130-142`); topic ranking uses weighted token overlap, an exact-title bonus, deterministic sorting, and `topic_limit` (`backend/services/interview_knowledge/local.py:82-85`, `106-128`). The dependency factory injects this concrete retriever into the planner (`backend/core/dependencies.py:288-300`), which adds the retrieved topics to the planning prompt (`backend/services/interview_planner/agent.py:32-47`). |
| Text production confirmed | **Supported, dated 2026-07-23.** State that the production text flow was remotely verified; do not convert PASS checks into accuracy, quality, or latency statistics. | The deployment report records the deployed revision and URLs (`DEPLOYMENT_REPORT.md:3-17`) and remote PASS checks for authenticated Resume extraction, interview planning/question generation, answer evaluation/completion, report generation, history, ownership, Firestore, and frontend routing (`DEPLOYMENT_REPORT.md:19-45`). Its narrative identifies Text Interview as the continuing production workflow (`DEPLOYMENT_REPORT.md:74-80`). |
| Voice source/local only unless deployment proof exists | **Required wording.** The current repository contains a voice implementation and local/private-service configuration, but the audited deployment record does not prove a live production speech pipeline. | The current source declares the browser voice WebSocket and its injected streaming question/speech services (`backend/gateway/api/voice.py:148-165`). The speech boundary documents Silero VAD, faster-whisper, VieNeu-TTS, its private WebSocket, and the embedded-local fallback (`backend/speech_service/README.md:1-16`); local setup runs the speech service separately (`README.md:3-8`). However, the latest tracked deployment report predates the current voice revision and explicitly says its deployed phase introduced no microphone capture, voice WebSocket, STT, streaming Gemini response, TTS, or separate speech service (`DEPLOYMENT_REPORT.md:74-80`). No later tracked deployment/E2E report was found. |
| No unsupported metrics | **Required.** Present implemented metric definitions only as methodology. Present current quantitative results as **N/A / `no_data`**, never as measured system performance. | The checked-in manifest has zero cases in every slice (`backend/evaluation_dataset.example.json:1-9`). The checked-in report has `status: "no_data"`, sample count zero, and null values for CV, STT, TTS, LLM, evaluator, and voice metrics (`backend/evaluation_report.json:1-63`). Unit tests use fake components and synthetic constants (`backend/app/tests/test_system_evaluation.py:52-125`), so their asserted numbers are framework tests, not system results. |

### Exact slide-safe language

- **Orchestration:** “In-process multi-agent orchestration; no LangGraph in the
  active application.”
- **Retrieval:** “Packaged-catalog lexical retrieval using token overlap and
  deterministic top-8 selection; no embedding model or vector database in the
  audited implementation.”
- **Deployment:** “Text workflow remotely verified in production on 23 July
  2026. Voice is implemented in current source and documented for local/private
  service operation; production voice deployment is not evidenced by the
  available deployment report.”
- **Evaluation:** “Evaluation methodology is implemented, but the available
  manifest is empty and the aggregate report is `no_data`; quantitative AI
  performance remains N/A.”

### Disallowed slide claims

- Any LangGraph node/graph, LangChain runtime, vector database, embedding model,
  semantic search, or semantic reranking shown as implemented architecture.
- “Production voice,” “deployed speech worker,” or a production voice latency
  claim without a newer deployment record tied to the current voice revision.
- Accuracy, F1, WER/CER, score consistency, latency, percentile, failure-rate,
  throughput, test-count, or dataset-size numbers presented as empirical
  product results unless a reproducible non-empty run and provenance record are
  supplied.
- Numeric values visible in UI screenshots described as benchmark evidence;
  those are sanitized product-output examples, as documented in
  `docs/presentation/PRODUCT_SCREENSHOT_EVIDENCE.md:3-18`.

### Current deck metrics: unsupported

A read-only inspection of slide 22 in
`FiPilot_Capstone_Presentation (1).pptx.pptx` found these claimed results:

- Resume extraction: 235 CVs; 49.88% precision; 51.37% recall.
- Speech: 200 WAVs; 5.93% WER; 4.33% CER; 15,423 ms STT; 1,333 ms TTS;
  RTF 1.20.
- Question/evaluator: 99.33% relevance; 100% CV alignment; MAE 0.7/10;
  consistency 97.34%.
- Voice: 1,605 ms average; 1,590 ms p50; 1,996 ms p95.

No matching non-empty manifest or primary result artifact was found. The
canonical checked-in report instead records zero samples and N/A for CV,
STT, TTS, question/evaluator, and voice sections
(`backend/evaluation_report.md:3-66`; `backend/evaluation_report.json:4-61`).
Every number above must therefore be removed from the result slide, not
relabelled as a FiPilot result. The isolated CPU
speech comparison in `docs/CLOUD_RUN_CPU_SPEECH_BENCHMARK.md:157-166` is a
runbook measurement with an explicit non-production limitation; it does not
validate the deck's end-to-end, latency, or quality claims.

### Architecture search record and limitations

The active Python/TypeScript source and first-party manifests were searched for
`langgraph`, `langchain`, `embedding`, common vector-store terms (`faiss`,
`pinecone`, `weaviate`, `chroma`, `qdrant`, `milvus`, `pgvector`), and semantic
retrieval/reranking terms, excluding `.git`, virtual environments, dependency
installations, `node_modules`, the PPTX, and the generated knowledge catalog's
interview-topic text. Matches were limited to explicit no-LangGraph comments,
compatibility/placeholders, tests/demo candidate content, documentation, and an
STT benchmark fixture name/reference sentence; no active import or dependency
was found. This absence
supports the scoped wording above but cannot rule out infrastructure or services
that are not represented in this repository.

The production claim is bounded by the tracked deployment report dated 2026-07-23.
Git history places the current voice implementation at revision `51fc3b57` dated
2026-08-12, after that report. A Dockerfile, deployment script, source code, or
passing local test demonstrates deployability or implementation—not that a
particular revision is serving production traffic. Production voice must remain
unconfirmed until a later first-party deployment record identifies the deployed
revision/service and records an end-to-end speech check. This audit did not
independently probe the dated production URLs, so “text production confirmed”
means confirmed by the first-party 2026-07-23 deployment report; it does not
establish that current HEAD is deployed or that the service remains live today.

## Evaluation dataset decision

No valid, approved, reproducible evaluation dataset was found for the current
FiPilot system. The existing system-evaluation framework was therefore **not run
against real data**. A safe rerun of the empty example manifest reproduced
`status=no_data`; it did not produce empirical metrics. The checked-in report
likewise has `status: "no_data"`, and every section has `sample_count: 0`
(`backend/evaluation_report.json:4-56`).

This is not a claim that no testing or experimentation occurred. The repository
contains unit-test fixtures, demo media, local diagnostic traces, mutable local
application data, and historical layout-model experiment images. None satisfies
all of the following requirements for presentation as an empirical evaluation
of the current system:

1. documented source, permission, and privacy/sanitization status;
2. ground truth or human labels appropriate to the metric;
3. a versioned manifest that identifies every input and expected value;
4. sufficient source fixtures and commands to reproduce the result; and
5. relevance to the active production implementation.

## What the current framework requires

The manifest contract supports six evidence slices
(`backend/services/system_evaluation/dataset.py:27-75`):

| Slice | Required evidence | Metrics implemented |
| --- | --- | --- |
| CV extraction | Resume file, expected skills, selected expected profile fields | Skill precision/recall/F1, profile-field accuracy, latency |
| STT | Mono uncompressed PCM16 16 kHz WAV, UTF-8 reference transcript, language category | WER, CER, latency, category breakdown |
| TTS | Synthesis text | First-audio time, generation time, generated-audio duration ratio |
| Question generation | Synthetic Candidate Profile, interview round, interview configuration | Gemini-judge relevance, difficulty alignment, CV alignment, latency |
| Answer evaluation | Synthetic profile, question, answer, configuration, human score from 0 to 10 | Repeated-score consistency, deviation, MAE versus human, latency |
| Voice turn | Content-free success/failure and total latency observations | Mean, p50, p95, failure rate |

The STT loader enforces the WAV format in
`backend/services/system_evaluation/dataset.py:145-158`. The real runner wires
the active Resume Agent, faster-whisper, VieNeu-TTS, Question Generator,
benchmark-only Gemini question judge, and Answer Evaluator
(`backend/scripts/run_system_evaluation.py:54-76`). Running non-empty slices
also requires the relevant speech dependencies/models and Google Application
Default Credentials, as documented in `docs/SYSTEM_EVALUATION.md:28-38`.

The framework is therefore *executable when a valid private manifest and its
fixtures are supplied*, but the audited workspace contains no such manifest.

## Candidate evidence and disposition

### 1. Checked-in evaluation manifest and reports

- `backend/evaluation_dataset.example.json` is an empty schema example: all six
  case arrays are empty.
- `backend/evaluation_report.json` and `backend/evaluation_report.md` are
  aggregate-only `no_data` outputs with zero samples.
- Git history shows that the example, framework, documentation, and `no_data`
  reports were introduced together in commit
  `9fda301b3fc3d0393a6db83e024e91dd22de39f5`; no earlier or later completed
  framework report exists in locally available history.

Disposition: **valid disclosure, not empirical results**. Preserve `no_data` in
the presentation.

### 2. Synthetic unit-test fixtures

`backend/app/tests/test_system_evaluation.py` creates temporary Resume text,
reference text, and PCM WAV data using explicit `PRIVATE_*_SENTINEL` strings and
uses `FakeProfileExtractor`, `FakeSTT`, `FakeTTS`, `FakeQuestionGenerator`,
`FakeQuestionJudge`, and `FakeAnswerEvaluator`
(`backend/app/tests/test_system_evaluation.py:52-125`). Its asserted scores and
latencies exercise aggregation and privacy-safe reporting; they are not outputs
from FiPilot's configured production models. The one `human_score=8.0` value is
a synthetic test constant (`backend/app/tests/test_system_evaluation.py:247-273`).

Disposition: **methodology/unit-test evidence only**. Do not present the test's
numeric assertions as system performance.

### 3. Tracked Candidate Resume: `FS_CV_VoQuangTrieu.docx`

- The document is tracked and was added in commit
  `21c89ef3459482dd83c8a35391b049535d720920`.
- A content-safe scan (counts only, no values emitted) found one email-like and
  one phone-like field. The filename also contains a person's name.
- No consent, sanitization statement, expected skills, expected profile fields,
  labelling procedure, or evaluation-manifest entry was found.

Disposition: **not approved or sanitized benchmark data**. It is a single
potentially personal Resume and has no ground truth. It must not be used in an
evaluation run or reproduced in presentation materials.

### 4. Current local audio/demo media

The project-owned audio-like files found outside dependency environments were:

- ignored `test.mp3`;
- ignored `.scratch/actual-test-2/narration.mp3` and
  `.scratch/actual-test-2/narration-fipilot.mp3`;
- ignored `.scratch/landing-video/narration.mp3`; and
- `frontend/public/fipilot-how-it-works.mp4` (plus its built copy).

The MP3s have no paired reference-transcript files, provenance/consent records,
or manifest entries, and they are not the PCM16 mono 16 kHz WAV required by the
STT evaluator. In particular, `test.mp3` is approximately 165.3 seconds,
stereo, and 44.1 kHz; the narration files are 24 kHz mono. The narration and MP4
assets are product-demo media, not labelled STT fixtures.

Disposition: **demo/diagnostic media, not evaluation data**.

### 5. Code-switch STT benchmark definition without fixtures

`backend/scripts/benchmark_stt_codeswitch.py` defines four reference sentences
for `01-fastapi.wav`, `02-langgraph.wav`, `03-cloud-run.wav`, and
`04-concurrency.wav` (`backend/scripts/benchmark_stt_codeswitch.py:23-50`). The
script itself calls them "sanitized" and refuses to run when they are absent
(`backend/scripts/benchmark_stt_codeswitch.py:75-85`). No copy of any of the
four WAV files was found in the working tree, ignored workspace, or reachable
Git object paths.

Disposition: **an incomplete benchmark recipe**. It cannot produce a
reproducible result without the missing audio and documented provenance. It is
also separate from `run_system_evaluation.py`.

### 6. Ad hoc end-to-end speech trace

`.scratch/speech-run2.stdout.log:4` contains one `SPEECH_E2E_RESULT` record with
a synthesized answer, STT output, one model-generated evaluation score, and
latency timings. It is an ignored local log, not an aggregate report produced by
the system-evaluation framework. No checked-in runner, input fixture, reference
transcript, environment lock, repeated sample set, or human label is linked to
the record. It also contains question/answer/transcript content, whereas the
framework intentionally keeps reports aggregate-only.

Disposition: **single diagnostic trace, not benchmark evidence**. Its score and
timings must not appear as evaluation results in the PPTX.

### 7. Ignored local SQLite databases

A read-only schema/count audit found:

- root `interview_app.db`: 0 sessions, 0 messages, 0 evaluations;
- `backend/interview_app.db`: 81 sessions, 167 messages, 11 evaluation rows.

Both files are ignored by `*.db` (`.gitignore:8`). The populated database is
mutable local application state, contains candidate/session/message fields, has
no dataset version or consent/sanitization record, and its evaluation rows are
the application's model evaluation payloads written by
`SQLiteInterviewRepository.save_evaluation`
(`backend/infrastructure/repositories/sqlite.py:359-380`), not independent human
labels. No deterministic mapping from these rows to a benchmark manifest exists.

Disposition: **private/local operational data, not a labelled dataset**. Do not
extract or report scores, text, or identities from it.

### 8. Historical Resume samples and preparation notebooks

Reachable Git history includes, among other items:

- `dataset/cv.pdf`, `dataset/cv2.pdf`, `dataset/--resume-28.pdf`, and
  `dataset/test1.pdf` in May 2026 commits;
- historical `backend/mock_cv.docx` / `backend/tts_stt/mock_cv.docx`; and
- `backend/notebooks/00_create_data.ipynb`, whose saved output references a
  developer-specific `/home/hoai/...` Resume collection and filenames that can
  identify candidates.

These files/notebook references predate the current evaluation manifest. They
have no expected extraction fields, split manifest for the current framework,
source licence/consent record, sanitization record, or stable acquisition
instructions. The notebook's external Resume collection is not present.
The historical mock DOCX is clearly synthetic, but it is only a small smoke
fixture with no versioned ground truth or recorded evaluation output; synthetic
content alone does not turn it into an empirical benchmark.

Disposition: **historical development inputs with unresolved provenance and no
current labels**. They are neither safe nor sufficient for the current CV
benchmark.

### 9. Historical YOLO/DocLayout evaluation artifacts

Commit `5e3e92c8ed4b6c0ffb9236c24e252561d8a96f64` ("add EDA & results")
contains executed EDA notebooks and rendered YOLO/DocLayout validation images
under `backend/notebooks/` and `backend/runs/detect/val*`. The notebooks display
dataset counts and model metrics, but important metrics are explicitly
hard-coded, and their data, annotations, weights, `results.csv`, and
`eval_results.xlsx` are referenced through developer-local absolute paths such
as `/home/hoai/user/resource/fipilot/backend/models/...`. Those required source
artifacts are not present anywhere in reachable Git objects.

The experiment is also not an evaluation of the current document pipeline. The
active `DocumentService` extracts text directly with `pypdf` or `python-docx`
(`backend/infrastructure/documents/pdf_service.py:5-43`); no active backend
module invokes YOLO or DocLayout for Resume extraction.

Disposition: **historical, incomplete, and obsolete-system evidence**. The
figures may document prior experimentation, but their quantitative results are
not reproducible from this repository and must not be presented as current
FiPilot evaluation results.

### 10. Cloud Run CPU speech benchmark statement

`docs/CLOUD_RUN_CPU_SPEECH_BENCHMARK.md:157-160` states that one 15-second,
469-chunk fixture took 2.316 seconds at one shape and 37.041 seconds at another.
No corresponding fixture, raw log, result file, commit-linked command output,
or repeated-sample summary was found. The same document identifies itself as a
runbook/latency benchmark rather than a production sizing recommendation.

Disposition: **documented anecdotal measurement, not reproducible evaluation
output**. Do not promote it to an empirical results slide.

### 11. Knowledge corpus, templates, screenshots, and dependency samples

- `Knowledge/`, `Template/`, and
  `backend/services/interview_knowledge/catalog.json` are interview knowledge
  inputs, not labelled evaluation cases.
- Frontend screenshots and product videos are UI/demo evidence, not AI metric
  datasets.
- Audio/CSV/test assets inside `backend/venv` or other dependency directories
  belong to installed third-party packages. They are neither FiPilot cases nor
  provenance-controlled project data. This includes the six VieNeu package
  voice-sample WAV/text pairs: they support that dependency's voice examples,
  are not tracked or manifest-linked FiPilot STT/TTS cases, and have no project
  benchmark licence/provenance record.

Disposition: **out of evaluation scope**.

## Search record

The audit used the following read-only searches. Exclusions avoid dependency
trees and browser caches where noted.

```powershell
# Current, ignored, and untracked paths
rg --files -uu -g '!**/.git/**' -g '!**/node_modules/**' `
  -g '!**/.venv/**' -g '!backend/venv/**'

# Candidate filenames and common dataset/media/result formats
rg --files -uu -g '*.wav' -g '*.mp3' -g '*.webm' -g '*.mp4' `
  -g '*.docx' -g '*.pdf' -g '*.json' -g '*.jsonl' -g '*.csv' `
  -g '*.tsv' -g '*.xlsx' -g '*.db' -g '*.sqlite*' `
  -g '!**/.git/**' -g '!**/node_modules/**' -g '!backend/venv/**'

# Alternate evaluation manifests, labels, and paired references
rg -n --hidden -g '!**/.git/**' -g '!**/node_modules/**' `
  -g '!backend/venv/**' `
  '"(cv_cases|stt_cases|tts_cases|question_cases|evaluator_cases|voice_turns|human_score|reference_text_path|resume_path)"' .
rg --files -uu -g '*.txt' -g '!**/.git/**' -g '!**/node_modules/**' `
  -g '!backend/venv/**' | rg -i `
  '(reference|transcript|answer|label|ground|truth|eval|benchmark|fixture|speech|audio|resume|cv)'

# Diagnostic and benchmark-like log records
rg -n --glob '*.log' --glob '*.out' `
  'SPEECH_E2E_RESULT|speech_latency|status=(completed|partial|no_data)|WER|CER|mAP50|human_score' `
  .scratch backend frontend .codex-preview

# Ignore/tracking/provenance checks
git status --short
git ls-files -- FS_CV_VoQuangTrieu.docx backend/interview_app.db interview_app.db test.mp3 '.scratch/**'
git check-ignore -v backend/interview_app.db interview_app.db test.mp3 '.scratch/actual-e2e-backend.out.log'
git log --follow --format='%H%x09%aI%x09%an%x09%s' -- FS_CV_VoQuangTrieu.docx

# All reachable historical paths and evaluation-report history
git rev-list --objects --all
git log --all --name-only --pretty=format:
git log --all -p -- backend/evaluation_report.json
git log --all --format='%H%x09%aI%x09%s' -- `
  backend/evaluation_report.json backend/evaluation_report.md `
  backend/evaluation_dataset.example.json docs/SYSTEM_EVALUATION.md
git ls-tree -r --long 5e3e92c8ed4b6c0ffb9236c24e252561d8a96f64

# Historical notebook/source-reference checks
git grep -n -i -e find_segment -e roboflow -e resumes_copy `
  -e layout_data -e DocLayout `
  5e3e92c8ed4b6c0ffb9236c24e252561d8a96f64
```

Two content-safe read-only inspections were also performed:

- DOCX XML was scanned in memory for counts of email-like and phone-like fields;
  no personal value was printed or copied.
- SQLite files were opened using SQLite `mode=ro`; only schema, row counts, date
  range, and aggregate counts were queried. No message, answer, candidate name,
  identifier, or report content was emitted.

## Evaluation run decision

No evaluation command was executed against real data because no valid non-empty
manifest and complete, approved fixture set exists. Running against the tracked
Resume, ignored media, local database, or historical artifacts would require
inventing ground truth, disregarding privacy/provenance, or evaluating an
obsolete pipeline.

The current framework and the empty-data behavior were safely verified from
`backend/`:

```powershell
.\.venv\Scripts\python.exe -m pytest app/tests/test_system_evaluation.py -q
# 4 passed in 1.64s

.\.venv\Scripts\python.exe scripts\run_system_evaluation.py `
  --dataset evaluation_dataset.example.json `
  --output-dir ..\.scratch\evaluation-evidence-pass-20260814 `
  --evaluator-repetitions 3
# status=no_data
# process exit code: 2 (the runner returns nonzero unless status=completed)

.\.venv\Scripts\python.exe scripts\benchmark_stt_codeswitch.py ..\.scratch
# process exit code: 2; missing 01-fastapi.wav, 02-langgraph.wav,
# 03-cloud-run.wav, and 04-concurrency.wav
```

The first result verifies framework behavior using fakes; it is not an empirical
AI-quality result. The second recreated the expected aggregate-only `no_data`
reports under ignored scratch storage. Output hashes were:

- JSON SHA-256:
  `3DB8515302363DC0DDDAC21E3910090474E424C17DB681528A52D6FD46FB0CBC`
- Markdown SHA-256:
  `BB82966C71E2E868AF5B5C9F1292ACCB6EA20C2B4FEF41B98E1F1714E78F0F33`

These validation outputs confirm that the machinery runs and that the available
manifest contains no cases; they do not justify any performance metric.

When an approved private dataset exists, the repository's documented command is:

```powershell
cd backend
python scripts/run_system_evaluation.py `
  --dataset C:\private-benchmark\evaluation_dataset.json `
  --output-dir . `
  --evaluator-repetitions 3
```

Only the aggregate JSON/Markdown outputs from that command, together with a
recorded commit, model/config versions, environment, dataset version, and label
review procedure, should feed the PPTX.

## Evaluation Readiness / Remaining Evidence Gap

> FiPilot has an implemented, privacy-aware evaluation methodology and
> synthetic unit coverage, but empirical validation is not yet available. The
> repository contains no approved, versioned labelled benchmark for Resume
> extraction, STT/TTS, question generation, answer scoring, or end-to-end voice
> latency. Until such a dataset is collected and run reproducibly, all
> quantitative evaluation fields remain **N/A (`no_data`)**.

The documented next evidence milestone is a private, consented/sanitized,
versioned manifest with representative slices (the project recommends at least
30 samples per language/domain slice), reference transcripts, independently
reviewed human answer labels, content-free voice observations, and captured
commit/model/config metadata (`docs/SYSTEM_EVALUATION.md:10-24`).
