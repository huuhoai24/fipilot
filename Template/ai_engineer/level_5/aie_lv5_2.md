# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 5) - Tập Đề Speculative Decoding và Triton Serving (2)

* **Role:** AI Engineer
* **Level:** Level 5
* **Experience:** Trên 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích khái niệm Speculative Decoding trong suy luận LLM. Tại sao nó lại giúp tăng tốc độ sinh token mà không làm thay đổi phân phối xác suất đầu ra?
* **expected_key_points:**
  - id: KP1_1
    content: Cơ chế Draft Model và Target Model
    keypoint_weight: 0.5
    description: Sử dụng một mô hình ngôn ngữ nhỏ, nhanh (Draft Model) sinh trước một chuỗi gồm $K$ tokens gợi ý. Sau đó gửi chuỗi này qua mô hình ngôn ngữ lớn (Target Model) chạy song song một bước để kiểm tra độ tin cậy.
  - id: KP1_2
    content: Cơ chế chấp nhận/loại bỏ (Acceptance Criterion)
    keypoint_weight: 0.5
    description: Target model kiểm tra phân phối xác suất của các tokens gợi ý; chấp nhận các tokens đạt tiêu chuẩn toán học, loại bỏ các token sai lệch và sinh lại từ vị trí đó. Đảm bảo kết quả sinh ra giống hệt Target model chạy độc lập.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa hai kỹ thuật lượng tử hóa sau huấn luyện: AWQ (Activation-aware Weight Quantization) và GPTQ.
* **expected_key_points:**
  - id: KP2_1
    content: Nguyên lý kỹ thuật GPTQ vs AWQ
    keypoint_weight: 0.5
    description: GPTQ dựa trên thông tin đạo hàm bậc hai (ma trận Hessian) tối ưu hóa trọng số. AWQ quan sát phân phối activation thực tế để bảo vệ các trọng số quan trọng nhất không bị méo dạng.
  - id: KP2_2
    content: Lựa chọn áp dụng thực tế
    keypoint_weight: 0.5
    description: AWQ giữ độ chính xác cực tốt cho mô hình nhỏ (7B/8B/13B); GPTQ tốt hơn cho các mô hình lớn khi chạy trên cụm GPU phục vụ đa người dùng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Cấu hình Dynamic Batching trong Triton Inference Server hoạt động thế nào? Hãy nêu 2 tham số quan trọng nhất cần tối ưu hóa.
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế Dynamic Batching của Triton
    keypoint_weight: 0.5
    description: Triton tự động gộp các request suy luận đơn lẻ của người dùng đến trong cửa sổ thời gian mili-giây thành một lô (batch) lớn để chạy trên GPU, tối ưu hóa song song phần cứng.
  - id: KP3_2
    content: 2 tham số tối ưu hóa
    keypoint_weight: 0.5
    description: Nêu đúng: max_queue_delay_microseconds (thời gian tối đa chờ gom lô) và max_batch_size (kích thước lô tối đa cho phép).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích kỹ thuật lượng tử hóa FP8 (định dạng E4M3 và E5M2) được hỗ trợ trên kiến trúc GPU NVIDIA Hopper (như H100). So sánh ưu thế và dải biểu diễn của hai định dạng này.
* **expected_key_points:**
  - id: KP4_1
    content: Đặc trưng định dạng E4M3 vs E5M2
    keypoint_weight: 0.6
    description: E4M3 có 4 bits số mũ (exponent), 3 bits phần lẻ (mantissa); dải giá trị hẹp hơn nhưng độ chính xác cao hơn, phù hợp cho forward pass (weights & activations). E5M2 có 5 bits số mũ, 2 bits phần lẻ; dải giá trị rộng hơn (tương tự FP16) nhưng độ chính xác thấp hơn, phù hợp cho gradients và backward pass.
  - id: KP4_2
    content: Ưu thế trên GPU H100
    keypoint_weight: 0.4
    description: Hỗ trợ trực tiếp bởi nhân Tensor Cores mới trên H100, tăng tốc độ tính toán ma trận gấp đôi so với FP16 mà không bị tràn số.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh cơ chế quản lý KV Cache của vLLM PagedAttention và TensorRT-LLM. Các cơ chế này giải quyết vấn đề lãng phí VRAM ra sao?
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế PagedAttention của vLLM
    keypoint_weight: 0.5
    description: Phân mảnh KV Cache thành các trang vật lý không liên tiếp tương tự như bộ nhớ ảo, giúp loại bỏ 96% sự lãng phí VRAM và cho phép chia sẻ bộ nhớ khi sinh đa luồng.
  - id: KP5_2
    content: KV Cache của TensorRT-LLM và In-flight Batching
    keypoint_weight: 0.5
    description: TensorRT-LLM sử dụng cơ chế cấp phát động bộ nhớ tương tự, tích hợp sâu vào compiler của TensorRT và hỗ trợ in-flight batching (thêm request mới ngay khi có token trống) giúp giảm latency hơn nữa.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế giải pháp Prompt Cache (như SGLang hay Prompt Cache) để giảm thiểu chi phí tính toán và độ trễ suy luận LLM đối với các câu hỏi có chung phần System Prompt dài.
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế lưu trữ KV Cache của tiền tố (Prefix Caching)
    keypoint_weight: 0.6
    description: Nhận diện phần tiền tố (System Prompt/tài liệu RAG cố định) chung -> chạy forward 1 lần để tính toán KV Cache -> lưu cache này vào RAM/VRAM sử dụng hàm băm (hash).
  - id: KP6_2
    content: So khớp và tái sử dụng
    keypoint_weight: 0.4
    description: Khi nhận request mới có cùng tiền tố, bỏ qua bước tính toán attention cho phần này, chỉ cần nạp trực tiếp KV Cache đã lưu và bắt đầu sinh chữ cho phần query mới.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy so sánh ưu nhược điểm của REST API (JSON qua HTTP/1.1) và gRPC (Protocol Buffers qua HTTP/2) khi thiết kế cổng API phục vụ suy luận mô hình (Model Serving) tải cao.
* **expected_key_points:**
  - id: KP7_1
    content: So sánh định dạng dữ liệu và giao thức
    keypoint_weight: 0.6
    description: REST dùng JSON dạng text, dễ đọc nhưng cồng kềnh. gRPC dùng Protobuf dạng nhị phân nén nhỏ gọn. HTTP/2 của gRPC hỗ trợ multiplexing (truyền nhiều request song song trên 1 kết nối) và bidirectional streaming.
  - id: KP7_2
    content: Lựa chọn cho Model Serving
    keypoint_weight: 0.4
    description: Chọn gRPC khi cần độ trễ cực thấp, giao tiếp microservices nội bộ hoặc khi streaming dữ liệu (audio/video). Chọn REST khi cần tích hợp nhanh với Web frontend.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống phục vụ suy luận LLM lớn (Llama-3-70B) chạy trên cụm server phục vụ hàng triệu người dùng đồng thời, đảm bảo tối ưu hóa VRAM và tốc độ sinh token bằng vLLM.
* **expected_key_points:**
  - id: KP8_1
    content: Cấu hình Tensor Parallelism và Continuous Batching
    keypoint_weight: 0.5
    description: Cấu hình phân tách mô hình Llama-3-70B chạy song song trên nhiều GPU (ví dụ 4x GPU A100 qua Tensor Parallelism); kích hoạt continuous batching để xử lý đồng thời các request có độ dài khác nhau một cách linh hoạt.
  - id: KP8_2
    content: Cơ chế PagedAttention của vLLM
    keypoint_weight: 0.5
    description: Giải thích cơ chế PagedAttention quản lý bộ nhớ KV Cache tương tự như bộ nhớ ảo (virtual memory) của hệ điều hành. Phân mảnh KV Cache thành các trang (pages) vật lý không cần liên tục trên VRAM, loại bỏ 96% sự lãng phí bộ nhớ và cho phép tăng batch size lớn hơn nhiều lần.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp lượng tử hóa mô hình end-to-end cho mô hình Vision-Language (VLM) chạy trên thiết bị edge của xe tự lái, đảm bảo thời gian xử lý ảnh < 30ms.
* **expected_key_points:**
  - id: KP9_1
    content: Lượng tử hóa đa phương thức (VLM Quantization)
    keypoint_weight: 0.6
    description: Áp dụng lượng tử hóa INT8/INT4 AWQ cho phần LLM (decoder) để giảm kích thước và tiết kiệm VRAM; sử dụng FP16/INT8 lượng tử hóa có hiệu chuẩn (calibrated quantization) cho phần Image Encoder (CNN/ViT) đảm bảo không suy giảm độ chính xác nhận diện vật cản.
  - id: KP9_2
    content: Tối ưu hóa chạy trên NPU Edge và Pipeline
    keypoint_weight: 0.4
    description: Chuyển đổi toàn bộ mô hình sang định dạng ONNX/TensorRT; thiết lập pipeline song song hóa: Image Encoder xử lý frame tiếp theo trong lúc LLM đang giải mã frame hiện tại.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống tự động hóa load testing và profiling hiệu năng cho Triton Inference Server để tìm ra điểm cân bằng tối ưu giữa Latency (độ trễ) và Throughput (băng thông).
* **expected_key_points:**
  - id: KP10_1
    content: Sử dụng Triton Model Analyzer và Triton Performance Analyzer
    keypoint_weight: 0.5
    description: Viết script chạy Triton Performance Analyzer giả lập các kịch bản tải thực tế; sử dụng Model Analyzer tự động quét qua các cấu hình khác nhau của dynamic batching và số lượng instance.
  - id: KP10_2
    content: Xác định điểm tối ưu và Cảnh báo
    keypoint_weight: 0.5
    description: Vẽ biểu đồ Pareto Frontier thể hiện mối tương quan giữa latency và throughput; thiết lập cấu hình tự động chọn điểm tối ưu đáp ứng SLA (ví dụ: latency p99 < 50ms) để tự động sinh file config.pbtxt trước khi deploy.

