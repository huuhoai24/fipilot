# Bộ Câu Hỏi Phỏng Vấn Data Scientist (Level 1)

* **Role:** Data Scientist
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong các bài toán phân lớp (Classification), hãy giải thích ý nghĩa và sự khác biệt bản chất giữa hai chỉ số đo lường hiệu năng: Precision (Độ chính xác) và Recall (Độ bao phủ). Nêu một kịch bản thực tế cần ưu tiên tối ưu hóa chỉ số Recall hơn Precision.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa chỉ số Precision và logic đo lường
    keypoint_weight: 0.4
    description: Precision đo lường tỷ lệ các mẫu thực sự thuộc nhãn Positive trong số tất cả các mẫu mà mô hình đã dự đoán là Positive (TP / (TP + FP)). Chỉ số này tập trung giảm thiểu sai lầm báo động giả (False Positive).
  - id: KP1_2
    content: Định nghĩa chỉ số Recall và logic đo lường
    keypoint_weight: 0.4
    description: Recall đo lường tỷ lệ các mẫu được mô hình dự đoán chính xác là Positive trên tổng số tất cả các mẫu thực tế mang nhãn Positive (TP / (TP + FN)). Chỉ số này tập trung giảm thiểu sai lầm bỏ sót (False Negative).
  - id: KP1_3
    content: Kịch bản thực tế ưu tiên tối ưu Recall kèm lý do
    keypoint_weight: 0.2
    description: Ví dụ trong bài toán chẩn đoán y tế (phát hiện bệnh hiểm nghèo) hoặc phát hiện gian lận thẻ tín dụng. Việc bỏ sót một ca bệnh thực tế (False Negative) nguy hiểm hơn rất nhiều so với việc báo động nhầm một người khỏe mạnh (False Positive), vì người bị báo nhầm có thể làm xét nghiệm chuyên sâu lại.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong xử lý dữ liệu (Data Preprocessing), hiện tượng Missing Values (Dữ liệu bị khuyết thiếu) ảnh hưởng thế nào đến thuật toán và hãy nêu hai phương pháp cơ bản để xử lý (Imputation) cho các biến số liên tục (Numerical Variables).
* **expected_key_points:**
  - id: KP2_1
    content: Hệ quả của Missing Values đối với các thuật toán học máy
    keypoint_weight: 0.4
    description: Đa số các thuật toán Machine Learning (như Linear Regression, SVM) không thể tiếp nhận input đầu vào chứa giá trị khuyết thiếu và sẽ báo lỗi. Hiện tượng này làm mất mát thông tin, làm giảm kích thước mẫu huấn luyện nếu xóa bỏ bừa bãi và có thể gây lệch (bias) kết quả dự báo.
  - id: KP2_2
    content: Phương pháp gán giá trị bằng thống kê tập trung (Mean/Median Imputation)
    keypoint_weight: 0.3
    description: Thay thế các giá trị bị khuyết bằng giá trị trung bình (Mean) hoặc trung vị (Median) tính toán từ các mẫu không khuyết thiếu của chính biến số đó. Gán trung vị (Median) thường an toàn hơn khi phân phối dữ liệu bị lệch hoặc chứa nhiều ngoại lai (Outliers).
  - id: KP2_3
    content: Phương pháp gán giá trị dựa trên mô hình hoặc giá trị cố định (Model-based/Constant Imputation)
    keypoint_weight: 0.3
    description: Sử dụng một giá trị cố định đại diện đặc biệt (như 0) hoặc áp dụng thuật toán học máy ngầm (như KNN Imputer, MICE) để dự đoán giá trị khuyết thiếu dựa trên mối tương quan với các đặc trưng khác trong dữ liệu.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy giải thích khái niệm Overfitting (Quá khớp) trong huấn luyện mô hình học máy. Làm thế nào bạn có thể nhận diện một mô hình đang bị Overfitting thông qua kết quả đo lường trên tập huấn luyện (Train set) và tập kiểm thử (Test set)?
* **expected_key_points:**
  - id: KP3_1
    content: Bản chất lý thuyết của hiện tượng Overfitting
    keypoint_weight: 0.5
    description: Overfitting xảy ra khi mô hình học quá kỹ cả các chi tiết nhiễu (Noise) và các biến động ngẫu nhiên trong tập dữ liệu huấn luyện thay vì học quy luật tổng quát. Điều này khiến mô hình mất đi khả năng tổng quát hóa (Generalization) trên dữ liệu mới chưa từng thấy.
  - id: KP3_2
    content: Cơ chế nhận diện qua sự chênh lệch hiệu năng (Train vs Test Performance)
    keypoint_weight: 0.5
    description: Nhận diện khi mô hình đạt chỉ số hiệu năng cực kỳ cao hoặc sai số (Error) rất thấp trên tập Train, nhưng khi đánh giá trên tập Test (hoặc Validation) thì hiệu năng giảm sút nghiêm trọng hoặc sai số tăng vọt.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi huấn luyện mô hình Linear Regression (Hồi quy tuyến tính), hiện tượng Multicollinearity (Đa cộng tuyến) là gì? Hiện tượng này gây ra hậu quả tiêu cực nào cho việc giải thích trọng số mô hình và cách nhận diện cơ bản là gì?
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa bản chất của Multicollinearity
    keypoint_weight: 0.4
    description: Đa cộng tuyến là hiện tượng hai hoặc nhiều biến độc lập (Features) trong mô hình hồi quy tuyến tính có mối tương quan tuyến tính rất mạnh mẽ hoặc phụ thuộc lẫn nhau, làm mất đi tính độc lập của các đặc trưng đầu vào.
  - id: KP4_2
    content: Hậu quả tiêu cực lên hệ số hồi quy (Coefficients)
    keypoint_weight: 0.3
    description: Làm cho việc ước lượng các trọng số hệ số hồi quy trở nên không ổn định, có phương sai lớn. Một thay đổi nhỏ trong dữ liệu có thể làm đảo lộn hoàn toàn giá trị hoặc dấu của hệ số, khiến ta không thể giải thích chính xác mức độ đóng góp cô lập của từng biến đối với biến mục tiêu.
  - id: KP4_3
    content: Cách nhận diện thông qua ma trận tương quan hoặc chỉ số VIF
    keypoint_weight: 0.3
    description: Nhận diện bằng cách rà soát ma trận tương quan (Correlation Matrix) tìm các cặp biến có hệ số Pearson quá cao (> 0.8), hoặc tính toán chỉ số nhân tử phóng đại phương sai VIF (Variance Inflation Factor), khi VIF vượt ngưỡng 5 hoặc 10 chứng tỏ biến đó bị đa cộng tuyến nặng.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích điểm khác biệt cốt lõi về mặt kiến trúc, cơ chế gộp mô hình và cách thức giảm thiểu sai số giữa hai phương pháp học tập kết hợp (Ensemble Learning): Bagging (như Random Forest) và Boosting (như Gradient Boosting/XGBoost).
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế huấn luyện và gộp mô hình của Bagging
    keypoint_weight: 0.4
    description: Bagging xây dựng các mô hình nền tảng (Base models - thường là các cây quyết định sâu) một cách song song và độc lập trên các tập dữ liệu con được lấy mẫu lại có hoàn tác (Bootstrap samples). Kết quả cuối cùng được gộp bằng cách lấy trung bình (Regression) hoặc bỏ phiếu đa số (Classification).
  - id: KP5_2
    content: Cơ chế huấn luyện tuần tự chuỗi của Boosting
    keypoint_weight: 0.4
    description: Boosting xây dựng các mô hình nền tảng (thường là các cây quyết định nông/Weak learners) một cách tuần tự (Sequentially). Mô hình sau được thiết kế để tập trung sửa chữa những sai lầm, tối ưu hàm mất mát dựa trên phần dư (Residuals) hoặc trọng số lỗi của mô hình trước nó.
  - id: KP5_3
    content: Khác biệt bản chất trong việc giảm thiểu Bias và Variance
    keypoint_weight: 0.2
    description: Bagging kết hợp các cây có tính linh hoạt cao (High variance, low bias) nhằm mục đích chính là giảm Phương sai (Variance), chống Overfitting. Boosting kết hợp các cây có độ phức tạp thấp để giảm dần Sai số chệch (Bias) qua từng bước, nhưng dễ bị Overfitting nếu dữ liệu chứa nhiều nhiễu.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi đối mặt với bài toán dữ liệu bị mất cân bằng nhãn nghiêm trọng (Imbalanced Data - ví dụ tỷ lệ nhãn lỗi chỉ chiếm 1%), hãy giải thích nguyên lý hoạt động của kỹ thuật trích xuất lại dữ liệu SMOTE (Synthetic Minority Over-sampling Technique). Kỹ thuật này tối ưu hơn phương pháp Random Over-sampling truyền thống ở điểm nào?
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên lý sinh dữ liệu nhân tạo dựa trên thuật toán hình học của SMOTE
    keypoint_weight: 0.5
    description: SMOTE không sao chép nguyên bản. Thuật toán tìm kiếm các điểm dữ liệu lân cận gần nhất (K-Nearest Neighbors) thuộc nhóm thiểu số của một mẫu hiện tại. Sau đó, nó chọn ngẫu nhiên một dòng lân cận và sinh ra một điểm dữ liệu nhân tạo mới nằm trên đoạn thẳng nối giữa mẫu gốc và điểm lân cận đó trong không gian đặc trưng.
  - id: KP6_2
    content: Ưu điểm giải quyết Overfitting so với Random Over-sampling
    keypoint_weight: 0.5
    description: Random Over-sampling thuần túy chỉ sao chép nhân bản y nguyên các bản ghi thiểu số có sẵn, dễ khiến mô hình bị học vẹt và Overfitting nặng nề trên vùng ranh giới quyết định. SMOTE tạo ra các mẫu mới có tính đa dạng sinh học cao hơn trong không gian hình học, giúp làm mịn vùng ranh giới quyết định (Decision Boundary) và tăng tính tổng quát hóa của mô hình.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong các thuật toán phân cụm không giám sát (Unsupervised Clustering), hãy giải thích nguyên lý hoạt động của thuật toán K-Means. Làm thế nào để bạn lựa chọn số lượng cụm K tối ưu thông qua kỹ thuật Elbow Method (Phương pháp khuỷu tay)?
* **expected_key_points:**
  - id: KP7_1
    content: Quy trình lặp tối ưu khoảng cách của thuật toán K-Means
    keypoint_weight: 0.5
    description: K-Means khởi tạo ngẫu nhiên K tâm cụm (Centroids). Sau đó lặp lại chuỗi hai bước: (1) Gán mỗi điểm dữ liệu vào tâm cụm gần nó nhất dựa trên khoảng cách (thường là khoảng cách Euclidean); (2) Cập nhật lại vị trí các tâm cụm bằng cách lấy giá trị trung bình tọa độ của tất cả các điểm thuộc cụm đó. Vòng lặp dừng lại khi vị trí các tâm cụm không còn thay đổi.
  - id: KP7_2
    content: Cơ chế lựa chọn K dựa trên đồ thị tối ưu chỉ số WCSS của Elbow Method
    keypoint_weight: 0.5
    description: Chạy K-Means với dải giá trị K tăng dần và tính toán tổng bình phương khoảng cách trong nội bộ cụm WCSS (Within-Cluster Sum of Squares) cho mỗi K. Vẽ đồ thị giữa K và WCSS; khi K tăng, WCSS sẽ giảm dần. Điểm "khuỷu tay" (Elbow) là vị trí mà tại đó tốc độ giảm của WCSS bắt đầu chậm lại rõ rệt. Giá trị K tại điểm rẽ gập này là số lượng cụm tối ưu cân bằng giữa độ chính xác phân cụm và độ phức tạp mô hình.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích sâu bản chất toán học của định lý Trade-off giữa Bias (Sai số chệch) và Variance (Phương sai) trong lỗi dự báo tổng quát (Generalization Error) của mô hình Machine Learning. Việc tăng độ phức tạp (Model Complexity) của mô hình ảnh hưởng đến hai thành phần này như thế nào?
* **expected_key_points:**
  - id: KP8_1
    content: Phân rã toán học của hàm lỗi dự báo (Error Decomposition)
    keypoint_weight: 0.4
    description: Lỗi bình phương trung bình tổng quát của mô hình được chứng minh phân rã thành tổng của ba thành phần toán học độc lập: Total Error = Bias^2 + Variance + Irreducible Noise. Trong đó Irreducible Noise là nhiễu nội tại của dữ liệu không thể triệt tiêu.
  - id: KP8_2
    content: Bản chất logic của Bias và Variance đối với hàm quy luật
    keypoint_weight: 0.3
    description: Bias đo lường mức độ sai lệch giữa giá trị dự báo trung bình của mô hình so với giá trị thực tế chính xác (thể hiện việc mô hình bị đơn giản hóa quá mức - Underfitting). Variance đo lường mức độ biến động của các kết quả dự báo của mô hình khi huấn luyện trên các tập dữ liệu khác nhau (thể hiện mức độ nhạy cảm với dữ liệu huấn luyện - Overfitting).
  - id: KP8_3
    content: Động lực biến đổi nghịch chiều khi thay đổi độ phức tạp mô hình
    keypoint_weight: 0.3
    description: Bias và Variance biến đổi nghịch chiều nhau khi thay đổi độ phức tạp mô hình. Khi tăng độ phức tạp mô hình (ví dụ tăng độ sâu của cây, tăng bậc đa thức), mô hình khớp tốt hơn nên Bias giảm dần, đổi lại mô hình trở nên nhạy cảm hơn nên Variance tăng vọt. Mục tiêu của Data Scientist là tìm điểm tối ưu tổng hợp (Sweet spot) để tổng sai số nhỏ nhất.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Khi xây dựng mô hình Logistic Regression hoặc Neural Network để phân lớp nhị phân, tại sao hàm Log Loss (Cross-Entropy Loss) lại được ưu tiên sử dụng làm hàm mất mát thay vì hàm lỗi bình phương trung bình MSE (Mean Squared Error)? Phân tích dựa trên khía cạnh đạo hàm và hình học tối ưu hóa.
* **expected_key_points:**
  - id: KP9_1
    content: Vấn đề độ dốc biến mất do hàm kích hoạt Sigmoid khi kết hợp với MSE
    keypoint_weight: 0.4
    description: Khi sử dụng hàm kích hoạt Sigmoid ở đầu ra, đạo hàm của Sigmoid tiến về sát giá trị 0 khi mô hình dự báo rất sai nhãn (giá trị tiến gần biên 0 hoặc 1). Nếu dùng MSE, đạo hàm của hàm mất mát đối với trọng số chứa thành phần đạo hàm Sigmoid này, dẫn đến hiện tượng độ dốc bị triệt tiêu (Gradient Vanishing), khiến thuật toán Gradient Descent học cực kỳ chậm hoặc bị kẹt.
  - id: KP9_2
    content: Cơ chế triệt tiêu toán học thông minh của hàm Log Loss
    keypoint_weight: 0.4
    description: Hàm mất mát Cross-Entropy sử dụng phép toán logarithm (ln). Khi tính đạo hàm của Cross-Entropy kết hợp với Sigmoid, thành phần logarithm này triệt tiêu hoàn toàn lượng đạo hàm của Sigmoid ở mẫu số. Kết quả đạo hàm cuối cùng thu được chỉ tỷ lệ tuyến tính với độ sai lệch giữa giá trị dự báo và thực tế (y - \hat{y}), giúp Gradient Descent cập nhật trọng số mạnh mẽ ngay cả khi mô hình dự báo rất sai.
  - id: KP9_3
    content: Tính chất lồi (Convexity) hỗ trợ tối ưu hóa toàn cục
    keypoint_weight: 0.2
    description: Khi kết hợp với mô hình tuyến tính, Log Loss đảm bảo hàm mất mát là một hàm lồi (Convex function), chỉ có duy nhất một điểm tối ưu toàn cục (Global Minimum), giúp thuật toán tối ưu hóa Gradient Descent cam kết hội tụ thành công. Trong khi MSE kết hợp Sigmoid tạo ra bề mặt phi lồi (Non-convex) có nhiều điểm tối ưu cục bộ (Local Minima).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong các bài toán học máy nâng cao hoặc phân tích thử nghiệm A/B Testing, kỹ thuật Tái lấy mẫu Bootstrap (Bootstrapping) hoạt động ra sao và nó giúp giải quyết bài toán gì khi ta cần ước lượng khoảng tin cậy (Confidence Interval) của một tham số thống kê phức tạp mà không rõ phân phối gốc?
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế lấy mẫu lặp đi lặp lại có hoàn tác của Bootstrap
    keypoint_weight: 0.4
    description: Từ tập dữ liệu gốc gồm N mẫu, Bootstrap tiến hành rút thăm ngẫu nhiên ra các tập dữ liệu con (Bootstrap samples) cũng có kích thước đúng bằng N, với điều kiện cho phép một mẫu có thể được rút trúng nhiều lần (Sampling with replacement - lấy mẫu có hoàn tác). Tiến trình này được lặp lại hàng nghìn lần để tạo ra hàng nghìn tập mẫu con độc lập.
  - id: KP10_2
    content: Xây dựng phân phối thực nghiệm của tham số thống kê (Empirical Distribution)
    keypoint_weight: 0.4
    description: Trên mỗi tập mẫu con Bootstrap, ta tính toán giá trị của tham số thống kê cần ước lượng (ví dụ: trung vị Median, tỷ lệ phần trăm Percentile, hoặc chỉ số Gini). Tập hợp hàng nghìn giá trị thu được này cấu thành nên một Phân phối thực nghiệm (Empirical Distribution) của tham số đó, mô phỏng lại phân phối chọn mẫu thực tế.
  - id: KP10_3
    content: Xác định khoảng tin cậy phi tham số độc lập với giả định phân phối
    keypoint_weight: 0.2
    description: Dựa trên phân phối thực nghiệm thu được, ta có thể xác định trực tiếp Khoảng tin cậy phi tham số (Non-parametric Confidence Interval) bằng phương pháp phân vị (Percentile method) mà không cần phụ thuộc vào bất kỳ giả định toán học cứng nhắc nào về phân phối của tổng thể gốc (như giả định phân phối chuẩn Central Limit Theorem).