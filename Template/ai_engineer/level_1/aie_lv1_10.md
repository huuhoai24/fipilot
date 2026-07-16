# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 1)

* **Role:** AI Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong bài toán phân loại (Classification), hãy phân biệt sự khác nhau về mục đích sử dụng và ý nghĩa toán học của hai hàm kích hoạt: Sigmoid và Softmax.
* **expected_key_points:**
  - id: KP1_1
    content: Ngữ cảnh và phân phối xác suất độc lập của Sigmoid
    keypoint_weight: 0.5
    description: Sigmoid nén một giá trị thô duy nhất về khoảng (0, 1), dùng cho bài toán phân loại nhị phân (Binary Classification) hoặc phân loại đa nhãn (Multi-label Classification) nơi xác suất của các lớp độc lập nhau.
  - id: KP1_2
    content: Ngữ cảnh và phân phối xác suất ràng buộc của Softmax
    keypoint_weight: 0.5
    description: Softmax nén một vector các điểm thô (Logits) thành một phân phối xác suất có tổng bằng 1, dùng cho bài toán phân loại đa lớp loại trừ lẫn nhau (Multi-class Classification).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Hiện tượng Vanishing Gradient (Triệt tiêu đạo hàm) là gì và tại sao nó lại khiến các mạng nơ-ron sâu (Deep Neural Networks) khó học hoặc ngừng hội tụ?
* **expected_key_points:**
  - id: KP2_1
    content: Bản chất toán học của hiện tượng suy giảm đạo hàm
    keypoint_weight: 0.5
    description: Là hiện tượng các giá trị đạo hàm riêng (Gradients) tính được trong quá trình Backpropagation bị giảm dần lũy thừa khi truyền ngược về các tầng đầu tiên của mạng.
  - id: KP2_2
    content: Hệ quả làm đóng băng cập nhật trọng số ở các tầng nông
    keypoint_weight: 0.5
    description: Khi gradient tiến gần về 0, các trọng số ở các tầng ẩn đầu tiên (gần input) gần như không được cập nhật, khiến mạng sâu không thể học được các đặc trưng nền tảng và ngừng hội tụ.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao chúng ta cần thực hiện bước xáo trộn dữ liệu (Data Shuffling) trước khi chia nhỏ dữ liệu thành các Mini-batch để huấn luyện mô hình?
* **expected_key_points:**
  - id: KP3_1
    content: Phá vỡ tính tuần tự và định kiến thứ tự dữ liệu
    keypoint_weight: 0.5
    description: Ngăn chặn việc mô hình học thuộc lòng thứ tự sắp xếp của dữ liệu đầu vào (ví dụ dữ liệu gom cụm toàn nhãn 0 xếp trước rồi đến nhãn 1), điều này có thể làm nhiễu hướng đi của Gradient.
  - id: KP3_2
    content: Đảm bảo tính đại diện phân phối cho các Mini-batch
    keypoint_weight: 0.5
    description: Giúp mỗi Mini-batch đều chứa một tập hợp mẫu ngẫu nhiên đại diện tương đối chính xác cho phân phối tổng thể của toàn bộ dataset, giúp quá trình cập nhật trọng số ổn định hơn.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong mạng nơ-ron tích chập (CNN), hai phép toán Max Pooling và Average Pooling hoạt động khác nhau thế nào và tác động của chúng lên bản đồ đặc trưng (Feature Map) là gì?
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế toán học của Max Pooling (Trích xuất đặc trưng mạnh nhất)
    keypoint_weight: 0.4
    description: Lấy giá trị lớn nhất trong vùng cửa sổ trượt, giúp giữ lại các đặc trưng nổi bật nhất (như cạnh, góc) và tăng tính bất biến đối với các biến đổi nhỏ.
  - id: KP4_2
    content: Cơ chế toán học của Average Pooling (Lấy thông tin nền mượt)
    keypoint_weight: 0.3
    description: Tính giá trị trung bình của các phần tử trong cửa sổ trượt, giúp làm mượt và giữ lại thông tin tổng thể của vùng không gian dữ liệu.
  - id: KP4_3
    content: Tác động chung làm giảm chiều không gian (Downsampling)
    keypoint_weight: 0.3
    description: Cả hai đều làm giảm kích thước chiều rộng và chiều cao của Feature Map, giúp giảm lượng tham số tính toán của hệ thống và kiểm soát Overfitting.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Đối với bài toán Object Detection (Phát hiện vật thể), hãy giải thích mục đích sử dụng của thuật toán Non-Maximum Suppression (NMS) trong giai đoạn hậu xử lý (Post-processing).
* **expected_key_points:**
  - id: KP5_1
    content: Loại bỏ các khung dự đoán trùng lặp (Redundant Bounding Boxes)
    keypoint_weight: 0.5
    description: Trong quá trình suy luận, mô hình có thể tạo ra rất nhiều Bounding Box chồng chéo xung quanh cùng một vật thể duy nhất; NMS dùng để lọc bỏ các hộp thừa này.
  - id: KP5_2
    content: Cơ chế dựa trên Object Score và ngưỡng IoU (Intersection over Union)
    keypoint_weight: 0.5
    description: Thuật toán sắp xếp các hộp theo điểm tự tin (Confidence score) giảm dần, chọn hộp cao nhất, sau đó tính IoU với các hộp xung quanh và xóa bỏ các hộp có chỉ số IoU vượt ngưỡng quy định (quá trùng lặp).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy phân biệt điểm cải tiến cốt lõi về cơ chế cập nhật tốc độ học (Learning Rate) của thuật toán tối ưu RMSprop so với thuật toán AdaGrad truyền thống.
* **expected_key_points:**
  - id: KP6_1
    content: Khuyết điểm phình to tổng bình phương gradient của AdaGrad
    keypoint_weight: 0.5
    description: AdaGrad cộng dồn mọi bình phương gradient từ đầu trận làm mẫu số phình to vô hạn, ép Learning Rate thích ứng giảm nhanh về sát 0 khiến mô hình bị đóng băng ở giai đoạn sau.
  - id: KP6_2
    content: Cơ chế Trung bình trượt lũy thừa (Exponential Moving Average) của RMSprop
    keypoint_weight: 0.5
    description: RMSprop giới hạn việc tính toán bình phương gradient trong một cửa sổ thời gian gần thông qua hệ số suy giảm $\beta$, giúp mẫu số ổn định, duy trì tốc độ học thích ứng mượt mà.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong huấn luyện học sâu, tại sao việc khởi tạo toàn bộ trọng số (Weights) bằng giá trị 0 tuyệt đối (Zero Initialization) lại là một sai lầm kỹ thuật nghiêm trọng? Kỹ thuật Xavier Initialization giải quyết lỗi này thế nào?
* **expected_key_points:**
  - id: KP7_1
    content: Lỗi mất tính đối xứng toán học (Symmetry Breaking Problem)
    keypoint_weight: 0.5
    description: Nếu toàn bộ trọng số bằng 0, mọi nơ-ron trong cùng một tầng ẩn sẽ tính toán ra cùng một giá trị đầu ra giống hệt nhau ở bước Forward và nhận cùng một lượng Gradient ở bước Backward. Hệ thống bị suy biến thành một nơ-ron duy nhất.
  - id: KP7_2
    content: Cơ chế giữ nguyên phương sai dòng chảy của Xavier Initialization
    keypoint_weight: 0.5
    description: Khởi tạo ngẫu nhiên trọng số từ một phân phối có phương sai tỷ lệ nghịch với số lượng nơ-ron đầu vào và đầu ra của tầng đó, giúp giữ cho phương sai của các giá trị activation và gradient ổn định xuyên suốt các tầng mạng.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong kiến trúc Transformer, hãy phân tích ý nghĩa toán học của thành phần tích vô hướng $QK^T$ chia cho $\sqrt{d_k}$ trong tầng Scaled Dot-Product Attention. Hệ số scale $\sqrt{d_k}$ đóng vai trò sinh tử gì cho hàm Softmax?
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất hình học đo độ tương đồng của phép nhân $QK^T$
    keypoint_weight: 0.4
    description: Phép nhân tích vô hướng ma trận giữa Query ($Q$) và Key ($K$) dùng để tính toán điểm số tương quan ngữ cảnh (Attention scores) giữa các cặp token trong chuỗi dữ liệu.
  - id: KP8_2
    content: Hiện tượng bão hòa đạo hàm Softmax khi số chiều $d_k$ lớn
    keypoint_weight: 0.3
    description: Khi số chiều vector $d_k$ lớn, giá trị tích vô hướng có phương sai phình to, đẩy các giá trị sau Softmax rơi vào các vùng có độ dốc cực nhỏ (vùng bão hòa), làm triệt tiêu dòng chảy đạo hàm.
  - id: KP8_3
    content: Ổn định phương sai về 1 nhờ hệ số scale $\sqrt{d_k}$
    keypoint_weight: 0.3
    description: Chia cho hệ số $\sqrt{d_k}$ giúp kéo phương sai của tích vô hướng lùi về bằng 1, giữ cho hàm Softmax luôn hoạt động ở vùng có độ dốc tốt, đảm bảo Gradient thông suốt lúc lan truyền ngược.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích cơ chế hoạt động và nguyên lý toán học của phương pháp huấn luyện tri thức tương phản Triplet Loss thường dùng trong học biểu diễn (Metric Learning) cho bài toán Face Recognition.
* **expected_key_points:**
  - id: KP9_1
    content: Cấu trúc đầu vào bộ ba (Anchor, Positive, Negative)
    keypoint_weight: 0.3
    description: Hàm mất mát xử lý đồng thời một bộ 3 mẫu ảnh: Anchor (Ảnh gốc của người A), Positive (Ảnh khác của người A) và Negative (Ảnh của người B hoàn toàn khác).
  - id: KP9_2
    content: Công thức tối ưu khoảng cách hình học không gian nhúng
    keypoint_weight: 0.4
    description: Hàm loss có công thức toán: $\max(d(A, P) - d(A, N) + \alpha, 0)$. Cơ chế ép khoảng cách giữa ảnh cùng người $d(A,P)$ tiến về 0 và đẩy khoảng cách giữa ảnh khác người $d(A,N)$ ra xa tối thiểu một khoảng biên an toàn $\alpha$.
  - id: KP9_3
    content: Khái niệm Hard Triplets trong kỹ thuật chọn mẫu (Mining)
    keypoint_weight: 0.3
    description: Trong thực tế huấn luyện, các bộ ba ngẫu nhiên dễ dàng đạt loss = 0. Do đó, cần áp dụng chiến lược lọc mẫu nâng cao (Semi-hard/Hard Triplet Mining) để ép mô hình học các mẫu cực kỳ giống nhau nhưng khác nhãn, giúp không gian nhúng phân tách sắc bén.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong kỹ thuật lượng tử hóa mô hình (Quantization như Post-Training Quantization - PTQ), hãy giải thích cơ chế ánh xạ toán học từ không gian số thực FP32 sang không gian số nguyên INT8. Khái niệm "Calibration" (Hiệu chuẩn) đóng vai trò gì trong quy trình này?
* **expected_key_points:**
  - id: KP10_1
    content: Công thức ánh xạ tuyến tính Affine Quantization
    keypoint_weight: 0.4
    description: Ánh xạ dựa trên công thức tuyến tính $q = \text{round}\left(\frac{x}{S}\right) + Z$, trong đó $S$ là hệ số tỷ xích (Scale - số thực) và $Z$ là điểm không (Zero-point - số nguyên) để ép dải FP32 vào khoảng [-128, 127] hoặc [0, 255].
  - id: KP10_2
    content: Bản chất và vai trò của bước Calibration
    keypoint_weight: 0.4
    description: Lượng tử hóa trực tiếp dễ gây mất mát thông tin do làm tròn. Calibration chạy thử một tập dữ liệu nhỏ (Calibration dataset) qua mạng để thu thập phân phối thực tế (nhận diện các giá trị min/max động của activation), từ đó tính toán ra hệ số $S$ và $Z$ tối ưu nhất.
  - id: KP10_3
    content: Giảm thiểu nhiễu lượng tử hóa (Quantization Noise)
    keypoint_weight: 0.2
    description: Việc áp dụng Calibration giúp phân phối dữ liệu sau khi ép về INT8 ít bị lệch cấu trúc so với FP32 ban đầu nhất, giảm thiểu tối đa sự suy giảm độ chính xác tổng thể (Accuracy drop) của mô hình.