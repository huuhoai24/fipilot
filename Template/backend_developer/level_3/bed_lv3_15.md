# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 3) - Tập Đề Microservices Security và Zero-Trust (15)

* **Role:** Backend Developer
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Vai trò của Data Plane (Sidecar) và Control Plane trong Service Mesh.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa Service Mesh và Data Plane
    keypoint_weight: 0.5
    description: Service Mesh là lớp hạ tầng chuyên dụng để quản lý giao tiếp giữa các dịch vụ. Data Plane gồm các Sidecar Proxies (như Envoy) chạy kèm ứng dụng để điều hướng toàn bộ traffic đầu vào/ra.
  - id: KP1_2
    content: Vai trò của Control Plane
    keypoint_weight: 0.5
    description: Control Plane (như Istiod) quản lý cấu hình, định tuyến, chính sách bảo mật và phân phối các cấu hình đó xuống các Sidecar Proxies hoạt động ở Data Plane.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Circuit Breaker Pattern và các trạng thái Closed, Open, Half-Open.
* **expected_key_points:**
  - id: KP2_1
    content: Mục tiêu và trạng thái Closed, Open
    keypoint_weight: 0.6
    description: Closed: hoạt động bình thường, cho phép traffic đi qua. Nếu tỷ lệ lỗi vượt ngưỡng, chuyển sang Open: chặn hoàn toàn traffic, trả về lỗi ngay lập tức để bảo vệ hệ thống phía sau.
  - id: KP2_2
    content: Trạng thái Half-Open và phục hồi
    keypoint_weight: 0.4
    description: Sau khoảng chờ cố định, chuyển sang Half-Open: cho phép một lượng nhỏ traffic thử nghiệm đi qua. Nếu thành công -> chuyển về Closed; nếu lỗi tiếp -> quay lại Open.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh gRPC (HTTP/2) và REST (HTTP/1.1) về hiệu năng.
* **expected_key_points:**
  - id: KP3_1
    content: So sánh giao thức và định dạng dữ liệu
    keypoint_weight: 0.5
    description: REST dùng HTTP/1.1 và JSON dạng text (dễ đọc nhưng cồng kềnh). gRPC dùng HTTP/2 (nhị phân, hỗ trợ multiplexing) và Protocol Buffers nén dữ liệu nhỏ gọn.
  - id: KP3_2
    content: Hiệu năng và luồng dữ liệu (Streaming)
    keypoint_weight: 0.5
    description: gRPC cho tốc độ truyền tải nhanh gấp nhiều lần REST, tiết kiệm CPU/băng thông và hỗ trợ streaming hai chiều thực sự, tối ưu cho giao tiếp nội bộ giữa các microservices.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế Service Discovery phân tán dùng Consul cho cụm máy chủ động.
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế Đăng ký dịch vụ (Service Registration)
    keypoint_weight: 0.5
    description: Khi khởi động, instance ứng dụng gửi thông tin (IP, port, health check URL) lên Consul agent. Consul agent liên tục gửi heartbeats để giám sát trạng thái sống của instance.
  - id: KP4_2
    content: Cơ chế Truy xuất dịch vụ (Service Discovery) và DNS
    keypoint_weight: 0.5
    description: Khi Dịch vụ A muốn gọi Dịch vụ B, nó truy vấn danh sách IP hợp lệ của B từ Consul qua DNS/HTTP API; sử dụng client-side load balancing để phân phối request.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** API Gateway Rate Limiting dùng Token Bucket và Redis Lua script.
* **expected_key_points:**
  - id: KP5_1
    content: Nguyên lý thuật toán Token Bucket
    keypoint_weight: 0.5
    description: Thiết lập một xô chứa tối đa $B$ tokens. Định kỳ tự động thêm $R$ tokens vào xô. Mỗi request đi qua phải tiêu thụ 1 token; nếu xô rỗng, request bị từ chối ngay lập tức (Rate Limit).
  - id: KP5_2
    content: Tích hợp Redis phân tán và Lua script
    keypoint_weight: 0.5
    description: Lưu trữ số lượng token hiện tại và nhãn thời gian cập nhật gần nhất trong Redis. Viết Lua script chạy nguyên tử (atomic) để kiểm tra và trừ token, tránh lỗi tranh chấp tài nguyên (race conditions).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Distributed Tracing với OpenTelemetry và HTTP Header Context Propagation.
* **expected_key_points:**
  - id: KP6_1
    content: Khái niệm Traces, Spans và Trace ID
    keypoint_weight: 0.5
    description: Một Trace đại diện cho toàn bộ luồng đi của một request qua các dịch vụ. Mỗi bước xử lý nhỏ trong một dịch vụ là một Span. Tất cả các Spans chung một Trace ID duy nhất.
  - id: KP6_2
    content: Cơ chế Context Propagation (Truyền ngữ cảnh)
    keypoint_weight: 0.5
    description: Khi Dịch vụ A gọi Dịch vụ B qua HTTP/gRPC, A chèn Trace ID và Parent Span ID vào HTTP Headers (W3C Trace Context). B đọc headers này để dựng tiếp Span con, tạo mối liên kết cha-con liền mạch trên cây phân tích lỗi.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh Blocking và Non-blocking API Gateway về hiệu năng xử lý.
* **expected_key_points:**
  - id: KP7_1
    content: Kiến trúc luồng xử lý Blocking vs Non-blocking
    keypoint_weight: 0.6
    description: Zuul 1 sử dụng mô hình Thread-per-request (mỗi request chiếm 1 thread riêng, bị block khi đợi I/O). Kong/Spring Cloud Gateway sử dụng Event Loop non-blocking (1 thread xử lý hàng ngàn kết nối không đồng bộ qua epoll/kqueue).
  - id: KP7_2
    content: Hiệu năng khi chịu tải cao
    keypoint_weight: 0.4
    description: Non-blocking API Gateway tiết kiệm bộ nhớ RAM và CPU cực tốt khi có hàng vạn kết nối đồng thời (high concurrency), tránh hiện tượng cạn kiệt thread pool.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giao dịch phân tán quy mô lớn dùng Saga kết hợp Outbox pattern.
* **expected_key_points:**
  - id: KP8_1
    content: Kết hợp Saga và Outbox Pattern
    keypoint_weight: 0.5
    description: Mỗi dịch vụ tham gia Saga ghi nhận trạng thái giao dịch cục bộ và ghi sự kiện vào Outbox Table trong cùng một transaction DB. Tiến trình CDC đẩy sự kiện này sang Kafka để kích hoạt dịch vụ tiếp theo bất đồng bộ.
  - id: KP8_2
    content: Cơ chế bù trừ (Compensation) tự động khi có lỗi
    keypoint_weight: 0.5
    description: Khi nhận sự kiện lỗi từ Kafka, Orchestrator tự động kích hoạt chuỗi sự kiện bù trừ (compensating events) theo thứ tự ngược lại để hoàn trả trạng thái nhất quán, giảm thiểu việc dùng khóa chặn tài nguyên.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Bảo mật Zero-Trust trong Kubernetes dùng mTLS, SPIFFE/SPIRE và OPA.
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế mTLS và Định danh SPIFFE/SPIRE
    keypoint_weight: 0.5
    description: Sử dụng SPIRE cấp phát tự động chứng chỉ X.509 ngắn hạn gắn với định danh bảo mật (SPIFFE ID) cho từng Pod. Sidecar proxy dùng chứng chỉ này để mã hóa giao tiếp và xác thực hai chiều mTLS.
  - id: KP9_2
    content: Kiểm soát truy cập động bằng OPA (Open Policy Agent)
    keypoint_weight: 0.5
    description: Sidecar gửi request tới OPA sidecar để kiểm tra quyền truy cập dựa trên chính sách viết bằng ngôn ngữ Rego (ví dụ: Service A chỉ được gọi API GET của Service B tại một số endpoint nhất định).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Triển khai phiên bản mới không downtime (Canary/Blue-Green) tự động qua Service Mesh.
* **expected_key_points:**
  - id: KP10_1
    content: Điều phối Traffic động bằng Istio VirtualService
    keypoint_weight: 0.5
    description: Cấu hình VirtualService của Istio để chia tỷ lệ traffic nhỏ (ví dụ 5%) sang phiên bản mới (Canary) và 95% chạy phiên bản cũ (Production).
  - id: KP10_2
    content: Tự động phân tích chỉ số và Rollback (Prometheus Metrics)
    keypoint_weight: 0.5
    description: Sử dụng Argo Rollouts giám sát các chỉ số thời gian thực từ Prometheus (tỷ lệ lỗi HTTP 5xx, latency p99). Nếu các chỉ số vượt ngưỡng an toàn, tự động rollback 100% traffic về bản cũ tức thời.

