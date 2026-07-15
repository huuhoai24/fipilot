import os
import sys
from pathlib import Path
import time
import json
import warnings
warnings.filterwarnings("ignore")

# Thêm thư mục src vào sys.path để import được module
sys.path.append(str(Path(__file__).resolve().parent / "src"))

from fipilot.resume_extraction import ResumeExtract
from fipilot.config.settings import cfg

def main():
    print("🚀 Khởi tạo model (có thể mất vài chục giây lần đầu)...")
    device = "cpu"
    
    # Khởi tạo extractor
    extractor = ResumeExtract(
        yolo_model=str(cfg.YOLO_MODEL),
        source_model="Alibaba-EI/SmartResume",
        llm_model="Qwen3-0.6B",
        dpi=150,
        max_workers=1,
        max_retries=1,
        device=device
    )

    # Đường dẫn đến file PDF test
    pdf_path = Path(__file__).resolve().parent / "test" / "AI_Engineer_candidate_dung-cong-anh-11835246.pdf"
    
    if not pdf_path.exists():
        print(f"❌ Không tìm thấy file PDF tại {pdf_path}")
        return

    print(f"\n📄 Đang xử lý file: {pdf_path.name}")
    print("⏳ Đang nhận diện bố cục và trích xuất text (Layout Detection)...")
    start_time = time.time()
    
    # 1. Trích xuất text từ CV
    t = time.time()
    boxes = extractor.layout_detection(pdf_path)
    print(f"  ⏱️  [1/6] Layout Detection (YOLO): {time.time() - t:.2f} giây.")
    
    t = time.time()
    boxes = extractor.remove_duplicate_boxes(boxes)
    print(f"  ⏱️  [2/6] Loại bỏ các box trùng lặp: {time.time() - t:.2f} giây.")
    
    t = time.time()
    boxes = extractor.inter_segment_sorting(boxes)
    print(f"  ⏱️  [3/6] Sắp xếp inter-segment: {time.time() - t:.2f} giây.")
    
    t = time.time()
    resume_lines = extractor.pair_resume(pdf_path)
    print(f"  ⏱️  [4/6] Trích xuất text / OCR: {time.time() - t:.2f} giây.")
    
    t = time.time()
    regions = extractor.intra_segment_sorting(boxes, resume_lines)
    print(f"  ⏱️  [5/6] Sắp xếp intra-segment: {time.time() - t:.2f} giây.")
    
    t = time.time()
    resume_text = extractor.linearize_layout_regions(regions)
    print(f"  ⏱️  [6/6] Chuyển đổi sang text tuyến tính: {time.time() - t:.2f} giây.")
    
    print(f"✅ Xong phần đọc text (Tổng cộng: {time.time() - start_time:.2f} giây).")
    
    print("\n🔍 5 dòng text đầu tiên trích xuất được để kiểm tra:")
    lines = resume_text.split('\n')
    for line in lines[:5]:
        print(f"  {line}")
    if len(lines) > 5:
        print(f"  ... và {len(lines) - 5} dòng khác.")
    
    # 2. Gọi LLM trích xuất
    print("\n🤖 Đang gọi LLM Qwen3 để bóc tách thông tin (Vì chạy CPU nên mất khoảng 1-3 phút)...")
    llm_start_time = time.time()
    
    TEMPLATES = ["match_info.jinja2", "work_exp.jinja2", "project.jinja2"]
    KEYS = ["match_info", "work_exp", "project"]
    
    try:
        # Gọi hàm extract_all - code sẽ tự detect và gọi combined prompt
        result = extractor.extract_all(resume_text, TEMPLATES, KEYS)
        
        llm_time = time.time() - llm_start_time
        print(f"\n✅ HOÀN THÀNH LLM TRÍCH XUẤT TRONG {llm_time:.2f} GIÂY! (Chạy Single-pass nhanh hơn 3 lần)")
        
        # In kết quả
        print("\n📊 KẾT QUẢ TRÍCH XUẤT (JSON):")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"❌ Có lỗi xảy ra trong quá trình trích xuất: {e}")

if __name__ == "__main__":
    main()
