# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 3) - Tập Đề Distributed Training và MLOps (3)

* **Role:** AI Engineer
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày sự khác biệt giữa hai chiến lược huấn luyện song song: Data Parallelism (DDP) và Model Parallelism.
* **expected_key_points:**
  - id: KP1_1
    content: Cơ chế Data Parallelism (DDP)
    keypoint_weight: 0.5
    description: Mô hình đầy đủ được nhân bản trên mỗi GPU. Dữ liệu được chia nhỏ, các GPU tính gradient độc lập rồi đồng bộ hóa gradients qua lệnh All-Reduce.
  - id: KP1_2
    content: Cơ chế Model Parallelism
    keypoint_weight: 0.5
    description: Áp dụng khi mô hình quá lớn không vừa 1 GPU. Chia nhỏ mô hình theo lớp (Pipeline Parallelism) hoặc chia nhỏ phép tính ma trận (Tensor Parallelism) qua nhiều GPU.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích khái niệm Data Drift và các phương pháp thống kê để phát hiện Data Drift trên hệ thống production.
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa Data Drift
    keypoint_weight: 0.4
    description: Là hiện tượng phân phối xác suất của dữ liệu đầu vào $P(X)$ thay đổi theo thời gian so với phân phối dữ liệu huấn luyện ban đầu.
  - id: KP2_2
    content: Phương pháp thống kê phát hiện
    keypoint_weight: 0.6
    description: Sử dụng kiểm định Kolmogorov-Smirnov (KS-test) cho biến liên tục, Chi-Square test cho biến phân loại, hoặc tính toán chỉ số PSI (Population Stability Index) và KL Divergence để đo khoảng cách phân phối.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Lượng tử hóa mô hình (Model Quantization) FP16 sang INT8 hoạt động ra sao? Phân biệt Post-Training Quantization (PTQ) và Quantization-Aware Training (QAT).
* **expected_key_points:**
  - id: KP3_1
    content: Nguyên lý lượng tử hóa
    keypoint_weight: 0.5
    description: Ánh xạ dải số thực FP16 sang dải số nguyên INT8 qua hệ số scale factor $S$ và zero-point $Z$ để giảm kích thước và tăng tốc độ tính toán.
  - id: KP3_2
    content: Phân biệt PTQ vs QAT
    keypoint_weight: 0.5
    description: PTQ lượng tử hóa sau khi train mà không cần huấn luyện lại (nhanh nhưng dễ mất độ chính xác). QAT mô phỏng sai số lượng tử hóa ngay trong quá trình train, giúp giữ nguyên độ chính xác tương đương FP16.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích chi tiết cơ chế hoạt động của thuật toán tối ưu hóa FlashAttention-2. Tại sao nó lại giúp tăng tốc độ huấn luyện mô hình Transformer đáng kể?
* **expected_key_points:**
  - id: KP4_1
    content: Tối ưu hóa I/O bộ nhớ và Tiling
    keypoint_weight: 0.5
    description: FlashAttention-2 chia nhỏ ma trận Query, Key, Value thành các khối (tiles) nạp vào bộ nhớ SRAM tốc độ cực nhanh của GPU để tính softmax từng phần, giảm thiểu số lần đọc ghi bộ nhớ HBM chậm.
  - id: KP4_2
    content: Song song hóa trên chiều dài chuỗi Query
    keypoint_weight: 0.5
    description: Phiên bản 2 cải tiến việc song song hóa trên chiều dài chuỗi của Query, phân bổ công việc tối ưu hơn qua các SMs của GPU, tăng tốc độ tính toán gấp đôi so với FlashAttention-1.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách thiết kế một hệ thống kiểm duyệt nội dung (Content Moderation System) tự động lọc văn bản và hình ảnh độc hại theo thời gian thực.
* **expected_key_points:**
  - id: KP6_1
    content: Pipeline xử lý đa phương thức (Multimodal Pipeline)
    keypoint_weight: 0.5
    description: Nhánh Text dùng mô hình BERT/LLM nhẹ phân loại. Nhánh Image dùng CNN/ViT phân loại ảnh nhạy cảm. Sử dụng bộ lọc băm ảnh (Perceptual Hashing) để lọc nhanh các ảnh vi phạm đã biết.
  - id: KP6_2
    content: Kiến trúc High Throughput và Caching
    keypoint_weight: 0.5
    description: Thiết lập Layer 1 dùng mô hình nhỏ nhanh để lọc 95% nội dung an toàn rõ ràng dưới 10ms; các nội dung nghi ngờ chuyển lên Layer 2 dùng mô hình nặng hơn xử lý.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế hoạt động của thuật toán tìm kiếm lân cận gần đúng ANN (Approximate Nearest Neighbors) bằng chỉ mục HNSW (Hierarchical Navigable Small World) trong Vector Database.
* **expected_key_points:**
  - id: KP7_1
    content: Cấu trúc đồ thị phân tầng của HNSW
    keypoint_weight: 0.6
    description: Xây dựng đồ thị nhiều tầng. Các tầng trên có liên kết thưa giúp tìm kiếm nhanh khoảng cách lớn (skip-list style). Các tầng dưới có liên kết dày giúp tinh chỉnh kết quả cục bộ.
  - id: KP7_2
    content: Ưu nhược điểm so với IVF-PQ
    keypoint_weight: 0.4
    description: HNSW cho tốc độ tìm kiếm cực nhanh và độ chính xác cao nhất, nhưng tốn lượng RAM rất lớn để lưu giữ đồ thị chỉ mục.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Làm thế nào để đo lường và tối ưu hóa độ trễ suy luận (Inference Latency) của mô hình Deep Learning lớn sử dụng TensorRT?
* **expected_key_points:**
  - id: KP5_1
    content: Quy trình chuyển đổi sang TensorRT
    keypoint_weight: 0.5
    description: Chuyển mô hình PyTorch sang ONNX -> dùng TensorRT builder để build engine tối ưu hóa riêng cho GPU cụ thể; cấu hình precision (FP16/INT8).
  - id: KP5_2
    content: Các kỹ thuật tối ưu hóa của TensorRT
    keypoint_weight: 0.5
    description: Thực hiện gộp lớp (layer fusion), lựa chọn thuật toán nhân ma trận tối ưu (kernel tuning), và quản lý động bộ nhớ đệm VRAM.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống MLflow & Kubeflow Pipeline tự động hóa hoàn toàn quy trình thu thập dữ liệu, phát hiện data drift, tự động trigger huấn luyện lại (Continuous Training), và deploy mô hình.
* **expected_key_points:**
  - id: KP8_1
    content: Thiết lập Pipeline Kubeflow và CDC
    keypoint_weight: 0.5
    description: Xây dựng Kubeflow pipeline dạng DAG: Data Prep -> Training -> Evaluation -> Validation. Dùng kafka/CDC theo dõi data và trigger pipeline khi chỉ số drift PSI vượt ngưỡng 0.2.
  - id: KP8_2
    content: Quản lý bằng MLflow Registry và CD
    keypoint_weight: 0.5
    description: MLflow ghi log siêu tham số, metrics, và model artifact. Xây dựng bước so sánh tự động: nếu mô hình mới (candidate) vượt qua độ chính xác của mô hình hiện tại (champion) và vượt qua bài test bias thì tự động cập nhật tag trong MLflow Model Registry để CD deploy.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp nén mô hình BERT lớn phục vụ cho việc deploy chạy trên thiết bị di động có dung lượng RAM cực nhỏ mà vẫn giữ được độ chính xác F1 > 95%.
* **expected_key_points:**
  - id: KP9_1
    content: Kết hợp các phương pháp nén mô hình
    keypoint_weight: 0.6
    description: Áp dụng cắt tỉa có cấu trúc (Structured Pruning) loại bỏ các heads attention ít quan trọng -> thực hiện lượng tử hóa sang INT8 -> áp dụng Knowledge Distillation (huấn luyện mô hình student nhỏ dựa trên teacher gốc).
  - id: KP9_2
    content: Tối ưu hóa chạy trên thiết bị di động
    keypoint_weight: 0.4
    description: Chuyển đổi mô hình sang ONNX Runtime Mobile hoặc TFLite để tận dụng bộ tăng tốc NPU trên điện thoại di động.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Hãy thiết kế hệ thống tìm kiếm hình ảnh tương đồng (Image Search Engine) quy mô 100 triệu ảnh. Yêu cầu thời gian phản hồi (latency) tìm kiếm < 150ms.
* **expected_key_points:**
  - id: KP10_1
    content: Embedding Pipeline và trích xuất đặc trưng
    keypoint_weight: 0.4
    description: Sử dụng mô hình CLIP ViT trích xuất ảnh thành vector 512 chiều; xây dựng batch pipeline để đẩy dữ liệu lên Vector DB.
  - id: KP10_2
    content: Vector Indexing và Cluster-based Retrieval
    keypoint_weight: 0.6
    description: Sử dụng chỉ mục IVF-PQ (Inverted File with Product Quantization) kết hợp HNSW để nén vector trên RAM và đảm bảo tốc độ quét lân cận dưới 50ms; cấu hình cache Redis lưu kết quả các truy vấn phổ biến.

