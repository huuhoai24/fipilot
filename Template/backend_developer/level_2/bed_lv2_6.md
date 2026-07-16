# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2) - Tập Đề Message Broker Basics (6)

* **Role:** Backend Developer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Message Broker là gì? Tại sao hệ thống cần sử dụng Message Broker để xử lý các tác vụ bất đồng bộ?
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa Message Broker
    keypoint_weight: 0.5
    description: Là hệ thống trung gian nhận, lưu trữ và chuyển tiếp các thông điệp (messages) giữa các ứng dụng khác nhau mà không cần kết nối trực tiếp.
  - id: KP1_2
    content: Vai trò xử lý bất đồng bộ (Asynchronous processing)
    keypoint_weight: 0.5
    description: Giúp giải phóng luồng chính của client ngay lập tức (ví dụ: gửi mail đăng ký chạy nền), tăng trải nghiệm người dùng và giúp hệ thống chịu tải tốt hơn.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa hai mô hình truyền thông điệp cơ bản: Point-to-Point (Queue) và Publish-Subscribe (Topic).
* **expected_key_points:**
  - id: KP2_1
    content: Mô hình Point-to-Point (Queue)
    keypoint_weight: 0.5
    description: Một tin nhắn gửi vào queue chỉ được tiêu thụ bởi duy nhất một consumer (quan hệ 1-1). Thường dùng để phân chia công việc.
  - id: KP2_2
    content: Mô hình Publish-Subscribe (Topic)
    keypoint_weight: 0.5
    description: Một tin nhắn gửi vào topic có thể được sao chép và tiêu thụ bởi nhiều consumers đăng ký nhận tin khác nhau (quan hệ 1-n).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích khái niệm Message Acknowledgment (ACK/NACK). Điều gì xảy ra nếu consumer bị sập trước khi gửi ACK cho broker?
* **expected_key_points:**
  - id: KP3_1
    content: Bản chất ACK và NACK
    keypoint_weight: 0.5
    description: ACK báo cho broker biết tin nhắn đã xử lý xong và có thể xóa khỏi hàng đợi. NACK báo xử lý lỗi để broker đẩy lại tin nhắn vào queue.
  - id: KP3_2
    content: Hành vi khi consumer sập trước khi ACK
    keypoint_weight: 0.5
    description: Broker sẽ phát hiện kết nối của consumer bị đóng đột ngột -> chuyển tin nhắn đó sang trạng thái chờ -> tự động gửi lại tin nhắn đó cho một consumer khác xử lý.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh sự khác nhau về nguyên lý hoạt động giữa RabbitMQ (chạy trên RAM, định tuyến động) và Apache Kafka (chạy trên log đĩa cứng, tuần tự).
* **expected_key_points:**
  - id: KP4_1
    content: Nguyên lý hoạt động RabbitMQ
    keypoint_weight: 0.5
    description: RabbitMQ là broker truyền thống, đẩy tin nhắn chủ động tới consumer và xóa tin nhắn ngay sau khi nhận ACK. Hỗ trợ định tuyến phức tạp bằng exchange/routing key.
  - id: KP4_2
    content: Nguyên lý hoạt động Apache Kafka
    keypoint_weight: 0.5
    description: Kafka là log stream phân tán lưu trữ tin nhắn cố định trên đĩa cứng; consumer chủ động pull tin nhắn dựa trên chỉ mục offset; hỗ trợ throughput cực cao.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Làm thế nào để đảm bảo thứ tự xử lý tin nhắn (Message Ordering) trong hệ thống sử dụng Message Broker phân tán khi có nhiều consumers chạy song song?
* **expected_key_points:**
  - id: KP5_1
    content: Nguyên nhân mất thứ tự tin nhắn
    keypoint_weight: 0.4
    description: Khi có nhiều consumer đọc chung từ 1 queue, tốc độ xử lý khác nhau giữa các worker làm đảo lộn thứ tự hoàn thành của các tin nhắn.
  - id: KP5_2
    content: Giải pháp bảo toàn thứ tự
    keypoint_weight: 0.6
    description: Sử dụng định tuyến khóa (như partition key trong Kafka để gộp các tin nhắn liên quan vào cùng một phân mảnh duy nhất), đảm bảo tại một thời điểm chỉ có 1 consumer xử lý phân mảnh đó.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế giải pháp xử lý các tin nhắn bị lỗi liên tục (poison messages) sử dụng hàng đợi lỗi Dead Letter Queue (DLQ).
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế hoạt động của DLQ
    keypoint_weight: 0.5
    description: Khi một tin nhắn bị xử lý lỗi vượt quá số lần thử lại cấu hình trước (retry limit) -> server tự động chuyển tin nhắn đó sang một hàng đợi đặc biệt gọi là Dead Letter Queue.
  - id: KP6_2
    content: Xử lý tin nhắn trong DLQ
    keypoint_weight: 0.5
    description: Giúp cách ly lỗi để không làm nghẽn hàng đợi chính; lập trình viên có thể viết worker riêng phân tích log hoặc kiểm tra thủ công nội dung tin nhắn lỗi trong DLQ.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là lỗi xử lý lặp tin nhắn (Duplicate Messages) khi nhận tin từ Message Broker? Backend Developer giải quyết vấn đề này ra sao?
* **expected_key_points:**
  - id: KP7_1
    content: Nguyên nhân tin nhắn bị lặp
    keypoint_weight: 0.5
    description: Do sự cố mạng giữa consumer và broker khiến gói tin ACK bị thất lạc; broker tưởng consumer chưa xử lý nên gửi lại tin nhắn đó lần hai.
  - id: KP7_2
    content: Giải pháp đảm bảo tính lũy đẳng (Idempotent Consumer)
    keypoint_weight: 0.5
    description: Lưu ID của tin nhắn đã xử lý thành công vào DB/Redis; trước khi xử lý tin nhắn mới, kiểm tra xem ID đã tồn tại chưa; nếu có thì bỏ qua.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống thông báo đẩy (Push Notifications) cho ứng dụng có 1 triệu người dùng hoạt động đồng thời sử dụng kiến trúc Event-Driven kết hợp Kafka và WebSockets.
* **expected_key_points:**
  - id: KP8_1
    content: Kiến trúc luồng sự kiện (Event pipeline)
    keypoint_weight: 0.5
    description: Các microservices sinh sự kiện thông báo đẩy vào Kafka topic -> cụm WebSocket Servers lắng nghe Kafka -> xác định kết nối socket của user đích -> đẩy thông báo xuống thiết bị.
  - id: KP8_2
    content: Quản lý kết nối WebSockets phân tán
    keypoint_weight: 0.5
    description: Sử dụng Redis Pub/Sub để chia sẻ trạng thái kết nối của user giữa các node WebSocket Servers khác nhau sau load balancer, đảm bảo tin nhắn định tuyến đúng máy chủ đang kết nối với user.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp chống nghẽn cổ chai (Consumer Lag) trong cụm Apache Kafka khi tốc độ đẩy tin của Producer vượt quá khả năng tiêu thụ của các Consumer.
* **expected_key_points:**
  - id: KP9_1
    content: Giám sát Consumer Lag và Scale out
    keypoint_weight: 0.5
    description: Theo dõi chỉ số offset lag trên Prometheus; tăng số lượng Partitions cho Kafka Topic và khởi động thêm các instances Consumer trong cùng một Consumer Group để chia tải xử lý song song.
  - id: KP9_2
    content: Tối ưu xử lý I/O tại Consumer
    keypoint_weight: 0.5
    description: Áp dụng kỹ thuật Batch Consumer (đọc theo lô tin nhắn); xử lý tin nhắn đa luồng (multi-threaded workers) cục bộ tại consumer, chỉ thực hiện commit offset sau khi cả lô được xử lý.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế luồng Transactional Outbox Pattern nhằm đảm bảo tính nhất quán tuyệt đối giữa ghi dữ liệu vào CSDL chính và gửi sự kiện tương ứng vào Message Broker.
* **expected_key_points:**
  - id: KP10_1
    content: Vấn đề lỗi không đồng nhất dữ liệu
    keypoint_weight: 0.5
    description: Nếu ghi DB thành công nhưng gửi message sang broker thất bại (hoặc ngược lại) do lỗi mạng, dữ liệu giữa các microservices sẽ bị bất nhất quán.
  - id: KP10_2
    content: Thiết kế Outbox Table và CDC/Polling
    keypoint_weight: 0.5
    description: Trong cùng 1 transaction DB: ghi dữ liệu nghiệp vụ và chèn 1 bản ghi sự kiện vào bảng phụ `Outbox`. Sử dụng một luồng chạy độc lập đọc bảng Outbox (CDC như Debezium hoặc Polling) để gửi sang broker, đảm bảo gửi thành công ít nhất một lần (at-least-once).

