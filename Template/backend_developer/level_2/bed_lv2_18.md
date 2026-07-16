# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2) - Tập Đề Search và Logging Basics (18)

* **Role:** Backend Developer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích vai trò của Logging trong phát triển ứng dụng Backend. Phân biệt các cấp độ Log: DEBUG, INFO, WARN, và ERROR.
* **expected_key_points:**
  - id: KP1_1
    content: Vai trò của Logging
    keypoint_weight: 0.5
    description: Logging giúp lập trình viên ghi lại quá trình chạy của phần mềm để phục vụ việc debug khi có lỗi, phân tích hiệu năng và giám sát bảo mật hệ thống.
  - id: KP1_2
    content: Phân biệt các cấp độ Log
    keypoint_weight: 0.5
    description: DEBUG (ghi vết chi tiết khi phát triển). INFO (thông tin luồng chạy thông thường). WARN (cảnh báo bất thường không gây lỗi sập). ERROR (lỗi nghiêm trọng làm hỏng nghiệp vụ).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Tìm kiếm toàn văn (Full-Text Search) là gì? Tại sao các câu lệnh SQL thông thường như `LIKE` lại không đáp ứng tốt khi tìm kiếm văn bản lớn?
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm Full-Text Search
    keypoint_weight: 0.5
    description: Là kỹ thuật tìm kiếm tất cả các từ trong tài liệu, hỗ trợ tìm kiếm mờ (fuzzy), từ đồng nghĩa và tính toán độ liên quan của kết quả trả về.
  - id: KP2_2
    content: Giới hạn của lệnh LIKE trong SQL
    keypoint_weight: 0.5
    description: Lệnh `LIKE '%keyword%'` bắt buộc DB phải quét tuần tự toàn bộ bảng (Full Table Scan), cực kỳ chậm trên bảng lớn và hoàn toàn không có khả năng xếp hạng kết quả.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày cấu trúc của bộ công cụ ELK Stack (Elasticsearch, Logstash, Kibana) dùng để quản lý log tập trung.
* **expected_key_points:**
  - id: KP3_1
    content: Vai trò từng thành phần trong ELK
    keypoint_weight: 0.6
    description: Logstash thu thập và cấu trúc hóa dữ liệu log từ máy chủ. Elasticsearch lưu trữ, tìm kiếm log tốc độ cao. Kibana là giao diện web trực quan hóa và truy vấn log.
  - id: KP3_2
    content: Mô hình thu thập log cơ bản
    keypoint_weight: 0.4
    description: Log file từ các servers ứng dụng được shipper đẩy về Logstash xử lý, lưu vào Elasticsearch để quản trị viên truy cập xem trên Kibana dashboard.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích nguyên lý hoạt động của chỉ mục đảo ngược (Inverted Index) trong Elasticsearch. Tại sao nó giúp tìm kiếm văn bản cực nhanh?
* **expected_key_points:**
  - id: KP4_1
    content: Khái niệm Inverted Index
    keypoint_weight: 0.5
    description: Thay vì ánh xạ tài liệu tới các từ; Inverted Index tách văn bản thành các từ tố (tokens) độc lập, rồi lập bản đồ ánh xạ từ mỗi từ tố tới danh sách các tài liệu chứa từ đó.
  - id: KP4_2
    content: Tại sao tốc độ tìm kiếm cực nhanh
    keypoint_weight: 0.5
    description: Giúp tìm kiếm từ khóa chỉ trong $O(1)$ thời gian băm, trực tiếp trả ra danh sách ID tài liệu khớp mà không cần duyệt qua nội dung tài liệu.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là lỗi ghi log quá mức (Log Flooding)? Backend Developer làm thế nào để cấu hình Log Rotation bảo vệ ổ đĩa máy chủ?
* **expected_key_points:**
  - id: KP5_1
    content: Hiện tượng Log Flooding
    keypoint_weight: 0.5
    description: Xảy ra khi ứng dụng ghi log liên tục với số lượng khổng lồ (thường do đặt log level DEBUG ở production hoặc ghi log trong vòng lặp vô tận), gây đầy ổ đĩa cứng.
  - id: KP5_2
    content: Giải pháp cấu hình Log Rotation
    keypoint_weight: 0.5
    description: Cấu hình thư viện log (như Logback, Winston) tự động cắt file log khi đạt dung lượng (ví dụ 10MB) và chỉ giữ lại tối đa N file log cũ gần nhất.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách sử dụng Elasticsearch kết hợp cơ sở dữ liệu quan hệ (PostgreSQL/MySQL) trong dự án. Làm thế nào để đồng bộ dữ liệu giữa chúng?
* **expected_key_points:**
  - id: KP6_1
    content: Phân chia vai trò của 2 cơ sở dữ liệu
    keypoint_weight: 0.5
    description: CSDL quan hệ đóng vai trò lưu trữ chính (Single Source of Truth) đảm bảo ACID giao dịch. Elasticsearch chỉ làm bản sao lưu index phục vụ tìm kiếm toàn văn.
  - id: KP6_2
    content: Các giải pháp đồng bộ dữ liệu phổ biến
    keypoint_weight: 0.5
    description: Đồng bộ đồng thời ở code ứng dụng (ứng dụng tự ghi cả 2 nơi); đồng bộ bất đồng bộ qua hàng đợi Message Queue; hoặc sử dụng công cụ CDC (Logstash/Debezium).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích rủi ro bảo mật khi ghi log thông tin nhạy cảm của người dùng (như mật khẩu, số thẻ tín dụng). Thiết kế giải pháp lọc (Log Masking) ở Backend.
* **expected_key_points:**
  - id: KP7_1
    content: Nguy cơ lộ dữ liệu nhạy cảm qua logs
    keypoint_weight: 0.5
    description: Logs hệ thống thường được lưu dạng text rõ và chia sẻ cho nhiều kỹ sư xem; nếu ghi log mật khẩu, token sẽ tạo ra lỗ hổng bảo mật nghiêm trọng.
  - id: KP7_2
    content: Giải pháp Log Masking tự động
    keypoint_weight: 0.5
    description: Viết bộ lọc custom layout của thư viện logging; sử dụng biểu thức chính quy (Regex) tự động tìm các từ khóa nhạy cảm (`password`, `credit_card`) và thay thế bằng dấu `***`.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống tìm kiếm sản phẩm thương mại điện tử quy mô 1 triệu sản phẩm hỗ trợ tìm kiếm mờ (fuzzy search) và gợi ý tự động (auto-suggest) dưới 50ms sử dụng Elasticsearch.
* **expected_key_points:**
  - id: KP8_1
    content: Cấu hình Analyzers và Edge N-gram trong Mapping
    keypoint_weight: 0.5
    description: Sử dụng bộ phân tích Edge N-gram trên trường tên sản phẩm để chia nhỏ các chữ từ gốc gõ phím phục vụ gợi ý tức thời (Auto-suggest) khi người dùng đang gõ.
  - id: KP8_2
    content: Thiết kế câu query Fuzzy Search và Caching
    keypoint_weight: 0.5
    description: Sử dụng `match` query cấu hình độ lệch ký tự (fuzziness) để tìm kiếm khi gõ sai chính tả; kết hợp cache shard request trong Elasticsearch để tăng tốc độ phản hồi < 50ms.
  - id: KP8_3
    content: Gợi ý tự động và xếp hạng
    keypoint_weight: 0.0
    description: Sử dụng Completion Suggester cho hiệu năng tối ưu gợi ý nhanh.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế pipeline thu thập và phân tích logs tập trung chịu tải cực lớn từ 100 instance ứng dụng Backend, đảm bảo logs không bị mất mát khi hệ thống Elasticsearch bị chậm tải.
* **expected_key_points:**
  - id: KP9_1
    content: Đặt hàng đợi làm bộ đệm chống tràn (Buffer)
    keypoint_weight: 0.5
    description: Không đẩy trực tiếp logs từ máy chủ ứng dụng về Elasticsearch. Đẩy logs vào cụm Kafka hoặc RabbitMQ đóng vai trò làm hàng đệm lưu trữ logs an toàn.
  - id: KP9_2
    content: Worker tiêu thụ logs có kiểm soát (Backpressure)
    keypoint_weight: 0.5
    description: Viết Logstash/Worker đọc logs từ Kafka và ghi vào Elasticsearch; cấu hình worker tự động điều tiết tốc độ đọc dựa trên tải trọng phản hồi của Elasticsearch.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc đồng bộ dữ liệu thời gian thực giữa MySQL và Elasticsearch sử dụng kỹ thuật Change Data Capture (CDC) với Debezium và Kafka, đảm bảo dữ liệu cập nhật sang ES dưới 1 giây.
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế hoạt động của Debezium CDC
    keypoint_weight: 0.5
    description: Debezium đóng vai trò làm replica ảo lắng nghe file log nhị phân (binlog) của MySQL để bắt các sự kiện thay đổi dữ liệu (insert/update/delete) dạng nguyên tử.
  - id: KP10_2
    content: Truyền nhận qua Kafka và ghi đè ES index
    keypoint_weight: 0.5
    description: Đẩy các event binlog vào Kafka topic phân mảnh hợp lý; viết Consumer đọc và chuyển đổi cấu trúc bản ghi để ghi đè (upsert) sang Elasticsearch lập tức dưới 1 giây.

