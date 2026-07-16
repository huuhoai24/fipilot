# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 1)

* **Role:** AI Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong Machine Learning, hãy phân biệt sự khác nhau cốt lõi giữa hai bài toán Supervised Learning (Học có giám sát) và Unsupervised Learning (Học không giám sát).
* **expected_key_points:**
  - id: KP1_1
    content: Sự hiện diện của Nhãn (Labels/Ground Truth)
    keypoint_weight: 0.5
    description: Supervised Learning yêu cầu tập dữ liệu đầu vào phải có nhãn đi kèm để mô hình học ánh xạ. Unsupervised Learning làm việc với dữ liệu không có nhãn.
  - id: KP1_2
    content: Mục tiêu thuật toán (Core Objective)
    keypoint_weight: 0.5
    description: Supervised Learning nhằm dự đoán nhãn/giá trị cho dữ liệu mới (Regression/Classification). Unsupervised Learning nhằm tìm ra cấu trúc, quy luật ẩn hoặc cụm dữ liệu (Clustering/Dimensionality Reduction).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Hiện tượng Overfitting (Quá khớp) là gì và làm thế nào để nhận biết mô hình đang bị Overfitting thông qua kết quả trên tập Train và tập Validation?
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa bản chất Overfitting
    keypoint_weight: 0.4
    description: Là hiện tượng mô hình học thuộc lòng cả nhiễu (noise) của tập Train, dẫn đến mất khả năng tổng quát hóa (generalization) trên dữ liệu mới.
  - id: KP2_2
    content: Dấu hiệu nhận biết qua chỉ số hiệu năng
    keypoint_weight: 0.6
    description: Độ chính xác (hoặc lỗi) trên tập Train rất tốt (lỗi thấp), nhưng trên tập Validation hoặc Test lại rất tệ (lỗi cao), tạo ra khoảng cách lớn giữa hai đường đồ thị hiệu năng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao việc thực hiện Feature Scaling (Chuẩn hóa dữ liệu đầu vào như Standardization hoặc Normalization) lại vô cùng quan trọng đối với các thuật toán tối ưu dựa trên Gradient Descent?
* **expected_key_points:**
  - id: KP3_1
    content: Đồng bộ hóa thang đo các thuộc tính
    keypoint_weight: 0.4
    description: Đưa các tính năng có khoảng giá trị chênh lệch lớn về cùng một không gian thang đo (ví dụ: 0 đến 1 hoặc phân phối chuẩn).
  - id: KP3_2
    content: Tốc độ hội tụ của Gradient Descent
    keypoint_weight: 0.6
    description: Giúp hàm mất mát (Loss function) bớt méo mó (bớt hình elip dẹt), giúp hướng đi của Gradient thẳng về điểm tối ưu hơn, tránh hiện tượng dao động (oscillations) và tăng tốc độ hội tụ.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy phân biệt ý nghĩa logic và ngữ cảnh sử dụng của ba hàm kích hoạt (Activation Functions) phổ biến trong Deep Learning: Sigmoid, Tanh, và ReLU.
* **expected_key_points:**
  - id: KP4_1
    content: Khoảng giá trị đầu ra (Output Range)
    keypoint_weight: 0.3
    description: Sigmoid nén dữ liệu vào khoảng (0, 1); Tanh nén vào khoảng (-1, 1); ReLU chuyển các giá trị âm về 0 và giữ nguyên các giá trị dương [0, +inf).
  - id: KP4_2
    content: Ngữ cảnh áp dụng (Application Context)
    keypoint_weight: 0.3
    description: Sigmoid dùng ở tầng ra của bài toán phân loại nhị phân; Tanh dùng ở các tầng ẩn hoặc mô hình RNN; ReLU là hàm mặc định cho các tầng ẩn của mạng CNN/MLP hiện đại.
  - id: KP4_3
    content: Hiện tượng triệt tiêu đạo hàm (Vanishing Gradient)
    keypoint_weight: 0.4
    description: Sigmoid và Tanh dễ bị bão hòa ở 2 đầu làm đạo hàm tiến về 0 gây triệt tiêu gradient; ReLU giải quyết được vấn đề này ở vùng giá trị dương nhờ đạo hàm bằng 1 cố định.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi đánh giá một mô hình phân loại (Classification), tại sao chỉ số Accuracy (Độ chính xác tổng thể) đôi khi không phản ánh đúng thực tế? Người ta dùng hai chỉ số Precision và Recall để giải quyết bài toán gì?
* **expected_key_points:**
  - id: KP5_1
    content: Vấn đề mất cân bằng dữ liệu (Imbalanced Data)
    keypoint_weight: 0.4
    description: Accuracy sẽ bị thao túng và cực cao nếu tập dữ liệu bị lệch nghiêm trọng (ví dụ 99% mẫu là âm tính), mô hình chỉ cần đoán bừa toàn âm tính vẫn đạt 99% accuracy.
  - id: KP5_2
    content: Ý nghĩa của Precision và Recall
    keypoint_weight: 0.6
    description: Precision đo lường tỷ lệ đoán đúng trong các mẫu được dự đoán là Dương tính (giảm thiểu sai lầm False Positive); Recall đo lường tỷ lệ tìm sót các mẫu Dương tính thật sự trong thực tế (giảm thiểu sai lầm False Negative).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong kiến trúc mạng mạng nơ-ron cuộn (CNN) dùng cho xử lý ảnh, hai tầng Convolutional Layer (Tầng cuộn) và Pooling Layer (Tầng gom cụm) đóng vai trò kỹ thuật gì?
* **expected_key_points:**
  - id: KP6_1
    content: Vai trò của Convolutional Layer
    keypoint_weight: 0.5
    description: Sử dụng các bộ lọc (Kernels/Filters) trượt trên ảnh để trích xuất các đặc trưng không gian (Features) từ thấp đến cao như cạnh, góc, vân bề mặt.
  - id: KP6_2
    content: Vai trò của Pooling Layer (Max/Average Pooling)
    keypoint_weight: 0.5
    description: Làm giảm kích thước không gian (Spatial dimensions) của bản đồ đặc trưng, giúp giảm lượng tham số tính toán, tăng tính bất biến đối với các phép dịch chuyển nhỏ (Translation invariance).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy giải thích quy trình hoạt động của kỹ thuật K-Fold Cross-Validation và lý do tại sao nó giúp đánh giá mô hình một cách khách quan hơn cách chia Train/Test tĩnh thông thường.
* **expected_key_points:**
  - id: KP7_1
    content: Cơ chế phân chia và lặp dữ liệu
    keypoint_weight: 0.5
    description: Chia tập dữ liệu thành K phần bằng nhau. Lặp K lần, mỗi lần chọn 1 phần làm Validation, K-1 phần còn lại làm Train. Kết quả cuối cùng là trung bình cộng hiệu năng của K lần chạy.
  - id: KP7_2
    content: Tính khách quan và giảm thiểu độ chệch (Bias)
    keypoint_weight: 0.5
    description: Đảm bảo mọi mẫu dữ liệu trong dataset đều có cơ hội được dùng để huấn luyện và kiểm thử một lần, loại bỏ yếu tố may rủi do việc chia cắt dữ liệu tĩnh gây ra.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Hiện tượng Triệt tiêu Đạo hàm (Vanishing Gradient) và Bùng nổ Đạo hàm (Exploding Gradient) trong mạng Deep Neural Network xảy ra do nguyên nhân toán học nào trong quá trình Backpropagation? Nêu giải pháp khắc phục cho từng hiện tượng.
* **expected_key_points:**
  - id: KP8_1
    content: Nguyên nhân toán học (Chain Rule nhân chuỗi)
    keypoint_weight: 0.4
    description: Do quy tắc chuỗi (Chain Rule) thực hiện nhân liên tiếp các ma trận trọng số và đạo hàm của hàm kích hoạt qua nhiều tầng ẩn. Nếu các giá trị này < 1, tích số sẽ tiến dần về 0 (Vanishing); nếu các giá trị này > 1, tích số sẽ tăng tiến lũy thừa tiến về vô cùng (Exploding).
  - id: KP8_2
    content: Giải pháp cho Vanishing Gradient
    keypoint_weight: 0.3
    description: Sử dụng hàm kích hoạt ReLU/LeakyReLU, áp dụng kiến trúc kết nối tắt Residual Connections (Skip connections), hoặc sử dụng Batch Normalization.
  - id: KP8_3
    content: Giải pháp cho Exploding Gradient
    keypoint_weight: 0.3
    description: Áp dụng kỹ thuật Giới hạn Đạo hàm (Gradient Clipping) để chặn giá trị trần của Gradient, hoặc khởi tạo trọng số một cách thông minh (Xavier/He Initialization).

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Cơ chế Tự chú ý (Self-Attention) trong kiến trúc Transformer hoạt động dựa trên các vector Query (Q), Key (K), và Value (V) như thế nào để tính toán mối quan hệ giữa các từ trong một câu?
* **expected_key_points:**
  - id: KP9_1
    content: Khởi tạo các không gian vector đầu vào
    keypoint_weight: 0.3
    description: Từ mỗi token đầu vào, nhân với các ma trận trọng số học được ($W_Q, W_K, W_V$) để tạo ra 3 vector tương ứng: Query ($Q$), Key ($K$), và Value ($V$).
  - id: KP9_2
    content: Tính toán điểm chú ý (Attention Score) bằng Scaled Dot-Product
    keypoint_weight: 0.4
    description: Lấy tích vô hướng giữa Query của từ hiện tại với Key của tất cả các từ khác ($Q \cdot K^T$), chia cho căn bậc hai của kích thước vector ($\sqrt{d_k}$) để ổn định đạo hàm, rồi đi qua hàm Softmax nhằm thu được trọng số chú ý dạng phân phối xác suất.
  - id: KP9_3
    content: Tổng hợp thông tin theo trọng số (Weighted Sum)
    keypoint_weight: 0.3
    description: Lấy kết quả phân phối xác suất từ hàm Softmax nhân với ma trận vector Value ($V$) tương ứng nhằm trích xuất ra biểu diễn ngữ cảnh mới của từ chứa thông tin liên kết của các từ xung quanh.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích sự đánh đổi về mặt tài nguyên tính toán (Compute), bộ nhớ (VRAM) và thời gian phản hồi (Latency) khi triển khai một mô hình ngôn ngữ lớn (LLM) bằng hai kỹ thuật: Fine-tuning (Tinh chỉnh trọng số) và RAG (Retrieval-Augmented Generation - Triển khai kèm kho tri thức).
* **expected_key_points:**
  - id: KP10_1
    content: Ràng buộc của kỹ thuật Fine-tuning
    keypoint_weight: 0.5
    description: Tiêu tốn tài nguyên tính toán (GPU/TPU) và VRAM cực lớn trong giai đoạn huấn luyện để cập nhật trọng số mạng; thời gian Latency khi chạy inference ổn định nhưng dữ liệu tri thức bị đóng băng cố định tại thời điểm training, muốn cập nhật phải retraining lại.
  - id: KP10_2
    content: Ràng buộc của kỹ thuật RAG
    keypoint_weight: 0.5
    description: Tiết kiệm tài nguyên huấn luyện mô hình vì đóng băng trọng số (triển khai dạng Zero-shot/In-context), tri thức cập nhật thời gian thực qua Vector Database. Tuy nhiên, làm tăng Latency đáng kể lúc inference do tốn thêm thời gian truy vấn tìm kiếm ngữ cảnh (Retrieval phase) và làm phình to chiều dài Context Window đính kèm đầu vào của LLM.