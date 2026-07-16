# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 2) - Tập Đề Time Series và sMAPE (13)

* **Role:** AI Engineer
* **Level:** Level 2
* **Experience:** 1 - 3  năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy nêu định nghĩa và cách nhận biết các thành phần chính của dữ liệu chuỗi thời gian (Time Series Data): Trend (Xu hướng), Seasonality (Mùa vụ), và Noise (Nhiễu).
* **expected_key_points:**
  - id: KP1_1
    content: Thành phần Trend và Seasonality
    keypoint_weight: 0.6
    description: Trend thể hiện hướng chuyển động dài hạn của dữ liệu (tăng hoặc giảm). Seasonality thể hiện sự dao động lặp đi lặp lại có tính chu kỳ cố định theo thời gian (ví dụ ngày, tuần, năm).
  - id: KP1_2
    content: Thành phần Noise
    keypoint_weight: 0.4
    description: Noise là các dao động ngẫu nhiên, không thể giải thích được bằng xu hướng hoặc tính mùa vụ, không có quy luật cố định.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Tính tự tương quan (Autocorrelation) là gì? Tại sao chỉ số ACF (Autocorrelation Function) và PACF (Partial Autocorrelation Function) lại quan trọng trong phân tích chuỗi thời gian?
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm tự tương quan
    keypoint_weight: 0.5
    description: Đo lường mức độ tương quan tuyến tính giữa các giá trị của chuỗi thời gian ở các thời điểm khác nhau (ví dụ $Y_t$ và $Y_{t-k}$).
  - id: KP2_2
    content: Vai trò của chỉ số ACF và PACF
    keypoint_weight: 0.5
    description: Dùng để xác định tính dừng của chuỗi, phát hiện tính chu kỳ, và là công cụ chính để xác định các siêu tham số $p$ (AR) và $q$ (MA) cho mô hình ARIMA.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy giải thích cơ chế lọc dữ liệu chuỗi thời gian sử dụng phương pháp trung bình động (Simple Moving Average - SMA) và trung bình động lũy thừa (Exponential Moving Average - EMA).
* **expected_key_points:**
  - id: KP3_1
    content: Đặc trưng Simple Moving Average (SMA)
    keypoint_weight: 0.5
    description: SMA tính trung bình cộng của các giá trị trong một cửa sổ thời gian cố định. Mọi mốc thời gian trong cửa sổ đều có trọng số bằng nhau.
  - id: KP3_2
    content: Đặc trưng Exponential Moving Average (EMA)
    keypoint_weight: 0.5
    description: EMA gán trọng số giảm dần theo hàm mũ cho các giá trị cũ hơn, giúp phản ứng nhanh hơn với các thay đổi đột ngột gần đây của dữ liệu.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày sự khác nhau giữa hai mô hình dự báo chuỗi thời gian cổ điển: ARIMA và SARIMA. Hãy giải thích ý nghĩa các tham số $(p, d, q)$ và $(P, D, Q)_s$.
* **expected_key_points:**
  - id: KP4_1
    content: Mô hình ARIMA và tham số (p, d, q)
    keypoint_weight: 0.5
    description: ARIMA dùng cho chuỗi không mùa vụ. $p$ là bậc của Auto-regressive (AR), $d$ là bậc của differencing để đưa chuỗi về tính dừng, $q$ là bậc của Moving Average (MA).
  - id: KP4_2
    content: Mô hình SARIMA và tham số mùa vụ
    keypoint_weight: 0.5
    description: SARIMA mở rộng từ ARIMA để xử lý tính mùa vụ. $(P, D, Q)_s$ là các tham số tương tự $(p, d, q)$ nhưng áp dụng ở mức độ mùa vụ với chu kỳ $s$ (ví dụ $s=12$ cho mùa vụ theo tháng).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích nguyên lý hoạt động của mô hình dự báo Prophet phát triển bởi Facebook. Tại sao nó lại phù hợp cho dữ liệu kinh doanh thực tế?
* **expected_key_points:**
  - id: KP5_1
    content: Nguyên lý mô hình cộng (Additive Model) của Prophet
    keypoint_weight: 0.6
    description: Prophet phân tách chuỗi thời gian thành công thức cộng: $y(t) = g(t) + s(t) + h(t) + \epsilon_t$ với $g(t)$ là trend phi tuyến, $s(t)$ là seasonality (năm/tuần/ngày), $h(t)$ là ảnh hưởng của các ngày lễ (holidays).
  - id: KP5_2
    content: Lý do phù hợp cho dữ liệu kinh doanh
    keypoint_weight: 0.4
    description: Xử lý cực tốt dữ liệu bị khuyết, dữ liệu có nhiều nhiễu/outliers, tự động phát hiện điểm thay đổi xu hướng (changepoints), và cho phép tích hợp trực tiếp danh sách ngày lễ tùy chỉnh.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh sự khác nhau giữa mạng RNN truyền thống, LSTM, và GRU (Gated Recurrent Unit) về cấu trúc phần cứng (số lượng cổng) và hiệu năng tính toán.
* **expected_key_points:**
  - id: KP6_1
    content: Cấu trúc cổng của LSTM vs GRU
    keypoint_weight: 0.6
    description: LSTM có 3 cổng (Forget, Input, Output) và 2 trạng thái (Cell state, Hidden state). GRU tinh giản hơn chỉ có 2 cổng (Reset, Update) và gộp chung Cell state vào Hidden state.
  - id: KP6_2
    content: Hiệu năng tính toán
    keypoint_weight: 0.4
    description: GRU có ít tham số hơn LSTM khoảng 25%, giúp huấn luyện nhanh hơn và tốn ít bộ nhớ hơn, trong khi vẫn đạt độ chính xác tương đương trên hầu hết các bài toán.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách tính và so sánh ưu nhược điểm của các chỉ số đánh giá dự báo chuỗi thời gian: MAE, RMSE, và sMAPE (Symmetric Mean Absolute Percentage Error).
* **expected_key_points:**
  - id: KP7_1
    content: Sự khác biệt của MAE và RMSE
    keypoint_weight: 0.5
    description: MAE đo sai số trung bình tuyệt đối trực quan. RMSE bình phương sai số trước khi lấy căn, rất nhạy cảm với các lỗi lớn. Cả hai đều phụ thuộc vào quy mô dữ liệu.
  - id: KP7_2
    content: Ưu nhược điểm của sMAPE
    keypoint_weight: 0.5
    description: sMAPE tính phần trăm sai số đối xứng: $sMAPE = \frac{100\%}{N} \sum \frac{|y_t - \hat{y}_t|}{(|y_t| + |\hat{y}_t|)/2}$. Không phụ thuộc quy mô, nhưng có thể bị mất ổn định khi cả giá trị thực tế và dự báo đều tiến về 0.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

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

