# BÁO CÁO TỔNG QUAN ĐỒ ÁN TỐT NGHIỆP

## Nền tảng phỏng vấn kỹ thuật ứng dụng trí tuệ nhân tạo — Fipilot

> **Trường:** `[Điền tên trường]`<br>
> **Khoa/Bộ môn:** `[Điền khoa hoặc bộ môn]`<br>
> **Ngành:** `[Điền ngành học]`<br>
> **Sinh viên thực hiện:** `[Họ tên – MSSV]`<br>
> **Giảng viên hướng dẫn:** `[Họ tên giảng viên]`<br>
> **Niên khóa:** `[Điền niên khóa]`<br>
> **Ngày chốt nội dung kỹ thuật:** 03/08/2026<br>
> **Tên repository:** `ai-interview-platform`<br>
> **Nhánh khảo sát:** `restore/first-deploy-frontend`<br>
> **Commit tham chiếu:** `e4ea78cfef37f95061db08b928a4acdecb39f811`

---

## Hướng dẫn sử dụng tài liệu

Tài liệu này tổng hợp trạng thái thực tế của mã nguồn để làm cơ sở viết báo cáo và chuẩn bị bảo vệ đồ án. Các nội dung được chia thành ba mức:

- **Đã triển khai:** có bằng chứng trực tiếp trong mã nguồn hoặc báo cáo triển khai.
- **Đặc tả đã duyệt:** đã được thiết kế trong ADR/spec nhưng chưa hoàn tất ở runtime.
- **Đề xuất:** hướng cải tiến, không được trình bày như kết quả đã hoàn thành.

Khi có khác biệt, thứ tự ưu tiên nguồn là: mã nguồn active tại `gateway`, `shared`, `services`, `orchestrator`, `infrastructure` → kiểm thử → tài liệu triển khai → ADR/spec → tài liệu cũ. Tệp [AI_Interview_Platform_Documentation_VI.md](AI_Interview_Platform_Documentation_VI.md) mô tả một kiến trúc legacy và không phải nguồn chuẩn cho runtime V2 hiện tại.

---

## Mục lục

1. Tóm tắt đồ án
2. Bối cảnh và bài toán
3. Mục tiêu, phạm vi và đối tượng sử dụng
4. Yêu cầu hệ thống
5. Ma trận trạng thái chức năng
6. Kiến trúc tổng thể
7. Công nghệ sử dụng
8. Cấu trúc mã nguồn
9. Mô hình miền và dữ liệu
10. Kiến trúc AI và cơ chế phỏng vấn thích ứng
11. Các luồng nghiệp vụ chính
12. Danh mục API
13. Thiết kế frontend
14. Thiết kế backend và speech service
15. Bảo mật, phân quyền và quyền riêng tư
16. Độ tin cậy, hiệu năng và khả năng mở rộng
17. Kiểm thử và bằng chứng chất lượng
18. Cài đặt và chạy dự án
19. Cấu hình môi trường
20. Triển khai production
21. Đóng góp kỹ thuật nổi bật
22. Hạn chế và rủi ro hiện tại
23. Hướng phát triển
24. Kịch bản demo
25. Gợi ý bố cục báo cáo và slide
26. Câu hỏi bảo vệ thường gặp
27. Thuật ngữ
28. Kết luận
29. Phụ lục lệnh kiểm tra và nguồn tham khảo

---

## 1. Tóm tắt đồ án

Fipilot là nền tảng luyện phỏng vấn kỹ thuật dựa trên Resume. Người dùng đăng nhập bằng Google/Firebase, tải Resume định dạng PDF hoặc DOCX, nhận Candidate Profile do AI trích xuất, cấu hình buổi phỏng vấn và trả lời bằng văn bản hoặc giọng nói. Hệ thống sử dụng Gemini để lập kế hoạch, sinh câu hỏi, đánh giá câu trả lời và tạo báo cáo cuối buổi. Mô tả miền chính thức của sản phẩm được ghi tại [CONTEXT.md](../CONTEXT.md#fipilot).

Kiến trúc hiện tại gồm ba tiến trình:

1. React web client tại cổng `5173`.
2. FastAPI gateway tại cổng `8000`.
3. Speech inference service tại cổng `9000`.

Cách tổ chức này cho phép phần nghiệp vụ và AI text giữ trong modular monolith, trong khi STT/VAD/TTS được tách riêng vì có yêu cầu GPU, model cache và luồng âm thanh khác biệt. Kiến trúc được mô tả trong [README.md](../README.md#ai-interview-platform), [local-architecture.md](local-architecture.md#local-architecture) và [SYSTEM_DESIGN_VI.md](SYSTEM_DESIGN_VI.md#3-kiến-trúc-tổng-thể).

### Từ khóa

`AI Interview`, `Resume Parsing`, `Candidate Profile`, `Adaptive Interview`, `Gemini`, `FastAPI`, `React`, `Firebase`, `Firestore`, `WebSocket`, `Speech-to-Text`, `Text-to-Speech`.

---

## 2. Bối cảnh và bài toán

### 2.1. Bối cảnh

Ứng viên kỹ thuật thường gặp ba khó khăn:

- Không biết nhà tuyển dụng sẽ tập trung vào phần nào trong kinh nghiệm cá nhân.
- Thiếu môi trường luyện tập có câu hỏi tiếp nối và độ khó thích ứng.
- Khó tự đánh giá đồng thời kiến thức, chiều sâu, tính đúng đắn và cách giao tiếp.

Một bộ câu hỏi cố định không tận dụng được nội dung Resume và không phản ứng theo chất lượng câu trả lời. Vì vậy, đồ án xây dựng một AI interviewer có khả năng tạo phiên phỏng vấn riêng cho từng Candidate Profile.

### 2.2. Phát biểu bài toán

Đầu vào của hệ thống gồm:

- Danh tính người dùng đã xác thực.
- Resume PDF/DOCX.
- Cấu hình phỏng vấn: hình thức, ngôn ngữ, cấp độ, thời lượng, phong cách, mục tiêu và số câu.
- Câu trả lời văn bản hoặc âm thanh theo từng lượt.

Đầu ra gồm:

- Candidate Profile có cấu trúc.
- Interview Plan và chuỗi câu hỏi thích ứng.
- Đánh giá chi tiết từng câu trả lời.
- Báo cáo tổng hợp, gợi ý học tập và khuyến nghị.
- Lịch sử phiên có thể tải lại theo đúng chủ sở hữu.

### 2.3. Giá trị của giải pháp

- Cá nhân hóa nội dung theo Resume thay vì chỉ theo chức danh chung.
- Tự động hóa pipeline từ đọc tài liệu đến báo cáo.
- Hỗ trợ cả luyện tập text và trải nghiệm hội thoại voice.
- Lưu state để có thể khôi phục phiên.
- Tách quyền sở hữu dữ liệu theo Firebase `uid`.

### 2.4. Phương pháp thực hiện đồ án

Đồ án được triển khai theo hướng phân rã contract và kiểm chứng từng seam:

1. Phân tích bài toán và xây dựng ngôn ngữ miền cho Resume, Candidate Profile và Interview Session.
2. Định nghĩa Pydantic/TypeScript contract trước khi nối transport và persistence.
3. Tách các tác vụ AI thành Resume, Planner, Question, Evaluator và Report agent.
4. Dùng rule-based orchestrator để điều phối đầu ra AI qua nhiều lượt.
5. Xây repository abstraction rồi kiểm thử cùng hành vi trên SQLite và Firestore.
6. Xây text flow trước, sau đó dùng chung domain state cho voice flow.
7. Viết unit, integration, API, ownership và resilience tests theo public seam.
8. Triển khai text lên Firebase Hosting/Cloud Run và ghi nhận kết quả E2E.
9. Dùng ADR/spec để quản lý các contract Resume Review chưa hoàn tất thay vì ghép hành vi tạm thời vào production.

---

## 3. Mục tiêu, phạm vi và đối tượng sử dụng

### 3.1. Mục tiêu tổng quát

Xây dựng một nền tảng web có thể mô phỏng phỏng vấn kỹ thuật cá nhân hóa, đánh giá câu trả lời bằng AI và trả kết quả có cấu trúc, đồng thời bảo đảm xác thực và cô lập dữ liệu người dùng.

### 3.2. Mục tiêu cụ thể

- Đọc Resume PDF/DOCX tối đa 10 MB.
- Chuẩn hóa nội dung thành Candidate Profile bằng Pydantic contract.
- Lập kế hoạch phỏng vấn theo hồ sơ và cấu hình.
- Sinh câu hỏi tiếng Việt hoặc tiếng Anh.
- Chấm điểm trên thang 0–10 và cung cấp feedback.
- Chọn follow-up hoặc tăng độ khó dựa trên kết quả.
- Hỗ trợ REST cho text và WebSocket cho voice.
- Lưu session, turn, evaluation và report bằng SQLite hoặc Firestore.
- Dùng Firebase ID token và ownership check cho tài nguyên riêng tư.
- Cung cấp health/readiness, logging và bộ kiểm thử tự động.

### 3.3. Phạm vi đã triển khai

- Đăng nhập Google qua Firebase.
- Upload và phân tích Resume.
- Xem Candidate Profile đã lưu, Profile Version, ETag và Interview Readiness.
- Phỏng vấn text thích ứng.
- Mã nguồn phỏng vấn voice realtime end-to-end.
- Báo cáo cuối buổi và lịch sử phiên.
- SQLite cho local, Firestore cho production.
- Firebase Hosting và Cloud Run cho production text.

### 3.4. Ngoài phạm vi hiện tại

- Hệ thống quản trị tuyển dụng nhiều vai trò.
- Đặt lịch và gửi thư mời phỏng vấn.
- OCR cho Resume scan dạng ảnh.
- Tự huấn luyện mô hình nền tảng.
- Lưu hoặc phát lại audio.
- Dashboard phân tích cấp doanh nghiệp.
- Knowledge base/RAG hoàn chỉnh; seam hiện chỉ được dự phòng tại [retriever.py](../backend/services/interview_knowledge/retriever.py#L1).

### 3.5. Đối tượng sử dụng

| Đối tượng | Nhu cầu chính |
| --- | --- |
| Ứng viên | Tải Resume, luyện text/voice, xem feedback và lịch sử |
| Người phát triển | Chạy local, thay repository/model, kiểm thử từng seam |
| Người vận hành | Theo dõi health/readiness, log, cấu hình Cloud Run/Firestore |
| Giảng viên/hội đồng | Đánh giá kiến trúc, AI pipeline, bảo mật và mức độ hoàn thiện |

### 3.6. Use case chính

| Actor | Use case | Tiền điều kiện | Kết quả |
| --- | --- | --- | --- |
| Ứng viên | Đăng nhập Google | Có tài khoản Google | Có Firebase session |
| Ứng viên | Upload Resume | Đã đăng nhập; file hợp lệ | Candidate Profile được persist |
| Ứng viên | Xem Candidate Profile | Sở hữu candidate ID | Profile, version và readiness hiển thị |
| Ứng viên | Cấu hình phỏng vấn | Có Candidate Profile | Interview Config sẵn sàng |
| Ứng viên | Thực hiện text interview | Session text đã tạo | Turn/evaluation được persist |
| Ứng viên | Thực hiện voice interview | Session voice và speech service ready | Transcript và turn được xử lý realtime |
| Ứng viên | Xem báo cáo | Session đã hoàn tất | Report được sinh hoặc tải lại |
| Ứng viên | Xem lịch sử | Đã đăng nhập | Danh sách session thuộc user |
| Hệ thống vận hành | Kiểm tra health/readiness | Service đang chạy | Trạng thái liveness/dependency |

Quan hệ chính có thể trình bày trong sơ đồ use case: `Đăng nhập` là tiền điều kiện chung; `Upload Resume` bao gồm `Extract document` và `Generate Candidate Profile`; `Thực hiện phỏng vấn` có hai chuyên biệt `Text` và `Voice`; `Voice` bao gồm `STT`, `VAD` và `TTS`; `Xem báo cáo` mở rộng từ một session đã hoàn tất.

---

## 4. Yêu cầu hệ thống

### 4.1. Yêu cầu chức năng

| Mã | Yêu cầu |
| --- | --- |
| FR-01 | Người dùng đăng nhập Google và chỉ truy cập dữ liệu thuộc `uid` của mình |
| FR-02 | Hệ thống nhận đúng một Resume PDF/DOCX tối đa 10 MB |
| FR-03 | Hệ thống trích text và dùng Gemini tạo Candidate Profile có cấu trúc |
| FR-04 | Người dùng xem lại hồ sơ và trạng thái sẵn sàng phỏng vấn |
| FR-05 | Người dùng cấu hình mode, ngôn ngữ, level, style, thời lượng và số câu |
| FR-06 | AI tạo Interview Plan và câu hỏi đầu tiên |
| FR-07 | Mỗi câu trả lời được đánh giá và dùng để quyết định lượt tiếp theo |
| FR-08 | Text interview hoạt động qua REST |
| FR-09 | Voice interview hoạt động qua WebSocket, STT, VAD và TTS |
| FR-10 | Phiên hoàn tất có thể sinh và đọc lại report |
| FR-11 | Người dùng xem lịch sử có phân trang |
| FR-12 | Hệ thống cung cấp health và readiness endpoint |

### 4.2. Yêu cầu phi chức năng

| Nhóm | Yêu cầu/định hướng |
| --- | --- |
| Bảo mật | Firebase token, ownership, CORS/origin allowlist, token nội bộ cho speech |
| Riêng tư | Xóa file Resume tạm; không persist audio; không log token/body/audio |
| Đúng đắn | Structured output và Pydantic validation cho kết quả LLM |
| Khôi phục | Persist toàn bộ Interview Session State |
| Mở rộng | Gateway/Firestore scale ngang; speech worker scale theo GPU |
| Khả dụng | Tách `/health` và `/ready`; retry lỗi Gemini tạm thời |
| Truy vết | Request correlation và structured log |
| Khả năng bảo trì | Phân lớp gateway, service, orchestrator, infrastructure và shared schema |

Các mục tiêu latency trong [SYSTEM_DESIGN_VI.md](SYSTEM_DESIGN_VI.md#22-yêu-cầu-phi-chức-năng) là SLO đề xuất, chưa phải benchmark đã đo.

---

## 5. Ma trận trạng thái chức năng

| Chức năng | Trạng thái tại commit khảo sát | Bằng chứng/lưu ý |
| --- | --- | --- |
| Google/Firebase login | Đã triển khai | [AuthContext.tsx](../frontend/src/contexts/AuthContext.tsx#L1) |
| Firebase bearer-token verification | Đã triển khai | [firebase.py](../backend/infrastructure/auth/firebase.py#L18) |
| Ownership candidate/session/report | Đã triển khai | Repository luôn nhận `user_id` |
| Upload PDF/DOCX ≤ 10 MB | Đã triển khai | [resume.py](../backend/gateway/api/resume.py#L23) |
| Extract PDF/DOCX text | Đã triển khai | [pdf_service.py](../backend/infrastructure/documents/pdf_service.py#L9) |
| Candidate Profile bằng Gemini | Đã triển khai | [profile_scanner/agent.py](../backend/services/profile_scanner/agent.py#L1) |
| Profile GET + strong ETag | Đã triển khai | [candidate_profile.py](../backend/gateway/api/candidate_profile.py#L15) |
| Backend readiness evaluator | Đã triển khai | [readiness.py](../backend/services/candidate_profile/readiness.py#L17) |
| Profile editor/PATCH | Đặc tả đã duyệt, chưa có runtime | [RESUME_REVIEW_UI_SPEC.md](RESUME_REVIEW_UI_SPEC.md#candidate-profile-resource) |
| `If-Match` và stale-version `412` | Đặc tả đã duyệt, chưa có runtime | [ADR 0007](adr/0007-use-owned-versioned-candidate-profile-resources.md) |
| Replacement Upload | Đặc tả đã duyệt, chưa có runtime | [ADR 0005](adr/0005-idempotent-atomic-resume-upload-retries.md) |
| Upload idempotency/status resource | Đặc tả đã duyệt, chưa có runtime | [ADR 0009](adr/0009-use-recoverable-resume-upload-operations.md) |
| Text interview | Đã triển khai và production report xác nhận | [interview.py](../backend/gateway/api/interview.py#L74), [DEPLOYMENT_REPORT.md](../DEPLOYMENT_REPORT.md#remote-verification) |
| Voice interview source | Đã triển khai trong source | [voice.py](../backend/gateway/api/voice.py#L147) |
| Voice production | Chưa có bằng chứng deploy mới | Report 23/07/2026 chỉ xác nhận Phase 1 text |
| Adaptive follow-up/difficulty | Đã triển khai | [decision_service.py](../backend/orchestrator/decision_service.py#L6) |
| Report generation/read | Đã triển khai | [report.py](../backend/gateway/api/report.py#L29) |
| Interview history | Đã triển khai | [report.py](../backend/gateway/api/report.py#L64) |
| SQLite/Firestore adapters | Đã triển khai | [repositories](../backend/infrastructure/repositories) |
| Template/Knowledge assets trong runtime | Chưa được nối vào orchestration V2 | `KnowledgeRetriever` mới là protocol tương lai |
| Proctoring/chuyển tab | Không có trong active V2 | Chỉ xuất hiện ở tài liệu/field legacy |

Điểm cần trình bày trung thực: các ADR 0001–0012 là quyết định thiết kế ràng buộc cho Resume Review, nhưng không tự động chứng minh tất cả chức năng đã có trong runtime.

---

## 6. Kiến trúc tổng thể

### 6.1. Sơ đồ ngữ cảnh

![System context](diagrams/01-system-context.svg)

Người dùng tương tác với React SPA. Frontend lấy Firebase ID token, gửi REST/WebSocket đến gateway. Gateway điều phối domain service, Firestore/SQLite, Vertex AI Gemini và speech service.

### 6.2. Sơ đồ container

![Container architecture](diagrams/02-container-architecture.svg)

| Container | Công nghệ | Trách nhiệm |
| --- | --- | --- |
| Web Client | React 18, TypeScript, Vite | UI, auth, upload, text/voice room, report/history |
| API Gateway | FastAPI, Python 3.12, Uvicorn | Auth, API, orchestration, persistence, Gemini |
| Speech Service | FastAPI WebSocket, faster-whisper, Silero VAD, VieNeu | STT/VAD/TTS và streaming audio |
| Firebase Auth | Managed service | Google login và ID token |
| Firestore | Managed NoSQL | Candidate, interview state, turns, evaluations, report |
| Vertex AI Gemini | Managed AI | Resume, plan, question, evaluation, report |

### 6.3. Kiểu kiến trúc

Backend là **modular monolith**: các module nghiệp vụ chạy cùng gateway nhưng có seam rõ. Speech inference là service riêng. Lựa chọn này giảm network hop và giữ shared state/schema đơn giản trong giai đoạn đồ án, đồng thời vẫn tách phần cần GPU để scale độc lập. Lập luận đầy đủ nằm tại [SYSTEM_DESIGN_VI.md](SYSTEM_DESIGN_VI.md#32-vì-sao-dùng-modular-monolith).

### 6.4. Luồng phụ thuộc

```text
Gateway API
  -> Domain services / Interview Orchestrator
    -> Repository, LLM, document, speech interfaces
      -> Firebase / Firestore / SQLite / Vertex / local or remote speech
```

`backend/core/dependencies.py` là composition root, quyết định implementation theo cấu hình môi trường.

---

## 7. Công nghệ sử dụng

### 7.1. Frontend

| Công nghệ | Vai trò |
| --- | --- |
| React 18 | Component UI |
| TypeScript | Kiểu dữ liệu và client contract |
| Vite | Dev server và production build |
| React Router 6 | Điều hướng SPA |
| TanStack Query 5 | Hạ tầng server-state |
| Zustand 4 | App state nhẹ |
| Firebase Web SDK | Google sign-in, token |
| Tailwind CSS 3 | Design tokens và responsive UI |
| Lucide React | Icon |
| Vitest + Testing Library | Unit/component tests |

Phiên bản phụ thuộc nằm tại [frontend/package.json](../frontend/package.json).

### 7.2. Backend

| Công nghệ | Vai trò |
| --- | --- |
| Python ≥ 3.12 | Runtime |
| FastAPI/Uvicorn | REST và WebSocket |
| Pydantic/Pydantic Settings | Schema và typed configuration |
| SQLAlchemy/SQLite | Persistence local |
| Firebase Admin | Verify ID token |
| Google Cloud Firestore | Persistence production |
| Google Gen AI SDK | Vertex Gemini |
| pypdf/python-docx | Extract Resume |
| pytest | Backend tests |

Nguồn: [pyproject.toml](../backend/pyproject.toml) và [requirements.txt](../backend/requirements.txt).

### 7.3. Speech/AI

| Công nghệ | Vai trò |
| --- | --- |
| Gemini 2.5 Flash | Tác vụ nhanh: plan/question và mặc định simple |
| Gemini 2.5 Pro | Tác vụ complex như evaluation/report |
| Gemini 2.5 Flash-Lite | Resume extraction mặc định |
| faster-whisper | Speech-to-Text |
| Silero VAD | Phát hiện vùng có giọng nói |
| VieNeu | Text-to-Speech tiếng Việt |
| Torch/Torchaudio | Runtime speech model |

Model là cấu hình, không hard-code vào business contract; giá trị mặc định được định nghĩa tại [settings.py](../backend/core/settings.py#L37) và speech dependency tại [requirements-speech.txt](../backend/requirements-speech.txt).

---

## 8. Cấu trúc mã nguồn

```text
ai-interview-platform/
├─ frontend/
│  ├─ src/pages/                 Các trang production
│  ├─ src/components/            Layout, UI, Candidate Profile, voice
│  ├─ src/contexts/              Firebase authentication context
│  ├─ src/lib/api.ts             API client tập trung
│  ├─ src/types/                 Canonical client contracts
│  └─ prototypes/                Thiết kế thử, không phải production
├─ backend/
│  ├─ gateway/api/               REST và WebSocket adapters
│  ├─ core/                      Settings, DI, startup, middleware, log
│  ├─ shared/schemas/            Pydantic domain/transport contracts
│  ├─ services/                  AI và domain services
│  ├─ orchestrator/              Adaptive interview workflow
│  ├─ infrastructure/            Auth, LLM, repository, document, speech
│  ├─ speech_service/            Tiến trình inference riêng
│  └─ app/tests/                 Test suite hiện hành
├─ docs/                         Spec, ADR, kiến trúc và hướng dẫn
├─ scripts/                      Script chạy local
├─ Knowledge/ và Template/       Tài sản kiến thức/câu hỏi, chưa nối active V2
└─ docker-compose.local.yml      Môi trường ba service
```

Các module trong `backend/app/` ngoài `app/tests` phần lớn là compatibility/legacy; entry point hiện hành là [gateway/main.py](../backend/gateway/main.py#L1), còn [backend/main.py](../backend/main.py#L1) chỉ re-export app để tương thích.

---

## 9. Mô hình miền và dữ liệu

### 9.1. Ngôn ngữ miền

Các khái niệm chuẩn gồm Resume, Candidate Profile, Profile Version, Interview Readiness, Interview Session, Interview Session Snapshot, Skill Evidence và Replacement Upload. Định nghĩa đầy đủ tại [CONTEXT.md](../CONTEXT.md#language).

### 9.2. Candidate Profile

Schema thực tế tại [candidate.py](../backend/shared/schemas/candidate.py#L8) gồm:

- `name`
- `years_experience`
- `recent_role`
- `specialization`
- `skills`
- `skill_evidence`
- `projects`
- `experiences`
- `education`
- metadata hiện hữu: `seniority_signal`, `confidence`, `confidence_score`, `extraction_method`

Nested structures:

```text
Project: name, description, technologies, role
Experience: company, title, start_date, end_date, description, technologies
Education: institution, degree, field_of_study, start_date, end_date
SkillEvidence hiện tại: skill, evidence[], source_section
```

`PersistedCandidateProfile` bổ sung `candidate_id` và `profile_version`. `education` vẫn đọc được dạng string legacy hoặc danh sách có cấu trúc.

### 9.3. Interview configuration và plan

`InterviewConfig` hỗ trợ:

- mode: `text` hoặc `voice`;
- language: `vi` hoặc `en`;
- experience level: `intern`, `junior`, `middle`, `senior`;
- duration: 5–180 phút;
- style: `technical`, `behavioral`, `mixed`;
- question count;
- objective;
- personality: `professional`, `friendly`, `challenging`, `supportive`.

`InterviewPlan` gồm nhiều round, mỗi round có topic, objective, difficulty, target skills, reasoning, weight và question budget. Contract nằm tại [interview.py](../backend/shared/schemas/interview.py#L31).

### 9.4. Interview Session State

State được persist gồm:

- Candidate Profile snapshot trong payload;
- Interview Config;
- Interview Plan;
- current turn và completed turns;
- current question index;
- memory;
- voice analytics.

Session lifecycle chính:

```text
created -> in_progress/interviewing -> completed/ended -> report_generated
```

### 9.5. Evaluation

Mỗi answer có các điểm 0–10: technical, depth, communication, engineering mindset, correctness và overall; kèm strengths, weaknesses, missing topics/concepts, feedback và follow-up signal. Xem [evaluation.py](../backend/shared/schemas/evaluation.py#L6).

### 9.6. Report

Report gồm overall/technical/communication/correctness score, summary, strengths, weaknesses, demonstrated/missing skills, skill assessments, recommendations, learning plan, confidence và một trong bốn hiring recommendation. Xem [report schemas](../backend/services/report_generator/schemas.py#L9).

### 9.7. Persistence local và production

![Data model](diagrams/05-data-model.svg)

SQLite có bốn bảng legacy-compatible: `users`, `sessions`, `messages`, `evaluations`; profile và state phức tạp được serialize JSON. Model SQLAlchemy nằm tại [models.py](../backend/models.py#L10).

Firestore tổ chức theo tenant boundary:

```text
users/{uid}
  candidates/{candidateId}
  interviews/{sessionId}
```

Session document chứa state, turns, evaluations và report. Collection helper tại [firestore.py](../backend/infrastructure/repositories/firestore.py#L459) luôn bắt đầu từ user document.

---

## 10. Kiến trúc AI và cơ chế phỏng vấn thích ứng

### 10.1. Các AI agent

| Agent/service | Đầu vào | Đầu ra |
| --- | --- | --- |
| Resume Agent | Resume text | Candidate Profile |
| Interview Planner | Profile + config | Interview Plan |
| Question Generator | Profile + round + config | Interview Question |
| Evaluator | Profile + question + answer | Answer Evaluation |
| Decision Service | Evaluation + state | Follow-up/tăng độ khó/câu tiếp/kết thúc |
| Report Generator | Profile + completed state | Interview Report |

### 10.2. Structured output

Các agent yêu cầu Gemini trả JSON phù hợp schema và dùng Pydantic validate. Nếu model trả sai shape, lời gọi thất bại hoặc được retry theo chính sách LLM adapter. Đây là điểm kiểm soát quan trọng vì LLM là thành phần có đầu ra xác suất.

### 10.3. Quy tắc thích ứng hiện tại

Decision Service áp dụng rule rõ ràng:

1. `follow_up_needed == true` → đặt follow-up.
2. `overall_score >= 8` → tăng difficulty.
3. Trường hợp khác → chuyển sang câu/topic tiếp theo.
4. Đủ `question_count` hoặc hết plan → kết thúc.

Nguồn: [decision_service.py](../backend/orchestrator/decision_service.py#L6) và [interview_orchestrator.py](../backend/orchestrator/interview_orchestrator.py#L49).

### 10.4. Model routing và retry

LLM adapter chọn simple/complex model theo task, dùng timeout, exponential backoff và jitter cho lỗi tạm thời. Voice evaluation dùng tuyến nhẹ hơn để giảm độ trễ. Chi tiết tại [vertex_gemini.py](../backend/infrastructure/llm/vertex_gemini.py#L69).

### 10.5. Giới hạn cần công bố

- Prompt Resume hiện chỉ đưa tối đa 12.000 ký tự đầu vào AI, xem [prompts.py](../backend/services/profile_scanner/prompts.py#L11).
- Không có OCR cho tài liệu scan.
- Chất lượng phụ thuộc nội dung Resume, model, prompt và quota Vertex AI.
- Hiring recommendation là gợi ý mô phỏng, không nên dùng như quyết định tuyển dụng tự động.

---

## 11. Các luồng nghiệp vụ chính

### 11.1. Đăng nhập và gọi API

1. Người dùng chọn đăng nhập Google.
2. Firebase Web SDK mở popup và giữ auth state.
3. API client lấy Firebase ID token.
4. Client gắn `Authorization: Bearer <token>`.
5. Backend Firebase Admin verify token với revoked-token check.
6. Route dùng `current_user.uid`, không nhận owner từ body.
7. Nếu API trả `401`, client refresh token tối đa một lần rồi gửi lại.

Nguồn: [AuthContext.tsx](../frontend/src/contexts/AuthContext.tsx#L18), [api.ts](../frontend/src/lib/api.ts#L38), [firebase.py](../backend/infrastructure/auth/firebase.py#L28).

### 11.2. Upload Resume

1. Frontend kiểm tra file PDF/DOCX tối đa 10 MB.
2. Gateway ghi file vào vùng tạm.
3. Backend kiểm tra extension và kích thước.
4. Document Service đọc PDF page hoặc DOCX paragraph/table.
5. Nội dung dưới 50 ký tự bị từ chối.
6. Resume Agent gọi Gemini tạo Candidate Profile.
7. Repository tạo Candidate, lưu raw text và profile.
8. File tạm luôn bị xóa trong `finally`.

Hạn chế runtime: đang dựa vào extension thay vì magic bytes; chưa có idempotency, upload status hoặc Replacement Upload. Luồng hiện tại nằm tại [resume.py](../backend/gateway/api/resume.py#L27).

### 11.3. Candidate Profile và readiness

Profile GET:

1. Load profile theo `(candidate_id, uid)`.
2. Foreign và missing cùng trả `404` để không lộ sự tồn tại tài nguyên.
3. Backend chạy `evaluate_interview_readiness`.
4. Response trả `profile`, `readiness` và strong ETag dạng `"<profile_version>"`.

Readiness yêu cầu tên thật, ít nhất một skill normalized và ít nhất một evidence có thể phỏng vấn từ Skill Evidence, project, experience hoặc qualifying structured education. Validator còn phát hiện experience âm/không hữu hạn, nested entry rỗng và evidence tham chiếu skill không tồn tại.

Runtime hiện chưa có PATCH/Save Corrections và interview start chưa enforce readiness. Đây là khoảng trống cần nêu rõ, không phải tính năng đã hoàn tất.

### 11.4. Text interview

![Text interview sequence](diagrams/03-text-interview-sequence.svg)

1. Client gửi candidate ID và Interview Config đến `/prepare` hoặc `/start`.
2. Gateway reload Candidate Profile thuộc user.
3. Preparation cache có thể chuẩn bị plan/câu đầu theo key gồm user, profile và config.
4. Orchestrator dùng Planner và Question Generator.
5. Gateway tạo session, persist state và turn đầu.
6. Mỗi answer được Evaluator chấm.
7. Decision Service chọn follow-up, tăng độ khó hoặc câu kế tiếp.
8. Gateway persist state/turn rồi trả response.
9. Khi `current_turn == null`, session hoàn tất.

### 11.5. Voice interview

![Voice interview sequence](diagrams/04-voice-interview-sequence.svg)

1. Client mở `WS /api/v2/voice/interview/{session_id}`.
2. Firebase token đi qua WebSocket subprotocol.
3. Gateway kiểm tra origin, token, ownership và voice mode.
4. Browser gửi PCM chunks sau sự kiện `start_listening`.
5. Speech service chạy Silero VAD và faster-whisper.
6. Transcript partial/final được gửi về client/gateway.
7. Transcript final đi qua cùng Orchestrator/Evaluator như text.
8. Gemini stream câu hỏi mới; text được chunk cho VieNeu-TTS.
9. PCM trả về browser để phát.
10. Barge-in hủy TTS khi người dùng bắt đầu nói.

Audio được giữ trong bounded queue và không persist. Source hiện hỗ trợ flow này, nhưng production report gần nhất chưa chứng minh speech service GPU đã deploy.

### 11.6. Report và history

1. Chỉ session completed mới được sinh report.
2. Nếu report đã tồn tại, service trả bản cũ thay vì gọi AI lại.
3. Report được persist, session chuyển `report_generated`.
4. History hỗ trợ `candidate_id`, `limit` và `offset`.

Lưu ý: service hiện còn reload Candidate Profile mới nhất khi generate report thay vì chỉ dùng snapshot; xem [report service](../backend/services/report_generator/service.py#L15). Điều này cần được sửa trước khi profile correction được bật.

---

## 12. Danh mục API

| Method | Endpoint | Auth | Chức năng |
| --- | --- | --- | --- |
| `GET` | `/health` | Không | Liveness |
| `GET` | `/ready` | Không | Readiness của settings/repository |
| `GET` | `/api/v2/auth/me` | Firebase | Identity hiện tại |
| `POST` | `/api/v2/resume/upload` | Firebase | Upload và parse Resume |
| `GET` | `/api/v2/candidates/{candidate_id}/profile` | Firebase | Profile + readiness + ETag |
| `POST` | `/api/v2/interview/prepare` | Firebase | Warm/cache plan và câu đầu |
| `POST` | `/api/v2/interview/start` | Firebase | Tạo session |
| `POST` | `/api/v2/interview/{session_id}/answer` | Firebase | Submit answer |
| `GET` | `/api/v2/interview/{session_id}` | Firebase | Khôi phục state |
| `WS` | `/api/v2/voice/interview/{session_id}` | Firebase subprotocol | Voice realtime |
| `POST` | `/api/v2/interview/{session_id}/report` | Firebase | Sinh/đọc lại report |
| `GET` | `/api/v2/interview/{session_id}/report` | Firebase | Đọc report |
| `GET` | `/api/v2/interviews` | Firebase | Lịch sử phân trang |
| `GET` | speech `/health`, `/ready` | Tùy môi trường | Speech health/readiness |
| `WS` | speech `/internal/v1/inference` | Internal token | STT/TTS inference |

FastAPI tự cung cấp OpenAPI `/openapi.json`, Swagger `/docs` và ReDoc `/redoc` nếu không bị tắt ở deployment.

### API chưa tồn tại trong runtime

- `PATCH /api/v2/candidates/{candidate_id}/profile`
- `POST /api/v2/candidates/{candidate_id}/resume` cho Replacement Upload
- Upload operation/status endpoint

Các endpoint này chỉ là target contract trong [RESUME_REVIEW_UI_SPEC.md](RESUME_REVIEW_UI_SPEC.md#9-target-api-contracts).

---

## 13. Thiết kế frontend

### 13.1. Production routes

| Route | Trang |
| --- | --- |
| `/login` | Google sign-in |
| `/text-interview` | Upload, setup và text interview |
| `/text-interview/:sessionId` | Khôi phục text session |
| `/text-interview/:sessionId/report` | Report |
| `/speech-interview` | Upload/setup voice |
| `/speech-interview/:sessionId` | Voice room |
| `/interview-history` | History |
| `/settings` | Local interview preferences |
| `/candidate-profile/:candidateId` | Profile Review read-only hiện tại |

Nguồn chuẩn: [App.tsx](../frontend/src/App.tsx#L22).

### 13.2. State và API

- Firebase auth state nằm trong `AuthContext`.
- Protected routes chặn user chưa đăng nhập.
- `api.ts` tập trung base URL, bearer token, one-time refresh và error mapping.
- Interview preferences được lưu ở client.
- PCM audio player quản lý playback voice.

### 13.3. UI/UX và accessibility

Hệ thống dùng design token, Satoshi/Segoe UI, một accent, card/divider tiết chế và component dùng lại như Button, Input, Card, Badge. Candidate Profile route có một `h1`, ordered sections, readiness links, focus target và layout responsive. Quy chuẩn đầy đủ tại [UI_GUIDELINES.md](UI_GUIDELINES.md#fipilot-ui-guidelines).

### 13.4. Responsive target

Các kích thước cần kiểm tra: 1440, 1024, 768 và 390 px. Tại 768 px trở xuống, Profile Review chuyển một cột và readiness nằm trước nội dung.

---

## 14. Thiết kế backend và speech service

### 14.1. Gateway layer

Route giữ mỏng: nhận request, resolve dependency/auth, gọi service/repository và trả contract. `gateway/main.py` cài CORS, middleware correlation và tất cả router.

### 14.2. Service layer

Mỗi tác vụ AI có agent/prompt/schema/service riêng: profile scanner, planner, question generator, answer evaluator và report generator. Candidate readiness là pure domain function, dễ kiểm thử.

### 14.3. Orchestrator

Orchestrator sở hữu workflow nhiều lượt, decision, follow-up và memory. Điều này tránh đặt business state machine trong API route.

### 14.4. Infrastructure layer

- Firebase adapter xác thực.
- Vertex adapter thực hiện model routing/retry/structured generation.
- SQLite/Firestore cùng tuân repository interface.
- Document adapter đọc PDF/DOCX.
- Speech adapter có local hoặc remote implementation.

### 14.5. Speech service

Speech service có liveness/readiness riêng, warm-up model và WebSocket inference nội bộ. Gateway có thể gọi bằng `SPEECH_SERVICE_URL`; production cần `SPEECH_SERVICE_TOKEN`, internal ingress/IAM và GPU phù hợp. Xem [speech README](../backend/speech_service/README.md#speech-inference-boundary).

---

## 15. Bảo mật, phân quyền và quyền riêng tư

### 15.1. Đã triển khai

- Firebase ID token được verify bằng Firebase Admin và `check_revoked=True`.
- Protected HTTP route dùng `current_user.uid`.
- Candidate/session/report đều lookup theo owner.
- Foreign và missing resource dùng cùng `404` ở các seam ownership quan trọng.
- Production startup bắt buộc Firebase auth, Firestore và đúng một HTTPS CORS origin.
- WebSocket voice kiểm tra exact origin, token, ownership và mode.
- Resume file tạm bị xóa.
- Audio không persist.
- Log không ghi body/audio/token; middleware dùng request ID.
- Cloud workload dùng Application Default Credentials, không cần private-key file trong image.

### 15.2. Trust boundaries

```text
Browser -- Firebase token --> Gateway
Gateway -- service identity/ADC --> Firestore + Vertex AI
Gateway -- internal token/private WSS --> Speech Service
```

### 15.3. Rủi ro và cải tiến

- Thêm rate limit và per-user quota.
- Dùng Secret Manager và rotate speech token.
- Thiết kế retention/delete-data workflow cho Resume, transcript và report.
- Kiểm tra MIME/magic bytes thay vì chỉ extension.
- Thêm audit trail cho Profile Corrections.
- Thêm transaction/version cho concurrent mutation.

---

## 16. Độ tin cậy, hiệu năng và khả năng mở rộng

### 16.1. Cơ chế hiện có

- Health và readiness tách biệt.
- Gemini adapter có timeout/retry/backoff/jitter.
- Preparation cache giảm thời gian chờ khi start.
- Report trả bản đã lưu nếu tồn tại.
- Voice dùng bounded queue, giới hạn chunk/session và fail-fast khi quá tải.
- State persist cho phép reload session.
- Firestore là managed store production.

### 16.2. Điểm nghẽn

- Gemini latency/quota.
- Firestore read-modify-write khi concurrent answer/report.
- WebSocket voice giữ connection state trong memory.
- GPU speech có cold start và giới hạn concurrent stream.
- SQLite local disk/locking không phù hợp nhiều replica.

### 16.3. Hướng scale

- Gateway text scale ngang với Firestore.
- Voice cần sticky connection hoặc distributed ownership khi có nhiều gateway.
- Speech worker scale theo số stream/GPU và cần admission control.
- Report có thể đưa sang job queue khi latency lớn.
- History nên chuyển cursor pagination khi dữ liệu tăng.

---

## 17. Kiểm thử và bằng chứng chất lượng

### 17.1. Backend

Repository có 32 file `test_*.py` trong `backend/app/tests`; phiên khảo sát collect được 197 test bằng pytest nhưng **không chạy toàn bộ suite trong tác vụ viết tài liệu này**. Các nhóm kiểm thử gồm:

- auth và cross-user ownership;
- Candidate Profile, ETag, readiness và NFKC normalization;
- SQLite và Firestore repository;
- Resume upload/extraction;
- planner, question, evaluator, decision và orchestrator;
- preparation cache;
- report/history;
- Vertex Gemini retry/schema;
- voice WebSocket, remote speech, STT/VAD/TTS, barge-in, reconnect, backpressure;
- logging/readiness/production settings.

### 17.2. Frontend

Có 8 file test với khoảng 29 khai báo `it/test`, bao phủ API client, PCM player, Candidate Profile, readiness summary, text/voice pages, history và settings.

### 17.3. Bằng chứng production gần nhất

[DEPLOYMENT_REPORT.md](../DEPLOYMENT_REPORT.md#remote-verification) ngày 23/07/2026 ghi nhận auth, Resume, text interview, report/history, ownership, Firestore, CORS và logging đã pass trên môi trường deploy. Báo cáo đó không chứng minh code voice mới hơn đã được deploy.

### 17.4. Lệnh kiểm tra chuẩn

```powershell
# Backend, chạy từ backend/
python -m pytest
python -m compileall -q core gateway infrastructure orchestrator services shared speech_service

# Frontend, chạy từ frontend/
npm exec tsc -- -b
npm run lint
npm test
npm run build
```

Không có backend static type checker/linter được check-in; không nên tuyên bố đã pass một công cụ không tồn tại.

---

## 18. Cài đặt và chạy dự án

### 18.1. Yêu cầu

- Python 3.12.
- Node.js/npm phù hợp lockfile.
- Google Cloud CLI.
- Firebase project config cho frontend.
- Google Application Default Credentials.
- GPU/CUDA là tùy chọn nhưng hữu ích cho speech.

### 18.2. Cài dependency

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt -r requirements-speech.txt

cd ..\frontend
npm ci
```

### 18.3. Tạo file cấu hình

```powershell
Copy-Item backend\.env.local.example backend\.env.local
Copy-Item backend\.env.speech.example backend\.env.speech
Copy-Item frontend\.env.local.example frontend\.env.local
```

Không commit `.env`, service-account JSON hoặc private key.

### 18.4. Xác thực Google Cloud

```powershell
gcloud auth login
gcloud auth application-default login
gcloud config set project <GOOGLE_CLOUD_PROJECT>
```

### 18.5. Chạy native

Tại repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_backend.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\run_speech_service.ps1
```

Mở terminal khác:

```powershell
cd frontend
npm run dev -- --host localhost
```

Truy cập `http://localhost:5173`.

### 18.6. Chạy Docker Compose

```powershell
$env:GOOGLE_ADC_DIR = "$env:APPDATA\gcloud"
docker compose -f docker-compose.local.yml up --build
```

Hướng dẫn chi tiết và health checks tại [local-development.md](local-development.md#local-development).

---

## 19. Cấu hình môi trường

### 19.1. Frontend

| Biến | Ý nghĩa |
| --- | --- |
| `VITE_API_BASE_URL` | URL gateway |
| `VITE_FIREBASE_API_KEY` | Public Firebase web config |
| `VITE_FIREBASE_AUTH_DOMAIN` | Firebase auth domain |
| `VITE_FIREBASE_PROJECT_ID` | Project ID |
| `VITE_FIREBASE_APP_ID` | Firebase app ID |

### 19.2. Backend chung

| Nhóm biến | Ví dụ |
| --- | --- |
| App | `APP_ENV`, `DEBUG`, `LOG_LEVEL` |
| Google | `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION` |
| Gemini | `GEMINI_SIMPLE_MODEL`, `GEMINI_COMPLEX_MODEL`, `GEMINI_RESUME_MODEL` |
| Auth | `AUTH_ENABLED`, `AUTH_PROVIDER`, `FIREBASE_PROJECT_ID` |
| CORS | `CORS_ALLOWED_ORIGINS` |
| Repository | `REPOSITORY_BACKEND`, `DATABASE_URL`, Firestore collection names |
| Voice limits | `MAX_VOICE_CHUNK_BYTES`, `MAX_VOICE_SESSION_BYTES` |
| Speech remote | `SPEECH_SERVICE_URL`, `SPEECH_SERVICE_TOKEN` |

### 19.3. Speech

| Nhóm | Biến chính |
| --- | --- |
| STT | `STT_MODEL`, `STT_DEVICE`, `STT_COMPUTE_TYPE`, `STT_LANGUAGE` |
| VAD | `VAD_THRESHOLD`, `VAD_MIN_SILENCE_MS`, `VAD_SPEECH_PAD_MS` |
| TTS | `TTS_MODE`, `TTS_DEVICE`, `TTS_VOICE`, `TTS_SAMPLE_RATE` |
| Queue | `STT_AUDIO_QUEUE_SIZE`, `TTS_QUEUE_SIZE` |

Nguồn mẫu: [backend/.env.example](../backend/.env.example), [backend/.env.local.example](../backend/.env.local.example), [frontend/.env.local.example](../frontend/.env.local.example).

---

## 20. Triển khai production

### 20.1. Kiến trúc đã được xác nhận ngày 23/07/2026

```text
Firebase Hosting -> Cloud Run Gateway -> Firestore
                                  \----> Vertex AI Gemini
Firebase Auth -------------------------> token verification
```

Deployment report ghi:

- Frontend trên Firebase Hosting.
- Backend `ai-interview-backend` trên Cloud Run `us-central1`.
- Firestore Native mode.
- Vertex AI qua Cloud Run service identity/ADC.
- Public Cloud Run invocation nhưng business routes vẫn yêu cầu Firebase token.
- Gateway 1 CPU, 1 GiB, concurrency 20, min 0, max 5 tại thời điểm báo cáo.

Chi tiết nhạy cảm vận hành như revision/URL có trong [DEPLOYMENT_REPORT.md](../DEPLOYMENT_REPORT.md#deployment); không cần đưa toàn bộ vào slide công khai.

### 20.2. Production voice mục tiêu

```text
Browser WSS -> Cloud Run Gateway
                  |
                  +-- private WSS --> GPU Speech Service
```

Speech worker nên cùng region, dùng internal ingress/IAM, secret token, GPU, model cache và min instance phù hợp. Đây là target architecture; cần deployment report và E2E mới trước khi tuyên bố đã vận hành production.

---

## 21. Đóng góp kỹ thuật nổi bật

1. Pipeline AI nhiều agent với structured output thay vì một prompt đơn khối.
2. Adaptive interview dùng rule có thể giải thích để chọn follow-up/tăng độ khó.
3. Cùng một domain state phục vụ text và voice.
4. Voice pipeline realtime có VAD, partial/final transcript, streaming question/TTS, barge-in và backpressure.
5. Repository abstraction chạy được SQLite local và Firestore production.
6. Firebase ownership isolation xuyên candidate, session và report.
7. Typed configuration và production startup guardrail.
8. Candidate Profile Readiness là pure backend domain validator dùng NFKC normalization.
9. Preparation cache giảm thời gian chờ lúc bắt đầu.
10. Bộ test bao phủ cả domain, API, persistence, auth và speech failure modes.

---

## 22. Hạn chế và rủi ro hiện tại

| Hạn chế | Ảnh hưởng |
| --- | --- |
| Resume prompt cắt 12.000 ký tự | Có thể mất nội dung cuối tài liệu dài |
| Chưa OCR | Resume scan ảnh không đọc được |
| Kiểm tra chủ yếu theo extension | Chưa đủ mạnh để xác định document type thật |
| Chưa có Profile PATCH | Profile Review đang read-only |
| Chưa có `If-Match` mutation | Chưa giải quyết concurrent profile edit |
| Chưa có replacement/idempotency/status | Retry upload có thể tạo resource lặp |
| Start chưa enforce readiness | Client sai vẫn có thể start profile chưa ready |
| Snapshot/version chưa transaction atomic | Có race khi correction được bật sau này |
| Report reload latest profile | Có thể sai lịch sử khi profile correction xuất hiện |
| Firestore update còn read-modify-write | Concurrent answer/report có nguy cơ conflict |
| Voice connection in-memory | Scale nhiều gateway cần sticky/distributed lease |
| Voice production chưa được xác nhận | Không nên demo bằng production nếu chưa deploy |
| Knowledge/Template chưa wired | Chưa phải RAG/curated question engine |
| Không có rate limiting | Có rủi ro quota/cost/abuse |
| Chưa có benchmark chính thức | Không được tuyên bố đạt p95 cụ thể |

Các khoảng trống Resume Review được ghi chính thức trong [RESUME_REVIEW_IMPLEMENTATION_RISKS.md](RESUME_REVIEW_IMPLEMENTATION_RISKS.md#resume-review-implementation-risks).

---

## 23. Hướng phát triển

### P0 — tính đúng đắn và contract

1. Implement strict Profile PATCH với allowlist.
2. Implement strong `If-Match`, `428` và stale `412`.
3. Enforce cùng một readiness validator ở text/voice start.
4. Tạo atomic immutable snapshot + `candidate_profile_version`.
5. Generate report chỉ từ session snapshot.
6. Kiểm tra magic bytes và xử lý toàn bộ document.

### P1 — upload và vận hành

1. Initial/Replacement Upload với Idempotency-Key.
2. Upload operation/status, lease và fenced generation.
3. Rate limit, per-user quota và GPU admission control.
4. OpenTelemetry/metrics/dashboard/alerts.
5. Data retention, export và delete workflow.
6. Deploy/private GPU speech service và load test.

### P2 — sản phẩm và nghiên cứu

1. Kết nối curated Knowledge/Template vào retriever/RAG có đánh giá.
2. OCR và đa định dạng tài liệu.
3. Rubric theo vị trí và cấp độ.
4. Human-in-the-loop cho evaluation quan trọng.
5. Theo dõi prompt/model version để tái lập report.
6. Đánh giá bias, fairness và calibration điểm.

---

## 24. Kịch bản demo

### 24.1. Demo an toàn 8–12 phút

1. Giới thiệu bài toán và kiến trúc ba service — 1 phút.
2. Đăng nhập Google — 30 giây.
3. Upload một Resume PDF/DOCX rõ nội dung — 1 phút.
4. Mở Candidate Profile, chỉ Profile Version và Readiness — 1 phút.
5. Chọn text, tiếng Việt, 2–3 câu, level phù hợp — 30 giây.
6. Start, trả lời một câu tốt và một câu thiếu ý — 3 phút.
7. Giải thích follow-up/độ khó và state persistence — 1 phút.
8. Hoàn tất, sinh report và mở history — 2 phút.
9. Kết thúc bằng hạn chế/roadmap — 1 phút.

### 24.2. Demo voice

Chỉ demo khi local speech service đã `/ready`, microphone permission hoạt động và GPU/model đã warm. Chuẩn bị text interview làm phương án dự phòng. Không tuyên bố voice production nếu chỉ chạy local.

### 24.3. Checklist trước bảo vệ

- Dùng Resume mẫu không chứa dữ liệu nhạy cảm.
- Đặt `question_count` nhỏ.
- Kiểm tra Firebase login và ADC.
- Gọi `/health`, `/ready`, speech `/ready`.
- Warm model speech trước.
- Kiểm tra quota Vertex AI và Internet.
- Có ảnh/video dự phòng.
- Không chiếu `.env`, token, log chứa PII hoặc Google account cá nhân.

---

## 25. Gợi ý bố cục báo cáo và slide

### 25.1. Bố cục báo cáo học thuật

1. **Chương 1 — Tổng quan:** lý do, bài toán, mục tiêu, phạm vi.
2. **Chương 2 — Cơ sở lý thuyết:** LLM, structured output, STT, VAD, TTS, WebSocket, Firebase.
3. **Chương 3 — Phân tích và thiết kế:** use case, kiến trúc, data model, API, bảo mật.
4. **Chương 4 — Cài đặt:** frontend, backend, AI agents, speech pipeline, persistence.
5. **Chương 5 — Kiểm thử và đánh giá:** test seams, E2E, hạn chế, đo lường.
6. **Chương 6 — Kết luận và hướng phát triển.**

### 25.2. Slide 12–15 trang

1. Tên đề tài/nhóm.
2. Bài toán.
3. Mục tiêu và phạm vi.
4. Use case.
5. Kiến trúc tổng thể.
6. Data/domain model.
7. AI pipeline.
8. Text sequence.
9. Voice sequence.
10. Bảo mật/ownership.
11. Demo.
12. Kiểm thử/bằng chứng.
13. Đóng góp.
14. Hạn chế/roadmap.
15. Kết luận.

### 25.3. Chỉ số nên đo bổ sung trước khi nộp

- Tỷ lệ Resume parse thành công theo tập mẫu.
- Tỷ lệ LLM structured output hợp lệ.
- p50/p95 plan, evaluation và report latency.
- STT Word Error Rate trên tập tiếng Việt đại diện.
- Time-to-first-transcript và time-to-first-audio.
- Test pass rate trên commit chốt.
- Chi phí Gemini trung bình mỗi interview.
- Đánh giá người dùng về mức liên quan của câu hỏi/feedback.

Không tự tạo số liệu. Chỉ đưa kết quả sau khi có dataset, quy trình và log đo rõ ràng.

---

## 26. Câu hỏi bảo vệ thường gặp

### Vì sao dùng LLM thay vì bộ câu hỏi cố định?

LLM tận dụng Resume và câu trả lời trước đó để cá nhân hóa. Hệ thống vẫn dùng Pydantic contract và rule decision để giảm tính tùy ý. Bộ câu hỏi curated có thể bổ sung sau qua Knowledge Retriever.

### Vì sao dùng modular monolith?

Nghiệp vụ interview chia sẻ schema/state chặt; in-process call đơn giản, dễ debug và phù hợp MVP. Speech được tách vì có profile tài nguyên khác: GPU, model cache và binary streaming.

### Vì sao dùng Firebase và Firestore?

Firebase cung cấp Google login/ID token, Firestore là managed database phù hợp user-scoped document và Cloud Run. SQLite giữ trải nghiệm local nhẹ qua cùng repository interface.

### AI chấm điểm có đáng tin hoàn toàn không?

Không. Structured schema chỉ đảm bảo shape, không đảm bảo tuyệt đối nội dung. Report là feedback luyện tập; cần benchmark, calibration và human review nếu dùng trong tuyển dụng thật.

### Hệ thống chống hallucination thế nào?

Prompt bám Candidate Profile/question, output theo schema, Pydantic validation và rule-based decision. Hướng tiếp theo là lưu prompt/model version, curated retrieval và evaluation dataset.

### Vì sao cần snapshot Candidate Profile?

Để một interview/report lịch sử không thay đổi khi user sửa hồ sơ sau đó. Source đã giữ profile trong state, nhưng transaction + exact profile version và report-from-snapshot vẫn cần hoàn thiện.

### Text và voice có dùng hai logic chấm khác nhau không?

Transcript final của voice được đưa qua cùng orchestrator/evaluator như text. Khác biệt chính nằm ở transport, VAD/STT/TTS và latency handling.

### Tại sao không lưu audio?

Giảm rủi ro quyền riêng tư, chi phí và phạm vi bảo mật. Đánh đổi là khó replay/debug lỗi âm thanh.

### Voice đã chạy production chưa?

Source hiện có flow end-to-end, nhưng deployment report gần nhất chỉ xác nhận text Phase 1. Vì vậy chỉ khẳng định voice chạy ở source/local cho đến khi có deployment và E2E report mới.

### Điểm chưa hoàn thiện quan trọng nhất là gì?

Profile correction/versioned mutation, replacement upload idempotency và atomic session snapshot. Đây là các contract đã thiết kế nhưng chưa hoàn tất runtime.

### Nếu có thêm thời gian sẽ ưu tiên gì?

Ưu tiên tính đúng đắn và bảo mật dữ liệu trước: PATCH/If-Match, readiness enforcement, atomic snapshot, report từ snapshot, magic-byte validation; sau đó mới scale voice/RAG.

---

## 27. Thuật ngữ

| Thuật ngữ | Ý nghĩa trong dự án |
| --- | --- |
| Resume | PDF/DOCX do ứng viên cung cấp |
| Candidate Profile | Hồ sơ có cấu trúc đã persist từ Resume |
| Profile Version | Số phiên bản server-controlled của profile |
| Profile Validity | Dữ liệu đúng type/shape/rule để lưu |
| Interview Readiness | Đủ identity, skill và evidence để start |
| Interview Session | Một buổi text/voice cùng config |
| Session Snapshot | Bản profile gắn với lịch sử session |
| Interview Plan | Các round/topic/difficulty do planner tạo |
| Turn | Một câu hỏi, câu trả lời và evaluation |
| Follow-up | Câu hỏi đào sâu dựa trên evaluation |
| Structured output | JSON từ LLM được validate bởi schema |
| STT | Speech-to-Text |
| VAD | Voice Activity Detection |
| TTS | Text-to-Speech |
| Barge-in | User nói để ngắt AI đang phát tiếng |
| Backpressure | Kiểm soát tốc độ/queue để tránh tràn memory |
| Ownership | Mọi resource được scope theo Firebase `uid` |
| ETag/If-Match | Cơ chế optimistic concurrency cho Profile Version |
| Idempotency key | Khóa bảo đảm retry mutation không tạo kết quả lặp |
| ADC | Google Application Default Credentials |

---

## 28. Kết luận

Fipilot đã xây dựng được nền tảng V2 có chiều sâu kỹ thuật: xác thực Firebase, ownership isolation, Resume-to-Profile bằng Gemini, phỏng vấn text thích ứng, source voice realtime, persistence SQLite/Firestore, report và lịch sử. Điểm nổi bật nhất là việc tách rõ AI agents, orchestration, infrastructure và speech service thay vì gom toàn bộ logic vào một API handler.

Mức độ hoàn thiện cần được trình bày chính xác. Text production đã có bằng chứng; voice source đã đầy đủ hơn deployment report; Resume Review nâng cao mới triển khai một phần. Việc nêu rõ những khoảng trống này không làm giảm giá trị đồ án, mà thể hiện khả năng đánh giá rủi ro, phân biệt thiết kế với implementation và lập roadmap kỹ thuật có trách nhiệm.

---

## 29. Phụ lục lệnh kiểm tra và nguồn tham khảo

### 29.1. Health checks

```powershell
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/ready
Invoke-RestMethod http://localhost:9000/health
Invoke-RestMethod http://localhost:9000/ready
```

### 29.2. Kiểm thử tập trung

```powershell
# Ví dụ backend
cd backend
python -m pytest app/tests/test_interview_api.py -q
python -m pytest app/tests/test_voice_websocket.py -q
python -m pytest app/tests/test_auth_and_ownership.py -q

# Ví dụ frontend
cd ..\frontend
npm test -- src/pages/TextInterviewPage.test.tsx
npm test -- src/pages/SpeechInterviewPage.test.tsx
```

### 29.3. Nguồn chính trong repository

- [Repository README](../README.md)
- [Domain context](../CONTEXT.md)
- [System Design tiếng Việt](SYSTEM_DESIGN_VI.md)
- [Local Development](local-development.md)
- [Local Architecture](local-architecture.md)
- [Deployment Report](../DEPLOYMENT_REPORT.md)
- [Production Checklist](../PRODUCTION_CHECKLIST.md)
- [Frontend package](../frontend/package.json)
- [Frontend routes](../frontend/src/App.tsx)
- [Frontend API client](../frontend/src/lib/api.ts)
- [FastAPI entry point](../backend/gateway/main.py)
- [Backend settings](../backend/core/settings.py)
- [Candidate schemas](../backend/shared/schemas/candidate.py)
- [Interview schemas](../backend/shared/schemas/interview.py)
- [Interview orchestrator](../backend/orchestrator/interview_orchestrator.py)
- [SQLite repository](../backend/infrastructure/repositories/sqlite.py)
- [Firestore repository](../backend/infrastructure/repositories/firestore.py)
- [Resume Review UI Specification](RESUME_REVIEW_UI_SPEC.md)
- [Resume Review Testing Seams](RESUME_REVIEW_TESTING_SEAMS.md)
- [Resume Review Implementation Risks](RESUME_REVIEW_IMPLEMENTATION_RISKS.md)
- [ADR directory](adr)

### 29.4. Ghi chú tái lập

Trước khi nộp báo cáo chính thức, cần chốt một commit sạch, chạy toàn bộ validation, ghi ngày/model/config, lưu test output và cập nhật lại ma trận trạng thái. Không dùng số test, latency, accuracy hoặc production status của tài liệu này như số liệu cuối cùng nếu repository đã thay đổi sau commit tham chiếu.
