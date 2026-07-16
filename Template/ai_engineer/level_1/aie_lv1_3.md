# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 1)

* **Role:** AI Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong bài toán tối ưu hóa bằng thuật toán Gradient Descent, đại lượng Learning Rate (Tốc độ học) đóng vai trò gì? Điều gì sẽ xảy ra nếu chọn giá trị Learning Rate quá lớn hoặc quá nhỏ?
* **expected_key_points:**
  - id: KP1_1
    content: Vai trò của Learning Rate làm kích thước bước đi (Step Size)
    keypoint_weight: 0.4
    description: Learning Rate là một siêu tham số (Hyperparameter) điều khiển kích thước của bước cập nhật trọng số theo hướng ngược chiều của gradient tại mỗi vòng lặp.
  - id: KP1_2
    content: Hệ quả khi chọn Learning Rate quá lớn
    keypoint_weight: 0.3
    description: Khi Learning Rate quá lớn, kích thước bước nhảy sẽ quá rộng, dẫn đến hiện tượng thuật toán bị dao động mạnh, vượt qua điểm tối ưu cục bộ (Overshooting) và có nguy cơ bị phân kỳ (Divergence).
  - id: KP1_3
    content: Hệ quả khi chọn Learning Rate quá nhỏ
    keypoint_weight: 0.3
    description: Khi Learning Rate quá nhỏ, mô hình sẽ thực hiện các bước cập nhật cực kỳ ngắn, làm tốc độ huấn luyện trở nên rất chậm, tốn tài nguyên tính toán và dễ bị kẹt ở các điểm tối ưu cục bộ tệ hoặc vùng yên ngựa.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy giải thích ý nghĩa toán học và mục đích sử dụng của hàm activation Softmax ở tầng đầu ra (Output layer) trong mạng nơ-ron sâu.
* **expected_key_points:**
  - id: KP2_1
    content: Chuyển đổi điểm số thô thành phân phối xác suất
    keypoint_weight: 0.5
    description: Softmax nén một vector chứa các điểm số thô (Logits) của các lớp đầu ra thành một vector chứa các giá trị số thực nằm trong khoảng (0, 1) có tổng bằng 1, đại diện cho một phân phối xác suất.
  - id: KP2_2
    content: Ngữ cảnh bài toán phân loại đa lớp (Multi-class Classification)
    keypoint_weight: 0.5
    description: Được sử dụng ở tầng cuối cùng của mô hình phân loại đa lớp loại trừ lẫn nhau (Mutually Exclusive), giúp xác định lớp nào có xác suất dự đoán cao nhất làm kết quả đầu ra.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao chúng ta cần phải chia tập dữ liệu ban đầu thành 3 tập độc lập: Training set, Validation set và Test set thay vì chỉ dùng một tập duy nhất?
* **expected_key_points:**
  - id: KP3_1
    content: Vai trò huấn luyện và điều chỉnh siêu tham số (Train & Validation)
    keypoint_weight: 0.5
    description: Training set được dùng trực tiếp để mô hình học và cập nhật trọng số (Weights/Biases). Validation set dùng để đánh giá mô hình trong lúc huấn luyện nhằm lựa chọn siêu tham số (Hyperparameters) và ngăn chặn Overfitting.
  - id: KP3_2
    content: Vai trò đánh giá độc lập cuối cùng của Test set
    keypoint_weight: 0.5
    description: Test set được giữ hoàn toàn độc lập và chỉ được mang ra sử dụng một lần duy nhất sau khi kếtthuấn luyện nhằm đánh giá năng lực tổng quát hóa (Generalization) khách quan của mô hình trên dữ liệu thực tế.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy phân biệt điểm khác nhau cốt lõi về mặt kiến trúc và cơ chế xử lý dữ liệu đầu vào giữa mạng nơ-ron tích chập (CNN) và mạng nơ-ron tuần hoàn (RNN).
* **expected_key_points:**
  - id: KP4_1
    content: Đặc trưng không gian của CNN (Spatial Features)
    keypoint_weight: 0.5
    description: CNN xử lý dữ liệu có cấu trúc lưới/không gian (như hình ảnh) bằng cách sử dụng các bộ lọc (Kernels) chia sẻ trọng số trượt trên ảnh, giúp trích xuất các đặc trưng mang tính bất biến vị trí.
  - id: KP4_2
    content: Đặc trưng tuần tự của RNN (Sequential Features)
    keypoint_weight: 0.5
    description: RNN thiết kế dành riêng cho dữ liệu chuỗi/thời gian (như văn bản, âm thanh) nhờ cơ chế kết nối phản hồi vòng lặp (Recurrent connections), cho phép lưu giữ trạng thái bộ nhớ (Hidden State) để truyền thông tin từ bước thời gian trước sang bước thời gian sau.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong bài toán phân loại (Classification), ma trận nhầm lẫn Confusion Matrix giúp Project Manager/Engineer tính toán được hai chỉ số F1-Score và ROC-AUC nhằm mục đích gì?
* **expected_key_points:**
  - id: KP5_1
    content: Bản chất trung bình điều hòa của F1-Score
    keypoint_weight: 0.5
    description: F1-Score là trung bình điều hòa (Harmonic Mean) giữa Precision và Recall, cung cấp một chỉ số đánh giá duy nhất cân bằng cả hai yếu tố, đặc biệt hữu ích khi làm việc trên tập dữ liệu mất cân bằng.
  - id: KP5_2
    content: Đo lường năng lực phân tách lớp của ROC-AUC
    keypoint_weight: 0.5
    description: ROC-AUC đo lường diện tích dưới đường cong biểu diễn mối quan hệ giữa True Positive Rate và False Positive Rate tại các ngưỡng phân loại khác nhau, thể hiện khả năng phân tách chính xác giữa hai lớp âm tính và dương tính của mô hình mà không phụ thuộc vào một ngưỡng cố định.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Kỹ thuật Transfer Learning (Học chuyển giao) hoạt động như thế nào trong Deep Learning? Khi nào chúng ta thực hiện Fine-tuning toàn bộ mô hình và khi nào chỉ đóng băng (Freeze) các tầng đặc trưng?
* **expected_key_points:**
  - id: KP6_1
    content: Tái sử dụng tri thức từ mô hình Pre-trained
    keypoint_weight: 0.4
    description: Tận dụng một mô hình đã được huấn luyện từ trước trên một tập dữ liệu khổng lồ (như ImageNet) để làm điểm xuất phát cho một bài toán mới có tập dữ liệu nhỏ hơn, giúp tiết kiệm thời gian và tài nguyên tính toán.
  - id: KP6_2
    content: Chiến lược đóng băng tầng đặc trưng (Feature Extraction)
    keypoint_weight: 0.3
    description: Áp dụng khi tập dữ liệu mới của ta rất nhỏ và có độ tương đồng cao với tập dữ liệu gốc; ta giữ nguyên trọng số của các tầng trích xuất đặc trưng nền tảng và chỉ huấn luyện lại tầng phân loại ở cuối.
  - id: KP6_3
    content: Chiến lược tinh chỉnh trọng số (Fine-tuning)
    keypoint_weight: 0.3
    description: Áp dụng khi tập dữ liệu mới đủ lớn hoặc có sự khác biệt lớn so với tập dữ liệu gốc; ta mở khóa và cho phép cập nhật lại trọng số của một số tầng sâu hoặc toàn bộ các tầng của mạng với một Learning Rate rất nhỏ.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Để kiểm soát và phạt độ phức tạp của mô hình nhằm giảm thiểu hiện tượng Overfitting, hai kỹ thuật Regularization L1 (Lasso) và L2 (Ridge) tác động toán học lên hàm mất mát (Loss Function) khác nhau như thế nào?
* **expected_key_points:**
  - id: KP7_1
    content: Cơ chế phạt toán học của L1 Regularization
    keypoint_weight: 0.5
    description: L1 cộng thêm tổng giá trị tuyệt đối của các trọng số (Norm L1) vào hàm mất mát. Kỹ thuật này có xu hướng ép các trọng số không quan trọng về bằng 0 tuyệt đối, tạo ra ma trận trọng số thưa thớt (Sparsity) và đóng vai trò như một bộ trọn lọc thuộc tính tự động.
  - id: KP7_2
    content: Cơ chế phạt toán học của L2 Regularization
    keypoint_weight: 0.5
    description: L2 cộng thêm tổng bình phương của các trọng số (Norm L2/Weight Decay) vào hàm mất mát. Kỹ thuật này phạt nặng các trọng số có giá trị lớn, ép chúng tiến dần về sát 0 nhưng không bằng 0 tuyệt đối, giúp phân bổ trọng số đều và làm mượt hàm dự đoán.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích cơ chế toán học cốt lõi của tầng Scaled Dot-Product Attention trong kiến trúc Multi-Head Attention của Transformer. Tại sao phép toán chia cho căn bậc hai của kích thước vector ($\sqrt{d_k}$) lại bắt buộc phải có?
* **expected_key_points:**
  - id: KP8_1
    content: Công thức toán học tính Attention Score
    keypoint_weight: 0.4
    description: Điểm số chú ý được tính bằng công thức $ \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V $, trong đó $Q, K, V$ là ma trận Query, Key, Value.
  - id: KP8_2
    content: Hiện tượng bão hòa hàm Softmax khi $d_k$ lớn
    keypoint_weight: 0.3
    description: Khi số chiều $d_k$ của vector rất lớn, tích vô hướng $QK^T$ sẽ có xu hướng nhận các giá trị có phương sai rất lớn, đẩy các giá trị này rơi vào các vùng có độ dốc cực nhỏ (vùng bão hòa) của hàm Softmax.
  - id: KP8_3
    content: Ổn định Gradient lúc Backpropagation
    keypoint_weight: 0.3
    description: Việc chia cho hệ số tỷ lệ $\sqrt{d_k}$ giúp kéo phương sai của tích vô hướng về bằng 1, giữ cho hàm Softmax hoạt động ở vùng có độ dốc tốt, từ đó ngăn chặn hiện tượng triệt tiêu đạo hàm (Vanishing Gradient) trong quá trình huấn luyện ngược.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong bài toán tối ưu hóa phân phối Generative Adversarial Networks (GAN), tại sao hàm mất mát Vanila GAN ban đầu dễ gặp hiện tượng sụp đổ chế độ (Mode Collapse)? Bản chất cơ chế hình học của Wasserstein GAN (WGAN) giải quyết lỗi này thế nào?
* **expected_key_points:**
  - id: KP9_1
    content: Bản chất Mode Collapse và giới hạn của Kullback-Leibler/JS Divergence
    keypoint_weight: 0.4
    description: Mode Collapse là hiện tượng mạng Generator chỉ học và sinh đi sinh lại một vài mẫu dữ liệu hẹp/an toàn mà bỏ qua toàn bộ sự đa dạng của phân phối thật. Nguyên nhân do Vanilla GAN dùng khoảng cách Jensen-Shannon (JS) để đo độ lệch; khi hai phân phối không chồng lấn, độ dốc gradient của JS biến mất (bằng 0), khiến Generator không có thông tin để học.
  - id: KP9_2
    content: Giải pháp đo khoảng cách bằng Earth Mover's Distance (EMD)
    keypoint_weight: 0.4
    description: WGAN thay thế khoảng cách JS bằng khoảng cách Wasserstein (Earth Mover's Distance). Khoảng cách này cung cấp một hàm đo lường khoảng cách liên tục và có đạo hàm dốc mượt mà ở mọi nơi, ngay cả khi hai phân phối nằm hoàn toàn tách rời nhau trong không gian hình học.
  - id: KP9_3
    content: Ràng buộc tính liên tục Lipschitz (Lipschitz Continuity)
    keypoint_weight: 0.2
    description: Để tính được khoảng cách Wasserstein, WGAN bắt buộc mạng Discriminator (lúc này gọi là Critic) phải thỏa mãn điều kiện ràng buộc toán học 1-Lipschitz continuity, thường được thực thi qua kỹ thuật Weight Clipping hoặc Gradient Penalty.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Khi huấn luyện một mô hình ngôn ngữ lớn (LLM) hoặc mạng nơ-ron sâu trên hệ thống phân tán đa GPU (Distributed Training), hãy phân tích sự khác nhau về cơ chế đồng bộ tham số giữa kỹ thuật Data Parallelism (DP) và Model Parallelism (MP).
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế phân mảnh dữ liệu của Data Parallelism (DP)
    keypoint_weight: 0.4
    description: Toàn bộ cấu trúc kiến trúc mô hình được sao chép nguyên vẹn giống nhau sang bộ nhớ của tất cả các GPU. Tập dữ liệu lớn (Batch) được chia nhỏ thành các Mini-batch phân phát cho từng GPU thực hiện Forward và Backward một cách độc lập song song.
  - id: KP10_2
    content: Cơ chế truyền thông đồng bộ All-Reduce trong DP
    keypoint_weight: 0.2
    description: After bước Backward, các GPU bắt buộc phải thực hiện giao tiếp truyền thông mạng thông qua thuật toán All-Reduce để tính toán trung bình cộng các gradient thu được, đồng bộ lại bộ trọng số trước khi bước vào epoch tiếp theo.
  - id: KP10_3
    content: Cơ chế phân mảnh kiến trúc của Model Parallelism (MP)
    keypoint_weight: 0.4
    description: Áp dụng khi mô hình quá lớn không thể nhét vừa một bộ nhớ VRAM của một GPU đơn lẻ. Cấu trúc mạng (các lớp hoặc các ma trận trọng số trong tầng Transformer) được cắt mảnh chia nhỏ ra để lưu trữ rải rác trên nhiều GPU khác nhau. Quá trình tính toán yêu cầu truyền thông tin tuần tự hoặc song song (như Tensor/Pipeline Parallelism) giữa các GPU tại từng tầng của mạng.