# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 4) - Tập Đề Multi-modal VLMs và Speech AI (11)

* **Role:** AI Engineer
* **Level:** Level 4
* **Experience:** 6 - 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Lớp chiếu tuyến tính (Projection Layer) như MLP hay Linear Projection đóng vai trò gì trong kiến trúc Vision-Language Model (VLM như LLaVA) và tại sao ta cần nó?
* **expected_key_points:**
  - id: KP1_1
    content: Bản chất toán học và đồng bộ không gian vector
    keypoint_weight: 0.5
    description: Image Encoder sinh ra đặc trưng ảnh có kích thước vector khác với chiều embedding của văn bản. Projection Layer chiếu vector đặc trưng ảnh sang không gian embedding văn bản của LLM.
  - id: KP1_2
    content: Vai trò của visual tokens
    keypoint_weight: 0.5
    description: Biến các đặc trưng ảnh thành các 'visual tokens' có ngữ nghĩa và định dạng giống với tokens chữ, cho phép LLM đọc hiểu hình ảnh trực tiếp.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt cơ chế Classifier-Free Guidance (CFG) và Classifier-Based Guidance trong mô hình khuếch tán (Diffusion Models) để kiểm soát chất lượng sinh ảnh.
* **expected_key_points:**
  - id: KP2_1
    content: Classifier-Based Guidance
    keypoint_weight: 0.5
    description: Sử dụng một mô hình phân loại ảnh phụ để tính toán gradient nhãn và cộng trực tiếp gradient này vào bước khử nhiễu để định hướng ảnh sinh ra (phức tạp, phụ thuộc phân loại).
  - id: KP2_2
    content: Classifier-Free Guidance (CFG)
    keypoint_weight: 0.5
    description: Huấn luyện đồng thời mô hình khuếch tán có nhãn và không nhãn (bằng cách che nhãn ngẫu nhiên). Khi suy luận, nội suy giữa hai dự đoán này để định hướng ảnh sinh ra theo prompt mà không cần mô hình phân loại phụ.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao các mô hình Speech AI xử lý âm thanh như Whisper sử dụng Log-Mel Spectrogram làm đầu vào thay vì sử dụng trực tiếp sóng âm thanh thô (Raw Audio Waveform)?
* **expected_key_points:**
  - id: KP3_1
    content: Thang đo Mel và cảm nhận phi tuyến của tai người
    keypoint_weight: 0.5
    description: Thang đo Mel mô phỏng cách tai người cảm nhận âm thanh phi tuyến tính (nhạy cảm với tần số thấp hơn tần số cao). Log-Mel chuyển đổi tần số sang thang đo này.
  - id: KP3_2
    content: Chuyển thành bài toán 2D và giảm chiều dữ liệu
    keypoint_weight: 0.5
    description: Biến đổi chuỗi âm thanh 1D dài vô hạn thành ma trận ảnh 2D (Thời gian x Tần số), giúp dễ áp dụng mạng CNN/Transformer để trích xuất đặc trưng.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế chi tiết kiến trúc CLIP (Contrastive Language-Image Pretraining) và phân tích hàm loss InfoNCE được sử dụng để tối ưu hóa mối tương quan ngữ nghĩa đa phương thức.
* **expected_key_points:**
  - id: KP4_1
    content: Kiến trúc Image Encoder và Text Encoder
    keypoint_weight: 0.5
    description: Image Encoder trích xuất đặc trưng ảnh, Text Encoder trích xuất đặc trưng văn bản. Chi chiếu hai đặc trưng này về cùng số chiều embedding và tính toán ma trận tương đồng cosine.
  - id: KP4_2
    content: Hàm loss InfoNCE toán học
    keypoint_weight: 0.5
    description: InfoNCE kéo gần vector của các cặp tương ứng (diagonal) và đẩy xa các cặp chéo (negative pairs). Sử dụng hàm loss cross-entropy đối xứng trên cả hai trục hàng và cột của ma trận tương đồng.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế hoán đổi và đồng bộ trong các mô hình tổng hợp giọng nói Zero-shot TTS (như VALL-E) sử dụng Neural Audio Codecs.
* **expected_key_points:**
  - id: KP5_1
    content: Mã hóa âm thanh thành Neural Codecs
    keypoint_weight: 0.5
    description: Sử dụng EnCodec nén âm thanh thành các mã số rời rạc (acoustic tokens) ở các tầng tần số khác nhau.
  - id: KP5_2
    content: Huấn luyện tự hồi quy (Autoregressive) trên tokens
    keypoint_weight: 0.5
    description: Huấn luyện mô hình Transformer nhận đầu vào là văn bản và 3 giây âm thanh mẫu (prompt), tự hồi quy sinh ra chuỗi acoustic tokens tương ứng cho văn bản mới.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích cách tối ưu hóa suy luận mô hình Vision-Language (VLM) lớn bằng công cụ TensorRT-LLM để đạt throughput tối đa trên máy chủ production.
* **expected_key_points:**
  - id: KP6_1
    content: Tách biệt suy luận Vision và LLM
    keypoint_weight: 0.5
    description: Image Encoder chạy một lần duy nhất sinh ra visual tokens. LLM chạy tự hồi quy sinh từ tiếp theo (nhiều bước). Cần thiết lập pipeline song song hóa hai giai đoạn này.
  - id: KP6_2
    content: Tối ưu hóa TensorRT-LLM
    keypoint_weight: 0.5
    description: Áp dụng PagedAttention cho KV Cache của phần LLM, lượng tử hóa INT4/INT8 AWQ cho LLM và FP16 cho Image Encoder để tăng throughput.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách đo lường chất lượng mô hình nhận dạng giọng nói tiếng Việt sử dụng chỉ số Word Error Rate (WER) và Character Error Rate (CER). Phân tích các trường hợp sai lệch do từ ghép tiếng Việt.
* **expected_key_points:**
  - id: KP7_1
    content: Công thức và ý nghĩa WER vs CER
    keypoint_weight: 0.6
    description: WER/CER = (S + D + I) / N với S là thay thế, D là xóa, I là thêm nhãn. WER tính theo từ phân cách bởi khoảng trắng, CER tính theo ký tự.
  - id: KP7_2
    content: Thách thức với tiếng Việt
    keypoint_weight: 0.4
    description: Tiếng Việt có từ ghép gồm nhiều tiếng phân cách bởi khoảng trắng. Đánh giá bằng WER thuần có thể phạt nặng các lỗi nhỏ viết hoa/viết liền; cần kết hợp CER để đánh giá đúng chất lượng.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống lồng tiếng tự động (Voice Dubbing) cho video bài giảng đa ngôn ngữ kết hợp Lip-sync (Wav2Lip) và Voice Cloning có độ trễ cực thấp.
* **expected_key_points:**
  - id: KP8_1
    content: Pipeline đồng bộ thời gian và Voice Cloning
    keypoint_weight: 0.5
    description: Dịch văn bản -> TTS sinh audio -> Dùng kỹ thuật Time-stretching điều chỉnh tốc độ nói của audio mới khớp đúng độ dài câu nói gốc trong video. Clone giọng giáo viên gốc qua XTTS.
  - id: KP8_2
    content: Đồng bộ hóa chuyển động môi bằng Wav2Lip
    keypoint_weight: 0.5
    description: Gửi video gốc và audio mới qua mô hình Wav2Lip để sinh lại vùng môi giáo viên khớp hoàn toàn với âm thanh mới; tối ưu hóa pipeline song song trên GPU để xuất video thời gian thực.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế mô hình chẩn đoán đa phương thức (Multimodal Medical Diagnostics) kết hợp ảnh X-quang phổi và hồ sơ bệnh án phi cấu trúc sử dụng kiến trúc học sâu kết hợp Cross-Attention Fusion.
* **expected_key_points:**
  - id: KP9_1
    content: Kiến trúc trích xuất và Cross-Attention Fusion
    keypoint_weight: 0.6
    description: Dùng ViT trích đặc trưng ảnh thành $v_{img}$, dùng ClinicalBERT trích đặc trưng bệnh án thành $v_{text}$. Áp dụng lớp Cross-Attention để đặc trưng ảnh chú ý đến từ khóa bệnh án và ngược lại.
  - id: KP9_2
    content: Giải thích mô hình và Attention Maps
    keypoint_weight: 0.4
    description: Sinh bản đồ nhiệt (attention maps) chồng lên ảnh X-quang để chỉ rõ vùng tổn thương mà mô hình dựa vào chẩn đoán, cung cấp tính giải thích được (explainability) cho bác sĩ.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống trợ lý ảo Multimodal thời gian thực nhận luồng audio/video liên tục từ camera/mic của người dùng và phản hồi dưới 500ms.
* **expected_key_points:**
  - id: KP10_1
    content: Kiến trúc mô hình tích hợp End-to-End
    keypoint_weight: 0.6
    description: Tránh dùng pipeline tuần tự (ASR -> LLM -> TTS). Sử dụng mô hình tích hợp (như GPT-4o style): nhận âm thanh thô qua encoder, xử lý trên mạng Transformer, sinh trực tiếp audio tokens đầu ra.
  - id: KP10_2
    content: Tối ưu hóa Streaming và truyền dữ liệu
    keypoint_weight: 0.4
    description: Sử dụng giao thức WebSockets truyền luồng âm thanh dạng chunks nhỏ; áp dụng Tensor Parallelism và dynamic batching trên server GPU để giảm thiểu độ trễ suy luận.

