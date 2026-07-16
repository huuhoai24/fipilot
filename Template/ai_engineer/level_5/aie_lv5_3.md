# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 5) - Tập Đề Feature Store và Fraud Detection (3)

* **Role:** AI Engineer
* **Level:** Level 5
* **Experience:** Trên 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Feature Store trong Machine Learning là gì? Tại sao nó giải quyết được hiện tượng lệch pha dữ liệu giữa huấn luyện và phục vụ mô hình (Training-Serving Skew)?
* **expected_key_points:**
  - id: KP1_1
    content: Khái niệm Feature Store
    keypoint_weight: 0.5
    description: Là kho lưu trữ tập trung chuyên quản lý, chia sẻ và phục vụ các đặc trưng dữ liệu (features) cho cả quá trình huấn luyện mô hình (offline) và suy luận mô hình (online).
  - id: KP1_2
    content: Giải quyết Training-Serving Skew
    keypoint_weight: 0.5
    description: Feature Store đảm bảo định nghĩa mã nguồn tính toán đặc trưng và dữ liệu đầu vào là đồng nhất 100% giữa offline pipeline (sinh tập train) và online pipeline (suy luận thời gian thực).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt mục đích sử dụng và đặc tính kỹ thuật của hai kho lưu trữ: Offline Feature Store và Online Feature Store.
* **expected_key_points:**
  - id: KP2_1
    content: Offline Feature Store
    keypoint_weight: 0.5
    description: Lưu trữ lượng dữ liệu lịch sử khổng lồ (thường dùng Parquet trên S3/HDFS, BigQuery, Snowflake), tối ưu cho truy vấn phân tích lô (batch queries) để sinh tập dữ liệu huấn luyện.
  - id: KP2_2
    content: Online Feature Store
    keypoint_weight: 0.5
    description: Lưu trữ giá trị đặc trưng mới nhất (thường dùng Redis, DynamoDB, Cassandra), tối ưu cho truy vấn đơn lẻ có độ trễ cực thấp (low latency < 10ms) phục vụ suy luận thời gian thực.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích khái niệm kiến trúc Lambda (Lambda Architecture) trong xử lý dữ liệu AI và vai trò của các lớp: Batch Layer, Speed Layer, và Serving Layer.
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế hoạt động của các lớp
    keypoint_weight: 0.6
    description: Batch Layer xử lý lượng lớn dữ liệu lịch sử định kỳ (chính xác cao, trễ lớn). Speed Layer xử lý luồng dữ liệu thời gian thực mới nhất (trễ thấp, có thể có sai số). Serving Layer gộp kết quả từ 2 lớp để phục vụ truy vấn.
  - id: KP3_2
    content: Ứng dụng trong AI
    keypoint_weight: 0.4
    description: Giúp tính toán đặc trưng người dùng tức thời (ví dụ số lượt click trong 5 phút qua) để cập nhật vào Feature Store phục vụ hệ thống gợi ý.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế database schema và cấu trúc bộ nhớ cache cho một Online Feature Store sử dụng Redis để lưu trữ đặc trưng của 50 triệu người dùng, yêu cầu truy vấn độ trễ < 5ms.
* **expected_key_points:**
  - id: KP4_1
    content: Thiết kế cấu trúc dữ liệu Redis (Data Structures)
    keypoint_weight: 0.5
    description: Sử dụng kiểu dữ liệu Hash trong Redis với Key dạng `user:features:<user_id>`, lưu trữ các trường đặc trưng dưới dạng các cặp field-value nhằm tiết kiệm bộ nhớ và cho phép cập nhật từng trường đơn lẻ.
  - id: KP4_2
    content: Tối ưu hóa dung lượng bộ nhớ (Memory Optimization)
    keypoint_weight: 0.5
    description: Áp dụng kỹ thuật nén Protocol Buffers hoặc MessagePack trước khi ghi vào Redis; thiết lập cơ chế hết hạn tự động (TTL) cho các người dùng không hoạt động để tránh phình to bộ nhớ RAM.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế pipeline CDC (Change Data Capture) đồng bộ dữ liệu giao dịch từ cơ sở dữ liệu chính (PostgreSQL) thời gian thực vào Feature Store phục vụ mô hình phát hiện gian lận.
* **expected_key_points:**
  - id: KP5_1
    content: Kiến trúc luồng dữ liệu CDC
    keypoint_weight: 0.6
    description: Sử dụng Debezium lắng nghe Write-Ahead Log (WAL) của PostgreSQL -> đẩy các sự kiện thay đổi (Insert, Update) vào Kafka -> Flink/Spark Streaming tiêu thụ sự kiện từ Kafka để tính toán các đặc trưng giao dịch (rolling count, rolling sum).
  - id: KP5_2
    content: Ghi dữ liệu vào Feature Store
    keypoint_weight: 0.4
    description: Đẩy song song các đặc trưng đã tính toán vào Online Feature Store (Redis) để suy luận thời gian thực và Offline Feature Store (S3/BigQuery) làm dữ liệu huấn luyện tương lai.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Làm thế nào để phát hiện và khắc phục hiện tượng rò rỉ biến mục tiêu (Target Leakage) trong quá trình thiết kế đặc trưng (Feature Engineering) cho bài toán dự đoán rời bỏ (Churn Prediction)?
* **expected_key_points:**
  - id: KP6_1
    content: Bản chất hiện tượng Target Leakage
    keypoint_weight: 0.5
    description: Xảy ra khi các đặc trưng huấn luyện chứa thông tin xuất hiện sau khi sự kiện mục tiêu xảy ra (ví dụ: đưa biến 'số cuộc gọi khiếu nại hủy dịch vụ' vào mô hình dự đoán churn trước khi họ hủy).
  - id: KP6_2
    content: Cách phòng ngừa và khắc phục
    keypoint_weight: 0.5
    description: Thiết lập quy tắc Time-travel query trong Feature Store (chỉ lấy đặc trưng tại thời điểm đúng bằng $t_0$ trước khi sự kiện xảy ra); thiết lập quy trình kiểm tra độ tương quan (correlation analysis) giữa đặc trưng và nhãn.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế hệ thống kiểm soát quyền truy cập và bảo mật dữ liệu nhạy cảm (PII) trong Feature Store của một tổ chức tài chính lớn.
* **expected_key_points:**
  - id: KP7_1
    content: Mã hóa và Ẩn danh dữ liệu (Anonymization)
    keypoint_weight: 0.5
    description: Tự động mã hóa (encrypt) dữ liệu nhạy cảm ở trạng thái lưu trữ (at rest) và truyền tải (in transit); áp dụng cơ chế băm (hashing/tokenization) cho các định danh người dùng.
  - id: KP7_2
    content: Kiểm soát truy cập (Access Control & Auditing)
    keypoint_weight: 0.5
    description: Thiết lập phân quyền dựa trên vai trò (RBAC) cho các nhóm Data Scientist (chỉ đọc) và Data Pipeline (ghi); ghi log toàn bộ lịch sử truy cập (audit log) để đảm bảo tuân thủ tiêu chuẩn bảo mật.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống phát hiện gian lận giao dịch tài chính (Real-time Fraud Detection) độ trễ dưới 20ms sử dụng Feature Store và Graph Neural Networks (GNN) trên đồ thị giao dịch liên kết.
* **expected_key_points:**
  - id: KP8_1
    content: Xây dựng đồ thị giao dịch liên kết (Transaction Graph)
    keypoint_weight: 0.5
    description: Coi tài khoản ngân hàng, thiết bị đăng nhập, thẻ tín dụng là các nút (nodes); các giao dịch chuyển tiền làm các cạnh (edges) có thuộc tính thời gian và số tiền.
  - id: KP8_2
    content: Suy luận GNN thời gian thực (Real-time GNN Inference)
    keypoint_weight: 0.5
    description: Khi phát sinh giao dịch mới, truy vấn nhanh Online Feature Store lấy thuộc tính của tài khoản và thiết bị -> Sử dụng mô hình GNN (GraphSAGE) cục bộ để truyền tin nhắn (message passing) trong phạm vi 2 bước lân cận để chấm điểm gian lận dưới 20ms.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống gợi ý quảng cáo thời gian thực hiển thị sản phẩm dựa trên hành vi click-stream của người dùng quy mô 100,000 requests/giây.
* **expected_key_points:**
  - id: KP9_1
    content: Xử lý Click-stream phân tán chịu tải cao
    keypoint_weight: 0.5
    description: Sử dụng cụm Apache Kafka hấp thụ hàng triệu event click/giây; dùng Flink để tính toán tức thời các đặc trưng động của user (ví dụ danh mục click nhiều nhất trong 5 phút qua).
  - id: KP9_2
    content: Cập nhật Feature Store và Suy luận mô hình
    keypoint_weight: 0.5
    description: Flink ghi đặc trưng động vào Redis Online Feature Store; khi có request quảng cáo, tháp User lấy đặc trưng động này từ Redis kết hợp đặc trưng tĩnh và gọi Two-Tower Model để xếp hạng quảng cáo dưới 15ms.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế pipeline tự động hóa quy trình tính toán đặc trưng (Feature Pipeline) quy mô lớn sử dụng Apache Spark và Feast Feature Store.
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa Feature View trong Feast
    keypoint_weight: 0.5
    description: Định nghĩa Feast Feature Views bao gồm schema đặc trưng, thực thể liên kết, và nguồn dữ liệu (Spark/Parquet cho offline, Redis cho online).
  - id: KP10_2
    content: Huấn luyện song song qua Spark và Feast Materialization
    keypoint_weight: 0.5
    description: Sử dụng Spark chạy tính toán các đặc trưng phức tạp (chuyển đổi dữ liệu, tính thống kê) từ data lake -> chạy Feast Materialization đẩy dữ liệu đặc trưng đã tính sang Redis cho môi trường online.

