# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 1)

* **Role:** Backend Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong phát triển ứng dụng Backend, việc băm mật khẩu (Password Hashing) khác gì so với mã hóa mật khẩu (Password Encryption)? Tại sao không được lưu mật khẩu dạng văn bản thô (Plain Text)?
* **expected_key_points:**
  - id: KP1_1
    content: Tính chất toán học một chiều của Hashing (One-way)
    keypoint_weight: 0.4
    description: Hashing là hàm biến đổi một chiều. Một khi mật khẩu đã băm thì không thể giải mã ngược lại để lấy chuỗi thô ban đầu, giúp bảo mật tuyệt đối ngay cả khi lộ chuỗi băm.
  - id: KP1_2
    content: Tính chất hai chiều của Encryption (Two-way)
    keypoint_weight: 0.3
    description: Encryption là quá trình mã hóa hai chiều, dữ liệu có thể được giải mã ngược lại về dạng ban đầu nếu có khóa giải mã (Decryption Key). Do đó, ít an toàn hơn Hashing đối với việc lưu mật khẩu.
  - id: KP1_3
    content: Rủi ro lộ thông tin khi lưu Plain Text (Data Breach)
    keypoint_weight: 0.3
    description: Lưu Plain Text khiến bất kỳ ai có quyền truy cập DB (hacker hoặc admin) đều đọc được mật khẩu, gây nguy cơ chiếm đoạt tài khoản dây chuyền trên các hệ thống khác của người dùng.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt điểm khác nhau về mặt logic tập hợp kết quả và cơ chế lọc giữa hai mệnh đề `WHERE` và `HAVING` trong câu lệnh SQL.
* **expected_key_points:**
  - id: KP2_1
    content: Đối tượng và thời điểm lọc dữ liệu của WHERE
    keypoint_weight: 0.5
    description: Mệnh đề WHERE lọc dữ liệu trên từng hàng thô (Raw rows) trước khi phép toán gộp nhóm (GROUP BY) diễn ra. WHERE không thể kết hợp với các hàm gộp (Aggregate functions).
  - id: KP2_2
    content: Đối tượng và thời điểm lọc dữ liệu của HAVING
    keypoint_weight: 0.5
    description: Mệnh đề HAVING lọc dữ liệu sau khi các hàng đã được gộp nhóm bởi GROUP BY. HAVING làm việc trên kết quả của nhóm và thường xuyên đi kèm các hàm gộp (như SUM, COUNT, AVG).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Giao thức mạng TCP (Transmission Control Protocol) và UDP (User Datagram Protocol) khác nhau như thế nào về cơ chế khởi tạo kết nối và độ tin cậy truyền tải?
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế hướng kết nối và tính đảm bảo dữ liệu của TCP
    keypoint_weight: 0.5
    description: TCP là giao thức hướng kết nối (Connection-oriented), bắt buộc phải bắt tay 3 bước (3-way handshake) trước khi truyền tin. Nó đảm bảo dữ liệu đến đích nguyên vẹn, đúng thứ tự và có cơ chế kiểm soát luồng/lỗi.
  - id: KP3_2
    content: Cơ chế không kết nối và tối ưu tốc độ của UDP
    keypoint_weight: 0.5
    description: UDP là giao thức không hướng kết nối (Connectionless), truyền gói tin đi ngay lập tức mà không cần thiết lập phiên. Nó không đảm bảo dữ liệu đến đích hay đúng thứ tự nhưng cho tốc độ cực nhanh, ít tốn băng thông (phù hợp Streaming/VoIP).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong thiết kế hướng đối tượng và bộ nguyên lý SOLID, nguyên lý "Liskov Substitution Principle" (LSP) quy định điều gì và nêu một dấu hiệu vi phạm phổ biến khi viết code?
* **expected_key_points:**
  - id: KP4_1
    content: Quy tắc thay thế đối tượng không làm thay đổi tính đúng đắn của hệ thống
    keypoint_weight: 0.5
    description: Quy định các đối tượng thuộc lớp con (Subclass) phải có khả năng thay thế hoàn toàn cho đối tượng của lớp cha (Superclass) mà không làm thay đổi hoặc phá vỡ tính đúng đắn logic của chương trình.
  - id: KP4_2
    content: Dấu hiệu vi phạm qua việc ném ngoại lệ hoặc làm rỗng hàm kế thừa
    keypoint_weight: 0.5
    description: Vi phạm xảy ra khi lớp con ghi đè một hàm của lớp cha nhưng lại ném ra ngoại lệ không mong muốn (ví dụ: `NotImplementedException`), hoặc phá vỡ các tiền điều kiện/hậu điều kiện của lớp cha, ép Client phải dùng phép kiểm tra kiểu dữ liệu (`instanceof`) trước khi gọi.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy phân biệt điểm khác biệt về cơ chế hoạt động, ưu điểm và nhược điểm của hai chiến lược tải dữ liệu liên quan của các thư viện ORM: Eager Loading và Lazy Loading.
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế lấy dữ liệu đồng thời của Eager Loading
    keypoint_weight: 0.5
    description: Eager Loading tự động truy vấn và tải toàn bộ dữ liệu quan hệ (cha và con) ngay trong câu lệnh đầu tiên thông qua phép toán JOIN. Giúp triệt tiêu lỗi N+1 Query, nhưng tiêu tốn bộ nhớ RAM và làm chậm câu lệnh nếu dữ liệu con khổng lồ mà không dùng đến.
  - id: KP5_2
    content: Cơ chế trì hoãn tải dữ liệu của Lazy Loading
    keypoint_weight: 0.5
    description: Lazy Loading trì hoãn việc tải dữ liệu con; dữ liệu con chỉ thực sự được truy vấn từ DB khi mã nguồn Backend gọi trực tiếp thuộc tính của nó. Tiết kiệm tài nguyên ban đầu nhưng cực kỳ dễ phát sinh hiện tượng N+1 Query Problem nếu gọi lặp trong vòng lặp.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Lỗ hổng bảo mật logic API "Broken Object Level Authorization" (BOLA / IDOR) xảy ra do lỗi lập trình nào ở Backend và giải pháp xử lý triệt để là gì?
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên nhân thiếu bước phân quyền dựa trên định danh tài nguyên (Object Check)
    keypoint_weight: 0.5
    description: Xảy ra khi Backend đã xác thực thành công danh tính người dùng (Authentication), nhưng tại Endpoint xử lý lại tin tưởng hoàn toàn vào ID tài nguyên do Client truyền lên mà không kiểm tra xem người dùng hiện tại có quyền sở hữu hoặc thao tác trên tài nguyên cụ thể đó hay không (ví dụ: sửa ID trên URL để xem hóa đơn người khác).
  - id: KP6_2
    content: Giải pháp xác thực quyền hạn dựa trên Context thông tin người dùng bảo mật
    keypoint_weight: 0.5
    description: Tại mỗi logic xử lý API liên quan đến ID tài nguyên, Backend bắt buộc phải trích xuất User ID an toàn từ Session/Token bảo mật, sau đó thực hiện câu lệnh truy vấn đối chiếu quyền hạn thực tế trên bản ghi dữ liệu yêu cầu trước khi trả về kết quả.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong quy trình phát triển sản phẩm Backend theo đội ngũ (Teamwork), công cụ "Database Migration" đóng vai trò quản lý gì?
* **expected_key_points:**
  - id: KP7_1
    content: Quản lý phiên bản cho cấu trúc cơ sở dữ liệu (Version Control for DB)
    keypoint_weight: 0.5
    description: Migration lưu trữ các thay đổi về cấu trúc Database (tạo bảng, thêm cột, sửa kiểu dữ liệu) dưới dạng các file mã nguồn có thứ tự thời gian, giúp theo dõi và quản lý lịch sử biến đổi của DB giống như Git quản lý mã nguồn.
  - id: KP7_2
    content: Đồng bộ hóa tính nhất quán môi trường tự động (CI/CD)
    keypoint_weight: 0.5
    description: Giúp tất cả lập trình viên trong đội ngũ và các môi trường chạy thử, môi trường thật (Staging, Production) dễ dàng đồng bộ cấu trúc DB một cách chính xác bằng câu lệnh tự động, tránh việc sửa tay cấu trúc gây sai lệch dữ liệu giữa các môi trường.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Khi xây dựng hệ thống phân tán đa máy chủ, định lý "CAP Theorem" khẳng định điều gì về sự đánh đổi kỹ thuật khi hiện tượng lỗi phân đoạn mạng (Network Partition) xảy ra?
* **expected_key_points:**
  - id: KP8_1
    content: Giới hạn tối đa 2 trên 3 yếu tố (Consistency, Availability, Partition Tolerance)
    keypoint_weight: 0.4
    description: Khẳng định một hệ thống dữ liệu phân tán chỉ có thể đáp ứng tối đa 2 trong 3 tính chất tại một thời điểm: Nhất quán dữ liệu (C), Sẵn sàng phản hồi (A), và Chịu lỗi phân đoạn mạng (P).
  - id: KP8_2
    content: Tính bắt buộc của yếu tố P trong môi trường mạng thực tế
    keypoint_weight: 0.2
    description: Môi trường mạng vật lý luôn tiềm ẩn rủi ro mất kết nối hoặc đứt cáp giữa các Node (Network Partition), nên yếu tố P là bắt buộc phải lựa chọn trong thiết kế hệ thống phân tán thực tế.
  - id: KP8_3
    content: Sự đánh đổi bắt buộc giữa cấu trúc CP và AP khi xảy ra sự cố mạng
    keypoint_weight: 0.4
    description: Khi có lỗi mạng, hệ thống buộc phải chọn: Hoặc bảo toàn Consistency (Mô hình CP) bằng cách từ chối request để tránh sai lệch dữ liệu giữa các node; Hoặc bảo toàn Availability (Mô hình AP) bằng cách chấp nhận phản hồi dữ liệu cũ/sai lệch từ các node bị cô lập để hệ thống luôn sẵn sàng sống.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích cấu trúc toán học logic và nguyên lý hoạt động của cấu trúc dữ liệu Bloom Filter. Tại sao nó được ứng dụng làm bộ lọc chặn trước Database lớn?
* **expected_key_points:**
  - id: KP9_1
    content: Nguyên lý mảng Bit toán học và tập hợp hàm băm độc lập (Probabilistic Structure)
    keypoint_weight: 0.4
    description: Bloom Filter sử dụng một mảng bit ban đầu bằng 0 và $k$ hàm băm độc lập. Khi nạp phần tử, chuỗi qua $k$ hàm băm để tìm vị trí và chuyển bit thành 1. Khi kiểm tra, nếu có ít nhất một vị trí bit bằng 0, phần tử chắc chắn 100% chưa tồn tại (Không bao giờ có lỗi False Negative).
  - id: KP9_2
    content: Ứng dụng tối ưu hóa hiệu năng đọc và đánh chặn truy vấn lãng phí (Chặn Cache Penetration)
    keypoint_weight: 0.4
    description: Đặt Bloom Filter nằm trước Database. Khi nhận request tìm kiếm ID, hệ thống kiểm tra qua Bloom Filter trước; nếu trả về "Không tồn tại", Backend phản hồi lỗi ngay lập tức mà không cần tốn chi phí thực hiện câu lệnh truy vấn đọc đĩa cứng IO của Database, giúp bảo vệ DB khỏi các cuộc tấn công quét ID rác.
  - id: KP9_3
    content: Đánh đổi rủi ro xảy ra hiện tượng False Positive (Dương tính giả)
    keypoint_weight: 0.2
    description: Do xung đột băm (Collision), Bloom Filter có xác suất nhỏ báo một phần tử "đã tồn tại" dù thực tế chưa có. Khi đó request vẫn xuống DB tìm kiếm (trả về rỗng), hệ thống chấp nhận sự đánh đổi này để đổi lấy tốc độ và không gian nhớ cực nhỏ $O(1)$.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong thiết kế kiến trúc Microservices hướng sự kiện (Event-Driven Architecture), hãy giải thích nguyên lý hoạt động kỹ thuật và mục đích sử dụng của mẫu thiết kế "Transactional Outbox Pattern".
* **expected_key_points:**
  - id: KP10_1
    content: Giải quyết bài toán không đồng bộ giữa ghi DB nội bộ và bắn Message Broker
    keypoint_weight: 0.4
    description: Đảm bảo tính toàn vẹn dữ liệu khi một Service cần đồng thời thực hiện hai hành động: Cập nhật Database nội bộ của riêng nó và gửi một sự kiện (Event) sang Message Broker (như Kafka). Nếu không có mẫu thiết kế này, một trong hai hành động lỗi sẽ gây mất đồng bộ hệ thống.
  - id: KP10_2
    content: Cơ chế sử dụng bảng Outbox trung gian trong cùng một Database Transaction
    keypoint_weight: 0.4
    description: Thay vì gửi trực tiếp sự kiện sang Message Broker trong lúc xử lý, Service sẽ lưu thông tin sự kiện đó dưới dạng một bản ghi vào một bảng trung gian gọi là bảng `Outbox` nằm ngay trong cùng một giao dịch cơ sở dữ liệu (Database Transaction) của nghiệp vụ chính. Điều này đảm bảo cả hai hành động ghi dữ liệu nghiệp vụ và ghi sự kiện đều cùng thành công hoặc cùng thất bại (ACID).
  - id: KP10_3
    content: Tiến trình quét độc lập chuyển tiếp sự kiện (Message Relay / Change Data Capture)
    keypoint_weight: 0.2
    description: Một tiến trình chạy độc lập song song (như Transaction Log Miner hoặc Polling Publisher) sẽ liên tục rà soát bảng `Outbox` này để lấy các sự kiện chưa xử lý, bắn chúng sang Message Broker, và đánh dấu đã hoàn thành sau khi nhận được phản hồi xác nhận thành công từ Broker.