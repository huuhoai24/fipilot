# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 5) - Tập Đề Spatio-Temporal GNN và Traffic Forecasting (14)

* **Role:** AI Engineer
* **Level:** Level 5
* **Experience:** Trên 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt các thành phần Trend, Seasonality, và Residuals trong quá trình phân rã chuỗi thời gian (Seasonal Decomposition).
* **expected_key_points:**
  - id: KP1_1
    content: Thành phần Trend và Seasonality
    keypoint_weight: 0.6
    description: Trend thể hiện hướng chuyển động dài hạn tăng/giảm của chuỗi. Seasonality thể hiện các dao động chu kỳ lặp lại cố định theo thời gian (ngày, tuần, năm).
  - id: KP1_2
    content: Thành phần Residuals (Nhiễu)
    keypoint_weight: 0.4
    description: Residuals là phần còn lại sau khi đã loại bỏ Trend và Seasonality khỏi chuỗi gốc, đại diện cho các dao động ngẫu nhiên, nhiễu không có quy luật.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Ý nghĩa của tính dừng (Stationarity) và phép lấy hiệu (Differencing) trong mô hình dự báo chuỗi thời gian cổ điển ARIMA.
* **expected_key_points:**
  - id: KP2_1
    content: Tính dừng (Stationarity)
    keypoint_weight: 0.5
    description: Yêu cầu các đặc trưng thống kê như mean, variance không đổi theo thời gian, giúp mô hình học được các quy luật ổn định.
  - id: KP2_2
    content: Phép lấy hiệu (Differencing)
    keypoint_weight: 0.5
    description: Tính hiệu số giữa các mốc thời gian liên tiếp ($Y_t - Y_{t-1}$) để loại bỏ xu hướng (trend) và mùa vụ, đưa chuỗi về tính dừng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy giải thích cơ chế lọc dữ liệu chuỗi thời gian sử dụng phương pháp trung bình động (Simple Moving Average - SMA) và trung bình động lũy thừa (Exponential Moving Average - EMA).
* **expected_key_points:**
  - id: KP3_1
    content: Simple Moving Average (SMA)
    keypoint_weight: 0.5
    description: Tính trung bình cộng trong một cửa sổ thời gian cố định. Mọi mốc thời gian đều có trọng số như nhau.
  - id: KP3_2
    content: Exponential Moving Average (EMA)
    keypoint_weight: 0.5
    description: Gán trọng số giảm dần theo hàm mũ cho dữ liệu cũ, giúp phản ứng nhanh hơn với các thay đổi đột ngột của dữ liệu gần đây.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cấu trúc và nguyên lý hoạt động của mạng nơ-ron tích chập thời gian TCN (Temporal Convolutional Network) so với mạng LSTM truyền thống.
* **expected_key_points:**
  - id: KP4_1
    content: Tích chập nhân quả và Dilated Convolutions trong TCN
    keypoint_weight: 0.6
    description: TCN sử dụng causal convolutions (không rò rỉ dữ liệu tương lai) và dilated convolutions (phép tích chập thưa rộng) để mở rộng trường thụ cảm theo cấp số mũ mà không tốn tham số.
  - id: KP4_2
    content: Song song hóa và hội tụ
    keypoint_weight: 0.4
    description: TCN xử lý song song toàn chuỗi trên GPU (nhanh hơn LSTM tuần tự) và tránh được lỗi vanishing gradient tốt hơn nhờ cấu trúc skip connections.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh ưu nhược điểm của các mô hình dự báo chuỗi thời gian: ARIMA, Prophet, và DeepAR khi xử lý dữ liệu thực tế có mùa vụ phức tạp.
* **expected_key_points:**
  - id: KP5_1
    content: Đặc trưng từng mô hình
    keypoint_weight: 0.6
    description: ARIMA tốt cho chuỗi dừng ngắn hạn. Prophet tốt cho dữ liệu kinh doanh có nhiều ngày lễ và xu hướng phi tuyến tính. DeepAR (Deep Learning) tốt cho dự báo xác suất trên hàng ngàn chuỗi thời gian liên quan chéo.
  - id: KP5_2
    content: Lựa chọn thực tế
    keypoint_weight: 0.4
    description: Sử dụng DeepAR khi cần khoảng tin cậy (probabilistic forecasting) và các chuỗi có sự phụ thuộc chéo; dùng Prophet khi dữ liệu khuyết nhiều.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách tính và so sánh vai trò của các chỉ số đánh giá dự báo: MAE, RMSE, và sMAPE.
* **expected_key_points:**
  - id: KP6_1
    content: So sánh MAE và RMSE
    keypoint_weight: 0.5
    description: MAE đo sai số tuyệt đối trung bình. RMSE bình phương sai số trước khi lấy căn, phạt nặng các lỗi lớn. Cả hai đều phụ thuộc vào quy mô dữ liệu.
  - id: KP6_2
    content: sMAPE đặc trưng
    keypoint_weight: 0.5
    description: sMAPE tính sai số theo tỷ lệ phần trăm đối xứng, thích hợp so sánh giữa các chuỗi khác quy mô nhưng kém ổn định khi nhãn thực tế gần bằng 0.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Làm thế nào để xử lý bài toán dự báo nhu cầu sản phẩm (Demand Forecasting) khi gặp hiện tượng chuỗi thời gian thưa (Intermittent Demand)?
* **expected_key_points:**
  - id: KP7_1
    content: Hạn chế của mô hình thường và Phương pháp Croston
    keypoint_weight: 0.6
    description: Các mô hình thường dự báo giá trị gần 0 cho mọi ngày. Phương pháp Croston phân tách chuỗi thành 2 phần độc lập: kích thước đơn hàng khi xảy ra giao dịch và khoảng thời gian giữa các giao dịch.
  - id: KP7_2
    content: Mô hình học sâu dự báo xác suất
    keypoint_weight: 0.4
    description: Sử dụng DeepAR dự đoán phân phối xác suất (ví dụ Negative Binomial distribution) để đưa ra khoảng tin cậy của nhu cầu thưa, giúp tối ưu hóa tồn kho.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống dự đoán lưu lượng giao thông thời gian thực tại các nút giao thông trong thành phố sử dụng mạng nơ-ron đồ thị không-thời gian (Spatio-Temporal Graph Neural Networks - STGNN).
* **expected_key_points:**
  - id: KP8_1
    content: Biểu diễn không gian bằng Graph Convolutional Networks (GCN)
    keypoint_weight: 0.5
    description: Coi các nút giao thông là các đỉnh (vertices), các con đường kết nối là các cạnh (edges) trên đồ thị. Sử dụng GCN để học mối tương quan không gian (sự ùn tắc ở nút này sẽ lan sang nút lân cận).
  - id: KP8_2
    content: Biểu diễn thời gian và tích hợp
    keypoint_weight: 0.5
    description: Sử dụng GRU/LSTM hoặc cơ chế Temporal Self-Attention tại mỗi nút để học mối tương quan thời gian (giờ cao điểm hàng ngày). Kết hợp thông tin không-thời gian để dự báo lưu lượng trong 15, 30, 60 phút tiếp theo.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp dự báo phụ tải điện quốc gia (Energy Load Forecasting) theo từng giờ trong tuần tới, đảm bảo độ chính xác cao trước các biến động thời tiết cực đoan.
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

