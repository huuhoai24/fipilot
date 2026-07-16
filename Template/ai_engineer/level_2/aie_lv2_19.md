# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 2) - Tập Đề QLoRA và LLM Agents (19)

* **Role:** AI Engineer
* **Level:** Level 2
* **Experience:** 1 - 3  năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Mô hình ngôn ngữ lớn (LLM) là gì? Giải thích cơ chế sinh từ tự hồi quy (Autoregressive generation) hoạt động như thế nào.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa LLM
    keypoint_weight: 0.4
    description: Là các mô hình mạng nơ-ron Transformer có kích thước cực lớn (hàng tỷ tham số), huấn luyện trên lượng dữ liệu khổng lồ để hiểu và sinh ngôn ngữ tự nhiên.
  - id: KP1_2
    content: Cơ chế sinh tự hồi quy (Autoregressive)
    keypoint_weight: 0.6
    description: Mô hình sinh văn bản từng từ (token) một từ trái qua phải. Từ được sinh ra ở bước $t$ sẽ được gộp ngược lại vào chuỗi đầu vào làm ngữ cảnh để dự đoán từ tiếp theo ở bước $t+1$.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày khái niệm và cho ví dụ minh họa về 3 kỹ thuật Prompt Engineering cơ bản: Few-shot Prompting, Chain of Thought (CoT), và System Prompts.
* **expected_key_points:**
  - id: KP2_1
    content: Few-shot Prompting và System Prompts
    keypoint_weight: 0.5
    description: System Prompts định nghĩa vai trò, quy tắc ứng xử của LLM. Few-shot Prompting cung cấp cho LLM một vài ví dụ minh họa mẫu đầu vào-đầu ra trong prompt để mô hình bắt chước làm theo.
  - id: KP2_2
    content: Chain of Thought (CoT)
    keypoint_weight: 0.5
    description: Chain of Thought yêu cầu LLM giải thích từng bước lập luận logic trước khi đưa ra kết quả cuối cùng (thường dùng câu 'Let's think step by step'), giúp tăng độ chính xác trên bài toán tính toán logic.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Định dạng file lượng tử hóa GGUF là gì? Tại sao định dạng này lại hữu ích cho việc chạy mô hình LLM trên máy tính cá nhân local?
* **expected_key_points:**
  - id: KP3_1
    content: Đặc trưng định dạng GGUF
    keypoint_weight: 0.5
    description: GGUF là định dạng file nhị phân được tối ưu hóa riêng bởi thư viện llama.cpp, lưu trữ toàn bộ trọng số mô hình đã lượng tử hóa (quantized) và metadata của LLM trong một file duy nhất.
  - id: KP3_2
    content: Lợi ích chạy local
    keypoint_weight: 0.5
    description: Hỗ trợ cơ chế CPU offloading (chuyển một phần lớp mô hình từ VRAM GPU sang RAM hệ thống để chạy), giúp chạy mượt mà các LLM lớn trên máy tính cá nhân có GPU yếu hoặc chỉ có CPU.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích kỹ thuật QLoRA (Quantized Low-Rank Adaptation). Những yếu tố công nghệ nào giúp QLoRA huấn luyện LLM lớn cực kỳ tiết kiệm bộ nhớ?
* **expected_key_points:**
  - id: KP4_1
    content: Lượng tử hóa mô hình gốc sang 4-bit NF4
    keypoint_weight: 0.6
    description: QLoRA lượng tử hóa các trọng số gốc của mô hình sang định dạng 4-bit NormalFloat (NF4) - một kiểu dữ liệu tối ưu riêng cho các trọng số có phân phối chuẩn, giúp nén cực mạnh mô hình gốc trên VRAM.
  - id: KP4_2
    content: Double Quantization và Paged Optimizers
    keypoint_weight: 0.4
    description: Double Quantization lượng tử hóa chính các hằng số scale factor để tiết kiệm thêm VRAM. Paged Optimizers tận dụng bộ nhớ RAM hệ thống thông qua cơ chế phân trang để tránh lỗi hết bộ nhớ (Out-Of-Memory) khi VRAM bị quá tải đột ngột.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh các kỹ thuật tinh chỉnh LLM: Full Fine-tuning, LoRA (Low-Rank Adaptation), và Prefix Tuning về số lượng tham số huấn luyện và hiệu năng đạt được.
* **expected_key_points:**
  - id: KP5_1
    content: Đặc trưng Prefix Tuning vs LoRA
    keypoint_weight: 0.6
    description: Prefix Tuning thêm các vector ảo học được (virtual tokens) vào đầu các lớp attention. LoRA thêm các ma trận cập nhật hạng thấp song song với lớp trọng số gốc. LoRA ổn định và dễ huấn luyện hơn Prefix Tuning.
  - id: KP5_2
    content: So sánh tham số và hiệu năng
    keypoint_weight: 0.4
    description: Full fine-tuning cập nhật 100% tham số, hiệu năng cao nhất nhưng tốn chi phí cực lớn. LoRA chỉ cập nhật <1% tham số nhưng đạt hiệu năng tương đương 95-99% so với Full fine-tuning trên hầu hết bài toán.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Hiện tượng Ảo tưởng (Hallucination) của LLM là gì? Hãy nêu nguyên nhân gốc rễ và 3 phương pháp kỹ thuật giảm thiểu hiện tượng này ở cấp độ ứng dụng.
* **expected_key_points:**
  - id: KP6_1
    content: Bản chất và nguyên nhân ảo tưởng
    keypoint_weight: 0.5
    description: Là hiện tượng LLM sinh ra thông tin trông rất thuyết phục nhưng sai lệch thực tế. Nguyên nhân do mô hình được huấn luyện đoán từ tiếp theo dựa trên xác suất, thiếu nguồn kiểm chứng thực tế và dữ liệu huấn luyện chứa thông tin sai.
  - id: KP6_2
    content: 3 phương pháp giảm thiểu
    keypoint_weight: 0.5
    description: Nêu được: Tích hợp RAG để bổ sung ngữ cảnh thực tế; thiết lập siêu tham số Temperature = 0 để giảm tính ngẫu nhiên; thiết lập Prompt hướng dẫn nghiêm ngặt yêu cầu LLM nói 'tôi không biết' nếu không tìm thấy thông tin.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách thức xây dựng bài test đánh giá năng lực viết code của mô hình ngôn ngữ sử dụng metric HumanEval. Cách tính chỉ số pass@k là gì?
* **expected_key_points:**
  - id: KP7_1
    content: Đánh giá bằng bộ test HumanEval
    keypoint_weight: 0.5
    description: Gửi các bài toán lập trình mẫu (prompt chứa hàm và mô tả) cho LLM sinh code. Chạy code sinh ra trực tiếp trên môi trường độc lập với bộ unit tests tự động để kiểm tra tính đúng đắn.
  - id: KP7_2
    content: Công thức và ý nghĩa pass@k
    keypoint_weight: 0.5
    description: pass@k đo tỷ lệ giải quyết bài toán thành công khi mô hình sinh ra $n$ mẫu thử và chọn ngẫu nhiên $k$ mẫu ($k \le n$): $pass@k = \mathbb{E} [1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}]$ với $c$ là số mẫu vượt qua unit tests. Đánh giá khách quan hơn sinh 1 lần duy nhất.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống AI Software Engineer Agent (như Devin) có khả năng tự động đọc log lỗi của hệ thống, định vị file lỗi, sửa code, chạy unit tests, và tạo Pull Request tự động.
* **expected_key_points:**
  - id: KP8_1
    content: Thiết lập Sandbox Environment và Tool Calling
    keypoint_weight: 0.5
    description: Cung cấp cho Agent một môi trường chạy biệt lập (Docker sandbox) an toàn; cung cấp các công cụ (tools) cho phép Agent gọi lệnh bash terminal để chạy test, công cụ đọc/ghi file, và công cụ tương tác Git API.
  - id: KP8_2
    content: Kiến trúc ReAct và Planning-Feedback loops
    keypoint_weight: 0.5
    description: Sử dụng cơ chế ReAct (Reasoning + Acting) để Agent tự lập kế hoạch sửa lỗi -> thực thi viết code -> chạy unit test tự động. Nếu test lỗi (compiler error/test fail), đọc log lỗi làm feedback nạp lại cho LLM để tự sửa lỗi (self-debugging loop) cho đến khi 100% test pass rồi mới push PR.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trình bày chi tiết cách huấn luyện mô hình ngôn ngữ sử dụng phương pháp DPO (Direct Preference Optimization). Viết công thức toán học hàm loss của DPO và so sánh ưu điểm lớn nhất so với quy trình RLHF truyền thống.
* **expected_key_points:**
  - id: KP9_1
    content: Công thức toán học loss function của DPO
    keypoint_weight: 0.5
    description: Công thức: $\mathcal{L}_{DPO}(\pi_\theta; \pi_{ref}) = -\mathbb{E}_{(x, y_w, y_l)} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w|x)}{\pi_{ref}(y_w|x)} - \beta \log \frac{\pi_\theta(y_l|x)}{\pi_{ref}(y_l|x)} \right) \right]$ với $y_w$ là câu trả lời được thích, $y_l$ là câu trả lời bị ghét, $\pi_{ref}$ là mô hình tham chiếu gốc.
  - id: KP9_2
    content: Ưu điểm so với RLHF
    keypoint_weight: 0.5
    description: DPO chứng minh toán học rằng hàm loss của nó tương đương trực tiếp với việc giải bài toán RLHF. Loại bỏ hoàn toàn phase train Reward model và phase chạy PPO RL cực kỳ mất ổn định và tốn RAM; giúp quá trình alignment dễ huấn luyện, hội tụ nhanh và ổn định hơn.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống AI Agent tự động sinh báo cáo phân tích thị trường tài chính hàng ngày bằng cách cào dữ liệu từ hàng ngàn nguồn tin trực tuyến, lọc tin giả, tổng hợp xu hướng và xuất báo cáo dạng PDF định dạng chuẩn.
* **expected_key_points:**
  - id: KP10_1
    content: Kiến trúc hệ thống thu thập và lọc tin giả (Credibility Filter)
    keypoint_weight: 0.5
    description: Xây dựng scraper cào tin tức tự động -> Nhập dữ liệu vào pipeline -> Sử dụng mô hình phân loại tin cậy (nhãn: tin tức chính thống, tin đồn mạng xã hội, tin giả) để lọc bỏ tin rác; dùng hybrid search lưu trữ ngữ cảnh ngắn hạn.
  - id: KP10_2
    content: Tổng hợp xu hướng và xuất PDF chất lượng cao
    keypoint_weight: 0.5
    description: Sử dụng LLM phân tích cảm xúc (Sentiment Analysis) và tóm tắt đa văn bản để đúc kết xu hướng thị trường; sử dụng các thư viện như ReportLab (Python) để tự động viết báo cáo thành PDF chuẩn có biểu đồ trực quan, thiết lập kiểm tra chất lượng số liệu đối chiếu chéo (cross-reference).

