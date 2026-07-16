# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 3) - Tập Đề LLM Agents và FlashAttention-2 (2)

* **Role:** AI Engineer
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt cơ chế hoạt động của kỹ thuật FlashAttention-2 so với Standard Attention. Tại sao FlashAttention-2 lại tối ưu được băng thông phần cứng?
* **expected_key_points:**
  - id: KP1_1
    content: Hạn chế Standard Attention và Tiling của FlashAttention
    keypoint_weight: 0.5
    description: Standard Attention ghi nhớ ma trận trung bình $N \times N$ ra bộ nhớ HBM chậm của GPU. FlashAttention chia nhỏ dữ liệu thành các khối nhỏ (tiles) nạp vào SRAM tốc độ cực nhanh để tính softmax từng phần (online softmax).
  - id: KP1_2
    content: Cải tiến của FlashAttention-2
    keypoint_weight: 0.5
    description: FlashAttention-2 giảm số lượng phép tính nhân ma trận không cần thiết, song song hóa trên chiều dài chuỗi của Query, giúp tận dụng tối đa các Tensor Cores của GPU.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy trình bày cơ chế hoạt động của mô hình Mixture of Experts (MoE). Làm thế nào hệ thống phân phối (Router) quyết định định tuyến các token?
* **expected_key_points:**
  - id: KP2_1
    content: Bản chất kiến trúc MoE
    keypoint_weight: 0.5
    description: Thay vì dùng một mạng FFN lớn cố định cho mọi token, MoE chứa nhiều mạng FFN song song (Experts). Chỉ kích hoạt một nhóm nhỏ experts cho mỗi token đầu vào.
  - id: KP2_2
    content: Định tuyến của Router
    keypoint_weight: 0.5
    description: Gating Network (Router) nhận vector biểu diễn của token, tính toán softmax trên tất cả experts để chọn ra top-k experts có điểm số cao nhất để xử lý token đó.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Kỹ thuật lượng tử hóa mô hình (Model Quantization) AWQ (Activation-aware Weight Quantization) khác biệt như thế nào so với GPTQ?
* **expected_key_points:**
  - id: KP3_1
    content: Nguyên lý lượng tử hóa AWQ vs GPTQ
    keypoint_weight: 0.6
    description: GPTQ dựa trên thông tin đạo hàm bậc hai (Hessian matrix) để tối ưu hóa trọng số sau khi lượng tử hóa. AWQ tìm kiếm các kênh trọng số quan trọng nhất bằng cách quan sát phân phối activation thực tế, sau đó nhân tỷ lệ các kênh này lên để giảm thiểu sai số lượng tử hóa mà không cần train lại.
  - id: KP3_2
    content: Ưu điểm của AWQ
    keypoint_weight: 0.4
    description: AWQ giữ độ chính xác cực tốt cho các mô hình nhỏ (7B/8B/13B) và hoạt động tốt hơn GPTQ khi mô hình chạy suy luận trên các dải dữ liệu lệch nhiều so với tập calibration.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế giải pháp RAG nâng cao hỗ trợ truy xuất và trả lời câu hỏi dựa trên các tài liệu PDF chứa nhiều cấu trúc bảng biểu phức tạp chồng chéo (Complex Tables).
* **expected_key_points:**
  - id: KP4_1
    content: Trích xuất và định dạng bảng biểu
    keypoint_weight: 0.5
    description: Sử dụng mô hình Layout Analysis (LayoutLM/Table Transformer) để phát hiện và chuyển đổi bảng biểu thành Markdown hoặc HTML để giữ nguyên cấu trúc hàng cột ngữ nghĩa.
  - id: KP4_2
    content: Chiến lược Chunking và Code Interpreter
    keypoint_weight: 0.5
    description: Tạo summary cho bảng biểu để nhúng vector (Parent-Child chunking). Khi LLM nhận câu hỏi tính toán trên bảng, thay vì để LLM tự tính nhẩm (dễ sai), ta tích hợp Code Interpreter để LLM tự viết code Python tính toán trên bảng dữ liệu đó.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách bạn xử lý hiện tượng 'Catastrophic Forgetting' (Quên thảm họa) khi thực hiện tinh chỉnh (Fine-tuning) mô hình ngôn ngữ lớn trên một tập dữ liệu chuyên ngành.
* **expected_key_points:**
  - id: KP5_1
    content: Nguyên nhân Catastrophic Forgetting
    keypoint_weight: 0.4
    description: Xảy ra khi mô hình cập nhật trọng số quá mạnh để tối ưu trên miền dữ liệu mới, làm mất đi các khả năng suy luận logic và kiến thức chung đã học ở giai đoạn pre-training.
  - id: KP5_2
    content: Các giải pháp khắc phục
    keypoint_weight: 0.6
    description: Nêu được các giải pháp: Sử dụng PEFT (như LoRA/QLoRA) chỉ huấn luyện adapter; áp dụng kỹ thuật trộn dữ liệu (Data Mixing) thêm 10-20% dữ liệu pre-training chung vào tập train mới; hoặc sử dụng hàm loss ràng buộc (như EWC - Elastic Weight Consolidation).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế hoạt động của thuật toán tối ưu hóa AdamW và lý do tại sao nó vượt trội hơn Adam khi huấn luyện mô hình Transformer lớn có sử dụng L2 Regularization.
* **expected_key_points:**
  - id: KP6_1
    content: Vấn đề của L2 Regularization trong Adam
    keypoint_weight: 0.6
    description: Trong Adam thông thường, hình phạt L2 được cộng trực tiếp vào loss, dẫn đến việc lượng cập nhật weight decay bị nhân với các giá trị khoảnh khắc thích ứng (moments), làm sai lệch hệ số decay thực tế.
  - id: KP6_2
    content: Cơ chế tách biệt của AdamW
    keypoint_weight: 0.4
    description: AdamW thực hiện tách biệt hoàn toàn (decouple) weight decay ra khỏi bước tính toán gradient thích ứng, trừ trực tiếp trọng số hiện tại sau bước tối ưu giúp giữ nguyên hệ số phạt mong muốn.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách thiết lập chiến lược kiểm định chất lượng mô hình (Model Evaluation) cho hệ thống RAG quy mô lớn sử dụng LLM-as-a-judge.
* **expected_key_points:**
  - id: KP7_1
    content: Thiết lập các tiêu chí đánh giá (Metrics)
    keypoint_weight: 0.5
    description: Định nghĩa rõ 3 tiêu chí: Faithfulness (câu trả lời có trung thực với tài liệu không), Answer Relevance (câu trả lời có đúng trọng tâm câu hỏi không), và Context Precision (tài liệu truy xuất có liên quan không).
  - id: KP7_2
    content: Quy trình chạy LLM-as-a-judge
    keypoint_weight: 0.5
    description: Sử dụng mô hình mạnh (như GPT-4) được cung cấp prompt chi tiết kèm rubric điểm số để chấm điểm tự động cho các câu trả lời sinh ra từ hệ thống RAG; chạy đối chiếu chéo (cross-validation) với điểm số của con người.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống LLM Multi-Agent tự động hóa quy trình phân tích dữ liệu kinh doanh. Hệ thống nhận câu hỏi từ user -> tự viết mã Python truy vấn SQL DB -> vẽ biểu đồ -> xuất file báo cáo phân tích.
* **expected_key_points:**
  - id: KP8_1
    content: Phân chia vai trò Agents và State Management
    keypoint_weight: 0.5
    description: Thiết kế: SQL Agent (chuyển ngôn ngữ sang SQL), Python Executor Agent (thực thi code trong Docker sandbox), Visualization Agent (vẽ biểu đồ), và Report Writer Agent (tổng hợp xuất PDF). Dùng framework LangGraph quản lý trạng thái.
  - id: KP8_2
    content: Cơ chế tự sửa lỗi (Self-Correction Loop) và bảo mật
    keypoint_weight: 0.5
    description: Nếu Python executor báo lỗi cú pháp hoặc SQL báo lỗi thiếu cột, gửi log lỗi ngược lại cho Agent để tự động sửa code; giới hạn quyền SQL chỉ đọc (read-only) và sandbox Docker hoàn toàn cô lập để tránh phá hoại dữ liệu.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Bạn cần huấn luyện một mô hình ngôn ngữ lớn (LLM) quy mô 70B trên cụm 16 GPU A100. Hãy thiết kế chi tiết chiến lược sharding mô hình sử dụng kết hợp Pipeline Parallelism (PP) và Tensor Parallelism (TP).
* **expected_key_points:**
  - id: KP9_1
    content: Cấu hình phân mảnh 3D Parallelism
    keypoint_weight: 0.5
    description: Thiết lập cấu hình: Tensor Parallelism (TP=8) trên 8 GPU của cùng một node để tận dụng tối đa băng thông NVLink cực nhanh; Pipeline Parallelism (PP=2) kết nối giữa 2 nodes qua mạng InfiniBand chậm hơn.
  - id: KP9_2
    content: Tối ưu hóa thời gian chờ (Pipeline Bubble)
    keypoint_weight: 0.5
    description: Áp dụng kỹ thuật 1F1B (One Forward, One Backward) để phân phối đều các micro-batches qua các giai đoạn của pipeline, giảm thiểu thời gian nhàn rỗi (bubble time) của các GPU trong cluster.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp căn chỉnh mô hình ngôn ngữ lớn sử dụng phương pháp DPO (Direct Preference Optimization). Viết công thức toán học hàm loss của DPO và phân tích tại sao nó ổn định hơn RLHF.
* **expected_key_points:**
  - id: KP10_1
    content: Công thức toán học hàm loss của DPO
    keypoint_weight: 0.5
    description: Công thức: $\mathcal{L}_{DPO}(\pi_\theta; \pi_{ref}) = -\mathbb{E}_{(x, y_w, y_l)} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w|x)}{\pi_{ref}(y_w|x)} - \beta \log \frac{\pi_\theta(y_l|x)}{\pi_{ref}(y_l|x)} \right) \right]$ với $y_w$ là câu trả lời được thích, $y_l$ là câu trả lời bị ghét, $\pi_{ref}$ là mô hình tham chiếu gốc.
  - id: KP10_2
    content: Lý do DPO ổn định hơn RLHF
    keypoint_weight: 0.5
    description: RLHF yêu cầu huấn luyện một Reward model riêng và tối ưu hóa chính sách bằng thuật toán PPO học tăng cường (rất nhạy cảm với các siêu tham số, dễ bị sập/không hội tụ). DPO tối ưu hóa trực tiếp mô hình qua toán học, không cần chạy học tăng cường, giúp huấn luyện ổn định và hội tụ nhanh.

