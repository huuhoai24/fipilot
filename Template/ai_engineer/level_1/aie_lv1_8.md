# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 1)

* **Role:** AI Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong huấn luyện mạng nơ-ron sâu, mục đích cốt lõi của hai giai đoạn Forward Propagation (Lan truyền tiến) và Backward Propagation (Lan truyền ngược) là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Mục đích của Forward Propagation (Tính giá trị đầu ra và độ lỗi)
    keypoint_weight: 0.5
    description: Lan truyền dữ liệu đầu vào qua các tầng của mạng để tính toán giá trị dự đoán, từ đó so sánh với nhãn thực tế để xác định giá trị của hàm mất mát (Loss function).
  - id: KP1_2
    content: Mục đích của Backward Propagation (Tính đạo hàm và cập nhật trọng số)
    keypoint_weight: 0.5
    description: Sử dụng quy tắc chuỗi (Chain Rule) để tính toán đạo hàm riêng (Gradients) của hàm mất mát đối với từng trọng số, làm cơ sở để thuật toán tối ưu cập nhật tham số nhằm giảm thiểu độ lỗi.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt sự khác biệt về mặt logic toán học và ngữ cảnh áp dụng giữa hai hàm mất mát: Binary Cross-Entropy Loss và Categorical Cross-Entropy Loss.
* **expected_key_points:**
  - id: KP2_1
    content: Ngữ cảnh phân loại nhị phân (Binary Classification)
    keypoint_weight: 0.5
    description: Binary Cross-Entropy được áp dụng khi bài toán chỉ có 2 lớp đối lập (0 và 1), kết hợp với hàm kích hoạt Sigmoid ở tầng đầu ra để dự đoán xác suất độc lập.
  - id: KP2_2
    content: Ngữ cảnh phân loại đa lớp loại trừ (Multi-class Classification)
    keypoint_weight: 0.5
    description: Categorical Cross-Entropy dùng cho bài toán có từ 3 lớp trở lên mang tính chất loại trừ lẫn nhau, yêu cầu nhãn đầu vào dạng mã hóa One-hot và kết hợp với hàm kích hoạt Softmax ở tầng đầu ra.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong tiền xử lý dữ liệu dạng bảng (Tabular Data), sự hiện diện của giá trị khuyết (Missing Values) gây ra hệ quả gì và nêu hai phương pháp thống kê cơ bản để điền khuyết (Imputation)?
* **expected_key_points:**
  - id: KP3_1
    content: Hệ quả của dữ liệu khuyết đối với thư viện tính toán
    keypoint_weight: 0.4
    description: Gây lỗi cho các phép toán đại số ma trận trong thư viện (như lỗi NaN trong NumPy/Scikit-Learn), khiến mô hình không thể thực thi huấn luyện hoặc làm sai lệch phân phối đặc trưng.
  - id: KP3_2
    content: Các phương pháp điền khuyết dựa trên số liệu thống kê đại diện
    keypoint_weight: 0.6
    description: Xử lý bằng cách điền khuyết bằng giá trị Mean (Trung bình) hoặc Median (Trung vị) đối với thuộc tính số liên tục, hoặc điền bằng giá trị Mode (Yếu vị/Giá trị xuất hiện nhiều nhất) đối với thuộc tính phân loại.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thuật toán Random Forest hoạt động dựa trên kỹ thuật Ensemble Learning nào? Tại sao nó lại kiểm soát hiện tượng Overfitting tốt hơn một cây quyết định (Decision Tree) đơn lẻ?
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế lấy mẫu Bagging và thuộc tính ngẫu nhiên
    keypoint_weight: 0.5
    description: Random Forest xây dựng nhiều cây quyết định song song, mỗi cây được huấn luyện trên một tập con dữ liệu lấy mẫu ngẫu nhiên có hoàn lại (Bootstrap sample) và tại mỗi nút phân nhánh chỉ chọn ngẫu nhiên một nhóm các thuộc tính (Features subset).
  - id: KP4_2
    content: Cơ chế bỏ phiếu số đông giúp giảm phương sai (Variance)
    keypoint_weight: 0.5
    description: Kết quả cuối cùng được tổng hợp từ việc bỏ phiếu số đông hoặc tính trung bình từ tất cả các cây. Việc kết hợp nhiều cây có thuộc tính không tương quan giúp triệt tiêu sai số ngẫu nhiên và giảm mạnh Variance tổng thể.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Kỹ thuật giảm số chiều dữ liệu Principal Component Analysis (PCA) hoạt động dựa trên nguyên lý toán học nào và mục đích sử dụng của nó trong tiền xử lý dữ liệu là gì?
* **expected_key_points:**
  - id: KP5_1
    content: Tìm không gian mới cực đại hóa phương sai và trực giao
    keypoint_weight: 0.5
    description: PCA thực hiện biến đổi tuyến tính không gian để tìm các trục tọa độ mới gọi là các thành phần chính (Principal Components) sao cho trục đầu tiên giữ lại phương sai lớn nhất của dữ liệu và các trục sau trực giao với các trục trước.
  - id: KP5_2
    content: Loại bỏ đa cộng tuyến và giảm chiều dữ liệu
    keypoint_weight: 0.5
    description: Giúp nén dữ liệu đầu vào, loại bỏ các thuộc tính dư thừa thông tin hoặc có tương quan cao (Multicollinearity), giảm thiểu chi phí tính toán và kiểm soát Overfitting.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi tối ưu mạng nơ-ron bằng thuật toán Adam, hãy giải thích ý nghĩa logic của các tham số Beta1, Beta2 và tác động khi thiết lập Learning Rate quá lớn.
* **expected_key_points:**
  - id: KP6_1
    content: Ý nghĩa hệ số suy giảm lũy thừa Beta1 và Beta2
    keypoint_weight: 0.5
    description: Beta1 điều khiển khoảnh khắc bậc 1 (Momentum - lưu giữ vận tốc gradient cũ). Beta2 điều khiển khoảnh khắc bậc 2 (RMSprop - lưu giữ bình phương gradient để tự thích ứng bước đi).
  - id: KP6_2
    content: Hiện tượng dao động loss do Learning Rate quá lớn
    keypoint_weight: 0.5
    description: Thiết lập Learning Rate quá lớn khiến các bước nhảy cập nhật tham số vượt quá điểm tối ưu, gây ra hiện tượng đồ thị mất mát dao động mạnh không thể hội tụ hoặc bị phân kỳ.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong kiến trúc mạng CNN xử lý ảnh, hãy phân biệt sự khác biệt về mặt chức năng tính toán giữa tầng Transposed Convolution (Tích chập chuyển vị) và tầng Convolution thông thường.
* **expected_key_points:**
  - id: KP7_1
    content: Tầng Convolution thực hiện giảm kích thước không gian (Downsampling)
    keypoint_weight: 0.5
    description: Sử dụng bộ lọc trượt quét để trích xuất các đặc trưng cốt lõi từ thấp đến cao, làm giảm kích thước chiều rộng và chiều cao của bản đồ đặc trưng (Feature map).
  - 	id: KP7_2
    content: Tầng Transposed Convolution thực hiện tăng kích thước không gian (Upsampling)
    keypoint_weight: 0.5
    description: Sử dụng phép toán cuộn ngược nhằm khôi phục, mở rộng hoặc phóng to kích thước hình học không gian của Feature map, thường ứng dụng trong bài toán Image Segmentation hoặc mạng Generative.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Khi huấn luyện các mạng học sâu lớn, tại sao kỹ thuật Mixed Precision Training (Huấn luyện độ chính xác hỗn hợp) giúp tối ưu bộ nhớ GPU? Hãy phân tích vai trò của kỹ thuật Loss Scaling trong quy trình này.
* **expected_key_points:**
  - id: KP8_1
    content: Tối ưu bộ nhớ nhờ kết hợp kiểu dữ liệu FP16 và FP32
    keypoint_weight: 0.4
    description: Chuyển đổi các phép toán tính Forward và Backward của trọng số sang số thực 16-bit (FP16) để tiết kiệm một nửa dung lượng VRAM và tận dụng phần cứng Tensor Cores tăng tốc, trong khi vẫn giữ một bản sao trọng số ở FP32 để cập nhật chính xác.
  - id: KP8_2
    content: Nguy cơ tràn dưới (Underflow) của gradient trên định dạng FP16
    keypoint_weight: 0.3
    description: Do FP16 có dải biểu diễn số nhỏ hơn FP32 rất nhiều, các giá trị gradient cực nhỏ tính được khi Backward dễ bị suy biến về bằng 0 tuyệt đối (Underflow) khiến mạng không thể cập nhật.
  - id: KP8_3
    content: Cơ chế nhân hệ số tỷ xích của Loss Scaling
    keypoint_weight: 0.3
    description: Nhân giá trị Loss với một hệ số lớn trước khi Backward để đẩy dải gradient lên vùng biểu diễn an toàn của FP16, sau đó chia lại cho chính hệ số đó trước khi cập nhật trọng số chính nhằm trả về giá trị thực tế.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong kiến trúc Transformer, tại sao cơ chế Multi-Head Attention lại vượt trội hơn Single-Head Attention? Hãy giải thích quy trình toán học khi kết hợp các Head dữ liệu lại với nhau ở đầu ra.
* **expected_key_points:**
  - id: KP9_1
    content: Khả năng học đa góc nhìn trong không gian biểu diễn (Subspaces)
    keypoint_weight: 0.4
    description: Multi-Head Attention cho phép mô hình đồng thời chú ý và liên kết thông tin từ các không gian biểu diễn khác nhau ở các vị trí khác nhau trong câu, tăng cường khả năng hiểu ngữ cảnh phức tạp.
  - id: KP9_2
    content: Cơ chế tính Attention độc lập song song
    keypoint_weight: 0.3
    description: Các ma trận Query, Key, Value ban đầu được chiếu tuyến tính thành nhiều tập ma trận nhỏ hơn để tính toán phép toán Scaled Dot-Product Attention hoàn toàn song song trên từng Head độc lập.
  - id: KP9_3
    content: Phép toán Concatenation và phép chiếu ma trận đầu ra ($W^O$)
    keypoint_weight: 0.3
    description: Kết quả đầu ra của tất cả các Head sẽ được nối liền mạch lại với nhau theo chiều ngang (Concatenate), sau đó nhân với một ma trận trọng số học được cuối cùng ($W^O$) để đưa dữ liệu về đúng kích thước chiều ẩn gốc.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Khi triển khai ứng dụng sử dụng Mô hình ngôn ngữ lớn (LLM), hãy phân biệt cơ chế toán học và sự khác biệt về tham số giữa phương pháp In-Context Learning (Prompt/Few-shot) và Parameter-Efficient Fine-Tuning (PEFT như LoRA).
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế đóng băng trọng số của In-Context Learning
    keypoint_weight: 0.4
    description: Không thay đổi hay cập nhật bất kỳ trọng số nào của LLM ($O(0)$ tham số cập nhật). Mô hình suy luận trực tiếp dựa trên ngữ cảnh nhét vào Context Window qua phép toán Attention lúc chạy Inference. Ràng buộc lớn là bị giới hạn bởi độ dài context window và tiêu tốn chi phí token lặp lại.
  - id: KP10_2
    content: Cơ chế phân rã ma trận hạng thấp của LoRA (PEFT)
    keypoint_weight: 0.4
    description: Đóng băng hoàn toàn ma trận trọng số gốc ($W_0 \in \mathbb{R}^{d \times k}$) và chèn thêm nhánh ma trận bổ trợ song song được phân rã thành tích của hai ma trận hạng thấp $A \in \mathbb{R}^{d \times r}$ và $B \in \mathbb{R}^{r \times k}$ với hạng $r \ll d$. Chỉ có ma trận $A$ và $B$ là được huấn luyện cập nhật.
  - id: KP10_3
    content: Hiệu năng tích hợp thông qua cộng gộp trọng số (Weight Merging)
    keypoint_weight: 0.2
    description: LoRA giảm lượng tham số lưu trữ đi hàng nghìn lần so với Full Fine-tuning. Tại thời điểm triển khai, trọng số của LoRA ($\Delta W = B \cdot A$) có thể được cộng trực tiếp vào ma trận gốc ($W = W_0 + \Delta W$), giúp thời gian Latency lúc inference bằng đúng mô hình gốc mà không bị phình to chuỗi token đầu vào.