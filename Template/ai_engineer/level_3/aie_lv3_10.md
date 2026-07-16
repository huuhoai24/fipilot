# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 3) - Tập Đề Speech AI và Vision-Language Models (10)

* **Role:** AI Engineer
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy giải thích khái niệm mô hình đa phương thức (Multimodal AI). Cho ví dụ về một ứng dụng đa phương thức phổ biến trong thực tế.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa Multimodal AI
    keypoint_weight: 0.5
    description: Là hệ thống AI có khả năng tiếp nhận, xử lý và hiểu đồng thời nhiều loại dữ liệu đầu vào khác nhau (như văn bản, hình ảnh, âm thanh, video) để thực hiện tác vụ.
  - id: KP1_2
    content: Ví dụ thực tế phù hợp
    keypoint_weight: 0.5
    description: Nêu được ví dụ cụ thể như: Image Captioning (nhìn ảnh sinh mô tả), Text-to-Image (nhập prompt sinh ảnh), trợ lý ảo VLM (như GPT-4o đọc tài liệu chứa ảnh để trả lời).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày khái niệm và mục tiêu của hai công nghệ xử lý tiếng nói: ASR (Automatic Speech Recognition) và TTS (Text-to-Speech).
* **expected_key_points:**
  - id: KP2_1
    content: Mục tiêu của ASR
    keypoint_weight: 0.5
    description: Chuyển đổi tín hiệu giọng nói (âm thanh đầu vào) thành văn bản chữ viết tương ứng (Speech-to-Text).
  - id: KP2_2
    content: Mục tiêu của TTS
    keypoint_weight: 0.5
    description: Chuyển đổi dữ liệu văn bản viết thành tín hiệu tiếng nói âm thanh nhân tạo tương ứng (Text-to-Speech).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Mel-Spectrogram là gì? Tại sao nó lại là dạng biểu diễn dữ liệu âm thanh phổ biến nhất trong các mô hình Deep Learning xử lý tiếng nói?
* **expected_key_points:**
  - id: KP3_1
    content: Khái niệm Mel-Spectrogram
    keypoint_weight: 0.5
    description: Là phổ tần số của tín hiệu âm thanh theo thời gian, trong đó các tần số được chuyển đổi sang thang đo Mel (Mel scale).
  - id: KP3_2
    content: Lý do phổ biến trong Deep Learning
    keypoint_weight: 0.5
    description: Thang đo Mel mô phỏng phi tuyến tính cách tai người cảm nhận âm thanh (nhạy cảm hơn với tần số thấp). Mel-Spectrogram chuyển âm thanh thành dạng ảnh 2D, cho phép áp dụng hiệu quả các kiến trúc CNN/Transformer để học đặc trưng.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích nguyên lý hoạt động của mô hình Whisper phát triển bởi OpenAI trong bài toán nhận dạng giọng nói đa ngôn ngữ.
* **expected_key_points:**
  - id: KP4_1
    content: Kiến trúc Encoder-Decoder của Whisper
    keypoint_weight: 0.5
    description: Tín hiệu âm thanh được chuyển thành log-Mel spectrogram -> đưa qua Encoder (CNN + Transformer) trích xuất đặc trưng -> Decoder (Transformer) nhận diện và sinh ra chuỗi văn bản tự hồi quy.
  - id: KP4_2
    content: Huấn luyện đa nhiệm (Multitask learning)
    keypoint_weight: 0.5
    description: Mô hình được huấn luyện trên lượng dữ liệu khổng lồ (680,000 giờ) với định dạng token đặc biệt để đồng thời thực hiện nhiều tác vụ: nhận diện giọng nói (transcription), dịch ngôn ngữ sang tiếng Anh (translation), và xác định hoạt động tiếng nói (VAD).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày kiến trúc kết hợp giữa Vision Encoder và LLM để xây dựng mô hình ngôn ngữ hình ảnh (Vision-Language Model - VLM như LLaVA). Kỹ thuật chiếu tuyến tính (Projection Layer) đóng vai trò gì?
* **expected_key_points:**
  - id: KP5_1
    content: Kiến trúc tổng thể của VLM
    keypoint_weight: 0.5
    description: Gồm 3 thành phần: Image Encoder (như CLIP ViT) trích xuất đặc trưng ảnh, Projection Layer chiếu vector ảnh sang không gian embedding của văn bản, và LLM đóng vai trò xử lý ngôn ngữ sinh câu trả lời.
  - id: KP5_2
    content: Vai trò của Projection Layer (như MLP)
    keypoint_weight: 0.5
    description: Do vector đặc trưng ảnh từ ViT có kích thước khác với vector token của LLM, Projection Layer thực hiện ánh xạ tuyến tính/phi tuyến để biến đổi vector ảnh thành các 'visual tokens' có cùng kích thước và không gian ngữ nghĩa với word embeddings, giúp LLM đọc hiểu ảnh như đọc các từ văn bản thông thường.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh các phương pháp tổng hợp giọng nói (TTS): kiến trúc hai giai đoạn truyền thống (như Tacotron2 kết hợp Vocoder WaveNet) và các mô hình sinh hiện đại dựa trên Diffusion hoặc Neural Codec (như VALL-E).
* **expected_key_points:**
  - id: KP6_1
    content: Đặc trưng kiến trúc hai giai đoạn truyền thống
    keypoint_weight: 0.5
    description: Giai đoạn 1 chuyển văn bản thành Mel-spectrogram (Tacotron2). Giai đoạn 2 chuyển Mel-spectrogram thành sóng âm thanh thô (Vocoder WaveNet). Chất lượng tốt nhưng tốc độ chậm và giọng nói thiếu cảm xúc tự nhiên.
  - id: KP6_2
    content: Đặc trưng mô hình hiện đại (Diffusion/Neural Codec)
    keypoint_weight: 0.5
    description: Sử dụng mô hình khuếch tán (Diffusion) sinh trực tiếp âm thanh từ text, hoặc dùng Neural Codec (VALL-E) mã hóa âm thanh thành các mã số (acoustic tokens) rồi huấn luyện LLM để sinh mã số này. Giúp bắt chước giọng nói cực giống (Zero-shot TTS) chỉ cần 3 giây giọng mẫu.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Cách đánh giá chất lượng mô hình nhận dạng giọng nói (ASR) bằng chỉ số Word Error Rate (WER) và Character Error Rate (CER). Giải thích công thức tính toán.
* **expected_key_points:**
  - id: KP7_1
    content: Công thức tính WER và CER
    keypoint_weight: 0.6
    description: Công thức: $WER/CER = \frac{S + D + I}{N}$ với $S$ là số từ/ký tự bị thế thế (Substitution), $D$ là số từ/ký tự bị xóa (Deletion), $I$ là số từ/ký tự bị chèn thêm (Insertion), và $N$ là tổng số từ/ký tự trong câu mẫu gốc.
  - id: KP7_2
    content: Trường hợp áp dụng
    keypoint_weight: 0.4
    description: WER dùng cho các ngôn ngữ có phân tách từ rõ ràng bằng khoảng trắng (như tiếng Anh). CER dùng cho các ngôn ngữ không có khoảng trắng phân tách từ rõ ràng (như tiếng Trung, tiếng Nhật) hoặc tiếng Việt để đánh giá chi tiết lỗi chính tả.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống Trợ lý ảo đa phương thức thời gian thực (Real-time Multimodal Assistant) có khả năng nghe giọng nói của người dùng, nhìn qua camera và phản hồi bằng giọng nói tự nhiên với độ trễ (end-to-end latency) < 500ms.
* **expected_key_points:**
  - id: KP8_1
    content: Thiết kế kiến trúc tích hợp (End-to-End Multimodal)
    keypoint_weight: 0.5
    description: Tránh dùng pipeline rời rạc (ASR -> LLM -> TTS) gây trễ lớn. Sử dụng mô hình tích hợp đa phương thức trực tiếp (như GPT-4o style): nhận trực tiếp luồng audio/video đầu vào qua encoder chuyên biệt, xử lý trên cùng một mạng nơ-ron Transformer trung tâm, và giải mã sinh trực tiếp audio tokens đầu ra (Vocoding) mà không qua text trung gian.
  - id: KP8_2
    content: Tối ưu hóa truyền nhận dữ liệu (Streaming & Quantization)
    keypoint_weight: 0.5
    description: Triển khai cơ chế truyền dữ liệu dạng luồng (audio streaming/chunking) qua WebSockets; sử dụng lượng tử hóa mô hình sang INT4/INT8 và TensorRT để đẩy nhanh tốc độ suy luận của mô hình trung tâm trên GPU.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp tự động sinh phụ đề (Subtitle) và lồng tiếng tự động (Voice Dubbing) cho video bài giảng đa ngôn ngữ, đảm bảo giọng lồng tiếng khớp khẩu hình chuyển động môi (Lip-sync) của giáo viên trong video.
* **expected_key_points:**
  - id: KP9_1
    content: Pipeline nhận dạng, dịch thuật và sinh giọng nói
    keypoint_weight: 0.5
    description: Whisper ASR nhận diện giọng nói -> Dịch thuật bằng LLM sang ngôn ngữ đích -> TTS sinh giọng lồng tiếng giữ nguyên chất giọng (voice cloning) của giáo viên gốc.
  - id: KP9_2
    content: Đồng bộ hóa hình ảnh và khớp khẩu hình (Lip-sync)
    keypoint_weight: 0.5
    description: Tính toán độ dài thời gian của câu dịch khớp với câu gốc (điều chỉnh tốc độ nói của TTS). Sử dụng mô hình học sâu sinh hình ảnh vùng môi (như Wav2Lip) nhận đầu vào là video giáo viên và file âm thanh lồng tiếng mới để tự động tái tạo, đồng bộ hóa chuyển động môi khớp hoàn toàn với âm thanh mới sinh ra.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế mô hình chẩn đoán bệnh từ hình ảnh X-quang phổi kết hợp với thông tin bệnh án dạng văn bản viết tay sử dụng kiến trúc học sâu đa phương thức (Multimodal Medical Diagnostics).
* **expected_key_points:**
  - id: KP10_1
    content: Thiết kế Fusion Pipeline (Kết hợp đa nguồn)
    keypoint_weight: 0.6
    description: Sử dụng mạng CNN/ViT (như DenseNet/DeiT) trích xuất đặc trưng ảnh X-quang phổi thành vector $v_{img}$. Sử dụng BioBERT/ClinicalBERT trích xuất đặc trưng văn bản bệnh án thành vector $v_{text}$. Kết hợp hai đặc trưng bằng kỹ thuật Cross-Attention (học quan hệ chéo giữa ảnh và text) hoặc gộp vector (Feature Concatenation).
  - id: KP10_2
    content: Huấn luyện có ràng buộc y khoa và giải thích được (Explainability)
    keypoint_weight: 0.4
    description: Huấn luyện mô hình sử dụng hàm loss kết hợp độ chính xác chẩn đoán và độ bao phủ báo cáo y khoa; sử dụng cơ chế Attention Rollout để trực quan hóa bản đồ nhiệt (Saliency Map/Heatmap) chỉ ra vị trí trên ảnh phổi mà mô hình dựa vào để chẩn đoán, giúp bác sĩ dễ dàng đối chứng.

