# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 3) - Tập Đề Disaster Recovery và Multi-Region active-active (7)

* **Role:** Backend Developer
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích ý nghĩa của các khái niệm SLA, SLO, và SLI trong vận hành hệ thống. Hãy tính toán thời gian ngừng hoạt động tối đa cho phép mỗi năm của một hệ thống cam kết SLA độ sẵn sàng 99.99%.
* **expected_key_points:**
  - id: KP1_1
    content: Khái niệm SLA, SLO, SLI
    keypoint_weight: 0.6
    description: SLI (Service Level Indicator) là chỉ số đo lường hiệu năng thực tế (ví dụ: tỷ lệ thành công). SLO (Service Level Objective) là mục tiêu cam kết nội bộ. SLA (Service Level Agreement) là cam kết pháp lý/hợp đồng với khách hàng kèm mức phạt tài chính nếu vi phạm.
  - id: KP1_2
    content: Tính toán thời gian downtime cho SLA 99.99%
    keypoint_weight: 0.4
    description: Thời gian downtime tối đa cho phép mỗi năm là: $365 \times 24 \times 60 \times (1 - 0.9999) \approx 52.56$ phút/năm.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh hai chỉ số quan trọng trong kịch bản Khôi phục sau thảm họa (Disaster Recovery): RTO (Recovery Time Objective) và RPO (Recovery Point Objective). Nêu một ví dụ thực tế.
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa RTO và RPO
    keypoint_weight: 0.6
    description: RTO là khoảng thời gian tối đa hệ thống được phép ngừng hoạt động kể từ khi xảy ra sự cố cho đến khi khôi phục xong. RPO là lượng dữ liệu tối đa được phép bị mất mát tính theo khoảng thời gian kể từ lần sao lưu gần nhất.
  - id: KP2_2
    content: Ví dụ thực tế phù hợp
    keypoint_weight: 0.4
    description: Nêu được ví dụ cụ thể, ví dụ: hệ thống ngân hàng yêu cầu RPO gần bằng 0 (không được mất giao dịch nào) và RTO < 10 phút.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa ba phương pháp sao lưu dữ liệu: Full Backup, Incremental Backup, và Differential Backup về dung lượng lưu trữ và thời gian khôi phục.
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế hoạt động của ba phương pháp
    keypoint_weight: 0.6
    description: Full Backup sao lưu toàn bộ dữ liệu. Incremental chỉ sao lưu phần thay đổi so với lần backup gần nhất. Differential sao lưu phần thay đổi so với lần Full Backup gần nhất.
  - id: KP3_2
    content: So sánh Dung lượng và Thời gian khôi phục
    keypoint_weight: 0.4
    description: Incremental tiết kiệm đĩa nhất nhưng thời gian khôi phục lâu nhất (phải khôi phục tuần tự từng bản cập nhật). Differential có dung lượng lớn hơn Incremental nhưng khôi phục nhanh hơn (chỉ cần bản Full và bản Differential gần nhất).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế kiến trúc triển khai hệ thống (Deployment Architecture) đa vùng theo mô hình Active-Passive kết hợp cơ chế DNS Failover tự động sử dụng Route 53.
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế giám sát sức khỏe (Health Check)
    keypoint_weight: 0.5
    description: Route 53 liên tục gửi các request kiểm tra sức khỏe tới endpoint của vùng Active; nếu phát hiện lỗi liên tiếp vượt quá số lần cấu hình, tự động đánh dấu vùng Active là unhealthy.
  - id: KP4_2
    content: Định tuyến lại traffic sang vùng Passive
    keypoint_weight: 0.5
    description: Tự động cập nhật bản ghi DNS trỏ IP sang vùng Passive; kích hoạt cơ chế kích hoạt cơ sở dữ liệu Passive (failover database) lên làm Read-Write chính.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế giải pháp phân phối tải toàn cầu (Global Server Load Balancing - GSLB) để điều hướng người dùng tới Datacenter gần nhất dựa trên độ trễ mạng thực tế.
* **expected_key_points:**
  - id: KP5_1
    content: DNS-based GSLB và Anycast IP
    keypoint_weight: 0.5
    description: Sử dụng công nghệ định tuyến Anycast IP để phát quảng bá một IP duy nhất từ nhiều địa điểm; mạng internet tự động dẫn hướng gói tin của user tới node mạng gần nhất về mặt địa lý.
  - id: KP5_2
    content: Đo lường Latency động
    keypoint_weight: 0.5
    description: GSLB đo độ trễ mạng (RTT) từ client tới các datacenters cục bộ và cập nhật bảng định tuyến động để đảm bảo độ trễ truy cập của người dùng luôn thấp nhất.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích cơ chế hoạt động của Circuit Breaker ở cấp độ mạng sử dụng các nhà cung cấp CDN (như Cloudflare) để bảo vệ hệ thống trước sự cố sập server gốc.
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế bảo vệ của CDN (Origin Shield)
    keypoint_weight: 0.5
    description: CDN đóng vai trò làm lớp đệm; khi server gốc bị sập (trả về 502/504), CDN tự động kích hoạt Circuit Breaker cấp mạng để từ chối các request mới hoặc phục vụ trang tĩnh tạm thời.
  - id: KP6_2
    content: Stale-While-Revalidate và Cache phục vụ lỗi
    keypoint_weight: 0.5
    description: Cấu hình CDN trả về dữ liệu cache cũ (stale cache) cho người dùng thay vị báo lỗi khi server gốc không phản hồi, duy trì trải nghiệm đọc tối thiểu của user.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh ưu nhược điểm của việc sử dụng Database Replication đồng bộ (Synchronous) và bất đồng bộ (Asynchronous) từ góc độ hiệu năng ghi dữ liệu và tính nhất quán khi xảy ra thảm họa.
* **expected_key_points:**
  - id: KP7_1
    content: Đồng bộ hóa đồng bộ (Synchronous)
    keypoint_weight: 0.5
    description: Đảm bảo ghi thành công lên cả master và replica trước khi trả về client. Không mất dữ liệu khi xảy ra sự cố (RPO = 0) nhưng độ trễ ghi rất lớn, phụ thuộc vào tốc độ mạng giữa hai node.
  - id: KP7_2
    content: Đồng bộ hóa bất đồng bộ (Asynchronous)
    keypoint_weight: 0.5
    description: Ghi xong master là trả về client luôn; dữ liệu đồng bộ ngầm. Hiệu năng ghi cực nhanh nhưng có rủi ro mất dữ liệu chưa kịp truyền đi khi master sập đột ngột (RPO > 0).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống phục vụ thanh toán trực tuyến đa quốc gia hoạt động theo mô hình Active-Active song song tại 3 vùng địa lý (Mỹ, Châu Âu, Châu Á), đảm bảo không xảy ra xung đột dữ liệu và độ trễ giao dịch < 200ms.
* **expected_key_points:**
  - id: KP8_1
    content: Thiết kế Data Layer phân tán và CRDTs
    keypoint_weight: 0.5
    description: Không dùng database quan hệ tập trung. Sử dụng cơ sở dữ liệu phân tán hỗ trợ multi-master (như CockroachDB hoặc Cassandra) kết hợp thuật toán đồng thuận Raft cục bộ; lưu số dư tài khoản dạng chuỗi giao dịch CRDTs để tự động gộp dữ liệu không gây khóa chặn liên lục địa.
  - id: KP8_2
    content: Định tuyến và Edge Computing
    keypoint_weight: 0.5
    description: Sử dụng Cloudflare Workers ở vùng biên để xử lý kiểm tra định dạng và thực hiện kiểm tra sơ bộ số dư cục bộ (local cache), hoàn thành giao dịch ghi nhanh tại vùng địa lý gần nhất rồi đồng bộ bất đồng bộ sau.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản và hệ thống tự động phục hồi sau thảm họa (Disaster Recovery Automation) cho toàn bộ cụm Kubernetes đa vùng khi một trong các vùng bị sập hoàn toàn mạng kết nối.
* **expected_key_points:**
  - id: KP9_1
    content: Phát hiện lỗi và Cô lập tự động (Auto-fencing)
    keypoint_weight: 0.5
    description: Thiết lập các node giám sát độc lập ngoài cụm (External Monitors). Khi 1 vùng bị sập kết nối mạng: cô lập ngay lập tức vùng đó khỏi các bản ghi DNS để tránh request đi vào.
  - id: KP9_2
    content: Dịch chuyển tài nguyên (Kubernetes Cluster Failover)
    keypoint_weight: 0.5
    description: Sử dụng ArgoCD và Velero để tự động phục hồi các stateful applications từ bản snapshot sao lưu định kỳ của vùng bị lỗi sang vùng đang chạy bình thường; cập nhật định tuyến IP chỉ trong vòng vài phút.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống giám sát và tự động scale tài nguyên (Auto-scaling) cực nhạy cho các dịch vụ Backend chịu tải biến động lớn đột ngột (như sự kiện Flash Sale), giảm thiểu thời gian trễ của việc tạo máy ảo/pods mới.
* **expected_key_points:**
  - id: KP10_1
    content: Scale dự đoán trước thời gian (Predictive & Pre-warm Scaling)
    keypoint_weight: 0.5
    description: Thiết lập lịch trình tự động khởi động và scale sẵn tài nguyên lên gấp 5 lần (pre-warming) trước thời điểm Flash Sale diễn ra 30 phút, tránh việc hệ thống bị sập do tốc độ scale không kịp tốc độ tải.
  - id: KP10_2
    content: Tối ưu hóa thời gian khởi chạy Pod (Cold Start Optimization)
    keypoint_weight: 0.5
    description: Tối ưu dung lượng Docker image cực nhỏ (dùng alpine/distroless); cấu hình sẵn cụm pods dự phòng ở trạng thái chờ (warm standby) để nhận tải tức thời dưới 5 giây khi có xung đột tải.

