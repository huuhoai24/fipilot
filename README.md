# FiPilot

FiPilot là nền tảng luyện phỏng vấn kỹ thuật bằng AI. Ứng dụng đọc CV, tạo câu hỏi theo kinh nghiệm thực tế, hỗ trợ trả lời bằng văn bản hoặc giọng nói, chấm từng lượt và lưu báo cáo phỏng vấn.

## Demo

[![Xem video demo FiPilot](docs/demo-cover.jpg)](docs/demo.mp4)

<div align="center">
  <video src="./docs/demo.mp4" controls width="900">
    Trình duyệt của bạn không hỗ trợ phát video trực tiếp.
  </video>
  <p><a href="./docs/demo.mp4">▶ Xem hoặc tải video demo</a></p>
</div>

Video web trong repository đã được tối ưu từ bản ghi gốc tại `demo.mp4`.

## Tính năng chính

- Đăng ký, đăng nhập và quản lý phiên bằng HttpOnly cookie.
- Nhận CV PDF/DOCX, trích xuất nội dung và dùng OCR khi tài liệu là ảnh quét.
- Chuẩn hóa CV thành hồ sơ có kỹ năng, dự án và kinh nghiệm bằng Azure OpenAI.
- Sinh câu hỏi theo role, level, CV và kho tri thức chuyên ngành.
- Đánh giá câu trả lời, đặt câu hỏi đào sâu và tạo báo cáo cuối buổi.
- Nhận dạng và tổng hợp giọng nói bằng Azure Speech.
- Lưu CV, phiên phỏng vấn, từng lượt trả lời và báo cáo trong PostgreSQL.

## Kiến trúc

```mermaid
flowchart LR
    Browser[Next.js frontend] -->|API proxy| API[FastAPI backend]
    API --> Document[DocumentService]
    Document --> OCR[RapidOCR]
    Document --> ResumeAgent[ResumeAgent]
    ResumeAgent --> LLM[Azure OpenAI]
    API --> Interview[Interview engine]
    Interview --> LLM
    Interview --> Knowledge[Knowledge base]
    API --> Speech[Azure Speech]
    API --> DB[(PostgreSQL)]
```

Pipeline CV đang hoạt động:

```text
PDF/DOCX → DocumentService → PyMuPDF4LLM/python-docx → RapidOCR fallback
         → ResumeAgent → Azure OpenAI → CandidateProfile → PostgreSQL
```

Backend chỉ dùng `.env` làm nguồn cấu hình LLM. Không còn pipeline YOLO, model GPU cục bộ hay `config.yaml` riêng.

## Công nghệ

| Thành phần | Công nghệ |
|---|---|
| Frontend | Next.js 16, React 19, TypeScript |
| Backend | Python 3.12, FastAPI, Pydantic |
| AI | Azure OpenAI, Azure Speech |
| Document | PyMuPDF4LLM, python-docx, pypdf, RapidOCR |
| Database | PostgreSQL 17, SQLAlchemy, Alembic |
| Runtime | uv, npm, Docker |

## Cấu trúc repository

```text
fipilot/
├── backend/
│   ├── api/                 # FastAPI app và API v1
│   ├── core/                # Dependency injection và logging
│   ├── gateway/api/         # API v2 theo kiến trúc mới
│   ├── infrastructure/      # Document, OCR, LLM và repository adapters
│   ├── services/            # Resume scanner và interview agents
│   ├── shared/schemas/      # Pydantic schemas dùng chung
│   ├── fipilot/             # Auth, interview engine, speech và persistence
│   ├── Knowledge/           # Kho tri thức theo role và level
│   └── alembic/             # Database migrations
├── frontend/                # Next.js application và API proxy
├── docs/                    # Tài liệu triển khai và video demo
└── README.md
```

## Yêu cầu

- Python 3.12 trở lên.
- [uv](https://docs.astral.sh/uv/).
- Node.js 24 trở lên và npm.
- Docker Engine với Docker Compose plugin.
- ffmpeg cho tính năng giọng nói.
- Một Azure OpenAI chat deployment và Azure Speech resource.

## Cấu hình

### Backend

Tạo `backend/.env` từ `backend/.env.example`:

```bash
cp backend/.env.example backend/.env
```

Cập nhật các biến sau:

```env
DATABASE_URL=postgresql+psycopg://fipilot:fipilot@127.0.0.1:5432/fipilot
COOKIE_SECURE=false

# Base URL, không dùng full Target URI /chat/completions?... của Azure Portal.
AZURE_OPENAI_BASE_URL=https://your-resource.openai.azure.com/openai/v1/
AZURE_OPENAI_API_KEY=your-api-key

# Điền deployment name, không phải endpoint và không phải embedding deployment.
AZURE_OPENAI_DEPLOYMENT=your-chat-deployment
AZURE_OPENAI_SIMPLE_DEPLOYMENT=your-chat-deployment
AZURE_OPENAI_COMPLEX_DEPLOYMENT=your-chat-deployment

AZURE_EMBEDDING_MODEL=text-embedding-3-small

AZURE_SPEECH_KEY=your-speech-key
AZURE_SPEECH_REGION=your-speech-region
AZURE_SPEECH_VOICE=vi-VN-HoaiMyNeural
```

Không commit `backend/.env`. Các file `.env.*` chứa secret cũng được ignore, ngoại trừ `.env.example`.

### Frontend

Tạo `frontend/.env.local`:

```env
RESUME_API_URL=http://127.0.0.1:8000
```

## Chạy local

### 1. PostgreSQL

```bash
cd backend
docker compose up -d postgres
```

Nếu máy không có Compose:

```bash
docker run --name fipilot-postgres \
  -e POSTGRES_DB=fipilot \
  -e POSTGRES_USER=fipilot \
  -e POSTGRES_PASSWORD=fipilot \
  -p 5432:5432 \
  -v fipilot-postgres:/var/lib/postgresql/data \
  -d postgres:17-alpine
```

### 2. Backend

```bash
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Kiểm tra:

- Health: <http://127.0.0.1:8000/health>
- Swagger UI: <http://127.0.0.1:8000/docs>

### 3. Frontend

Mở terminal khác:

```bash
cd frontend
npm install
npm run dev
```

Mở <http://localhost:3000>.

## Luồng sử dụng

1. Tạo tài khoản hoặc đăng nhập.
2. Chọn vị trí và cấp độ phỏng vấn.
3. Upload CV PDF/DOCX.
4. Kiểm tra thiết bị và bắt đầu phỏng vấn.
5. Trả lời bằng microphone hoặc văn bản.
6. Xem báo cáo và lịch sử phỏng vấn.

## API chính

| Method | Endpoint | Mục đích |
|---|---|---|
| `GET` | `/health` | Kiểm tra service và cấu hình database |
| `POST` | `/api/v1/auth/register` | Tạo tài khoản |
| `POST` | `/api/v1/auth/login` | Đăng nhập |
| `GET` | `/api/v1/auth/me` | Lấy người dùng hiện tại |
| `POST` | `/api/v1/resume/upload` | Upload và phân tích CV |
| `GET` | `/api/v1/resumes/latest` | Lấy CV gần nhất |
| `POST` | `/api/v1/interview/questions` | Sinh câu hỏi đầu tiên |
| `POST` | `/api/v1/interview/next` | Chấm câu trả lời và sinh câu tiếp theo |
| `POST` | `/api/v1/interview/report` | Tạo báo cáo cuối buổi |
| `GET` | `/api/v1/interviews` | Lấy lịch sử phỏng vấn |
| `POST` | `/api/v1/speech` | Tổng hợp giọng nói |
| `POST` | `/api/v1/speech/recognize` | Nhận dạng giọng nói |

Các endpoint v2 vẫn được giữ tại `/api/v2` cho pipeline service/gateway mới. Xem schema đầy đủ trong Swagger UI.

## Kiểm thử

```bash
cd backend
uv run python -m unittest discover -s test -p 'test_*.py' -v
uv run python -m compileall -q api core fipilot gateway infrastructure services shared

cd ../frontend
npm run typecheck -- --incremental false
```

## Docker

Build backend:

```bash
docker build -t fipilot-backend ./backend
```

Docker image không còn cài Torch/Ultralytics hoặc copy model YOLO. Database migration cần được chạy trước khi phục vụ request có persistence.

## Triển khai

Hướng dẫn triển khai Azure Container Apps, ACR và PostgreSQL Flexible Server nằm tại [docs/AZURE_DEPLOY.md](docs/AZURE_DEPLOY.md).

Khi chạy production:

- Đặt `COOKIE_SECURE=true`.
- Quản lý API key bằng secret store, không ghi trực tiếp vào image.
- Chỉ cho phép origin frontend tin cậy tại lớp ingress/API gateway.
- Chạy `alembic upgrade head` cho mỗi phiên bản schema mới.

## Trạng thái bàn giao

- Pipeline CV hiện tại: `DocumentService → ResumeAgent → PostgreSQL`.
- LLM chat: cấu hình thống nhất qua `.env`.
- Knowledge base được giữ lại vì interview engine sử dụng lúc tạo câu hỏi.
- Script vá tạm, notebook thử nghiệm, Azure ML prototype, log/debug artifact và SQLite cũ đã được loại bỏ.
- Backend unit tests, OpenAPI schema, document smoke-test, frontend typecheck và Docker build đã được xác nhận.
