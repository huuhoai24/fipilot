# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 1)

* **Role:** AI Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong huấn luyện mạng nơ-ron, mục đích cốt lõi của quá trình Forward Propagation (Lan truyền tiến) và Backward Propagation (Lan truyền ngược) là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Mục đích của Forward Propagation (Tính toán đầu ra và độ lỗi)
    keypoint_weight: 0.5
    description: Lan truyền dữ liệu đầu vào qua các tầng của mạng để tính toán giá trị dự đoán đầu ra, từ đó so sánh với nhãn thực tế để tính toán giá trị của hàm mất mát (Loss function).
  - id: KP1_2
    content: Mục đích của Backward Propagation (Tính đạo hàm và cập nhật trọng số)
    keypoint_weight: 0.5
    description: Sử dụng quy tắc chuỗi (Chain Rule) để tính toán đạo hàm riêng (Gradients) của hàm mất mát đối với từng trọng số (Weights/Biases), làm cơ sở cho thuật toán tối ưu cập nhật tham số nhằm giảm thiểu độ lỗi.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt sự khác biệt logic và ngữ cảnh sử dụng giữa hai hàm mất mát: Binary Cross-Entropy Loss và Categorical Cross-Entropy Loss.
* **expected_key_points:**
  - id: KP2_1
    content: Ngữ cảnh phân loại nhị phân (Binary Classification)
    keypoint_weight: 0.5
    description: Binary Cross-Entropy được sử dụng khi bài toán chỉ có 2 lớp đối lập (0 và 1), kết hợp với hàm kích hoạt Sigmoid ở tầng đầu ra để dự đoán xác suất độc lập cho một lớp.
  - id: KP2_2
    content: Ngữ cảnh phân loại đa lớp loại trừ (Multi-class Classification)
    keypoint_weight: 0.5
    description: Categorical Cross-Entropy được sử dụng cho bài toán có từ 3 lớp trở lên và các lớp mang tính loại trừ lẫn nhau, yêu cầu nhãn đầu vào dạng mã hóa One-hot và kết hợp với hàm kích hoạt Softmax ở tầng đầu ra.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong xử lý dữ liệu dạng bảng (Tabular Data) hoặc chuỗi thời gian, giá trị Missing Value (Dữ liệu bị khuyết) gây ra hệ quả gì và nêu hai phương pháp cơ bản để xử lý (Imputation)?
* **expected_key_points:**
  - id: KP3_1
    content: Hệ quả của dữ liệu khuyết lên mô hình
    keypoint_weight: 0.4
    description: Khiến các phép toán ma trận trong thư viện (như NumPy, Scikit-Learn) bị lỗi không thể tính toán (lỗi NaN), hoặc làm sai lệch phân phối đặc trưng của dữ liệu.
  - id: KP3_2
    content: Phương pháp xóa bỏ (Deletion) và điền khuyết bằng thống kê (Statistical Imputation)
    keypoint_weight: 0.6
    description: Xử lý bằng cách xóa bỏ các hàng/cột chứa dữ liệu khuyết nếu tỷ lệ quá nhỏ; hoặc điền khuyết bằng các giá trị đại diện như Mean (Trung bình), Median (Trung vị) cho biến liên tục, hoặc Mode (Yếu vị) cho biến phân loại.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thuật toán Random Forest hoạt động dựa trên kỹ thuật Ensemble Learning nào? Tại sao nó lại có khả năng giảm thiểu hiện tượng Overfitting tốt hơn một cây quyết định (Decision Tree) đơn lẻ?
* **expected_key_points:**
  - id: KP4_1
    content: Kỹ thuật Bagging (Bootstrap Aggregating) và lấy mẫu ngẫu nhiên thuộc tính
    keypoint_weight: 0.5
    description: Random Forest xây dựng nhiều cây quyết định độc lập song song. Mỗi cây được huấn luyện trên một tập con dữ liệu lấy mẫu ngẫu nhiên có hoàn lại (Bootstrap sample) và tại mỗi nút phân nhánh chỉ chọn ngẫu nhiên một nhóm các thuộc tính (Features subset).
  - id: KP4_2
    content: Cơ chế bỏ phiếu số đông (Voting/Averaging) giảm Variance
    keypoint_weight: 0.5
    description: Kết quả dự đoán cuối cùng là trung bình cộng (bài toán hồi quy) hoặc bỏ phiếu số đông (bài toán phân loại) từ tất cả các cây. Việc kết hợp nhiều cây có Bias cao nhưng không tương quan với nhau giúp triệt tiêu sai số ngẫu nhiên, làm giảm mạnh phương sai (Variance) tổng thể của mô hình.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Kỹ thuật giảm số chiều dữ liệu Principal Component Analysis (PCA) hoạt động dựa trên nguyên lý toán học nào và mục đích sử dụng của nó trong tiền xử lý dữ liệu là gì?
* **expected_key_points:**
  - id: KP5_1
    content: Cực đại hóa phương sai và trực giao không gian
    keypoint_weight: 0.5
    description: PCA tìm kiếm các trục tọa độ mới gọi là các thành phần chính (Principal Components) bằng cách biến đổi tuyến tính không gian dữ liệu sao cho trục đầu tiên giữ lại phương sai (Variance) lớn nhất của dữ liệu, và các trục tiếp theo phải trực giao (Orthogonal) với các trục trước đó.
  - id: KP5_2
    content: Loại bỏ đa cộng tuyến và giảm chi phí tính toán
    keypoint_weight: 0.5
    description: Giúp nén dữ liệu, giảm hiện tượng quá khớp (Overfitting) bằng cách loại bỏ các thuộc tính bị dư thừa thông tin hoặc có tương quan cao (Multicollinearity), đồng thời giảm kích thước dữ liệu đầu vào giúp mô hình chạy nhanh hơn.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi cấu hình siêu tham số để tối ưu mạng nơ-ron bằng thuật toán Adam, hãy giải thích ý nghĩa logic của các tham số Beta1, Beta2 và hiện tượng gì xảy ra nếu thiết lập Learning Rate quá lớn từ đầu?
* **expected_key_points:**
  - id: KP6_1
    content: Ý nghĩa của tham số Beta1 và Beta2
    keypoint_weight: 0.5
    description: Beta1 là hệ số suy giảm lũy thừa cho khoảnh khắc bậc 1 (Momentum - vận tốc gradient cũ). Beta2 là hệ số suy giảm lũy thừa cho khoảnh khắc bậc 2 (RMSprop - bình phương gradient để tự thích ứng bước đi).
  - id: KP6_2
    content: Tác động của Learning Rate quá lớn lên đồ thị mất mát
    keypoint_weight: 0.5
    description: Khi Learning Rate quá lớn, hàm tối ưu sẽ thực hiện các bước nhảy quá rộng qua lại giữa các vách của hàm mất mát, gây ra hiện tượng dao động mạnh không thể hội tụ, làm tăng giá trị loss (Exploding Loss) hoặc làm mô hình phân kỳ.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong kiến trúc mạng CNN xử lý ảnh, hãy phân biệt sự khác nhau về mặt chức năng tính toán giữa tầng Transposed Convolution (Tích chập chuyển vị) và tầng Convolution (Tích chập) thông thường.
* **expected_key_points:**
  - id: KP7_1
    content: Tầng Convolution làm giảm không gian (Downsampling)
    keypoint_weight: 0.5
    description: Thực hiện phép nhân chập trượt filter để trích xuất đặc trưng cốt lõi, thường làm giảm kích thước chiều rộng và chiều cao của bản đồ đặc trưng đầu vào (Feature map).
  - id: KP7_2
    content: Tầng Transposed Convolution làm tăng không gian (Upsampling)
    keypoint_weight: 0.5
    description: Hoạt động ngược lại, dùng để khôi phục hoặc phóng to kích thước không gian (Spatial dimensions) từ một bản đồ đặc trưng nhỏ thành lớn hơn, thường ứng dụng trong các bài toán Image Segmentation (Phân đoạn hình ảnh) hoặc mô hình Generative (GAN, Autoencoder).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Khi sử dụng các mô hình học sâu lớn, tại sao kỹ thuật Mixed Precision Training (Huấn luyện độ chính xác hỗn hợp) lại giúp tối ưu hóa bộ nhớ GPU? Hãy phân tích vai trò của kỹ thuật Loss Scaling trong quy trình này.
* **expected_key_points:**
  - id: KP8_1
    content: Kết hợp hai kiểu dữ liệu FP16 và FP32 trên bộ nhớ
    keypoint_weight: 0.4
    description: Thay vì tính toán toàn bộ bằng số thực 32-bit (FP32), kỹ thuật này chuyển đổi các phép toán tính Forward và Backward của trọng số/activation sang số thực 16-bit (FP16) để tiết kiệm một nửa dung lượng VRAM và tận dụng phần cứng tăng tốc (như Tensor Cores). Tuy nhiên, một bản sao trọng số chính vẫn được giữ ở FP32 để cập nhật nhằm tránh sai số tích lũy.
  - id: KP8_2
    content: Vấn đề Underflow (Tràn dưới) của số thực FP16
    keypoint_weight: 0.3
    description: Kiểu dữ liệu FP16 có khoảng giá trị biểu diễn nhỏ hơn rất nhiều so với FP32. Trong lúc tính Backward, nhiều giá trị gradient cực nhỏ sẽ bị suy biến về bằng 0 tuyệt đối (Underflow), khiến mô hình không thể học.
  - id: KP8_3
    content: Cơ chế nhân tỷ xích của Loss Scaling
    keypoint_weight: 0.3
    description: Trước khi thực hiện lan truyền ngược, giá trị Loss sẽ được nhân với một hệ số tỷ xích lớn (Scale factor) để đẩy toàn bộ dải giá trị gradient lên vùng biểu diễn an toàn của FP16. Sau khi tính xong gradient và trước khi cập nhật trọng số, các gradient này sẽ được chia lại cho chính hệ số tỷ xích đó để trả về giá trị thực chính xác ban đầu.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong kiến trúc Transformer, tại sao cơ chế Multi-Head Attention lại vượt trội hơn Single-Head Attention thông thường? Hãy giải thích cơ chế toán học khi kết hợp các Head dữ liệu lại với nhau.
* **expected_key_points:**
  - id: KP9_1
    content: Khả năng học đa góc nhìn và ngữ cảnh không gian (Multiple Subspaces)
    keypoint_weight: 0.4
    description: Multi-Head Attention cho phép mô hình đồng thời chú ý và liên kết thông tin từ các không gian biểu diễn (Subspaces) khác nhau ở các vị trí khác nhau trong câu, thay vì chỉ tập trung vào một mối quan hệ ngữ cảnh duy nhất.
  - id: KP9_2
    content: Cơ chế tính toán Attention độc lập song song
    keypoint_weight: 0.3
    description: Các ma trận chiếu $Q, K, V$ ban đầu được phân tách hoặc chiếu tuyến tính độc lập thành $h$ tập ma trận nhỏ hơn. Hệ thống thực hiện tính toán phép toán Scaled Dot-Product Attention hoàn toàn song song trên từng Head độc lập này.
  - id: KP9_3
    content: Phép toán Concatenation và chiếu ma trận đầu ra ($W^O$)
    keypoint_weight: 0.3
    description: Kết quả đầu ra của tất cả các Head ($head_1, head_2, ..., head_h$) sẽ được nối liền mạch lại với nhau theo chiều ngang (Concatenate), sau đó nhân với một ma trận trọng số học được cuối cùng ($W^O$) để đưa dữ liệu về đúng kích thước chiều ẩn gốc (Hidden dimension).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Khi triển khai ứng dụng dùng Mô hình ngôn ngữ lớn (LLM), hãy phân biệt cơ chế toán học và sự khác biệt về khả năng kiểm soát dữ liệu giữa phương pháp In-Context Learning (Prompt Engineering/Few-shot) và Parameter-Efficient Fine-Tuning (PEFT như LoRA).
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế của In-Context Learning (Đóng băng trọng số)
    keypoint_weight: 0.4
    description: Không hề thay đổi hay cập nhật bất kỳ trọng số nào của LLM ($O(0)$ tham số cập nhật). Mô hình học và suy luận trực tiếp dựa trên các ví dụ mẫu (Examples) hoặc ngữ cảnh được nhét vào trong Context Window thông qua phép toán Attention lúc chạy Inference. Ràng buộc lớn là bị giới hạn bởi độ dài context window và tiêu tốn chi phí token lặp lại cho mỗi request.
  - id: KP10_2
    content: Cơ chế phân rã ma trận hạng thấp của LoRA (PEFT)
    keypoint_weight: 0.4
    description: Đóng băng hoàn toàn các ma trận trọng số gốc của mô hình ($W_0 \in \mathbb{R}^{d \times k}$). Thay vào đó, nó chèn thêm các nhánh ma trận bổ trợ nhỏ được phân rã thành tích của hai ma trận hạng thấp (Low-rank matrices) $A \in \mathbb{R}^{d \times r}$ và $B \in \mathbb{R}^{r \times k}$ với tham số hạng $r \ll d$. Chỉ có ma trận $A$ và $B$ là được huấn luyện cập nhật trọng số.
  - id: KP10_3
    content: So sánh về lưu trữ và hiệu năng tích hợp (Weight Merging)
    keypoint_weight: 0.2
    description: LoRA giúp giảm lượng tham số cần huấn luyện và lưu trữ đi hàng nghìn lần so với Full Fine-tuning, cho phép dễ dàng hoán đổi các adapter cho các task khác nhau. Tại thời điểm deploy, trọng số của LoRA ($\Delta W = B \cdot A$) có thể được cộng trực tiếp vào ma trận gốc ($W = W_0 + \Delta W$), giúp thời gian Latency lúc inference bằng đúng mô hình gốc mà không bị phình to chuỗi token đầu vào như In-Context Learning.