# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 2) - Tập Đề Optimization và PEFT (2)

* **Role:** AI Engineer
* **Level:** Level 2
* **Experience:** 1 - 3  năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt ý nghĩa của các chỉ số Precision, Recall và F1-Score. Khi nào bạn sẽ ưu tiên tối ưu hóa Precision hơn Recall và ngược lại?
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa các chỉ số
    keypoint_weight: 0.5
    description: Precision = TP / (TP + FP) (tỷ lệ dự đoán đúng trong số dự đoán dương). Recall = TP / (TP + FN) (tỷ lệ phát hiện đúng trong số thực tế dương). F1-Score là trung bình điều hòa của Precision và Recall.
  - id: KP1_2
    content: Trường hợp ưu tiên cụ thể
    keypoint_weight: 0.5
    description: Ưu tiên Precision khi chi phí cho False Positive cao (ví dụ: bộ lọc thư rác Spam Filter). Ưu tiên Recall khi chi phí cho False Negative cao (ví dụ: chẩn đoán bệnh ung thư).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh sự khác nhau giữa thuật toán phân cụm K-Means và DBSCAN về nguyên lý hoạt động, ưu nhược điểm.
* **expected_key_points:**
  - id: KP2_1
    content: Nguyên lý K-Means vs DBSCAN
    keypoint_weight: 0.5
    description: K-Means dựa trên khoảng cách tới tâm cụm (centroid), yêu cầu khai báo trước số cụm K. DBSCAN dựa trên mật độ điểm lân cận (tham số eps, min_samples), tự động tìm số lượng cụm.
  - id: KP2_2
    content: Hình dạng cụm và nhiễu (Noise)
    keypoint_weight: 0.5
    description: K-Means chỉ phân cụm dạng hình cầu và bắt buộc mọi điểm phải thuộc cụm. DBSCAN phân được cụm hình dạng bất kỳ và có khả năng phát hiện nhiễu (outliers) không thuộc cụm nào.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày bản chất của thuật toán Random Forest. Cách tính lỗi Out-of-Bag (OOB) error là gì và vai trò của nó?
* **expected_key_points:**
  - id: KP3_1
    content: Bản chất thuật toán Random Forest
    keypoint_weight: 0.5
    description: Là phương pháp ensemble học máy dựa trên cơ chế Bagging (Bootstrap Aggregating) kết hợp ngẫu nhiên hóa đặc trưng (feature randomness) trên nhiều cây quyết định để giảm variance.
  - id: KP3_2
    content: Khái niệm và vai trò của OOB Error
    keypoint_weight: 0.5
    description: OOB error được tính trên các mẫu dữ liệu không được lựa chọn (chiếm khoảng 36.8%) trong quá trình bootstrap của mỗi cây. Dùng để đánh giá độ chính xác của mô hình tương đương như tập validation mà không cần chia tập dữ liệu riêng.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích sự khác biệt trong cơ chế cập nhật trọng số của các thuật toán tối ưu hóa: SGD, RMSprop và Adam. Tại sao Adam được sử dụng phổ biến nhất?
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế hoạt động từng optimizer
    keypoint_weight: 0.6
    description: SGD cập nhật dựa trực tiếp trên gradient hiện tại (có thể kèm Momentum). RMSprop điều chỉnh learning rate cho từng trọng số dựa trên trung bình động bình phương gradient (giải quyết dao động). Adam kết hợp cả hai: Momentum (moment thứ nhất) và RMSprop (moment thứ hai).
  - id: KP4_2
    content: Lý do Adam phổ biến
    keypoint_weight: 0.4
    description: Adam tự động điều chỉnh learning rate thích ứng, hội tụ nhanh, hoạt động tốt trên dữ liệu thưa (sparse gradients) và ít nhạy cảm với cấu hình siêu tham số ban đầu.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày chi tiết cơ chế Self-Attention trong kiến trúc Transformer. Tại sao nó lại vượt trội hơn RNN trong xử lý ngữ cảnh dài?
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế toán học của Self-Attention
    keypoint_weight: 0.6
    description: Chuyển vector đầu vào thành 3 ma trận Query (Q), Key (K), Value (V). Tính điểm attention: `Attention(Q, K, V) = softmax(Q K^T / sqrt(d_k)) V`. Thể hiện mối quan hệ giữa mọi cặp từ trong câu.
  - id: KP5_2
    content: Ưu thế so với RNN
    keypoint_weight: 0.4
    description: RNN xử lý tuần tự (sequential) dễ bị mất thông tin ngữ cảnh dài và không thể song song hóa. Self-Attention tính toán song song hoàn toàn trên toàn bộ chuỗi đầu vào, bắt được quan hệ tầm xa (long-range dependencies) bất kể khoảng cách.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt hai phương pháp Ensemble Learning: Bagging và Boosting. Nêu ví dụ về một thuật toán đại diện cho mỗi loại.
* **expected_key_points:**
  - id: KP6_1
    content: Bản chất Bagging vs Boosting
    keypoint_weight: 0.6
    description: Bagging huấn luyện các mô hình độc lập song song trên các mẫu bootstrap dữ liệu, mục tiêu giảm variance (ví dụ Random Forest). Boosting huấn luyện các mô hình tuần tự nối tiếp nhau, mô hình sau sửa sai cho mô hình trước bằng cách gán trọng số lớn hơn cho mẫu lỗi, mục tiêu giảm bias.
  - id: KP6_2
    content: Thuật toán đại diện cụ thể
    keypoint_weight: 0.4
    description: Bagging: Random Forest. Boosting: AdaBoost, Gradient Boosting, XGBoost, hoặc LightGBM.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Làm thế nào để xử lý bài toán mất cân bằng dữ liệu (imbalanced dataset) nghiêm trọng trong mô hình phân loại nhị phân? Hãy nêu các giải pháp ở cấp độ dữ liệu và cấp độ mô hình.
* **expected_key_points:**
  - id: KP7_1
    content: Giải pháp ở cấp độ dữ liệu
    keypoint_weight: 0.5
    description: Sử dụng các kỹ thuật resampling: Oversampling tập thiểu số (SMOTE, ADASYN) hoặc Undersampling tập đa số; chú ý chỉ áp dụng resampling trên tập train, không áp dụng trên tập validation/test.
  - id: KP7_2
    content: Giải pháp ở cấp độ mô hình/loss function
    keypoint_weight: 0.5
    description: Sử dụng tham số class_weight để phạt nặng hơn lỗi trên lớp thiểu số; sử dụng Focal Loss (giảm trọng số các mẫu dễ phân loại, tập trung mẫu khó); thay đổi metric đánh giá từ Accuracy sang F1-score/ROC-AUC.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** So sánh hai phương pháp Fine-tuning LLM: Full Fine-tuning và Parameter-Efficient Fine-tuning (PEFT) sử dụng LoRA (Low-Rank Adaptation) / QLoRA. Phân tích về tài nguyên tính toán và hiệu năng.
* **expected_key_points:**
  - id: KP8_1
    content: Cơ chế hoạt động của LoRA và QLoRA
    keypoint_weight: 0.5
    description: LoRA đóng băng các trọng số gốc $W_0$ của Transformer và thêm các ma trận tích cập nhật hạng thấp $A$ và $B$ ($W = W_0 + B A$). QLoRA nâng cấp LoRA bằng cách lượng tử hóa trọng số gốc sang dạng 4-bit NormalFloat (NF4) kết hợp Double Quantization để tiết kiệm tối đa VRAM.
  - id: KP8_2
    content: So sánh về tài nguyên và hiệu năng
    keypoint_weight: 0.5
    description: Full Fine-tuning cập nhật toàn bộ tham số, yêu cầu VRAM cực lớn (gấp nhiều lần kích thước mô hình để chứa gradients/optimizer states). LoRA/QLoRA giảm số tham số cần huấn luyện >99%, cho phép train mô hình lớn trên 1 GPU dân dụng mà vẫn giữ được chất lượng tương đương.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống công cụ tìm kiếm ngữ nghĩa (Semantic Search Engine) cho kho tài liệu khổng lồ chứa hàng triệu văn bản. Hãy đề xuất giải pháp xử lý và tối ưu hóa.
* **expected_key_points:**
  - id: KP9_1
    content: Xây dựng pipeline nhúng dữ liệu (Embedding Pipeline)
    keypoint_weight: 0.5
    description: Sử dụng mô hình embedding (ví dụ Sentence-Transformers, Cohere) chuyển đổi văn bản thành vector mật độ cao (dense vectors); lưu trữ và lập chỉ mục (index) trong Vector DB (như Pinecone, Milvus, Qdrant) sử dụng thuật toán HNSW (Hierarchical Navigable Small World).
  - id: KP9_2
    content: Tối ưu hóa tìm kiếm và hybrid search
    keypoint_weight: 0.5
    description: Kết hợp Dense Retrieval (Semantic) và Sparse Retrieval (BM25/Keyword) bằng kỹ thuật Hybrid Search, đi kèm mô hình Cross-Encoder Re-ranker ở phase cuối để tăng độ chính xác kết quả.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Bạn gặp kịch bản deploy một mô hình LLM lớn lên hệ thống production nhưng bị giới hạn tài nguyên GPU (VRAM). Hãy đề xuất các giải pháp kỹ thuật để tối ưu hóa throughput (số token xử lý/giây) và giảm latency.
* **expected_key_points:**
  - id: KP10_1
    content: Kỹ thuật tối ưu bộ nhớ VRAM
    keypoint_weight: 0.5
    description: Áp dụng Quantization (GPTQ, AWQ sang 4-bit/8-bit), sử dụng KV Cache Quantization và chia sẻ KV Cache qua PagedAttention (giống vLLM) để tối ưu hóa không gian bộ nhớ đệm.
  - id: KP10_2
    content: Kỹ thuật tối ưu hóa luồng xử lý (Inference Optimization)
    keypoint_weight: 0.5
    description: Sử dụng Continuous Batching (ghép các request động), Tensor Parallelism để phân tách mô hình qua nhiều GPU, và Speculative Decoding (dùng mô hình nhỏ sinh nháp, mô hình lớn verify) để đẩy nhanh tốc độ sinh token.

