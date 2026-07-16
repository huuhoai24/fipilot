# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 2) - Tập Đề Deep Learning và LLM Architectures (3)

* **Role:** AI Engineer
* **Level:** Level 2
* **Experience:** 1 - 3  năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Hàm kích hoạt (activation function) là gì? So sánh các hàm ReLU, LeakyReLU và GELU về công thức và ưu nhược điểm.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa hàm kích hoạt
    keypoint_weight: 0.4
    description: Là hàm phi tuyến áp dụng lên đầu ra của các nơ-ron, giúp mạng học được các quan hệ phi tuyến phức tạp trong dữ liệu.
  - id: KP1_2
    content: So sánh ReLU, LeakyReLU và GELU
    keypoint_weight: 0.6
    description: ReLU: $f(x)=max(0,x)$, đơn giản nhưng gặp lỗi 'dying ReLU'. LeakyReLU: $f(x)=max(\alpha x, x)$ sửa lỗi dying ReLU bằng cách cho phép rò rỉ giá trị âm. GELU: kết hợp thuộc tính của ReLU và Dropout qua phân phối Gauss, mượt mà hơn ở điểm 0, giúp mô hình Transformer hoạt động ổn định hơn.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa phương pháp nhúng từ Word2Vec (Skip-gram/CBOW) và các mô hình Contextual Embedding như BERT.
* **expected_key_points:**
  - id: KP2_1
    content: Đặc trưng Word2Vec (Static)
    keypoint_weight: 0.5
    description: Word2Vec tạo ra vector nhúng tĩnh cho mỗi từ độc lập với ngữ cảnh (từ 'bank' trong 'river bank' và 'money bank' có cùng vector).
  - id: KP2_2
    content: Đặc trưng Contextual Embedding (Dynamic)
    keypoint_weight: 0.5
    description: Mô hình như BERT sử dụng Transformer Self-Attention sinh ra vector nhúng động thay đổi tùy thuộc vào ngữ cảnh của các từ xung quanh trong câu.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt hai kỹ thuật chuẩn hóa Batch Normalization và Layer Normalization. Khi nào nên dùng loại nào?
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế Batch Norm vs Layer Norm
    keypoint_weight: 0.6
    description: Batch Norm chuẩn hóa dữ liệu trên chiều batch (tính trung bình/phương sai của một đặc trưng qua tất cả samples trong batch). Layer Norm chuẩn hóa trên chiều feature (tính trung bình/phương sai của tất cả đặc trưng trong một sample duy nhất).
  - id: KP3_2
    content: Phạm vi và thời điểm áp dụng
    keypoint_weight: 0.4
    description: Batch Norm thích hợp cho CNN và mạng MLP có batch size ổn định. Layer Norm hoạt động độc lập với batch size, rất phù hợp cho dữ liệu chuỗi có độ dài thay đổi như RNN và Transformer.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy giải thích cơ chế hoạt động của kỹ thuật Tokenization trong xử lý ngôn ngữ tự nhiên (NLP) như Byte Pair Encoding (BPE) hoặc WordPiece.
* **expected_key_points:**
  - id: KP4_1
    content: Mục tiêu của Subword Tokenization
    keypoint_weight: 0.4
    description: Giải quyết vấn đề từ ngoài từ điển (Out-Of-Vocabulary - OOV) và giảm kích thước từ điển bằng cách chia từ thành các subwords/characters.
  - id: KP4_2
    content: Thuật toán BPE hoặc WordPiece
    keypoint_weight: 0.6
    description: BPE bắt đầu từ các ký tự đơn lẻ, lặp đi lặp lại việc ghép cặp ký tự/subword xuất hiện nhiều nhất trong ngữ liệu thành token mới. WordPiece tương tự nhưng chọn cặp giúp tối đa hóa khả năng dự đoán (likelihood) của mô hình ngôn ngữ.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh hai mô hình ngôn ngữ BERT và GPT về kiến trúc (Encoder-only vs Decoder-only) và mục tiêu huấn luyện pre-training.
* **expected_key_points:**
  - id: KP5_1
    content: Kiến trúc Encoder vs Decoder
    keypoint_weight: 0.5
    description: BERT là Encoder-only, sử dụng cơ chế self-attention hai chiều (bi-directional) để hiểu ngữ cảnh đầy đủ. GPT là Decoder-only, sử dụng masked self-attention (chỉ nhìn về phía trước/bên trái) để sinh văn bản.
  - id: KP5_2
    content: Mục tiêu pre-training
    keypoint_weight: 0.5
    description: BERT được huấn luyện bằng Masked Language Modeling (MLM - đoán từ bị che) và Next Sentence Prediction (NSP). GPT huấn luyện bằng Causal Language Modeling (CLM - đoán từ tiếp theo từ trái qua phải).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy phân tích sự khác nhau giữa các thuật toán Boosting dựa trên cây quyết định: Gradient Boosting, XGBoost, và LightGBM.
* **expected_key_points:**
  - id: KP6_1
    content: Sự phát triển của XGBoost từ Gradient Boosting
    keypoint_weight: 0.5
    description: Gradient Boosting xây dựng cây tuần tự dựa trên gradient của loss. XGBoost tối ưu hóa bằng cách thêm L1/L2 regularization vào loss function của cây, tính toán song song việc tìm điểm chia (split finding), và xử lý tốt dữ liệu khuyết.
  - id: KP6_2
    content: Đặc trưng tối ưu của LightGBM
    keypoint_weight: 0.5
    description: LightGBM phát triển cây theo chiều sâu (Leaf-wise) thay vì chiều ngang (Level-wise) như XGBoost; sử dụng kỹ thuật GOSS (Gradient-based One-Side Sampling) và EFB (Exclusive Feature Bundling) giúp tốc độ train nhanh hơn rất nhiều và tốn ít RAM hơn.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách sử dụng và phân biệt các chỉ số đánh giá mô hình sinh văn bản (LLM): BLEU, ROUGE và Perplexity.
* **expected_key_points:**
  - id: KP7_1
    content: Ý nghĩa BLEU và ROUGE
    keypoint_weight: 0.6
    description: BLEU đo lường độ chính xác (precision) của các n-gram từ bản dịch máy so với bản dịch mẫu của con người (thường dùng cho dịch máy). ROUGE đo lường độ bao phủ (recall) dựa trên các chuỗi con chung dài nhất (LCS), thường dùng cho tóm tắt văn bản (summarization).
  - id: KP7_2
    content: Ý nghĩa Perplexity (PPL)
    keypoint_weight: 0.4
    description: Đo lường mức độ bất ngờ của mô hình ngôn ngữ khi dự đoán từ tiếp theo. PPL càng thấp chứng tỏ mô hình có khả năng dự đoán từ ngữ chính xác, tự tin hơn.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Khi huấn luyện các mô hình AI lớn trên hệ thống nhiều GPU, hãy phân biệt các chiến lược huấn luyện phân tán: Data Parallelism (DP/DDP) so với Model Parallelism (Pipeline Parallelism vs Tensor Parallelism).
* **expected_key_points:**
  - id: KP8_1
    content: Chiến lược Data Parallelism
    keypoint_weight: 0.5
    description: Mô hình đầy đủ được sao chép trên mỗi GPU, dữ liệu huấn luyện được chia thành các phần nhỏ (shards). Mỗi GPU tính gradient độc lập, sau đó đồng bộ hóa gradients qua lệnh All-Reduce (DDP tối ưu hơn DP nhờ chạy bất đồng bộ).
  - id: KP8_2
    content: Chiến lược Model Parallelism
    keypoint_weight: 0.5
    description: Áp dụng khi mô hình quá lớn không vừa 1 GPU. Pipeline Parallelism chia mô hình theo các lớp (layers) nằm trên các GPU khác nhau. Tensor Parallelism chia nhỏ các phép tính ma trận nội bộ (ví dụ phân tách ma trận Attention QKV) của cùng một layer qua nhiều GPU.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc một hệ thống nhận diện khuôn mặt (Face Recognition) có độ chính xác cao chạy trên thiết bị Edge di động có giới hạn về RAM và CPU.
* **expected_key_points:**
  - id: KP9_1
    content: Lựa chọn mô hình và tối ưu cấu trúc
    keypoint_weight: 0.5
    description: Sử dụng mô hình Face Detection nhẹ (như RetinaFace/MTCNN) kết hợp mô hình trích xuất đặc trưng (Feature Extractor) như MobileNetV3 hoặc ShuffleNet được huấn luyện bằng hàm loss đặc thù ArcFace để tối ưu hóa không gian embedding.
  - id: KP9_2
    content: Kỹ thuật tối ưu hóa thiết bị di động
    keypoint_weight: 0.5
    description: Lượng tử hóa mô hình sang INT8, chuyển sang định dạng TFLite hoặc ONNX Runtime Mobile để tận dụng NPU trên điện thoại; lưu trữ vectors đặc trưng của các khuôn mặt đã biết trong DB nội bộ (SQLite/Realm) để so khớp cosin cục bộ.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống bảo mật cổng API bảo vệ ứng dụng LLM khỏi các cuộc tấn công Prompt Injection, Jailbreaking và rò rỉ dữ liệu nhạy cảm (PII Leakage).
* **expected_key_points:**
  - id: KP10_1
    content: Kiểm soát Input (Prompt Injection Guardrails)
    keypoint_weight: 0.5
    description: Xây dựng lớp phòng thủ đầu vào sử dụng mô hình phân loại phụ (ví dụ Llama Guard) để phát hiện prompt độc hại, hoặc sử dụng các luật Regex/Vector search để lọc mã độc/câu lệnh ẩn.
  - id: KP10_2
    content: Kiểm soát Output và lọc PII
    keypoint_weight: 0.5
    description: Xây dựng lớp kiểm duyệt đầu ra (Output Moderation) quét thông tin nhạy cảm của người dùng (PII như CCCD, SĐT, Email) bằng các thư viện như Microsoft Presidio để che giấu (masking) thông tin trước khi trả về client.

