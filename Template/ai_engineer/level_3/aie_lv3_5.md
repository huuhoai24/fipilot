# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 3) - Tập Đề NLP và Bi-LSTM CRF (5)

* **Role:** AI Engineer
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày cấu trúc cơ bản và vai trò của mô hình Bi-LSTM kết hợp lớp CRF (Conditional Random Fields) trong bài toán trích xuất thực thể (NER).
* **expected_key_points:**
  - id: KP1_1
    content: Vai trò của Bi-LSTM
    keypoint_weight: 0.5
    description: Bi-LSTM học đặc trưng ngữ cảnh hai chiều của các từ trong câu, tạo ra vector đặc trưng cho từng token đầu vào.
  - id: KP1_2
    content: Vai trò của lớp CRF
    keypoint_weight: 0.5
    description: CRF học các ràng buộc tuần tự giữa các nhãn thực thể (ví dụ nhãn I-PER phải đi sau B-PER), tối ưu hóa xác suất của toàn bộ chuỗi nhãn thay vì dự đoán độc lập.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh cơ chế hoạt động của thuật toán sinh chữ Beam Search và Greedy Search. Khi nào nên điều chỉnh tham số Beam Width?
* **expected_key_points:**
  - id: KP2_1
    content: Cơ chế Beam Search vs Greedy Search
    keypoint_weight: 0.6
    description: Greedy Search chỉ chọn từ có xác suất cao nhất tại mỗi bước. Beam Search duy trì $B$ nhánh câu có xác suất tích lũy cao nhất để tìm kiếm giải pháp tối ưu hơn.
  - id: KP2_2
    content: Điều chỉnh Beam Width
    keypoint_weight: 0.4
    description: Tăng Beam Width giúp cải thiện chất lượng câu dịch/sinh chữ nhưng làm tăng thời gian tính toán tuyến tính; cần cân bằng tốc độ và chất lượng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tokenization là gì? Tại sao các mô hình ngôn ngữ lớn (LLM) hiện đại đều sử dụng Subword Tokenization thay vì Word Tokenization?
* **expected_key_points:**
  - id: KP3_1
    content: Khái niệm Tokenization
    keypoint_weight: 0.4
    description: Là bước tiền xử lý chia văn bản thành các đơn vị nhỏ hơn gọi là tokens (ký tự, từ, hoặc từ con).
  - id: KP3_2
    content: Lý do chọn Subword
    keypoint_weight: 0.6
    description: Giúp loại bỏ hoàn toàn lỗi Từ ngoài từ điển (OOV), kiểm soát kích thước từ điển không bị quá lớn, và giữ được cấu trúc tiền tố/hậu tố ngữ pháp của từ.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích chi tiết kiến trúc Transformer Encoder-Decoder (như T5) so với Decoder-only (như LLaMA). Trong trường hợp nào bạn chọn kiến trúc nào?
* **expected_key_points:**
  - id: KP4_1
    content: Kiến trúc Encoder-Decoder vs Decoder-only
    keypoint_weight: 0.5
    description: Encoder-Decoder có khối Encoder độc lập xử lý đầu vào rồi truyền thông tin qua Cross-Attention sang Decoder. Decoder-only xử lý cả đầu vào và đầu ra trên một khối duy nhất dùng masked attention.
  - id: KP4_2
    content: Lựa chọn áp dụng phù hợp
    keypoint_weight: 0.5
    description: Chọn Encoder-Decoder cho các tác vụ dịch máy, tóm tắt văn bản, trích xuất thông tin. Chọn Decoder-only cho sinh văn bản tự do, viết code, hội thoại (chatbot) do khả năng scaling tốt hơn.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích sự khác biệt giữa các mô hình ngôn ngữ LLaMA, Mistral, và Qwen về cơ chế chú ý Grouped-Query Attention (GQA).
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế GQA
    keypoint_weight: 0.6
    description: GQA chia các Query heads thành các nhóm. Mỗi nhóm Query heads sẽ dùng chung một cặp Key và Value head duy nhất. Nằm giữa Multi-Head Attention và Multi-Query Attention.
  - id: KP5_2
    content: Lợi ích đối với hệ thống
    keypoint_weight: 0.4
    description: Giảm dung lượng KV Cache lưu trữ trên VRAM GPU giúp tăng batch size và tốc độ suy luận mà không bị suy giảm độ chính xác.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách bạn đánh giá năng lực viết code của mô hình ngôn ngữ lớn (LLM) sử dụng bộ test HumanEval và chỉ số pass@k.
* **expected_key_points:**
  - id: KP6_1
    content: Quy trình đánh giá bằng HumanEval
    keypoint_weight: 0.5
    description: Cho LLM sinh code cho các bài toán lập trình mẫu; thực thi trực tiếp code sinh ra trong môi trường sandbox biệt lập với bộ unit tests tự động.
  - id: KP6_2
    content: Công thức và ý nghĩa pass@k
    keypoint_weight: 0.5
    description: pass@k đo tỷ lệ giải quyết bài toán thành công khi mô hình sinh $n$ mẫu thử và chọn ngẫu nhiên $k$ mẫu: $pass@k = \mathbb{E} [1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}]$ với $c$ là số mẫu vượt qua unit tests.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy giải thích chỉ số Perplexity (PPL) trong đánh giá mô hình ngôn ngữ. Công thức tính PPL từ Loss function (Cross-Entropy) là gì?
* **expected_key_points:**
  - id: KP7_1
    content: Định nghĩa Perplexity
    keypoint_weight: 0.5
    description: Đo lường mức độ bất ngờ hoặc độ không chắc chắn của mô hình ngôn ngữ khi dự đoán từ tiếp theo. Chỉ số này càng thấp mô hình dự đoán càng tốt.
  - id: KP7_2
    content: Công thức tính PPL từ Cross-Entropy Loss
    keypoint_weight: 0.5
    description: PPL là lũy thừa cơ số e của hàm loss Cross-Entropy: $PPL = e^{\mathcal{L}}$ (hoặc $2^{\mathcal{L}}$ tùy thuộc cơ số logarit).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống trích xuất thông tin bệnh án y khoa tiếng Việt phi cấu trúc (như triệu chứng, chẩn đoán, thuốc điều trị) từ văn bản bác sĩ gõ tự do.
* **expected_key_points:**
  - id: KP8_1
    content: Huấn luyện mô hình NER chuyên biệt
    keypoint_weight: 0.5
    description: Sử dụng PhoBERT hoặc ViBERT làm backbone; fine-tune trên tập dữ liệu bệnh án y khoa được gán nhãn theo định dạng BIO. Kết hợp CRF hoặc softmax lớp cuối để dự đoán thực thể.
  - id: KP8_2
    content: Chuẩn hóa thực thể y khoa (Entity Normalization/Linking)
    keypoint_weight: 0.5
    description: Xây dựng pipeline so khớp các thực thể trích xuất được với từ điển chuẩn quốc tế (như ICD-10 cho bệnh lý, RxNorm cho tên thuốc) bằng cách sử dụng vector embedding và thuật toán so khớp mờ để giải quyết lỗi chính tả viết tắt của bác sĩ.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp dịch thuật tài liệu pháp lý chuyên ngành tự động hỗ trợ 50 ngôn ngữ, tối ưu hóa bộ nhớ dịch thuật (Translation Memory) để đảm bảo tính nhất quán của thuật ngữ pháp lý.
* **expected_key_points:**
  - id: KP9_1
    content: Kiến trúc dịch máy kết hợp thuật ngữ (Terminology-constrained Translation)
    keypoint_weight: 0.5
    description: Sử dụng mô hình dịch thuật đa ngôn ngữ (như NLLB-200) fine-tune trên văn bản pháp luật. Tích hợp cơ chế ràng buộc thuật ngữ (Lexicon constraint): chèn trực tiếp các cặp thuật ngữ pháp lý chuẩn vào prompt hoặc ma trận attention để bắt mô hình dịch đúng từ quy định.
  - id: KP9_2
    content: Tích hợp Translation Memory (TM)
    keypoint_weight: 0.5
    description: Thiết lập Vector DB lưu trữ các câu pháp lý đã được dịch chuẩn bởi chuyên gia. Khi có tài liệu mới, truy vấn câu tương đồng từ TM; nếu độ tương đồng > 90%, lấy trực tiếp bản dịch cũ; ngược lại mới gửi qua mô hình dịch máy.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống tóm tắt tài liệu văn bản dài (Long-document Summarization - ví dụ báo cáo nghiên cứu 100 trang) vượt quá giới hạn cửa sổ ngữ cảnh của các mô hình LLM thông thường.
* **expected_key_points:**
  - id: KP10_1
    content: Chiến lược tóm tắt phân cấp (Hierarchical/MapReduce Summarization)
    keypoint_weight: 0.6
    description: Chia tài liệu thành các chương/mục nhỏ -> Giai đoạn Map: gửi từng phần qua LLM để sinh tóm tắt cục bộ -> Giai đoạn Reduce: ghép các bản tóm tắt cục bộ lại và tóm tắt một lần nữa để có kết quả tổng quan cuối cùng.
  - id: KP10_2
    content: Lưu trữ trạng thái ngữ cảnh (Memory-based/Incremental Summarization)
    keypoint_weight: 0.4
    description: Sử dụng cơ chế cập nhật nháp (incremental): đọc chương 1 -> tóm tắt -> dùng tóm tắt chương 1 làm ngữ cảnh đầu vào khi đọc và tóm tắt chương 2, đảm bảo luồng thông tin không bị ngắt quãng.

