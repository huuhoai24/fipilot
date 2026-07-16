# ==============================================================================
# Hướng dẫn chạy trên Google Colab:
#
# Bước 1: Cài đặt các thư viện cần thiết bằng cách chạy cell sau trên Colab:
# !pip install ultralytics pymupdf transformers torch pyyaml json-repair
#
# Bước 2: Đảm bảo bạn đã upload/mount thư mục chứa mã nguồn này (đặc biệt là thư mục fipilot, best.pt và test/1.pdf)
#
# Bước 3: Chạy script này bằng lệnh:
# !python run_colab.py
# ==============================================================================

import os
import sys
import json
from pathlib import Path
import warnings

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
from fipilot.configs.settings import cfg

def main():
    print("🚀 Khởi tạo ResumeExtract...")
    # Khởi tạo bộ trích xuất thông tin
    # cfg.YOLO_MODEL mặc định trỏ tới file best.pt nằm ở ROOT
    extractor = ResumeExtract(
        yolo_model=str(cfg.YOLO_MODEL),
        dpi=150
    )
    
    # Đường dẫn tới file 1.pdf trong thư mục test
    pdf_path = ROOT / "test" / "1.pdf"
    
    if not pdf_path.exists():
        print(f"❌ Không tìm thấy file PDF tại: {pdf_path}")
        print("Vui lòng kiểm tra lại xem file test/1.pdf có nằm trong thư mục hiện tại hay chưa.")
        return

    print(f"📄 Đang xử lý file PDF: {pdf_path.name}")
    print("⏳ Đang chạy pipeline phân tích cấu trúc layout và gọi LLM...")
    
    try:
        # Chạy pipeline bóc tách thông tin
        result_json = extractor.pipeline(pdf_path)
        
        print("\n✅ HOÀN THÀNH!")
        print("\n📊 KẾT QUẢ TRÍCH XUẤT (JSON):")
        print(result_json)
        
    except Exception as e:
        print(f"❌ Đã xảy ra lỗi trong quá trình xử lý: {e}")

if __name__ == "__main__":
    main()
