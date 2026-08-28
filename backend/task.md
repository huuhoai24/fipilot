# Upload Resume Backend — Task List

## Các bước triển khai

- [x] Đọc notebook POC và kiến trúc hiện tại
- [/] Triển khai code

### Files cần tạo/sửa

- [x] `infrastructure/repositories/__init__.py` [NEW]
- [x] `infrastructure/repositories/postgres_repository.py` [NEW]
- [x] `infrastructure/documents/pdf_service.py` [MODIFY] — pymupdf4llm primary cho PDF
- [x] `gateway/__init__.py` [NEW]
- [x] `gateway/api/__init__.py` [NEW]
- [x] `gateway/api/resume.py` [NEW] — route POST /api/v2/resume/upload
- [x] `core/dependencies.py` [MODIFY] — get_resume_repository, get_current_user
- [x] `api/main.py` [MODIFY] — mount resume router
- [x] `pyproject.toml` — thêm python-docx, pypdf, pillow, rapidocr-onnxruntime
- [x] E2E test với CV_hoainh.docx — đang chờ LLM response
