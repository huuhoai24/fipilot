# AI Interview Platform - Tài liệu dự án

## 1. Tổng quan

AI Interview Platform là hệ thống phỏng vấn kỹ thuật có tích hợp trí tuệ nhân tạo. Hệ thống hỗ trợ admin tạo phiên phỏng vấn từ CV ứng viên, gợi ý bộ câu hỏi phù hợp, tiến hành phỏng vấn thời gian thực bằng giọng nói hoặc văn bản, chấm điểm câu trả lời và sinh báo cáo đánh giá sau buổi phỏng vấn.

Dự án gồm hai phần chính:

- Backend: FastAPI, SQLite, SQLAlchemy, WebSocket, AI services, CV parser, TTS/STT và evaluation pipeline.
- Frontend: React, TypeScript, Vite, TailwindCSS, Zustand và React Query.

Hệ thống được thiết kế cho quy trình tuyển dụng IT, đặc biệt phù hợp với các vị trí như Software Engineer, Backend Developer, Frontend Developer, AI Engineer, Data Engineer, DevOps Engineer, Tester/QA, Business Analyst và Cybersecurity Analyst.

## 2. Mục tiêu sản phẩm

- Giảm thời gian chuẩn bị buổi phỏng vấn từ CV ứng viên.
- Tự động trích xuất hồ sơ ứng viên từ PDF hoặc DOCX.
- Gợi ý template câu hỏi phù hợp với vai trò, cấp độ và kỹ năng của ứng viên.
- Tạo môi trường phỏng vấn trực tuyến có AI interviewer.
- Hỗ trợ ứng viên trả lời bằng microphone hoặc nhập văn bản.
- Đánh giá từng câu trả lời theo rubric và sinh báo cáo tổng hợp.
- Ghi nhận hành vi chuyển tab hoặc rời cửa sổ trong lúc phỏng vấn.
- Cho phép admin chọn cách track CV: workflow nhanh hoặc LLM Gemma.

## 3. Kiến trúc tổng thể

Luồng xử lý tổng quát của hệ thống:

1. Admin đăng nhập vào frontend.
2. Admin upload CV ứng viên.
3. Backend kiểm tra file, đọc nội dung và phân tích profile bằng workflow hoặc LLM.
4. Backend match profile với template câu hỏi phù hợp.
5. Admin xác nhận profile, chọn template và tạo session phỏng vấn.
6. Ứng viên vào phòng phỏng vấn.
7. Frontend kết nối WebSocket với backend.
8. AI interviewer mở màn và điều phối luồng câu hỏi.
9. Ứng viên trả lời bằng giọng nói hoặc văn bản.
10. Backend chuyển âm thanh thành văn bản nếu câu trả lời là audio.
11. Backend lưu transcript, đánh giá câu trả lời và sinh câu hỏi tiếp theo.
12. Khi kết thúc, backend sinh báo cáo đánh giá tổng hợp.
13. Frontend hiển thị điểm số, nhận xét, rubric từng câu và thống kê proctoring.

## 4. Cấu trúc thư mục

```text
ai-interview-platform/
  backend/
    main.py                 API, WebSocket và workflow chính.
    models.py               SQLAlchemy models.
    database.py             Kết nối SQLite và quản lý DB session.
    crud.py                 Các hàm thao tác DB cơ bản.
    cv_parser.py            CV extractor bằng workflow và LLM Gemma.
    ai_services.py          LLM, STT, evaluation và adaptive question plan.
    tts_service.py          Text-to-speech bằng VieNeu.
    template_service.py     Đọc và match template câu hỏi.
    requirements.txt        Danh sách thư viện backend.
    .env                    Cấu hình model, API key và Ollama local.

  frontend/
    src/
      App.tsx
      lib/api.ts
      pages/
        InterviewFlowPage.tsx
        InterviewSessionPage.tsx
        EvaluationReportPage.tsx
      components/
      store/
    package.json
    vite.config.ts

  Template/
    Bộ câu hỏi phỏng vấn theo role và level.
```

## 5. Công nghệ sử dụng

### 5.1. Backend

- FastAPI: xây dựng REST API và WebSocket.
- Uvicorn: ASGI server để chạy backend.
- SQLAlchemy: ORM làm việc với database.
- SQLite: database local cho phiên bản demo/prototype.
- Pydantic: định nghĩa request và response schema.
- pypdf và python-docx: đọc nội dung từ PDF/DOCX.
- OpenAI SDK: gọi các endpoint OpenAI-compatible, bao gồm Ollama local.
- Groq SDK: fallback STT bằng Whisper.
- Transformers và Torch: chạy PhoWhisper local cho tiếng Việt.
- VieNeu và static-ffmpeg: tổng hợp giọng nói và xử lý audio.

### 5.2. Frontend

- React 18.
- TypeScript.
- Vite.
- TailwindCSS.
- React Router.
- React Query.
- Zustand.
- lucide-react.
- react-dropzone.
- react-markdown.

## 6. Database model

### 6.1. User

Bảng `users` lưu thông tin người dùng cơ bản.

```text
users
  id
  name
```

### 6.2. Session

Bảng `sessions` lưu thông tin một phiên phỏng vấn.

```text
sessions
  id
  user_id
  status
  role
  level
  language
  candidate_name
  question_count
  template_id
  current_question_id
  follow_up_count
  completed_question_ids
  state
  question_plan_json
  proctoring_events_json
  created_at
  report_data
```

Các trạng thái quan trọng của session:

- CHITCHAT: phiên mới được tạo, AI đang chuẩn bị hoặc gửi lời mở màn.
- INTERVIEWING: phiên đang diễn ra.
- ENDED: phiên đã kết thúc và báo cáo đã sẵn sàng hoặc đang được sinh.

### 6.3. Message

Bảng `messages` lưu transcript hội thoại.

```text
messages
  id
  session_id
  role       user | ai
  content
  created_at
```

### 6.4. Evaluation

Bảng `evaluations` lưu kết quả chấm điểm từng câu hỏi.

```text
evaluations
  id
  session_id
  question_id
  answer_id
  correctness
  score
  explanation
  rubric_json
```

## 7. Backend API

### 7.1. Tạo session

```http
POST /api/sessions
```

Payload mẫu:

```json
{
  "name": "Candidate Name",
  "role": "AI Engineer",
  "level": "1",
  "language": "vi",
  "template_id": "ai_engineer_lv1",
  "skills": ["Python", "RAG"],
  "recent_role": "Developer",
  "years_experience": 0,
  "education": "Bachelor..."
}
```

Chức năng chính:

- Kiểm tra template có hợp lệ hay không.
- Tạo session mới trong database.
- Lưu question plan ban đầu.
- Chạy background task để chuẩn bị adaptive question plan.

### 7.2. Track CV

```http
POST /api/cv/extract
```

Form data:

- `file`: file CV dạng PDF hoặc DOCX.
- `parser_mode`: `workflow` hoặc `llm`.

Chức năng:

- Kiểm tra extension, kích thước và nội dung thật của file.
- Đọc text từ CV.
- Kiểm tra file có giống resume thật hay không.
- Kiểm tra CV có phải tiếng Anh hay không.
- Parse profile ứng viên.
- Match template câu hỏi phù hợp.

### 7.3. WebSocket phỏng vấn

```text
ws://localhost:8000/ws/interview/{session_id}
```

WebSocket hỗ trợ:

- Gửi audio bytes.
- Gửi text answer.
- Nhận JSON message từ AI.
- Nhận binary audio TTS.
- Tự động gửi lời mở màn nếu session chưa có history.

## 8. CV tracking

Hệ thống có hai chế độ track CV.

### 8.1. Workflow nhanh

Workflow nhanh nằm trong file `backend/cv_parser.py`.

Ưu điểm:

- Nhanh.
- Không phụ thuộc LLM.
- Ổn định với CV có text rõ.
- Phù hợp cho demo, chạy local hoặc fallback khi LLM lỗi.

Workflow đã được tối ưu cho CV AI:

- Nhận diện `AI/ML`, `PyTorch`, `CNN`, `Transformer`, `OCR`, `RAG`, `LangChain`, `LangGraph`, `LLM APIs`, `FastAPI`, `Computer Vision`, `OpenCV`, `Ultralytics`, `CLIP`, `Pandas` và `Matplotlib`.
- Ưu tiên `AI Engineer` nếu CV có degree Artificial Intelligence hoặc có nhiều tín hiệu AI/CV/RAG.
- Không để `Position | Backend Developer` trong project làm lệch role fit nếu CV có tín hiệu AI mạnh.
- Giữ thứ tự skill theo thứ tự xuất hiện trong CV.

### 8.2. LLM Gemma

Chế độ `llm` dùng `gemma4:e2b` thông qua OpenAI-compatible endpoint, mặc định là Ollama local.

```env
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_API_KEY=ollama
OLLAMA_CV_MODEL=gemma4:e2b
```

Nếu LLM lỗi, backend fallback về workflow nhanh và trả thêm `parser_warning`.

## 9. Interview flow trên frontend

Trang chính là `InterviewFlowPage.tsx`.

Bước 1: Admin upload CV, chọn JD tùy chọn, chọn ngôn ngữ và chọn chế độ track CV.

Bước 2: Frontend hiển thị profile đã trích xuất, bao gồm họ tên, kinh nghiệm, level, role, học vấn, kỹ năng và vai trò gần nhất.

Bước 3: Frontend hiển thị các template phù hợp nhất, bao gồm điểm match, số câu hỏi, độ khó và thời lượng dự kiến.

Bước 4: Admin chọn bắt đầu ngay hoặc phỏng vấn sau. Nếu chọn bắt đầu ngay, hệ thống hiển thị cảnh báo trước khi vào phòng phỏng vấn.

## 10. Phỏng vấn thời gian thực

Trang chính là `InterviewSessionPage.tsx`.

Chức năng:

- Mở webcam preview.
- Kết nối WebSocket.
- Hiển thị live transcript.
- Phát audio AI bằng TTS.
- Thu âm bằng MediaRecorder.
- Tự động dừng ghi âm khi im lặng.
- Cho phép nhập câu trả lời bằng text.
- Có nút kết thúc phỏng vấn.

Luồng xử lý audio:

1. Frontend ghi âm audio dạng webm/opus.
2. Frontend gửi audio bytes qua WebSocket.
3. Backend chạy STT để chuyển audio thành text.
4. Backend lưu message của user.
5. AI sinh phản hồi hoặc câu hỏi tiếp theo.
6. Backend tổng hợp audio TTS.
7. Frontend phát audio và reveal text transcript.

## 11. Kiểm soát lượt trả lời và chấm điểm rỗng

Hệ thống khóa microphone và input text cho đến khi AI mở màn hoặc hỏi xong. Điều này tránh tình huống ứng viên gửi câu trả lời trước khi AI bắt đầu.

Sau khi ứng viên gửi câu trả lời, hệ thống tiếp tục khóa input để chờ AI phản hồi. Khi AI nói xong, input mới được mở lại.

Nếu người dùng không nói gì, trả lời quá ngắn, chọn bỏ qua hoặc transcript không rõ, backend không gọi evaluator fallback điểm trung bình. Câu trả lời đó được xem là không hợp lệ và điểm là `0/10`.

Nếu cả phiên không có câu trả lời hợp lệ từ ứng viên, report tổng kết sẽ có điểm `0/10`, thay vì để LLM tự đánh giá thành `5/10`.

## 12. Proctoring và phát hiện chuyển tab

Frontend phát hiện hành vi rời khỏi phòng phỏng vấn bằng browser API:

- `document.visibilitychange`: phát hiện tab bị ẩn hoặc người dùng chuyển tab.
- `window.blur`: phát hiện cửa sổ phỏng vấn mất focus.

Khi phát hiện vi phạm:

- Frontend hiển thị cảnh báo trong phòng phỏng vấn.
- Bộ đếm trên UI tăng lên.
- Frontend gửi event về backend.
- Backend lưu event vào `sessions.proctoring_events_json`.

Report hiển thị:

- Số lần chuyển tab.
- Số lần cửa sổ mất focus.
- Tổng số cảnh báo.

## 13. Evaluation report

Trang chính là `EvaluationReportPage.tsx`.

Report bao gồm:

- Thông tin ứng viên.
- Role, level và thời gian.
- Tổng điểm.
- Hire recommendation.
- Nhận xét chung.
- Thống kê proctoring.
- Điểm theo độ khó.
- Điểm mạnh.
- Điểm cần cải thiện.
- Đánh giá từng câu.
- Rubric chi tiết.
- Keyword hints.
- Gợi ý cải thiện.
- Xuất JSON.
- Tạo lại report.

## 14. Hướng dẫn chạy dự án

### 14.1. Chạy backend

```powershell
cd backend
.\venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Backend URL:

```text
http://127.0.0.1:8000
```

### 14.2. Chạy frontend

```powershell
cd frontend
npm install
npm run dev -- --host 127.0.0.1
```

Frontend URL mặc định:

```text
http://127.0.0.1:5173
```

Nếu port `5173` đang bận, Vite có thể tự chuyển sang `5174`.

### 14.3. Build frontend

```powershell
cd frontend
npm run build
```

## 15. Biến môi trường quan trọng

File: `backend/.env`.

```env
CORE_API_KEY=ollama
CORE_BASE_URL=http://localhost:11434/v1
CORE_MODEL=gemma4:e2b

EVALUATOR_API_KEY=ollama
EVALUATOR_BASE_URL=http://localhost:11434/v1
EVALUATOR_MODEL=gemma4:e2b

OLLAMA_CV_MODEL=gemma4:e2b

GROQ_API_KEY=...
DATABASE_URL=sqlite:///./interview_app.db
```

## 16. Lưu ý khi kiểm thử

- Sau khi sửa backend, cần restart Uvicorn để code mới có hiệu lực.
- Sau khi track CV, profile đã nằm trong state frontend; muốn thấy kết quả parser mới thì cần upload và track lại CV.
- Nếu LLM Gemma và workflow cho kết quả khác nhau, cần kiểm tra raw text được extract từ PDF/DOCX vì layout thực tế có thể khác ảnh chụp.
- Web app chỉ detect tab/window focus, không detect được tên ứng dụng desktop khác.
- VieNeu và PhoWhisper có thể load chậm trong lúc backend startup.
- Report cũ đã sinh trước khi sửa logic sẽ vẫn giữ dữ liệu cũ trong database; cần tạo session mới hoặc đánh giá lại.

## 17. Hướng phát triển

- Thêm export PDF report.
- Thêm dashboard thống kê theo role và template.
- Thêm authentication backend và phân quyền thật sự.
- Lưu lịch phỏng vấn vào database thay vì local store.
- Thêm chế độ full-screen enforcement cho phiên phỏng vấn.
- Thêm screen/camera proctoring nâng cao nếu có native app hoặc browser extension.
- Cải tiến CV parser theo hướng hybrid workflow + small LLM fallback theo từng field.
- Thêm unit test cho `cv_parser`, `template_service` và report generation.
- Tách report generation thành background worker riêng nếu số lượng session lớn.

## 18. Kết luận

AI Interview Platform là một hệ thống phỏng vấn kỹ thuật bằng AI tương đối đầy đủ, bao gồm CV parsing, template matching, realtime interview, STT/TTS, evaluation và proctoring. Kiến trúc hiện tại phù hợp cho demo, prototype và sử dụng nội bộ. Để đưa vào production, dự án cần bổ sung authentication backend, phân quyền, queue worker, logging/monitoring và cơ chế lưu trữ file/report chuẩn hóa hơn.
