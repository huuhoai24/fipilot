# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 2) - Tập Đề Time Series và ML Pipeline (7)

* **Role:** AI Engineer
* **Level:** Level 2
* **Experience:** 1 - 3  năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Thế nào là bài toán Dự báo chuỗi thời gian (Time Series Forecasting)? Hãy nêu sự khác biệt lớn nhất giữa dữ liệu chuỗi thời gian và dữ liệu bảng (Tabular data) thông thường.
* **expected_key_points:**
  - id: KP1_1
    content: Khái niệm Time Series Forecasting
    keypoint_weight: 0.5
    description: Là bài toán dự đoán các giá trị tương lai dựa trên các giá trị lịch sử đã được thu thập theo trình tự thời gian liên tục.
  - id: KP1_2
    content: Sự khác biệt cốt lõi (Tính phụ thuộc thời gian)
    keypoint_weight: 0.5
    description: Dữ liệu bảng giả định các mẫu độc lập và phân phối cùng kiểu (i.i.d). Dữ liệu chuỗi thời gian có sự phụ thuộc lẫn nhau rất lớn giữa các mốc thời gian liên tiếp (tự tương quan - autocorrelation) và có tính xu hướng (trend), tính mùa vụ (seasonality).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích hiện tượng Vanishing Gradient. Tại sao kiến trúc LSTM lại giải quyết được một phần vấn đề này so với mạng RNN truyền thống?
* **expected_key_points:**
  - id: KP2_1
    content: Lỗi Vanishing Gradient trong RNN
    keypoint_weight: 0.5
    description: Khi chuỗi đầu vào quá dài, đạo hàm lan truyền ngược nhân liên tiếp các giá trị nhỏ hơn 1 dẫn đến gradient biến mất ở các bước thời gian đầu, khiến mạng quên đi ngữ cảnh xa.
  - id: KP2_2
    content: Cơ chế Cell State và Gates của LSTM
    keypoint_weight: 0.5
    description: LSTM bổ sung đường truyền Cell State đóng vai trò như băng chuyền thông tin xuyên suốt; điều khiển thông tin qua 3 cổng (Forget gate, Input gate, Output gate) giúp gradient có thể lan truyền ngược dễ dàng mà không bị triệt tiêu hoàn toàn.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Khi theo dõi quá trình huấn luyện, làm thế nào để nhận biết mô hình đang bị hiện tượng Underfitting (Chưa khớp)? Nêu 2 cách khắc phục.
* **expected_key_points:**
  - id: KP3_1
    content: Dấu hiệu nhận biết Underfitting
    keypoint_weight: 0.5
    description: Xảy ra khi cả Train Loss và Validation Loss đều ở mức rất cao, hoặc mô hình không đạt được độ chính xác mong muốn ngay cả trên tập dữ liệu huấn luyện.
  - id: KP3_2
    content: Hai cách khắc phục phổ biến
    keypoint_weight: 0.5
    description: Tăng độ phức tạp của mô hình (thêm lớp, thêm nơ-ron), giảm regularization (giảm dropout, giảm L1/L2), hoặc thực hiện feature engineering tạo thêm các đặc trưng hữu ích.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích các khái niệm: Tính dừng (Stationarity), Phép lấy hiệu (Differencing), và Phân rã chuỗi thời gian (Seasonal Decomposition) trong tiền xử lý dữ liệu chuỗi thời gian.
* **expected_key_points:**
  - id: KP4_1
    content: Ý nghĩa tính dừng và differencing
    keypoint_weight: 0.5
    description: Tính dừng yêu cầu các đặc trưng thống kê (mean, variance) của chuỗi không đổi theo thời gian (thuận lợi cho dự báo). Differencing là tính hiệu số giữa các mốc thời gian liên tiếp ($Y_t - Y_{t-1}$) nhằm loại bỏ trend và seasonality để đưa chuỗi về tính dừng.
  - id: KP4_2
    content: Phân rã chuỗi (Seasonal Decomposition)
    keypoint_weight: 0.5
    description: Tách một chuỗi thời gian thành 3 thành phần độc lập: Trend (Xu hướng dài hạn), Seasonal (Mẫu lặp lại định kỳ), và Residual/Noise (Nhiễu ngẫu nhiên).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cơ chế Attention-based Encoder-Decoder trong bài toán dịch máy. Nó cải tiến gì so với kiến trúc Encoder-Decoder thông thường?
* **expected_key_points:**
  - id: KP5_1
    content: Hạn chế của Encoder-Decoder thông thường
    keypoint_weight: 0.4
    description: Encoder phải nén toàn bộ thông tin của câu đầu vào thành một vector ngữ cảnh có kích thước cố định (bottleneck), gây mất mát thông tin đối với các câu dài.
  - id: KP5_2
    content: Cơ chế cải tiến của Attention
    keypoint_weight: 0.6
    description: Cho phép Decoder truy cập vào tất cả các trạng thái ẩn (hidden states) của Encoder. Tại mỗi bước dịch từ, Decoder tính toán trọng số chú ý (attention weights) để tập trung vào những từ liên quan nhất ở câu nguồn thay vì phụ thuộc vào một vector duy nhất.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt mô hình Transformer-XL và Transformer thông thường. Kỹ thuật nào giúp Transformer-XL xử lý ngữ cảnh cực dài tốt hơn?
* **expected_key_points:**
  - id: KP6_1
    content: Vấn đề Context Fragmentation ở Transformer
    keypoint_weight: 0.5
    description: Transformer thông thường chia văn bản thành các phân đoạn cố định độc lập (segments), bỏ qua mối quan hệ giữa các phân đoạn, gây mất thông tin ở biên phân đoạn (context fragmentation).
  - id: KP6_2
    content: Kỹ thuật của Transformer-XL
    keypoint_weight: 0.5
    description: Bổ sung cơ chế Recurrence ở cấp độ phân đoạn (Segment-level Recurrence): lưu trạng thái ẩn của phân đoạn trước và dùng nó làm ngữ cảnh cho phân đoạn sau. Đi kèm kỹ thuật Relative Position Encoding (mã hóa vị trí tương đối) thay cho Absolute Position Encoding.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày ưu nhược điểm của các chỉ số đánh giá bài toán hồi quy (Regression): Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), và Mean Absolute Percentage Error (MAPE).
* **expected_key_points:**
  - id: KP7_1
    content: So sánh MAE và RMSE
    keypoint_weight: 0.6
    description: MAE đo trung bình khoảng cách tuyệt đối, dễ hiểu, ít bị ảnh hưởng bởi outliers. RMSE lấy căn bậc hai của bình phương sai số, phạt rất nặng các sai số lớn, thích hợp khi cần tránh các lỗi lớn tuyệt đối.
  - id: KP7_2
    content: Đặc trưng của MAPE
    keypoint_weight: 0.4
    description: MAPE đo sai số theo tỷ lệ phần trăm, giúp dễ so sánh quy mô trên các tập dữ liệu khác nhau, nhưng gặp lỗi chia cho 0 hoặc giá trị tiến về vô cùng khi nhãn thực tế gần bằng 0.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống dự báo nhu cầu sản phẩm (Demand Forecasting) thời gian thực cho một chuỗi siêu thị bán lẻ lớn với hàng chục ngàn mặt hàng có tính mùa vụ và biến động cao.
* **expected_key_points:**
  - id: KP8_1
    content: Feature Engineering cho dữ liệu thời gian
    keypoint_weight: 0.5
    description: Tạo các đặc trưng trễ (lag features), trung bình động (rolling mean/std), đặc trưng lịch (thứ trong tuần, ngày lễ, sự kiện khuyến mãi, thời tiết), và thông tin tồn kho.
  - id: KP8_2
    content: Kiến trúc mô hình phân cấp (Hierarchical/Ensemble Model)
    keypoint_weight: 0.5
    description: Sử dụng mô hình ensemble (như LightGBM/XGBoost xử lý dữ liệu tabular tốt) kết hợp Deep Learning (DeepAR hoặc Temporal Fusion Transformer) để học các mẫu chuỗi thời gian phức tạp; xây dựng cơ chế huấn luyện phân cấp (theo cửa hàng, theo nhóm ngành hàng) để tối ưu hóa dự báo.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế một pipeline tự động hóa quy trình thu thập dữ liệu, huấn luyện lại (Continuous Training) và kiểm định chất lượng mô hình (Model Validation) sử dụng Kubeflow và MLflow.
* **expected_key_points:**
  - id: KP9_1
    content: Kiến trúc Pipeline Kubeflow
    keypoint_weight: 0.5
    description: Xây dựng các bước Kubeflow Pipelines (KFP) dạng DAG (Directed Acyclic Graph): Data Ingestion -> Preprocessing -> Hyperparameter Tuning -> Training -> Evaluation. Sử dụng triggers tự động chạy pipeline khi phát hiện data drift.
  - id: KP9_2
    content: Quản lý bằng MLflow và Kiểm định chất lượng
    keypoint_weight: 0.5
    description: Sử dụng MLflow Tracking ghi lại parameters, loss, metrics, và lưu trữ artifact (mô hình). Xây dựng bước kiểm định: so sánh mô hình mới (candidate) với mô hình đang chạy (champion) trên tập dữ liệu kiểm định chuẩn; nếu mô hình mới tốt hơn và vượt qua bài test bias/fairness thì mới đẩy lên Model Registry để CD.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống trích xuất thông tin y tế từ các bệnh án tiếng Việt (Clinical Named Entity Recognition) yêu cầu độ chính xác cực cao đối với các nhãn: Triệu chứng, Tên bệnh, Đơn thuốc.
* **expected_key_points:**
  - id: KP10_1
    content: Lựa chọn mô hình ngôn ngữ chuyên biệt
    keypoint_weight: 0.5
    description: Sử dụng mô hình tiếng Việt pre-trained chất lượng cao (như PhoBERT, ViBERT) hoặc LLM được fine-tune riêng trên ngữ liệu y khoa tiếng Việt để hiểu được các thuật ngữ y học phức tạp.
  - id: KP10_2
    content: Kiến trúc NER và Hậu xử lý
    keypoint_weight: 0.5
    description: Thiết kế đầu ra dạng BIO tagging kết hợp CRF (Conditional Random Fields) ở lớp cuối cùng để tối ưu hóa tính tuần tự của nhãn; xây dựng từ điển y khoa (knowledge graph y tế) để hậu xử lý chuẩn hóa tên bệnh và đơn thuốc.

