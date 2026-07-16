# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2) - Tập Đề NoSQL Databases (12)

* **Role:** Backend Developer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh sự khác nhau cơ bản giữa cơ sở dữ liệu quan hệ (SQL) và cơ sở dữ liệu phi quan hệ (NoSQL). Khi nào nên chọn hệ quản trị nào?
* **expected_key_points:**
  - id: KP1_1
    content: Bản chất SQL vs NoSQL
    keypoint_weight: 0.5
    description: SQL lưu dưới dạng bảng có cấu trúc schema cố định, hỗ trợ ACID và JOIN mạnh mẽ. NoSQL không có cấu trúc schema cố định (schemaless), lưu dạng Document, Key-Value, Columnar hoặc Graph.
  - id: KP1_2
    content: Kịch bản lựa chọn tối ưu
    keypoint_weight: 0.5
    description: Chọn SQL cho giao dịch tài chính, hệ thống ERP cần tính toàn vẹn cao. Chọn NoSQL cho dữ liệu không đồng nhất, log lớn, hoặc ứng dụng cần scale ngang cực nhanh.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày cấu trúc dữ liệu Document-oriented của MongoDB. Tại sao việc lưu trữ dữ liệu dạng BSON/JSON lại linh hoạt hơn lưu trữ dạng bảng?
* **expected_key_points:**
  - id: KP2_1
    content: Bản chất Document trong MongoDB
    keypoint_weight: 0.5
    description: Dữ liệu được lưu dưới dạng các tài liệu (Documents) có định dạng BSON (Binary JSON), cho phép lồng các mảng (arrays) hoặc các tài liệu con (subdocuments).
  - id: KP2_2
    content: Tính linh hoạt của Schemaless
    keypoint_weight: 0.5
    description: Cho phép các tài liệu trong cùng một collection có các trường thông tin hoàn toàn khác nhau; dễ dàng thay đổi cấu trúc dữ liệu mà không cần chạy migration bảng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích khái niệm Key-Value Store trong NoSQL. Nêu ví dụ thực tế về việc sử dụng Redis làm Key-Value Store trong dự án.
* **expected_key_points:**
  - id: KP3_1
    content: Định nghĩa Key-Value Store
    keypoint_weight: 0.6
    description: Là cơ sở dữ liệu đơn giản nhất trong đó mọi bản ghi được lưu trữ dưới dạng một cặp khóa (Key) duy nhất ánh xạ tới một giá trị (Value) dữ liệu.
  - id: KP3_2
    content: Ví dụ thực tế sử dụng Redis
    keypoint_weight: 0.4
    description: Sử dụng Redis làm bộ lưu trữ cache cho thông tin cấu hình hệ thống hoặc token đăng nhập của người dùng, giúp truy xuất cực nhanh.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích định lý CAP trong hệ thống phân tán. Tại sao một hệ thống cơ sở dữ liệu phân tán không thể đạt được cả 3 yếu tố: Consistency, Availability, và Partition Tolerance cùng lúc?
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa 3 yếu tố CAP
    keypoint_weight: 0.5
    description: Consistency (mọi node đọc cùng dữ liệu mới nhất), Availability (mọi request đều nhận phản hồi không lỗi), Partition Tolerance (hệ thống vẫn chạy dù đứt kết nối mạng giữa các nodes).
  - id: KP4_2
    content: Tại sao không thể đồng thời cả 3
    keypoint_weight: 0.5
    description: Nếu có đứt mạng (P), để giữ tính nhất quán (C), ta phải từ chối ghi ở node bị cô lập (mất A). Ngược lại, nếu cho phép ghi ở node bị cô lập để giữ (A), dữ liệu giữa các node sẽ bị lệch (mất C).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích sự khác nhau giữa cơ chế thiết kế cơ sở dữ liệu quan hệ (chuyển sang nhiều bảng và dùng JOIN) và NoSQL (gộp dữ liệu vào một tài liệu - Denormalization).
* **expected_key_points:**
  - id: KP5_1
    content: Thiết kế Normalized vs Denormalized
    keypoint_weight: 0.5
    description: SQL ưu tiên chia nhỏ dữ liệu để tránh dư thừa (Normalization). NoSQL ưu tiên gộp toàn bộ thông tin liên quan vào chung 1 tài liệu (Denormalization) để đọc nhanh trong 1 query.
  - id: KP5_2
    content: Đánh đổi khi cập nhật và đọc
    keypoint_weight: 0.5
    description: Mô hình gộp của NoSQL đọc rất nhanh vì không cần JOIN nhưng cập nhật dữ liệu trùng lặp sẽ phức tạp và dễ gây bất nhất quán dữ liệu.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh sự khác nhau về cơ chế sao lưu và tính nhất quán dữ liệu giữa hai cơ chế persistence của Redis: RDB (Redis Database) và AOF (Append Only File).
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên lý hoạt động RDB vs AOF
    keypoint_weight: 0.6
    description: RDB chụp ảnh nhanh dữ liệu (snapshot) tại các khoảng thời gian cố định và ghi vào đĩa. AOF ghi lại mọi câu lệnh thay đổi dữ liệu vào cuối file log tuần tự trên đĩa.
  - id: KP6_2
    content: So sánh ưu nhược điểm hiệu năng
    keypoint_weight: 0.4
    description: RDB khôi phục nhanh hơn và ít tốn I/O đĩa nhưng dễ mất dữ liệu gần nhất khi sập nguồn. AOF an toàn dữ liệu hơn (RPO nhỏ) nhưng file log phình to nhanh và làm chậm hiệu năng ghi.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là lỗi nhất quán cuối cùng (Eventual Consistency) trong các cơ sở dữ liệu NoSQL phân tán (như Cassandra)? Làm thế nào để cấu hình mức độ nhất quán đọc/ghi (Quorum consistency)?
* **expected_key_points:**
  - id: KP7_1
    content: Bản chất Eventual Consistency
    keypoint_weight: 0.5
    description: Khi dữ liệu được ghi vào một node, nó sẽ đồng bộ bất đồng bộ sang các node khác; trong quá trình đồng bộ, client đọc ở node khác có thể nhận dữ liệu cũ.
  - id: KP7_2
    content: Cơ chế Quorum Consistency
    keypoint_weight: 0.5
    description: Cấu hình số lượng node tối thiểu phải xác nhận ghi thành công (W) và đọc thành công (R). Nếu $W + R > N$ (tổng số replicas), hệ thống sẽ đạt mức nhất quán mạnh (Strong Consistency).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế cơ sở dữ liệu NoSQL MongoDB lưu trữ dữ liệu của trang tin tức lớn hỗ trợ: bài viết, danh mục, bình luận của độc giả, và lượt thích, đảm bảo hiệu năng đọc tối đa.
* **expected_key_points:**
  - id: KP8_1
    content: Thiết kế nhúng subdocument bình luận
    keypoint_weight: 0.5
    description: Lưu trữ thông tin bài viết và nhúng danh sách 100 bình luận mới nhất (embedded array) vào chung tài liệu Bài viết để hiển thị nhanh trang chi tiết mà không cần JOIN.
  - id: KP8_2
    content: Tách collection cho bình luận phân trang
    keypoint_weight: 0.5
    description: Nếu số lượng bình luận cực lớn (>1000), tách bình luận sang collection `Comments` độc lập liên kết qua `article_id` để tránh vượt quá giới hạn kích thước tài liệu 16MB của MongoDB.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp giải quyết hiện tượng lệch dữ liệu (Stale Cache) khi cập nhật đồng thời ở cơ sở dữ liệu quan hệ chính PostgreSQL và NoSQL MongoDB đóng vai trò làm CSDL lưu trữ báo cáo.
* **expected_key_points:**
  - id: KP9_1
    content: Sử dụng Change Data Capture (CDC)
    keypoint_weight: 0.5
    description: Không viết mã ứng dụng cập nhật song song cả 2 DB. Sử dụng công cụ CDC (Debezium) lắng nghe file log WAL của PostgreSQL để phát hiện thay đổi.
  - id: KP9_2
    content: Đồng bộ bất đồng bộ qua Kafka
    keypoint_weight: 0.5
    description: Đẩy các sự kiện thay đổi từ CDC vào Kafka topic; viết các Consumers xử lý các sự kiện này để cập nhật tương ứng sang MongoDB, đảm bảo dữ liệu hội tụ chính xác.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống lưu trữ Time-Series (dữ liệu chuỗi thời gian) phục vụ giám sát nhiệt độ của 100,000 thiết bị cảm biến gửi dữ liệu mỗi 5 giây sử dụng MongoDB Bucket Design Pattern.
* **expected_key_points:**
  - id: KP10_1
    content: Nguyên lý Bucket Design Pattern
    keypoint_weight: 0.6
    description: Không tạo mỗi dòng dữ liệu là 1 document. Gom các dữ liệu đo được trong cùng một khoảng thời gian (ví dụ 1 giờ) của 1 thiết bị vào chung 1 document dưới dạng mảng dữ liệu lồng.
  - id: KP10_2
    content: Tối ưu hóa hiệu năng lưu trữ và index
    keypoint_weight: 0.4
    description: Giúp giảm thiểu số lượng tài liệu vật lý khổng lồ, tiết kiệm RAM để lưu trữ index và tối ưu hóa tốc độ truy vấn biểu thị đồ thị theo khoảng thời gian.

