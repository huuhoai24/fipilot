# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 5) - Tập Đề Distributed LLM Training và GPU Memory (12)

* **Role:** AI Engineer
* **Level:** Level 5
* **Experience:** Trên 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh cơ chế Tensor Parallelism (Megatron-LM) và Pipeline Parallelism (PipeDream) trong huấn luyện phân tán mô hình Transformer lớn.
* **expected_key_points:**
  - id: KP1_1
    content: Cơ chế Tensor Parallelism (TP)
    keypoint_weight: 0.5
    description: Chia nhỏ ma trận trọng số của từng lớp self-attention và MLP (phân mảnh dọc/ngang) qua các GPU trong cùng một node, yêu cầu giao tiếp All-Reduce liên tục.
  - id: KP1_2
    content: Cơ chế Pipeline Parallelism (PP)
    keypoint_weight: 0.5
    description: Chia mô hình theo các lớp dọc (ví dụ lớp 1-16 trên GPU 0, lớp 17-32 trên GPU 1). Dữ liệu truyền tuần tự qua các GPU, yêu cầu giao tiếp ít hơn nhưng có thời gian GPU nhàn rỗi (bubble).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích khái niệm Ring All-Reduce và tại sao nó lại tối ưu hóa băng thông giao tiếp mạng giữa các GPU so với cơ chế All-Reduce tập trung (Master-Slave).
* **expected_key_points:**
  - id: KP2_1
    content: Nguyên lý Ring All-Reduce
    keypoint_weight: 0.6
    description: Các GPU được sắp xếp thành một vòng tròn logic. Mỗi GPU chỉ truyền dữ liệu cho GPU tiếp theo và nhận dữ liệu từ GPU phía trước. Quá trình chia làm 2 giai đoạn: Scatter-Reduce và All-Gather.
  - id: KP2_2
    content: Tối ưu hóa băng thông mạng
    keypoint_weight: 0.4
    description: Tổng dung lượng dữ liệu truyền qua mỗi kết nối là độc lập với số lượng GPU $N$, tránh nghẽn cổ chai tại GPU master và tận dụng tối đa băng thông kết nối song song.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày lợi ích và cơ chế hoạt động của huấn luyện độ chính xác hỗn hợp (Mixed Precision Training) sử dụng BF16 so với FP16. Tại sao BF16 lại được khuyên dùng cho các mô hình lớn?
* **expected_key_points:**
  - id: KP3_1
    content: BF16 vs FP16 cấu trúc số học
    keypoint_weight: 0.5
    description: FP16 có 5 bits số mũ và 10 bits phần lẻ. BF16 có 8 bits số mũ (ngang FP32) và 7 bits phần lẻ, giúp biểu diễn dải giá trị rộng hơn nhưng độ chính xác thấp hơn một chút.
  - id: KP3_2
    content: Ưu thế của BF16 trong huấn luyện LLM
    keypoint_weight: 0.5
    description: Dải giá trị rộng của BF16 giúp tránh hoàn toàn lỗi tràn số (overflow) và dưới số (underflow) của gradient, loại bỏ nhu cầu sử dụng kỹ thuật phức tạp dynamic loss scaling của FP16.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế phân mảnh bộ nhớ của DeepSpeed ZeRO Stage 1, 2, và 3. ZeRO-Offload và ZeRO-Infinity cải tiến gì để tận dụng bộ nhớ CPU và NVMe?
* **expected_key_points:**
  - id: KP4_1
    content: Phân mảnh của các Stage ZeRO
    keypoint_weight: 0.5
    description: ZeRO-1 phân mảnh Optimizer States qua các GPU. ZeRO-2 phân mảnh thêm Gradients. ZeRO-3 phân mảnh toàn bộ Parameters của mô hình qua các GPU (chỉ thu thập lại khi cần thiết trong forward/backward pass).
  - id: KP4_2
    content: ZeRO-Offload và ZeRO-Infinity
    keypoint_weight: 0.5
    description: ZeRO-Offload chuyển optimizer states và tính toán cập nhật trọng số sang bộ nhớ và CPU hệ thống. ZeRO-Infinity hỗ trợ offload sang cả ổ cứng NVMe, cho phép train mô hình quy mô 100B+ trên GPU đơn lẻ.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích hiện tượng 'Pipeline Bubble' trong Pipeline Parallelism. Kỹ thuật lịch trình Interleaved 1F1B giúp giảm bubble time như thế nào?
* **expected_key_points:**
  - id: KP5_1
    content: Bản chất của Pipeline Bubble
    keypoint_weight: 0.5
    description: Là thời gian nhàn rỗi của các GPU ở đầu và cuối pipeline khi chờ đợi micro-batches từ các GPU khác truyền sang trong forward/backward pass.
  - id: KP5_2
    content: Cơ chế Interleaved 1F1B
    keypoint_weight: 0.5
    description: Mỗi GPU được phân bổ nhiều phân đoạn lớp không liên tiếp (ví dụ GPU 0 giữ lớp 1-4 và 9-12). Chạy xen kẽ 1 bước forward và 1 bước backward của các micro-batches khác nhau để giữ các GPU luôn bận rộn.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế giải pháp phân mảnh dữ liệu (Data Sharding) và đồng bộ hóa gradients trong huấn luyện phân tán quy mô hàng ngàn nodes sử dụng PyTorch Distributed Data Parallel (DDP).
* **expected_key_points:**
  - id: KP6_1
    content: Phân mảnh dữ liệu qua DistributedSampler
    keypoint_weight: 0.5
    description: Sử dụng DistributedSampler đảm bảo mỗi GPU worker chỉ đọc các phân mảnh dữ liệu (chunks) không trùng lặp từ tập train tổng.
  - id: KP6_2
    content: Đồng bộ gradients qua All-Reduce bucketed
    keypoint_weight: 0.5
    description: Trong backward pass, DDP tự động gom các gradients của các lớp thành các nhóm (buckets) và chạy All-Reduce song song với quá trình tính gradient của lớp tiếp theo để giảm độ trễ truyền thông.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh hiệu năng truyền thông và băng thông giữa công nghệ kết nối NVLink/NVSwitch và khe cắm PCIe Gen4/Gen5 khi chạy Tensor Parallelism qua cụm máy chủ GPU.
* **expected_key_points:**
  - id: KP7_1
    content: Băng thông kết nối NVLink vs PCIe
    keypoint_weight: 0.6
    description: PCIe Gen4 đạt tối đa 32GB/s, Gen5 đạt 64GB/s. NVLink thế hệ mới (trên H100) đạt băng thông lên tới 900GB/s song phương giữa các GPU.
  - id: KP7_2
    content: Ảnh hưởng đến Tensor Parallelism
    keypoint_weight: 0.4
    description: Tensor Parallelism yêu cầu giao tiếp All-Reduce ở mỗi lớp attention. Nếu chạy qua PCIe sẽ bị nghẽn băng thông nghiêm trọng làm GPU nhàn rỗi; bắt buộc phải chạy TP trên các GPU được kết nối trực tiếp qua NVLink/NVSwitch.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp huấn luyện một mô hình ngôn ngữ 100B từ đầu (from scratch) trên cụm 64 GPU H100 kết nối qua mạng InfiniBand. Hãy trình bày cấu hình song song hóa chi tiết.
* **expected_key_points:**
  - id: KP8_1
    content: Thiết lập cấu hình 3D Parallelism
    keypoint_weight: 0.5
    description: Cấu hình: Tensor Parallelism (TP=8) trên 8 GPU trong cùng một node (dùng NVLink); Pipeline Parallelism (PP=4) chia dọc mô hình qua 4 nodes; Data Parallelism kết hợp ZeRO-1 (DP=2) phân mảnh dữ liệu qua cụm còn lại kết nối bằng InfiniBand.
  - id: KP8_2
    content: Tối ưu hóa thời gian tính toán và truyền thông
    keypoint_weight: 0.5
    description: Kích hoạt FlashAttention-2, Activation Checkpointing, và sử dụng BF16 Mixed Precision; cấu hình GPU-Direct RDMA để InfiniBand truyền trực tiếp dữ liệu giữa VRAM của các GPU khác node không đi qua RAM CPU.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích nguyên nhân và thiết kế hệ thống tự động phục hồi lỗi (Fault Tolerance & Checkpointing) khi một node GPU trong cụm bị sập (hardware failure) giữa quá trình huấn luyện LLM lớn kéo dài nhiều tuần.
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế lưu trữ Checkpoint phân tán (Elastic Checkpointing)
    keypoint_weight: 0.5
    description: Sử dụng thư viện TorchElastic hoặc DeepSpeed checkpointing để tự động lưu trọng số mô hình định kỳ lên hệ thống lưu trữ phân tán dùng chung (như Ceph/S3).
  - id: KP9_2
    content: Tự động phát hiện lỗi và khởi động lại cụm (Auto-recovery)
    keypoint_weight: 0.5
    description: Thiết lập Kubernetes / Slurm controller theo dõi trạng thái nodes. Khi phát hiện 1 GPU lỗi -> tự động cô lập node đó -> cấp phát node dự phòng -> reload mô hình từ checkpoint gần nhất và tiếp tục huấn luyện mà không cần sự can thiệp thủ công.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống tối ưu hóa phân bổ tài nguyên động (Dynamic Resource Allocation) cho cụm máy chủ huấn luyện và phục vụ mô hình AI sử dụng Kubernetes kết hợp Slurm.
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế quản lý GPU của Kubernetes và Slurm
    keypoint_weight: 0.5
    description: Sử dụng Slurm để quản lý hàng đợi và cấp phát GPU độc quyền cho các tác vụ huấn luyện LLM dài hạn. Sử dụng Kubernetes để quản lý các microservices phục vụ suy luận mô hình (serving).
  - id: KP10_2
    content: Tối ưu hóa động (Dynamic GPU Sharing)
    keypoint_weight: 0.5
    description: Thiết lập hệ thống auto-scaler: khi hàng đợi huấn luyện trống, Kubernetes tự động thu hồi tài nguyên GPU nhàn rỗi để phân bổ cho các tác vụ phục vụ suy luận (serving) hoặc lượng tử hóa mô hình.

