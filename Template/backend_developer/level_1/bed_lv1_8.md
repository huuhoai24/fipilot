# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 1)

* **Role:** Backend Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong kiến trúc Web, giao thức HTTP hoạt động theo mô hình nào? Hãy nêu điểm khác biệt cơ bản về tính năng lưu trữ thông tin trạng thái giữa HTTP và một kết nối dùng Session/Cookie.
* **expected_key_points:**
  - id: KP1_1
    content: Mô hình Request-Response (Yêu cầu - Phản hồi)
    keypoint_weight: 0.4
    description: HTTP hoạt động theo mô hình Client-Server, trong đó Client gửi một HTTP Request lên máy chủ và Server xử lý rồi trả về một HTTP Response, kết nối sau đó kết thúc.
  - id: KP1_2
    content: Tính chất không lưu trạng thái (Stateless) của HTTP
    keypoint_weight: 0.6
    description: Bản chất HTTP là giao thức Stateless, mỗi Request độc lập hoàn toàn và Server không tự động lưu giữ thông tin của các Request trước đó. Do đó, hệ thống cần sử dụng thêm cơ chế Session/Cookie hoặc Token để lưu giữ trạng thái đăng nhập/phiên làm việc của người dùng (Stateful).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt sự khác nhau về mặt logic tập hợp dữ liệu kết quả khi sử dụng phép toán `LEFT JOIN` và `RIGHT JOIN` trong câu lệnh SQL.
* **expected_key_points:**
  - id: KP2_1
    content: Logic xử lý của phép toán LEFT JOIN
    keypoint_weight: 0.5
    description: Trả về tất cả các hàng từ bảng bên trái (Left table) và các hàng trùng khớp từ bảng bên phải (Right table). Nếu không có hàng trùng khớp, các cột của bảng bên phải sẽ nhận giá trị NULL.
  - id: KP2_2
    content: Logic xử lý của phép toán RIGHT JOIN
    keypoint_weight: 0.5
    description: Trả về tất cả các hàng từ bảng bên phải (Right table) và các hàng trùng khớp từ bảng bên trái (Left table). Nếu không có hàng trùng khớp, các cột của bảng bên trái sẽ nhận giá trị NULL (hoạt động đối xứng ngược với LEFT JOIN).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Khi thiết kế một ứng dụng Backend, việc băm mật khẩu (Password Hashing) đóng vai trò gì và tại sao chúng ta không được phép lưu mật khẩu dưới dạng văn bản thô (Plain text) vào Database?
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế mã hóa một chiều ngăn chặn lộ thông tin gốc
    keypoint_weight: 0.6
    description: Hashing là phép toán biến đổi một chiều (One-way function). Mật khẩu thô đi qua hàm băm (như BCrypt, Argon2) để tạo ra một chuỗi ký tự đại diện cố định và không thể bị dịch ngược lại thành mật khẩu gốc.
  - id: KP3_2
    content: Giảm thiểu thiệt hại khi Database bị rò rỉ (Data Breach)
    keypoint_weight: 0.4
    description: Ngăn chặn việc quản trị viên hệ thống hoặc hacker (nếu chiếm quyền truy cập Database) có thể đọc và lấy trực tiếp mật khẩu của người dùng, bảo vệ tài khoản của họ trên các hệ thống khác.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong thiết kế hướng đối tượng và bộ nguyên lý SOLID, nguyên lý "Liskov Substitution Principle" (LSP - Nguyên lý thay thế Liskov) quy định điều gì và nêu một dấu hiệu vi phạm nguyên lý này khi viết code?
* **expected_key_points:**
  - id: KP4_1
    content: Quy tắc thay thế không phá vỡ tính đúng đắn của chương trình
    keypoint_weight: 0.5
    description: Quy định các đối tượng thuộc lớp con (Subclass) phải có khả năng thay thế hoàn toàn cho đối tượng của lớp cha (Superclass) mà không làm thay đổi hay phá vỡ tính đúng đắn logic của chương trình.
  - id: KP4_2
    content: Dấu hiệu vi phạm qua việc ném ngoại lệ hoặc thay đổi hành vi cốt lõi
    keypoint_weight: 0.5
    description: Vi phạm xảy ra khi lớp con ghi đè (override) một hàm của lớp cha nhưng lại ném ra một ngoại lệ không được định nghĩa (`NotImplementedException`), hoặc làm thay đổi hoàn toàn kỳ vọng kết quả đầu ra của lớp cha, ép Client phải kiểm tra kiểu dữ liệu (`instanceof`) trước khi gọi hàm.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy phân biệt điểm khác biệt về cơ chế hoạt động, ưu nhược điểm giữa hai chiến lược tải dữ liệu liên quan của các thư viện ORM: Eager Loading và Lazy Loading.
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế lấy dữ liệu đồng thời của Eager Loading
    keypoint_weight: 0.5
    description: Eager Loading tự động truy vấn và tải toàn bộ dữ liệu quan hệ liên quan (cha và con) ngay trong câu lệnh SQL đầu tiên (thường dùng phép JOIN). Ưu điểm là tránh lỗi N+1 Query, nhưng nhược điểm là tiêu tốn nhiều bộ nhớ RAM và làm chậm câu lệnh nếu dữ liệu con quá lớn và không dùng đến.
  - id: KP5_2
    content: Cơ chế tải dữ liệu khi có yêu cầu gọi của Lazy Loading
    keypoint_weight: 0.5
    description: Lazy Loading trì hoãn việc tải dữ liệu liên quan; dữ liệu con chỉ thực sự được truy vấn từ DB khi mã nguồn gọi trực tiếp đến thuộc tính của nó. Ưu điểm là tiết kiệm tài nguyên ban đầu, nhưng nhược điểm lớn là cực kỳ dễ phát sinh hiện tượng N+1 Query Problem nếu gọi trong vòng lặp.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong kiến trúc hệ thống, lỗ hổng "Broken Object Level Authorization" (BOLA / IDOR) xảy ra do lỗi logic nào ở Backend và giải pháp phòng chống triệt để là gì?
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên nhân thiếu bước phân quyền dựa trên định danh tài nguyên (Object-level check)
    keypoint_weight: 0.5
    description: Xảy ra khi Backend đã xác thực được danh tính người dùng (Authentication thành công), nhưng tại Endpoint xử lý lại tin tưởng hoàn toàn vào ID tài nguyên do Client gửi lên mà không kiểm tra xem người dùng hiện tại có quyền sở hữu hoặc thao tác trên tài nguyên đó hay không (ví dụ: thay đổi `invoice_id` trên URL để xem hóa đơn người khác).
  - id: KP6_2
    content: Giải pháp xác thực quyền hạn dựa trên Context thông tin người dùng bảo mật
    keypoint_weight: 0.5
    description: Tại mỗi API xử lý theo ID, Backend bắt buộc phải trích xuất User ID an toàn từ Session/Token, sau đó thực hiện câu lệnh truy vấn đối chiếu quyền sở hữu đối với bản ghi tài nguyên yêu cầu trong DB trước khi trả về dữ liệu.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Khái niệm "Database Migration" đóng vai trò quản lý gì trong quy trình phát triển sản phẩm Backend theo đội ngũ (Teamwork)?
* **expected_key_points:**
  - id: KP7_1
    content: Hệ thống quản lý phiên bản cho cấu trúc cơ sở dữ liệu (Version Control for Database)
    keypoint_weight: 0.5
    description: Migration lưu trữ các thay đổi về cấu trúc Database (tạo bảng, thêm cột, sửa kiểu dữ liệu) dưới dạng các file mã nguồn có thứ tự thời gian, cho phép theo dõi lịch sử biến đổi giống như Git quản lý code.
  - id: KP7_2
    content: Đồng bộ hóa môi trường nhất quán giữa các lập trình viên và hệ thống (CI/CD)
    keypoint_weight: 0.5
    description: Giúp tất cả lập trình viên trong đội ngũ và các môi trường chạy thử (Staging, Production) dễ dàng đồng bộ cấu trúc DB chính xác bằng cách chạy một câu lệnh tự động, tránh việc sửa cấu trúc bằng tay gây sai lệch dữ liệu.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Khi xây dựng hệ thống phân tán, định lý "CAP Theorem" quy định sự đánh đổi kỹ thuật như thế nào khi hiện tượng lỗi phân đoạn mạng (Network Partition) xảy ra?
* **expected_key_points:**
  - id: KP8_1
    content: Giới hạn tối đa 2 trên 3 yếu tố (Consistency, Availability, Partition Tolerance)
    keypoint_weight: 0.4
    description: Khẳng định một hệ thống dữ liệu phân tán chỉ có thể đạt được tối đa 2 trong 3 tính chất tại một thời điểm: Nhất quán dữ liệu (C), Sẵn sàng phản hồi (A), và Chịu lỗi phân đoạn mạng (P).
  - id: KP8_2
    content: Tính bắt buộc của yếu tố P trong môi trường mạng thực tế
    keypoint_weight: 0.2
    description: Môi trường mạng vật lý luôn tiềm ẩn nguy cơ mất kết nối hoặc đứt cáp giữa các Node (Network Partition), nên yếu tố P (Partition Tolerance) là bắt buộc phải lựa chọn trong thiết kế hệ thống phân tán thực tế.
  - id: KP8_3
    content: Sự đánh đổi bắt buộc giữa cấu trúc CP và AP khi xảy ra lỗi mạng
    keypoint_weight: 0.4
    description: Khi xuất hiện lỗi phân đoạn mạng, hệ thống buộc phải chọn: Hoặc bảo toàn **Consistency (Mô hình CP)** bằng cách từ chối request/báo lỗi để tránh sai lệch dữ liệu giữa các node; Hoặc bảo toàn **Availability (Mô hình AP)** bằng cách chấp nhận trả về dữ liệu cũ/sai lệch từ các node bị cô lập để hệ thống luôn sẵn sàng hoạt động.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích nguyên lý hoạt động kỹ thuật của cấu trúc dữ liệu Bloom Filter và lý do tại sao nó được ứng dụng để tối ưu hóa hiệu năng đọc (Read Performance) trước khi truy vấn xuống Database lớn.
* **expected_key_points:**
  - id: KP9_1
    content: Nguyên lý mảng Bit toán học và tập hợp hàm băm độc lập (Probabilistic Structure)
    keypoint_weight: 0.4
    description: Bloom Filter sử dụng một mảng bit ban đầu bằng 0 và $k$ hàm băm độc lập. Khi nạp phần tử, chuỗi qua $k$ hàm băm để tìm vị trí và chuyển bit thành 1. Khi kiểm tra, nếu có ít nhất một vị trí bit bằng 0, phần tử chắc chắn 100% chưa tồn tại (Không có False Negative).
  - id: KP9_2
    content: Ứng dụng làm bộ lọc chặn các truy vấn lãng phí (Chặn Cache Penetration)
    keypoint_weight: 0.4
    description: Đặt Bloom Filter nằm trước Database. Khi nhận request tìm kiếm ID, hệ thống kiểm tra qua Bloom Filter trước; nếu trả về "Không tồn tại", Backend phản hồi lỗi ngay lập tức mà không cần tốn chi phí thực hiện câu lệnh truy vấn đọc đĩa cứng IO của Database, giúp bảo vệ DB khỏi các cuộc tấn công quét ID rác.
  - id: KP9_3
    content: Đánh đổi rủi ro xảy ra hiện tượng False Positive (Dương tính giả)
    keypoint_weight: 0.2
    description: Do xung đột băm (Collision), Bloom Filter có xác suất nhỏ báo một phần tử "đã tồn tại" dù thực tế chưa có. Trong tình huống đó, request vẫn đi tiếp xuống DB để tìm kiếm (trả về rỗng), hệ thống chấp nhận sự đánh đổi này để đổi lấy tốc độ và không gian nhớ cực nhỏ $O(1)$.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong thiết kế kiến trúc Microservices hướng sự kiện (Event-Driven Architecture), hãy giải thích nguyên lý hoạt động và mục đích sử dụng của mẫu thiết kế "Transactional Outbox Pattern".
* **expected_key_points:**
  - id: KP10_1
    content: Giải quyết bài toán không đồng bộ giữa ghi Database nội bộ và bắn Message Broker
    keypoint_weight: 0.4
    description: Đảm bảo tính toàn vẹn dữ liệu khi một Service cần đồng thời thực hiện hai hành động: Cập nhật Database của riêng nó và gửi một sự kiện (Event) sang Message Broker (như Kafka) cho các service khác. Nếu không có mẫu thiết kế này, một trong hai hành động lỗi sẽ gây mất đồng bộ hệ thống.
  - id: KP10_2
    content: Cơ chế sử dụng bảng Outbox trung gian trong cùng một Database Transaction
    keypoint_weight: 0.4
    description: Thay vì gửi trực tiếp sự kiện sang Message Broker trong lúc xử lý, Service sẽ lưu thông tin sự kiện đó dưới dạng một bản ghi vào một bảng trung gian gọi là bảng `Outbox` nằm ngay trong cùng một giao dịch cơ sở dữ liệu (Database Transaction) của nghiệp vụ chính. Điều này đảm bảo cả hai hành động ghi dữ liệu nghiệp vụ và ghi sự kiện đều cùng thành công hoặc cùng thất bại (ACID).
  - id: KP10_3
    content: Tiến trình quét độc lập chuyển tiếp sự kiện (Message Relay / Change Data Capture)
    keypoint_weight: 0.2
    description: Một tiến trình chạy độc lập song song (như Transaction Log Miner hoặc Polling Publisher) sẽ liên tục rà soát bảng `Outbox` này để lấy các sự kiện chưa xử lý, bắn chúng sang Message Broker, và đánh dấu đã hoàn thành sau khi nhận được phản hồi xác nhận thành công từ Broker.