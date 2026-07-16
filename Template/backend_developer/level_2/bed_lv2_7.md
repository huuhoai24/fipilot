# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2) - Tập Đề Basic System Scaling (7)

* **Role:** Backend Developer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa hai hình thức mở rộng hệ thống: Mở rộng theo chiều dọc (Vertical Scaling) và Mở rộng theo chiều ngang (Horizontal Scaling).
* **expected_key_points:**
  - id: KP1_1
    content: Đặc trưng Vertical Scaling
    keypoint_weight: 0.5
    description: Tăng cường tài nguyên phần cứng (CPU, RAM, SSD) cho máy chủ hiện tại. Dễ thực hiện nhưng bị giới hạn vật lý và có điểm chết duy nhất (Single Point of Failure).
  - id: KP1_2
    content: Đặc trưng Horizontal Scaling
    keypoint_weight: 0.5
    description: Bổ sung thêm nhiều máy chủ chạy song song. Khó cấu hình hơn nhưng hỗ trợ scale không giới hạn và tăng tính sẵn sàng cao (High Availability).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Load Balancer (Bộ cân bằng tải) là gì? Giải thích vai trò của nó trong việc phân phối traffic người dùng tới cụm máy chủ Backend.
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm Load Balancer
    keypoint_weight: 0.5
    description: Là thiết bị phần cứng hoặc phần mềm đứng trước cụm máy chủ, nhận request từ client và điều hướng chúng tới các server đang hoạt động phía sau.
  - id: KP2_2
    content: Vai trò phân phối tải và tăng độ tin cậy
    keypoint_weight: 0.5
    description: Giúp tránh quá tải cho bất kỳ máy chủ đơn lẻ nào; tự động loại bỏ server bị lỗi (unhealthy) khỏi danh sách định tuyến bằng cách kiểm tra sức khỏe (Health Check).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày cơ chế hoạt động của kiến trúc Database Replication dạng Master-Slave (hoặc Primary-Replica) để tăng khả năng đọc dữ liệu.
* **expected_key_points:**
  - id: KP3_1
    content: Vai trò Master và Slave
    keypoint_weight: 0.6
    description: Master node nhận toàn bộ các câu lệnh ghi (INSERT, UPDATE, DELETE). Slave nodes chỉ nhận các câu lệnh đọc (SELECT). Dữ liệu ghi từ Master được đồng bộ sang các Slaves.
  - id: KP3_2
    content: Tăng khả năng đọc (Read Scalability)
    keypoint_weight: 0.4
    description: Cho phép phân tán hàng vạn câu query đọc của người dùng sang nhiều Slave nodes, giúp giảm tải cực tốt cho Master node.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích sự khác nhau về nguyên lý hoạt động giữa ba thuật toán cân bằng tải phổ biến: Round Robin, Least Connections, và IP Hash.
* **expected_key_points:**
  - id: KP4_1
    content: Nguyên lý Round Robin và Least Connections
    keypoint_weight: 0.6
    description: Round Robin chia tải tuần tự đều cho các servers (phù hợp khi các server cấu hình bằng nhau). Least Connections chuyển request tới server đang xử lý ít kết nối nhất (phù hợp tác vụ dài ngắn khác nhau).
  - id: KP4_2
    content: Nguyên lý IP Hash
    keypoint_weight: 0.4
    description: Băm địa chỉ IP của client để trỏ cố định client đó vào một server duy nhất, thường dùng khi ứng dụng cần duy trì Session dạng Stateful.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích hiện tượng lệch pha dữ liệu (Replication Lag) trong kiến trúc Master-Slave bất đồng bộ. Lập trình viên Backend có thể xử lý lỗi đọc dữ liệu cũ ra sao?
* **expected_key_points:**
  - id: KP5_1
    content: Nguyên nhân xảy ra Replication Lag
    keypoint_weight: 0.5
    description: Do độ trễ truyền tải mạng hoặc Slave node bị quá tải dẫn đến việc đồng bộ dữ liệu ghi từ Master sang các Slaves bị chậm trễ từ vài giây đến vài phút.
  - id: KP5_2
    content: Giải pháp khắc phục ở tầng Backend
    keypoint_weight: 0.5
    description: Đối với các tác vụ quan trọng vừa ghi xong cần đọc lại ngay (ví dụ: đổi mật khẩu), bắt buộc định tuyến câu query đọc đó trực tiếp lên Master node thay vì Slave node.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là kỹ thuật phân vùng cơ sở dữ liệu (Database Sharding)? Phân biệt sự khác nhau giữa Vertical Sharding và Horizontal Sharding.
* **expected_key_points:**
  - id: KP6_1
    content: Khái niệm Database Sharding
    keypoint_weight: 0.5
    description: Là việc chia nhỏ một bảng dữ liệu khổng lồ thành nhiều cơ sở dữ liệu vật lý độc lập (shards) đặt trên nhiều máy chủ khác nhau để tăng tốc độ ghi đọc.
  - id: KP6_2
    content: Phân biệt Vertical vs Horizontal Sharding
    keypoint_weight: 0.5
    description: Vertical Sharding chia bảng theo cột (tách cột ít dùng sang bảng khác). Horizontal Sharding chia bảng theo dòng (ví dụ: dòng ID chẵn ở Shard 1, dòng lẻ ở Shard 2).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích vai trò và vị trí triển khai của Web Server (như Nginx) làm Reverse Proxy đứng trước Application Server (như Node.js, Spring Boot, Gunicorn).
* **expected_key_points:**
  - id: KP7_1
    content: Khái niệm Reverse Proxy
    keypoint_weight: 0.5
    description: Là máy chủ đệm đứng giữa các clients và Application Server; nhận các requests từ client và chuyển tiếp an toàn xuống ứng dụng Backend xử lý.
  - id: KP7_2
    content: Ưu điểm của Nginx làm Reverse Proxy
    keypoint_weight: 0.5
    description: Xử lý rất tốt các kết nối tĩnh, nén gzip; thực hiện SSL Termination (giải mã HTTPS tại Nginx giúp backend giảm tải); hỗ trợ cân bằng tải cơ bản và bảo vệ ứng dụng backend khỏi tiếp xúc trực tiếp mạng internet công cộng.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống phục vụ đọc/ghi dữ liệu cho ứng dụng mạng xã hội quy mô 10 triệu người dùng hoạt động hàng ngày, đảm bảo hệ thống không bị sập khi có luồng truy cập tăng đột biến.
* **expected_key_points:**
  - id: KP8_1
    content: Thiết kế phân tầng Caching và Load Balancing
    keypoint_weight: 0.5
    description: Đặt CDN ở biên cho ảnh/video static; Load Balancers định tuyến xuống cụm Web Servers; sử dụng Redis Cache đa tầng (L1/L2) để lưu trữ thông tin bảng tin (news feed).
  - id: KP8_2
    content: Thiết kế cơ sở dữ liệu phân tán
    keypoint_weight: 0.5
    description: Sử dụng kiến trúc Database Replication Master-Slave; Sharding dữ liệu người dùng dựa trên ID vùng địa lý; sử dụng Message Broker (Kafka) để xử lý bất đồng bộ các tác vụ ghi nặng (like, comment, notifications).

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp phân mảnh cơ sở dữ liệu (Database Sharding) sử dụng thuật toán nhất quán băm (Consistent Hashing) để quản lý 1 tỷ bản ghi người dùng phân bổ trên 5 nodes cơ sở dữ liệu.
* **expected_key_points:**
  - id: KP9_1
    content: Nguyên lý hoạt động Consistent Hashing
    keypoint_weight: 0.5
    description: Ánh xạ các Database Nodes và khóa dữ liệu (User ID) lên cùng một vòng tròn băm logic (Hash Ring) có kích thước cố định, dữ liệu sẽ được lưu tại Node đầu tiên tìm thấy theo chiều kim đồng hồ.
  - id: KP9_2
    content: Tối ưu hóa phân bổ tải và scale out
    keypoint_weight: 0.5
    description: Sử dụng Virtual Nodes cho mỗi DB Node vật lý để phân phối dữ liệu đều hơn trên vòng tròn băm, tránh điểm nóng (hotspotting); khi thêm/bớt DB Node chỉ cần di chuyển tối đa 1/N lượng dữ liệu.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp Dynamic Rate Limiting (Giới hạn tần suất gọi API động) có khả năng tự động điều chỉnh ngưỡng giới hạn request dựa trên tài nguyên CPU/RAM hiện tại của cụm máy chủ Backend.
* **expected_key_points:**
  - id: KP10_1
    content: Thu thập chỉ số tài nguyên thời gian thực
    keypoint_weight: 0.5
    description: Cài đặt một tiến trình chạy ngầm (Agent) thu thập mức sử dụng CPU/RAM của server -> cập nhật liên tục điểm số tải trọng lên Redis.
  - id: KP10_2
    content: Điều chỉnh Rate Limit động tại API Gateway
    keypoint_weight: 0.5
    description: API Gateway đọc điểm số tải trọng từ Redis: nếu CPU > 85%, Gateway tự động giảm ngưỡng Rate Limit của người dùng phổ thông xuống 50% để bảo vệ hệ thống không bị quá tải sập nguồn.

