# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 1)

* **Role:** AI Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong bài toán tối ưu hóa, tại sao chúng ta lại sử dụng Stochastic Gradient Descent (SGD) hoặc Mini-batch Gradient Descent thay vì Batch Gradient Descent (Vanilla GD) truyền thống khi làm việc với tập dữ liệu lớn?
* **expected_key_points:**
  - id: KP1_1
    content: Chi phí tính toán và bộ nhớ (VRAM/RAM)
    keypoint_weight: 0.5
    description: Batch Gradient Descent yêu cầu nạp và tính toán đạo hàm trên toàn bộ tập dữ liệu cùng một lúc, gây quá tải bộ nhớ và cực kỳ chậm. SGD hoặc Mini-batch chỉ tính toán trên 1 mẫu hoặc 1 nhóm mẫu nhỏ, giúp tiết kiệm tài nguyên bộ nhớ.
  - id: KP1_2
    content: Tốc độ cập nhật trọng số và khả năng thoát tối ưu cục bộ
    keypoint_weight: 0.5
    description: Việc tính toán trên các tập con giúp mô hình cập nhật trọng số liên tục nhiều lần trong một epoch (thay vì chỉ 1 lần), tăng tốc độ hội tụ và tạo ra sự nhiễu ngẫu nhiên giúp mô hình dễ thoát khỏi các điểm tối ưu cục bộ tệ.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Hàm kích hoạt (Activation Function) phi tuyến tính đóng vai trò logic toán học gì trong mạng nơ-ron? Nếu không sử dụng hàm kích hoạt phi tuyến tính thì mạng nơ-ron sâu sẽ bị suy biến như thế nào?
* **expected_key_points:**
  - id: KP2_1
    content: Khả năng học các mối quan hệ phi tuyến phức tạp
    keypoint_weight: 0.5
    description: Hàm kích hoạt phi tuyến tính cho phép mạng nơ-ron bẻ cong không gian dữ liệu, từ đó học được các ranh giới quyết định phức tạp thay vì chỉ phân tách tuyến tính phẳng.
  - id: KP2_2
    content: Hiện tượng suy biến thành mô hình tuyến tính phẳng
    keypoint_weight: 0.5
    description: Nếu không có hàm phi tuyến, tích các phép biến đổi tuyến tính tại các tầng ẩn (ma trận nhân ma trận) sẽ suy biến toán học kết hợp lại thành một phép biến đổi tuyến tính duy nhất. Lúc này mạng nơ-ron sâu nhiều tầng chỉ có sức mạnh tương đương một mô hình Tuyến tính đơn tầng (Linear Regression).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt điểm khác nhau cơ bản và hệ quả thực tế giữa hai lỗi đo lường dữ liệu: High Bias (Độ chệch cao) và High Variance (Phương sai cao).
* **expected_key_points:**
  - id: KP3_1
    content: Bản chất của High Bias (Underfitting)
    keypoint_weight: 0.5
    description: High Bias xảy ra khi mô hình quá đơn giản, không học được cấu trúc của dữ liệu huấn luyện, dẫn đến độ lỗi cao trên cả tập Train lẫn tập Validation (Underfitting).
  - id: KP3_2
    content: Bản chất của High Variance (Overfitting)
    keypoint_weight: 0.5
    description: High Variance xảy ra khi mô hình quá phức tạp, học thuộc lòng cả nhiễu của tập dữ liệu huấn luyện, dẫn đến độ lỗi trên tập Train rất thấp nhưng độ lỗi trên tập Validation lại rất cao (Overfitting).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong mạng nơ-ron tích chập (CNN) dùng cho xử lý ảnh, hãy giải thích ý nghĩa kỹ thuật và tác động hình học của hai siêu tham số: Stride (Bước nhảy) và Padding (Đệm rìa).
* **expected_key_points:**
  - id: KP4_1
    content: Khái niệm và tác động của Stride
    keypoint_weight: 0.5
    description: Stride quy định khoảng cách bước dịch chuyển của bộ lọc (Kernel) khi trượt qua ảnh đầu vào. Stride càng lớn thì kích thước không gian (chiều rộng/cao) của bản đồ đặc trưng (Feature map) đầu ra càng giảm nhanh, giúp giảm lượng tính toán.
  - id: KP4_2
    content: Khái niệm và tác động của Padding (Same/Valid Padding)
    keypoint_weight: 0.5
    description: Padding là việc thêm các giá trị (thường là 0) vào rìa xung quanh ảnh gốc. Mục đích nhằm bảo toàn kích thước không gian của Feature map sau phép cuộn (Same Padding) và ngăn chặn việc mất mát thông tin ở các cạnh/góc ảnh do bị filter duyệt qua ít lần hơn phần trung tâm.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi đánh giá một mô hình phân loại đa lớp (Multi-class Classification) có tập dữ liệu bị mất cân bằng nghiêm trọng, tại sao chỉ số Macro-F1 và Micro-F1 lại cho ra các kết quả phản ánh khác nhau?
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế tính toán không trọng số của Macro-F1
    keypoint_weight: 0.5
    description: Macro-F1 tính toán chỉ số F1-score độc lập cho từng lớp rồi lấy trung bình cộng giản đơn, coi trọng vai trò của mọi lớp ngang nhau bất kể số lượng mẫu. Chỉ số này phản ánh tốt hiệu năng trên các nhóm lớp thiểu số (Minority classes).
  - id: KP5_2
    content: Cơ chế tính toán tổng gộp của Micro-F1
    keypoint_weight: 0.5
    description: Micro-F1 thu thập tổng số True Positive, False Positive, False Negative trên toàn bộ hệ thống trước rồi mới tính toán F1-score tổng thể. Chỉ số này bị thao túng mạnh bởi các lớp đa số (Majority classes) chiếm số đông dữ liệu.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong huấn luyện học sâu, thuật toán tối ưu RMSprop (Root Mean Square Propagation) giải quyết vấn đề gì của thuật toán AdaGrad truyền thống bằng cơ chế toán học nào?
* **expected_key_points:**
  - id: KP6_1
    content: Khuyết điểm suy giảm Learning Rate vô hạn của AdaGrad
    keypoint_weight: 0.5
    description: AdaGrad cộng dồn tất cả bình phương gradient từ đầu trận, khiến tổng này phình to liên tục theo thời gian, ép Learning Rate thích ứng bị thu nhỏ tiến về 0 khiến mô hình ngừng học hoàn toàn ở các epoch sau.
  - id: KP6_2
    content: Cơ chế trung bình trượt lũy thừa (Exponential Moving Average) của RMSprop
    keypoint_weight: 0.5
    description: RMSprop sửa lỗi bằng cách áp dụng trung bình trượt lũy thừa có trọng số ($\beta$) cho bình phương gradient, giúp chỉ giữ lại thông tin biến động của các bước gần nhất, ngăn chặn tổng phình to vô hạn và duy trì tốc độ học ổn định.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy giải thích quy trình hoạt động logic của kỹ thuật Data Augmentation (Tăng cường dữ liệu) đối với bài toán phân loại hình ảnh. Tại sao kỹ thuật này đóng vai trò như một cơ chế Regularization?
* **expected_key_points:**
  - id: KP7_1
    content: Cơ chế biến đổi hình học và màu sắc dữ liệu ảnh
    keypoint_weight: 0.5
    description: Áp dụng các phép biến đổi ngẫu nhiên lên ảnh gốc (như lật ngang, xoay góc, cắt mờ, thay đổi độ sáng/tương phản) để sinh ra các biến thể ảnh mới mà không làm thay đổi nhãn bản chất.
  - id: KP7_2
    content: Bản chất Regularization mở rộng không gian mẫu
    keypoint_weight: 0.5
    description: Giúp làm giàu dữ liệu một cách nhân tạo, ép mô hình không được học thuộc lòng các góc nhìn cố định, tăng cường tính bất biến và khả năng tổng quát hóa, từ đó giảm thiểu hiện tượng Overfitting hiệu quả.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong kiến trúc mạng nơ-ron tích chập sâu, tại sao các mạng quá sâu (như hơn 100 tầng) gặp hiện tượng suy thoái hiệu năng (Degradation Problem) và kiến trúc Residual Network (ResNet) giải quyết bài toán này bằng khối toán học Residual Block như thế nào?
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất hiện tượng suy thoái (Degradation) khác biệt với Vanishing
    keypoint_weight: 0.3
    description: Khi mạng quá sâu, độ chính xác bắt đầu bị bão hòa và sau đó tụt dốc nhanh chóng trên cả tập Train lẫn Test. Lỗi này không phải do Overfitting hay Vanishing Gradient, mà do các tầng sâu quá khó để tự học được phép đồng nhất (Identity mapping).
  - id: KP8_2
    content: Cơ chế kết nối tắt (Skip Connection / Shortcut Connection)
    keypoint_weight: 0.4
    description: ResNet chèn thêm một nhánh kết nối tắt truyền thẳng dữ liệu đầu vào $x$ vượt cấp qua các tầng ẩn, cộng trực tiếp vào đầu ra của khối xử lý phi tuyến tính tạo thành hàm mục tiêu $H(x) = F(x) + x$.
  - id: KP8_3
    content: Cơ chế toán học giúp dòng chảy gradient thông suốt
    keypoint_weight: 0.3
    description: Thay vì bắt các tầng ẩn học hàm mục tiêu gốc $H(x)$, khối ép chúng học phần dư $F(x) = H(x) - x$. Khi tính đạo hàm, thành phần $+x$ giúp gradient luôn có một lượng cộng $+1$ cố định truyền ngược trực tiếp về các tầng trước mà không bị suy biến, triệt tiêu.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Khái niệm "Attention Bottleneck" trong kiến trúc Encoder-Decoder truyền thống (Seq2Seq dùng RNN/LSTM) là gì? Cơ chế Bahdanau Additive Attention giải quyết giới hạn này như thế nào?
* **expected_key_points:**
  - id: KP9_1
    content: Điểm nghẽn mã hóa vector ngữ cảnh cố định (Context Vector)
    keypoint_weight: 0.4
    description: Mạng Seq2Seq truyền thống bắt ép toàn bộ chuỗi đầu vào dài phải nén thông tin vào một vector trạng thái ẩn cuối cùng có kích thước cố định (Bottleneck), gây mất mát thông tin nghiêm trọng khi xử lý câu dài.
  - id: KP9_2
    content: Cơ chế tính điểm tương đồng động (Alignment Scores)
    keypoint_weight: 0.3
    description: Bahdanau Attention cho phép bộ Decoder tại mỗi bước giải mã tự động tính toán điểm số tương quan (Alignment) giữa trạng thái ẩn hiện tại của nó với toàn bộ các trạng thái ẩn (Hidden states) của phía Encoder.
  - id: KP9_3
    content: Tổng hợp vector ngữ cảnh động theo trọng số Softmax
    keypoint_weight: 0.3
    description: Điểm số đi qua hàm Softmax tạo thành trọng số phân phối xác suất chú ý, thực hiện phép nhân tổng có trọng số với các trạng thái ẩn Encoder để tạo ra một Vector ngữ cảnh động riêng biệt biến đổi linh hoạt cho từng từ được dịch.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong huấn luyện và tối ưu hệ thống Nhận diện khuôn mặt (Face Recognition) hoặc Tìm kiếm tương đồng, tại sao hàm mất mát Softmax thông thường không hiệu quả? Hãy giải thích cơ chế toán học của hàm mất mát Triplet Loss.
* **expected_key_points:**
  - id: KP10_1
    content: Giới hạn của Softmax trong học biểu diễn (Metric Learning)
    keypoint_weight: 0.3
    description: Softmax chỉ cố gắng tối ưu phân tách ranh giới giữa các lớp cố định có sẵn trong tập huấn luyện, không tối ưu cho việc kéo gần/đẩy xa không gian khoảng cách vector (Embedding space) để nhận diện các đối tượng hoàn toàn mới nằm ngoài tập train.
  - id: KP10_2
    content: Ba thành phần vector đầu vào của cấu trúc Triplet
    keypoint_weight: 0.3
    description: Triplet Loss làm việc trên bộ 3 mẫu ảnh đồng thời: Anchor (Ảnh gốc đối tượng A), Positive (Ảnh khác cũng của đối tượng A), và Negative (Ảnh của đối tượng B khác hoàn toàn).
  - id: KP10_3
    content: Công thức tối ưu hình học khoảng cách và hệ số Margin ($\alpha$)
    keypoint_weight: 0.4
    description: Hàm mất mát có công thức $\max(d(A, P) - d(A, N) + \alpha, 0)$. Cơ chế ép khoảng cách giữa Anchor và Positive $d(A,P)$ phải nhỏ lại, đồng thời đẩy khoảng cách giữa Anchor và Negative $d(A,N)$ ra xa nhau tối thiểu một khoảng biên an toàn quy định bởi tham số Margin $\alpha$.