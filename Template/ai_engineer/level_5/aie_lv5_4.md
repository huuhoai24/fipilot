# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 5) - Tập Đề Spatio-Temporal GNN và IoT Analytics (4)

* **Role:** AI Engineer
* **Level:** Level 5
* **Experience:** Trên 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong phân tích dữ liệu chuỗi thời gian (Time Series), hãy giải thích khái niệm tính dừng (Stationarity) và tầm quan trọng của nó trong việc dự báo.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa tính dừng (Stationarity)
    keypoint_weight: 0.5
    description: Là thuộc tính của chuỗi thời gian khi các đặc trưng thống kê như trung bình (mean), phương sai (variance) không thay đổi theo thời gian.
  - id: KP1_2
    content: Tầm quan trọng trong dự báo
    keypoint_weight: 0.5
    description: Các mô hình dự báo cổ điển giả định dữ liệu có tính dừng để đảm bảo các mối quan hệ học được trong quá khứ vẫn đúng trong tương lai; dùng differencing để đưa chuỗi về tính dừng.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh ưu nhược điểm của các chỉ số đánh giá dự báo chuỗi thời gian: MAE, RMSE, và sMAPE.
* **expected_key_points:**
  - id: KP2_1
    content: So sánh MAE và RMSE
    keypoint_weight: 0.5
    description: MAE dễ hiểu, đo khoảng cách trực tiếp. RMSE phạt nặng các sai số lớn do bình phương. Cả hai đều phụ thuộc vào quy mô dữ liệu.
  - id: KP2_2
    content: Ý nghĩa và nhược điểm sMAPE
    keypoint_weight: 0.5
    description: sMAPE tính phần trạng thái phần trăm sai số đối xứng, giúp dễ so sánh giữa các chuỗi có quy mô khác nhau, nhưng bị mất ổn định khi giá trị thực tế/dự báo gần bằng 0.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích cơ chế hoạt động của thuật toán tự hồi quy ARIMA. Các tham số $(p, d, q)$ thể hiện điều gì?
* **expected_key_points:**
  - id: KP3_1
    content: Bản chất thuật toán ARIMA
    keypoint_weight: 0.4
    description: Kết hợp giữa Auto-regressive (AR - tự hồi quy), Integrated (I - lấy hiệu phân kỳ), và Moving Average (MA - trung bình trượt sai số).
  - id: KP3_2
    content: Ý nghĩa tham số (p, d, q)
    keypoint_weight: 0.6
    description: $p$ là bậc của AR (số lượng giá trị trễ dùng dự báo). $d$ là số lần lấy hiệu (differencing) để chuỗi đạt tính dừng. $q$ là bậc của MA (số lượng sai số trễ dùng dự báo).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích nguyên lý hoạt động của mô hình dự báo Prophet phát triển bởi Facebook. Tại sao mô hình này lại hoạt động hiệu quả trên dữ liệu kinh doanh thực tế?
* **expected_key_points:**
  - id: KP4_1
    content: Cấu trúc mô hình cộng (Additive Model)
    keypoint_weight: 0.6
    description: Phân tách chuỗi thời gian thành: $y(t) = g(t) + s(t) + h(t) + \epsilon_t$ với $g(t)$ là xu hướng (trend), $s(t)$ là tính mùa vụ (seasonality), và $h(t)$ là ảnh hưởng của các ngày lễ (holidays).
  - id: KP4_2
    content: Ưu điểm với dữ liệu thực tế
    keypoint_weight: 0.4
    description: Tự động phát hiện điểm thay đổi xu hướng (changepoints), xử lý tốt dữ liệu bị khuyết, dữ liệu chứa nhiều nhiễu, và cho phép cấu hình trực tiếp các ngày lễ đặc thù.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cấu trúc và nguyên lý hoạt động của kiến trúc Temporal Fusion Transformer (TFT) trong bài toán dự báo chuỗi thời gian đa biến.
* **expected_key_points:**
  - id: KP5_1
    content: Ưu điểm của TFT so với Transformer thường
    keypoint_weight: 0.5
    description: TFT thiết kế riêng cho chuỗi thời gian, hỗ trợ đầu vào chứa cả biến đặc trưng tĩnh (static covariates) và biến biến đổi theo thời gian (time-varying covariates).
  - id: KP5_2
    content: Cơ chế Attention trong TFT
    keypoint_weight: 0.5
    description: Sử dụng cơ chế tự chú ý (self-attention) để hiểu mối tương quan thời gian dài và sử dụng lớp Gate Addnorm để tự động loại bỏ các đặc trưng không quan trọng (feature selection).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh sự khác nhau giữa LSTM và mạng nơ-ron tích chập thời gian TCN (Temporal Convolutional Network) trong việc xử lý dữ liệu chuỗi thời gian.
* **expected_key_points:**
  - id: KP6_1
    content: Cấu trúc tích chập nhân quả (Causal Convolutions) của TCN
    keypoint_weight: 0.6
    description: TCN sử dụng causal convolutions (đảm bảo không rò rỉ dữ liệu tương lai) kết hợp dilated convolutions để mở rộng trường thụ cảm (receptive field) theo cấp số mũ mà không làm mất thông tin tuần tự.
  - id: KP6_2
    content: So sánh hiệu năng và tính song song
    keypoint_weight: 0.4
    description: LSTM xử lý tuần tự nên chậm. TCN xử lý song song hoàn toàn trên toàn chuỗi giúp train nhanh hơn, tránh được lỗi vanishing gradient tốt hơn nhờ skip connections.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Làm thế nào để xử lý bài toán dự báo nhu cầu sản phẩm (Demand Forecasting) khi gặp hiện tượng chuỗi thời gian thưa (Intermittent Demand)?
* **expected_key_points:**
  - id: KP7_1
    content: Hạn chế của mô hình thường và Phương pháp Croston
    keypoint_weight: 0.6
    description: Các mô hình thường dự báo giá trị gần 0 cho mọi ngày. Phương pháp Croston phân tách chuỗi thành 2 phần độc lập: kích thước đơn hàng khi xảy ra giao dịch và khoảng thời gian giữa các giao dịch.
  - id: KP7_2
    content: Ứng dụng mô hình Deep Learning thưa
    keypoint_weight: 0.4
    description: Sử dụng các mô hình dự báo xác suất như DeepAR (dự đoán phân phối xác suất thay vì giá trị điểm) để ước lượng khoảng tin cậy của nhu cầu thưa.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống dự báo nhu cầu sản phẩm (Demand Forecasting) thời gian thực cho một chuỗi siêu thị bán lẻ quy mô lớn (50,000 mặt hàng, 100 cửa hàng) có tính mùa vụ và nhạy cảm với giá cả.
* **expected_key_points:**
  - id: KP8_1
    content: Feature Engineering cho dữ liệu thời gian
    keypoint_weight: 0.5
    description: Tạo các đặc trưng trễ (lags), trung bình động (rolling metrics), đặc trưng lịch (thứ tự ngày, ngày lễ, sự kiện khuyến mãi, thời tiết), và độ co giãn của cầu theo giá (price elasticity).
  - id: KP8_2
    content: Kiến trúc mô hình phân cấp và huấn luyện
    keypoint_weight: 0.5
    description: Sử dụng mô hình lai kết hợp LightGBM (cho dữ liệu bảng) và DeepAR (cho học chuỗi thời gian phân cấp); xây dựng pipeline huấn luyện song song qua Spark để cập nhật mô hình hàng tuần.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống dự báo phụ tải điện quốc gia (Energy Load Forecasting) theo từng giờ trong tuần tới, đảm bảo độ chính xác cao trước các biến động thời tiết cực đoan.
* **expected_key_points:**
  - id: KP9_1
    content: Thu thập và tích hợp dữ liệu đa nguồn (Feature Fusion)
    keypoint_weight: 0.5
    description: Tích hợp dữ liệu phụ tải lịch sử, thông số thời tiết thực tế và dự báo (nhiệt độ, độ ẩm, sức gió), thông tin lịch (thứ tự ngày, ngày nghỉ lễ, giờ làm việc), và các chỉ số kinh tế.
  - id: KP9_2
    content: Mô hình dự báo và cơ chế thích ứng
    keypoint_weight: 0.5
    description: Sử dụng mô hình lai kết hợp (Hybrid model): XGBoost/LightGBM cho các biến đặc trưng tĩnh và LSTM/GRU hoặc Temporal Fusion Transformer (TFT) để bắt ngữ cảnh chuỗi; thiết lập cơ chế tự động hiệu chỉnh dự báo khi có cảnh báo thời tiết cực đoan đột xuất.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế pipeline xử lý song song và dự báo thời gian thực cho hàng triệu luồng cảm biến chuỗi thời gian (IoT Sensors) gửi về liên tục sử dụng Apache Kafka, Apache Flink, và mô hình Deep Learning.
* **expected_key_points:**
  - id: KP10_1
    content: Kiến trúc Streaming Pipeline
    keypoint_weight: 0.5
    description: Sử dụng Kafka làm hàng đợi tin nhắn chịu tải cao hấp thụ dữ liệu cảm biến. Dùng Flink để xử lý luồng dữ liệu theo thời gian thực (sliding windows) để trích xuất các đặc trưng chuỗi thời gian (rolling mean, rolling std).
  - id: KP10_2
    content: Suy luận mô hình song song (Scalable Inference)
    keypoint_weight: 0.5
    description: Triển khai cụm các worker node chạy suy luận bằng mô hình Deep Learning nhẹ (như TCN - Temporal Convolutional Network) được tối ưu hóa qua TensorRT/ONNX Runtime; kết quả dự báo được ghi ngược lại Kafka để gửi cảnh báo lỗi tức thời.

