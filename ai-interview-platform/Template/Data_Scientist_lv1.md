# Bộ Câu Hỏi Phỏng Vấn Data Scientist (Level 1)

* **Role:** Data Scientist
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thống kê, sự khác biệt giữa hai đại lượng Mean (Giá trị trung bình) và Median (Số trung vị) là gì? Khi nào nên dùng Median thay vì Mean?
* **Đáp án mẫu:** - Mean là tổng tất cả các giá trị chia cho số lượng phần tử. Median là giá trị nằm chính giữa tập dữ liệu khi đã sắp xếp thứ tự.
  - Nên dùng Median khi tập dữ liệu xuất hiện các giá trị ngoại lai cực đoan (Outliers) hoặc dữ liệu bị lệch nghiêm trọng (Skewed), vì Mean rất dễ bị kéo lệch bởi Outliers còn Median thì không.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Khái niệm p-value trong kiểm định giả thuyết thống kê (Hypothesis Testing) mang ý nghĩa gì? Ngưỡng ý nghĩa 0.05 thường được dùng như thế nào?
* **Đáp án mẫu:** - p-value là xác suất quan sát được kết quả thực tế (hoặc cực đoan hơn) nếu giả thuyết không (Null Hypothesis - $H_0$) là đúng.
  - Nếu p-value < 0.05, chúng ta bác bỏ giả thuyết không $H_0$ và công nhận kết quả có ý nghĩa thống kê. Nếu p-value >= 0.05, chúng ta chưa có đủ bằng chứng để bác bỏ $H_0$.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong bài toán học máy, tại sao chúng ta cần thực hiện bước Khai phá dữ liệu (Exploratory Data Analysis - EDA)?
* **Đáp án mẫu:** EDA giúp Data Scientist hiểu được cấu trúc dữ liệu, phát hiện các giá trị bất thường (outliers), các ô dữ liệu trống (missing values), tìm ra mối quan hệ/độ tương quan giữa các biến, từ đó đưa ra hướng tiền xử lý và lựa chọn mô hình phù hợp.

---

## CÂU HỎI TRUNG BÌNH (4 câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Định lý Giới hạn Trung tâm (Central Limit Theorem - CLT) phát biểu điều gì và tại sao nó lại quan trọng trong phân tích thống kê?
* **Đáp án mẫu:** CLT phát biểu rằng: Khi kích thước mẫu đủ lớn (thường $n \ge 30$), phân phối của các giá trị trung bình mẫu sẽ xấp xỉ phân phối chuẩn (Normal Distribution), bất kể tổng thể ban đầu tuân theo phân phối nào. Định lý này cho phép áp dụng các kiểm định thống kê dạng tham số (như Z-test, T-test) lên các tập dữ liệu thực tế.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Hiện tượng Đa cộng tuyến (Multicollinearity) trong mô hình Hồi quy tuyến tính (Linear Regression) là gì và nó gây ra tác hại gì?
* **Đáp án mẫu:** - Định nghĩa: Là hiện tượng hai hoặc nhiều biến độc lập (features) trong mô hình có mối quan hệ tuyến tính mạnh với nhau.
  - Tác hại: Làm giảm độ tin cậy của việc ước lượng các hệ số hồi quy, khiến mô hình khó xác định chính xác mức độ tác động riêng lẻ của từng biến lên biến mục tiêu.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Đánh đổi Phương sai và Độ chệch (Bias-Variance Tradeoff) ảnh hưởng như thế nào đến khả năng tổng quát hóa của một mô hình học máy?
* **Đáp án mẫu:** - High Bias (Độ chệch cao): Mô hình quá đơn giản, không học được quy luật dữ liệu, dẫn đến hiện tượng Underfitting (lỗi cao trên cả tập Train và Test).
  - High Variance (Phương sai cao): Mô hình quá phức tạp, học cả nhiễu của dữ liệu, dẫn đến hiện tượng Overfitting (lỗi thấp trên tập Train nhưng lỗi cao trên tập Test).
  - Mục tiêu là tìm điểm cân bằng để giảm thiểu cả hai yếu tố giúp tổng lỗi (Total Error) của mô hình đạt mức thấp nhất.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Phương pháp giảm chiều dữ liệu PCA (Principal Component Analysis) hoạt động dựa trên nguyên lý cốt lõi nào?
* **Đáp án mẫu:** PCA biến đổi tập dữ liệu từ không gian nhiều chiều ban đầu sang một không gian ít chiều hơn bằng cách tìm ra các trục tọa độ mới (gọi là Principal Components) vuông góc với nhau, sao cho lượng phương sai (thông tin) của dữ liệu được lưu giữ lại trên các trục mới này là lớn nhất.

---

## CÂU HỎI KHÓ (3 câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong thuật toán phân cụm K-Means, làm thế nào để xác định số lượng cụm (K) tối ưu khi dữ liệu không có nhãn trước?
* **Đáp án mẫu:** Có hai kỹ thuật phổ biến:
  1. Phương pháp khuỷu tay (Elbow Method): Vẽ biểu đồ tổng bình phương khoảng cách trong cụm (WCSS) theo các giá trị K, chọn điểm mà tại đó tốc độ giảm của đồ thị bắt đầu chậm lại rõ rệt (tạo thành hình khuỷu tay).
  2. Chỉ số Silhouette (Silhouette Score): Đo lường mức độ tương đồng của một điểm với cụm của nó so với các cụm khác; giá trị score càng gần 1 chứng tỏ phân cụm càng tối ưu.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thuật toán Random Forest và Gradient Boosting (như XGBoost) đều dựa trên kỹ thuật Ensemble Learning. Hãy chỉ ra sự khác biệt cốt lõi về cơ chế xây dựng cây giữa hai thuật toán này.
* **Đáp án mẫu:** - Random Forest dùng kỹ thuật Bagging: Xây dựng nhiều cây quyết định độc lập, chạy song song với nhau từ các mẫu dữ liệu ngẫu nhiên khác nhau. Kết quả cuối cùng được lấy bằng cách bầu chọn (Voting) hoặc trung bình cộng.
  - Gradient Boosting dùng kỹ thuật Boosting: Xây dựng các cây quyết định một cách tuần tự. Mỗi cây mới sau được thiết kế để tập trung tối ưu hóa và sửa chữa những sai số (Residuals) do cây phía trước tạo ra.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Giả sử bạn xây dựng mô hình A/B Testing để đo lường mức độ hiệu quả của một tính năng UI mới. Lỗi loại I (Type I Error) và Lỗi loại II (Type II Error) trong ngữ cảnh này nghĩa là gì?
* **Đáp án mẫu:** - Lỗi loại I ($\alpha$): Xảy ra khi mô hình kết luận tính năng UI mới mang lại hiệu quả vượt trội, nhưng trên thực tế nó không hề có tác dụng gì (Dương tính giả - False Positive).
  - Lỗi loại II ($\beta$): Xảy ra khi mô hình kết luận tính năng UI mới không đem lại khác biệt gì, nhưng trên thực tế nó có mang lại hiệu quả thực sự (Âm tính giả - False Negative).