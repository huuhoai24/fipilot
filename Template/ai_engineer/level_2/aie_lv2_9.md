# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 2) - Tập Đề Reinforcement Learning và Multimodal Models (9)

* **Role:** AI Engineer
* **Level:** Level 2
* **Experience:** 1 - 3  năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Học tăng cường (Reinforcement Learning - RL) là gì? Hãy trình bày vai trò và sự tương tác giữa các thực thể: Agent, Environment, State, Action, và Reward.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa Reinforcement Learning
    keypoint_weight: 0.4
    description: Là một nhánh của Machine Learning học cách đưa ra các quyết định hành động tối ưu thông qua việc tương tác thử-sai với môi trường để tối đa hóa phần thưởng tích lũy.
  - id: KP1_2
    content: Sự tương tác giữa các thực thể
    keypoint_weight: 0.6
    description: Tại mỗi bước thời gian, Agent (Tác nhân) quan sát State (Trạng thái) từ Environment (Môi trường) -> thực hiện một Action (Hành động) -> Environment chuyển sang State mới và trả về một Reward (Phần thưởng) cho Agent.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt bài toán phân loại đa lớp (Multi-class Classification) và bài toán phân loại đa nhãn (Multi-label Classification) về bản chất và cách thiết kế lớp cuối cùng (Output Layer) của mạng nơ-ron.
* **expected_key_points:**
  - id: KP2_1
    content: Bản chất khác biệt
    keypoint_weight: 0.5
    description: Multi-class yêu cầu mỗi mẫu chỉ thuộc về duy nhất một lớp trong số nhiều lớp. Multi-label cho phép mỗi mẫu đồng thời thuộc về nhiều lớp khác nhau (hoặc không thuộc lớp nào).
  - id: KP2_2
    content: Thiết kế Output Layer và Activation
    keypoint_weight: 0.5
    description: Với Multi-class, lớp cuối dùng hàm kích hoạt Softmax để tạo phân phối xác suất tổng bằng 1. Với Multi-label, dùng hàm kích hoạt Sigmoid độc lập cho mỗi nơ-ron đầu ra để tính xác suất riêng lẻ của từng nhãn.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tăng cường dữ liệu (Data Augmentation) trong Computer Vision là gì? Nêu 3 kỹ thuật phổ biến và giải thích tại sao nó giúp tăng chất lượng mô hình.
* **expected_key_points:**
  - id: KP3_1
    content: Khái niệm Data Augmentation
    keypoint_weight: 0.4
    description: Là kỹ thuật tạo ra các mẫu dữ liệu huấn luyện mới bằng cách biến đổi ngẫu nhiên các ảnh gốc có sẵn mà không làm thay đổi nhãn của ảnh.
  - id: KP3_2
    content: Các kỹ thuật và vai trò
    keypoint_weight: 0.6
    description: Nêu được 3 kỹ thuật: Lật ảnh (Horizontal/Vertical Flip), Xoay ảnh (Rotation), Cắt ảnh ngẫu nhiên (Random Crop), hoặc Thay đổi độ sáng (Brightness jittering). Giúp mô hình tăng tính bất biến (invariance), giảm overfitting và học tốt hơn các biến thể dữ liệu thực tế.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích vai trò và cách thực hiện hai kỹ thuật căn chỉnh mô hình ngôn ngữ lớn (LLM Alignment): RLHF (Reinforcement Learning from Human Feedback) và DPO (Direct Preference Optimization).
* **expected_key_points:**
  - id: KP4_1
    content: Quy trình RLHF
    keypoint_weight: 0.5
    description: Huấn luyện mô hình Supervised Fine-Tuning (SFT) -> Huấn luyện một Reward Model dựa trên dữ liệu so sánh sở thích của con người -> Sử dụng thuật toán PPO (Proximal Policy Optimization) để tối ưu hóa mô hình SFT nhận phần thưởng lớn nhất từ Reward Model.
  - id: KP4_2
    content: Cải tiến của DPO
    keypoint_weight: 0.5
    description: DPO loại bỏ hoàn toàn việc huấn luyện Reward Model riêng biệt và việc chạy học tăng cường phức tạp. DPO tối ưu hóa trực tiếp mô hình ngôn ngữ trên dữ liệu sở thích (cặp câu trả lời được thích/không thích) bằng cách giải toán học trực tiếp qua hàm loss Cross-Entropy sửa đổi.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích sự khác biệt giữa hai thuật toán Q-Learning (Tabular) và Deep Q-Network (DQN) trong học tăng cường. Kỹ thuật Experience Replay trong DQN giải quyết vấn đề gì?
* **expected_key_points:**
  - id: KP5_1
    content: Q-Learning vs DQN
    keypoint_weight: 0.5
    description: Q-Learning sử dụng một bảng Q-table để lưu trữ giá trị Q cho mọi cặp trạng thái-hành động (chỉ dùng cho không gian trạng thái nhỏ). DQN thay thế Q-table bằng một mạng nơ-ron sâu (Function Approximator) để dự đoán giá trị Q cho không gian trạng thái lớn hoặc liên tục.
  - id: KP5_2
    content: Vai trò của Experience Replay
    keypoint_weight: 0.5
    description: Lưu trữ các trải nghiệm tương tác cũ vào một bộ nhớ đệm (replay buffer) và lấy mẫu ngẫu nhiên để huấn luyện mạng. Giải quyết vấn đề tự tương quan (autocorrelation) của các mẫu dữ liệu liên tiếp trong chuỗi và tăng tính ổn định của gradient.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh hai kiến trúc BERT (Autoregressive/Masked Language Model) và GPT (Causal Language Model) trong xử lý ngôn ngữ.
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế Attention bi-directional vs causal
    keypoint_weight: 0.6
    description: BERT cho phép các token chú ý đến cả các từ phía sau nhờ cơ chế Bidirectional, rất tốt cho các bài toán hiểu văn bản (NLU). GPT sử dụng Causal Masked Attention chặn nhìn các từ tương lai, phù hợp cho bài toán sinh chữ (NLG).
  - id: KP6_2
    content: Ứng dụng phù hợp
    keypoint_weight: 0.4
    description: BERT: Trích xuất thực thể NER, Phân loại văn bản, Trả lời câu hỏi (QA). GPT: Chatbot, viết code, viết báo cáo, sinh văn bản sáng tạo.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách giải quyết bài toán thiếu nhãn dữ liệu huấn luyện bằng hai phương pháp: Semi-supervised Learning (Học bán giám sát) và Active Learning (Học chủ động).
* **expected_key_points:**
  - id: KP7_1
    content: Nguyên lý Semi-supervised Learning
    keypoint_weight: 0.5
    description: Kết hợp lượng nhỏ dữ liệu có nhãn và lượng lớn dữ liệu không nhãn để huấn luyện mô hình (ví dụ dùng kỹ thuật Pseudo-labeling: dùng mô hình hiện tại dự đoán nhãn cho dữ liệu không nhãn, chọn các dự đoán tin cậy cao để nạp lại vào tập train).
  - id: KP7_2
    content: Nguyên lý Active Learning
    keypoint_weight: 0.5
    description: Là quy trình tương tác trong đó mô hình chủ động chọn ra các mẫu dữ liệu không nhãn khó nhất hoặc có độ không chắc chắn (uncertainty) cao nhất để yêu cầu con người (annotator) dán nhãn, giúp giảm tối đa số lượng nhãn cần dán mà vẫn đạt độ chính xác cao.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản huấn luyện một hệ thống điều khiển tự động (như Robot vượt chướng ngại vật hoặc Tối ưu hóa điều phối đèn tín hiệu giao thông) sử dụng Deep Reinforcement Learning.
* **expected_key_points:**
  - id: KP8_1
    content: Định nghĩa State space, Action space, và Reward function
    keypoint_weight: 0.6
    description: Thiết kế State space (ví dụ: khoảng cách tới xe xung quanh, tốc độ xe, độ dài hàng đợi). Action space (ví dụ: thời gian đèn xanh/đỏ cho mỗi làn). Reward function (ví dụ: phạt thời gian chờ trung bình, thưởng khi xe thoát nhanh).
  - id: KP8_2
    content: Lựa chọn thuật toán và đối phó rủi ro
    keypoint_weight: 0.4
    description: Sử dụng thuật toán học tăng cường liên tục như DDPG, PPO hoặc SAC; xây dựng môi trường giả lập (Simulation) an toàn để train agent trước khi deploy lên thực tế.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống trích xuất thông tin từ các tài liệu văn bản phi cấu trúc dạng ảnh quét (như hóa đơn, tờ khai hải quan) sử dụng mô hình học sâu đa phương thức (Multimodal Document AI) kết hợp Text và Vision.
* **expected_key_points:**
  - id: KP9_1
    content: Kiến trúc mô hình đa phương thức (Multimodal Architecture)
    keypoint_weight: 0.5
    description: Sử dụng các mô hình như LayoutLMv3 hoặc Donut. LayoutLMv3 học đồng thời 3 thông tin: Text (đọc từ OCR), Layout (tọa độ 2D của bounding box), và Vision (đặc trưng ảnh của từng vùng chữ). Donut là kiến trúc end-to-end không cần OCR, dùng ViT encoder ảnh và Transformer decoder để sinh trực tiếp cấu trúc JSON đầu ra.
  - id: KP9_2
    content: Xử lý dữ liệu huấn luyện và đánh giá
    keypoint_weight: 0.5
    description: Định nghĩa nhãn dạng khóa-giá trị, phân nhóm các nhãn; đánh giá bằng chỉ số F1-score cấp độ thực thể và độ chính xác JSON cấu trúc.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Hãy thiết kế cấu hình và tối ưu hóa hệ thống máy chủ Triton Inference Server để deploy đồng thời nhiều mô hình AI chạy song song, tận dụng tối đa phần cứng GPU.
* **expected_key_points:**
  - id: KP10_1
    content: Cấu hình Dynamic Batching và Concurrent Model Execution
    keypoint_weight: 0.6
    description: Kích hoạt cờ dynamic_batching trong file `config.pbtxt` để Triton tự động gộp các request đơn lẻ thành batch lớn trong cửa sổ thời gian mili-giây. Cấu hình instance_group để deploy nhiều bản sao (instances) của cùng một mô hình chạy song song trên GPU.
  - id: KP10_2
    content: Sử dụng định dạng tối ưu và Model Control
    keypoint_weight: 0.4
    description: Convert mô hình sang ONNX/TensorRT để tối ưu hóa thời gian chạy; sử dụng cơ chế Model Control API (EXPLICIT mode) để load/unload mô hình động mà không cần restart server, giúp tối ưu hóa dung lượng VRAM.

