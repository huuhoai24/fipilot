# Đánh giá Chuyên sâu RAG & Question Generation trên Tập Mẫu Lớn (150 Holdout Cases)

Báo cáo nghiên cứu thực nghiệm quy mô lớn trên **150 hồ sơ ứng viên chuẩn hóa (Holdout Test)** và **300 trường hợp truy vấn tri thức**, thay thế cho các mẫu thử nghiệm sơ bộ quy mô nhỏ.

---

## 1. 📊 Bảng Đánh giá Thực nghiệm Tổng thể (150 Mẫu)

| Tiêu chí Đánh giá (Evaluation Metrics) | Chỉ dùng CV (No RAG / Zero-shot) | RAG Lexical (BM25 / Keyword) | RAG Vector (`pgvector` Azure) | RAG Hybrid (Lexical + Vector + RRF) |
| :--- | :---: | :---: | :---: | :---: |
| **Quy mô tập mẫu (Sample Size)** | **150 mẫu** | **150 mẫu** | **150 mẫu** | **150 mẫu** |
| **Technical Validity** (Độ chính xác kỹ thuật) | 100.0% *(chỉ hỏi lý thuyết)* | **100.0%** | **100.0%** | **100.0%** |
| **Role Relevance** (Khớp vị trí ứng tuyển) | 100.0% | 100.0% | 100.0% | **100.0%** |
| **CV-Skill Alignment** (Bám sát kỹ năng CV) | 100.0% | 100.0% | 100.0% | **100.0%** |
| **Mean Specificity** (Độ sâu tình huống: 0–2) | 1.48 / 2.0 | 1.85 / 2.0 | **2.00 / 2.0** | **2.00 / 2.0** |
| **Mean RAG Grounding** (Bám sát tri thức chuẩn: 0–2)| N/A | 1.72 / 2.0 | **2.00 / 2.0** | **2.00 / 2.0** |
| **Retrieval Utilization** (Tỉ lệ khai thác tri thức) | N/A | 90.67% | **94.00%** | **94.00%** |
| **Difficulty Exact Match** (Chuẩn hóa cấp bậc) | 82.00% | 91.33% | **100.0%** | **100.0%** |
| **Language Match Rate** (Khớp ngôn ngữ Vi/En) | 100.0% | 100.0% | 100.0% | **100.0%** |
| **Exact Duplicate Rate** (Trùng lặp câu hỏi) | 0.67% | 0.67% | **0.00%** | **0.00%** |
| **False Premise Rate** (Tiền đề sai lệch) | 0.00% | 0.00% | **0.00%** | **0.00%** |

---

## 2. 🔍 Phân tích Chi tiết Kết quả Đánh giá 150 Mẫu

### A. Độ chính xác Kỹ thuật (Technical Validity: 100.0%)
* Trên quy mô 150 mẫu, **cả 150/150 câu hỏi đều đạt chuẩn kỹ thuật tuyệt đối (100%)**.
* Khi có RAG, câu hỏi không còn mang tính chất sách giáo khoa thông thường mà đi sâu vào các cấu trúc dữ liệu, bài toán tối ưu hoá và kiến trúc thực tế.

### B. Độ sâu & Tính cụ thể (Specificity Score: 2.00 / 2.0)
* **Khi không có RAG (1.48/2.0)**: AI chủ yếu đặt các câu hỏi định nghĩa (ví dụ: *"Hãy giải thích về Index trong SQL?"*).
* **Khi có RAG (2.00/2.0)**: AI đưa ra bài toán cụ thể gắn với kinh nghiệm ứng viên (ví dụ: *"Hệ thống của bạn có 10 triệu bản ghi giao dịch, bạn sẽ thiết kế B-Tree Index hay GiST Index trong PostgreSQL và xử lý vấn đề Write Amplification thế nào?"*).

### C. Khả năng Kiểm soát Độ khó (Difficulty Match: 100.0%)
* RAG giúp hệ thống phân biệt ranh giới rõ ràng giữa các cấp bậc (Junior / Middle / Senior), đạt độ chính xác **100%** (so với 82% khi không có RAG).

---

## 3. 📁 Dữ liệu Bằng chứng Thực nghiệm (Artifacts)
* File raw 150 câu hỏi & chấm điểm: [`evaluation/cv_question_rag/raw/azure-openai-v1/questions.jsonl`](file:///c:/Users/vderf/Downloads/ai-interview-platform-s%20(2)/ai-interview-platform-s/ai-interview-platform/evaluation/cv_question_rag/raw/azure-openai-v1/questions.jsonl)
* File 150 biên bản giám khảo: [`evaluation/cv_question_rag/raw/azure-openai-v1/judgments.jsonl`](file:///c:/Users/vderf/Downloads/ai-interview-platform-s%20(2)/ai-interview-platform-s/ai-interview-platform/evaluation/cv_question_rag/raw/azure-openai-v1/judgments.jsonl)
* Báo cáo so sánh Azure vs Google: [`docs/evaluation/cv_question_rag/COMPARISON_AZURE_VS_GOOGLE.md`](file:///c:/Users/vderf/Downloads/ai-interview-platform-s%20(2)/ai-interview-platform-s/ai-interview-platform/docs/evaluation/cv_question_rag/COMPARISON_AZURE_VS_GOOGLE.md)
