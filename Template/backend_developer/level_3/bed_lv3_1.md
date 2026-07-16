# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 3) - Tập Đề Distributed Consensus và Transactions (1)

* **Role:** Backend Developer
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Phân tích và so sánh sự khác nhau về bản chất toán học, cơ chế bầu chọn Leader và kịch bản áp dụng giữa hai giao thức đồng thuận phân tán phổ biến: Raft và Paxos.
* **expected_key_points:**
  - id: KP1_1
    content: Bản chất toán học và độ phức tạp thiết kế
    keypoint_weight: 0.5
    description: Paxos là mô hình đồng thuận lý thuyết cơ bản dựa trên các vai trò Proposer, Acceptor, Learner; thiết kế rất phức tạp để hiện thực hóa trong thực tế. Raft được thiết kế thân thiện, chia bài toán thành 3 bài toán con độc lập: Leader Election, Log Replication, và Safety.
  - id: KP1_2
    content: Cơ chế bầu chọn Leader và áp dụng
    keypoint_weight: 0.5
    description: Raft bắt buộc phải có duy nhất một Leader hoạt động tại mọi thời điểm để điều phối ghi. Paxos (đặc biệt Multi-Paxos) có thể tối ưu hóa không cần Leader cứng hoặc cho phép nhiều Leader đề xuất song song; áp dụng Raft cho ETCD/Consul, Paxos cho Spanner/Chubby.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích cơ chế hoạt động của thuật toán đồng thuận Two-Phase Commit (2PC) trong việc đảm bảo tính nguyên tử (Atomicity) của giao dịch phân tán qua nhiều cơ sở dữ liệu độc lập.
* **expected_key_points:**
  - id: KP2_1
    content: Hai giai đoạn của 2PC: Prepare và Commit
    keypoint_weight: 0.6
    description: Giai đoạn 1 (Prepare): Coordinator gửi yêu cầu chuẩn bị tới tất cả các Participants. Các Participants thực hiện giao dịch cục bộ ghi vào WAL và phản hồi YES hoặc NO. Giai đoạn 2 (Commit): Nếu tất cả phản hồi YES, Coordinator gửi lệnh COMMIT; ngược lại gửi lệnh ROLLBACK để hủy bỏ toàn bộ.
  - id: KP2_2
    content: Hạn chế nghẽn cổ chai và Blocking
    keypoint_weight: 0.4
    description: 2PC có hạn chế là giao thức dạng chặn (blocking proto). Nếu Coordinator bị sập ở giai đoạn 2, các Participants phải giữ khóa tài nguyên vô thời hạn để chờ lệnh tiếp theo, làm sập toàn bộ hệ thống.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa tính nhất quán nhất thời (Eventual Consistency) và tính nhất quán mạnh (Strong Consistency) trong hệ thống phân tán. Việc lựa chọn này ảnh hưởng thế nào đến độ trễ hệ thống theo định lý CAP?
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
* **Câu hỏi:** Thiết kế cơ chế xử lý trường hợp Split-brain (phân mảnh cụm) trong hệ thống phân tán sử dụng giao thức bầu chọn Leader dựa trên số đông (Quorum).
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
* **Câu hỏi:** Thiết kế giải pháp giao dịch phân tán sử dụng Saga Pattern (so sánh Saga Orchestration và Saga Choreography) cho hệ thống e-commerce xử lý đơn hàng phức tạp qua các dịch vụ: Order, Payment, và Inventory.
* **expected_key_points:**
  - id: KP5_1
    content: Saga Orchestration vs Saga Choreography
    keypoint_weight: 0.5
    description: Orchestration sử dụng một dịch vụ trung tâm (Orchestrator) để điều phối tuần tự các bước giao dịch cục bộ và gọi lệnh hoàn trả (compensating transaction) nếu có bước lỗi. Choreography dựa trên các sự kiện (event-driven) để các dịch vụ tự lắng nghe và phản ứng gián tiếp.
  - id: KP5_2
    content: Thiết kế cơ chế Hoàn trả (Compensating Transactions)
    keypoint_weight: 0.5
    description: Mỗi bước giao dịch thành công phải có một giao dịch bù trừ tương ứng (ví dụ: cộng lại kho hàng nếu thanh toán lỗi) để đảm bảo đưa hệ thống về trạng thái nhất quán nhất thời khi có lỗi phát sinh.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích nguyên nhân và thiết kế giải pháp khắc phục hiện tượng Blocking trong giao thức Two-Phase Commit (2PC) bằng cách chuyển sang giao thức Three-Phase Commit (3PC).
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
* **Câu hỏi:** Giải thích mô hình đồng thuận Paxos: Vai trò của Proposer, Acceptor, Learner và cách nó giải quyết xung đột khi có nhiều Proposers cùng gửi đề xuất đồng thời.
* **expected_key_points:**
  - id: KP7_1
    content: Vai trò của Proposer, Acceptor, Learner
    keypoint_weight: 0.5
    description: Proposer nhận yêu cầu từ client và đề xuất giá trị. Acceptor bỏ phiếu đồng ý/không đồng ý với đề xuất. Learner nhận giá trị đã đồng thuận để phục vụ client.
  - id: KP7_2
    content: Giải quyết xung đột qua 2 giai đoạn của Paxos
    keypoint_weight: 0.5
    description: Giai đoạn 1 (Prepare/Promise): Proposer gửi mã số đề xuất $N$; Acceptor cam kết từ chối các đề xuất có mã nhỏ hơn $N$. Giai đoạn 2 (Accept/Accepted): Proposer gửi giá trị kèm số $N$; Acceptor chấp nhận nếu chưa hứa với đề xuất lớn hơn, giải quyết triệt để xung đột bằng cách chỉ chấp thuận đề xuất có số hiệu lớn nhất.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống phân phối vé ca nhạc tải cực cao (quy mô 100k requests/giây), đảm bảo không bán vượt số lượng vé thực tế (Over-selling) sử dụng cơ chế Distributed Lock và Transaction Isolation.
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
* **Câu hỏi:** Thiết kế hệ thống cơ sở dữ liệu đa vùng chủ động-chủ động (Multi-region Active-Active Database) đảm bảo đồng bộ hóa hai chiều và giải quyết xung đột dữ liệu (Conflict Resolution) dựa trên Vector Clocks hoặc CRDTs.
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
* **Câu hỏi:** Xây dựng giải pháp đảm bảo tính nhất quán dữ liệu giữa Transactional Database (PostgreSQL) và Search Index (Elasticsearch) quy mô lớn sử dụng Outbox Pattern kết hợp Change Data Capture (CDC) qua Kafka.
* **expected_key_points:**
  - id: KP10_1
    content: Thiết kế Outbox Pattern
    keypoint_weight: 0.5
    description: Khi cập nhật DB, ghi thông tin sự kiện thay đổi vào một bảng phụ tên `outbox_table` trong cùng một transaction cục bộ (đảm bảo tính nguyên tử tuyệt đối).
  - id: KP10_2
    content: Đọc dữ liệu CDC và Đồng bộ Elasticsearch
    keypoint_weight: 0.5
    description: Sử dụng công cụ CDC (như Debezium) đọc logs của bảng outbox -> đẩy vào Kafka topic -> Subscriber tiêu thụ tin nhắn từ Kafka và cập nhật bất đồng bộ vào Elasticsearch, giải phóng tài nguyên tính toán của PostgreSQL.

