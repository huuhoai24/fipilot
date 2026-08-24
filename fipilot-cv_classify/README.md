# FiPilot - AI-Powered Mock Interview Platform

> Azure pgvector setup and knowledge publishing: [backend/docs/azure-pgvector.md](backend/docs/azure-pgvector.md)

**FiPilot** là nền tảng luyện phỏng vấn kỹ thuật thông minh ứng dụng AI:
- **Phân tích cấu trúc CV (Resume Layout Extraction)**: Sử dụng mô hình YOLO ONNX và PyMuPDF để nhận diện bố cục, phân loại các khối kinh nghiệm, dự án, kỹ năng.
- **Sinh câu hỏi phỏng vấn sát thực tế (Adaptive Question Engine)**: Truy xuất dữ liệu chuyên ngành (Knowledge Index) kết hợp cùng thông tin từ CV ứng viên để sinh câu hỏi và bộ tiêu chí chấm điểm (Rubric).
- **Phỏng vấn thời gian thực bằng giọng nói & văn bản**: Hỗ trợ chuyển đổi giọng nói (STT / TTS) qua Azure Speech Service và giao diện tương tác trực tiếp.
- **Đánh giá & Chấm điểm tức thì (Real-time Evaluation)**: Chấm điểm từng lượt trả lời (Turn-by-turn evaluation) và tổng kết báo cáo năng lực chi tiết (Final Report).

---

## 1. Kiến trúc hệ thống (System Architecture)

```
fipilot/
├── backend/                       # Backend API & AI Core (Python / FastAPI)
│   ├── api/                       # RESTful API Endpoints (Auth, Resume, Interview, Speech)
│   ├── fipilot/                   # Core business logic & AI Pipelines
│   │   ├── auth.py                # Quản lý User Authentication & Session (Bcrypt, SHA-256)
│   │   ├── resume_extraction.py   # Pipeline bóc tách Resume (YOLO ONNX + PyMuPDF + LLM)
│   │   ├── interview_engine.py    # Điều phối tiến trình phỏng vấn & chấm điểm
│   │   ├── knowledge_index.py     # Tra cứu tri thức ngành nghề (Knowledge Domain)
│   │   ├── stt.py / tts.py        # Module xử lý giọng nói (Azure Speech + ffmpeg)
│   │   ├── models.py              # SQLAlchemy Schema (Users, Resumes, Interviews, Sessions)
│   │   └── persistence.py         # Tầng lưu trữ cơ sở dữ liệu PostgreSQL
│   ├── models/                    # Lưu trữ mô hình AI (best.onnx)
│   ├── Knowledge/                 # Cơ sở tri thức theo từng chuyên ngành (AI, Backend, Frontend...)
│   ├── pyproject.toml / uv.lock   # Quản lý gói phụ thuộc bằng uv
│   └── alembic/                   # Quản lý Database Migrations
│
├── frontend/                      # Giao diện Web (Next.js 16, React 19, TypeScript, Tailwind CSS)
│   ├── src/app/                   # App Router (Dashboard, Mock Interview Session, Feedback)
│   ├── src/components/            # UI Components & Mock Interview Stages
│   └── src/lib/                   # API Proxy, Auth Helpers & Client Identity
│
└── docs/                          # Hướng dẫn triển khai (Azure Deploy)
```

---

## 2. Yêu cầu môi trường (Prerequisites)

Trước khi bắt đầu, hãy đảm bảo máy tính của bạn đã cài đặt:
1. **Python**: Phiên bản 3.12 trở lên.
2. **uv**: Công cụ quản lý môi trường & package Python siêu nhanh (Khuyên dùng thay thế cho pip/venv).
   - Cài đặt nhanh `uv`:
     - **Linux/macOS**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
     - **Windows**: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
3. **Node.js**: Phiên bản 20.x hoặc 24.x (kèm `npm`).
4. **Docker**: Dùng để chạy PostgreSQL database.
5. **ffmpeg**: Bắt buộc để xử lý file âm thanh trong quá trình chuyển đổi giọng nói (STT / TTS).
   - **Linux (Ubuntu/Debian)**: `sudo apt update && sudo apt install -y ffmpeg`
   - **Linux (Arch/EndeavourOS)**: `sudo pacman -S ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Windows**: Tải qua [ffmpeg.org](https://ffmpeg.org/download.html) và thêm vào System PATH.

---

## 3. Cấu hình biến môi trường (Environment Variables)

### Cấu hình Backend (`backend/.env`)
Tạo file `backend/.env` từ file mẫu `backend/.env.example`:

```env
# Database kết nối PostgreSQL cục bộ
DATABASE_URL=postgresql+psycopg://fipilot:fipilot@127.0.0.1:5432/fipilot
COOKIE_SECURE=false

# Azure AI Services & LLM Keys
AZURE_OPENAI_API_KEY="<YOUR_AZURE_OPENAI_API_KEY>"
AZURE_FOUNDRY_ENDPOINT="https://<your-resource>.services.ai.azure.com"
AZURE_FOUNDRY_API_KEY="<YOUR_AZURE_FOUNDRY_API_KEY>"
AZURE_EMBEDDING_MODEL="text-embedding-3-small"

# Azure Speech (Voice AI)
AZURE_SPEECH_KEY="<YOUR_AZURE_SPEECH_KEY>"
AZURE_SPEECH_REGION="centralindia"
AZURE_SPEECH_VOICE="en-US-Harper:MAI-Voice-2"

# HuggingFace (Tùy chọn tải layout model bổ sung)
HUGGINGFACE_API_KEY="<YOUR_HF_TOKEN>"
```

### Cấu hình Frontend (`frontend/.env.local`)
Tạo file `frontend/.env.local` (nếu chạy local thì Next.js tự động mặc định proxy về `http://localhost:8000`):

```env
RESUME_API_URL=http://localhost:8000
```

---

## 4. Hướng dẫn cài đặt & Khởi chạy End-to-End với `uv` (Local)

### Bước 1: Khởi động Cơ sở dữ liệu (PostgreSQL)

Mở Terminal và chạy:

```bash
cd backend

# Cách 1: Khởi động container có sẵn
docker start fipilot-postgres

# Hoặc Cách 2: Tạo mới container nếu chưa từng tạo
docker run --name fipilot-postgres \
  -e POSTGRES_DB=fipilot \
  -e POSTGRES_USER=fipilot \
  -e POSTGRES_PASSWORD=fipilot \
  -p 5432:5432 \
  -v fipilot-postgres:/var/lib/postgresql/data \
  -d postgres:17-alpine
```

---

### Bước 2: Đồng bộ Dependencies & Khởi chạy Backend với `uv`

Tại thư mục `backend`:

```bash
cd backend

# 1. Cài đặt và đồng bộ toàn bộ dependencies từ uv.lock (Tự động tạo .venv nếu chưa có)
uv sync

# 2. Chạy Database Migrations để tạo bảng
uv run alembic upgrade head

# 3. Khởi động Backend Server (Port 8000)
uv run uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

> 🔍 **Kiểm tra Backend**: Mở trình duyệt truy cập Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### Bước 3: Cài đặt Dependencies & Khởi chạy Frontend

Mở một cửa sổ Terminal mới:

```bash
cd frontend

# 1. Cài đặt các gói npm
npm install

# 2. Khởi chạy Next.js Development Server (Port 3000)
npm run dev
```

> 🌐 **Truy cập Ứng dụng**: Mở trình duyệt vào [http://localhost:3000](http://localhost:3000)

---

## 5. Quy trình trải nghiệm người dùng (End-to-End Flow)

1. **Đăng ký & Đăng nhập**:
   - Nhấn nút **"Try for free"** hoặc **"Sign In"** ở góc phải trên.
   - Nhập thông tin để tạo tài khoản hoặc đăng nhập. Hệ thống sẽ cấp phát phiên làm việc an toàn (`HttpOnly Cookie`).
2. **Chọn Role & Tải CV**:
   - Lựa chọn vị trí muốn phỏng vấn (ví dụ: *AI Engineer, Backend Developer, Frontend Developer...*) và cấp độ (*Junior, Middle, Senior*).
   - Tải lên file CV định dạng `.pdf`. Mô hình YOLO ONNX sẽ tự động phân tích khối và trích xuất dự án/kỹ năng.
3. **Tiến hành Phỏng vấn**:
   - Hệ thống phát câu chào bằng giọng nói và đặt câu hỏi mở đầu.
   - Ứng viên có thể trả lời bằng **Microphone (giọng nói)** hoặc bật khung **Chat** để gõ văn bản.
   - AI chấm điểm theo rubric, phản hồi và đặt câu hỏi đào sâu (Follow-up questions).
4. **Xem Báo cáo Tổng kết (Feedback Report)**:
   - Kết thúc buổi phỏng vấn, hệ thống tự động tổng hợp toàn bộ các turn hỏi - đáp.
   - Hiển thị điểm số chuẩn hóa, điểm mạnh, điểm yếu và các đề xuất cải thiện chuyên môn.
   - Lịch sử buổi phỏng vấn sẽ được lưu lại trong mục **Interview History** trên Dashboard.

---

## 6. Hướng dẫn Triển khai lên Cloud (Deploy to Azure)

Dự án đã được đóng gói sẵn Docker tối ưu và có thể deploy lên **Azure Container Apps**:

- **Chi tiết các bước triển khai Azure**: Tham khảo file tài liệu [`docs/AZURE_DEPLOY.md`](docs/AZURE_DEPLOY.md).
- **Tóm tắt quy trình deploy Azure**:
  1. Tạo Azure Container Registry (ACR) và PostgreSQL Flexible Server.
  2. Build và Push Docker Image cho Backend và Frontend.
  3. Deploy 2 Container Apps (`fipilot-backend` và `fipilot-frontend`).
  4. Chạy `alembic upgrade head` trực tiếp trong Backend Container App để khởi tạo Database.
