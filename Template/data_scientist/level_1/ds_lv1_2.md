# Bộ Câu Hỏi Phỏng Vấn Data Scientist (Level 1)

* **Role:** Data Scientist
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong giai đoạn chuẩn bị dữ liệu (Data Preprocessing), hãy phân biệt sự khác biệt cơ bản về mặt công thức toán học và mục đích sử dụng giữa hai kỹ thuật chuẩn hóa đặc trưng: Min-Max Scaling (Normalization) và Standardization (Z-score Normalization).
* **expected_key_points:**
  - id: KP1_1
    content: Nguyên lý và công thức của Min-Max Scaling
    keypoint_weight: 0.5
    description: Biến đổi dữ liệu bằng cách trừ đi giá trị nhỏ nhất và chia cho khoảng biến thiên (Max - Min), đưa dải giá trị của đặc trưng về một khoảng cố định (thường là từ 0 đến 1). Kỹ thuật này rất nhạy cảm với các giá trị ngoại lai (Outliers) vì giá trị cực biên sẽ làm co cụm phần lớn dữ liệu bình thường còn lại.
  - id: KP1_2
    content: Nguyên lý và công thức của Standardization (Z-score)
    keypoint_weight: 0.5
    description: Biến đổi dữ liệu bằng cách trừ đi giá trị trung bình (Mean) và chia cho độ lệch chuẩn (Standard Deviation), đưa dữ liệu về dạng có trung bình bằng 0 và độ lệch chuẩn bằng 1 (Phân phối chuẩn hóa). Kỹ thuật này không giới hạn biên cứng của dữ liệu và có khả năng chống chịu với giá trị ngoại lai tốt hơn Min-Max Scaling.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Khi xây dựng mô hình cây quyết định (Decision Tree), khái niệm Entropy dùng để đo lường điều gì? Một nút (Node) trong cây được coi là hoàn toàn thuần khiết (Pure Node) khi giá trị Entropy bằng bao nhiêu và ý nghĩa của nó là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa bản chất đo lường độ hỗn loạn của Entropy
    keypoint_weight: 0.5
    description: Trong lý thuyết thông tin và học máy, Entropy là chỉ số toán học dùng để đo lường mức độ hỗn loạn, độ bất định hoặc tính không đồng nhất của thông tin thuộc một tập dữ liệu nhãn.
  - id: KP2_2
    content: Trạng thái thuần khiết tuyệt đối khi Entropy bằng 0
    keypoint_weight: 0.5
    description: Một nút đạt trạng thái thuần khiết tuyệt đối khi giá trị Entropy bằng 0. Ý nghĩa là tất cả các mẫu dữ liệu rơi vào nút đó đều thuộc về duy nhất một lớp nhãn mục tiêu (Pure node), không còn tính bất định, giúp cây đưa ra quyết định phân lớp chắc chắn tại nút đó.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong đánh giá mô hình học máy phân lớp nhị phân, đường cong ROC (Receiver Operating Characteristic) được vẽ dựa trên hai trục chỉ số nào? Chỉ số AUC (Area Under the Curve) đại diện cho điều gì và một mô hình dự báo ngẫu nhiên có AUC bằng bao nhiêu?
* **expected_key_points:**
  - id: KP3_1
    content: Thành phần cấu thành hai trục của đường cong ROC
    keypoint_weight: 0.4
    description: Đường cong ROC biểu diễn mối quan hệ đồ thị giữa True Positive Rate (TPR / Recall / Độ nhạy) trên trục tung và False Positive Rate (FPR / Tỷ lệ báo động nhầm, tính bằng 1 - Specificity) trên trục hoành khi thay đổi các ngưỡng quyết định (Classification Thresholds).
  - id: KP3_2
    content: Ý nghĩa định lượng khả năng phân tách của chỉ số AUC
    keypoint_weight: 0.4
    description: AUC đo lường toàn bộ không gian hình học nằm dưới đường cong ROC. Nó đại diện cho năng lực tổng quát của mô hình trong việc phân biệt và tách biệt chính xác giữa hai lớp nhãn (Positive và Negative). Giá trị AUC càng gần 1 chứng tỏ mô hình phân loại càng hoàn hảo.
  - id: KP3_3
    content: Giá trị AUC của mô hình dự báo ngẫu nhiên
    keypoint_weight: 0.2
    description: Một mô hình dự báo ngẫu nhiên hoàn toàn (Random guessing, giống như tung đồng xu) sẽ có giá trị AUC bằng 0.5, tương ứng với một đường thẳng chéo phân đôi đồ thị ROC.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thuật toán K-Nearest Neighbors (KNN) là một mô hình học máy dựa trên khoảng cách. Hãy giải thích cơ chế dự báo của KNN cho bài toán phân lớp và tại sao thuật toán này lại nhạy cảm với việc lựa chọn giá trị của tham số $K$ quá nhỏ hoặc quá lớn?
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế bỏ phiếu dựa trên khoảng cách hình học của KNN
    keypoint_weight: 0.4
    description: Khi có một điểm dữ liệu mới cần dự báo, KNN tính toán khoảng cách (như khoảng cách Euclidean) từ điểm đó tới tất cả các điểm trong tập huấn luyện. Sau đó chọn ra $K$ điểm lân cận gần nhất và tiến hành bỏ phiếu đa số (Majority voting) dựa trên nhãn của các điểm lân cận này để gán nhãn cho điểm mới.
  - id: KP4_2
    content: Hệ quả hiệu năng khi chọn giá trị $K$ quá nhỏ
    keypoint_weight: 0.3
    description: Khi chọn $K$ quá nhỏ (ví dụ $K=1$), ranh giới quyết định của mô hình sẽ trở nên cực kỳ phức tạp và răng cưa. Mô hình bị nhạy cảm quá mức với các điểm nhiễu (Noise) hoặc ngoại lai trong dữ liệu huấn luyện, dẫn đến hiện tượng Quá khớp (Overfitting).
  - id: KP4_3
    content: Hệ quả hiệu năng khi chọn giá trị $K$ quá lớn
    keypoint_weight: 0.3
    description: Khi chọn $K$ quá lớn (ví dụ $K$ tiến gần bằng tổng số mẫu), ranh giới quyết định bị làm mịn quá mức. Mô hình sẽ có xu hướng luôn dự báo nhãn thuộc về lớp đa số trong dữ liệu bất kể vị trí thực tế của điểm cần dự báo, dẫn đến hiện tượng Dưới khớp (Underfitting).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong kiểm định giả thuyết thống kê (Hypothesis Testing) phục vụ cho việc phân tích thử nghiệm A/B Testing, hãy phân biệt sự khác biệt bản chất giữa lỗi loại một (Type I Error) và lỗi loại hai (Type II Error). Việc tăng kích thước mẫu (Sample Size) ảnh hưởng đến lỗi loại hai như thế nào?
* **expected_key_points:**
  - id: KP5_1
    content: Bản chất bác bỏ sai của lỗi loại một (Type I Error / Alpha)
    keypoint_weight: 0.4
    description: Lỗi loại một xảy ra khi ta thực hiện bác bỏ giả thuyết không H0 trong khi thực tế H0 là hoàn toàn đúng (Báo động giả / False Positive). Ví dụ: Kết luận phương án thiết kế giao diện mới làm tăng tỷ lệ chuyển đổi nhưng thực tế nó không mang lại sự khác biệt nào.
  - id: KP5_2
    content: Bản chất bỏ sót của lỗi loại hai (Type II Error / Beta)
    keypoint_weight: 0.4
    description: Lỗi loại hai xảy ra khi ta chấp nhận hoặc không thể bác bỏ giả thuyết không H0 trong khi thực tế H0 là sai (Bỏ sót cơ hội / False Negative). Ví dụ: Không phát hiện ra sự cải tiến vượt trội của giao diện mới và giữ lại giao diện cũ.
  - id: KP5_3
    content: Tác động của kích thước mẫu lên lỗi loại hai và lực lượng kiểm định
    keypoint_weight: 0.2
    description: Việc gia tăng kích thước mẫu huấn luyện giúp thu hẹp phương sai sai số chọn mẫu, từ đó trực tiếp giảm thiểu xác suất xảy ra lỗi loại hai (Beta), đồng thời làm gia tăng sức mạnh lực lượng kiểm định thống kê (Statistical Power = 1 - Beta), giúp phát hiện các thay đổi nhỏ tốt hơn.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi huấn luyện mô hình hồi quy tuyến tính hoặc hồi quy Logistic, tại sao chúng ta thường áp dụng kỹ thuật Regularization (L1 Lasso hoặc L2 Ridge)? Hãy phân biệt cơ chế tác động lên các hệ số trọng số (Coefficients) giữa L1 và L2 Regularization.
* **expected_key_points:**
  - id: KP6_1
    content: Mục đích chống Overfitting bằng cách phạt hàm lỗi của Regularization
    keypoint_weight: 0.4
    description: Regularization thêm một thành phần phạt (Penalty term) dựa trên độ lớn của các hệ số trọng số vào hàm mất mát (Loss function). Mục đích nhằm ép các trọng số không được phình to quá mức, giảm độ phức tạp của mô hình để chống Overfitting và tăng khả năng tổng quát hóa.
  - id: KP6_2
    content: Cơ chế thu nhỏ trọng số về mức bằng 0 và trích chọn đặc trưng của L1 Lasso
    keypoint_weight: 0.3
    description: L1 Regularization (Lasso) cộng thêm tổng giá trị tuyệt đối của các trọng số vào hàm lỗi. Bản chất toán học của L1 giúp ép các hệ số trọng số của các biến không quan trọng về bằng 0 một cách tuyệt đối, đóng vai trò như một cơ chế tự động trích chọn đặc trưng (Feature Selection) tạo ra mô hình thưa thớt (Sparse model).
  - id: KP6_3
    content: Cơ chế thu nhỏ trọng số tiệm cận 0 của L2 Ridge
    keypoint_weight: 0.3
    description: L2 Regularization (Ridge) cộng thêm tổng bình phương của các trọng số vào hàm lỗi. Cơ chế này thu nhỏ đồng đều giá trị của tất cả các trọng số về sát mức 0 nhưng không bao giờ triệt tiêu chúng về bằng 0 tuyệt đối, giúp kiểm soát tốt hiện tượng đa cộng tuyến (Multicollinearity).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Thuật toán K-Means và thuật toán Hierarchical Clustering (Phân cụm phân cấp) đều dùng để phân cụm dữ liệu phi giám sát. Hãy phân biệt sự khác biệt cốt lõi về mặt triết lý khởi tạo cấu trúc cụm và cách thức hoạt động giữa hai thuật toán này.
* **expected_key_points:**
  - id: KP7_1
    content: Bản chất phân hoạch cố định dựa trên số K định trước của K-Means
    keypoint_weight: 0.5
    description: K-Means tiếp cận theo hướng phân hoạch (Partitioning), yêu cầu người dùng phải xác định cứng số lượng cụm K ngay từ đầu. Thuật toán hoạt động bằng cách lặp đi lặp lại việc cập nhật tâm cụm vật lý dựa trên khoảng cách, cố gắng tối ưu hóa tiêu chí khoảng cách trong nội bộ cụm.
  - id: KP7_2
    content: Bản chất xây dựng sơ đồ phân cấp dạng cây (Dendrogram) của Hierarchical Clustering
    keypoint_weight: 0.5
    description: Hierarchical Clustering tiếp cận theo hướng phân cấp, không yêu cầu xác định trước số cụm. Nó hoạt động bằng cách xây dựng một sơ đồ cấu trúc phân tầng dạng cây (Dendrogram) theo hai cơ chế: Gom cụm dần từ dưới lên (Agglomerative - coi mỗi điểm là một cụm rồi gộp các cụm gần nhau lại) hoặc chia tách từ trên xuống (Divisive). Người dùng có thể cắt cây tại các độ cao khác nhau để lấy số lượng cụm mong muốn sau khi thuật toán chạy xong.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Kỹ thuật Giảm chiều dữ liệu PCA (Principal Component Analysis) hoạt động dựa trên nguyên lý toán học nào để tìm ra các thành phần chính? Hãy giải thích mối liên quan giữa ma trận hiệp phương sai (Covariance Matrix), trị riêng (Eigenvalues) và vectơ riêng (Eigenvectors) trong tiến trình này.
* **expected_key_points:**
  - id: KP8_1
    content: Mục tiêu toán học tối đa hóa phương sai dữ liệu chiếu của PCA
    keypoint_weight: 0.4
    description: PCA thực hiện phép biến đổi tuyến tính để chiếu tập dữ liệu gốc từ không gian đa chiều về một không gian mới có số chiều nhỏ hơn, sao cho lượng thông tin được bảo toàn là lớn nhất. Tiêu chuẩn toán học để bảo toàn thông tin ở đây là tối đa hóa phương sai (Variance) của dữ liệu trên các trục tọa độ mới (Principal Components).
  - id: KP8_2
    content: Vai trò phân tích cấu trúc tương quan của Ma trận hiệp phương sai
    keypoint_weight: 0.3
    description: PCA tính toán ma trận hiệp phương sai (Covariance Matrix) từ tập dữ liệu đặc trưng đã được chuẩn hóa để đo lường và làm rõ cấu trúc mối tương quan tuyến tính chằng chịt giữa tất cả các cặp biến đặc trưng đầu vào hằng ngày.
  - id: KP8_3
    content: Ý nghĩa hình học của Vectơ riêng và Trị riêng trong việc xác định Trục thành phần chính
    keypoint_weight: 0.3
    description: Hệ thống thực hiện phân rã giá trị đặc trưng (Eigenvalue Decomposition) hoặc phân rã giá trị suy biến (SVD) trên ma trận hiệp phương sai. Các Vectơ riêng (Eigenvectors) xác định hướng hình học của các trục tọa độ mới (Trục thành phần chính). Các Trị riêng (Eigenvalues) tương ứng đo lường độ lớn của phương sai (lượng thông tin) mà trục đặc trưng đó nắm giữ, làm căn cứ để sắp xếp thứ tự ưu tiên và lựa chọn số lượng thành phần giữ lại.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong huấn luyện các mạng thần kinh nhân tạo sâu (Deep Neural Networks), hiện tượng Gradient Vanishing (Triệt tiêu đạo hàm) là gì? Hãy phân tích nguyên nhân bản chất xuất phát từ việc lựa chọn hàm kích hoạt (Activation Function) kết hợp toán tử lan truyền ngược (Backpropagation), và nêu hai giải pháp khắc phục ở mức kiến trúc.
* **expected_key_points:**
  - id: KP9_1
    content: Bản chất toán học và hệ quả của hiện tượng Gradient Vanishing
    keypoint_weight: 0.4
    description: Hiện tượng xảy ra khi các giá trị đạo hàm của hàm mất mát (Gradients) bị thu nhỏ tiệm cận về mức số 0 cực kỳ nhanh trong quá trình lan truyền ngược về các tầng đầu tiên (Early layers) của mạng. Hệ quả là trọng số của các tầng đầu gần như không được cập nhật, khiến mạng sâu không thể học được các đặc trưng vĩ mô cốt lõi.
  - id: KP9_2
    content: Nguyên nhân do phép nhân chuỗi đạo hàm của hàm Sigmoid/Tanh ở Backpropagation
    keypoint_weight: 0.3
    description: Do sử dụng các hàm kích hoạt phi tuyến tính có vùng bão hòa biên đạo hàm cực nhỏ như Sigmoid (đạo hàm lớn nhất là 0.25) hoặc Tanh (đạo hàm lớn nhất là 1.0). Khi thực hiện thuật toán lan truyền ngược (Backpropagation), quy tắc chuỗi (Chain Rule) bắt buộc thực hiện phép nhân liên tiếp các giá trị đạo hàm nhỏ này qua nhiều tầng, làm giá trị tích số bị triệt tiêu lũy thừa tiến về 0.
  - id: KP9_3
    content: Các giải pháp kỹ thuật khắc phục ở mức kiến trúc mạng
    keypoint_weight: 0.3
    description: Khắc phục bằng cách thay thế các hàm kích hoạt cũ bằng hàm ReLU (Rectified Linear Unit) hoặc các biến thể của nó (Leaky ReLU) vì đạo hàm của ReLU ở vùng dương luôn bằng 1, không làm thu nhỏ gradient; kết hợp áp dụng kỹ thuật chuẩn hóa theo lô Batch Normalization hoặc thiết kế các kết nối tắt vượt tầng (Skip Connections / Residual Connections như trong ResNet).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong mô hình Support Vector Machine (SVM), kỹ thuật "Kernel Trick" giải quyết bài toán gì đối với dữ liệu phi tuyến tính (Non-linear Data)? Hãy giải thích cơ chế toán học giúp Kernel Trick tối ưu hóa chi phí tính toán khi chuyển đổi không gian đặc trưng đa chiều.
* **expected_key_points:**
  - id: KP10_1
    content: Mục tiêu chuyển đổi không gian để tìm siêu phẳng phân tách tuyến tính
    keypoint_weight: 0.4
    description: Khi dữ liệu thô ở không gian gốc bị phân bổ phi tuyến tính phức tạp (không thể phân tách bằng một đường thẳng hay siêu phẳng), Kernel Trick hỗ trợ ánh xạ (Mapping) ngầm tập dữ liệu này lên một không gian đặc trưng mới có số chiều cao hơn rất nhiều (thậm chí vô hạn chiều), nơi mà dữ liệu trở nên phân tách tuyến tính được (Linearly separable).
  - id: KP10_2
    content: Cơ chế toán học tính toán trực tiếp tích vô hướng ở không gian thấp (Dot Product Optimization)
    keypoint_weight: 0.4
    description: Thay vì phải thực hiện tường minh phép toán chuyển đổi tất cả các điểm dữ liệu lên không gian cao (vốn cực kỳ tốn tài nguyên tính toán và bộ nhớ), hàm Kernel cho phép tính toán trực tiếp giá trị tích vô hướng (Dot product) của hai điểm trong không gian cao thông qua một biểu thức toán học thực thi ngay tại không gian gốc thấp ban đầu.
  - id: KP10_3
    content: Triệt tiêu rủi ro của "Lời nguyền đa chiều" (Curse of Dimensionality) lên hiệu năng tính toán
    keypoint_weight: 0.2
    description: Giúp thuật toán SVM tối ưu hóa hàm mục tiêu kép (Dual optimization problem) đạt hiệu năng cực cao, triệt tiêu hoàn toàn chi phí tính toán tường minh ở không gian vô hạn chiều, bảo vệ hệ thống khỏi các thảm họa sụp đổ tài nguyên xử lý dữ liệu lớn.