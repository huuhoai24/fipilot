# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 2) - Tập Đề LLMs và Self-RAG (11)

* **Role:** AI Engineer
* **Level:** Level 2
* **Experience:** 1 - 3  năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt cơ chế học tương phản (Contrastive Learning) và học tạo sinh (Generative Learning). Nêu ví dụ về mô hình ứng dụng cho từng loại.
* **expected_key_points:**
  - id: KP1_1
    content: Bản chất Contrastive Learning vs Generative Learning
    keypoint_weight: 0.6
    description: Contrastive Learning học cách so sánh sự tương đồng giữa các mẫu để kéo gần/đẩy xa chúng trong không gian embedding (ví dụ CLIP). Generative Learning học cách mô phỏng phân phối dữ liệu gốc để sinh ra mẫu mới (ví dụ VAE, GAN, Diffusion).
  - id: KP1_2
    content: Mô hình ví dụ tiêu biểu
    keypoint_weight: 0.4
    description: Contrastive: CLIP, SimCLR. Generative: Stable Diffusion, StyleGAN, GPT.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh sự khác nhau giữa kiến trúc Transformer Encoder-Decoder (như T5, BART) và Decoder-only (như LLaMA, GPT).
* **expected_key_points:**
  - id: KP2_1
    content: Cơ chế hoạt động từng loại
    keypoint_weight: 0.6
    description: Encoder-Decoder xử lý câu đầu vào qua Encoder rồi truyền thông tin qua Cross-Attention sang Decoder sinh câu đầu ra (phù hợp dịch máy, tóm tắt). Decoder-only xử lý cả đầu vào và đầu ra trên một khối duy nhất sử dụng masked attention (phù hợp sinh văn bản tự do).
  - id: KP2_2
    content: Tối ưu hóa và độ phổ biến hiện nay
    keypoint_weight: 0.4
    description: Decoder-only dễ dàng scaling lên kích thước cực lớn, tiết kiệm bộ nhớ khi train và suy luận, nên đang là kiến trúc chủ đạo cho LLMs hiện nay.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Thuật toán mã hóa Tokenizer BPE (Byte Pair Encoding) hoạt động như thế nào? Tại sao nó giải quyết được vấn đề từ ngoài từ điển (OOV)?
* **expected_key_points:**
  - id: KP3_1
    content: Quy trình ghép cặp ký tự của BPE
    keypoint_weight: 0.5
    description: Khởi tạo từ điển bằng tất cả ký tự đơn lẻ. Lặp đi lặp lại việc tìm kiếm và gộp cặp token xuất hiện nhiều nhất trong tập văn bản huấn luyện thành một token mới, dừng lại khi đạt kích thước từ điển mong muốn.
  - id: KP3_2
    content: Giải quyết từ ngoài từ điển (OOV)
    keypoint_weight: 0.5
    description: BPE có thể chia các từ lạ chưa từng thấy thành các subwords quen thuộc đã có trong từ điển, hoặc tệ nhất là chia về các ký tự đơn lẻ, đảm bảo không bao giờ gặp lỗi OOV.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế Masked Self-Attention trong mô hình GPT (Decoder-only) và tại sao nó lại cần thiết cho bài toán sinh chữ (Auto-regressive generation).
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế Masked Self-Attention
    keypoint_weight: 0.6
    description: Sử dụng một ma trận mặt nạ tam giác dưới (lower triangular mask) đặt giá trị $-\infty$ cho các vị trí từ tương lai trong phép tính Softmax, chặn không cho token hiện tại chú ý đến các token phía sau nó.
  - id: KP4_2
    content: Sự cần thiết cho Auto-regressive
    keypoint_weight: 0.4
    description: Khi sinh chữ tự hồi quy, tại mỗi bước ta chỉ có các từ trước đó. Việc sử dụng mask đảm bảo mô hình khi train không bị rò rỉ thông tin từ tương lai và hoạt động đúng như khi suy luận thực tế.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày phương pháp đánh giá mô hình phân loại đa nhãn (Multi-label Classification) sử dụng chỉ số Hamming Loss và Subset Accuracy.
* **expected_key_points:**
  - id: KP5_1
    content: Chỉ số Hamming Loss
    keypoint_weight: 0.5
    description: Đo lường tỷ lệ các nhãn bị dự đoán sai (bao gồm cả dự đoán thừa và thiếu) trên tổng số nhãn: $Hamming\ Loss = \frac{1}{N \cdot L} \sum \sum (y_{i,j} \oplus \hat{y}_{i,j})$. Càng nhỏ càng tốt.
  - id: KP5_2
    content: Chỉ số Subset Accuracy (Exact Match Ratio)
    keypoint_weight: 0.5
    description: Đo lường tỷ lệ các mẫu mà tập hợp nhãn dự đoán khớp hoàn toàn 100% với tập hợp nhãn thực tế. Đây là chỉ số khắt khe vì chỉ cần sai 1 nhãn phụ cũng tính là sai mẫu đó.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày khái niệm FlashAttention và lý do tại sao nó giúp tăng tốc độ huấn luyện mô hình Transformer mà không làm thay đổi kết quả đầu ra toán học.
* **expected_key_points:**
  - id: KP6_1
    content: Tối ưu hóa đọc ghi bộ nhớ (I/O Complexity)
    keypoint_weight: 0.6
    description: Attention thông thường ghi ma trận $N \times N$ ra bộ nhớ HBM chậm của GPU. FlashAttention chia nhỏ ma trận thành các khối (tiling), tính toán toán học Softmax lũy tiến trên bộ nhớ SRAM tốc độ cực nhanh, giảm số lần đọc ghi HBM.
  - id: KP6_2
    content: Tính chính xác toán học
    keypoint_weight: 0.4
    description: FlashAttention không phải là thuật toán xấp xỉ (approximation); nó cho kết quả đầu ra giống hệt toán học so với Standard Attention nhưng tối ưu ở cấp độ phần cứng GPU.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh các chiến lược Fine-tuning LLM: Full Fine-tuning vs Parameter-Efficient Fine-tuning (PEFT) như LoRA/QLoRA về mặt chi phí và chất lượng mô hình.
* **expected_key_points:**
  - id: KP7_1
    content: Chi phí tài nguyên (VRAM/Storage)
    keypoint_weight: 0.5
    description: Full fine-tuning yêu cầu VRAM cực lớn để lưu trữ toàn bộ gradients và optimizer states của tất cả tham số. LoRA/QLoRA chỉ lưu và cập nhật một lượng rất nhỏ trọng số adapter, cho phép train trên GPU phổ thông và lưu trữ nhiều adapters nhẹ cho các tác vụ khác nhau.
  - id: KP7_2
    content: Độ chính xác và tính tổng quát
    keypoint_weight: 0.5
    description: LoRA/QLoRA đạt độ chính xác gần như tương đương Full fine-tuning trên hầu hết tác vụ, và ít bị hiện tượng thảm họa quên (catastrophic forgetting) của mô hình gốc.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống Self-RAG hoặc Corrective RAG (CRAG) có khả năng tự động đánh giá tài liệu truy vấn, tra cứu lại khi thiếu thông tin, và kiểm tra tính nhất quán (hallucination) của câu trả lời sinh ra.
* **expected_key_points:**
  - id: KP8_1
    content: Bước đánh giá chất lượng tài liệu (Retrieval Evaluator)
    keypoint_weight: 0.5
    description: Sau khi lấy tài liệu từ Vector DB, sử dụng một mô hình phân loại nhẹ hoặc LLM prompt đánh giá độ liên quan. Nếu tài liệu rác -> kích hoạt tìm kiếm bổ sung bằng Web Search API để sửa đổi ngữ cảnh (CRAG).
  - id: KP8_2
    content: Bước sinh chữ và kiểm tra ảo giác (NLI/Attribution Verification)
    keypoint_weight: 0.5
    description: LLM sinh câu trả lời -> Dùng mô hình Natural Language Inference (NLI) hoặc Prompt chấm điểm chéo để kiểm tra xem mọi thông tin trong câu trả lời có được chứng minh hoàn toàn bởi ngữ cảnh truy vấn không (Attribution Check). Nếu phát hiện thông tin không căn cứ -> yêu cầu sinh lại hoặc lọc bỏ.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích cách tối ưu hóa bộ nhớ GPU khi huấn luyện các mô hình ngôn ngữ lớn (LLM) sử dụng cơ chế DeepSpeed ZeRO Stage 3. Giải thích cách tham số được phân mảnh và truyền tải giữa các GPU trong forward/backward pass.
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế phân mảnh đầy đủ (Full Sharding)
    keypoint_weight: 0.5
    description: ZeRO-3 phân mảnh tất cả 3 thành phần: Optimizer States, Gradients, và Model Parameters (Trọng số gốc) đồng đều trên toàn bộ các GPU trong cluster. Mỗi GPU chỉ giữ $1/N$ tham số của mô hình.
  - id: KP9_2
    content: Giao tiếp trong Forward và Backward pass
    keypoint_weight: 0.5
    description: Trong forward pass, tại mỗi layer, các GPU chạy lệnh All-Gather để thu thập đầy đủ tham số của layer đó, thực hiện tính toán, rồi lập tức giải phóng (delete) các tham số không thuộc về mình. Quy trình lặp lại tương tự trong backward pass để tính gradients và All-Reduce gradients.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp bảo mật toàn diện chống tấn công Prompt Injection, Jailbreaking và rò rỉ dữ liệu nhạy cảm (PII Leakage) cho cổng API LLM phục vụ khách hàng doanh nghiệp.
* **expected_key_points:**
  - id: KP10_1
    content: Phòng vệ đầu vào (Input Guardrails)
    keypoint_weight: 0.5
    description: Thiết lập lớp tiền xử lý: sử dụng vector search so khớp prompt với dữ liệu jailbreak đã biết, dùng mô hình Llama Guard phân loại nội dung an toàn, thiết lập các chỉ thị hệ thống (system prompts) phân tách rõ ràng phần hướng dẫn của dev và dữ liệu nhập của user.
  - id: KP10_2
    content: Kiểm duyệt đầu ra (Output Moderation & PII Redaction)
    keypoint_weight: 0.5
    description: Quét nội dung sinh ra qua mô hình NER hoặc Regex để tự động ẩn (redact) các thông tin PII (CCCD, SĐT, Email). Thiết lập mô hình hậu kiểm đánh giá độ độc hại đầu ra trước khi gửi về client.

