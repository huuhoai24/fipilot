# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 1)

* **Role:** AI Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong Machine Learning, hãy nêu sự khác biệt bản chất giữa thuật toán phân cụm K-Means (Unsupervised) và thuật toán phân loại K-Nearest Neighbors (Supervised).
* **expected_key_points:**
  - id: KP1_1
    content: Phân biệt dựa trên nhãn dữ liệu (Data Labels)
    keypoint_weight: 0.5
    description: K-Means làm việc với dữ liệu không nhãn (Unsupervised) để nhóm các điểm dữ liệu tương đồng. KNN làm việc với dữ liệu có nhãn (Supervised) để dự đoán nhãn cho mẫu mới dựa trên các láng giềng gần nhất.
  - id: KP1_2
    content: Cơ chế hoạt động cốt lõi (Core Mechanism)
    keypoint_weight: 0.5
    description: K-Means lặp đi lặp lại việc cập nhật các tâm cụm (Centroids) để tối thiểu hóa khoảng cách nội cụm. KNN tính khoảng cách từ mẫu thử nghiệm đến toàn bộ tập huấn luyện để bỏ phiếu (Voting) quyết định nhãn tại thời điểm inference.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Hiện tượng Underfitting (Dưới khớp) xảy ra khi nào? Làm thế nào để nhận biết mô hình bị Underfitting và hướng khắc phục cơ bản là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa và dấu hiệu qua độ lỗi (Error/Loss)
    keypoint_weight: 0.5
    description: Underfitting xảy ra khi mô hình quá đơn giản, không học được cấu trúc của dữ liệu. Biểu hiện là độ lỗi rất cao (High Bias) trên cả tập huấn luyện (Train) lẫn tập kiểm thử (Validation/Test).
  - id: KP2_2
    content: Hướng giải quyết kỹ thuật (Mitigation)
    keypoint_weight: 0.5
    description: Khắc phục bằng cách tăng độ phức tạp của mô hình (ví dụ: dùng mạng nơ-ron sâu hơn, thêm tầng, tăng số lượng tham số), hoặc trích xuất thêm các đặc trưng tốt hơn (Feature Engineering).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Hàm mất mát Mean Squared Error (MSE) và Cross-Entropy Loss thường được sử dụng cho những loại bài toán nào trong Machine Learning?
* **expected_key_points:**
  - id: KP3_1
    content: Ngữ cảnh sử dụng MSE
    keypoint_weight: 0.5
    description: MSE được sử dụng cho bài toán hồi quy (Regression), tính toán trung bình bình phương khoảng cách giữa giá trị dự đoán liên tục và giá trị thực tế.
  - id: KP3_2
    content: Ngữ cảnh sử dụng Cross-Entropy Loss
    keypoint_weight: 0.5
    description: Cross-Entropy được sử dụng cho bài toán phân loại (Classification), đo lường sự khác biệt giữa hai phân phối xác suất (xác suất dự đoán của mô hình và nhãn One-hot thực tế).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Kỹ thuật chuẩn hóa Batch Normalization hoạt động theo cơ chế nào và tại sao nó lại giúp tăng tốc độ cũng như tính ổn định của quá trình huấn luyện mạng nơ-ron sâu?
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế chuẩn hóa theo Batch (Mini-batch Normalization)
    keypoint_weight: 0.4
    description: Batch Normalization chuẩn hóa giá trị đầu ra của một tầng ẩn (activation) về phân phối có trung bình bằng 0 và phương sai bằng 1 dựa trên các mẫu trong mini-batch, sau đó áp dụng phép biến đổi tuyến tính có thể học được (scale và shift).
  - id: KP4_2
    content: Giải quyết Internal Covariate Shift
    keypoint_weight: 0.3
    description: Giảm thiểu sự thay đổi liên tục của phân phối dữ liệu đầu vào ở các tầng sâu khi các tham số của tầng trước thay đổi trong quá trình training.
  - id: KP4_3
    content: Tác động tích cực lên Gradient và Learning Rate
    keypoint_weight: 0.3
    description: Giúp giữ cho các giá trị activation không rơi vào vùng bão hòa của hàm kích hoạt, ngăn chặn triệt tiêu đạo hàm, cho phép sử dụng Learning Rate lớn hơn và đóng vai trò như một cơ chế regularization nhẹ.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong huấn luyện Deep Learning, thuật toán tối ưu Adam (Adaptive Moment Estimation) cải tiến điểm gì so với thuật toán Stochastic Gradient Descent (SGD) truyền thống?
* **expected_key_points:**
  - id: KP5_1
    content: Tích hợp cơ chế Quán tính (Momentum)
    keypoint_weight: 0.4
    description: Adam sử dụng khoảnh khắc lũy thừa bậc một (First Moment) để lưu giữ vận tốc và hướng đi của các gradient trước đó, giúp mô hình vượt qua các điểm tối ưu cục bộ (Local Minima) hoặc vùng yên ngựa (Saddle Points).
  - id: KP5_2
    content: Cơ chế Tốc độ học thích ứng (Adaptive Learning Rate)
    keypoint_weight: 0.6
    description: Adam sử dụng khoảnh khắc lũy thừa bậc hai (Second Moment - bình phương gradient) để tự động điều chỉnh Learning Rate riêng biệt cho từng tham số: tham số nào có gradient biến động lớn sẽ bị giảm tốc độ học, tham số nào có gradient nhỏ sẽ được tăng tốc độ học.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi huấn luyện mô hình Object Detection (Phát hiện vật thể), chỉ số IoU (Intersection over Union) và mAP (mean Average Precision) dùng để đánh giá điều gì?
* **expected_key_points:**
  - id: KP6_1
    content: Ý nghĩa logic của IoU
    keypoint_weight: 0.4
    description: IoU đo lường mức độ chồng lấn giữa khung hình chữ nhật dự đoán (Bounding Box) và khung hình thực tế (Ground Truth) bằng tỷ lệ giữa diện tích phần giao (Intersection) trên diện tích phần hợp (Union).
  - id: KP6_2
    content: Cơ chế tính toán mAP
    keypoint_weight: 0.6
    description: mAP là giá trị trung bình cộng của chỉ số Average Precision (AP) trên tất cả các lớp (Classes) cần nhận diện. AP được tính bằng diện tích dưới đường cong Precision-Recall tại một ngưỡng IoU xác định, thể hiện năng lực phân loại lẫn định vị vật thể của mô hình.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Để giảm thiểu hiện tượng Overfitting trong mạng nơ-ron, kỹ thuật Dropout hoạt động như thế nào trong quá trình Forward-propagation và Backward-propagation?
* **expected_key_points:**
  - id: KP7_1
    content: Cơ chế hoạt động trong Forward-propagation
    keypoint_weight: 0.5
    description: Tại mỗi bước huấn luyện, Dropout chủ động ngắt ngẫu nhiên một tỷ lệ p các nút (neurons) trong một tầng ẩn, ép mạng nơ-ron không được phụ thuộc quá mức vào bất kỳ một liên kết cụ thể nào và phải học các đặc trưng mang tính tổng quát.
  - id: KP7_2
    content: Cơ chế hoạt động trong Backward-propagation và Test-time
    keypoint_weight: 0.5
    description: Trong lúc Backpropagation, gradient chỉ được truyền ngược qua các nút đang hoạt động (không bị tắt). Khi ở chế độ Evaluation/Test, toàn bộ các nút sẽ được mở lại nhưng trọng số sẽ được nhân với tỷ lệ scale (1-p) để cân bằng năng lượng đầu ra.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao mạng RNN (Recurrent Neural Network) truyền thống gặp khó khăn lớn khi xử lý chuỗi dữ liệu dài (Long-term Dependencies) và kiến trúc LSTM (Long Short-Term Memory) giải quyết vấn đề đó bằng cơ chế toán học nào?
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất lỗi nghẽn mạch toán học của RNN
    keypoint_weight: 0.3
    description: Khi lan truyền ngược qua thời gian (BPTT) trên một chuỗi dài, phép nhân ma trận trọng số lặp đi lặp lại nhiều lần khiến gradient bị suy giảm lũy thừa, dẫn đến hiện tượng triệt tiêu đạo hàm (Vanishing Gradient) và làm mất thông tin từ quá khứ xa.
  - id: KP8_2
    content: Vai trò của Cell State và hầm thông tin xuyên suốt
    keypoint_weight: 0.3
    description: LSTM bổ sung thành phần Cell State đóng vai trò như một đường băng bộ nhớ tuyến tính xuyên suốt thời gian, cho phép thông tin cũ chảy qua mạng với rất ít sự thay đổi hay suy giảm đạo hàm.
  - id: KP8_3
    content: Cơ chế điều tiết luồng thông tin của các Cổng (Gates)
    keypoint_weight: 0.4
    description: Sử dụng 3 cổng điều khiển bằng hàm Sigmoid: Forget Gate (quyết định xóa bỏ thông tin cũ không còn giá trị), Input Gate (quyết định nạp thông tin mới vào Cell State) và Output Gate (quyết định xuất thông tin gì ra Hidden State tiếp theo).

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong bài toán tối ưu hóa phân phối Generative Adversarial Networks (GAN), hãy giải thích trò chơi minimax (minimax game) giữa hai mạng Generator (Mạng sinh) và Discriminator (Mạng phân biệt) thông qua hàm mục tiêu (Objective Function).
* **expected_key_points:**
  - id: KP9_1
    content: Mục tiêu tối ưu toán học của Discriminator (D)
    keypoint_weight: 0.4
    description: Mạng D cố gắng tối đa hóa (Maximize) xác suất gán nhãn chính xác cho dữ liệu thật là 1 (Real) và dữ liệu do mạng G sinh ra là 0 (Fake), tương ứng với việc tăng giá trị của $V(D, G)$.
  - id: KP9_2
    content: Mục tiêu tối ưu toán học của Generator (G)
    keypoint_weight: 0.4
    description: Mạng G cố gắng tối thiểu hóa (Minimize) khả năng bị mạng D phát hiện lỗi, tương ứng với việc lừa mạng D gán nhãn dữ liệu Fake tiến gần về 1, làm giảm giá trị hàm mục tiêu đối với biến của nó.
  - id: KP9_3
    content: Trạng thái cân bằng Nash (Nash Equilibrium)
    keypoint_weight: 0.2
    description: Trò chơi đạt điểm dừng tối ưu khi mạng G sinh ra dữ liệu giả giống hệt dữ liệu thật đến mức mạng D hoàn toàn bất lực và chỉ có thể đoán mò với xác suất chính xác là 50% ($D(x) = 0.5$).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Kỹ thuật Quantization (Lượng tử hóa mô hình như INT8 Quantization) hoạt động dựa trên nguyên lý toán học nào để nén mô hình AI? Hãy phân biệt sự đánh đổi về mặt bộ nhớ, phần cứng hiển thị và độ chính xác (Accuracy).
* **expected_key_points:**
  - id: KP10_1
    content: Nguyên lý ánh xạ không gian số thực sang số nguyên
    keypoint_weight: 0.4
    description: Thực hiện ánh xạ (Mapping) các giá trị trọng số và activation từ không gian số thực dấu phẩy động liên tục có độ chính xác cao 32-bit (FP32) sang không gian số nguyên rời rạc 8-bit (INT8) thông qua một tỷ lệ tỷ xích (Scale) và điểm không (Zero-point).
  - id: KP10_2
    content: Lợi ích về mặt phần cứng và bộ nhớ (VRAM/Compute)
    keypoint_weight: 0.4
    description: Giảm dung lượng lưu trữ file mô hình và bộ nhớ VRAM đi gần 4 lần, cho phép tận dụng các tập lệnh tính toán số nguyên tốc độ cao trên phần cứng chip nhúng/edge devices (như INT8 Tensor Cores), giảm đáng kể điện năng tiêu thụ và độ trễ phản hồi (Latency).
  - id: KP10_3
    content: Rủi ro suy giảm hiệu năng độ chính xác (Quantization Noise)
    keypoint_weight: 0.2
    description: Gây ra hiện tượng mất mát thông tin do làm tròn dữ liệu (Quantization Noise/Error), dẫn đến việc mô hình có khả năng bị suy giảm nhẹ độ chính xác (Accuracy/F1-score) so với phiên bản FP32 gốc.