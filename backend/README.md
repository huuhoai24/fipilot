# FiPilot Backend - Resume Parser & Structured Information Extractor
## 🌟 Tính năng nổi bật

1. **Nhận diện bố cục trực quan (Layout Detection)**
   - Sử dụng mô hình YOLOv8 (`ultralytics`) để nhận diện các khối văn bản/bố cục trên trang CV (được chuyển từ PDF thành hình ảnh).
   - Tự động loại bỏ các khối trùng lặp hoặc chồng lấn dựa trên thuật toán lọc IOA (Intersection over Area).

2. **Căn chỉnh và Tuyến tính hóa văn bản (Text Alignment & Linearization)**
   - Trích xuất văn bản thô từ tệp PDF gốc bằng PyMuPDF (`fitz`).
   - Gán tọa độ các dòng chữ vào khối bố cục tương ứng được phát hiện bởi YOLO (áp dụng kiểm tra trọng tâm dòng chữ nằm trong bounding box).
   - **Sắp xếp đa cấp độ (Multi-level sorting)**:
     - *Inter-segment sorting*: Sắp xếp các khối bố cục theo hàng và cột trên trang CV để đảm bảo đúng thứ tự đọc tự nhiên.
     - *Intra-segment sorting*: Sắp xếp các dòng văn bản bên trong từng khối theo thứ tự từ trên xuống dưới, từ trái qua phải.
   - Tuyến tính hóa toàn bộ văn bản của CV kèm theo chỉ số dòng (ví dụ: `[0]: text`) giúp LLM dễ dàng định vị vị trí dòng dữ liệu.

3. **Trích xuất thông tin có cấu trúc song song (Parallel LLM Extraction)**
   - Sử dụng Groq API (`llama-3.3-70b-versatile`) với định dạng JSON đầu ra ổn định.
   - Trích xuất dữ liệu song song qua `ThreadPoolExecutor` dựa trên các mẫu prompt Jinja2:
     - `match_info.jinja2`: Trích xuất vai trò công việc chuẩn hóa (Normalized Role), học vấn cao nhất (Education Level), và danh sách kỹ năng chuyên môn (Technical Skills).
     - `work_exp.jinja2`: Trích xuất lịch sử làm việc (Tên công ty, vị trí, thời gian bắt đầu/kết thúc, khoảng chỉ số dòng mô tả).
     - `project.jinja2`: Trích xuất các dự án cá nhân/học thuật nổi bật (Tên dự án, công nghệ sử dụng, khoảng chỉ số dòng mô tả).

4. **Hậu xử lý và Làm giàu dữ liệu (Data Enrichment & Utilities)**
   - Tính toán tổng số năm và số tháng kinh nghiệm thực tế dựa trên thông tin lịch sử làm việc được trích xuất.
   - Nhận diện và bỏ qua các tệp PDF dạng quét (Scanned PDF) không có lớp văn bản thực tế.
   - Công cụ lấy mẫu CV (`sample_resumes.py`) hỗ trợ phân bổ mẫu theo đúng tỉ lệ phân phối ban đầu (thuật toán Hamilton / phương pháp số dư lớn nhất).

---

## 📁 Cấu trúc thư mục dự án

```text
backend/
├── pyproject.toml              # Cấu hình dự án và danh sách thư viện phụ thuộc (uv)
├── uv.lock                     # UV lockfile
├── main.py                     # Entry point (stub)
├── .python-version             # Phiên bản Python sử dụng (>=3.12)
├── models/
│   └── yolo26_train_results/   # Lưu trữ trọng số mô hình YOLO (best.pt) dùng phát hiện bố cục
├── prompts/
│   ├── match_info.jinja2       # Prompt template trích xuất thông tin chung & kỹ năng
│   ├── project.jinja2          # Prompt template trích xuất dự án
│   └── work_exp.jinja2         # Prompt template trích xuất kinh nghiệm làm việc
├── src/
│   └── fipilot/
│       ├── __init__.py
│       ├── resume_extraction.py # Lớp chính ResumeExtract điều phối pipeline
│       ├── config/
│       │   ├── __init__.py
│       │   └── settings.py      # Cấu hình đường dẫn, ngưỡng IOA, LLM model, worker,...
│       └── utils/
│           ├── __init__.py
│           ├── resume_extract_module.py # Các hàm tiện ích (tính YOE, lọc box trùng, ghi file,...)
│           └── sample_resumes.py        # Tiện ích chia tách/lấy mẫu CV theo phân phối
├── notebooks/                   # Các Jupyter Notebook dùng trong quá trình nghiên cứu & phát triển
│   ├── 01_resume_parsing.ipynb
│   ├── 02_resume_detection_block.ipynb
│   └── 03_resume_extraction.ipynb
└── test/                        # Tệp tin PDF và hình ảnh chạy thử nghiệm
```

---

## 🛠 Hướng dẫn cài đặt và sử dụng

### 1. Yêu cầu hệ thống
- **Python**: Phiên bản 3.12 trở lên.
- Đã cài đặt công cụ quản lý package [**uv**](https://github.com/astral-sh/uv).
- Cần có khóa API của **Groq** (`GROQ_API_KEY`).

### 2. Cài đặt môi trường
Sử dụng `uv` để cài đặt nhanh chóng toàn bộ thư viện phụ thuộc:
```bash
# Đồng bộ hóa môi trường ảo và cài đặt dependencies
uv sync
```

### 3. Cấu hình biến môi trường
Tạo tệp `.env` ở thư mục gốc của dự án và cấu hình khóa API của Groq:
```env
GROQ_API_KEY=your_groq_api_key_here
```

Cấu hình dự án có thể điều chỉnh trực tiếp trong tệp `src/fipilot/config/settings.py`.

### 4. Chạy thử nghiệm trích xuất
Hệ thống sử dụng pipeline tích hợp trong `ResumeExtract`. Bạn có thể khởi chạy hoặc tích hợp vào code Python như sau:

```python
from fipilot.resume_extraction import ResumeExtract
from fipilot.config import cfg

# Khởi tạo bộ trích xuất CV
extractor = ResumeExtract(
    yolo_model=str(cfg.YOLO_MODEL),
    llm_model=cfg.LLM_MODEL,
    dpi=200,
    max_workers=cfg.MAX_WORKER,
    max_retries=cfg.MAX_RETRIES
)

# Cấu hình các template trích xuất
TEMPLATES = ["match_info.jinja2", "work_exp.jinja2", "project.jinja2"]
KEYS = ["match_info", "work_exp", "project"]

# Thực hiện trích xuất dữ liệu từ một CV PDF
result = extractor.process_create_data(
    pdf_path="test/2.pdf",
    txt_dir=str(cfg.TXT_DIR),
    json_dir=str(cfg.JSON_DIR),
    TEMPLATES=TEMPLATES,
    KEYS=KEYS
)

print(f"Kết quả trích xuất được lưu tại: {result}")
```

### 5. Sử dụng công cụ lấy mẫu CV (Sampling Tool)
Để lấy mẫu CV phục vụ việc huấn luyện hoặc đánh giá theo đúng phân phối từ các thư mục con:
```bash
uv run python src/fipilot/utils/sample_resumes.py --raw-dir data/raw/resumes --processed-dir data/processed/yolo --target 400
```
