# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 2) - Tập Đề Loss Functions và RAG (1)

* **Role:** AI Engineer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt sự khác biệt cốt lõi giữa ba hàm mất mát: Mean Squared Error (MSE), Cross-Entropy Loss, và Huber Loss. Khi nào nên dùng loại nào?
* **expected_key_points:**
  - id: KP1_1
    content: Bản chất toán học và phạm vi áp dụng
    keypoint_weight: 0.5
    description: MSE dùng cho bài toán hồi quy (đầu ra liên tục), phạt nặng các sai số lớn. Cross-Entropy dùng cho phân loại (xác suất phân phối lớp). Huber Loss là sự kết hợp giữa MSE và MAE, giảm tác động của outliers.
  - id: KP1_2
    content: Độ nhạy với Outliers
    keypoint_weight: 0.5
    description: MSE cực kỳ nhạy cảm với outliers do bình phương sai số. Huber Loss hoạt động giống MSE khi sai số nhỏ và giống MAE khi sai số lớn, giúp mô hình ổn định trước nhiễu.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày sự khác nhau giữa hai kỹ thuật giảm chiều dữ liệu PCA (Principal Component Analysis) và t-SNE (t-Distributed Stochastic Neighbor Embedding) về mục đích và đặc trưng.
* **expected_key_points:**
  - id: KP2_1
    content: Nguyên lý hoạt động tuyến tính vs phi tuyến
    keypoint_weight: 0.5
    description: PCA là kỹ thuật tuyến tính nhằm giữ lại phương sai lớn nhất của dữ liệu trên các trục chiếu mới. t-SNE là kỹ thuật phi tuyến dựa trên xác suất, bảo toàn cấu trúc lân cận gần của dữ liệu.
  - id: KP2_2
    content: Mục đích sử dụng chính
    keypoint_weight: 0.5
    description: PCA thường dùng để giảm chiều tiền xử lý trước khi đưa vào mô hình học máy. t-SNE chủ yếu dùng để trực quan hóa dữ liệu trong không gian 2D/3D.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích tác động của L1 (Lasso) và L2 (Ridge) Regularization lên các trọng số (weights) của mô hình. Tại sao L1 lại tạo ra sự thưa thớt (sparsity)?
* **expected_key_points:**
  - id: KP3_1
    content: Tác động lên trọng số của L1 và L2
    keypoint_weight: 0.5
    description: L1 cộng thêm trị tuyệt đối của trọng số vào loss function, có xu hướng triệt tiêu trọng số về đúng 0. L2 cộng thêm bình phương trọng số, thu nhỏ trọng số về gần 0 nhưng không bằng 0.
  - id: KP3_2
    content: Lý do L1 tạo ra tính thưa thớt (sparsity)
    keypoint_weight: 0.5
    description: Do dạng hình học của L1 regularization boundary có các đỉnh nhọn nằm trên các trục tọa độ, khiến nghiệm tối ưu dễ rơi vào các điểm làm một số trọng số bằng 0 (lọc đặc trưng tự động).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Hiện tượng Vanishing Gradient và Exploding Gradient trong Deep Learning là gì? Hãy nêu nguyên nhân và ít nhất 3 giải pháp khắc phục phổ biến.
* **expected_key_points:**
  - id: KP4_1
    content: Bản chất và nguyên nhân hiện tượng
    keypoint_weight: 0.5
    description: Xảy ra khi lan truyền ngược qua mạng nơ-ron sâu; vanishing làm gradient cực nhỏ khiến weights không cập nhật; exploding làm gradient cực lớn gây phân kỳ/mất ổn định. Nguyên nhân do kích hoạt sigmoid/tanh hoặc nhân ma trận nhiều lớp.
  - id: KP4_2
    content: Các giải pháp khắc phục
    keypoint_weight: 0.5
    description: Nêu được ít nhất 3 giải pháp: Sử dụng hàm kích hoạt ReLU/GELU, Batch Normalization, Skip Connections (kiểu ResNet), Khởi tạo trọng số (He/Xavier initialization), hoặc Gradient Clipping.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày luồng hoạt động cơ bản của hệ thống RAG (Retrieval-Augmented Generation) và cách bạn đánh giá chất lượng của thành phần Retrieval.
* **expected_key_points:**
  - id: KP5_1
    content: Luồng hoạt động của hệ thống RAG
    keypoint_weight: 0.5
    description: User query -> chuyển thành vector embedding -> truy vấn vector DB tìm k đoạn văn bản liên quan nhất (Retrieval) -> ghép query và ngữ cảnh làm prompt -> gửi LLM sinh câu trả lời (Generation).
  - id: KP5_2
    content: Đánh giá chất lượng Retrieval
    keypoint_weight: 0.5
    description: Sử dụng các chỉ số như Hit Rate (tỷ lệ tìm thấy đoạn chứa đáp án), MRR (Mean Reciprocal Rank), Precision@K, Recall@K, hoặc sử dụng LLM-as-a-judge để đánh giá mức độ liên quan (context relevance).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Rò rỉ dữ liệu (Data Leakage) là gì? Hãy nêu 2 trường hợp rò rỉ dữ liệu phổ biến trong quá trình tiền xử lý và cách bạn thiết lập pipeline để tránh hiện tượng này.
* **expected_key_points:**
  - id: KP6_1
    content: Bản chất và ví dụ về Data Leakage
    keypoint_weight: 0.5
    description: Là hiện tượng thông tin từ tập validation/test vô tình bị đưa vào quá trình huấn luyện mô hình. Ví dụ: Tính toán mean/std của toàn bộ tập dữ liệu trước khi split, hoặc sử dụng target encoding trên toàn bộ tập dữ liệu.
  - id: KP6_2
    content: Thiết lập pipeline phòng tránh
    keypoint_weight: 0.5
    description: Chia dữ liệu thành train/val/test trước tiên. Chỉ fit các bộ scaler/encoder trên tập train, sau đó transform lên tập val và test.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy so sánh sự khác nhau về Inductive Bias (định kiến quy nạp) của mạng CNN và kiến trúc Transformer đối với dữ liệu hình ảnh.
* **expected_key_points:**
  - id: KP7_1
    content: Inductive Bias của CNN
    keypoint_weight: 0.5
    description: CNN có inductive bias mạnh mẽ: translation invariance (bất biến dịch chuyển) và locality (tính cục bộ - các pixel gần nhau có quan hệ chặt chẽ). Giúp hội tụ nhanh trên tập dữ liệu nhỏ.
  - id: KP7_2
    content: Inductive Bias của Transformer
    keypoint_weight: 0.5
    description: Transformer có inductive bias rất yếu, không giả định cấu trúc không gian của ảnh (sử dụng self-attention toàn cục). Cần lượng dữ liệu lớn (như ViT) để học các mẫu không gian nhưng có giới hạn trần hiệu năng cao hơn CNN.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Khi triển khai mô hình lên các thiết bị Edge (như điện thoại di động, camera IoT), hãy phân tích sự khác biệt giữa Post-Training Quantization (PTQ) và Quantization-Aware Training (QAT) về quy trình thực hiện, hiệu năng và độ chính xác.
* **expected_key_points:**
  - id: KP8_1
    content: Phân tích Post-Training Quantization (PTQ)
    keypoint_weight: 0.5
    description: Thực hiện lượng tử hóa (ví dụ FP32 sang INT8) sau khi mô hình đã train xong mà không cần huấn luyện lại. Quy trình nhanh, nhưng có thể làm suy giảm độ chính xác đáng kể trên các mô hình nhạy cảm.
  - id: KP8_2
    content: Phân tích Quantization-Aware Training (QAT)
    keypoint_weight: 0.5
    description: Mô phỏng sai số lượng tử hóa (fake quantization) ngay trong quá trình train thông qua lan truyền ngược. Tốn thời gian huấn luyện nhưng giữ được độ chính xác gần như tương đương FP32.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp xử lý vấn đề Cold Start (người dùng mới hoặc sản phẩm mới chưa có lịch sử tương tác) trong hệ thống khuyến nghị (Recommender System).
* **expected_key_points:**
  - id: KP9_1
    content: Giải quyết Cold Start cho Người dùng mới
    keypoint_weight: 0.5
    description: Sử dụng khảo sát ban đầu khi đăng ký, hiển thị các sản phẩm phổ biến nhất (popularity-based), hoặc lọc cộng tác dựa trên demographic (tuổi, giới tính, vùng miền).
  - id: KP9_2
    content: Giải quyết Cold Start cho Sản phẩm mới
    keypoint_weight: 0.5
    description: Sử dụng Content-based filtering (phân tích đặc trưng văn bản, hình ảnh của sản phẩm để map vào sở thích user) hoặc áp dụng thuật toán Multi-Armed Bandit (Epsilon-greedy) để phân bổ lượt hiển thị thử nghiệm.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Hãy thiết kế kiến trúc hệ thống phát hiện giao dịch gian lận (Fraud Detection) thời gian thực. Hệ thống phải đáp ứng độ trễ (latency) dưới 100ms và xử lý hàng ngàn giao dịch mỗi giây.
* **expected_key_points:**
  - id: KP10_1
    content: Thiết kế Feature Store và Streaming Pipeline
    keypoint_weight: 0.4
    description: Sử dụng Kafka/Flink để xử lý luồng dữ liệu giao dịch thời gian thực; tích hợp Feature Store (ví dụ: Redis/Feast) để lấy nhanh các đặc trưng lịch sử của user với độ trễ thấp.
  - id: KP10_2
    content: Chiến lược phục vụ mô hình (Model Serving)
    keypoint_weight: 0.6
    description: Deploy mô hình (ví dụ XGBoost/LightGBM hoặc mô hình Deep Learning nhẹ) sử dụng Triton Inference Server hoặc ONNX Runtime để tối ưu hóa throughput; chia thành 2 phase: Rule-based/Light model nhanh (latency < 20ms) và Deep model nặng xử lý bất đồng bộ sau đó.

