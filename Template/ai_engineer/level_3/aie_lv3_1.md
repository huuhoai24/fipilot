# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 3) - Tập Đề MoE và LLM Alignment (1)

* **Role:** AI Engineer
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt cơ chế mã hóa vị trí RoPE (Rotary Position Embedding) và Absolute Position Embedding trong mô hình Transformer. Tại sao RoPE lại ưu việt hơn khi suy rộng cửa sổ ngữ cảnh (Context Window Extension)?
* **expected_key_points:**
  - id: KP1_1
    content: Nguyên lý toán học của RoPE vs Absolute
    keypoint_weight: 0.5
    description: Absolute Position Embedding cộng trực tiếp một vector vị trí cố định vào token embedding. RoPE (Rotary) áp dụng phép quay ma trận 2D trên các cặp phần tử của vector query/key dựa trên vị trí của chúng, giữ nguyên tích vô hướng phụ thuộc vào khoảng cách tương đối.
  - id: KP1_2
    content: Ưu việt khi mở rộng ngữ cảnh
    keypoint_weight: 0.5
    description: RoPE có tính suy rộng khoảng cách tương đối rất tốt. Có thể áp dụng các kỹ thuật như Linear Interpolation hoặc NTK-aware scaling trên góc quay để mở rộng cửa sổ ngữ cảnh lên gấp nhiều lần mà không cần train lại từ đầu.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh cơ chế Grouped-Query Attention (GQA) với Multi-Head Attention (MHA) và Multi-Query Attention (MQA) về mặt lý thuyết toán học và hiệu quả quản lý KV Cache.
* **expected_key_points:**
  - id: KP2_1
    content: Bản chất toán học và phân chia Heads
    keypoint_weight: 0.5
    description: MHA có số lượng Key-Value heads bằng Query heads. MQA chỉ dùng duy nhất 1 Key-Value head cho tất cả Query heads. GQA chia Query heads thành các nhóm (groups), mỗi nhóm dùng chung 1 Key-Value head.
  - id: KP2_2
    content: Hiệu quả quản lý KV Cache
    keypoint_weight: 0.5
    description: MQA tiết kiệm RAM nhất nhưng giảm độ chính xác. GQA giảm kích thước KV Cache lưu trên VRAM từ 4 đến 8 lần so với MHA, giúp tăng mạnh batch size và throughput suy luận mà vẫn giữ nguyên độ chính xác.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Phân tích sự khác biệt giữa các kỹ thuật lượng tử hóa mô hình LLM sau huấn luyện (Post-Training Quantization): GPTQ, AWQ, và GGUF. Khi nào nên áp dụng phương pháp nào?
* **expected_key_points:**
  - id: KP3_1
    content: Nguyên lý kỹ thuật GPTQ vs AWQ
    keypoint_weight: 0.6
    description: GPTQ lượng tử hóa trọng số dựa trên sai số dòng thứ hai của Taylor expansion (xử lý ma trận Hessian). AWQ quan sát phân phối activation để bảo vệ các trọng số quan trọng nhất (salient weights) không bị biến dạng khi lượng tử hóa.
  - id: KP3_2
    content: Đặc trưng GGUF và lựa chọn áp dụng
    keypoint_weight: 0.4
    description: GGUF tối ưu cho CPU/GPU offloading trên máy local. Áp dụng GPTQ cho batch size lớn/server chuyên dụng; AWQ giữ độ chính xác tốt nhất cho các mô hình nhỏ (như 7B/8B); GGUF cho môi trường local/edge.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích chi tiết kiến trúc Mixture of Experts (MoE) trong LLM. Cơ chế hoạt động của Gating Network (Router) là gì và làm thế nào để giải quyết bài toán mất cân bằng phân bổ chuyên gia (Expert Load Imbalance)?
* **expected_key_points:**
  - id: KP4_1
    content: Cấu trúc MoE và Router
    keypoint_weight: 0.5
    description: MoE thay lớp MLP bằng nhiều mạng MLP song song (Experts). Router tính trọng số xác suất để phân bổ mỗi token đầu vào cho Top-K experts hoạt động (active parameters), giúp tăng dung lượng mô hình mà giữ nguyên FLOPs tính toán.
  - id: KP4_2
    content: Giải quyết Expert Load Imbalance
    keypoint_weight: 0.5
    description: Thêm một hàm phạt mất cân bằng (Auxiliary Loss) vào loss function chính để phạt Router nếu nó dồn quá nhiều token vào một vài experts; hoặc sử dụng thuật toán Expert Capacity giới hạn số lượng token tối đa một expert được xử lý.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế hệ thống RAG (Retrieval-Augmented Generation) đáp ứng yêu cầu tra cứu đa ngôn ngữ (Cross-lingual) cho một tập đoàn đa quốc gia. Đề xuất giải pháp và các bước xử lý.
* **expected_key_points:**
  - id: KP5_1
    content: Xây dựng Multilingual Indexing Pipeline
    keypoint_weight: 0.5
    description: Sử dụng mô hình nhúng đa ngôn ngữ (Multilingual Embedding như Cohere Multilingual v3 hoặc mE5) để ánh xạ văn bản của các ngôn ngữ khác nhau vào cùng một không gian vector ngữ nghĩa.
  - id: KP5_2
    content: Kịch bản truy vấn và Translation-on-the-fly
    keypoint_weight: 0.5
    description: Khi nhận query bằng ngôn ngữ A -> truy vấn vector DB lấy tài liệu ngôn ngữ B -> dùng LLM dịch/tổng hợp tài liệu đó trực tiếp và trả về câu trả lời bằng ngôn ngữ A; sử dụng cross-encoder reranker đa ngôn ngữ để sắp xếp lại tài liệu.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích nguyên nhân xảy ra lỗi bùng nổ gradient (Gradient Explosion) khi huấn luyện các mô hình AI quy mô lớn bằng thư viện DeepSpeed và đề xuất 3 giải pháp kiểm soát hệ thống.
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên nhân bùng nổ gradient
    keypoint_weight: 0.5
    description: Do việc nhân liên tiếp các ma trận trọng số lớn, hoặc do lỗi tràn số (overflow) khi sử dụng định dạng FP16 có dải động (dynamic range) hẹp làm giá trị loss đột ngột tăng lên vô cực (NaN loss).
  - id: KP6_2
    content: Giải pháp kiểm soát hệ thống
    keypoint_weight: 0.5
    description: Sử dụng kỹ thuật FP16 loss scaling (tự động điều chỉnh tỷ lệ loss), áp dụng gradient clipping (cắt giới hạn chuẩn gradient), hoặc chuyển sang sử dụng định dạng BF16 có dải động rộng tương đương FP32.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh sự khác biệt trong tối ưu hóa I/O bộ nhớ của thuật toán FlashAttention-2 so với FlashAttention-1. Những cải tiến nào giúp phiên bản 2 chạy nhanh gấp đôi?
* **expected_key_points:**
  - id: KP7_1
    content: Tối ưu hóa phân bổ luồng (Thread-block Parallelism)
    keypoint_weight: 0.5
    description: FlashAttention-2 thay đổi cách phân chia công việc: thực hiện song song hóa trên cả chiều dài chuỗi của Query (Query sequence length), giúp tận dụng tối đa các SMs (Streaming Multiprocessors) của GPU.
  - id: KP7_2
    content: Giảm thiểu tính toán trung gian và tối ưu Tensor Cores
    keypoint_weight: 0.5
    description: Phiên bản 2 tinh giản các phép tính toán trung gian trong vòng lặp softmax, giảm số lần truy cập SRAM và đồng bộ hóa luồng; định dạng lại các phép tính nhân ma trận để khớp hoàn hảo với cấu trúc Tensor Cores của GPU.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Hãy thiết kế kiến trúc huấn luyện một mô hình LLM MoE quy mô 30 tỷ tham số (30B) từ đầu (from scratch) trên cụm 8 GPU A100 (80GB VRAM). Hãy trình bày cấu hình song song hóa và tối ưu hóa VRAM.
* **expected_key_points:**
  - id: KP8_1
    content: Chiến lược 3D Parallelism và Expert Parallelism
    keypoint_weight: 0.5
    description: Cấu hình Tensor Parallelism (TP=2), Pipeline Parallelism (PP=2), Data Parallelism kết hợp Expert Parallelism (EP=2) để phân tách mô hình MoE qua 8 GPU; các experts của MoE được sharding qua 2 GPU thông qua EP.
  - id: KP8_2
    content: Tối ưu hóa VRAM và truyền thông
    keypoint_weight: 0.5
    description: Sử dụng DeepSpeed ZeRO-2 cho các tham số không phải expert; kích hoạt Activation Checkpointing; tối ưu hóa băng thông NVLink cho phép toán All-to-All khi định tuyến token giữa các GPU chứa experts khác nhau.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trình bày giải pháp Alignment cho LLM sử dụng kỹ thuật KTO (Kahneman-Tversky Optimization) so với DPO (Direct Preference Optimization). Phân tích về hàm loss toán học và tính khả thi trong thực tế dự án.
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế toán học của KTO dựa trên Prospect Theory
    keypoint_weight: 0.6
    description: KTO không tối ưu hóa trên cặp dữ liệu so sánh ($y_w, y_l$) như DPO, mà tối ưu hóa trực tiếp trên các mẫu đơn lẻ được nhãn (thumbs-up/thumbs-down). Hàm loss áp dụng hàm giá trị phi tuyến của Kahneman-Tversky để mô hình hóa việc con người nhạy cảm với tổn thất hơn là lợi ích.
  - id: KP9_2
    content: Tính khả thi thực tế
    keypoint_weight: 0.4
    description: KTO dễ thu thập dữ liệu hơn nhiều trong thực tế (chỉ cần log tương tác của user thích/ghét) và hoạt động tốt hơn DPO trên các tập dữ liệu mất cân bằng nghiêm trọng.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống Chatbot Multi-Agent tự động giám sát, phát hiện, phân tích nguyên nhân và đưa ra giải pháp khắc phục sự cố (Auto-remediation) cho cụm Kubernetes production của doanh nghiệp.
* **expected_key_points:**
  - id: KP10_1
    content: Kiến trúc các Tác nhân chuyên biệt (Specialized Agents)
    keypoint_weight: 0.5
    description: Thiết kế: K8s Monitor Agent (quét logs/metrics), Root Cause Analyzer Agent (suy luận logic sử dụng đồ thị lỗi), Patch Generator Agent (tạo file YAML sửa đổi), và Supervisor Agent (Human-in-the-loop duyệt lệnh nhạy cảm).
  - id: KP10_2
    content: Cơ chế an toàn hệ thống (System Safety)
    keypoint_weight: 0.5
    description: Thiết lập môi trường Sandbox để chạy thử nghiệm các lệnh sửa lỗi trước khi áp dụng vào cluster chính; giới hạn quyền RBAC tối thiểu cho các agents; ghi log đầy đủ các hành động để audit.

