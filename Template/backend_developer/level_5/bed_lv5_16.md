# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 5) - Tập Đề HTTP/3 và Zero-Trust Security (16)

* **Role:** Backend Developer
* **Level:** Level 5
* **Experience:** Trên 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Phân tích cơ chế hoạt động và so sánh các điểm cải tiến cốt lõi của giao thức HTTP/3 (chạy trên UDP/QUIC) so với HTTP/2 (chạy trên TCP). Giao thức này giải quyết lỗi Head-of-line Blocking ra sao?
* **expected_key_points:**
  - id: KP1_1
    content: Giao thức truyền tải TCP vs UDP/QUIC
    keypoint_weight: 0.5
    description: HTTP/2 dùng TCP nên nếu mất 1 gói tin, toàn bộ kết nối bị dừng (Head-of-line blocking ở cấp TCP). HTTP/3 dùng giao thức QUIC chạy trên nền UDP, quản lý các luồng (streams) độc lập nhau.
  - id: KP1_2
    content: Giải quyết Head-of-line Blocking và Bắt tay nhanh
    keypoint_weight: 0.5
    description: Trong QUIC, nếu 1 stream bị mất gói tin, chỉ duy nhất stream đó bị chậm, các streams khác vẫn truyền nhận bình thường. QUIC kết hợp bắt tay mã hóa TLS 1.3 giúp thiết lập kết nối chỉ trong 1-RTT hoặc 0-RTT.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích cơ chế bắt tay (Handshake) của giao thức TLS 1.3. Tại sao nó lại giảm độ trễ thiết lập kết nối (1-RTT và 0-RTT) so với TLS 1.2?
* **expected_key_points:**
  - id: KP2_1
    content: Bắt tay 1-RTT của TLS 1.3
    keypoint_weight: 0.5
    description: TLS 1.2 yêu cầu 2 lần gửi/nhận (2-RTT) để hoàn thành bắt tay. TLS 1.3 gộp quá trình thỏa thuận thuật toán mã hóa và trao đổi khóa (Key Exchange) vào ngay lượt ClientHello đầu tiên, giảm xuống còn 1-RTT.
  - id: KP2_2
    content: Cơ chế 0-RTT (Zero Round Trip Time Resumption)
    keypoint_weight: 0.5
    description: Cho phép client gửi kèm dữ liệu ứng dụng ngay trong gói tin ClientHello đầu tiên nếu hai bên đã từng kết nối trước đó và sử dụng lại khóa cũ (Pre-Shared Key - PSK).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa Token-based Authentication (sử dụng JWT) và Session-based Authentication về mặt bảo mật, lưu trữ trạng thái và khả năng mở rộng quy mô hệ thống.
* **expected_key_points:**
  - id: KP3_1
    content: Lưu trữ trạng thái (Stateful vs Stateless)
    keypoint_weight: 0.5
    description: Session-based yêu cầu server lưu trữ trạng thái session (trong DB/Redis) và gửi Session ID cho client. Token-based (JWT) là không lưu trạng thái (stateless), mọi thông tin user nằm sẵn trong chữ ký của JWT lưu ở client.
  - id: KP3_2
    content: Khả năng mở rộng quy mô (Scalability)
    keypoint_weight: 0.5
    description: JWT dễ scale out hơn vì server không cần truy vấn session store ở mỗi request; tuy nhiên JWT khó thu hồi (revoke) trước hạn hơn Session-based.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế cơ chế bảo mật chống tấn công DDoS và Brute Force tại lớp API Gateway sử dụng IP Rate Limiting và Web Application Firewall (WAF).
* **expected_key_points:**
  - id: KP4_1
    content: Thiết lập IP Rate Limiting động
    keypoint_weight: 0.5
    description: Cấu hình Rate Limiting dựa trên IP kết hợp thuật toán Leaky Bucket; sử dụng Redis để đếm số request theo cửa sổ thời gian trượt (sliding window log).
  - id: KP4_2
    content: Tích hợp WAF và Phân tích hành vi
    keypoint_weight: 0.5
    description: Sử dụng WAF (như Cloudflare/AWS WAF) để chặn các mẫu payload tấn công SQL Injection, XSS; tự động cách ly các IP gửi request bất thường dựa trên điểm số uy tín IP (IP reputation score).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế hoạt động của WebSockets và Server-Sent Events (SSE) để truyền dữ liệu thời gian thực. Trong trường hợp nào bạn chọn giải pháp nào?
* **expected_key_points:**
  - id: KP5_1
    content: Nguyên lý WebSockets vs SSE
    keypoint_weight: 0.5
    description: WebSockets thiết lập kết nối song phương (duplex) hai chiều qua TCP. SSE thiết lập kết nối đơn phương một chiều từ server sang client qua giao thức HTTP tiêu chuẩn.
  - id: KP5_2
    content: Kịch bản lựa chọn áp dụng
    keypoint_weight: 0.5
    description: Chọn WebSockets cho ứng dụng chat, game online (cần gửi nhận liên tục từ cả hai phía). Chọn SSE cho bảng giá chứng khoán, tin tức trực tiếp, thông báo đẩy (chỉ cần server đẩy thông tin, client ít gửi ngược).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế giải pháp xác thực phân tán đa miền (Single Sign-On - SSO) sử dụng OAuth2 và OpenID Connect (OIDC).
* **expected_key_points:**
  - id: KP6_1
    content: Vai trò của Identity Provider (IdP) và Client
    keypoint_weight: 0.5
    description: Xây dựng IdP tập trung quản lý thông tin người dùng. Các ứng dụng (Clients) sử dụng luồng Authorization Code Flow để xác thực qua IdP.
  - id: KP6_2
    content: Sử dụng ID Token và Access Token
    keypoint_weight: 0.5
    description: IdP trả về ID Token (chứa thông tin profile người dùng dạng OIDC) và Access Token (để gọi các tài nguyên API được ủy quyền).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích cách phòng chống lỗi rò rỉ token bảo mật sử dụng JWT và cơ chế xoay vòng Refresh Token (Refresh Token Rotation).
* **expected_key_points:**
  - id: KP7_1
    content: Cơ chế xoay vòng Refresh Token (RTR)
    keypoint_weight: 0.6
    description: Mỗi lần client dùng Refresh Token để lấy Access Token mới, server sẽ thu hồi Refresh Token cũ và phát hành một cặp Access/Refresh Token hoàn toàn mới.
  - id: KP7_2
    content: Phát hiện tấn công dùng lại Token cũ (Replay detection)
    keypoint_weight: 0.4
    description: Nếu server nhận được một Refresh Token đã từng bị thu hồi -> lập tức coi là vụ rò rỉ bảo mật -> hủy bỏ toàn bộ phiên làm việc của user đó trên mọi thiết bị và yêu cầu login lại.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống Chat thời gian thực phục vụ 10 triệu người dùng kết nối đồng thời sử dụng WebSockets, cụm Redis Pub/Sub làm trung tâm định tuyến tin nhắn và Kafka để lưu trữ tin nhắn bất đồng bộ.
* **expected_key_points:**
  - id: KP8_1
    content: Quản lý kết nối WebSockets phân tán và Redis Pub/Sub
    keypoint_weight: 0.5
    description: Deploy cụm WebSocket Servers sau Load Balancer. Khi User A gửi tin cho User B, Server A đẩy tin lên kênh Redis Pub/Sub của User B; Server B (đang giữ kết nối socket với B) nhận tin từ Redis và đẩy xuống thiết bị User B.
  - id: KP8_2
    content: Lưu trữ tin nhắn bất đồng bộ qua Kafka
    keypoint_weight: 0.5
    description: WebSocket servers đẩy song song tin nhắn vào Kafka -> các Worker tiêu thụ tin nhắn từ Kafka để ghi vào DB lưu trữ lịch sử (Cassandra/ScyllaDB), đảm bảo không ảnh hưởng đến độ trễ truyền tin thời gian thực.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống APIs có tính bảo mật cực cao đáp ứng tiêu chuẩn tài chính quốc tế (như FAPI - Financial-grade API), sử dụng Mutual TLS (mTLS), Token Binding, và mã hóa JWE (JSON Web Encryption).
* **expected_key_points:**
  - id: KP9_1
    content: Mutual TLS (mTLS) và Token Binding
    keypoint_weight: 0.5
    description: Bắt buộc xác thực chứng chỉ từ cả hai phía (client và server) qua mTLS; liên kết Access Token trực tiếp với vân tay chứng chỉ client (token binding) để kẻ trộm token không dùng được nếu thiếu chứng chỉ.
  - id: KP9_2
    content: Mã hóa JWE và Chữ ký JWS
    keypoint_weight: 0.5
    description: Payload API không gửi dạng rõ; mã hóa nội dung bằng JWE sử dụng khóa công khai của client và ký số bằng JWS sử dụng khóa riêng của server để chống nghe lén và giả mạo.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc phân quyền động (Attribute-Based Access Control - ABAC) cho hệ thống ERP lớn phức tạp của tập đoàn, hỗ trợ phân quyền mịn dựa trên thời gian, địa điểm, trạng thái giao dịch và thuộc tính người dùng.
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa chính sách thuộc tính (Attributes)
    keypoint_weight: 0.5
    description: Quyền truy cập quyết định dựa trên sự kết hợp các thuộc tính: User (chức vụ, phòng ban), Resource (loại tài liệu, giá trị giao dịch), và Environment (thời gian làm việc, IP trong/ngoài văn phòng).
  - id: KP10_2
    content: Công cụ thực thi chính sách (Policy Decision Point)
    keypoint_weight: 0.5
    description: Xây dựng công cụ kiểm tra quyền tập trung (PDP); các API Gateway/Microservices (PEP) gửi yêu cầu phân quyền dạng JSON; PDP đánh giá chính sách động và trả về kết quả cho phép/từ chối.

