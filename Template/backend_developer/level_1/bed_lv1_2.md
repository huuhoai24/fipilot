# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 1)

* **Role:** Backend Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế RESTful API, bốn phương thức HTTP Methods: GET, POST, PUT, DELETE đóng vai trò gì và phương thức nào có tính chất Idempotent (Đồng nhất)?
* **expected_key_points:**
  - id: KP1_1
    content: Vai trò xử lý dữ liệu của các phương thức (CRUD Operations)
    keypoint_weight: 0.5
    description: GET dùng để đọc dữ liệu (Read); POST dùng để tạo mới dữ liệu (Create); PUT dùng để cập nhật đè toàn bộ dữ liệu (Update); DELETE dùng để xóa dữ liệu (Delete).
  - id: KP1_2
    content: Xác định chính xác tính chất Idempotent (Tính đồng nhất)
    keypoint_weight: 0.5
    description: Idempotent nghĩa là việc thực hiện một yêu cầu nhiều lần liên tiếp sẽ cho ra cùng một kết quả trên hệ thống giống như thực hiện một lần duy nhất. Các phương thức có tính Idempotent là GET, PUT, DELETE. POST không có tính chất này vì nhiều request liên tiếp sẽ tạo ra nhiều bản ghi trùng lặp.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong Cơ sở dữ liệu quan hệ (RDBMS), việc thiết lập chỉ mục (Database Index) đem lại lợi ích gì cho hệ thống Backend và hệ quả tiêu cực của nó là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Lợi ích tăng tốc độ truy vấn (Read Performance)
    keypoint_weight: 0.5
    description: Index giúp tăng đáng kể tốc độ tìm kiếm và truy vấn dữ liệu (SELECT) bằng cách cho phép Database Engine tìm kiếm trực tiếp qua cấu trúc chỉ mục (như B-Tree) thay vì phải quét toàn bộ bảng dữ liệu (Table Scan).
  - id: KP2_2
    content: Chi phí bộ nhớ và giảm hiệu năng ghi dữ liệu (Write Overhead)
    keypoint_weight: 0.5
    description: Index làm tiêu tốn thêm không gian lưu trữ trên ổ đĩa. Đồng thời, nó làm giảm tốc độ của các thao tác ghi (INSERT, UPDATE, DELETE) vì Database bắt buộc phải tốn thêm tài nguyên tính toán để cập nhật và sắp xếp lại cấu trúc của cây chỉ mục.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Sự khác biệt cốt lõi về mặt bảo mật thông tin trên đường truyền mạng giữa hai giao thức HTTP và HTTPS là gì?
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế mã hóa dữ liệu của chứng chỉ SSL/TLS
    keypoint_weight: 0.6
    description: HTTP truyền dữ liệu dưới dạng văn bản thô (Plain text), không mã hóa, dễ bị hacker can thiệp và nghe lén. HTTPS tích hợp thêm lớp bảo mật mã hóa SSL/TLS để chuyển đổi toàn bộ dữ liệu truyền tải thành các chuỗi mật mã an toàn.
  - id: KP3_2
    content: Xác thực danh tính máy chủ (Server Authentication)
    keypoint_weight: 0.4
    description: HTTPS cung cấp cơ chế xác thực máy chủ thông qua chứng chỉ số được cấp phát bởi các bên trung gian uy tín (Certificate Authority - CA), giúp Client đảm bảo đang kết nối đúng đến máy chủ thật chứ không phải máy chủ giả mạo.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong thiết kế hệ thống phần mềm, nguyên lý "S" (Single Responsibility Principle - SRP) và "O" (Open/Closed Principle - OCP) trong bộ nguyên lý SOLID quy định quy tắc viết code như thế nào?
* **expected_key_points:**
  - id: KP4_1
    content: Nguyên lý Đơn trách nhiệm (Single Responsibility Principle)
    keypoint_weight: 0.5
    description: Quy định một Class, Module hoặc Hàm chỉ nên đảm nhận một trách nhiệm cốt lõi duy nhất, nghĩa là nó chỉ có một và duy nhất một lý do để thay đổi khi yêu cầu nghiệp vụ thay đổi.
  - id: KP4_2
    content: Nguyên lý Đóng/Mở (Open/Closed Principle)
    keypoint_weight: 0.5
    description: Quy định một thành phần phần mềm nên được thiết kế mở đối với việc mở rộng tính năng mới (Open for extension) nhưng đóng lại đối với việc sửa đổi mã nguồn cốt lõi hiện tại (Closed for modification) nhằm tránh làm gãy hệ thống cũ.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi xây dựng tính năng Xác thực người dùng (Authentication), hãy phân biệt cơ chế Session-based Authentication và Token-based Authentication (như JWT) về mặt lưu trữ trạng thái (State).
* **expected_key_points:**
  - id: KP5_1
    content: Bản chất lưu trạng thái (Stateful) của Session-based Authentication
    keypoint_weight: 0.5
    description: Server chịu trách nhiệm tạo và lưu trữ thông tin Session của người dùng trong bộ nhớ (RAM/Database). Client chỉ lưu một chuỗi Session ID trong Cookie. Mỗi request gửi lên, Server bắt buộc phải đối chiếu Session ID với bộ lưu trữ của mình để xác thực.
  - id: KP5_2
    content: Bản chất không lưu trạng thái (Stateless) của Token-based Authentication (JWT)
    keypoint_weight: 0.5
    description: Toàn bộ thông tin định danh của người dùng được mã hóa và ký số bảo mật nằm ngay trong chuỗi Token cấp cho Client lưu trữ. Server không cần lưu trạng thái token; mỗi request gửi lên, Server chỉ cần giải mã kiểm tra tính toàn vẹn của chữ ký số (Signature) là có thể xác thực người dùng ngay lập tức.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy giải thích quy trình xử lý luồng dữ liệu của chiến lược "Cache-Aside Pattern" (như dùng Redis làm bộ đệm cho MySQL) khi hệ thống tiếp nhận một yêu cầu đọc dữ liệu (Read Request).
* **expected_key_points:**
  - id: KP6_1
    content: Luồng xử lý khi xảy ra hiện tượng Cache Hit
    keypoint_weight: 0.4
    description: Ứng dụng Backend kiểm tra key dữ liệu trong Cache trước. Nếu dữ liệu tồn tại (Cache Hit), lấy dữ liệu ra và trả về ngay lập tức cho Client mà không cần truy vấn xuống Database.
  - id: KP6_2
    content: Luồng xử lý khi xảy ra hiện tượng Cache Miss
    keypoint_weight: 0.6
    description: Nếu dữ liệu không tồn tại trong Cache (Cache Miss), Backend sẽ thực hiện câu lệnh truy vấn dữ liệu từ Database gốc, trả về kết quả cho Client, đồng thời lập tức ghi nạp dữ liệu đó kèm thời gian hết hạn (TTL) vào Cache để phục vụ cho các lượt gọi sau.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Lỗ hổng bảo mật ứng dụng Web "SQL Injection" xảy ra do lỗi lập trình nào ở Backend và làm thế nào để phòng chống triệt để lỗ hổng này?
* **expected_key_points:**
  - id: KP7_1
    content: Nguyên nhân do nối chuỗi dữ liệu đầu vào trực tiếp (Raw SQL String Concatenation)
    keypoint_weight: 0.5
    description: Xảy ra khi Backend tin tưởng và thực hiện nối các chuỗi dữ liệu thô do người dùng nhập từ giao diện trực tiếp vào câu lệnh SQL truy vấn Database, tạo cơ hội cho hacker chèn thêm các đoạn mã SQL độc hại để thao túng cấu trúc câu lệnh gốc.
  - id: KP7_2
    content: Giải pháp phòng chống bằng Parameterized Queries (Prepared Statements)
    keypoint_weight: 0.5
    description: Sử dụng kỹ thuật Parameterized Queries (hoặc dùng các thư viện ORM). Cơ chế này ép dữ liệu nhập vào của người dùng bắt buộc chỉ được xử lý như một tham số truyền thuần túy (Literal value), tách biệt hoàn toàn và không có quyền thực thi như câu lệnh SQL.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong quản lý giao dịch Cơ sở dữ liệu (Database Transactions), hãy giải thích ý nghĩa logic của bốn tính chất trong bộ nguyên lý ACID.
* **expected_key_points:**
  - id: KP8_1
    content: Tính nguyên tử (Atomicity) và Tính nhất quán (Consistency)
    keypoint_weight: 0.5
    description: Atomicity quy định giao dịch phải được thực hiện trọn vẹn "tất cả hoặc không có gì" (All or Nothing); nếu một lệnh lỗi, toàn bộ giao dịch bị hủy bỏ (Rollback). Consistency đảm bảo dữ liệu phải chuyển đổi hợp lệ từ trạng thái đúng này sang trạng thái đúng khác, không vi phạm các ràng buộc (Constraints/Rules).
  - id: KP8_2
    content: Tính cô lập (Isolation) và Tính bền vững (Durability)
    keypoint_weight: 0.5
    description: Isolation đảm bảo các giao dịch chạy song song không được can thiệp hay nhìn thấy dữ liệu tạm thời của nhau cho đến khi được Commit chính thức. Durability đảm bảo một khi giao dịch đã Commit thành công, dữ liệu sẽ được lưu trữ vĩnh viễn xuống ổ đĩa cứng, không bị mất ngay cả khi hệ thống sập nguồn đột ngột.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Khi xây dựng kiến trúc Microservices hoặc hệ thống phân tán, định lý "CAP Theorem" khẳng định điều gì về sự đánh đổi kỹ thuật khi xảy ra hiện tượng lỗi phân đoạn mạng (Network Partition)?
* **expected_key_points:**
  - id: KP9_1
    content: Giới hạn tối đa 2 trên 3 yếu tố của hệ thống phân tán
    keypoint_weight: 0.3
    description: Định lý CAP khẳng định một hệ thống dữ liệu phân tán chỉ có thể đáp ứng tối đa 2 trong 3 yếu tố: C (Consistency - Tính nhất quán), A (Availability - Tính sẵn sàng), và P (Partition Tolerance - Tính chịu lỗi phân đoạn mạng).
  - id: KP9_2
    content: Sự bắt buộc của yếu tố P trong môi trường mạng thực tế
    keypoint_weight: 0.3
    description: Vì môi trường mạng vật lý luôn tiềm ẩn rủi ro lỗi phần cứng, đứt cáp hoặc mất kết nối giữa các node, nên yếu tố P (Partition Tolerance) là bắt buộc phải lựa chọn trong thiết kế hệ thống phân tán.
  - id: KP9_3
    content: Sự đánh đổi duy nhất giữa kiến trúc CP và AP khi có sự cố
    keypoint_weight: 0.4
    description: Khi xảy ra sự cố Network Partition, hệ thống chỉ được phép chọn 1 trong 2 hướng: Hoặc bảo toàn Consistency (Kiến trúc CP) - từ chối xử lý hoặc báo lỗi request để tránh sai lệch dữ liệu giữa các node; Hoặc bảo toàn Availability (Kiến trúc AP) - chấp nhận cho các node phản hồi dữ liệu dù có thể bị lệch toán học (dữ liệu cũ) để đảm bảo hệ thống luôn sẵn sàng sống.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân biệt điểm khác nhau về mặt cơ chế hoạt động mạng, ưu nhược điểm giữa hai mô hình giao tiếp kiến trúc hệ thống: HTTP REST API (Synchronous) và Message Broker (Asynchronous hướng sự kiện).
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế giao tiếp đồng bộ (Synchronous) của REST API
    keypoint_weight: 0.5
    description: Hoạt động theo mô hình Request-Response trực tiếp. Client gửi yêu cầu lên Server và bắt buộc phải treo luồng tính toán để đợi Server phản hồi kết quả về rồi mới chạy tiếp. Dễ gây nghẽn mạch dây chuyền nếu một dịch vụ phía sau bị chậm (Tight Coupling).
  - id: KP10_2
    content: Cơ chế giao tiếp bất đồng bộ (Asynchronous) của Message Broker
    keypoint_weight: 0.5
    description: Hoạt động theo mô hình Event-driven (Publisher-Subscriber) gián tiếp thông qua hàng đợi (như Kafka, RabbitMQ). Dịch vụ gửi (Producer) chỉ cần đẩy thông điệp vào Broker rồi tiếp tục làm việc khác ngay lập tức; dịch vụ nhận (Consumer) tự động lấy ra xử lý sau, giúp hệ thống giảm sự phụ thuộc giữa các dịch vụ (Loose Coupling) và tăng khả năng chịu tải.