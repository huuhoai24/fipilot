# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 5) - Tập Đề Observability và Prometheus Alerting (9)

* **Role:** Backend Developer
* **Level:** Level 5
* **Experience:** Trên 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích khái niệm Observability (Tính giám sát được) của hệ thống phần mềm Backend. Phân biệt ba trụ cột chính: Metrics, Logs, và Traces.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa Observability
    keypoint_weight: 0.4
    description: Là khả năng đo lường và suy luận các trạng thái hoạt động bên trong của một hệ thống dựa trên dữ liệu đầu ra mà nó cung cấp.
  - id: KP1_2
    content: Ba trụ cột: Metrics, Logs, Traces
    keypoint_weight: 0.6
    description: Metrics: số liệu thống kê định lượng theo thời gian (CPU, RPS, error rate). Logs: nhật ký chi tiết các sự kiện xảy ra có mốc thời gian. Traces: dòng chảy vòng đời của một request qua toàn bộ các hệ thống.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích nguyên lý hoạt động và mô hình thu thập dữ liệu giám sát của Prometheus. Phân biệt cơ chế Pull-based và Push-based.
* **expected_key_points:**
  - id: KP2_1
    content: Mô hình Pull-based của Prometheus
    keypoint_weight: 0.5
    description: Prometheus định kỳ chủ động gọi HTTP GET tới endpoint `/metrics` của các ứng dụng (targets) để lấy dữ liệu, giúp ứng dụng nhẹ tải hơn và dễ quản lý tập trung.
  - id: KP2_2
    content: Mô hình Push-based và Pushgateway
    keypoint_weight: 0.5
    description: Các tác vụ chạy ngắn hạn (short-lived/cronjobs) không thể đợi pull sẽ chủ động đẩy metrics lên Prometheus Pushgateway; Prometheus sẽ pull dữ liệu từ Pushgateway này.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau về bản chất toán học và kịch bản sử dụng giữa bốn loại metrics cơ bản trong Prometheus: Counter, Gauge, Histogram, và Summary.
* **expected_key_points:**
  - id: KP3_1
    content: Đặc trưng Counter và Gauge
    keypoint_weight: 0.5
    description: Counter là biến chỉ tăng (hoặc reset về 0), dùng đếm số request, số lỗi. Gauge là biến có thể tăng/giảm tự do, dùng đo nhiệt độ, dung lượng RAM, số kết nối hoạt động.
  - id: KP3_2
    content: Đặc trưng Histogram và Summary
    keypoint_weight: 0.5
    description: Histogram chia khoảng (buckets) để tính toán phân phối thời gian xử lý (latency) phía server. Summary tính toán trực tiếp các điểm phân vị (quantiles) ngay tại phía client ứng dụng.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế hệ thống cảnh báo tự động (Alerting System) thông minh kết hợp Prometheus, Alertmanager để gửi cảnh báo lỗi qua Slack/PagerDuty, giảm thiểu hiện tượng nhiễu cảnh báo (Alert Fatigue).
* **expected_key_points:**
  - id: KP4_1
    content: Cấu hình Alerting Rules trong Prometheus
    keypoint_weight: 0.5
    description: Viết các câu lệnh PromQL để cảnh báo (ví dụ: tỷ lệ lỗi HTTP 5xx > 1% trong 5 phút); thiết lập độ ưu tiên của cảnh báo (severity: warning, critical).
  - id: KP4_2
    content: Tính năng Grouping, Inhibition, và Silencing
    keypoint_weight: 0.5
    description: Sử dụng Alertmanager gộp các cảnh báo liên quan vào 1 tin nhắn (Grouping); tắt cảnh báo phụ nếu cảnh báo chính đã kích hoạt (Inhibition); thiết lập khoảng tắt tạm thời khi đang bảo trì hệ thống (Silencing).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế dashboard Grafana giám sát hiệu năng tổng thể của ứng dụng Backend dựa trên phương pháp 4 Tín Hiệu Vàng (Four Golden Signals).
* **expected_key_points:**
  - id: KP5_1
    content: Định nghĩa 4 Tín Hiệu Vàng
    keypoint_weight: 0.6
    description: Latency (thời gian xử lý request). Traffic (băng thông/số lượng request rps). Errors (tỷ lệ request bị lỗi). Saturation (mức độ đầy của tài nguyên: CPU, bộ đệm, memory pool).
  - id: KP5_2
    content: Biểu diễn trực quan trên Grafana
    keypoint_weight: 0.4
    description: Vẽ các đồ thị đường (time-series) cho Latency p95/p99; đồ thị cột cho RPS; đồ thị tỷ lệ phần trăm cho Errors; thiết lập cảnh báo màu sắc khi Saturation vượt 85%.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích cơ chế hoạt động của Giám sát phân tán (Distributed Tracing) trong môi trường xử lý không đồng bộ (Asynchronous/Event-driven) sử dụng Kafka và các workers xử lý chạy ngầm.
* **expected_key_points:**
  - id: KP6_1
    content: Trích xuất và Chèn Trace Context qua Kafka Header
    keypoint_weight: 0.6
    description: Khi gửi tin nhắn vào Kafka, Producer chèn Traceparent (chứa Trace ID, Span ID) vào Kafka Record Headers. Worker khi đọc tin từ Kafka trích xuất header này để tiếp tục vẽ Span con.
  - id: KP6_2
    content: Theo dõi luồng không đồng bộ hoàn chỉnh
    keypoint_weight: 0.4
    description: Dựng sơ đồ thể hiện rõ khoảng thời gian tin nhắn nằm trong Kafka queue và khoảng thời gian thực tế worker xử lý, hỗ trợ phát hiện nghẽn worker.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh hiệu năng, tính mở rộng và độ phức tạp lưu trữ dữ liệu giám sát khi triển khai OpenTelemetry Collector chạy dạng Agent (DaemonSet) so với chạy dạng Gateway tập trung.
* **expected_key_points:**
  - id: KP7_1
    content: Triển khai dạng Agent (DaemonSet)
    keypoint_weight: 0.5
    description: Mỗi node K8s chạy 1 collector agent. Ứng dụng đẩy metrics/traces local qua gRPC/localhost (trễ thấp nhất), giảm tải xử lý cho ứng dụng nhưng khó scale độc lập.
  - id: KP7_2
    content: Triển khai dạng Gateway tập trung
    keypoint_weight: 0.5
    description: Chạy cụm Collectors tập trung sau load balancer. Dễ dàng quản lý cấu hình nén, lọc dữ liệu (filtering) và scale out dựa trên tải lượng, nhưng tăng độ trễ mạng khi gửi metrics.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống giám sát và chuẩn đoán sự cố thời gian thực cho hệ thống microservices quy mô 500+ dịch vụ chạy trên Kubernetes, đảm bảo tự động phát hiện nút thắt cổ chai và truy vết nguyên nhân lỗi trong vòng 1 phút.
* **expected_key_points:**
  - id: KP8_1
    content: Tự động phát hiện bất thường (Anomaly Detection)
    keypoint_weight: 0.5
    description: Sử dụng Prometheus kết hợp thuật toán dự báo (như Holt-Winters) để tự động phát hiện các đột biến RPS hoặc latency bất thường so với lịch sử mà không cần cài ngưỡng cứng (static thresholds).
  - id: KP8_2
    content: Tương quan dữ liệu tự động (Telemetry Correlation)
    keypoint_weight: 0.5
    description: Tích hợp Trace ID vào cấu trúc log (Log Correlation). Khi phát hiện Alert lỗi -> tự động trích xuất Trace ID lỗi -> liên kết sang sơ đồ Distributed Tracing để chỉ ra chính xác dòng code/dịch vụ bị sập chỉ dưới 1 phút.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp lưu trữ metrics phân tán dài hạn chịu tải ghi cực cao sử dụng Prometheus kết hợp Thanos hoặc Cortex để phục vụ phân tích dữ liệu lịch sử nhiều năm.
* **expected_key_points:**
  - id: KP9_1
    content: Kiến trúc Thanos (Sidecar và Store Gateway)
    keypoint_weight: 0.5
    description: Thanos Sidecar đẩy các khối dữ liệu cũ (blocks) của Prometheus lên Object Storage (S3/GCS) định kỳ. Thanos Store Gateway hỗ trợ truy vấn dữ liệu lịch sử trực tiếp từ Object Storage thông qua Thanos Query.
  - id: KP9_2
    content: Nén và Giảm độ phân giải dữ liệu (Compaction & Downsampling)
    keypoint_weight: 0.5
    description: Sử dụng Thanos Compactor chạy nền để gộp các block nhỏ thành block lớn và giảm độ phân giải dữ liệu lịch sử (ví dụ: giữ trung bình 5 phút thay vì từng giây cho dữ liệu thọ > 1 tháng) giúp tiết kiệm đĩa cứng và tăng tốc độ vẽ đồ thị.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc thu thập logs phân tán an toàn và bảo mật cho ngân hàng số, tự động phát hiện và ẩn danh dữ liệu nhạy cảm (PII masking) ngay tại log shipper trước khi đẩy về kho logs tập trung.
* **expected_key_points:**
  - id: KP10_1
    content: Lọc và Ẩn danh tại nguồn (PII Masking)
    keypoint_weight: 0.6
    description: Cấu hình Log Shipper (Fluent Bit/Vector) sử dụng biểu thức chính quy (Regex) quét qua các trường log thô để phát hiện các mẫu PII nhạy cảm (số thẻ tín dụng, số điện thoại, mật khẩu) -> thay thế bằng mã băm hoặc dấu hoa thị `****` trước khi gửi đi.
  - id: KP10_2
    content: Mã hóa log và Phân quyền truy cập
    keypoint_weight: 0.4
    description: Mã hóa toàn bộ log trên đường truyền (TLS); thiết lập phân quyền kiểm soát truy cập (RBAC) trên Kibana/Elasticsearch, đảm bảo chỉ có các quản trị viên bảo mật được cấp quyền mới có thể xem log gốc giải mã.

