# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 5) - Tập Đề Global LLM Supercomputing và MoE TCO (1)

* **Role:** AI Engineer
* **Level:** Level 5
* **Experience:** Trên 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Phân tích và so sánh sự khác nhau về băng thông mạng, giao thức truyền thông và mô hình lập trình (Programming Model) khi huấn luyện LLM lớn giữa cụm GPU NVIDIA H100 (sử dụng InfiniBand NDR) và cụm Google TPU v5p (sử dụng ICI - Inter-Chassis Interconnect).
* **expected_key_points:**
  - id: KP1_1
    content: NVIDIA H100 vs Google TPU v5p Network
    keypoint_weight: 0.5
    description: NVIDIA H100 sử dụng mạng InfiniBand NDR (400Gbps/port) kết hợp công cụ GPUDirect RDMA. Google TPU v5p sử dụng mạng kết nối tùy chỉnh ICI (Inter-Chassis Interconnect) cung cấp băng thông cực lớn (>4.8Tbps song phương) dạng đồ thị vòng lập phương 3D.
  - id: KP1_2
    content: Mô hình lập trình và Thư viện đồng bộ
    keypoint_weight: 0.5
    description: NVIDIA tối ưu qua thư viện NCCL (PyTorch DDP/FSDP). Google TPU tối ưu hóa qua compiler XLA và JAX/TensorFlow (phép toán sharding trực quan qua SPMD), giúp tự động song song hóa dễ dàng hơn.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân tích sự đánh đổi (Trade-offs) giữa kiến trúc Dense LLM và Sparse MoE (Mixture of Experts) ở quy mô cực lớn (>500 tỷ tham số) từ góc độ chi phí vận hành (Total Cost of Ownership - TCO) và tài nguyên phần cứng phục vụ suy luận.
* **expected_key_points:**
  - id: KP2_1
    content: Chi phí lưu trữ VRAM và Số lượng Node phục vụ
    keypoint_weight: 0.5
    description: MoE có tổng tham số cực lớn nên yêu cầu lượng VRAM khổng lồ để lưu trữ trọng số mô hình gốc, dẫn đến việc bắt buộc phải deploy qua cụm nhiều GPU (đội chi phí hạ tầng). Dense model cùng năng lực kích hoạt có dung lượng nhỏ hơn, dễ deploy trên ít GPU hơn.
  - id: KP2_2
    content: Chi phí tính toán trên mỗi Token sinh ra (FLOPs/Token)
    keypoint_weight: 0.5
    description: MoE chỉ kích hoạt một nhóm nhỏ experts trên mỗi token, giúp giảm mạnh số lượng FLOPs tính toán và điện năng tiêu thụ trên mỗi request so với Dense model cùng tổng số tham số, tối ưu chi phí chạy thực tế.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Phân tích sự khác biệt về bản chất kỹ thuật giữa phương pháp lượng tử hóa sau huấn luyện 4-bit (như FP4/NF4) và kiến trúc mô hình 1-bit/1.58-bit (BitNet) về mặt hiệu năng trên custom hardware ASICs.
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
* **Câu hỏi:** Thiết kế cơ chế định tuyến tối ưu (Routing/Gating) cho kiến trúc MoE đa phân cấp (Hierarchical MoE) nhằm cân bằng tải giữa các nodes tính toán và giảm thiểu latency All-to-All.
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế của Hierarchical MoE
    keypoint_weight: 0.5
    description: Phân cấp định tuyến: Router cấp 1 định tuyến token sang node GPU phù hợp; Router cấp 2 định tuyến token sang expert tương ứng trong node đó, giảm thiểu giao tiếp liên node.
  - id: KP4_2
    content: Tối ưu hóa phép toán All-to-All và Cân bằng tải
    keypoint_weight: 0.5
    description: Thiết kế thuật toán định tuyến song hành (Parallel Routing) và tối ưu hóa băng thông NVLink; sử dụng hàm loss phạt mất cân bằng động để Router phân bổ đều tokens.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế hệ thống RAG quy mô toàn cầu cho tập doanh nghiệp đa quốc gia xử lý hàng tỷ tài liệu, hỗ trợ phân quyền truy cập động (Dynamic Role-based Access) ở cấp độ dòng (row-level security) và mã hóa dữ liệu.
* **expected_key_points:**
  - id: KP5_1
    content: Row-level Security (RLS) trên Vector DB
    keypoint_weight: 0.5
    description: Lưu trữ metadata quyền truy cập của từng tài liệu; khi người dùng tìm kiếm, thực hiện pre-filtering lọc đúng các tài liệu thuộc nhóm quyền của họ dựa trên danh tính người dùng.
  - id: KP5_2
    content: Bảo mật dữ liệu nhạy cảm và Mã hóa
    keypoint_weight: 0.5
    description: Áp dụng mã hóa Homomorphic Encryption hoặc thiết lập Proxy mã hóa trước khi đẩy query lên Vector DB đám mây; đảm bảo tuân thủ nghiêm ngặt chuẩn bảo mật GDPR/HIPAA.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích nguyên nhân sâu xa và thiết kế giải pháp xử lý lỗi mất ổn định toán học (Loss Spike) khi pre-train mô hình 175B+ từ đầu, bao gồm cả các kỹ thuật dynamic weight scaling và checkpoint rollback phân tán.
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên nhân toán học gây Loss Spike
    keypoint_weight: 0.4
    description: Do tích lũy lỗi số học khi mô hình quá sâu, lỗi tràn số khi dùng FP16, hoặc gặp phải các batch dữ liệu nhiễu cực đoan làm gradient bùng nổ.
  - id: KP6_2
    content: Quy trình tự động phục hồi
    keypoint_weight: 0.6
    description: Thiết lập giám sát loss tự động; khi phát hiện loss tăng đột biến (>3x trong 5 steps): dừng huấn luyện -> tự động rollback cụm về checkpoint trước đó 2 epochs -> bỏ qua batch dữ liệu lỗi -> giảm 50% learning rate hoặc thay đổi random seed để vượt qua điểm mất ổn định.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cách tối ưu hóa băng thông bộ nhớ của FlashAttention-3 và cách tận dụng phần cứng Tensor Memory Accelerator (TMA) của H100 kết hợp định dạng số FP8.
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
* **Câu hỏi:** Thiết kế hệ thống huấn luyện một mô hình MoE 500B từ đầu (from scratch) trên cụm 256x H100 kết nối song song qua mạng InfiniBand, tối ưu hóa sự phối hợp giữa TP, PP, DP, và EP (Expert Parallelism).
* **expected_key_points:**
  - id: KP8_1
    content: Chiến lược 3D Parallelism và Expert Parallelism
    keypoint_weight: 0.5
    description: Cấu hình Tensor Parallelism (TP=8) trong từng node để tận dụng tối đa NVLink; Pipeline Parallelism (PP=4) chia dọc qua các node; Data Parallelism kết hợp Expert Parallelism (EP=8) để phân tách các experts qua các GPU còn lại kết nối bằng InfiniBand.
  - id: KP8_2
    content: Tối ưu hóa truyền thông và VRAM
    keypoint_weight: 0.5
    description: Sử dụng DeepSpeed ZeRO-1 cho các tham số không phải expert; kích hoạt GPUDirect RDMA giảm thiểu nghẽn băng thông khi chạy phép toán All-to-All định tuyến token; áp dụng FP8 Mixed Precision.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Xây dựng giải pháp Alignment toàn diện cho LLM lớn kết hợp RLHF, DPO, và kỹ thuật căn chỉnh sở thích nhóm (Group Preference Alignment - như KTO) đáp ứng đa văn hóa và giảm thiểu hiện tượng Alignment Tax (sụt giảm năng lực cốt lõi).
* **expected_key_points:**
  - id: KP9_1
    content: Cân bằng giữa các mục tiêu Alignment khác nhau
    keypoint_weight: 0.5
    description: Thiết lập hàm loss đa nhiệm (multi-objective loss) kết hợp điểm số của con người và hàm phạt KL divergence với mô hình gốc để tránh mô hình bị lệch hướng ngữ nghĩa cốt lõi (Alignment Tax).
  - id: KP9_2
    content: Căn chỉnh sở thích nhóm đa văn hóa
    keypoint_weight: 0.5
    description: Sử dụng KTO (Kahneman-Tversky Optimization) huấn luyện trên các tập dữ liệu nhãn đơn lẻ (thích/không thích) thu thập từ nhiều nhóm văn hóa khác nhau, kết hợp cơ chế MoE để cá nhân hóa câu trả lời.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc Multi-Agent phục vụ vận hành tự động toàn bộ hạ tầng đám mây (Cloud Infrastructure AI Agent) có khả năng tự động phân tích logs lỗi, phát hiện lỗ hổng bảo mật, tự động viết patch cấu hình Terraform/K8s và thực thi an toàn.
* **expected_key_points:**
  - id: KP10_1
    content: Kiến trúc các Tác nhân chuyên biệt (Specialized Agents)
    keypoint_weight: 0.5
    description: Thiết kế: Cloud Monitor Agent (quét logs/metrics), Security Auditor Agent (suy luận lỗ hổng bảo mật), Terraform Patch Agent (tạo code sửa đổi), và Supervisor Agent (Human-in-the-loop duyệt lệnh nhạy cảm).
  - id: KP10_2
    content: Cơ chế an toàn hệ thống (System Safety)
    keypoint_weight: 0.5
    description: Thiết lập môi trường Sandbox để chạy thử nghiệm các lệnh sửa lỗi trước khi áp dụng vào cluster chính; giới hạn quyền RBAC tối thiểu cho các agents; ghi log đầy đủ các hành động để audit.

