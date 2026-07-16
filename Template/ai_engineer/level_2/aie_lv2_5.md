# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 2) - Tập Đề Fine-Tuning LLMs và LSTM vs Transformer (5)

* **Role:** AI Engineer
* **Level:** Level 2
* **Experience:** 1 - 3  năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Khái niệm Transfer Learning (Học chuyển giao) là gì và những lợi ích chính của phương pháp này trong huấn luyện mô hình AI?
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa Transfer Learning
    keypoint_weight: 0.5
    description: Là kỹ thuật tận dụng một mô hình đã được huấn luyện trên một tập dữ liệu lớn cho một bài toán gốc (pre-trained model), sau đó tinh chỉnh (fine-tune) lại trên tập dữ liệu nhỏ hơn của bài toán mới liên quan.
  - id: KP1_2
    content: Lợi ích chính
    keypoint_weight: 0.5
    description: Tiết kiệm thời gian huấn luyện và tài nguyên tính toán; đạt hiệu năng cao hơn so với train từ đầu (scratch) khi tập dữ liệu mới quá nhỏ.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh sự khác nhau về nguyên lý cập nhật trọng số của 3 biến thể Gradient Descent: Batch GD, Stochastic GD (SGD), và Mini-batch GD.
* **expected_key_points:**
  - id: KP2_1
    content: Nguyên lý hoạt động từng loại
    keypoint_weight: 0.6
    description: Batch GD tính toán gradient trên toàn bộ tập dữ liệu trước khi cập nhật (chậm, ổn định). SGD cập nhật trọng số sau mỗi mẫu dữ liệu duy nhất (nhanh, dao động mạnh). Mini-batch GD cập nhật sau mỗi nhóm mẫu dữ liệu nhỏ (batch size 32, 64,...).
  - id: KP2_2
    content: Sự cân bằng của Mini-batch GD
    keypoint_weight: 0.4
    description: Mini-batch GD là sự kết hợp tối ưu: tận dụng được tính toán song song của GPU (vectorization) của Batch GD và tốc độ hội tụ nhanh của SGD.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tốc độ học (Learning Rate - LR) là gì? Hiện tượng gì xảy ra đối với quá trình hội tụ của mô hình khi LR quá lớn hoặc quá nhỏ?
* **expected_key_points:**
  - id: KP3_1
    content: Định nghĩa Learning Rate
    keypoint_weight: 0.4
    description: Là siêu tham số kiểm soát kích thước bước nhảy của trọng số hướng về cực tiểu của hàm mất mát trong quá trình tối ưu hóa.
  - id: KP3_2
    content: Tác động khi LR quá lớn/quá nhỏ
    keypoint_weight: 0.6
    description: LR quá lớn làm cho mô hình nhảy qua nhảy lại điểm cực tiểu, gây phân kỳ hoặc không thể hội tụ (loss tăng hoặc dao động mạnh). LR quá nhỏ làm mô hình hội tụ cực kỳ chậm và dễ bị kẹt ở các điểm cực tiểu cục bộ (local minima) hoặc điểm yên ngựa (saddle points).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy giải thích cơ chế hoạt động của kỹ thuật thích ứng hạng thấp LoRA (Low-Rank Adaptation) trong việc tinh chỉnh hiệu quả tham số (PEFT) cho LLMs.
* **expected_key_points:**
  - id: KP4_1
    content: Nguyên lý toán học của LoRA
    keypoint_weight: 0.6
    description: Đóng băng trọng số gốc của mô hình $W_0 \in \mathbb{R}^{d \times k}$. Thêm hai ma trận cập nhật hạng thấp $A \in \mathbb{R}^{d \times r}$ và $B \in \mathbb{R}^{r \times k}$ với $r \ll \min(d,k)$. Trọng số cập nhật là $\Delta W = B \cdot A$. Phép tính forward: $h = W_0 x + B A x$.
  - id: KP4_2
    content: Lợi ích về bộ nhớ và suy luận
    keypoint_weight: 0.4
    description: Giảm lượng tham số cần train lên tới 10,000 lần, giảm VRAM khi huấn luyện. Khi suy luận, các ma trận LoRA có thể cộng trực tiếp vào trọng số gốc ($W_0 + BA$) để không làm tăng độ trễ suy luận.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh sự khác nhau giữa kiến trúc LSTM (Long Short-Term Memory) và Transformer trong việc xử lý dữ liệu chuỗi (như văn bản, chuỗi thời gian).
* **expected_key_points:**
  - id: KP5_1
    content: Bản chất xử lý tuần tự vs song song
    keypoint_weight: 0.5
    description: LSTM xử lý tuần tự từng bước thời gian (step-by-step) nên không thể song song hóa hiệu quả trên GPU. Transformer xử lý song song toàn bộ chuỗi cùng một lúc nhờ cơ chế Self-Attention.
  - id: KP5_2
    content: Khả năng lưu trữ ngữ cảnh dài
    keypoint_weight: 0.5
    description: LSTM dùng các cổng (gates) để truyền thông tin nhưng vẫn gặp giới hạn khi chuỗi quá dài (lỗi trôi thông tin). Transformer kết nối trực tiếp mọi vị trí trong câu thông qua Self-Attention, giúp nắm bắt thông tin dài cực tốt.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày khái niệm và cơ chế hoạt động của kỹ thuật Nén tri thức (Knowledge Distillation) để thu nhỏ mô hình Deep Learning phục vụ deploy.
* **expected_key_points:**
  - id: KP6_1
    content: Khái niệm Teacher và Student model
    keypoint_weight: 0.5
    description: Knowledge Distillation truyền tri thức từ một mô hình lớn, phức tạp (Teacher Model) sang một mô hình nhỏ hơn, nhẹ hơn (Student Model) nhằm giảm kích thước mà không làm mất nhiều độ chính xác.
  - id: KP6_2
    content: Cơ chế Soft Target và Softmax Temperature
    keypoint_weight: 0.5
    description: Student học từ 'Soft Targets' (phân phối xác suất đầu ra mượt mà của Teacher tạo ra bởi hàm Softmax với tham số Temperature $T > 1$). Soft targets chứa nhiều thông tin ẩn về mối quan hệ giữa các lớp hơn là nhãn cứng (hard labels).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cấu trúc và vai trò của cơ chế Multi-Head Attention trong mô hình Transformer.
* **expected_key_points:**
  - id: KP7_1
    content: Cấu trúc Multi-Head Attention
    keypoint_weight: 0.6
    description: Thay vì tính attention 1 lần trên toàn bộ chiều vector, Multi-Head Attention chia nhỏ vector Query, Key, Value thành $h$ phần (heads) và chiếu vào các không gian biểu diễn khác nhau. Tính toán attention song song trên từng head, sau đó Concatenate kết quả lại và nhân với ma trận chiếu đầu ra $W^O$.
  - id: KP7_2
    content: Vai trò ngữ nghĩa
    keypoint_weight: 0.4
    description: Giúp mô hình đồng thời tập trung vào thông tin từ các không gian biểu diễn khác nhau ở các vị trí khác nhau (ví dụ: một head học quan hệ chủ ngữ-vị ngữ, head khác học quan hệ đại từ thay thế).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp Advanced RAG (Retrieval-Augmented Generation nâng cao) để xử lý các tài liệu PDF phức tạp chứa bảng biểu (tables), sơ đồ (charts) và hình ảnh.
* **expected_key_points:**
  - id: KP8_1
    content: Phân tích cấu trúc tài liệu (Document Parsing)
    keypoint_weight: 0.5
    description: Sử dụng mô hình phân tích bố cục (như LayoutParser, Unstructured) hoặc Vision LLM (như GPT-4o, ColPali) để trích xuất cấu trúc văn bản, bảng biểu, ảnh. Chuyển bảng biểu thành định dạng Markdown/HTML trước khi nhúng vector.
  - id: KP8_2
    content: Chiến lược Indexing và Retrieval đa phương thức (Multimodal/Hierarchical)
    keypoint_weight: 0.5
    description: Áp dụng kỹ thuật Parent-Child Chunking (lưu chunk nhỏ để tìm kiếm, lấy chunk lớn/ngữ cảnh đầy đủ cho LLM), sinh tóm tắt text (summaries) cho hình ảnh/bảng biểu rồi thực hiện nhúng vector trên phần tóm tắt đó, sử dụng hybrid search kết hợp reranker.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trình bày cách bạn tối ưu hóa bộ nhớ GPU khi huấn luyện các mô hình ngôn ngữ lớn (LLM) sử dụng thư viện DeepSpeed với cơ chế ZeRO (Zero Redundancy Optimizer) Stage 1, 2, và 3.
* **expected_key_points:**
  - id: KP9_1
    content: Phân bổ tài nguyên bộ nhớ khi train
    keypoint_weight: 0.4
    description: Bộ nhớ khi train LLM bị chiếm bởi: Trọng số mô hình (Parameters), Gradients, và Trạng thái tối ưu hóa (Optimizer States - ví dụ Adam chiếm gấp 4 lần trọng số).
  - id: KP9_2
    content: Cơ chế hoạt động của các Stage ZeRO
    keypoint_weight: 0.6
    description: ZeRO-1 phân mảnh (partition) Optimizer States qua các GPU. ZeRO-2 tiếp tục phân mảnh Gradients. ZeRO-3 phân mảnh toàn bộ Parameters của mô hình qua các GPU (chỉ thu thập lại qua lệnh All-Gather khi cần thiết trong forward/backward pass). Giúp giảm mạnh nhu cầu VRAM trên mỗi GPU.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống gợi ý tin tức (News Recommendation System) thời gian thực có khả năng cập nhật sở thích người dùng liên tục và xử lý hàng triệu bài viết sử dụng Graph Neural Networks (GNN).
* **expected_key_points:**
  - id: KP10_1
    content: Xây dựng Đồ thị Tương tác (User-Item Bipartite Graph)
    keypoint_weight: 0.5
    description: Biểu diễn người dùng, bài viết, chủ đề dưới dạng các nút (nodes) trên đồ thị; các tương tác (click, share, đọc) làm các cạnh (edges) có thuộc tính thời gian và mức độ tương tác.
  - id: KP10_2
    content: Huấn luyện GNN và cập nhật thời gian thực
    keypoint_weight: 0.5
    description: Sử dụng mô hình GNN (như GraphSAGE/LightGCN) để thực hiện truyền tin nhắn (message passing) học đặc trưng cấu trúc đồ thị. Sử dụng cơ chế hàng đợi streaming (Kafka) và mô hình dynamic embedding để cập nhật vector đại diện của user ngay khi họ click vào tin tức mới.

