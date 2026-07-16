# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 4) - Tập Đề Federated Learning và Privacy-Preserving AI (19)

* **Role:** AI Engineer
* **Level:** Level 4
* **Experience:** 6 - 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Học liên hợp (Federated Learning) là gì? Tại sao phương pháp này lại là xu hướng giải quyết bài toán quyền riêng tư dữ liệu?
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa Federated Learning
    keypoint_weight: 0.5
    description: Là kỹ thuật huấn luyện mô hình học máy phân tán trên nhiều thiết bị client (điện thoại, bệnh viện) chứa dữ liệu cục bộ, không cần thu thập dữ liệu thô về máy chủ trung tâm.
  - id: KP1_2
    content: Giải quyết quyền riêng tư dữ liệu
    keypoint_weight: 0.5
    description: Dữ liệu cá nhân nhạy cảm luôn nằm an toàn trên thiết bị của người dùng; chỉ có các cập nhật trọng số mô hình (gradients/parameters) được truyền đi.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau về bản chất dữ liệu đầu vào giữa Horizontal Federated Learning và Vertical Federated Learning.
* **expected_key_points:**
  - id: KP2_1
    content: Horizontal Federated Learning (Lọc ngang)
    keypoint_weight: 0.5
    description: Các thiết bị client chia sẻ cùng một tập các đặc trưng (features) nhưng sở hữu các mẫu người dùng khác nhau (ví dụ: các ứng dụng bàn phím trên điện thoại khác nhau).
  - id: KP2_2
    content: Vertical Federated Learning (Lọc dọc)
    keypoint_weight: 0.5
    description: Các client sở hữu các đặc trưng khác nhau của cùng một nhóm người dùng chung (ví dụ: một ngân hàng và một công ty thương mại điện tử ở cùng một thành phố hợp tác train mô hình chấm điểm tín dụng).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy giải thích khái niệm Bảo mật vi phân (Differential Privacy) và vai trò của cơ chế thêm nhiễu (Noise Addition) trong việc bảo vệ dữ liệu huấn luyện.
* **expected_key_points:**
  - id: KP3_1
    content: Định nghĩa Differential Privacy (DP)
    keypoint_weight: 0.5
    description: Là khung toán học đảm bảo kết quả đầu ra của thuật toán/mô hình ít thay đổi dù có hay không có sự xuất hiện của bất kỳ một cá nhân cụ thể nào trong tập dữ liệu.
  - id: KP3_2
    content: Cơ chế thêm nhiễu (Noise Addition)
    keypoint_weight: 0.5
    description: Thêm nhiễu ngẫu nhiên (Gauss hoặc Laplace) vào gradient trong quá trình huấn luyện cục bộ để ngăn chặn kẻ tấn công suy dịch ngược thông tin cá nhân từ trọng số mô hình.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích chi tiết cơ chế hoạt động của thuật toán Federated Averaging (FedAvg). Tại sao thuật toán FedProx lại vượt trội hơn FedAvg khi huấn luyện trên dữ liệu không đồng nhất (Non-IID)?
* **expected_key_points:**
  - id: KP4_1
    content: Nguyên lý hoạt động của FedAvg
    keypoint_weight: 0.5
    description: Server gửi mô hình gốc cho các clients -> các clients train cục bộ $E$ epochs -> gửi trọng số mới về server -> server tính trung bình cộng trọng số để cập nhật mô hình gốc và lặp lại vòng tiếp theo.
  - id: KP4_2
    content: Cải tiến của FedProx cho dữ liệu Non-IID
    keypoint_weight: 0.5
    description: Khi dữ liệu Non-IID, FedAvg dễ bị phân kỳ. FedProx bổ sung một số hạng phạt (Proximal Term) vào hàm loss cục bộ để ràng buộc trọng số mới của client không được lệch quá xa so với mô hình gốc từ server, giúp hội tụ ổn định.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế cơ chế Secure Aggregation (mã hóa đa bên MPC) đảm bảo máy chủ trung tâm (Server) không thể đọc được trọng số cập nhật của từng client riêng lẻ trong Federated Learning.
* **expected_key_points:**
  - id: KP5_1
    content: Mã hóa bằng mặt nạ ngẫu nhiên (Pairwise Masking)
    keypoint_weight: 0.6
    description: Các cặp client tự thỏa thuận các khóa chung ngẫu nhiên và cộng mặt nạ này vào trọng số của mình trước khi gửi lên server. Mặt nạ được thiết kế sao cho khi server cộng tổng trọng số của tất cả các clients, các mặt nạ ngẫu nhiên này tự triệt tiêu lẫn nhau hoàn toàn.
  - id: KP5_2
    content: Xử lý lỗi rớt mạng của client (Drop-out handling)
    keypoint_weight: 0.4
    description: Sử dụng kỹ thuật chia sẻ bí mật Shamir (Shamir's Secret Sharing) để server có thể khôi phục các mặt nạ của các clients bị mất kết nối giữa chừng mà không làm rò rỉ dữ liệu.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy giải thích cách áp dụng kỹ thuật Differential Privacy vào quá trình huấn luyện mô hình học sâu cục bộ sử dụng thuật toán DP-SGD (Differentially Private SGD).
* **expected_key_points:**
  - id: KP6_1
    content: Hai bước cốt lõi của DP-SGD
    keypoint_weight: 0.6
    description: Bước 1: Giới hạn chuẩn gradient (Gradient Clipping) để tránh một mẫu dữ liệu cá biệt làm thay đổi quá mạnh trọng số. Bước 2: Thêm nhiễu Gauss ngẫu nhiên vào gradient đã cắt trước khi thực hiện cập nhật trọng số mô hình.
  - id: KP6_2
    content: Đo lường ngân sách bảo mật (Privacy Budget)
    keypoint_weight: 0.4
    description: Theo dõi lượng thông tin rò rỉ qua các tham số $\epsilon$ (epsilon) và $\delta$ (delta); dừng huấn luyện khi ngân sách bảo mật đạt ngưỡng quy định để tránh rò rỉ.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích các nguy cơ tấn công bảo mật phổ biến trong hệ thống Federated Learning: Phân biệt Model Poisoning Attack và Membership Inference Attack.
* **expected_key_points:**
  - id: KP7_1
    content: Tấn công đầu độc mô hình (Model Poisoning)
    keypoint_weight: 0.5
    description: Kẻ tấn công giả danh client gửi các trọng số sai lệch lên server nhằm làm hỏng độ chính xác của mô hình hoặc cài cắm cửa sau (backdoor) để mô hình phân loại sai các mẫu định trước.
  - id: KP7_2
    content: Tấn công suy luận thành viên (Membership Inference)
    keypoint_weight: 0.5
    description: Kẻ tấn công quan sát đầu ra hoặc loss của mô hình để suy dịch ngược xem một mẫu dữ liệu cá nhân cụ thể có nằm trong tập dữ liệu huấn luyện cục bộ của client hay không.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống Federated Learning huấn luyện mô hình chẩn đoán ung thư từ hình ảnh X-quang phổi phân tán qua 10 bệnh viện lớn, đảm bảo không chia sẻ ảnh gốc và đối phó tốt với việc mất kết nối mạng (network dropouts).
* **expected_key_points:**
  - id: KP8_1
    content: Kiến trúc Pipeline huấn luyện phân tán
    keypoint_weight: 0.5
    description: Thiết lập cụm server trung tâm điều phối bằng framework Flower hoặc PySyft. Thiết lập các worker node tại mỗi bệnh viện; huấn luyện mô hình CNN (DenseNet) cục bộ bằng dữ liệu ảnh phổi của riêng viện đó.
  - id: KP8_2
    content: Cơ chế gộp không đồng bộ và bảo mật
    keypoint_weight: 0.5
    description: Sử dụng thuật toán gộp không đồng bộ (Asynchronous Aggregation) để server không phải chờ đợi các viện bị lag mạng; tích hợp Secure Aggregation và DP-SGD để bảo vệ tối đa dữ liệu bệnh nhân.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống Federated Learning huấn luyện mô hình dự đoán từ tiếp theo trên bàn phím di động của hàng triệu người dùng, tối ưu hóa băng thông mạng truyền tải của thiết bị di động.
* **expected_key_points:**
  - id: KP9_1
    content: Nén trọng số mô hình khi truyền tải (Model Compression)
    keypoint_weight: 0.6
    description: Áp dụng kỹ thuật nén gradient (gradient quantization) xuống 1-bit hoặc 2-bit, và sử dụng cơ chế thưa hóa (Sparsification) chỉ gửi 10% các tham số có thay đổi lớn nhất về server để giảm dung lượng mạng truyền tải.
  - id: KP9_2
    content: Cấu hình trigger huấn luyện cục bộ
    keypoint_weight: 0.4
    description: Chỉ kích hoạt huấn luyện cục bộ khi điện thoại của người dùng ở trạng thái sạc pin, kết nối Wifi, và không sử dụng (idle) để tránh làm hao pin và ảnh hưởng đến trải nghiệm người dùng.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp Mã hóa đồng cấu (Homomorphic Encryption) cho phép server bên thứ ba chạy suy luận mô hình phân loại nợ xấu trực tiếp trên dữ liệu tài chính đã được mã hóa của người dùng.
* **expected_key_points:**
  - id: KP10_1
    content: Nguyên lý Mã hóa đồng cấu (Fully Homomorphic Encryption - FHE)
    keypoint_weight: 0.5
    description: Cho phép thực hiện các phép toán cộng và nhân trực tiếp trên bản mã (ciphertext) mà không cần giải mã. Kết quả tính toán sau khi giải mã bởi client trùng khớp với kết quả tính toán trên bản rõ.
  - id: KP10_2
    content: Thiết kế mô hình AI tương thích FHE
    keypoint_weight: 0.5
    description: Do FHE chỉ hỗ trợ các phép toán cộng và nhân, ta phải xấp xỉ các hàm kích hoạt phi tuyến (như Sigmoid, ReLU) thành các hàm đa thức (polynomial approximation) và nén mô hình để giảm thiểu thời gian tính toán của FHE.

