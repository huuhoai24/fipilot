# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 4) - Tập Đề Enterprise Scaling và MoE Architecture (1)

* **Role:** AI Engineer
* **Level:** Level 4
* **Experience:** 6 - 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Phân tích và so sánh sự khác nhau về băng thông và độ trễ truyền thông (Network Overhead) giữa Megatron-LM Tensor Parallelism (TP) và DeepSpeed ZeRO-3 khi huấn luyện LLM lớn trên cụm nhiều node.
* **expected_key_points:**
  - id: KP1_1
    content: Tần suất giao tiếp và độ trễ của TP vs ZeRO-3
    keypoint_weight: 0.5
    description: Tensor Parallelism phân mảnh ma trận trong từng lớp attention, yêu cầu 2 phép toán All-Reduce ở mỗi layer (tần suất cực cao, cực kỳ nhạy cảm với latency của mạng). ZeRO-3 thu thập tham số ở cấp độ layer trước forward/backward, giao tiếp dạng khối lớn (All-Gather và Reduce-Scatter) nên ít nhạy cảm với latency hơn.
  - id: KP1_2
    content: Yêu cầu kết nối phần cứng
    keypoint_weight: 0.5
    description: TP bắt buộc phải chạy trên các GPU kết nối băng thông cực lớn (>300GB/s qua NVLink) trong cùng một node. ZeRO-3 có thể scale hiệu quả qua các node kết nối bằng mạng chậm hơn (như 100GbE) nếu cấu hình tối ưu hóa overlap truyền thông và tính toán.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao các mô hình ngôn ngữ lớn siêu lớn (như GPT-4) sử dụng kiến trúc Mixture of Experts (MoE) thay vì Dense model thông thường khi vận hành trong môi trường production?
* **expected_key_points:**
  - id: KP2_1
    content: Cơ chế Sparse Activation của MoE
    keypoint_weight: 0.5
    description: MoE phân tách mô hình thành nhiều chuyên gia (Experts) độc lập. Router chỉ kích hoạt một nhóm nhỏ experts (ví dụ Top-2) cho mỗi token đầu vào.
  - id: KP2_2
    content: Tối ưu hóa tài nguyên tính toán và suy luận
    keypoint_weight: 0.5
    description: Cho phép tăng mạnh dung lượng kiến thức và tham số của mô hình (sparse parameters) mà giữ nguyên số lượng phép toán FLOPs thực tế trên mỗi token, giúp giảm độ trễ sinh từ (time-to-first-token) và tăng throughput suy luận.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Phân tích sự khác biệt về bản chất kỹ thuật giữa phương pháp lượng tử hóa sau huấn luyện 4-bit (như FP4/NF4) và kiến trúc mô hình 1-bit/1.58-bit (BitNet).
* **expected_key_points:**
  - id: KP3_1
    content: Lượng tử hóa PTQ vs Huấn luyện từ đầu 1-bit
    keypoint_weight: 0.5
    description: FP4/NF4 là lượng tử hóa sau huấn luyện (PTQ) nén các tham số FP16 của mô hình đã train về 4-bit. BitNet huấn luyện mô hình từ đầu với các trọng số chỉ nhận giá trị trong tập {-1, 0, 1} (1.58-bit).
  - id: KP3_2
    content: Hiệu quả tính toán phần cứng
    keypoint_weight: 0.5
    description: FP4/NF4 vẫn yêu cầu các phép toán nhân ma trận số thực (floating-point multiply-accumulate). BitNet loại bỏ hoàn toàn phép nhân ma trận số thực, chuyển thành các phép cộng ma trận số nguyên (integer addition), giúp giảm tiêu thụ năng lượng lên tới hàng chục lần.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế cơ chế Router cân bằng tải động (Dynamic Routing) trong mạng MoE nhằm giải quyết triệt để bài toán sụt giảm hiệu năng do expert capacity limit (báo động tràn dung lượng chuyên gia).
* **expected_key_points:**
  - id: KP4_1
    content: Hiện tượng Expert Capacity Limit và sụt giảm hiệu năng
    keypoint_weight: 0.5
    description: Khi các token dồn quá nhiều vào một expert nổi tiếng, expert đó bị tràn dung lượng (capacity overflow), dẫn đến việc các token bị drop hoặc định tuyến sang expert phụ không tối ưu, làm giảm độ chính xác.
  - id: KP4_2
    content: Thiết kế Router động và Sinkhorn Algorithm
    keypoint_weight: 0.5
    description: Áp dụng thuật toán tối ưu hóa Sinkhorn để giải bài toán định tuyến như bài toán phân bổ tối ưu (optimal transport), cân bằng tải cứng cho các experts mà vẫn giữ độ tương quan ngữ nghĩa cao nhất.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế giải pháp RAG đa quốc gia có tính bảo mật phân quyền (Access Control List - ACL) xử lý hàng triệu tài liệu bảo mật nội bộ, sử dụng Vector DB phân tán.
* **expected_key_points:**
  - id: KP5_1
    content: Tích hợp ACL vào Vector Database
    keypoint_weight: 0.5
    description: Mỗi chunk tài liệu khi lưu vào Vector DB được gán kèm siêu dữ liệu (metadata) chứa danh sách các nhóm/vai trò người dùng được phép truy cập (ACL IDs).
  - id: KP5_2
    content: Truy vấn an toàn thời gian thực
    keypoint_weight: 0.5
    description: Khi nhận request, giải mã JWT token của user lấy vai trò -> thực hiện tìm kiếm vector kết hợp bộ lọc metadata (pre-filtering) để loại bỏ các tài liệu không được phép trước khi đưa qua LLM, đảm bảo không rò rỉ thông tin.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy phân tích nguyên nhân xảy ra lỗi bùng nổ mất ổn định huấn luyện (Loss Spike) khi pre-train mô hình LLM 70B+ từ đầu và thiết kế quy trình xử lý tự động phục hồi lỗi (Auto-recovery pipeline).
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên nhân Loss Spike
    keypoint_weight: 0.4
    description: Do tích lũy sai số dấu phẩy động khi mô hình quá sâu, lỗi tràn số khi dùng FP16, hoặc gặp phải các batch dữ liệu nhiễu cực đoan làm gradient bùng nổ.
  - id: KP6_2
    content: Quy trình tự động phục hồi
    keypoint_weight: 0.6
    description: Thiết lập giám sát loss tự động; khi phát hiện loss tăng đột biến (>3x trong 5 steps): dừng huấn luyện -> tự động rollback cụm về checkpoint trước đó 2 epochs -> bỏ qua batch dữ liệu lỗi -> giảm 50% learning rate hoặc thay đổi random seed để vượt qua điểm mất ổn định.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích sự khác biệt trong tối ưu hóa I/O bộ nhớ của thuật toán FlashAttention-3 so với các phiên bản trước khi chạy trên kiến trúc GPU NVIDIA Hopper (như H100).
* **expected_key_points:**
  - id: KP7_1
    content: Tận dụng Tensor Memory Accelerator (TMA)
    keypoint_weight: 0.5
    description: FlashAttention-3 sử dụng phần cứng TMA của H100 để tự động truyền dữ liệu giữa bộ nhớ toàn cục (HBM) và bộ nhớ chia sẻ (Shared Memory) không đồng bộ, giải phóng tài nguyên tính toán của nhân GPU.
  - id: KP7_2
    content: Phép tính GEMM không đồng bộ và Lượng tử hóa FP8
    keypoint_weight: 0.5
    description: Thực hiện song song hóa phép nhân ma trận và softmax không đồng bộ (Warp Group GEMM), tích hợp lượng tử hóa FP8 để tăng tốc độ tính toán chú ý gấp đôi so với FlashAttention-2.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc huấn luyện mô hình MoE quy mô 100 tỷ tham số (100B) từ đầu (from scratch) trên cụm 128 GPU H100 kết nối qua mạng InfiniBand. Hãy trình bày cấu hình song song hóa chi tiết.
* **expected_key_points:**
  - id: KP8_1
    content: Chiến lược 3D Parallelism và Expert Parallelism
    keypoint_weight: 0.5
    description: Cấu hình Tensor Parallelism (TP=8) trong từng node để tận dụng tối đa NVLink; Pipeline Parallelism (PP=4) chia dọc qua các node; Data Parallelism kết hợp Expert Parallelism (EP=4) để phân tách các experts qua các GPU còn lại kết nối bằng InfiniBand.
  - id: KP8_2
    content: Tối ưu hóa truyền thông và VRAM
    keypoint_weight: 0.5
    description: Sử dụng DeepSpeed ZeRO-1 cho các tham số không phải expert; kích hoạt GPUDirect RDMA giảm thiểu nghẽn băng thông khi chạy phép toán All-to-All định tuyến token; áp dụng FP8 Mixed Precision.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp tối ưu hóa bộ nhớ GPU khi chạy quy trình Alignment nâng cao cho LLM bằng RLHF (Reinforcement Learning from Human Feedback) sử dụng thuật toán PPO. Giải quyết bài toán cạn kiệt VRAM khi chạy đồng thời 4 mô hình.
* **expected_key_points:**
  - id: KP9_1
    content: Nguyên nhân cạn kiệt bộ nhớ trong PPO
    keypoint_weight: 0.4
    description: PPO yêu cầu chạy đồng thời 4 mô hình: Actor (trainable), Reference (frozen), Critic (trainable), và Reward (frozen), vượt quá dung lượng VRAM của các GPU thông thường.
  - id: KP9_2
    content: Thiết kế giải pháp tối ưu hóa bộ nhớ
    keypoint_weight: 0.6
    description: Áp dụng kỹ thuật chia sẻ tham số (Parameter Sharing) giữa Actor và Critic; offload mô hình Reference và Reward sang CPU hoặc bộ nhớ hệ thống; sử dụng lượng tử hóa LoRA/QLoRA cho Actor và Critic để giảm dung lượng gradients và optimizer states.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống tác nhân AI tự động hóa kiểm thử phần mềm (AI Software Engineer Agent) có khả năng tự động đọc log lỗi CI/CD, định vị file code lỗi trên repo lớn (>1M dòng code), viết code sửa lỗi, chạy unit test tự động và tạo Pull Request hoàn chỉnh.
* **expected_key_points:**
  - id: KP10_1
    content: Phân cấp Tác nhân và Quản lý mã nguồn
    keypoint_weight: 0.5
    description: Thiết kế kiến trúc Multi-Agent phân cấp: Planner Agent (lên kế hoạch), Repository Analyzer Agent (phân tích cấu trúc file dùng AST), Code Generator Agent (sửa code), và Validation Agent (chạy test).
  - id: KP10_2
    content: Cơ chế Phục hồi Lỗi tự động (Self-debugging Loop)
    keypoint_weight: 0.5
    description: Thiết lập Sandbox Docker cô lập hoàn toàn để chạy lệnh test; Validation Agent thu thập logs lỗi biên dịch/test fail nạp ngược lại cho Code Generator dưới dạng feedback để tự động sửa đổi cho đến khi 100% test pass mới tạo PR.

