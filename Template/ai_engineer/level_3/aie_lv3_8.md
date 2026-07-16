# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 3) - Tập Đề Reinforcement Learning và PPO (8)

* **Role:** AI Engineer
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong học tăng cường (Reinforcement Learning), hãy phân biệt ý nghĩa và vai trò của hai khái niệm: Policy (Chính sách) và Value Function (Hàm giá trị).
* **expected_key_points:**
  - id: KP1_1
    content: Khái niệm Policy
    keypoint_weight: 0.5
    description: Là chiến lược/hành vi của Agent, ánh xạ từ trạng thái (state) sang phân phối xác suất các hành động (actions) có thể thực hiện: $\pi(a|s)$.
  - id: KP1_2
    content: Khái niệm Value Function
    keypoint_weight: 0.5
    description: Dự đoán tổng phần thưởng tích lũy (expected cumulative reward) mà Agent có thể nhận được trong tương lai nếu bắt đầu từ một trạng thái $s$ và tuân theo policy hiện tại.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa hai nhánh thuật toán: Model-based Reinforcement Learning và Model-free Reinforcement Learning.
* **expected_key_points:**
  - id: KP2_1
    content: Đặc trưng Model-based RL
    keypoint_weight: 0.5
    description: Agent cố gắng xây dựng/học một mô hình giả lập của môi trường (hiểu được quy luật chuyển đổi trạng thái và reward) để lập kế hoạch trước khi thực hiện hành động thực tế.
  - id: KP2_2
    content: Đặc trưng Model-free RL
    keypoint_weight: 0.5
    description: Agent không cần hiểu hay xây dựng mô hình môi trường; học trực tiếp từ các tương tác thử-sai thực tế (ví dụ Q-learning, Policy Gradient). Tiết kiệm công sức xây dựng model nhưng tốn nhiều mẫu tương tác hơn.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Thuật toán Q-learning hoạt động như thế nào? Hãy viết công thức cập nhật giá trị Q-value và giải thích ý nghĩa các tham số.
* **expected_key_points:**
  - id: KP3_1
    content: Nguyên lý hoạt động của Q-learning
    keypoint_weight: 0.4
    description: Là thuật toán model-free, off-policy học giá trị tối ưu của các cặp trạng thái-hành động sử dụng phương trình Bellman để hội tụ.
  - id: KP3_2
    content: Công thức cập nhật Q-value
    keypoint_weight: 0.6
    description: Công thức: $Q(s,a) \leftarrow Q(s,a) + \alpha [R + \gamma \max_{a'} Q(s',a') - Q(s,a)]$. Siêu tham số $\alpha$ là learning rate, $\gamma$ là discount factor (hệ số giảm giá trị phần thưởng tương lai).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích sự khác biệt giữa thuật toán Policy Gradient và Q-learning (Value-based). Khi nào nên ưu tiên chọn Policy Gradient?
* **expected_key_points:**
  - id: KP4_1
    content: Policy Gradient vs Q-learning
    keypoint_weight: 0.5
    description: Q-learning tối ưu hóa gián tiếp bằng cách học giá trị hành động Q rồi chọn hành động max. Policy Gradient tối ưu hóa trực tiếp các tham số của policy $\pi_\theta(a|s)$ bằng cách tăng xác suất của các hành động mang lại phần thưởng cao.
  - id: KP4_2
    content: Trường hợp ưu tiên dùng Policy Gradient
    keypoint_weight: 0.5
    description: Ưu tiên chọn Policy Gradient khi không gian hành động là liên tục (continuous action space - ví dụ góc quay vô lăng, lực đẩy robot), hoặc khi bài toán yêu cầu một chính sách ngẫu nhiên tối ưu (stochastic policy).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cơ chế hoạt động của thuật toán PPO (Proximal Policy Optimization). Tại sao PPO giúp quá trình huấn luyện học tăng cường ổn định hơn so với TRPO?
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế Clipped Surrogate Objective của PPO
    keypoint_weight: 0.6
    description: PPO tối ưu hóa hàm loss giới hạn sự thay đổi của policy mới so với policy cũ bằng cách kẹp tỷ lệ xác suất $r_t(\theta)$ trong khoảng $[1-\epsilon, 1+\epsilon]$: $L^{CLIP}(\theta) = \hat{\mathbb{E}}_t [\min(r_t(\theta)\hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t)]$.
  - id: KP5_2
    content: Lý do huấn luyện ổn định
    keypoint_weight: 0.4
    description: Giúp ngăn chặn việc cập nhật trọng số quá lớn làm hỏng hoàn toàn policy đang học (vấn đề nhạy cảm của RL), chạy nhanh và dễ cài đặt hơn nhiều so với TRPO.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh cơ chế hoạt động của thuật toán Actor-Critic và Deep Q-Network (DQN).
* **expected_key_points:**
  - id: KP6_1
    content: Kiến trúc kết hợp Actor-Critic
    keypoint_weight: 0.6
    description: Actor-Critic kết hợp cả hai nhánh: Actor (đóng vai trò policy, quyết định hành động) và Critic (đóng vai trò value function, đánh giá hành động của Actor bằng cách tính toán hàm giá trị $V(s)$ hoặc $Q(s,a)$).
  - id: KP6_2
    content: So sánh với DQN
    keypoint_weight: 0.4
    description: DQN là thuần value-based, chỉ học hàm Q và chọn hành động rời rạc bằng cách argmax. Actor-Critic có thể tối ưu hiệu quả trên cả không gian hành động liên tục và giảm phương sai (variance) tốt hơn so với thuần Policy Gradient.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích thách thức Exploration (Khám phá) vs Exploitation (Khai thác) trong học tăng cường. Nêu cách giải quyết sử dụng phương pháp $\epsilon$-greedy và UCB (Upper Confidence Bound).
* **expected_key_points:**
  - id: KP7_1
    content: Thách thức Exploration vs Exploitation
    keypoint_weight: 0.5
    description: Exploration là thử các hành động mới để tìm kiếm phần thưởng tốt hơn trong tương lai. Exploitation là chọn hành động hiện tại đang có điểm thưởng cao nhất. Cần cân bằng để tránh tối ưu cục bộ.
  - id: KP7_2
    content: Cơ chế Epsilon-greedy và UCB
    keypoint_weight: 0.5
    description: $\epsilon$-greedy chọn ngẫu nhiên hành động mới với xác suất $\epsilon$, và chọn hành động tốt nhất với xác suất $1-\epsilon$. UCB chọn hành động dựa trên giá trị ước lượng cộng với độ bất định (uncertainty) của hành động đó, ưu tiên khám phá các hành động ít được thử nghiệm.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản huấn luyện một Agent tự lái xe trong môi trường giả lập (Autonomous Driving Simulation) sử dụng các thuật toán Deep Reinforcement Learning kết hợp thông tin cảm biến đa nguồn (Sensor Fusion).
* **expected_key_points:**
  - id: KP8_1
    content: Đặc trưng đầu vào đa nguồn (State Space)
    keypoint_weight: 0.5
    description: Tích hợp ảnh camera (qua mạng CNN/ViT lấy đặc trưng không gian), dữ liệu mây điểm LiDAR (qua PointNet trích xuất khoảng cách vật cản) và thông số xe (tốc độ, góc lái).
  - id: KP8_2
    content: Thiết kế hàm thưởng (Reward Function) và thuật toán
    keypoint_weight: 0.5
    description: Thưởng khi xe đi đúng làn và giữ tốc độ ổn định; phạt nặng khi va chạm (collision), đi chệch làn, hoặc phanh gấp liên tục. Sử dụng thuật toán học tăng cường liên tục như DDPG, PPO hoặc SAC để kiểm soát tay lái và chân ga mượt mà.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp tối ưu hóa năng lượng cho hệ thống HVAC (Sưởi, thông gió, điều hòa) trong tòa nhà thông minh sử dụng Deep Reinforcement Learning.
* **expected_key_points:**
  - id: KP9_1
    content: Định nghĩa môi trường học và biến số
    keypoint_weight: 0.5
    description: State space gồm: nhiệt độ trong phòng, nhiệt độ môi trường ngoài, độ ẩm, số lượng người hiện tại. Action space: điều chỉnh công suất làm lạnh/sưởi của các máy điều hòa. Reward: cân bằng giữa lượng điện năng tiêu thụ (phạt khi dùng nhiều điện) và độ thoải mái của con người (phạt khi nhiệt độ lệch xa mức tối ưu).
  - id: KP9_2
    content: Xử lý tính an toàn (Safe RL) và triển khai
    keypoint_weight: 0.5
    description: Do không thể train thử-sai trực tiếp trên tòa nhà thật (gây hỏng thiết bị), ta xây dựng mô hình nhiệt động lực học tòa nhà (EnergyPlus) làm môi trường giả lập để train Agent; áp dụng các ràng buộc an toàn (Safety constraints) để chặn các hành động thay đổi công suất đột ngột của Agent.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống giao dịch tài chính tự động (Algorithmic Trading Agent) sử dụng học tăng cường sâu để tối đa hóa lợi nhuận và quản lý rủi ro sụt giảm tài sản (Drawdown).
* **expected_key_points:**
  - id: KP10_1
    content: Thiết kế State, Action và Reward y khoa tài chính
    keypoint_weight: 0.6
    description: State space gồm: chuỗi nến giá lịch sử, các chỉ báo kỹ thuật (RSI, MACD), vị thế tài khoản hiện tại. Action space: Mua (Buy), Bán (Sell), hoặc Đứng ngoài (Hold). Reward: Tỷ lệ lợi nhuận ròng điều chỉnh theo rủi ro (như Sharpe Ratio hoặc Sortino Ratio) kết hợp hình phạt nặng dựa trên mức sụt giảm tài sản tối đa (Max Drawdown).
  - id: KP10_2
    content: Đối phó rủi ro Overfitting trên dữ liệu lịch sử
    keypoint_weight: 0.4
    description: Sử dụng kỹ thuật train trên môi trường giả lập có thêm nhiễu thị trường (Market Simulator), áp dụng phí giao dịch thực tế (transaction cost) khi tính toán reward để tránh việc agent giao dịch quá nhiều lần gây lãng phí phí giao dịch.

