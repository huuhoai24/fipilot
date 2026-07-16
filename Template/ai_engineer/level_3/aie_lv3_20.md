# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 3) - Tập Đề SAC và Sim-to-Real RL (20)

* **Role:** AI Engineer
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong học tăng cường (Reinforcement Learning), phân biệt sự khác nhau về bản chất và hiệu năng giữa thuật toán On-Policy (như PPO) và Off-Policy (như DQN).
* **expected_key_points:**
  - id: KP1_1
    content: Bản chất On-Policy vs Off-Policy
    keypoint_weight: 0.5
    description: On-Policy yêu cầu Agent học trực tiếp từ các dữ liệu tương tác sinh ra bởi chính sách (policy) hiện tại. Off-Policy cho phép Agent học từ các dữ liệu lưu giữ trong bộ nhớ đệm (replay buffer) được sinh ra bởi các chính sách cũ hoặc hành động ngẫu nhiên khác.
  - id: KP1_2
    content: Hiệu quả sử dụng mẫu (Sample Efficiency)
    keypoint_weight: 0.5
    description: Off-Policy có hiệu quả sử dụng mẫu cao hơn nhiều lần do có thể tái sử dụng dữ liệu cũ nhiều lần để cập nhật trọng số; On-Policy phải loại bỏ dữ liệu cũ sau khi cập nhật chính sách.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Viết phương trình Bellman (Bellman Equation) cho hàm giá trị tối ưu $Q^*(s,a)$ và giải thích ý nghĩa toán học của từng thành phần.
* **expected_key_points:**
  - id: KP2_1
    content: Phương trình Bellman tối ưu cho Q-value
    keypoint_weight: 0.6
    description: Công thức: $Q^*(s,a) = R(s,a) + \gamma \sum_{s'} P(s'|s,a) \max_{a'} Q^*(s',a')$. hoặc dạng kỳ vọng $R_t + \gamma \max_{a'} Q(s_{t+1}, a')$.
  - id: KP2_2
    content: Ý nghĩa các thành phần
    keypoint_weight: 0.4
    description: $R(s,a)$ là phần thưởng tức thời. $\gamma$ là hệ số discount factor. $P(s'|s,a)$ là xác suất chuyển trạng thái của môi trường. $\max_{a'} Q^*(s',a')$ là giá trị tối ưu của bước tiếp theo.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích thách thức Phần thưởng thưa thớt (Sparse Reward Problem) trong học tăng cường. Nêu một ví dụ thực tế.
* **expected_key_points:**
  - id: KP3_1
    content: Bản chất Sparse Reward
    keypoint_weight: 0.5
    description: Xảy ra khi Agent chỉ nhận được phần thưởng khi hoàn thành toàn bộ mục tiêu dài hạn (ví dụ robot giải mê cung chỉ nhận thưởng khi thoát ra, phần lớn các hành động khác đều nhận reward = 0).
  - id: KP3_2
    content: Tác động đến quá trình học
    keypoint_weight: 0.5
    description: Agent đi lung tung ngẫu nhiên và không bao giờ tìm thấy phần thưởng để cập nhật chính sách; khiến mô hình không thể hội tụ.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích nguyên lý hoạt động của thuật toán SAC (Soft Actor-Critic) cho không gian hành động liên tục. Vai trò của thành phần Entropy Regularization trong hàm loss của SAC là gì?
* **expected_key_points:**
  - id: KP4_1
    content: Tối đa hóa Entropy Regularization
    keypoint_weight: 0.6
    description: SAC tối ưu hóa chính sách để đồng thời đạt phần thưởng cao nhất và có mức độ ngẫu nhiên (entropy) lớn nhất: $J(\pi) = \sum \mathbb{E} [R(s_t, a_t) + \alpha H(\pi(\cdot|s_t))]$ với $H$ là entropy của policy và $\alpha$ là hệ số điều chỉnh.
  - id: KP4_2
    content: Lợi ích của Entropy
    keypoint_weight: 0.4
    description: Khuyến khích Agent tích cực khám phá không gian hành động, tránh rơi vào tối ưu cục bộ, và giúp chính sách có tính tổng quát hóa tốt hơn khi môi trường thực tế thay đổi.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cơ chế hoạt động của thuật toán DDPG (Deep Deterministic Policy Gradient) và cách nó mở rộng từ DQN để xử lý không gian hành động liên tục.
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế Deterministic Policy của DDPG
    keypoint_weight: 0.5
    description: DDPG trực tiếp đầu ra một hành động cụ thể $a = \mu_\theta(s)$ thay vì phân phối xác suất. Sử dụng mạng Critic để ước lượng giá trị $Q(s, a)$ và cập nhật mạng Actor bằng cách tăng giá trị Q này.
  - id: KP5_2
    content: Tương đồng với DQN và Target Networks
    keypoint_weight: 0.5
    description: Sử dụng replay buffer để học off-policy và sử dụng Target Networks cập nhật chậm (soft updates: $\theta' \leftarrow \tau \theta + (1-\tau)\theta'$) để giữ quá trình huấn luyện ổn định.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày các phương pháp giải quyết bài toán Sparse Reward sử dụng kỹ thuật Hindsight Experience Replay (HER) và tạo hình phần thưởng (Reward Shaping).
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế hoạt động của HER
    keypoint_weight: 0.6
    description: HER lưu trữ các trải nghiệm thất bại vào replay buffer nhưng giả định mục tiêu thực tế đạt được là một mục tiêu ảo (virtual goal), dạy Agent cách đạt được các điểm mốc trung gian dù nó không hoàn thành nhiệm vụ chính.
  - id: KP6_2
    content: Cơ chế của Reward Shaping
    keypoint_weight: 0.4
    description: Tự thiết kế thêm các phần thưởng phụ (heuristic rewards) để định hướng Agent (ví dụ thưởng khi khoảng cách tới mục tiêu ngắn lại); cần cẩn thận để tránh Agent tìm kẽ hở tối đa hóa reward phụ mà không làm task chính.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích các kỹ thuật mô phỏng môi trường vật lý (Physics Simulation) sử dụng NVIDIA Isaac Gym để huấn luyện robot song song quy mô lớn.
* **expected_key_points:**
  - id: KP7_1
    content: Ưu thế huấn luyện song song trên GPU (End-to-End GPU simulation)
    keypoint_weight: 0.6
    description: Isaac Gym chạy giả lập vật lý và tính toán mô hình RL trên cùng một GPU, loại bỏ bước truyền tải dữ liệu chậm từ CPU sang GPU. Cho phép chạy đồng thời hàng ngàn môi trường robot song song.
  - id: KP7_2
    content: Lợi ích về thời gian huấn luyện
    keypoint_weight: 0.4
    description: Giảm thời gian huấn luyện các tác vụ robot phức tạp (như học đi, gắp đồ) từ nhiều tuần xuống còn vài giờ.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống điều khiển cánh tay robot gắp sản phẩm lỗi (Robot Grasping) trong nhà máy tự động hóa sử dụng học tăng cường Sim-to-Real. Làm thế nào để giải quyết sự lệch pha giữa mô phỏng và thực tế (Reality Gap)?
* **expected_key_points:**
  - id: KP8_1
    content: Áp dụng kỹ thuật Domain Randomization
    keypoint_weight: 0.5
    description: Randomization ngẫu nhiên hóa các thông số vật lý trong môi trường giả lập (khối lượng vật, độ ma sát, lực đẩy) và thông số hình ảnh (ánh sáng, camera noise) để Agent học chính sách có tính bất biến cao.
  - id: KP8_2
    content: Domain Adaptation và Fine-tuning thực tế
    keypoint_weight: 0.5
    description: Sử dụng mô hình chuyển đổi đặc trưng ảnh từ thật sang giả lập (như CycleGAN) hoặc thực hiện fine-tune cục bộ mô hình RL trên robot thật bằng một lượng nhỏ dữ liệu thực tế an toàn.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống điều phối hệ thống đèn tín hiệu giao thông thông minh cho toàn thành phố sử dụng học tăng cường đa tác nhân (Multi-Agent Reinforcement Learning - MARL).
* **expected_key_points:**
  - id: KP9_1
    content: Định nghĩa các tác nhân và Môi trường phân tán
    keypoint_weight: 0.5
    description: Mỗi nút giao thông là một Agent. State gồm hàng đợi xe và tốc độ trung bình. Action là thời gian đèn xanh cho các hướng. Reward là giảm thiểu tổng thời gian chờ của xe.
  - id: KP9_2
    content: Cơ chế giao tiếp và gộp (Cooperative MARL)
    keypoint_weight: 0.5
    description: Sử dụng thuật toán QMIX hoặc MAPPO: thiết lập mạng gộp giá trị Q của các agents (Mixing Network) để tối ưu hóa hàm lợi ích chung của toàn thành phố, tránh việc các nút cạnh tranh cục bộ gây tắc nghẽn dây chuyền.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống giao dịch chứng khoán phái sinh tự động (Algorithmic Trading Agent) sử dụng thuật toán PPO kết hợp quản lý rủi ro VaR (Value at Risk) trong hàm loss.
* **expected_key_points:**
  - id: KP10_1
    content: Thiết kế State, Action và Reward y khoa tài chính
    keypoint_weight: 0.6
    description: State space gồm: chuỗi nến giá lịch sử, các chỉ báo kỹ thuật (RSI, MACD), vị thế tài khoản hiện tại. Action space: Mua (Buy), Bán (Sell), hoặc Đứng ngoài (Hold). Reward: Tỷ lệ lợi nhuận ròng điều chỉnh theo rủi ro (như Sharpe Ratio hoặc Sortino Ratio) kết hợp hình phạt nặng dựa trên mức sụt giảm tài sản tối đa (Max Drawdown).
  - id: KP10_2
    content: Đối phó rủi ro Overfitting trên dữ liệu lịch sử
    keypoint_weight: 0.4
    description: Sử dụng kỹ thuật train trên môi trường giả lập có thêm nhiễu thị trường (Market Simulator), áp dụng phí giao dịch thực tế (transaction cost) khi tính toán reward để tránh việc agent giao dịch quá nhiều lần gây lãng phí phí giao dịch.

