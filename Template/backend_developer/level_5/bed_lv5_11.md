# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 5) - Tập Đề Distributed Consensus và Leader Leases (11)

* **Role:** Backend Developer
* **Level:** Level 5
* **Experience:** Trên 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh sự khác nhau về cơ chế ghi log, bầu chọn Leader và tối ưu hóa số vòng mạng (network round-trips) khi đạt đồng thuận giữa giao thức Raft và Multi-Paxos.
* **expected_key_points:**
  - id: KP1_1
    content: Ghi log và Bầu chọn Leader
    keypoint_weight: 0.5
    description: Raft yêu cầu log phải liên tục và chỉ cho phép node có log cập nhật nhất làm Leader. Multi-Paxos cho phép log có khoảng trống (holes) và bất kỳ node nào cũng có thể làm Leader, sau đó lấp đầy khoảng trống sau.
  - id: KP1_2
    content: Tối ưu hóa vòng mạng (Network Round-trips)
    keypoint_weight: 0.5
    description: Raft mất ít nhất 1-RTT để replicate log và commit. Multi-Paxos sau khi thiết lập Leader ở phase 1 có thể bỏ qua phase 1 ở các đề xuất tiếp theo, đạt đồng thuận chỉ trong 1-RTT duy nhất (Phase 2).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích cơ chế hoạt động của Saga Pattern (so sánh Saga Orchestration và Saga Choreography) trong giao dịch phân tán.
* **expected_key_points:**
  - id: KP2_1
    content: Saga Orchestration vs Saga Choreography
    keypoint_weight: 0.5
    description: Orchestration sử dụng một dịch vụ trung tâm (Orchestrator) để điều phối tuần tự các bước giao dịch cục bộ và gọi lệnh hoàn trả (compensating transaction) nếu có bước lỗi. Choreography dựa trên các sự kiện (event-driven) để các dịch vụ tự lắng nghe và phản ứng gián tiếp.
  - id: KP2_2
    content: Thiết kế cơ chế Hoàn trả (Compensating Transactions)
    keypoint_weight: 0.5
    description: Mỗi bước giao dịch thành công phải có một giao dịch bù trừ tương ứng (ví dụ: cộng lại kho hàng nếu thanh toán lỗi) để đảm bảo đưa hệ thống về trạng thái nhất quán nhất thời khi có lỗi phát sinh.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt Eventual Consistency và Strong Consistency trong mô hình CAP. Việc lựa chọn này ảnh hưởng thế nào đến độ trễ hệ thống theo định lý CAP?
* **expected_key_points:**
  - id: KP3_1
    content: Bản chất Strong vs Eventual Consistency
    keypoint_weight: 0.5
    description: Strong Consistency đảm bảo mọi request đọc tại mọi node đều trả về giá trị mới nhất của lệnh ghi trước đó. Eventual Consistency chấp nhận dữ liệu có độ trễ đồng bộ nhất thời, đảm bảo các node sẽ đạt trạng thái đồng nhất sau một khoảng thời gian không có lệnh ghi mới.
  - id: KP3_2
    content: Ảnh hưởng độ trễ và Định lý CAP
    keypoint_weight: 0.5
    description: Chọn Strong Consistency yêu cầu đồng bộ hóa khóa chặn qua các nodes, tăng vọt độ trễ truy vấn (CP). Chọn Eventual Consistency tối ưu hóa tốc độ ghi đọc do không cần khóa đồng bộ trực tiếp (AP).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế cơ chế chống phân mảnh cụm (Split-brain) trong hệ thống phân tán sử dụng giao thức bầu chọn Leader dựa trên số đông (Quorum).
* **expected_key_points:**
  - id: KP4_1
    content: Khái niệm Split-brain và nguyên nhân
    keypoint_weight: 0.4
    description: Xảy ra khi kết nối mạng giữa các nodes bị đứt làm cụm bị chia tách thành 2 hoặc nhiều phân vùng độc lập. Mỗi phân vùng tự bầu một Leader riêng, dẫn đến ghi đè dữ liệu mâu thuẫn.
  - id: KP4_2
    content: Giải pháp dựa trên Quorum (Số đông)
    keypoint_weight: 0.6
    description: Yêu cầu mọi quyết định ghi hoặc bầu chọn Leader phải được chấp thuận bởi số đông tối thiểu $\lfloor N/2 \rfloor + 1$ nodes. Phân vùng thiểu số không đạt đủ số lượng node sẽ tự động chuyển sang chế độ Read-only hoặc tự hủy tư cách Leader, đảm bảo không xảy ra mâu thuẫn dữ liệu.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Xây dựng giải pháp đảm bảo tính lũy đẳng (Idempotency) khi xử lý các sự kiện thanh toán trùng lặp nhận từ Message Broker.
* **expected_key_points:**
  - id: KP5_1
    content: Sử dụng Idempotency Key và Database Constraint
    keypoint_weight: 0.5
    description: Mỗi giao dịch đính kèm một khóa duy nhất `idempotency_key`. Sử dụng ràng buộc duy nhất (Unique Constraint) trong DB trên khóa này để ngăn chặn chèn bản ghi trùng lặp.
  - id: KP5_2
    content: Cơ chế State Machine và Khóa phân tán
    keypoint_weight: 0.5
    description: Kiểm tra trạng thái giao dịch trước khi xử lý (ví dụ: chỉ xử lý nếu status = PENDING); sử dụng Redis Distributed Lock trên khóa idempotency để chặn các luồng gọi song song đồng thời.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh Two-Phase Commit (2PC) và Three-Phase Commit (3PC) về khả năng khắc phục lỗi blocking khi Coordinator bị sập giữa chừng.
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên nhân Blocking của 2PC
    keypoint_weight: 0.5
    description: Trong 2PC, các participant không biết trạng thái của coordinator nếu bị mất kết nối ở giai đoạn Commit, dẫn đến việc phải giữ khóa tài nguyên chờ đợi.
  - id: KP6_2
    content: Cải tiến của 3PC (Pre-Commit phase)
    keypoint_weight: 0.5
    description: 3PC chia giai đoạn 2 thành: Can-Commit, Pre-Commit, và Do-Commit. Bổ sung cơ chế timeout tự động cho cả coordinator và participant; nếu participant bị ngắt kết nối ở trạng thái Pre-Commit, nó vẫn có thể tự động commit an toàn vì biết tất cả các node khác đã đồng ý ở bước Can-Commit.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích vai trò của cơ chế Raft Leader Leases trong việc tối ưu hóa hiệu năng đọc của hệ thống mà vẫn đảm bảo tính nhất quán mạnh (Strong Consistency).
* **expected_key_points:**
  - id: KP7_1
    content: Vấn đề của phép đọc trên Raft thông thường
    keypoint_weight: 0.5
    description: Thông thường, để đảm bảo tính nhất quán mạnh khi đọc, Leader vẫn phải chạy All-Reduce/Heartbeats qua các followers để xác nhận mình vẫn là Leader (tốn round-trips).
  - id: KP7_2
    content: Cơ chế hoạt động của Leader Leases
    keypoint_weight: 0.5
    description: Followers cam kết không bầu chọn Leader mới trong một khoảng thời gian cố định (Lease Time). Trong khoảng thời gian này, Leader hiện tại tự tin trả lời trực tiếp các request đọc từ Local RAM mà không cần liên hệ followers, tăng throughput đọc gấp nhiều lần.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống bán vé ca nhạc tải cực cao (100k rps) không bán vượt số lượng thực tế sử dụng Distributed Lock.
* **expected_key_points:**
  - id: KP8_1
    content: Quản lý hàng đợi và Giảm tải Database
    keypoint_weight: 0.5
    description: Tránh ghi trực tiếp vào DB quan hệ. Sử dụng Redis Distributed Lock (hoặc hàng đợi Redis Streams/Kafka) để xếp hàng requests; kiểm tra và trừ lượng vé tồn kho (inventory count) trực tiếp trên Redis sử dụng các lệnh nguyên tử (Lua script).
  - id: KP8_2
    content: Giao dịch ghi DB và Đồng bộ dữ liệu
    keypoint_weight: 0.5
    description: Sử dụng PostgreSQL với mức cô lập giao dịch Repeatable Read hoặc Serializable để đảm bảo trừ kho hàng chính xác khi đồng bộ offline từ Redis; thiết lập cơ chế rollback vé nếu thanh toán thất bại trong 5 phút.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế cơ sở dữ liệu đa vùng Active-Active giải quyết xung đột bằng Vector Clocks hoặc CRDTs.
* **expected_key_points:**
  - id: KP9_1
    content: Phát hiện xung đột bằng Vector Clocks
    keypoint_weight: 0.5
    description: Mỗi node gán kèm một nhãn thời gian logic dạng vector thể hiện số phiên bản sửa đổi tại các node lân cận để xác định thứ tự nhân quả và phát hiện khi có hai sửa đổi đồng thời xảy ra tại hai vùng khác nhau.
  - id: KP9_2
    content: Giải quyết xung đột bằng CRDTs (Conflict-free Replicated Data Types)
    keypoint_weight: 0.5
    description: Sử dụng cấu trúc dữ liệu CRDTs (như LWW-Element-Set hoặc PN-Counter) tự động gộp dữ liệu đồng bộ mà không cần phân xử tập trung, đảm bảo dữ liệu cuối cùng ở tất cả các vùng sẽ hội tụ về cùng một giá trị chính xác.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Xây dựng giải pháp đồng bộ dữ liệu PostgreSQL và Elasticsearch dùng Outbox Pattern và Debezium CDC.
* **expected_key_points:**
  - id: KP10_1
    content: Thiết kế Outbox Pattern
    keypoint_weight: 0.5
    description: Khi cập nhật DB, ghi thông tin sự kiện thay đổi vào một bảng phụ tên `outbox_table` trong cùng một transaction cục bộ (đảm bảo tính nguyên tử tuyệt đối).
  - id: KP10_2
    content: Đọc dữ liệu CDC và Đồng bộ Elasticsearch
    keypoint_weight: 0.5
    description: Sử dụng công cụ CDC (như Debezium) đọc logs của bảng outbox -> đẩy vào Kafka topic -> Subscriber tiêu thụ tin nhắn từ Kafka và cập nhật bất đồng bộ vào Elasticsearch, giải phóng tài nguyên tính toán của PostgreSQL.

