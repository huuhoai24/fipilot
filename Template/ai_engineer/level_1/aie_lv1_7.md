# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 1)

* **Role:** AI Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong bài toán tối ưu hóa mạng nơ-ron bằng Gradient Descent, đại lượng Learning Rate (Tốc độ học) đóng vai trò gì và hệ quả khi chọn giá trị này quá lớn là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Kích thước bước đi (Step size) trong cập nhật tham số
    keypoint_weight: 0.5
    description: Learning Rate là một siêu tham số điều khiển kích thước của bước cập nhật trọng số ngược chiều gradient để tìm điểm tối ưu của hàm mất mát.
  - id: KP1_2
    content: Hiện tượng dao động mạnh hoặc phân kỳ (Overshooting/Divergence)
    keypoint_weight: 0.5
    description: Nếu Learning Rate quá lớn, bước nhảy sẽ quá rộng khiến thuật toán nhảy qua lại giữa các vách đồ thị, không thể hội tụ (Overshooting) và có nguy cơ làm phình to hàm loss (Divergence).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Hàm kích hoạt Softmax thường được sử dụng ở tầng nào của mạng nơ-ron sâu và vai trò toán học của nó trong bài toán phân loại là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Vị trí tại tầng đầu ra (Output Layer) của bài toán phân loại đa lớp
    keypoint_weight: 0.4
    description: Softmax được đặt ở tầng cuối cùng của mô hình phân loại đa lớp mang tính chất loại trừ lẫn nhau (Multi-class Classification).
  - id: KP2_2
    content: Chuẩn hóa điểm thô thành phân phối xác suất
    keypoint_weight: 0.6
    description: Softmax nén một vector chứa các điểm số thô (Logits) thành một vector chứa các số thực nằm trong khoảng (0, 1) có tổng bằng 1, đại diện cho phân phối xác suất dự đoán của các lớp.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao việc chia tập dữ liệu ban đầu thành 3 tập riêng biệt: Training set, Validation set và Test set lại mang tính bắt buộc khi xây dựng mô hình học máy?
* **expected_key_points:**
  - id: KP3_1
    content: Vai trò của tập Huấn luyện (Train) và tập Tối ưu (Validation)
    keypoint_weight: 0.5
    description: Training set dùng để mô hình học trực tiếp và cập nhật trọng số. Validation set dùng để đánh giá độc lập trong lúc huấn luyện nhằm lựa chọn siêu tham số và phát hiện sớm Overfitting.
  - id: KP3_2
    content: Tính khách quan kiểm thử cuối cùng của Test set
    keypoint_weight: 0.5
    description: Test set được giữ bảo mật hoàn toàn, chỉ mang ra chạy một lần duy nhất sau khi hoàn thành huấn luyện để đánh giá năng lực tổng quát hóa khách quan của mô hình trên dữ liệu thực tế.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy phân biệt điểm khác biệt cốt lõi về mặt kiến trúc xử lý dữ liệu đầu vào giữa mạng nơ-ron tích chập (CNN) và mạng nơ-ron tuần hoàn (RNN).
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế trích xuất đặc trưng không gian (Spatial) của CNN
    keypoint_weight: 0.5
    description: CNN sử dụng các bộ lọc (Kernels) chia sẻ trọng số trượt qua dữ liệu dạng lưới (như hình ảnh) để trích xuất các đặc trưng không gian mang tính bất biến vị trí.
  - id: KP4_2
    content: Cơ chế trạng thái ẩn lưu giữ thông tin tuần tự (Sequential) của RNN
    keypoint_weight: 0.5
    description: RNN sử dụng các liên kết vòng lặp phản hồi để truyền trạng thái ẩn (Hidden State) qua từng bước thời gian, chuyên dùng để xử lý chuỗi dữ liệu có tính phụ thuộc thời gian (văn bản, âm thanh).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi đánh giá một mô hình phân loại (Classification), tại sao chỉ số F1-Score và chỉ số ROC-AUC lại đáng tin cậy hơn chỉ số Accuracy (Độ chính xác tổng thể) nếu tập dữ liệu bị mất cân bằng nghiêm trọng?
* **expected_key_points:**
  - id: KP5_1
    content: Khuyết điểm bị thao túng của Accuracy khi dữ liệu lệch
    keypoint_weight: 0.3
    description: Accuracy sẽ cực kỳ cao nếu tập dữ liệu bị lệch (ví dụ 99% âm tính), mô hình chỉ cần đoán bừa toàn bộ âm tính vẫn đạt 99% accuracy mà không có giá trị phân loại thực tế.
  - id: KP5_2
    content: Bản chất trung bình điều hòa của F1-Score
    keypoint_weight: 0.3
    description: F1-Score kết hợp cân bằng cả Precision (giảm thiểu False Positive) và Recall (giảm thiểu False Negative) bằng phép tính trung bình điều hòa, giúp phản ánh đúng năng lực nhận diện trên nhóm thiểu số.
  - id: KP5_3
    content: Khả năng phân tách lớp không phụ thuộc ngưỡng của ROC-AUC
    keypoint_weight: 0.4
    description: ROC-AUC đo lường diện tích dưới đường cong biểu diễn mối quan hệ giữa True Positive Rate và False Positive Rate tại tất cả các ngưỡng phân loại, thể hiện năng lực phân tách lớp tổng thể của mô hình.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Kỹ thuật Học chuyển giao (Transfer Learning) hoạt động như thế nào trong Deep Learning? Khi nào chúng ta nên áp dụng chiến lược đóng băng (Freeze) các tầng đặc trưng?
* **expected_key_points:**
  - id: KP6_1
    content: Tái sử dụng tri thức từ mô hình Pre-trained lớn
    keypoint_weight: 0.5
    description: Tận dụng một mô hình đã được huấn luyện thành công từ trước trên một tập dữ liệu khổng lồ (như ImageNet) làm điểm xuất phát cho bài toán mới, giúp tiết kiệm thời gian và tài nguyên tính toán.
  - id: KP6_2
    content: Chiến lược đóng băng (Freeze) khi dữ liệu mới nhỏ và tương đồng
    keypoint_weight: 0.5
    description: Khi tập dữ liệu mới của ta có quy mô rất nhỏ và có độ tương đồng đặc trưng cao với tập dữ liệu gốc, ta giữ nguyên trọng số của các tầng trích xuất đặc trưng nền tảng và chỉ huấn luyện lại tầng phân loại ở cuối để tránh Overfitting.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Để giảm thiểu hiện tượng quá khớp (Overfitting), hai kỹ thuật Regularization L1 (Lasso) và L2 (Ridge) tác động hình học toán học lên các trọng số (Weights) khác nhau như thế nào?
* **expected_key_points:**
  - id: KP7_1
    content: Cơ chế ép trọng số về 0 tuyệt đối của L1 (Sparsity)
    keypoint_weight: 0.5
    description: L1 cộng thêm tổng giá trị tuyệt đối của các trọng số vào hàm loss, có xu hướng loại bỏ các thuộc tính không quan trọng bằng cách ép trọng số của chúng về bằng 0 tuyệt đối (tạo ra ma trận thưa).
  - id: KP7_2
    content: Cơ chế thu nhỏ đều trọng số sát 0 của L2 (Weight Decay)
    keypoint_weight: 0.5
    description: L2 cộng thêm tổng bình phương của các trọng số vào hàm loss, phạt nặng các trọng số có giá trị lớn, ép chúng nhỏ dần về sát 0 nhưng không bằng 0 tuyệt đối, giúp làm mượt đồ thị dự đoán.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích công thức toán học cốt lõi của tầng Scaled Dot-Product Attention trong kiến trúc Multi-Head Attention của Transformer. Tại sao phép toán chia cho $\sqrt{d_k}$ lại bắt buộc phải có?
* **expected_key_points:**
  - id: KP8_1
    content: Công thức toán học tổng quát tính Attention Score
    keypoint_weight: 0.4
    description: Điểm chú ý được tính dựa trên biểu thức $\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$ với $Q, K, V$ lần lượt là các ma trận Query, Key và Value.
  - id: KP8_2
    content: Hiện tượng bão hòa hàm Softmax khi số chiều $d_k$ phình to
    keypoint_weight: 0.3
    description: Khi số chiều $d_k$ của vector lớn, tích vô hướng $QK^T$ sẽ nhận các giá trị có phương sai rất lớn, đẩy các giá trị sau khi tính toán rơi vào vùng bão hòa có độ dốc cực kỳ phẳng của hàm kích hoạt Softmax.
  - id: KP8_3
    content: Ổn định Gradient ngăn chặn triệt tiêu đạo hàm (Vanishing Gradient)
    keypoint_weight: 0.3
    description: Chia cho hệ số tỷ lệ $\sqrt{d_k}$ giúp kéo phương sai của tích vô hướng về bằng 1, giữ cho hàm Softmax hoạt động ở vùng có độ dốc tốt, đảm bảo dòng chảy đạo hàm thông suốt trong lúc Backpropagation.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hiện tượng sụp đổ chế độ (Mode Collapse) trong mô hình Generative Adversarial Networks (GAN) truyền thống xảy ra do nguyên nhân toán học nào? Bản chất hình học của Wasserstein GAN (WGAN) giải quyết lỗi này thế nào?
* **expected_key_points:**
  - id: KP9_1
    content: Bản chất Mode Collapse và giới hạn khoảng cách JS/KL Divergence
    keypoint_weight: 0.4
    description: Mode Collapse xảy ra khi mạng Generator chỉ sinh đi sinh lại một vài mẫu dữ liệu hẹp an toàn. Nguyên nhân do Vanilla GAN dùng khoảng cách Jensen-Shannon (JS) để đo độ lệch; khi hai phân phối không chồng lấn, độ dốc gradient của JS bị triệt tiêu về 0, khiến Generator mất phương hướng học.
  - id: KP9_2
    content: Giải pháp dùng Earth Mover's Distance (Khoảng cách Wasserstein)
    keypoint_weight: 0.4
    description: WGAN thay thế bằng khoảng cách Wasserstein, cung cấp một hàm đo lường khoảng cách liên tục và có đạo hàm dốc mượt mà ở mọi nơi, ngay cả khi phân phối thực và giả nằm tách rời nhau hoàn toàn trong không gian hình học.
  - id: KP9_3
    content: Ràng buộc tính liên tục 1-Lipschitz (Lipschitz Continuity)
    keypoint_weight: 0.2
    description: Để tính được khoảng cách Wasserstein, WGAN bắt buộc mạng Discriminator phải thỏa mãn điều kiện ràng buộc toán học 1-Lipschitz continuity, thường được thực thi qua kỹ thuật Weight Clipping hoặc Gradient Penalty.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Khi huấn luyện mô hình ngôn ngữ lớn (LLM) trên hệ thống phân tán đa GPU (Distributed Training), hãy phân tích sự khác nhau về cơ chế hoạt động của kỹ thuật Data Parallelism (DP) và Model Parallelism (MP).
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế nhân bản kiến trúc mạng và phân mảnh dữ liệu của Data Parallelism
    keypoint_weight: 0.4
    description: DP sao chép nguyên vẹn toàn bộ trọng số mô hình sang tất cả các GPU. Tập dữ liệu lớn (Batch) được chia nhỏ thành các phần phân phát cho từng GPU thực hiện Forward và Backward một cách độc lập song song.
  - id: KP10_2
    content: Cơ chế truyền thông đồng bộ All-Reduce trong DP
    keypoint_weight: 0.2
    description: Sau bước Backward, các GPU thực hiện giao tiếp mạng qua thuật toán All-Reduce để tính trung bình cộng các gradient thu được, đồng bộ lại toàn bộ trọng số trước khi bước vào bước tiếp theo.
  - id: KP10_3
    content: Cơ chế phân mảnh kiến trúc mô hình của Model Parallelism
    keypoint_weight: 0.4
    description: Áp dụng khi mô hình quá khổng lồ không thể nhét vừa VRAM của một GPU đơn lẻ. Các ma trận trọng số hoặc các tầng (như các layer Transformer) được cắt mảnh chia nhỏ ra để lưu trữ rải rác trên nhiều GPU khác nhau, quá trình tính toán yêu cầu truyền thông tin liên tục giữa các thiết bị.