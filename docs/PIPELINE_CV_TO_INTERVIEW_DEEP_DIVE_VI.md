# Pipeline kỹ thuật từ Resume đến phỏng vấn và báo cáo

> Phạm vi: tài liệu chuyên sâu về luồng dữ liệu `Resume -> document text -> Candidate Profile -> readiness -> Interview Plan -> Question -> Answer Evaluation -> Report`.
>
> Ảnh chụp khảo sát: worktree ngày 20/08/2026, HEAD `3a38b481` trên nhánh `feature/ai-lab-vertex`, có thay đổi local chưa commit. Vì vậy tài liệu này mô tả **worktree đã đọc**, không chỉ commit HEAD.
>
> Nguồn: chỉ dùng source code, test, `CONTEXT.md`, ADR và đặc tả trong repository. Tài liệu tổng quan hiện có vẫn là [BAO_CAO_TONG_QUAN_DU_AN.md](BAO_CAO_TONG_QUAN_DU_AN.md) và [SYSTEM_DESIGN_VI.md](SYSTEM_DESIGN_VI.md); tài liệu này không thay thế chúng mà đào sâu riêng pipeline runtime và các khoảng cách so với contract Resume Review.

## 1. Cách đọc trạng thái trong tài liệu

Ba nhãn sau được dùng xuyên suốt:

- **IMPLEMENTED**: có đường chạy trong `backend/gateway`, `backend/shared`, `backend/services`, `backend/orchestrator`, `backend/infrastructure` hoặc frontend production hiện tại.
- **PARTIAL**: có một phần contract/runtime, nhưng chưa thỏa toàn bộ đặc tả đã duyệt.
- **SPEC/PENDING**: đã được định nghĩa trong `CONTEXT.md`, ADR hoặc Resume Review spec nhưng chưa có đường chạy production hoàn chỉnh.

Điểm cần nhớ nhất: pipeline phỏng vấn text/voice, đánh giá answer và report đã có runtime; workspace sửa Candidate Profile, Replacement Upload, upload idempotency/status, concurrency bằng `If-Match`, audit/provenance bền vững và snapshot version nguyên tử vẫn chủ yếu là contract đang chờ triển khai. Danh sách route được mount thực tế nằm tại [backend/gateway/main.py#L122](../backend/gateway/main.py#L122).

## 2. Bản đồ end-to-end

```text
Firebase user
   |
   | Bearer ID token
   v
POST /api/v2/resume/upload (multipart file)
   |
   +-- validate extension + actual signature/MIME + size
   +-- PDF native text; OCR fallback khi sparse/image-only
   |   hoặc DOCX paragraphs + tables
   +-- normalize text, require >= 50 characters
   +-- SHA-256 + owner/version-scoped extraction cache
   +-- bounded, section-aware Resume context (<= 16,000 chars)
   +-- Gemini classification + structured ResumeExtractionResult
   +-- rule-based verification/reconciliation
   +-- persist Candidate + raw_resume_text + CandidateProfile
   v
Upload response: candidate_id + profile + confidence_score + extraction metadata
   |
   +--> GET /api/v2/candidates/{candidate_id}/profile
   |      -> persisted profile + profile_version + ETag + readiness issues
   |
   +--> POST /api/v2/interview/prepare (optional warm-up)
   |      -> persistent/in-memory InterviewPlan blueprint
   |
   `--> POST /api/v2/interview/start
          -> reload owned profile
          -> get/create InterviewPlan
          -> generate first InterviewQuestion
          -> create session and persist InterviewSessionState
                    |
                    +--> text: REST answer loop
                    |      evaluate -> decide -> next/follow-up -> persist
                    |
                    `--> voice: WebSocket
                           PCM -> VAD -> STT -> transcript
                           -> same answer service/orchestrator
                           -> streamed question -> TTS -> PCM
                    |
                    v
                session completed
                    |
                    v
          POST /api/v2/interview/{session_id}/report
          -> Gemini InterviewReport -> persist -> history/readback
```

Các lớp chịu trách nhiệm:

| Lớp | Vai trò | Nguồn chính |
| --- | --- | --- |
| Frontend | auth token, upload, cấu hình, text/voice UI, report/history | [App.tsx#L20](../frontend/src/App.tsx#L20), [api.ts#L74](../frontend/src/lib/api.ts#L74) |
| Gateway | REST/WebSocket transport, auth dependency, status mapping | [gateway/main.py#L87](../backend/gateway/main.py#L87) |
| Service/agent | extraction, planning, generation, evaluation, report | [core/dependencies.py#L269](../backend/core/dependencies.py#L269) |
| Orchestrator | state machine và quyết định lượt kế tiếp | [interview_orchestrator.py#L32](../backend/orchestrator/interview_orchestrator.py#L32) |
| Infrastructure | Firebase, Gemini, document/OCR, speech, SQLite/Firestore | [core/dependencies.py#L25](../backend/core/dependencies.py#L25) |
| Shared schemas | contract Pydantic dùng giữa các lớp | [shared/schemas/candidate.py#L8](../backend/shared/schemas/candidate.py#L8), [shared/schemas/interview.py#L47](../backend/shared/schemas/interview.py#L47) |

## 3. Điều kiện nền: authentication và ownership

### 3.1. REST

**IMPLEMENTED.** Frontend lấy Firebase ID token, gắn `Authorization: Bearer <token>`, và chỉ refresh token đúng một lần khi response là `401`; các lỗi mạng được đóng gói thành `ApiError` có `status`, `code`, `issues`, `retryable` và category tại [frontend/src/lib/api.ts#L74](../frontend/src/lib/api.ts#L74).

Backend `get_current_user`:

- Khi `AUTH_ENABLED=true`, bắt buộc Bearer token và gọi Firebase Admin verify tại [backend/core/dependencies.py#L175](../backend/core/dependencies.py#L175).
- Firebase adapter yêu cầu `uid`/`sub`, bỏ các token nhạy cảm khỏi claims và dùng Application Default Credentials tại [backend/infrastructure/auth/firebase.py#L28](../backend/infrastructure/auth/firebase.py#L28).
- Khi `AUTH_ENABLED=false`, dùng `AUTH_DEV_USER_ID`; đây chỉ là đường local development tại [backend/core/dependencies.py#L180](../backend/core/dependencies.py#L180).

### 3.2. Ownership

**IMPLEMENTED.** `candidate_id` và `session_id` chỉ là resource ID, không phải bằng chứng quyền truy cập:

- SQLite lọc candidate/session bằng cả ID lẫn owner, xem [sqlite.py#L555](../backend/infrastructure/repositories/sqlite.py#L555).
- Firestore đặt dữ liệu dưới `users/{uid}/candidates` và `users/{uid}/interviews`, xem [firestore.py#L681](../backend/infrastructure/repositories/firestore.py#L681).
- Profile GET trả cùng một `404 candidate_profile_not_found` cho missing và foreign resource tại [candidate_profile.py#L26](../backend/gateway/api/candidate_profile.py#L26).
- Ownership của auth, candidate, session, answer, report, history và prepare có test tại [test_auth_and_ownership.py#L218](../backend/app/tests/test_auth_and_ownership.py#L218).

### 3.3. Voice WebSocket

**IMPLEMENTED.** WebSocket không dùng header Authorization như REST. Client gửi hai subprotocol: protocol marker `firebase-auth` và token. Gateway kiểm tra origin allowlist, token, owner session và mode; mã đóng gồm `4401` auth, `4403` origin, `4404` missing/foreign session, `4409` mode/state conflict, `4429` duplicate live connection tại [voice.py#L146](../backend/gateway/api/voice.py#L146) và [voice.py#L169](../backend/gateway/api/voice.py#L169).

## 4. Giai đoạn A — nhận và trích text từ Resume

### 4.1. HTTP input hiện tại

**IMPLEMENTED:** `POST /api/v2/resume/upload` nhận một field multipart tên `file`, yêu cầu auth qua dependency tại [backend/gateway/api/resume.py#L45](../backend/gateway/api/resume.py#L45).

Contract runtime hiện tại:

| Thuộc tính | Hành vi |
| --- | --- |
| Tên field | `file` |
| Filename extension | chỉ `.pdf`, `.docx` |
| Dung lượng | tối đa 10 MiB; kiểm sau khi ghi temp file |
| Temp file | `NamedTemporaryFile(delete=False)`, xóa trong `finally` |
| Content fingerprint | SHA-256 toàn bộ bytes |
| Idempotency-Key | **chưa yêu cầu** |
| Replacement target | **chưa có route** |
| Upload status resource | **chưa có** |

Xem giới hạn và temp-file lifecycle tại [resume.py#L41](../backend/gateway/api/resume.py#L41), [resume.py#L73](../backend/gateway/api/resume.py#L73), [resume.py#L247](../backend/gateway/api/resume.py#L247).

Lưu ý về multipart: handler khai báo một `UploadFile`, nhưng chưa có lớp kiểm tra cardinality để chủ động trả `400 multiple_files_not_allowed` như contract mục tiêu.

### 4.2. Xác minh loại file thực

**IMPLEMENTED.** Route kiểm extension sớm, sau đó `DocumentService` kiểm thêm nội dung:

- PDF phải có `%PDF-` trong 1.024 byte đầu.
- DOCX phải bắt đầu `PK`, là ZIP hợp lệ, có `[Content_Types].xml` và `word/document.xml`.
- Tổng dung lượng bung nén DOCX không vượt 50 MiB.
- MIME khai báo, nếu có, phải khớp allowlist.
- Extension và signature không khớp trả `file_type_mismatch`/`415`.

Nguồn: [pdf_service.py#L60](../backend/infrastructure/documents/pdf_service.py#L60).

Điều này tốt hơn việc chỉ tin extension, nhưng signature DOCX hiện mới nhận diện ZIP chung trước khi kiểm members; validation container sau đó mới phân biệt DOCX hợp lệ.

### 4.3. PDF extraction và OCR fallback

**IMPLEMENTED trong worktree hiện tại**, dù ADR 0004 cũ nói contract không OCR; đây là thay đổi runtime cần đồng bộ lại ADR/spec.

Trình tự tại [pdf_service.py#L97](../backend/infrastructure/documents/pdf_service.py#L97):

1. `pypdf.PdfReader` đọc từng page.
2. PDF encrypted chỉ được chấp nhận nếu decrypt bằng mật khẩu rỗng; nếu không trả `encrypted_document`/`422`.
3. Mỗi page gọi `extract_text`; page lỗi trở thành chuỗi rỗng và warning `page_parse_failed`.
4. `classify_text_quality` đếm ký tự alphanumeric và số page có text. Tài liệu được xem là `IMAGE_ONLY`, `SPARSE`, `NORMAL` hoặc `UNUSABLE` tại [quality.py#L21](../backend/infrastructure/documents/quality.py#L21).
5. Nếu toàn tài liệu image-only/sparse, các page có dưới 50 ký tự alphanumeric được render bằng PyMuPDF ở scale 2x và chạy `RapidOCR`.
6. OCR chỉ thử tối đa 20 page và toàn tài liệu có deadline mặc định 30 giây; warning có thể là `ocr_page_limit_reached`, `ocr_empty`, `ocr_timeout`, `ocr_failed`.
7. Kết quả page được NFKC normalize, bỏ NUL, co khoảng trắng từng dòng; toàn văn phải có ít nhất 50 ký tự, nếu không trả `no_extractable_text`/`422`.
8. `extraction_method` là `native_pdf`, `ocr` hoặc `mixed`. Có bất kỳ warning nào thì status là `partial`.

OCR engine load lazy để không trả chi phí model cho PDF bình thường tại [ocr.py#L10](../backend/infrastructure/documents/ocr.py#L10).

### 4.4. DOCX extraction

**IMPLEMENTED.** `python-docx` lấy:

- paragraph không rỗng;
- từng row/cell trong table;
- table row cũng được nối vào plain text bằng ` | `;
- structured table metadata được giữ trong `DocumentExtractionResult.tables`.

DOCX không có page count vì mô hình tài liệu reflow; text dưới 50 ký tự trả `no_extractable_text`. Xem [pdf_service.py#L187](../backend/infrastructure/documents/pdf_service.py#L187).

### 4.5. Output của document extraction

`DocumentExtractionResult` tại [documents/models.py#L26](../backend/infrastructure/documents/models.py#L26):

```json
{
  "text": "normalized full document text",
  "source_type": "pdf | docx",
  "page_count": 2,
  "character_count": 8421,
  "extraction_method": "native_pdf | ocr | mixed | docx",
  "status": "complete | partial | failed",
  "is_partial": false,
  "warnings": [],
  "pages": [
    {
      "page_number": 1,
      "text": "...",
      "extraction_method": "native_pdf | ocr",
      "warnings": []
    }
  ],
  "tables": [
    { "page_number": null, "rows": [["cell 1", "cell 2"]] }
  ]
}
```

Không phải toàn bộ object này được trả về client. `pages`, `tables` và full `text` chỉ sống trong server pipeline; response upload chỉ trả metadata chọn lọc.

## 5. Giai đoạn B — text Resume thành Candidate Profile

### 5.1. Tạo context cho Gemini

**IMPLEMENTED.** Full extracted text được đưa qua `build_resume_context` tại [profile_scanner/context.py#L104](../backend/services/profile_scanner/context.py#L104):

- nếu <= 16.000 ký tự: dùng toàn bộ;
- nếu dài hơn: split theo heading/alias section, co boilerplate lặp lại, phân ngân sách có trọng số và giữ cả head lẫn tail;
- output có `total_characters`, `characters_considered`, `is_partial`, `warnings=("content_omitted",)`;
- context bị cắt luôn phải được biểu diễn là Partial Extraction, không được báo complete.

Do đó “trích toàn bộ text” và “đưa toàn bộ text vào LLM” là hai chuyện khác nhau: document layer có thể đọc đủ, nhưng profile extraction hiện bị giới hạn context 16.000 ký tự.

### 5.2. Classification trước extraction

**IMPLEMENTED.** Resume content được coi là untrusted data. System instruction cấm làm theo instruction bên trong file tại [profile_scanner/prompts.py#L6](../backend/services/profile_scanner/prompts.py#L6).

Gemini phải trả `document_type` và `classification_confidence`. Chỉ khi:

- `document_type == "resume"`; và
- `classification_confidence >= 0.7`

thì mới tiếp tục. Nếu không, `NonResumeDocumentError` trở thành `not_a_resume`/`422`; xem [profile_scanner/agent.py#L26](../backend/services/profile_scanner/agent.py#L26).

Prompt chỉ chấp nhận Resume thuộc 10 domain kỹ thuật: AI Engineer, Backend Developer, Business Analyst, Data Engineer, Data Scientist, DevOps Engineer, Full Stack Developer, Software Engineer, Tester/QA/QC, Web Developer; prompt yêu cầu reject báo cáo dự án, thesis, research paper, JD, certificate và portfolio team tại [profile_scanner/prompts.py#L20](../backend/services/profile_scanner/prompts.py#L20).

### 5.3. Raw structured output của LLM

`ResumeExtractionResult` tại [profile_scanner/schemas.py#L16](../backend/services/profile_scanner/schemas.py#L16):

```json
{
  "document_type": "resume | portfolio | job_description | academic_report | project_report | research_paper | certificate | other",
  "classification_confidence": 0.93,
  "name": "Nguyen Van A",
  "years_experience": 2.5,
  "recent_role": "Backend Developer",
  "skills": ["Python", "FastAPI", "PostgreSQL"],
  "skill_evidence": [
    {
      "skill": "FastAPI",
      "evidence": "Built REST APIs for order processing",
      "source_section": "experience"
    }
  ],
  "projects": [
    {
      "name": "Order Service",
      "description": "Designed and deployed an order API",
      "technologies": ["FastAPI", "PostgreSQL"],
      "role": "Backend developer"
    }
  ],
  "experiences": [
    {
      "company": "Example Co",
      "title": "Backend Developer",
      "start_date": "2024",
      "end_date": "Present",
      "description": "Built APIs",
      "technologies": ["Python"]
    }
  ],
  "education": [
    {
      "institution": "Example University",
      "degree": "BSc",
      "field_of_study": "Computer Science",
      "start_date": "2020",
      "end_date": "2024"
    }
  ],
  "specialization": "Backend Developer",
  "confidence_score": 0.88
}
```

Các giới hạn prompt/schema conversion:

- tối đa 30 skills;
- tối đa 8 skill-evidence items;
- mỗi extracted evidence ban đầu là một string, sau đó đổi thành list một phần tử trong canonical profile;
- tối đa 6 projects và 6 experiences;
- evidence không tham chiếu một skill hiện có bị bỏ;
- ưu tiên skill có evidence trước rồi mới đến skill khác.

Conversion nằm tại [profile_scanner/schemas.py#L39](../backend/services/profile_scanner/schemas.py#L39); yêu cầu chất lượng nằm tại [profile_scanner/prompts.py#L49](../backend/services/profile_scanner/prompts.py#L49).

### 5.4. Verification/reconciliation sau LLM

**IMPLEMENTED nhưng hẹp.** Sau structured output, server không tin hoàn toàn LLM:

- rule parser tìm experience line dạng `title at company | start - end` trong section experience;
- sửa company/title/date theo text parse được;
- loại một số false-positive experience bắt nguồn từ identity block;
- gắn trạng thái provenance `supported`, `normalized_match`, `unsupported`, `uncertain` cho name/recent_role/specialization, skills và trường experience.

Xem [profile_scanner/verification.py#L79](../backend/services/profile_scanner/verification.py#L79).

Giới hạn quan trọng: `ResumeProcessingResult.provenance` có trong memory tại [profile_scanner/agent.py#L17](../backend/services/profile_scanner/agent.py#L17), nhưng upload route không persist hay trả danh sách provenance đó. Hiện chỉ `source_section` trong skill evidence và một số `extraction_method` đi vào persisted profile. Contract ADR 0008 về stable evidence identity/provenance vì vậy chưa hoàn tất.

### 5.5. Canonical Candidate Profile output

Canonical backend schema tại [shared/schemas/candidate.py#L38](../backend/shared/schemas/candidate.py#L38):

| Field | Type | Ý nghĩa runtime |
| --- | --- | --- |
| `candidate_id` | `str \| null` | server resource ID; trong upload response, ID đáng tin cậy nằm ở top-level; Profile GET mới đảm bảo field này trong `profile` |
| `name` | `str`, default `Candidate` | identity; fallback này không đạt readiness |
| `years_experience` | `float \| null` | số năm; readiness evaluator đánh dấu âm/non-finite invalid |
| `recent_role` | `str \| null` | optional |
| `skills` | `string[]` | canonical skill list |
| `skill_evidence` | object[] | `skill`, `evidence: string[]`, `source_section` |
| `projects` | object[] | `name`, `description`, `technologies`, `role` |
| `experiences` | object[] | `company`, `title`, dates, description, technologies |
| `education` | `string \| structured[] \| null` | đọc legacy string hoặc structured education |
| `specialization` | `str \| null` | suy ra từ evidence |
| `seniority_signal` | `str \| null` | derived/read-only nhưng hiện ở chung model |
| `confidence`, `confidence_score` | `0..1` | giữ compatibility hai tên; thiếu một field sẽ copy từ field kia |
| `extraction_method` | `str \| null` | `section_aware_verified` hoặc `section_aware_partial` cho AI extraction |

Nested canonical keys được định nghĩa tại [shared/schemas/candidate.py#L8](../backend/shared/schemas/candidate.py#L8). Frontend mirror tại [frontend/src/types/index.ts#L30](../frontend/src/types/index.ts#L30).

Điểm yếu contract hiện tại: `CandidateProfile` dùng Pydantic default `extra="ignore"`, trộn editable và read-only fields, chưa có `evidence_id`, và correction request schema strict riêng chưa tồn tại.

## 6. Cache, persistence và response sau upload

### 6.1. Hai tầng reuse extraction

**IMPLEMENTED, nhưng đây không phải upload idempotency.** Sau SHA-256:

1. In-memory `ProcessedResumeCache`: key = hash của `(extraction version, uid, content hash)`, TTL mặc định 1 giờ, tối đa 256 entry tại [profile_scanner/cache.py#L20](../backend/services/profile_scanner/cache.py#L20).
2. Persistent `resume_extraction_artifact`: cùng key owner/version-scoped trong SQLite/Firestore tại [sqlite.py#L55](../backend/infrastructure/repositories/sqlite.py#L55) và [firestore.py#L82](../backend/infrastructure/repositories/firestore.py#L82).

Cache hit bỏ qua Gemini extraction nhưng **vẫn tạo một Candidate mới**. Test xác nhận cùng Resume thành công tái dùng extraction cho candidate mới tại [test_resume_upload_v2.py#L158](../backend/app/tests/test_resume_upload_v2.py#L158).

### 6.2. Persistence hiện tại

Upload lần lượt:

1. `create_candidate`;
2. `save_candidate_resume_text`;
3. `save_candidate_profile`;
4. store in-memory cache;
5. save persistent extraction artifact.

Nguồn: [resume.py#L193](../backend/gateway/api/resume.py#L193).

Mỗi repository operation SQLite commit riêng tại [sqlite.py#L48](../backend/infrastructure/repositories/sqlite.py#L48) và [sqlite.py#L106](../backend/infrastructure/repositories/sqlite.py#L106). Vì vậy initial upload chưa phải một transaction nguyên tử end-to-end: lỗi sau `create_candidate` có thể để lại candidate/profile/resume ở trạng thái trung gian. Firestore cũng dùng nhiều write độc lập.

### 6.3. HTTP success output thực tế

Upload route trả shape tại [resume.py#L223](../backend/gateway/api/resume.py#L223):

```json
{
  "candidate_id": "123",
  "profile": {
    "candidate_id": null,
    "name": "Nguyen Van A",
    "years_experience": 2.5,
    "recent_role": "Backend Developer",
    "skills": ["Python", "FastAPI"],
    "skill_evidence": [],
    "projects": [],
    "experiences": [],
    "education": [],
    "specialization": "Backend Developer",
    "seniority_signal": null,
    "confidence": 0.88,
    "confidence_score": 0.88,
    "extraction_method": "section_aware_verified"
  },
  "confidence_score": 0.88,
  "extraction": {
    "status": "complete | partial",
    "source_type": "pdf | docx",
    "page_count": 2,
    "character_count": 8421,
    "extraction_method": "native_pdf | ocr | mixed | docx",
    "is_partial": false,
    "warnings": [],
    "context_characters_considered": 8421,
    "context_total_characters": 8421
  }
}
```

Frontend `ResumeUploadResponse` hiện chỉ khai báo ba field `candidate_id`, `profile`, `confidence_score`, nên TypeScript/UI bỏ qua `extraction` và không hiển thị Partial Extraction warning; xem [frontend/src/types/index.ts#L109](../frontend/src/types/index.ts#L109).

Ở response upload hiện tại, `candidate_id` được cấp riêng ở top-level. Object `profile` là `CandidateProfile` do extraction tạo ra nên `profile.candidate_id` thường là `null` và chưa có `profile_version`; hai field persisted này chỉ được đảm bảo khi đọc lại qua Profile GET.

### 6.4. Upload errors hiện tại

| Status | Code/body hiện tại | Nguồn |
| --- | --- | --- |
| 401 | FastAPI `detail` cho missing/invalid bearer | [core/dependencies.py#L188](../backend/core/dependencies.py#L188) |
| 413 | generic `detail: Resume file is too large.` | [resume.py#L77](../backend/gateway/api/resume.py#L77) |
| 415 | structured `unsupported_file_type` | [resume.py#L59](../backend/gateway/api/resume.py#L59) |
| 415 | structured `file_type_mismatch` | [pdf_service.py#L60](../backend/infrastructure/documents/pdf_service.py#L60) |
| 422 | `invalid_document`, `encrypted_document`, `no_extractable_text` | [pdf_service.py#L97](../backend/infrastructure/documents/pdf_service.py#L97) |
| 422 | structured `not_a_resume` | [resume.py#L179](../backend/gateway/api/resume.py#L179) |
| 422 | generic `detail` khi final `resume_text.strip() < 50` ở route compatibility path | [resume.py#L124](../backend/gateway/api/resume.py#L124) |
| 503 | structured `transient_service_failure` cho `LLMServiceError` | [gateway/main.py#L91](../backend/gateway/main.py#L91) |

Error contract chưa đồng nhất hoàn toàn: có response `{error:{...},request_id}` và có FastAPI `{detail:...}`.

## 7. Candidate Profile Review và Interview Readiness

### 7.1. Profile GET

**IMPLEMENTED.** `GET /api/v2/candidates/{candidate_id}/profile`:

- auth + owner scope;
- trả `profile` là `PersistedCandidateProfile` có `candidate_id` và `profile_version >= 1`;
- trả `readiness`;
- set strong ETag dạng `"1"`;
- CORS expose header `ETag`.

Nguồn: [candidate_profile.py#L15](../backend/gateway/api/candidate_profile.py#L15), [candidate.py#L72](../backend/shared/schemas/candidate.py#L72), [gateway/main.py#L113](../backend/gateway/main.py#L113).

### 7.2. Readiness algorithm

**IMPLEMENTED để đọc, chưa enforce khi start.** Text được normalize NFKC, trim/co Unicode whitespace và comparison key casefold tại [normalization.py#L6](../backend/services/candidate_profile/normalization.py#L6).

Một profile chỉ `is_ready=true` khi không có bất kỳ issue nào, gồm:

1. Name không blank và không phải fallback `Candidate`.
2. Có ít nhất một normalized skill.
3. Có ít nhất một evidence có thể phỏng vấn:
   - một nonblank string trong `skill_evidence[].evidence`; hoặc
   - project có `name` hoặc `description`; hoặc
   - experience có `title`, `company` hoặc `description`; hoặc
   - structured education có `institution` và `degree` hoặc `field_of_study`.
4. Không có validity issue:
   - `years_experience` âm hoặc non-finite;
   - nested entry hoàn toàn rỗng;
   - evidence skill không match skills.

Evaluator trả **toàn bộ** issues theo thứ tự section, không dừng ở lỗi đầu; xem [readiness.py#L17](../backend/services/candidate_profile/readiness.py#L17).

Output:

```json
{
  "is_ready": false,
  "issues": [
    {
      "code": "missing_skills",
      "origin": "interview_readiness",
      "field_path": "skills"
    }
  ]
}
```

Các code chính: `missing_name`, `fallback_name`, `missing_skills`, `missing_interviewable_evidence`, `invalid_years_experience`, `empty_nested_entry`, `evidence_skill_not_found`.

### 7.3. Frontend Profile Review hiện tại

**PARTIAL.** Route `/candidate-profile/:candidateId` đã được bảo vệ và tải profile+ETag qua API tại [frontend/src/App.tsx#L25](../frontend/src/App.tsx#L25) và [CandidateProfilePage.tsx#L388](../frontend/src/pages/CandidateProfilePage.tsx#L388).

Trang hiện:

- hiển thị readiness summary và focus link;
- hiển thị profile version;
- hiển thị identity, skills/evidence, project, experience, education;
- giữ legacy education dạng read-only;
- là **read-only**, không có editor/save/PATCH/start actions;
- nút chính quay lại setup/upload, không phải durable review workflow hoàn chỉnh.

Nguồn UI read-only: [CandidateProfilePage.tsx#L327](../frontend/src/pages/CandidateProfilePage.tsx#L327), [CandidateProfilePage.tsx#L492](../frontend/src/pages/CandidateProfilePage.tsx#L492).

### 7.4. Những contract Review còn thiếu

**SPEC/PENDING**, theo [RESUME_REVIEW_UI_SPEC.md](RESUME_REVIEW_UI_SPEC.md) và ADR:

- `PATCH /api/v2/candidates/{candidate_id}/profile` với strict allowlist;
- `If-Match` bắt buộc, parse strong ETag, stale `412`, increment đúng một lần;
- editor cho canonical fields;
- `evidence_id` UUID bền vững và provenance bất biến;
- Profile Audit Event;
- legacy education explicit replacement;
- Partial Extraction acknowledgement;
- unsaved-draft state/conflict recovery;
- start text/speech trực tiếp từ Profile Review;
- backend-authoritative readiness enforcement ở cả text và voice start.

Các quyết định ràng buộc: [ADR 0001](adr/0001-reviewed-candidate-profile-source-of-truth.md), [ADR 0002](adr/0002-strict-candidate-profile-correction-contract.md), [ADR 0003](adr/0003-separate-profile-validity-from-interview-readiness.md), [ADR 0007](adr/0007-use-owned-versioned-candidate-profile-resources.md), [ADR 0008](adr/0008-preserve-profile-provenance-through-explicit-identities.md).

## 8. Sau output trích CV cần gì để đến generation?

Đây là câu trả lời trực tiếp cho “có output trích CV rồi thì còn cần gì nữa mới generation”.

### 8.1. Điều kiện runtime thực tế hiện nay

Để gọi question generation đầu tiên, client cần:

1. **Candidate Profile đã persist** và có `candidate_id`. Không gửi toàn bộ local profile vào `/start`; request chỉ gửi ID và config.
2. **Authenticated owner** của candidate đó.
3. **InterviewConfig hợp lệ**:
   - `mode`: `text | voice`, default text;
   - `language`: `vi | en`;
   - `experience_level`: bắt buộc, `intern | junior | middle | senior`;
   - `duration_minutes`: 5..180, default 30;
   - `interview_style`: `technical | behavioral | mixed`;
   - `question_count`: >= 1, default 10;
   - `objective`: string;
   - `interviewer_personality`: professional/friendly/challenging/supportive.

Schema tại [shared/schemas/interview.py#L47](../backend/shared/schemas/interview.py#L47), payload frontend tại [TextInterviewPage.tsx#L320](../frontend/src/pages/TextInterviewPage.tsx#L320).

4. **Interview Plan**: planner cần profile + config + curated knowledge topics.
5. **Selected round** từ plan: question generator cần profile + round + config.

`POST /api/v2/interview/start` request thực tế:

```json
{
  "candidate_id": "123",
  "interview_config": {
    "mode": "text",
    "language": "vi",
    "experience_level": "junior",
    "duration_minutes": 30,
    "interview_style": "technical",
    "question_count": 10,
    "objective": "Evaluate technical knowledge and practical experience",
    "interviewer_personality": "professional"
  }
}
```

### 8.2. Điều kiện product contract mục tiêu

Theo spec, trước generation còn phải thỏa:

- profile là bản committed mới nhất;
- backend readiness `is_ready=true`;
- không dùng local draft chưa save;
- start atomically snapshot profile và exact `profile_version` vào session;
- nếu replacement đang pending, dùng profile committed cũ;
- text và voice dùng cùng readiness validator.

### 8.3. Mismatch quan trọng

**Hiện `/start` không gọi `evaluate_interview_readiness`.** Nó chỉ load owned profile rồi lập plan/generate question tại [interview.py#L111](../backend/gateway/api/interview.py#L111). Do đó một profile có name fallback, không skill hoặc không evidence vẫn có thể vào generation nếu client gọi API trực tiếp. Readiness hiện chỉ là thông tin của Profile GET.

## 9. Interview preparation và planning

### 9.1. Optional prepare endpoint

**IMPLEMENTED.** Frontend debounce 800 ms rồi gọi `POST /api/v2/interview/prepare` khi đã có uploaded profile và config hợp lệ tại [TextInterviewPage.tsx#L345](../frontend/src/pages/TextInterviewPage.tsx#L345).

Prepare:

- reload owned persisted profile;
- tạo key bằng blueprint version + owner + candidate ID + profile version + hash toàn bộ config;
- deduplicate concurrent request trong process;
- TTL in-memory mặc định 300 giây/128 entries;
- lookup/save blueprint artifact ở repository;
- trả `{status:"ready", profile_version}`.

Nguồn: [interview.py#L67](../backend/gateway/api/interview.py#L67), [interview_preparation/service.py#L27](../backend/services/interview_preparation/service.py#L27).

Prepare không tạo session và không sinh first question; generated questions chủ ý không cache.

### 9.2. Curated knowledge retrieval

**IMPLEMENTED.** Planner dùng `KnowledgeRetriever`:

- mặc định `local`: đọc `catalog.json`, tokenize toàn profile, chọn một trong 10 domain bằng term overlap, lấy level guidance và top 8 topic có overlap tại [interview_knowledge/local.py#L82](../backend/services/interview_knowledge/local.py#L82);
- tùy chọn `firestore_vector`: Vertex embedding + Firestore vector search được wire trong composition root tại [core/dependencies.py#L288](../backend/core/dependencies.py#L288).

Knowledge chỉ hướng dẫn depth/topic; profile evidence vẫn là nguồn authoritative trong planner prompt.

### 9.3. Planner input và output

`InterviewPlannerAgent` gửi Gemini task `simple`, temperature 0.1, thinking budget 0 tại [interview_planner/agent.py#L26](../backend/services/interview_planner/agent.py#L26).

Input prompt:

- full `candidate_profile`;
- full `interview_config`;
- `curated_knowledge`;
- yêu cầu ưu tiên project deep dive và evidence-backed skills, cơ chế/trade-off/debug/measurement thay vì định nghĩa chung.

Nguồn: [interview_planner/prompts.py#L14](../backend/services/interview_planner/prompts.py#L14).

Output `InterviewPlan`:

```json
{
  "duration_minutes": 30,
  "rounds": [
    {
      "round_id": "round-1",
      "topic": "FastAPI concurrency",
      "objective": "Validate practical API design decisions",
      "difficulty": "medium",
      "reasoning": "Candidate reports production FastAPI experience",
      "recommended_question_areas": ["async trade-offs", "error handling"],
      "weight": 0.3,
      "target_skills": ["FastAPI", "Python"],
      "question_budget": 2
    }
  ],
  "coverage_goals": ["Validate backend depth"],
  "risk_areas": ["Sparse performance evidence"],
  "planner_summary": "Plan focuses on evidence-backed backend work."
}
```

Schema: [shared/schemas/interview.py#L58](../backend/shared/schemas/interview.py#L58).

Rủi ro: schema/prompt không bắt `rounds` phải đủ tương ứng `question_count`; orchestrator có thể kết thúc khi hết rounds trước khi đạt question count.

## 10. Question generation và session start

### 10.1. Question Generator

**IMPLEMENTED.** Input = Candidate Profile + một InterviewRound + InterviewConfig. Output `InterviewQuestion` gồm:

- `question`;
- `language`;
- `topic`;
- `difficulty`;
- `reasoning`;
- `expected_answer_points`;
- `follow_up_questions`.

Schema tại [shared/schemas/interview.py#L78](../backend/shared/schemas/interview.py#L78). Prompt yêu cầu đúng một câu hỏi chính, evidence-grounded, probe phụ nằm trong follow-up list và tone personality chỉ áp dụng voice tại [question_generator/prompts.py#L28](../backend/services/question_generator/prompts.py#L28).

Model route: simple, temperature 0.2, thinking budget 0 tại [question_generator/agent.py#L20](../backend/services/question_generator/agent.py#L20).

### 10.2. Start sequence thực tế

`POST /api/v2/interview/start` tại [interview.py#L111](../backend/gateway/api/interview.py#L111):

1. load persisted owned profile;
2. get/create plan;
3. generate first question;
4. dựng `InterviewSessionState` chứa profile, config, plan và current turn;
5. nếu text, chèn opening turn và giữ planned question ở `pending_turn`;
6. sau các LLM calls mới create session;
7. persist state payload;
8. persist current turn;
9. trả session response.

Response:

```json
{
  "session_id": "456",
  "started_at": "2026-08-20T10:00:00Z",
  "state": {
    "candidate_profile": { "...": "snapshot content" },
    "interview_config": { "...": "..." },
    "interview_plan": { "...": "..." },
    "phase": "opening | interviewing",
    "opening_turn": null,
    "pending_turn": null,
    "current_turn": { "...": "..." },
    "completed_turns": [],
    "current_question_index": 0,
    "memory": { "previous_topics": [], "covered_skills": [], "weaknesses": [], "follow_up_points": [] },
    "voice_analytics": { "speaking_duration_ms": 0, "response_latencies_ms": [], "interruption_count": 0 }
  },
  "answer_replayed": false
}
```

### 10.3. Snapshot hiện tại và snapshot mục tiêu

**PARTIAL.** Profile content thực sự được copy vào `InterviewSessionState`, nên session có snapshot dữ liệu để orchestration dùng tại [interview_orchestrator.py#L67](../backend/orchestrator/interview_orchestrator.py#L67).

Nhưng chưa đạt ADR 0007 vì:

- không có trường `candidate_profile_version` riêng trong `InterviewSessionState`/session record;
- profile read và session create không nằm trong một transaction;
- plan và first-question LLM calls xảy ra giữa read và create;
- session chưa được create trước khi orchestration dùng snapshot;
- concurrent correction/replacement contract chưa tồn tại.

## 11. Text interview loop

### 11.1. Opening

Text mode thêm `turn-opening`, hỏi ứng viên giới thiệu bản thân; planned question đầu tiên được giữ trong `pending_turn`. Answer opening được persist nhưng không chạy evaluator và không tính vào `completed_turns`; sau đó pending turn trở thành current turn tại [conversation_flow.py#L11](../backend/orchestrator/conversation_flow.py#L11).

### 11.2. Answer request

`POST /api/v2/interview/{session_id}/answer`:

```json
{
  "turn_id": "turn-1-fastapi-medium",
  "answer": "Ứng viên trả lời..."
}
```

`turn_id` dài 1..200, answer dài 1..12.000 tại [interview.py#L50](../backend/gateway/api/interview.py#L50).

### 11.3. Answer idempotency/concurrency

**IMPLEMENTED cho answer, không phải upload.** `InterviewAnswerSubmissionService`:

- trim answer;
- load owner-scoped session;
- bắt đúng mode;
- bắt đúng active turn;
- SHA-256 normalized answer;
- claim unique `(session_id, turn_id)` trước evaluator;
- same hash + completed -> replay latest state;
- same turn + khác hash -> `answer_already_submitted`;
- processing duplicate -> `answer_submission_in_progress`;
- evaluator/persistence exception -> abandon claim để retry.

Nguồn: [interview_answer_service.py#L33](../backend/services/interview_answer_service.py#L33). SQLite unique constraint nằm tại [models.py#L51](../backend/models.py#L51); concurrent behavior có test tại [test_answer_submission_idempotency.py#L130](../backend/app/tests/test_answer_submission_idempotency.py#L130).

### 11.4. Answer Evaluation

`EvaluatorAgent` nhận:

- profile snapshot trong state;
- current `InterviewQuestion`, gồm expected answer points;
- candidate answer;
- config/language/mode.

Prompt chấm correctness, technical depth, practical experience, communication; output 0..10, strengths, weaknesses, missing topics/concepts, feedback và follow-up decision tại [answer_evaluator/prompts.py#L14](../backend/services/answer_evaluator/prompts.py#L14).

`AnswerEvaluation` output tại [shared/schemas/evaluation.py#L16](../backend/shared/schemas/evaluation.py#L16):

```json
{
  "turn_id": "",
  "scores": {
    "technical_score": 7.5,
    "depth_score": 6.5,
    "communication_score": 8.0,
    "engineering_mindset_score": 7.0,
    "overall_score": 7.3
  },
  "overall_score": 7.3,
  "technical_score": 7.5,
  "communication_score": 8.0,
  "correctness_score": 7.0,
  "strengths": ["Nêu đúng trade-off"],
  "weaknesses": ["Thiếu số đo latency"],
  "missing_topics": [],
  "missing_concepts": ["Backpressure"],
  "feedback": "...",
  "follow_up_needed": true,
  "follow_up_reason": "Cần làm rõ cơ chế backpressure."
}
```

Voice evaluation dùng simple model và thinking budget 0 để giảm critical-path latency; text dùng `EVALUATOR_TASK_TYPE`, mặc định complex tại [answer_evaluator/agent.py#L19](../backend/services/answer_evaluator/agent.py#L19).

### 11.5. Adaptive decision

Rule deterministic tại [decision_service.py#L6](../backend/orchestrator/decision_service.py#L6):

1. `follow_up_needed=true` -> `follow_up`.
2. Ngược lại overall score >= 8 -> `increase_difficulty` (`easy -> medium -> hard`).
3. Ngược lại -> `next_question`/round tiếp.
4. Orchestrator luôn dừng trước adaptive branch nếu số completed turns đạt `question_count`.
5. Nếu hết rounds, session cũng kết thúc dù chưa đạt question count.

Follow-up ưu tiên canned probe chưa hỏi; nếu hết probe thì generate lại với danh sách câu cần tránh. Turn ID chứa turn number để không collision tại [interview_orchestrator.py#L270](../backend/orchestrator/interview_orchestrator.py#L270).

Text mode prefetch question kế tiếp song song với evaluation để giảm latency; task bị cancel nếu decision chọn follow-up/increase difficulty tại [interview_orchestrator.py#L102](../backend/orchestrator/interview_orchestrator.py#L102).

### 11.6. Persistence mỗi lượt

Sau evaluation, service atomically theo boundary repository “complete answer claim + update state” trong mỗi adapter, rồi lưu turn hiện tại kế tiếp. `state_payload` là snapshot khôi phục chính; GET `/api/v2/interview/{session_id}` deserialize lại schema tại [interview.py#L230](../backend/gateway/api/interview.py#L230).

## 12. Voice interview loop

### 12.1. Chung domain với text

**IMPLEMENTED.** Voice không có orchestrator khác. `VoiceAnswerSubmissionService` là wrapper gọi cùng `InterviewAnswerSubmissionService` với `expected_mode=VOICE`, nhờ đó dùng chung claim, evaluator, decision và persistence tại [voice_session/answer_service.py#L22](../backend/services/voice_session/answer_service.py#L22).

### 12.2. Connection và modes

Một route WebSocket hỗ trợ ba purpose:

| URL | Session mode bắt buộc | Mục đích |
| --- | --- | --- |
| `/api/v2/voice/interview/{id}` | `voice` | full voice interview |
| `...?purpose=transcription` | `text` | speech input cho text answer |
| `...?purpose=playback` | `text` | đọc interviewer dialogue trong text UI |

Validation nằm tại [voice.py#L216](../backend/gateway/api/voice.py#L216).

### 12.3. Client control contract

`ClientVoiceEvent` strict `extra=forbid` tại [voice_session/events.py#L10](../backend/services/voice_session/events.py#L10):

- `start_listening`;
- `stop_listening`;
- `audio_chunk` announcement có `sequence`, encoding `pcm_s16le`, sample rate 16000;
- `confirm_answer` có nonblank `text` và `turn_id`;
- `start_barge_in`;
- `playback_complete`;
- `speak_question`;
- `speak_interviewer`;
- `stop_playback`.

Binary frame chứa PCM thực; server acknowledge `sequence` và `bytes_received`.

### 12.4. State machine và server events

Ephemeral voice status:

```text
IDLE -> WAITING_FOR_USER -> USER_SPEAKING -> TRANSCRIBING
     -> EVALUATING -> AI_THINKING -> AI_SPEAKING -> WAITING_FOR_USER
                                      `-> INTERRUPTED (barge-in)
```

Enum tại [voice_session/schemas.py#L9](../backend/services/voice_session/schemas.py#L9).

Server JSON events gồm `connected`, `state`, `audio_ack`, `processing`, `question_start`, `question_delta`, `question_complete`, `tts_start`, `audio_format`, `tts_complete`, `tts_cancelled`, `completed`, `error`; binary frames chiều server->client là PCM TTS. Event builders tại [voice_session/events.py#L67](../backend/services/voice_session/events.py#L67).

### 12.5. STT/VAD pipeline

Default local composition tại [core/dependencies.py#L214](../backend/core/dependencies.py#L214):

- Silero VAD: threshold 0.5, min silence 900 ms, speech pad 120 ms;
- faster-whisper: mặc định `large-v3`, CPU, int8, language `vi`;
- partial interval 2.5 giây;
- ngừng partial sau 20 giây buffered speech;
- final beam size 5;
- queue 800 frames;
- audio chunk max 256 KiB, session max 64 MiB.

Nếu `SPEECH_SERVICE_URL` được set, gateway dùng `RemoteAudioPipelineFactory` và `RemoteStreamingTTS`; nếu không dùng local model trong gateway process.

Final transcript có thể tự động submit vào answer service. Khi evaluation hoàn tất, voice path có thể stream question JSON từ Gemini, publish delta đồng thời sang TTS và gửi first audio sớm; xem [voice.py#L743](../backend/gateway/api/voice.py#L743).

### 12.6. TTS và barge-in

Default TTS là VieNeu, mode `v3turbo`, sample rate 24 kHz, semantic chunk target >= 3 words và <= 80 chars. Question text được feed theo delta vào bounded TTS queue. Khi ứng viên bắt đầu nói lúc AI đang phát, callback cancel TTS và phát `tts_cancelled`.

Audio/transcript chưa hoàn tất chỉ ở memory; durable session lưu final candidate answer, evaluation, voice analytics, không lưu raw audio.

## 13. Session completion và report

### 13.1. Điều kiện generate report

**IMPLEMENTED.** `POST /api/v2/interview/{session_id}/report` chỉ cho session status `completed` hoặc `report_generated`, state phải tồn tại và `current_turn` phải null. Nếu report đã có, service trả report cũ thay vì gọi LLM lại tại [report_generator/service.py#L15](../backend/services/report_generator/service.py#L15).

### 13.2. Report input

Prompt nhận:

- Candidate Profile;
- InterviewConfig;
- InterviewPlan;
- toàn bộ completed turns gồm question, answer, evaluation.

Yêu cầu: evidence-based coaching, không invent, phân biệt missing đã đánh giá với unevaluated, narrative đúng ngôn ngữ, score 0..10, confidence 0..1 tại [report_generator/prompts.py#L17](../backend/services/report_generator/prompts.py#L17).

### 13.3. Report output

`InterviewReport` tại [report_generator/schemas.py#L30](../backend/services/report_generator/schemas.py#L30):

```json
{
  "id": "uuid",
  "session_id": "456",
  "overall_score": 7.4,
  "technical_score": 7.5,
  "communication_score": 8.0,
  "correctness_score": 7.0,
  "summary": "...",
  "strengths": ["..."],
  "weaknesses": ["..."],
  "demonstrated_skills": ["FastAPI"],
  "missing_skills": ["Backpressure"],
  "skill_assessments": [
    { "skill": "FastAPI", "score": 7.5, "evidence": ["..."], "feedback": "..." }
  ],
  "recommendations": ["..."],
  "learning_plan": [
    { "topic": "Backpressure", "priority": "high", "reason": "...", "recommended_action": "..." }
  ],
  "hiring_recommendation": "strong_hire | hire | consider | no_hire",
  "confidence_score": 0.82,
  "generated_at": "2026-08-20T10:30:00Z"
}
```

Ứng dụng override `id`, `session_id`, `generated_at` sau Gemini tại [report_generator/agent.py#L16](../backend/services/report_generator/agent.py#L16).

### 13.4. Mismatch snapshot nghiêm trọng

**Hiện ReportService reload Candidate Profile mới nhất từ repository**, rồi truyền profile đó vào report generator tại [report_generator/service.py#L38](../backend/services/report_generator/service.py#L38), mặc dù session state đã chứa profile snapshot.

Hệ quả khi profile editing được triển khai: correction sau interview nhưng trước report generation có thể làm report dùng profile mới, trái ADR 0001/0007 về historical immutability. Cách đúng theo spec là report chỉ dùng snapshot đã persist trong session và exact `candidate_profile_version`.

### 13.5. Report persistence/history

- SQLite lưu report JSON trên row session tại [sqlite.py#L532](../backend/infrastructure/repositories/sqlite.py#L532).
- Firestore lưu `report` trong interview document, đồng thời set status/report_id/completed_at tại [firestore.py#L616](../backend/infrastructure/repositories/firestore.py#L616).
- `GET /api/v2/interview/{id}/report` đọc report owner-scoped.
- `GET /api/v2/interviews?candidate_id=&limit=&offset=` trả history, limit 1..100 tại [gateway/api/report.py#L45](../backend/gateway/api/report.py#L45).

Service-level report idempotency đã có cho request tuần tự. Firestore check-then-set và SQLite get-then-save chưa thể hiện một distributed transactional claim cho hai report request đồng thời.

## 14. Mô hình lưu trữ thực tế

### 14.1. SQLite

Các bảng chính tại [backend/models.py](../backend/models.py):

| Bảng | Nội dung |
| --- | --- |
| `users` | owner ID, name, `profile_json`, `profile_version`, `raw_resume_text` |
| `sessions` | candidate/owner, status, config summary, state JSON, report JSON |
| `messages` | serialized turns |
| `evaluations` | score/rubric legacy + current repository writes |
| `answer_submissions` | unique session+turn hash/status claim |
| `interview_blueprint_artifacts` | owner/candidate-scoped reusable plan |
| `resume_extraction_artifacts` | owner/content/version-scoped reusable profile extraction |

`profile_version` tồn tại và mặc định 1 nhưng `save_candidate_profile` hiện không increment tại [sqlite.py#L106](../backend/infrastructure/repositories/sqlite.py#L106).

### 14.2. Firestore

```text
users/{uid}
  candidates/{candidateId}
    name
    profile
    profile_version
    raw_resume_text
  resume_extraction_artifacts/{artifactKey}
  interview_blueprints/{artifactKey}
  interviews/{sessionId}
    candidate_id, status, state_payload, turns, evaluations, report
    answer_submissions/{hash(turnId)}
```

Profile version legacy backfill về 1 xảy ra khi read tại [firestore.py#L157](../backend/infrastructure/repositories/firestore.py#L157); save cũng giữ nguyên version thay vì increment.

### 14.3. Chưa có persistence theo spec

Không tìm thấy model/repository contract production cho:

- upload operation/status;
- idempotency record với `processing/completed/rejected/retryable_failure`;
- processing lease/heartbeat/fencing generation;
- Profile Audit Event;
- extraction warning acknowledgement;
- immutable evidence ID/provenance record;
- session `candidate_profile_version` riêng.

## 15. API inventory: runtime và target

| Method/path | Runtime | Ghi chú |
| --- | --- | --- |
| `POST /api/v2/resume/upload` | **IMPLEMENTED** | synchronous initial upload, không Idempotency-Key |
| `GET /api/v2/candidates/{id}/profile` | **IMPLEMENTED** | profile + readiness + ETag |
| `PATCH /api/v2/candidates/{id}/profile` | **SPEC/PENDING** | correction + If-Match |
| `POST /api/v2/candidates/{id}/resume` | **SPEC/PENDING** | atomic Replacement Upload |
| `GET /api/v2/resume/uploads/{upload_id}` hoặc status URL tương đương | **SPEC/PENDING** | owner-scoped polling |
| `POST /api/v2/interview/prepare` | **IMPLEMENTED** | warm/deduplicate plan |
| `POST /api/v2/interview/start` | **PARTIAL** | start works; readiness/snapshot transaction missing |
| `POST /api/v2/interview/{id}/answer` | **IMPLEMENTED** | text + answer idempotency |
| `GET /api/v2/interview/{id}` | **IMPLEMENTED** | reload session state |
| `WS /api/v2/voice/interview/{id}` | **IMPLEMENTED source** | full voice/transcription/playback |
| `POST /api/v2/interview/{id}/report` | **PARTIAL** | works/idempotent sequentially; wrong profile source risk |
| `GET /api/v2/interview/{id}/report` | **IMPLEMENTED** | owner-scoped |
| `GET /api/v2/interviews` | **IMPLEMENTED** | offset pagination |

## 16. External integrations và cấu hình

### 16.1. Vertex Gemini

Default routing tại [core/settings.py#L44](../backend/core/settings.py#L44):

| Task | Model route mặc định | Ghi chú |
| --- | --- | --- |
| Resume extraction | `gemini-2.5-flash-lite`, location `global` | riêng service, max attempt 1 |
| Planner/question | `gemini-2.5-flash` | task simple |
| Text evaluator/report | `gemini-2.5-pro` mặc định | task complex |
| Voice evaluator | simple model | critical latency path |

Vertex adapter dùng ADC, structured JSON/Pydantic validation, timeout mặc định 60 giây và retry config mặc định 3 lần, trừ resume service override max attempt 1 tại [vertex_gemini.py#L50](../backend/infrastructure/llm/vertex_gemini.py#L50) và [core/dependencies.py#L101](../backend/core/dependencies.py#L101).

### 16.2. Repository

- `REPOSITORY_BACKEND=sqlite|firestore`;
- SQLite cần DB session;
- Firestore cần `GOOGLE_CLOUD_PROJECT`, database/collection settings;
- factory tại [core/dependencies.py#L56](../backend/core/dependencies.py#L56).

### 16.3. Knowledge

- `INTERVIEW_KNOWLEDGE_BACKEND=local|firestore_vector`;
- vector model mặc định `gemini-embedding-001`, dimension 768, top-k 5;
- settings tại [core/settings.py#L164](../backend/core/settings.py#L164).

### 16.4. Speech

- Local: Silero VAD + faster-whisper + VieNeu-TTS.
- Remote: `SPEECH_SERVICE_URL` và optional `SPEECH_SERVICE_TOKEN`.
- Speech service riêng có `/health`, `/ready` và WebSocket inference; composition chọn local/remote tại [core/dependencies.py#L132](../backend/core/dependencies.py#L132).

### 16.5. Frontend

- `VITE_API_BASE_URL` quyết định REST/WS base URL;
- Firebase client lấy current user/token;
- API adapter retry đúng một lần sau 401;
- frontend hiện không gửi `Idempotency-Key` và không có PATCH/If-Match adapter tại [frontend/src/lib/api.ts#L196](../frontend/src/lib/api.ts#L196).

## 17. Test coverage theo seam

### 17.1. Những seam đã có test đáng kể

| Seam | Bằng chứng |
| --- | --- |
| Actual file detection, malformed DOCX, OCR success/fail/timeout | [test_document_processing.py#L26](../backend/app/tests/test_document_processing.py#L26) |
| Resume structured extraction, non-resume rejection, evidence limits | [test_resume_agent.py#L36](../backend/app/tests/test_resume_agent.py#L36) |
| Upload persistence, safe LLM error, cache owner-scope, partial status | [test_resume_upload_v2.py#L89](../backend/app/tests/test_resume_upload_v2.py#L89) |
| Profile ownership, ETag, readiness response | [test_candidate_profile_api.py#L75](../backend/app/tests/test_candidate_profile_api.py#L75) |
| Readiness rules/all issues/NFKC/legacy education | [test_candidate_profile_readiness.py#L10](../backend/app/tests/test_candidate_profile_readiness.py#L10) |
| Blueprint key/cache/concurrent prepare | [test_interview_preparation.py#L19](../backend/app/tests/test_interview_preparation.py#L19) |
| Text start/voice mode/prepare reuse/opening/replay/reload | [test_interview_api.py#L183](../backend/app/tests/test_interview_api.py#L183) |
| Adaptive follow-up/difficulty/finish/memory/prefetch | [test_interview_orchestrator.py#L93](../backend/app/tests/test_interview_orchestrator.py#L93) |
| Concurrent answer claim/conflict/stale turn | [test_answer_submission_idempotency.py#L130](../backend/app/tests/test_answer_submission_idempotency.py#L130) |
| Voice auth/origin/ownership/mode/events/reconnect/barge-in/limits | [test_voice_websocket.py#L505](../backend/app/tests/test_voice_websocket.py#L505) |
| Audio batching/VAD/STT language/hotwords/privacy | [test_voice_audio_pipeline.py#L107](../backend/app/tests/test_voice_audio_pipeline.py#L107) |
| Report complete-only/idempotency/history | [test_report_service.py#L120](../backend/app/tests/test_report_service.py#L120) |
| SQLite và Firestore parity cơ bản | [test_sqlite_repository.py#L30](../backend/app/tests/test_sqlite_repository.py#L30), [test_firestore_repository.py#L166](../backend/app/tests/test_firestore_repository.py#L166) |
| Frontend API/profile/setup/text/voice/report pages | [frontend/src/lib/api.test.ts](../frontend/src/lib/api.test.ts), [frontend/src/pages/CandidateProfilePage.test.tsx](../frontend/src/pages/CandidateProfilePage.test.tsx) |

### 17.2. Contract suites còn thiếu theo normative testing seams

[RESUME_REVIEW_TESTING_SEAMS.md](RESUME_REVIEW_TESTING_SEAMS.md) yêu cầu nhưng runtime/test hiện chưa hoàn chỉnh cho:

- strict correction payload, alias/read-only rejection;
- `If-Match` parser và all precondition statuses;
- two-writer profile version atomicity trên cả SQLite/Firestore;
- evidence ID backfill/provenance/audit;
- upload idempotency lifecycle, replay, lease/fencing/status ownership;
- atomic replacement và stale replacement commit;
- start readiness parity text/voice;
- atomic snapshot version selection;
- report bất biến sau profile update;
- frontend dirty draft/conflict/reload/replacement/polling state;
- full responsive + keyboard + screen-reader review editor checks.

### 17.3. Offline system evaluation harness

Ngoài unit/integration tests, repo có evaluation runner nhận manifest gồm CV, STT, TTS, question, evaluator và voice-turn cases; runner chạy các evaluator rồi xuất JSON/Markdown tại [system_evaluation/runner.py#L15](../backend/services/system_evaluation/runner.py#L15) và [run_system_evaluation.py#L36](../backend/scripts/run_system_evaluation.py#L36).

Metrics utility có edit distance/WER-like counts, skill precision-recall-F1, profile-field match, average/percentile/deviation tại [system_evaluation/metrics.py#L14](../backend/services/system_evaluation/metrics.py#L14). Các artifact milestone nằm dưới `docs/evaluation/`; chúng là evidence offline, không phải runtime request path.

### 17.4. Validation thực tế khi lập tài liệu

Hai nhóm focused tests được chạy từ `backend/` trên đúng worktree đã khảo sát:

```powershell
& '.venv/Scripts/python.exe' -m pytest app/tests/test_candidate_profile_api.py app/tests/test_candidate_profile_readiness.py app/tests/test_candidate_profile_normalization.py app/tests/test_resume_upload_v2.py app/tests/test_document_processing.py app/tests/test_interview_api.py app/tests/test_report_service.py -q
```

Kết quả: `38 passed, 1 warning in 7.57s`.

```powershell
& '.venv/Scripts/python.exe' -m pytest app/tests/test_interview_planner_agent.py app/tests/test_question_generator_agent.py app/tests/test_evaluator_agent.py app/tests/test_interview_orchestrator.py app/tests/test_report_agent.py app/tests/test_report_api.py -q
```

Kết quả: `33 passed, 1 warning in 2.26s`.

Cả hai warning đều là `StarletteDeprecationWarning` từ `fastapi/testclient.py` về việc dùng httpx với `starlette.testclient`; không có test failure. Đây là focused validation cho pipeline, không phải full backend/frontend suite.

## 18. IMPLEMENTED vs SPEC/PENDING — ma trận chi tiết

| Năng lực | Trạng thái | Nhận xét chính |
| --- | --- | --- |
| PDF/DOCX <= 10 MiB | IMPLEMENTED | route dùng hardcoded 10 MiB |
| Actual signature/MIME validation | IMPLEMENTED | PDF header, DOCX ZIP members |
| OCR image/sparse PDF | IMPLEMENTED | ADR 0004 cần cập nhật để phản ánh runtime |
| >= 50 normalized chars | IMPLEMENTED | phần lớn structured; compatibility branch còn generic detail |
| Non-resume classification | IMPLEMENTED | Gemini + threshold 0.7, 10 tech domains |
| Section-aware 16k context | IMPLEMENTED | omitted content -> partial warning |
| Structured Candidate Profile | IMPLEMENTED | chưa strict correction model/evidence ID |
| Rule-based verification | PARTIAL | provenance không persist/return |
| Extraction reuse cache | IMPLEMENTED | tránh model call; không phải idempotency |
| Initial upload atomicity | PENDING | nhiều commits/writes riêng |
| Upload Idempotency-Key | PENDING | frontend/backend đều chưa có |
| Upload status/lease/fencing | PENDING | chưa có model/route/repository |
| Partial Extraction response | PARTIAL | backend trả metadata; frontend type/UI bỏ qua |
| Candidate Profile GET/ETag | IMPLEMENTED | strong ETag read-only |
| Profile version increment | PENDING | version giữ nguyên 1 |
| Profile PATCH/If-Match | PENDING | không có route/schema |
| Durable editable review UI | PENDING | current page read-only |
| Replacement Upload | PENDING | không có route/transaction |
| Readiness evaluator | IMPLEMENTED | profile GET dùng |
| Readiness gate on `/start` | PENDING | API hiện bypass được |
| Prepare/cache/persistent blueprint | IMPLEMENTED | key có owner/profile version/config |
| Local curated knowledge | IMPLEMENTED | lexical retrieval |
| Firestore vector knowledge | IMPLEMENTED source | cần operational index/config |
| Planner/question generation | IMPLEMENTED | structured Gemini output |
| Text opening + adaptive loop | IMPLEMENTED | answer claim/replay có test |
| Voice realtime loop | IMPLEMENTED source | deployment/load evidence là chuyện riêng |
| Session profile content snapshot | PARTIAL | có trong state, thiếu atomic version contract |
| Final report | IMPLEMENTED | sequential reuse đã có |
| Historical report profile immutability | PENDING/BUG | report reload latest profile |

## 19. Rủi ro và ưu tiên sửa

### P0 — correctness/contract

1. **Readiness bypass:** `/start` phải gọi cùng validator và trả `422 profile_not_interview_ready` với toàn bộ issues trước planner/session creation.
2. **Report dùng sai profile source:** bỏ reload current Candidate Profile; dùng session snapshot và recorded version.
3. **Snapshot không nguyên tử:** repository cần operation “read latest owned profile + create session snapshot/version” trong transaction trước orchestration.
4. **Profile version chỉ trang trí:** hiện ETag/version không bảo vệ write vì không có PATCH/If-Match/increment.
5. **Upload không nguyên tử:** nhiều commit có thể để orphan/half-persisted candidate.

### P0 — upload recovery/security contract

6. Thêm Idempotency-Key, fingerprint binding, processing/completed/rejected/retryable states, 24h retention, 30m lease và fencing.
7. Thêm explicit multipart cardinality và đồng nhất structured error cho size/insufficient text/auth.
8. Partial Extraction backend đã có nhưng frontend không parse/render warning.

### P1 — profile review/provenance

9. Tách strict correction schema khỏi response model; forbid unknown/alias/read-only fields.
10. Backfill/persist `evidence_id`, source metadata và audit events.
11. Xây durable editor, dirty state, save conflict và replacement UI.
12. Đồng bộ ADR 0004/spec với OCR runtime hiện tại.

### P1 — concurrency/operations

13. Persistent blueprint save của Firestore và report generation cần audit thêm cho concurrent cross-instance behavior.
14. `question_count` và number of plan rounds cần invariant rõ để không kết thúc sớm ngoài ý muốn.
15. Voice source có test sâu nhưng vẫn cần deployment/load/admission-control evidence trước khi gọi là production-ready.

## 20. Sequence chuẩn mục tiêu sau khi đóng các gap

```text
1. User sign-in -> Firebase token
2. Select exactly one PDF/DOCX -> client creates opaque Idempotency-Key
3. POST upload -> backend claims owner/key/fingerprint before extraction
4. Detect actual document -> extract full text/OCR -> classify Resume
5. Build structured profile -> verify -> persist profile/version/audit/warning atomically
6. Return/poll terminal upload result -> navigate canonical profile route
7. GET profile -> Profile + ETag + readiness + warnings/provenance metadata
8. User reviews/edits -> PATCH canonical fields with If-Match
9. Backend validates/normalizes -> atomic compare/write/version++/audit
10. Client sees clean, saved, backend-ready profile
11. POST start with candidate_id + config only
12. Transaction selects latest profile/version and creates immutable session snapshot
13. Planner retrieves curated knowledge and creates/reuses versioned blueprint
14. Generator creates first question
15. Text/voice answers use same idempotent answer service and evaluator
16. Deterministic policy selects follow-up/difficulty/next/end
17. Completed session generates report only from stored session snapshot/turns
18. Report and history remain unchanged after later profile corrections/replacements
```

## 21. Kết luận ngắn

Pipeline hiện tại đã đi được trọn đường kỹ thuật từ file PDF/DOCX đến text/OCR, structured profile, planning, adaptive text/voice interview, answer evaluation và final report. “Output trích CV” không đi thẳng vào generator: nó phải được persist thành Candidate Profile có `candidate_id`, kết hợp với InterviewConfig, qua planning/knowledge retrieval để tạo InterviewPlan, rồi một selected round mới đi vào Question Generator.

Tuy nhiên, không nên diễn giải hệ thống hiện tại như Resume Review contract đã hoàn tất. Những phần quan trọng nhất còn thiếu là writable/versioned profile, upload idempotency và recovery, atomic replacement, readiness enforcement, atomic snapshot version, và report immutability. Đây là ranh giới rõ giữa demo pipeline đang chạy và contract production an toàn đã được ADR/spec định nghĩa.
