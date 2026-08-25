# So sánh Đánh giá QuestGen & RAG: Azure OpenAI vs Google Cloud Vertex AI

Báo cáo đối sánh kết quả đánh giá thực nghiệm độc lập trên cùng 1 bộ dữ liệu chuẩn (300 mẫu Resume, 150 mẫu Holdout Test):

---

## 1. Bảng so sánh tổng quan giữa Azure OpenAI và Google Cloud

| Tiêu chí đánh giá (Metric) | Google Cloud (Gemini 2.5) | Azure OpenAI (GPT-4.1-mini) | So sánh & Nhận xét |
| :--- | :---: | :---: | :--- |
| **Model sử dụng** | `gemini-2.5-flash` / `pro` | `gpt41mini` (GPT-4.1-mini) | Cả 2 đều thuộc thế hệ SOTA mới nhất |
| **Retrieval HitRate@1** | 91.67% | 91.67% | Ngang nhau (dùng chung RAG Index) |
| **Retrieval HitRate@5 / HitRate@8** | 100.0% / 100.0% | 100.0% / 100.0% | Độ phủ tri thức 100% |
| **MRR@8** (Mean Reciprocal Rank) | 0.9564 | 0.9564 | Xếp hạng tri thức tối ưu |
| **Technical Validity Rate** | 100.0% | **100.0%** | Cả 2 đều chính xác 100% về mặt kỹ thuật |
| **Role Relevance Rate** | 100.0% | **100.0%** | Khớp 100% vị trí ứng tuyển |
| **CV-derived Skill Alignment** | 100.0% | **100.0%** | Khớp 100% kỹ năng trích xuất từ CV |
| **Mean Clarity** (Độ rõ ràng) | **5.00 / 5.0** | 4.85 / 5.0 | Gemini ngắn gọn hơn, GPT-4.1-mini chi tiết hơn |
| **Mean Specificity** (Độ sâu tình huống) | 1.54 / 2.0 | **2.00 / 2.0** | **Azure GPT-4.1-mini vượt trội** (hỏi sâu tình huống thực tế) |
| **Mean RAG Grounding** (Bám sát RAG) | 1.42 / 2.0 | **2.00 / 2.0** | **Azure GPT-4.1-mini vượt trội** (tận dụng tri thức RAG triệt để) |
| **Retrieval Utilization Rate** | 90.67% | **94.00%** | Azure OpenAI khai thác RAG tốt hơn (+3.33%) |
| **Difficulty Exact Match** | 83.33% | **100.0%** | Azure OpenAI phân loại đúng level 100% |
| **Exact Duplicate Rate** | 0.67% | **0.00%** | Azure OpenAI không bị trùng lặp |
| **False Premise Rate** | 0.00% | 0.00% | Không có câu hỏi nào đưa ra giả định sai |

---

## 2. Đường dẫn cấu trúc thư mục lưu trữ:

### 🔹 Dữ liệu Azure OpenAI (Mới):
- **Báo cáo tổng hợp**: [`docs/evaluation/cv_question_rag_azure/CV_QUESTION_RAG_REPORT.md`](file:///c:/Users/vderf/Downloads/ai-interview-platform-s%20(2)/ai-interview-platform-s/ai-interview-platform/docs/evaluation/cv_question_rag_azure/CV_QUESTION_RAG_REPORT.md)
- **Raw JSONL & Chấm điểm**: [`evaluation/cv_question_rag/raw/azure-openai-v1/`](file:///c:/Users/vderf/Downloads/ai-interview-platform-s%20(2)/ai-interview-platform-s/ai-interview-platform/evaluation/cv_question_rag/raw/azure-openai-v1)
- **Mẫu Human Review**: [`docs/evaluation/cv_question_rag_azure/HUMAN_REVIEW_TEMPLATE.csv`](file:///c:/Users/vderf/Downloads/ai-interview-platform-s%20(2)/ai-interview-platform-s/ai-interview-platform/docs/evaluation/cv_question_rag_azure/HUMAN_REVIEW_TEMPLATE.csv)

### 🔹 Dữ liệu Google Cloud (Cũ):
- **Báo cáo tổng hợp**: [`docs/evaluation/cv_question_rag_google/CV_QUESTION_RAG_REPORT.md`](file:///c:/Users/vderf/Downloads/ai-interview-platform-s%20(2)/ai-interview-platform-s/ai-interview-platform/docs/evaluation/cv_question_rag_google/CV_QUESTION_RAG_REPORT.md)
- **Toàn bộ Milestone evals cũ**:
  - `docs/evaluation/m0/` đến `docs/evaluation/m8/`
  - `evaluation/ragas_pilot/`
  - `evaluation/evidence/`
