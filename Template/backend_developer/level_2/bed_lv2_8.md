# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2) - Tập Đề Microservices Basics (8)

* **Role:** Backend Developer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Phân tích ưu điểm và nhược điểm của kiến trúc nguyên khối (Monolith Architecture) so với kiến trúc vi dịch vụ (Microservices Architecture).
* **expected_key_points:**
  - id: KP1_1
    content: Ưu nhược điểm Monolith Architecture
    keypoint_weight: 0.5
    description: Ưu điểm: Dễ phát triển ban đầu, triển khai đơn giản, gọi hàm nội bộ hiệu năng cao. Nhược điểm: Khó scale độc lập từng phần khi app phình to, một lỗi nhỏ có thể làm sập toàn bộ hệ thống.
  - id: KP1_2
    content: Ưu nhược điểm Microservices Architecture
    keypoint_weight: 0.5
    description: Ưu điểm: Dễ scale độc lập, sử dụng công nghệ linh hoạt cho từng dịch vụ, đội ngũ phát triển chạy song song dễ hơn. Nhược điểm: Hệ thống phân tán phức tạp, khó debug, overhead truyền tải mạng lớn.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** API Gateway đóng vai trò gì trong kiến trúc Microservices? Chỉ ra các lợi ích chính của nó đối với các ứng dụng Client.
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm API Gateway
    keypoint_weight: 0.5
    description: Là cổng truy cập duy nhất (Single Entry Point) đứng trước hệ thống Microservices, nhận toàn bộ request từ Client và định tuyến chúng đến đúng dịch vụ tương ứng.
  - id: KP2_2
    content: Lợi ích đối với Client
    keypoint_weight: 0.5
    description: Che giấu sự phức tạp của hệ thống backend; cho phép gộp request; thực hiện xác thực (authentication), ghi log và giới hạn tần suất gọi (rate limiting) tập trung.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích khái niệm Service Discovery (Phát hiện dịch vụ). Tại sao nó là thành phần bắt buộc trong môi trường Cloud/Microservices động?
* **expected_key_points:**
  - id: KP3_1
    content: Khái niệm Service Discovery
    keypoint_weight: 0.5
    description: Là cơ chế tự động theo dõi, đăng ký và tra cứu địa chỉ IP/Port của các instances dịch vụ đang hoạt động trong hệ thống phân tán (ví dụ dùng Consul, Eureka).
  - id: KP3_2
    content: Lý do bắt buộc trong môi trường động
    keypoint_weight: 0.5
    description: Trong môi trường Cloud/Kubernetes, các instances dịch vụ liên tục được khởi tạo hoặc hủy đi làm IP thay đổi liên tục; Service Discovery giúp các dịch vụ tự động tìm thấy nhau không cần hardcode IP.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh sự khác nhau về giao thức truyền thông, hiệu năng và kịch bản sử dụng giữa hai phương thức giao tiếp Microservices: REST (HTTP/1.1) và gRPC (HTTP/2).
* **expected_key_points:**
  - id: KP4_1
    content: Bản chất giao thức và định dạng dữ liệu
    keypoint_weight: 0.5
    description: REST dùng HTTP/1.1 và JSON dạng text (dễ đọc nhưng dung lượng lớn). gRPC dùng HTTP/2 (nhị phân, hỗ trợ multiplexing) và Protocol Buffers nén dữ liệu cực kỳ nhỏ gọn.
  - id: KP4_2
    content: Hiệu năng và kịch bản áp dụng
    keypoint_weight: 0.5
    description: gRPC cho tốc độ truyền tải nhanh gấp nhiều lần REST, tiết kiệm CPU/băng thông và hỗ trợ streaming hai chiều, tối ưu cho giao tiếp nội bộ (Internal) giữa các microservices.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế hoạt động của mẫu thiết kế Circuit Breaker trong Microservices. Tại sao nó giúp ngăn chặn lỗi dây chuyền (Cascading Failures)?
* **expected_key_points:**
  - id: KP5_1
    content: Ba trạng thái của Circuit Breaker
    keypoint_weight: 0.6
    description: Closed: hoạt động bình thường. Open: tỷ lệ lỗi gọi dịch vụ khác vượt ngưỡng, ngắt kết nối lập tức, trả lỗi nhanh bảo vệ hệ thống. Half-Open: gửi thử 1 vài request kiểm tra xem dịch vụ đích phục hồi chưa.
  - id: KP5_2
    content: Ngăn chặn lỗi dây chuyền
    keypoint_weight: 0.4
    description: Ngăn không cho một dịch vụ bị treo (do đợi phản hồi từ dịch vụ lỗi) làm cạn kiệt luồng (thread pool) của chính nó và lan truyền lỗi ra toàn hệ thống.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Làm thế nào để quản lý các cấu hình hệ thống (như database credentials, API keys) một cách tập trung và an toàn trong môi trường Microservices?
* **expected_key_points:**
  - id: KP6_1
    content: Sử dụng Config Server tập trung
    keypoint_weight: 0.5
    description: Sử dụng các công cụ quản lý cấu hình tập trung như Spring Cloud Config, Consul, etcd để quản lý và phân phối cấu hình động cho các dịch vụ khi khởi động.
  - id: KP6_2
    content: Quản lý bảo mật thông tin nhạy cảm (Secrets)
    keypoint_weight: 0.5
    description: Sử dụng HashiCorp Vault, AWS Secrets Manager hoặc Kubernetes Secrets để mã hóa và lưu trữ an toàn các mật khẩu, API keys; không lưu file cấu hình rõ vào Git.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm Database-per-Service trong Microservices. Thách thức lớn nhất khi áp dụng mẫu thiết kế này là gì?
* **expected_key_points:**
  - id: KP7_1
    content: Đặc trưng Database-per-Service
    keypoint_weight: 0.5
    description: Mỗi microservice sở hữu cơ sở dữ liệu riêng biệt của nó; các dịch vụ khác không được phép truy cập trực tiếp DB này mà phải gọi qua API.
  - id: KP7_2
    content: Thách thức về giao dịch và báo cáo
    keypoint_weight: 0.5
    description: Khó đảm bảo tính toàn vẹn giao dịch trên nhiều DB (giao dịch phân tán); việc viết các báo cáo liên bảng (cross-database queries) trở nên rất phức tạp.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp giao dịch phân tán sử dụng Saga Pattern theo mô hình Điều phối trung tâm (Orchestration-based Saga) cho luồng đặt hàng thanh toán của ứng dụng thương mại điện tử.
* **expected_key_points:**
  - id: KP8_1
    content: Vai trò của Saga Orchestrator
    keypoint_weight: 0.5
    description: Thiết lập một dịch vụ trung tâm (Order Orchestrator) quản lý trạng thái máy (State Machine); định kỳ gửi lệnh thực thi giao dịch cục bộ đến dịch vụ Payment, Inventory.
  - id: KP8_2
    content: Thiết kế giao dịch bù trừ (Compensating Transactions)
    keypoint_weight: 0.5
    description: Nếu bước trừ tiền thành công nhưng bước trừ kho lỗi, Orchestrator tự động gọi API hoàn tiền (Refund Payment) để đưa hệ thống về trạng thái nhất quán nhất thời.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp giám sát lỗi phân tán (Distributed Tracing) sử dụng OpenTelemetry để truy vết nguyên nhân gây trễ (high latency) của một request đi qua 5 microservices.
* **expected_key_points:**
  - id: KP9_1
    content: Truyền ngữ cảnh Trace Context (Propagation)
    keypoint_weight: 0.5
    description: Khi dịch vụ A gọi dịch vụ B, A tự động chèn Trace ID và Span ID hiện tại vào tiêu đề (HTTP Headers/gRPC Metadata). Dịch vụ B đọc tiêu đề này để dựng tiếp Span con liên tục.
  - id: KP9_2
    content: Gửi và trực quan hóa dữ liệu Trace
    keypoint_weight: 0.5
    description: Các microservices gửi bất đồng bộ dữ liệu trace về bộ thu thập (Collector) để đẩy sang Jaeger/Zipkin vẽ biểu đồ dạng cây, giúp xác định chính xác dịch vụ/câu query DB gây trễ.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc API Gateway phân tán hỗ trợ Dynamic Routing (Định tuyến động) và Hot-Reload cấu hình định tuyến (không cần khởi động lại Gateway) sử dụng Kong Gateway hoặc Spring Cloud Gateway.
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế định tuyến động
    keypoint_weight: 0.5
    description: Định nghĩa bảng định tuyến (Route Map) lưu trữ trong cơ sở dữ liệu hoặc KV store phân tán (etcd/Consul); Gateway định kỳ đọc hoặc lắng nghe sự thay đổi của bảng này.
  - id: KP10_2
    content: Hot-Reload không downtime
    keypoint_weight: 0.5
    description: Sử dụng tính năng Reactive của Gateway để nạp lại cấu hình định tuyến trực tiếp vào bộ nhớ RAM khi nhận sự kiện webhook thay đổi từ Git/DB mà không làm đứt kết nối hiện tại của khách hàng.

