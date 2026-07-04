# AI Interview Platform

Nền tảng phỏng vấn AI full-stack: React + TypeScript frontend, FastAPI backend (STT/TTS, LLM evaluation, CV parsing qua Ollama/Groq/OpenAI), kết nối real-time qua WebSocket.

## Kiến trúc

- **Frontend**: React 18 + TypeScript + Tailwind, dark navy/indigo design system, Zustand cho state, React Query cho data fetching.
- **Backend**: FastAPI (`backend/main.py`) — quản lý session, trích xuất CV, chấm điểm AI, text-to-speech, WebSocket cho phòng phỏng vấn real-time.
- **Giao tiếp**: REST (`/api/...`) cho CRUD + CV extraction; WebSocket (`/ws/interview/{session_id}`) cho luồng audio/text real-time trong lúc phỏng vấn.

## Đã triển khai

| Màn hình | Route | File | Trạng thái |
|---|---|---|---|
| Dashboard | `/` | `src/pages/DashboardPage.tsx` | Nối API (`api.getSessions`) |
| Interview Flow Wizard | `/interview-flow` | `src/pages/InterviewFlowPage.tsx` | Nối API (`api.extractCv`, `api.createSession`) |
| Interview Session (video/audio thật) | `/interview-flow/session/:id` | `src/pages/InterviewSessionPage.tsx` | WebSocket + webcam + mic thật |
| Template Manager | `/templates` | `src/pages/TemplateManagerPage.tsx` | Mock (chưa nối API) |
| Interview History | `/history` | `src/pages/HistoryPage.tsx` | Nối API (`api.getSessions`) |
| Evaluation Report | `/history/:id` | `src/pages/EvaluationReportPage.tsx` | Nối API (`api.getReport`) |
| Interview Settings | `/settings` | `src/pages/SettingsPage.tsx` | Mock (chưa nối API) |

Auth (login/register), phân quyền admin/user, danh sách "phỏng vấn đang chờ" vẫn dùng state phía client (`useAuthStore`, `useScheduleStore`) — chưa có endpoint backend tương ứng.

## Cài đặt & chạy

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend cần các biến môi trường cho LLM/TTS provider (xem `ai_services.py`, `tts_service.py` — dùng Groq/OpenAI/Ollama tuỳ cấu hình) và Ollama chạy local nếu dùng cho CV extraction. Database SQLite (`interview_app.db`) đã có sẵn, tự migrate khi khởi động (`migrate_db()` trong `main.py`).

### Frontend

Yêu cầu Node.js ≥ 18.

```bash
npm install
npm run dev
```

Mở `http://localhost:5173`. File `.env` đã cấu hình sẵn:

```
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws
```

Đổi giá trị này nếu backend chạy ở host/port khác.

Build production:

```bash
npm run build
npm run preview
```

## Cấu trúc frontend

```
src/
├── components/
│   ├── ui/                      # Button, Card, Badge, Input, Toggle, Slider — design system
│   ├── layout/                  # Sidebar (có sublist phiên đang chạy), AppLayout, UserMenu
│   ├── WaveformVisualizer.tsx   # dùng ở các màn hình mock, KHÔNG dùng trong InterviewSessionPage
│   ├── StepIndicator.tsx
│   └── CvDropzone.tsx
├── pages/                       # 7 màn hình chính
├── lib/api.ts                   # toàn bộ lời gọi REST tới backend FastAPI
├── data/mockData.ts             # mock data cho các phần chưa nối API (Templates, Settings)
├── types/index.ts
├── store/
│   ├── useAuthStore.ts          # auth giả lập phía client (chưa có endpoint backend)
│   ├── useScheduleStore.ts      # danh sách "đang chờ phỏng vấn", phía client
│   ├── useActiveSessionStore.ts # track các phòng phỏng vấn đang mở, phục vụ sidebar sublist
│   └── useAppStore.ts           # sidebar collapse, user menu toggle
└── lib/utils.ts
```

## Lưu ý quan trọng về `InterviewSessionPage`

Trang phỏng vấn thực tế (`/interview-flow/session/:id`) **không dùng** `WaveformVisualizer` hay mock data — đây là giao diện video-call thật:
- Mở webcam (`getUserMedia`) hiển thị video người dùng.
- Kết nối WebSocket tới `ws://.../ws/interview/{session_id}`.
- Ghi âm bằng `MediaRecorder` theo kiểu push-to-talk (giữ nút "Giữ để Trả lời"), gửi audio blob qua WebSocket.
- Nhận audio trả về từ AI, phát qua `AudioContext`; nhận text để hiển thị transcript (render markdown).
- Khi server gửi `status: "ENDED"` hoặc người dùng bấm nút kết thúc, gọi `api.endSession()` rồi chuyển sang trang Evaluation Report.

`useActiveSessionStore` chỉ làm nhiệm vụ phụ: ghi nhớ "phiên nào đang mở" để Sidebar hiển thị danh sách quay lại nhanh khi có nhiều phiên phỏng vấn chạy song song — nó không thay thế hay can thiệp vào logic WebSocket/audio ở trên.

## Việc còn thiếu để hoàn thiện tích hợp backend

- `TemplateManagerPage` và `SettingsPage` vẫn dùng mock data — cần thêm endpoint backend tương ứng rồi nối qua React Query giống các trang khác.
- Auth (`useAuthStore`) hoàn toàn phía client, không có bảng user/JWT thật ở backend — cần thêm nếu muốn nhiều người dùng thật đăng nhập độc lập.
- `useScheduleStore` (danh sách chờ) không persist ở backend — mất khi reload trang.

## Design tokens

- Background `#0F1117`, surface `#1A1D27`, accent indigo `#6366F1`
- Font: Inter (display/body) + JetBrains Mono (data/code)
- Xem `tailwind.config.js` cho toàn bộ token màu/spacing.
