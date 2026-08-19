import json
import os
import sys
import warnings
from pathlib import Path

# Tắt các cảnh báo không cần thiết
warnings.filterwarnings("ignore")

# Xác định ROOT (thư mục chứa script này)
ROOT = Path(__file__).resolve().parent
# Thêm ROOT vào sys.path để Python nhận diện được package `fipilot`
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

# Thiết lập HF Token nếu có để tăng tốc tải model từ Hugging Face
if os.getenv("HUGGINGFACE_API_KEY"):
    os.environ["HF_TOKEN"] = os.getenv("HUGGINGFACE_API_KEY")

from fipilot.resume_extraction import ResumeExtract


def main():
    print("🚀 Khởi tạo ResumeExtract...")
    # Khởi tạo bộ trích xuất thông tin (tự động load/download YOLO model từ config)
    extractor = ResumeExtract(dpi=150)

    # Đường dẫn tới file 1.pdf trong thư mục test
    pdf_path = ROOT / "test" / "CV_hoainh.pdf"

    if not pdf_path.exists():
        print(f"❌ Không tìm thấy file PDF tại: {pdf_path}")
        print(
            "Vui lòng kiểm tra lại xem file test/1.pdf có nằm trong thư mục hiện tại hay chưa."
        )
        return
    print(f"📄 Đang xử lý file PDF: {pdf_path.name}")
    print("⏳ Đang chạy pipeline phân tích cấu trúc layout và gọi LLM...")

    import time

    start_time = time.time()

    try:
        # Chạy pipeline bóc tách thông tin
        result_json = extractor.pipeline(pdf_path)

        elapsed_time = time.time() - start_time
        print("\n✅ HOÀN THÀNH!")
        print(
            f"⏱️ Thời gian xử lý: {elapsed_time:.2f} giây (~ {elapsed_time / 60:.2f} phút)"
        )
        print("\n📊 KẾT QUẢ TRÍCH XUẤT (JSON):")
        print(result_json)

    except Exception as e:
        print(f"❌ Đã xảy ra lỗi trong quá trình xử lý: {e}")


if __name__ == "__main__":
    main()
