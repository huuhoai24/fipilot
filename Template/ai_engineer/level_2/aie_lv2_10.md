# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 2) - Tập Đề Model Compression và vLLM Serving (10)

* **Role:** AI Engineer
* **Level:** Level 2
* **Experience:** 1 - 3  năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày mục đích chính của việc Nén mô hình (Model Compression). Hãy liệt kê 3 phương pháp nén mô hình phổ biến nhất hiện nay.
* **expected_key_points:**
  - id: KP1_1
    content: Mục đích nén mô hình
    keypoint_weight: 0.5
    description: Giảm kích thước file mô hình, tiết kiệm bộ nhớ RAM/VRAM, tăng tốc độ suy luận (inference speed) và giảm điện năng tiêu thụ để phù hợp deploy lên thiết bị Edge hoặc server giới hạn tài nguyên.
  - id: KP1_2
    content: 3 phương pháp phổ biến
    keypoint_weight: 0.5
    description: Nêu được: Lượng tử hóa (Quantization), Cắt tỉa (Pruning), và Chuyển giao tri thức (Knowledge Distillation) hoặc Kiến trúc mạng gọn nhẹ (Compact Network Design).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt vai trò của CPU và GPU trong quy trình huấn luyện (Training) và suy luận (Inference) của các mô hình học sâu.
* **expected_key_points:**
  - id: KP2_1
    content: Đặc trưng của CPU
    keypoint_weight: 0.5
    description: CPU có ít nhân xử lý mạnh mẽ, tối ưu cho tính toán tuần tự, xử lý logic phức tạp, điều phối dữ liệu và chuẩn bị dữ liệu (Data Loading).
  - id: KP2_2
    content: Đặc trưng của GPU
    keypoint_weight: 0.5
    description: GPU có hàng ngàn nhân xử lý song song, tối ưu cho việc tính toán ma trận và các phép toán số học song song quy mô lớn đặc trưng của Deep Learning.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Khái niệm Pipeline trong Machine Learning là gì? Tại sao việc xây dựng một pipeline tự động lại quan trọng đối với các dự án AI thực tế?
* **expected_key_points:**
  - id: KP3_1
    content: Khái niệm ML Pipeline
    keypoint_weight: 0.5
    description: Là một chuỗi các bước xử lý dữ liệu và huấn luyện mô hình được liên kết tuần tự: Data Collection -> Data Prep -> Feature Engineering -> Model Training -> Evaluation -> Deployment.
  - id: KP3_2
    content: Tầm quan trọng của tự động hóa
    keypoint_weight: 0.5
    description: Đảm bảo tính nhất quán giữa môi trường huấn luyện và production (tránh training-serving skew), giúp dễ dàng huấn luyện lại (retrain) mô hình khi có dữ liệu mới, và tăng tính tái lập (reproducibility) của dự án.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích kỹ thuật Cắt tỉa mạng nơ-ron (Pruning). Phân biệt sự khác nhau giữa Structured Pruning (Cắt tỉa có cấu trúc) và Unstructured Pruning (Cắt tỉa không cấu trúc).
* **expected_key_points:**
  - id: KP4_1
    content: Nguyên lý Pruning
    keypoint_weight: 0.4
    description: Loại bỏ các trọng số (weights) hoặc kết nối ít quan trọng (gần bằng 0) ra khỏi mạng nơ-ron để làm mô hình nhẹ hơn mà ít làm suy giảm độ chính xác.
  - id: KP4_2
    content: Structured vs Unstructured Pruning
    keypoint_weight: 0.6
    description: Unstructured Pruning cắt tỉa các trọng số đơn lẻ ngẫu nhiên, tạo ra ma trận thưa (sparse matrix). Nó tiết kiệm dung lượng đĩa nhưng khó tăng tốc độ trên phần cứng GPU tiêu chuẩn. Structured Pruning cắt tỉa toàn bộ các kênh đặc trưng (channels), bộ lọc (filters) hoặc các lớp (layers), tạo ra ma trận nhỏ hơn có cấu trúc, giúp tăng tốc độ suy luận trực tiếp trên phần cứng thông thường.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế hoạt động và cấu trúc của Variational Autoencoder (VAE) trong bài toán sinh dữ liệu.
* **expected_key_points:**
  - id: KP5_1
    content: Mã hóa sang Phân phối xác suất (Latent Distribution)
    keypoint_weight: 0.6
    description: Thay vì ánh xạ ảnh đầu vào trực tiếp sang một vector ẩn cố định như Autoencoder thông thường, VAE mã hóa đầu vào thành các tham số của một phân phối xác suất ẩn (trung bình $\mu$ và phương sai $\sigma$).
  - id: KP5_2
    content: Cơ chế Reparameterization Trick và Loss Function
    keypoint_weight: 0.4
    description: Sử dụng Reparameterization trick ($z = \mu + \sigma \cdot \epsilon$ với $\epsilon \sim \mathcal{N}(0, I)$) để cho phép lan truyền ngược qua bước lấy mẫu ngẫu nhiên. Hàm loss gồm Reconstruction Loss (sai số tái tạo) và KL Divergence Loss (ràng buộc phân phối ẩn gần với phân phối chuẩn).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy so sánh sự khác nhau giữa REST API và gRPC khi thiết kế cổng API phục vụ suy luận mô hình (Model Inference Service). Trong trường hợp nào bạn sẽ ưu tiên dùng gRPC?
* **expected_key_points:**
  - id: KP6_1
    content: So sánh REST API và gRPC
    keypoint_weight: 0.6
    description: REST API sử dụng giao thức HTTP/1.1 truyền dữ liệu dạng text (JSON/XML), dễ tích hợp, thân thiện với web client. gRPC sử dụng HTTP/2 truyền dữ liệu nhị phân (Protocol Buffers), hỗ trợ bidirectional streaming và nén tiêu đề (header compression).
  - id: KP6_2
    content: Trường hợp ưu tiên dùng gRPC
    keypoint_weight: 0.4
    description: Ưu tiên gRPC khi cần độ trễ cực thấp (low latency), throughput cao, giao tiếp giữa các microservices nội bộ (inter-service communication), hoặc khi truyền luồng dữ liệu liên tục (streaming dữ liệu âm thanh/video để chạy AI).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày các phương pháp tối ưu hóa tốc độ nạp dữ liệu và huấn luyện mô hình bằng PyTorch (Mixed Precision Training, Pin Memory, và DataLoader worker configuration).
* **expected_key_points:**
  - id: KP7_1
    content: Mixed Precision Training (AMP)
    keypoint_weight: 0.5
    description: Sử dụng cả kiểu dữ liệu FP16 và FP32 trong huấn luyện. Phép toán forward chạy trên FP16 để tăng tốc độ tính toán của Tensor Cores, trong khi giữ một bản sao FP32 để cập nhật trọng số chính xác nhằm tránh mất mát gradient.
  - id: KP7_2
    content: Tối ưu nạp dữ liệu (Pin Memory và Workers)
    keypoint_weight: 0.5
    description: Cấu hình `num_workers > 0` trong DataLoader để nạp dữ liệu đa luồng (multi-processing). Thiết lập `pin_memory=True` giúp dữ liệu được nạp vào vùng nhớ RAM khóa trang (page-locked memory), tăng tốc độ truyền tải dữ liệu từ RAM sang VRAM của GPU.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Xây dựng giải pháp deploy một mô hình LLM lớn (ví dụ Llama-3-70B) chạy suy luận phục vụ hàng ngàn người dùng đồng thời, đảm bảo tối ưu hóa VRAM và tốc độ sinh token bằng vLLM.
* **expected_key_points:**
  - id: KP8_1
    content: Cơ chế PagedAttention của vLLM
    keypoint_weight: 0.6
    description: Giải thích cơ chế PagedAttention quản lý bộ nhớ KV Cache tương tự như bộ nhớ ảo (virtual memory) của hệ điều hành. Phân mảnh KV Cache thành các trang (pages) vật lý không cần liên tục trên VRAM, loại bỏ 96% sự lãng phí bộ nhớ và cho phép tăng batch size lớn hơn nhiều lần.
  - id: KP8_2
    content: Thiết lập Tensor Parallelism và Continuous Batching
    keypoint_weight: 0.4
    description: Cấu hình phân tách mô hình Llama-3-70B chạy song song trên nhiều GPU (ví dụ 4x GPU A100 qua Tensor Parallelism); kích hoạt continuous batching để xử lý đồng thời các request có độ dài khác nhau một cách linh hoạt.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống chuẩn hóa địa chỉ viết tay/phi cấu trúc (Address Standardization) thành cấu trúc chuẩn: Số nhà, Tên đường, Phường/Xã, Quận/Huyện, Tỉnh/Thành phố sử dụng Sequence-to-Sequence hoặc LLM fine-tune.
* **expected_key_points:**
  - id: KP9_1
    content: Pipeline xử lý dữ liệu và cấu trúc hóa
    keypoint_weight: 0.5
    description: Tiền xử lý văn bản (loại bỏ ký tự đặc biệt, chuẩn hóa chữ viết tắt) -> Dùng mô hình Sequence-to-Sequence (T5/BART) hoặc fine-tune LLM nhỏ (như Llama-3-8B/Qwen-2-7B) bằng kỹ thuật LoRA để chuyển đổi văn bản địa chỉ tự do thành JSON chuẩn.
  - id: KP9_2
    content: So khớp từ điển địa lý (Elasticsearch/Geocoding matching)
    keypoint_weight: 0.5
    description: Sử dụng Elasticsearch lập chỉ mục (index) từ điển hành chính quốc gia đầy đủ; thực hiện so khớp mờ (fuzzy matching) các trường địa chỉ trích xuất được để chuẩn hóa các lỗi chính tả viết tay, đảm bảo độ chính xác tuyệt đối.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống Học liên hợp (Federated Learning) để huấn luyện mô hình dự đoán từ tiếp theo trên bàn phím điện thoại di động mà không cần thu thập dữ liệu cá nhân của người dùng về máy chủ.
* **expected_key_points:**
  - id: KP10_1
    content: Quy trình huấn luyện phân tán cục bộ (Local Training)
    keypoint_weight: 0.5
    description: Mô hình được tải xuống điện thoại của người dùng; quá trình huấn luyện diễn ra cục bộ trên thiết bị bằng chính lịch sử gõ phím của người dùng khi cắm sạc pin và kết nối Wifi.
  - id: KP10_2
    content: Cơ chế gộp trọng số (Aggregation) và bảo mật
    keypoint_weight: 0.5
    description: Thiết bị chỉ gửi cập nhật trọng số (gradients/weights) về server trung tâm, không gửi dữ liệu thô. Server sử dụng thuật toán Federated Averaging (FedAvg) để gộp các trọng số; áp dụng bảo mật bằng cơ chế Secure Aggregation và Differential Privacy để tránh việc tái tạo ngược dữ liệu từ trọng số.

