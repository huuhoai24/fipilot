# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 5) - Tập Đề Pre-LN Transformers và PyTorch FSDP (16)

* **Role:** AI Engineer
* **Level:** Level 5
* **Experience:** Trên 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh sự khác nhau về cơ chế hoạt động và phạm vi áp dụng giữa ba kỹ thuật chuẩn hóa: Batch Normalization, Layer Normalization, và Group Normalization.
* **expected_key_points:**
  - id: KP1_1
    content: Phạm vi tính toán trung bình và phương sai
    keypoint_weight: 0.6
    description: Batch Normalization tính toán trên toàn bộ batch dữ liệu cho từng feature (phụ thuộc batch size). Layer Normalization tính toán trên tất cả features của một mẫu đơn lẻ (độc lập batch size). Group Normalization chia features thành các nhóm và tính toán trong từng nhóm của mẫu đơn lẻ.
  - id: KP1_2
    content: Phạm vi áp dụng tối ưu
    keypoint_weight: 0.4
    description: Batch Norm tối ưu cho CNN trong bài toán Computer Vision. Layer Norm tối ưu cho RNN/Transformer trong xử lý chuỗi. Group Norm tối ưu khi batch size cực nhỏ (ví dụ 1 hoặc 2) trong các bài toán segmentation.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao kỹ thuật Gradient Clipping lại cần thiết khi huấn luyện các mạng nơ-ron sâu hoặc mạng tuần tự? Phân biệt Clip by Value và Clip by Norm.
* **expected_key_points:**
  - id: KP2_1
    content: Hiện tượng bùng nổ gradient và vai trò của Clipping
    keypoint_weight: 0.5
    description: Giúp ngăn chặn hiện tượng bùng nổ gradient làm cập nhật trọng số quá mạnh gây NaN loss hoặc mất ổn định mô hình.
  - id: KP2_2
    content: Clip by Value vs Clip by Norm
    keypoint_weight: 0.5
    description: Clip by Value cắt từng phần tử gradient độc lập nếu vượt ngưỡng $[-c, c]$. Clip by Norm cắt toàn bộ vector gradient theo tỷ lệ nếu chuẩn của nó vượt ngưỡng, giúp giữ nguyên hướng của vector gradient.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích vai trò và lợi ích của việc sử dụng trung bình động lũy thừa (Exponential Moving Average - EMA) của trọng số mô hình khi huấn luyện GAN hoặc mô hình khuếch tán (Diffusion Models).
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế tính toán EMA weights
    keypoint_weight: 0.5
    description: Lưu trữ một bản sao trọng số mô hình được cập nhật chậm theo công thức: $\theta_{EMA} \leftarrow \beta \theta_{EMA} + (1-\beta)\theta_{train}$ với $\beta \approx 0.999$.
  - id: KP3_2
    content: Lợi ích khi suy luận (Inference)
    keypoint_weight: 0.5
    description: Giúp giảm thiểu độ nhiễu và biến động của trọng số trong quá trình huấn luyện đối kháng/khuếch tán, tạo ra các kết quả sinh ảnh mượt mà, chất lượng cao và ổn định hơn.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích nguyên lý hoạt động và sự khác biệt về cơ chế cập nhật trọng số của các thuật toán tối ưu hóa: SGD, RMSprop và Adam. Tại sao Adam là thuật toán phổ biến nhất?
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế hoạt động từng optimizer
    keypoint_weight: 0.6
    description: SGD cập nhật theo hướng gradient hiện tại. RMSprop điều chỉnh learning rate cho từng trọng số dựa trên trung bình động bình phương gradient gần đây (giảm bước nhảy trên hướng dốc). Adam kết hợp cả hai: Momentum (trung bình động gradient) và RMSprop (trung bình động bình phương gradient).
  - id: KP4_2
    content: Lý do Adam được sử dụng phổ biến nhất
    keypoint_weight: 0.4
    description: Adam tự động điều chỉnh learning rate thích ứng cho từng tham số, hội tụ rất nhanh và ổn định trên nhiều kiến trúc mạng khác nhau mà không cần tinh chỉnh nhiều.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế hoạt động của lớp Layer Normalization trong mô hình Transformer. Tại sao kiến trúc Pre-LN lại ổn định hơn Post-LN khi huấn luyện mô hình rất sâu?
* **expected_key_points:**
  - id: KP5_1
    content: Công thức toán học của Layer Norm
    keypoint_weight: 0.4
    description: Layer Norm chuẩn hóa đầu vào của một layer về phân phối có trung bình bằng 0 và phương sai bằng 1 trên chiều của feature dimension, kèm theo hai hệ số học được $\gamma$ và $\beta$.
  - id: KP5_2
    content: So sánh Pre-LN và Post-LN
    keypoint_weight: 0.6
    description: Post-LN đặt LN sau skip connection, làm gradient ở các lớp đầu dễ bị vanishing khi mạng quá sâu. Pre-LN đặt LN trước sub-layer và nằm trên nhánh chính của skip connection, cho phép gradient lan truyền ngược trực tiếp qua identity path mà không bị suy giảm, giúp huấn luyện cực kỳ ổn định.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích tác động của Batch Size cực lớn (ví dụ 32k) đến khả năng tổng quát hóa của mô hình và cách điều chỉnh Tốc độ học tương ứng sử dụng LARS hoặc LAMB optimizer.
* **expected_key_points:**
  - id: KP6_1
    content: Tác động của Large Batch Size và Generalization Gap
    keypoint_weight: 0.5
    description: Tăng batch size giúp song song hóa tốt nhưng dễ làm mô hình rơi vào các điểm cực tiểu nhọn (sharp minima) có khả năng tổng quát hóa kém trên tập test (generalization gap).
  - id: KP6_2
    content: Cơ chế của LARS / LAMB optimizer
    keypoint_weight: 0.5
    description: LARS/LAMB tính toán tốc độ học cục bộ (local learning rate) cho từng layer dựa trên tỷ lệ giữa chuẩn trọng số và chuẩn gradient của layer đó, giúp huấn luyện ổn định với batch size cực lớn lên tới chục ngàn mẫu.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế kỹ thuật huấn luyện mô hình khi gặp dữ liệu bị lệch (Imbalanced Dataset) sử dụng kỹ thuật Focal Loss kết hợp Class Weights.
* **expected_key_points:**
  - id: KP7_1
    content: Nguyên lý hoạt động và công thức Focal Loss
    keypoint_weight: 0.6
    description: Công thức: $FL(p_t) = -\alpha_t (1 - p_t)^\gamma \log(p_t)$. Tham số $\gamma$ giúp giảm thiểu đóng góp loss từ các mẫu dễ phân loại, ép mô hình tập trung học các mẫu khó (thường thuộc lớp thiểu số).
  - id: KP7_2
    content: Tích hợp Class Weights
    keypoint_weight: 0.4
    description: Gán hệ số trọng số nghịch đảo tần suất xuất hiện của lớp dữ liệu để phạt nặng hơn các lỗi dự đoán sai lớp thiểu số.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp phân tích và khắc phục lỗi mất ổn định huấn luyện (Training Instability/Loss Spike) khi train mô hình LLM 70B từ đầu.
* **expected_key_points:**
  - id: KP8_1
    content: Các công cụ giám sát và phân tích
    keypoint_weight: 0.4
    description: Theo dõi chuẩn gradient (gradient norm), chuẩn trọng số (weight norm), và tỷ lệ số lượng giá trị NaN/overflow phát sinh trong tensor activation ở từng layer thông qua TensorBoard/W&B.
  - id: KP8_2
    content: Thiết kế giải pháp khắc phục
    keypoint_weight: 0.6
    description: Áp dụng Layer Normalization thích ứng (RMSNorm); thay thế FP16 bằng BF16; thiết lập hệ thống tự động rollback checkpoint và điều chỉnh giảm learning rate tạm thời khi phát hiện gradient norm vượt ngưỡng an toàn.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống huấn luyện đa nút tự động đồng bộ hóa gradients và weights sử dụng PyTorch FSDP (Fully Sharded Data Parallel). So sánh ưu thế của FSDP so với DDP thông thường.
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế Sharding của PyTorch FSDP
    keypoint_weight: 0.5
    description: FSDP phân mảnh hoàn toàn trọng số mô hình, gradients, và trạng thái optimizer trên toàn bộ các GPU trong cluster (tương tự ZeRO-3), chỉ thu thập lại qua All-Gather khi cần.
  - id: KP9_2
    content: So sánh với DDP
    keypoint_weight: 0.5
    description: DDP nhân bản toàn bộ mô hình trên mỗi GPU nên bị giới hạn bởi dung lượng VRAM của 1 GPU đơn lẻ. FSDP cho phép huấn luyện các mô hình lớn gấp nhiều lần dung lượng của 1 GPU bằng cách tận dụng bộ nhớ gộp của toàn cụm.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống tối ưu hóa hyperparameters tự động quy mô lớn sử dụng thư viện Ray Tune kết hợp thuật toán ASHA (Asynchronous Successive Halving Algorithm).
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế hoạt động của thuật toán ASHA
    keypoint_weight: 0.6
    description: ASHA chạy song song không đồng bộ hàng trăm cấu hình thử nghiệm. Định kỳ đánh giá hiệu năng; loại bỏ sớm các cấu hình hoạt động kém (early stopping) để dồn tài nguyên GPU cho các cấu hình hứa hẹn nhất, giúp tiết kiệm 10x chi phí tính toán.
  - id: KP10_2
    content: Kiến trúc hệ thống và Tích hợp
    keypoint_weight: 0.4
    description: Thiết lập Ray Cluster điều phối tài nguyên động qua Kubernetes; cấu hình lưu checkpoint tự động cho phép dừng/chạy lại thử nghiệm linh hoạt.

