# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2) - Tập Đề WebSockets và Real-time (17)

* **Role:** Backend Developer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** WebSockets là gì? So sánh sự khác nhau về cơ chế kết nối giữa WebSockets và HTTP Short Polling truyền thống.
* **expected_key_points:**
  - id: KP1_1
    content: Bản chất giao thức WebSockets
    keypoint_weight: 0.5
    description: WebSockets thiết lập một kết nối TCP song phương (full-duplex) liên tục, cho phép cả client và server chủ động truyền dữ liệu cho nhau qua 1 cổng kết nối duy nhất.
  - id: KP1_2
    content: So sánh với HTTP Short Polling
    keypoint_weight: 0.5
    description: HTTP Short Polling yêu cầu client liên tục gửi request HTTP sau mỗi khoảng thời gian ngắn để hỏi dữ liệu mới, gây lãng phí băng thông và độ trễ cao.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích cơ chế bắt tay (Handshake) để nâng cấp từ giao thức HTTP lên WebSockets.
* **expected_key_points:**
  - id: KP2_1
    content: HTTP Upgrade Request
    keypoint_weight: 0.6
    description: Client gửi request HTTP GET thông thường kèm theo tiêu đề đặc biệt: `Connection: Upgrade` và `Upgrade: websocket` để yêu cầu nâng cấp giao thức.
  - id: KP2_2
    content: Xác nhận từ Server (101 Switching Protocols)
    keypoint_weight: 0.4
    description: Server chấp nhận nâng cấp sẽ trả về mã phản hồi `101 Switching Protocols` kèm theo khóa mã hóa bắt tay được đồng ý; sau đó kết nối TCP được giữ lại cho WebSockets.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày cách sử dụng cơ chế Heartbeat (Ping/Pong) để duy trì và kiểm tra trạng thái kết nối WebSockets giữa Client và Server.
* **expected_key_points:**
  - id: KP3_1
    content: Mục đích của Ping/Pong
    keypoint_weight: 0.5
    description: Để phát hiện và đóng các kết nối 'chết' (zombie connections) do rớt mạng đột ngột mà trình duyệt hoặc server không kịp gửi gói tin đóng kết nối thông thường.
  - id: KP3_2
    content: Luồng hoạt động định kỳ
    keypoint_weight: 0.5
    description: Server định kỳ gửi gói tin `Ping` tới client; client nhận được bắt buộc phải gửi lại gói tin `Pong`. Nếu quá thời gian timeout server không nhận được `Pong` -> tự động hủy kết nối.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh sự khác nhau về hiệu năng, hướng truyền dữ liệu và kịch bản áp dụng giữa hai giải pháp thời gian thực: WebSockets và Server-Sent Events (SSE).
* **expected_key_points:**
  - id: KP4_1
    content: Bản chất WebSockets vs SSE
    keypoint_weight: 0.5
    description: WebSockets hỗ trợ truyền dữ liệu hai chiều thực sự (bi-directional). SSE thiết lập kết nối một chiều duy nhất từ Server đẩy về Client (unidirectional) chạy trên nền HTTP tiêu chuẩn.
  - id: KP4_2
    content: Kịch bản lựa chọn áp dụng
    keypoint_weight: 0.5
    description: Dùng WebSockets cho ứng dụng chat, game online (cần gửi dữ liệu liên tục từ cả hai phía). Dùng SSE cho bảng giá chứng khoán, tin tức, dashboard theo dõi (chỉ cần đẩy từ server).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Làm thế nào để xử lý xác thực người dùng (Authentication) an toàn khi thiết lập kết nối WebSockets?
* **expected_key_points:**
  - id: KP5_1
    content: Vấn đề headers trong handshake
    keypoint_weight: 0.5
    description: Giao thức WebSockets của trình duyệt không cho phép gửi custom headers (như `Authorization`) trong HTTP handshake ban đầu. Không nên truyền token rõ qua URL query string.
  - id: KP5_2
    content: Giải pháp xác thực qua tin nhắn đầu tiên hoặc cookie
    keypoint_weight: 0.5
    description: Cho phép thiết lập kết nối thô -> client bắt buộc gửi tin nhắn JSON chứa token xác thực đầu tiên trong vòng 5 giây; server kiểm tra token hợp lệ thì giữ kết nối, ngược lại ngắt kết nối.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Làm thế nào để scale ngang (scale out) cụm WebSocket Servers chạy sau Load Balancer? Giải quyết vấn đề chia sẻ trạng thái kết nối ra sao?
* **expected_key_points:**
  - id: KP6_1
    content: Nguy cơ mất kết nối khi scale ngang
    keypoint_weight: 0.5
    description: Nếu user A kết nối tới Server 1 và user B kết nối tới Server 2; Server 1 không thể tự gửi tin trực tiếp tới user B vì socket của B nằm trên RAM của Server 2.
  - id: KP6_2
    content: Giải pháp sử dụng Redis Pub/Sub
    keypoint_weight: 0.5
    description: Sử dụng Redis làm kênh Pub/Sub dùng chung; khi muốn gửi tin tới user B, Server 1 đẩy tin lên kênh Redis; Server 2 lắng nghe kênh và đẩy xuống socket thực tế của user B.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách sử dụng thư viện Socket.io trong Node.js. Socket.io giải quyết vấn đề gì khi trình duyệt cũ không hỗ trợ WebSockets?
* **expected_key_points:**
  - id: KP7_1
    content: Cơ chế tự động chuyển đổi giao thức (Fallback)
    keypoint_weight: 0.6
    description: Socket.io tự động thăm dò kết nối; nếu trình duyệt không hỗ trợ WebSockets, nó tự động hạ cấp xuống dùng HTTP Long Polling để duy trì tính năng thời gian thực.
  - id: KP7_2
    content: Tính năng quản lý phòng (Rooms) và phát tin (Broadcasting)
    keypoint_weight: 0.4
    description: Cung cấp các API tiện lợi sẵn có để quản lý chia nhóm người dùng theo phòng chat (`socket.join('room-name')`) và phát tin hàng loạt (`io.to(...).emit(...)`).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống Chat nhóm thời gian thực hỗ trợ 100,000 kết nối đồng thời, đảm bảo tin nhắn được lưu trữ lịch sử bất đồng bộ vào cơ sở dữ liệu và không làm trễ tốc độ truyền tin tức thời.
* **expected_key_points:**
  - id: KP8_1
    content: Thiết kế luồng truyền tin tức thời
    keypoint_weight: 0.5
    description: Sử dụng cụm WebSocket Servers định tuyến tin nhắn siêu nhanh qua bộ đệm Redis Pub/Sub để phát trực tiếp cho các thành viên trong nhóm đang online dưới 50ms.
  - id: KP8_2
    content: Lưu trữ lịch sử tin nhắn bất đồng bộ qua Queue
    keypoint_weight: 0.5
    description: WebSocket Server đẩy tin nhắn song song vào hàng đợi (RabbitMQ/Kafka) -> worker tiêu thụ hàng đợi để lưu vào DB (MongoDB/Cassandra) chạy ngầm, tránh làm chậm luồng socket.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp quản lý vòng đời kết nối WebSockets (Connection Lifecycle) trên API Gateway hỗ trợ kiểm soát kết nối zombie, giới hạn số lượng kết nối tối đa trên mỗi tài khoản người dùng.
* **expected_key_points:**
  - id: KP9_1
    content: Giới hạn kết nối tối đa trên mỗi tài khoản
    keypoint_weight: 0.5
    description: Mỗi khi thiết lập kết nối, tăng biến đếm số lượng socket của user trong Redis bằng lệnh nguyên tử; nếu vượt quá giới hạn (ví dụ 3 kết nối đồng thời) -> từ chối kết nối mới.
  - id: KP9_2
    content: Dọn dẹp kết nối zombie và cập nhật biến đếm
    keypoint_weight: 0.5
    description: Định kỳ gửi Ping; nếu mất kết nối -> đóng socket -> giảm biến đếm tương ứng trong Redis, đảm bảo giải phóng bộ nhớ RAM cho Gateway.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống hiển thị tọa độ xe giao hàng thời gian thực (Real-time Live Tracking) cho 20,000 shipper di chuyển liên tục trên bản đồ cho khách hàng theo dõi dưới 1 giây.
* **expected_key_points:**
  - id: KP10_1
    content: Sử dụng Redis Geospatial dữ liệu tọa độ
    keypoint_weight: 0.5
    description: Shipper gửi tọa độ qua WebSockets thô -> ghi đè tọa độ nhanh vào bộ nhớ Redis sử dụng lệnh `GEOADD` để lưu trữ dữ liệu vị trí địa lý của shipper.
  - id: KP10_2
    content: Phát tọa độ cục bộ cho khách hàng liên quan
    keypoint_weight: 0.5
    description: Khách hàng đăng ký lắng nghe tọa độ theo ID đơn hàng; backend sử dụng Redis Pub/Sub định tuyến tọa độ shipper tới đúng phòng socket của khách hàng đang mở bản đồ.

