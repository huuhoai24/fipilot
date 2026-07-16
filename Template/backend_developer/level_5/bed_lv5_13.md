# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 5) - Tập Đề Kafka Consumer Groups và Event Sourcing (13)

* **Role:** Backend Developer
* **Level:** Level 5
* **Experience:** Trên 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh cơ chế Pull-based của Kafka và Push-based của RabbitMQ.
* **expected_key_points:**
  - id: KP1_1
    content: Mô hình Push vs Pull và Quản lý trạng thái
    keypoint_weight: 0.5
    description: RabbitMQ đẩy tin nhắn chủ động tới consumer và xóa tin nhắn ngay sau khi ack (RabbitMQ quản lý trạng thái). Kafka yêu cầu consumer tự pull tin nhắn dựa trên chỉ mục offset; tin nhắn lưu trữ cố định trên đĩa cứng theo log retention (consumer tự quản lý trạng thái).
  - id: KP1_2
    content: Khả năng chịu tải và Thứ tự tin nhắn
    keypoint_weight: 0.5
    description: Kafka hỗ trợ băng thông cực lớn (throughput triệu events/s) nhờ tuần tự hóa ghi đĩa và Zero-copy. RabbitMQ hỗ trợ định tuyến tin nhắn phức tạp (routing key, exchange) nhưng throughput thấp hơn.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Tính lũy đẳng (Idempotency) trong xử lý sự kiện bất đồng bộ.
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm Idempotency
    keypoint_weight: 0.5
    description: Đảm bảo việc thực thi một tin nhắn duy nhất nhiều lần vẫn mang lại kết quả giống hệt như thực thi một lần duy nhất, không gây mâu thuẫn trạng thái.
  - id: KP2_2
    content: Lý do bắt buộc trong hệ thống phân tán
    keypoint_weight: 0.5
    description: Do các lỗi mạng hoặc rớt node, các bản tin có thể bị gửi lặp lại (retry). Nếu không lũy đẳng, các tác vụ nhạy cảm như thanh toán, cộng tiền sẽ bị thực hiện sai lệch nhiều lần.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt At-least-once, At-most-once, và Exactly-once delivery.
* **expected_key_points:**
  - id: KP3_1
    content: Bản chất ba cơ chế
    keypoint_weight: 0.6
    description: At-most-once: tin nhắn gửi tối đa 1 lần (có thể mất mát). At-least-once: tin nhắn gửi ít nhất 1 lần, đảm bảo không mất nhưng có thể lặp. Exactly-once: tin nhắn đến đúng 1 lần duy nhất và xử lý chính xác.
  - id: KP3_2
    content: Độ khó thực hiện của Exactly-once
    keypoint_weight: 0.4
    description: Exactly-once khó thực hiện nhất vì đòi hỏi sự phối hợp giao dịch nguyên tử (transactional coordination) giữa producer, broker và consumer để rollback nếu xảy ra lỗi giữa chừng.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Cơ chế Consumer Group trong Kafka và cách scale out giữ tính thứ tự.
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế phân chia Partition cho Consumer
    keypoint_weight: 0.5
    description: Kafka phân bổ mỗi partition trong một topic cho duy nhất một consumer trong cùng một group tại một thời điểm để đảm bảo xử lý tuần tự.
  - id: KP4_2
    content: Mở rộng quy mô mà vẫn giữ thứ tự tin nhắn
    keypoint_weight: 0.5
    description: Tăng số lượng partitions của topic và tăng số lượng consumers tương ứng (số consumer tối đa bằng số partitions). Sử dụng hashing key hợp lý để gom các sự kiện liên quan vào cùng một partition.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế Retry Queue và Dead Letter Queue với Exponential Backoff.
* **expected_key_points:**
  - id: KP5_1
    content: Luồng đi của tin nhắn lỗi và Retry Queue
    keypoint_weight: 0.5
    description: Khi xử lý lỗi -> gửi tin nhắn sang Retry Queue gán kèm nhãn số lần thử lại và thời gian hết hạn (TTL). Consumer của Retry Queue đọc tin nhắn sau khoảng chờ lũy thừa (ví dụ: 2s, 4s, 8s).
  - id: KP5_2
    content: Chuyển sang DLQ
    keypoint_weight: 0.5
    description: Nếu số lần thử vượt quá ngưỡng (ví dụ: 5 lần) -> tự động chuyển sang DLQ (Dead Letter Queue) để cô lập lỗi; thiết lập hệ thống cảnh báo và dashboard để kỹ sư kiểm tra thủ công.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Hiện tượng Rebalance trong Kafka Consumer Group và cách tối ưu cấu hình.
* **expected_key_points:**
  - id: KP6_1
    content: Bản chất và nguyên nhân Rebalance
    keypoint_weight: 0.5
    description: Là quá trình điều phối lại việc gán partitions cho các consumers khi có sự thay đổi thành viên trong group (thêm consumer mới, consumer bị chết, hoặc mất kết nối heartbeats).
  - id: KP6_2
    content: Tối ưu cấu hình giảm thiểu Rebalance
    keypoint_weight: 0.5
    description: Tăng `session.timeout.ms` để tránh rớt mạng tạm thời bị coi là chết; tăng `max.poll.interval.ms` để dành thêm thời gian cho consumer xử lý các tác vụ nặng tránh bị hiểu nhầm là treo.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh Message Queue truyền thống và Event Stream từ góc độ Event Replay.
* **expected_key_points:**
  - id: KP7_1
    content: Lưu trữ dữ liệu lịch sử
    keypoint_weight: 0.5
    description: Message Queue xóa tin nhắn ngay sau khi xử lý thành công. Event Stream lưu giữ toàn bộ log sự kiện tuần tự trên đĩa cứng theo cấu hình thời gian dài hoặc vô hạn.
  - id: KP7_2
    content: Khả năng tái phát lại (Event Replay)
    keypoint_weight: 0.5
    description: Event Stream cho phép di chuyển con trỏ offset của consumer về quá khứ để phát lại toàn bộ lịch sử sự kiện phục vụ sửa lỗi, phân tích hoặc dựng lại trạng thái DB.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế cổng thanh toán điện tử dùng Event Sourcing và CQRS.
* **expected_key_points:**
  - id: KP8_1
    content: Thiết kế Event Store và Tính bất biến
    keypoint_weight: 0.5
    description: Mọi thay đổi số dư được lưu dưới dạng chuỗi các sự kiện bất biến (nhập tiền, trừ tiền) trong Event Store. Trạng thái số dư hiện tại được dựng lại bằng cách phát lại (replay) chuỗi sự kiện này.
  - id: KP8_2
    content: Kiến trúc CQRS và Read Model
    keypoint_weight: 0.5
    description: Tách biệt ghi (Command) ghi thẳng vào Event Store và đọc (Query) đọc từ Read Database (được đồng bộ bất đồng bộ qua Kafka). Thiết lập cơ chế chiếu (Projections) để cập nhật nhanh Read DB.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống xử lý đơn hàng 100k rps giữ thứ tự tuyệt đối trên Kafka.
* **expected_key_points:**
  - id: KP9_1
    content: Thiết kế Partition Key và Hashing
    keypoint_weight: 0.5
    description: Sử dụng `order_id` làm partition key để đảm bảo toàn bộ các sự kiện của cùng một đơn hàng (tạo, thanh toán, giao hàng) luôn được đẩy vào duy nhất một partition cố định.
  - id: KP9_2
    content: Cấu hình Producer và Consumer an toàn
    keypoint_weight: 0.5
    description: Cấu hình Producer: `acks=all`, `max.in.flight.requests.per.connection=1` (hoặc bật idempotence) để tránh lộn xộn thứ tự khi gửi lỗi. Consumer sử dụng luồng xử lý đơn lẻ cho mỗi partition.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc Multi-datacenter Kafka đồng bộ dữ liệu không mất tin nhắn.
* **expected_key_points:**
  - id: KP10_1
    content: Kiến trúc MirrorMaker 2 / Confluent Replicator
    keypoint_weight: 0.5
    description: Thiết lập các cụm Kafka độc lập tại mỗi datacenter; sử dụng MirrorMaker 2 để sao chép bất đồng bộ các topics giữa các vùng địa lý theo mô hình Active-Active hoặc Active-Passive.
  - id: KP10_2
    content: Đối phó thảm thảm họa mạng phân mảnh (Network Partition)
    keypoint_weight: 0.5
    description: Sử dụng cơ chế Local Writes để ứng dụng tại mỗi vùng vẫn ghi bình thường vào cụm Kafka local; khi mạng kết nối xuyên lục địa hoạt động trở lại, hệ thống replication tự động đồng bộ bù các tin nhắn bị lệch.

