# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2) - Tập Đề Relational Database Basics (1)

* **Role:** Backend Developer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày ý nghĩa của các thuộc tính trong mô hình giao dịch ACID (Atomicity, Consistency, Isolation, Durability) của cơ sở dữ liệu quan hệ.
* **expected_key_points:**
  - id: KP1_1
    content: Thuộc tính Atomicity và Consistency
    keypoint_weight: 0.5
    description: Atomicity (Tính nguyên tử) đảm bảo giao dịch chạy thành công hoàn toàn hoặc không thực hiện gì. Consistency (Tính nhất quán) đảm bảo dữ liệu hợp lệ theo mọi ràng buộc trước và sau giao dịch.
  - id: KP1_2
    content: Thuộc tính Isolation và Durability
    keypoint_weight: 0.5
    description: Isolation (Tính cô lập) đảm bảo các giao dịch chạy song song không nhìn thấy dữ liệu trung gian của nhau. Durability (Tính bền vững) đảm bảo dữ liệu được lưu vĩnh viễn vào ổ cứng khi commit.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa các loại SQL Joins phổ biến: INNER JOIN, LEFT JOIN, và RIGHT JOIN. Cho ví dụ thực tế.
* **expected_key_points:**
  - id: KP2_1
    content: Bản chất của các loại Joins
    keypoint_weight: 0.6
    description: INNER JOIN chỉ trả về bản ghi khớp ở cả 2 bảng. LEFT JOIN trả về toàn bộ bảng bên trái và dữ liệu khớp ở bảng phải (nếu không có thì trả NULL). RIGHT JOIN ngược lại với LEFT JOIN.
  - id: KP2_2
    content: Ví dụ thực tế rõ ràng
    keypoint_weight: 0.4
    description: Lấy ví dụ kết hợp bảng Users và Orders: INNER JOIN lấy user có đơn hàng, LEFT JOIN lấy toàn bộ user (kể cả chưa mua đơn nào).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao chúng ta cần sử dụng Indexes trong cơ sở dữ liệu quan hệ? Chỉ ra ưu điểm và nhược điểm về hiệu năng khi tạo index.
* **expected_key_points:**
  - id: KP3_1
    content: Mục đích và ưu điểm của Index
    keypoint_weight: 0.5
    description: Indexes giúp tăng tốc độ truy vấn SELECT và tìm kiếm dữ liệu bằng cách sử dụng các cấu trúc dữ liệu như B-Tree để tránh quét toàn bộ bảng (Full Table Scan).
  - id: KP3_2
    content: Nhược điểm về hiệu năng
    keypoint_weight: 0.5
    description: Làm chậm các câu lệnh ghi (INSERT, UPDATE, DELETE) vì hệ thống phải cập nhật cấu trúc index tương ứng trên ổ đĩa; đồng thời tiêu tốn thêm không gian lưu trữ.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích sự khác nhau giữa hai cấu trúc dữ liệu index phổ biến trong CSDL quan hệ: B-Tree Index và Hash Index. Khi nào nên dùng loại nào?
* **expected_key_points:**
  - id: KP4_1
    content: Cấu trúc dữ liệu và khả năng tìm kiếm
    keypoint_weight: 0.5
    description: B-Tree lưu dưới dạng cây cân bằng hỗ trợ tìm kiếm dải (range queries), sắp xếp dữ liệu. Hash Index lưu dạng bảng băm chỉ hỗ trợ tìm kiếm khớp chính xác (equality check).
  - id: KP4_2
    content: Kịch bản lựa chọn tối ưu
    keypoint_weight: 0.5
    description: Sử dụng B-Tree Index cho hầu hết các trường tìm kiếm, lọc và sắp xếp. Sử dụng Hash Index cho các trường ID hoặc mã băm chỉ truy vấn bằng toán tử bằng (=).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm Khóa ngoại (Foreign Key) và cơ chế Cascade Delete. Việc lạm dụng Cascade Delete có thể gây ra những rủi ro gì?
* **expected_key_points:**
  - id: KP5_1
    content: Bản chất Khóa ngoại và Cascade Delete
    keypoint_weight: 0.5
    description: Khóa ngoại đảm bảo tính toàn vẹn tham chiếu. Cascade Delete tự động xóa các bản ghi con ở bảng tham chiếu khi bản ghi cha bị xóa.
  - id: KP5_2
    content: Rủi ro khi lạm dụng
    keypoint_weight: 0.5
    description: Có thể gây mất dữ liệu hàng loạt không kiểm soát được nếu vô tình xóa bản ghi cha; gây chậm hệ thống do kích hoạt khóa chặn lan truyền (locking propagation) trên nhiều bảng lớn.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là lỗi N+1 Query trong ORM (như Hibernate, Sequelize, Prisma)? Làm thế nào để giải quyết lỗi này?
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên nhân lỗi N+1 Query
    keypoint_weight: 0.5
    description: Xảy ra khi ORM thực hiện 1 truy vấn để lấy danh sách cha (1), sau đó lặp qua danh sách đó và thực hiện thêm N truy vấn để lấy dữ liệu con liên quan.
  - id: KP6_2
    content: Giải pháp khắc phục
    keypoint_weight: 0.5
    description: Sử dụng kỹ thuật Eager Loading (như `include`, `join`, `preload`, hoặc `select_related` tùy ORM) để gộp truy vấn con bằng INNER/LEFT JOIN hoặc dùng câu lệnh `IN (id1, id2...)`.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Mức độ chuẩn hóa cơ sở dữ liệu (Normalization) từ 1NF, 2NF đến 3NF nhằm giải quyết vấn đề gì? Khi nào nên khử chuẩn hóa (Denormalization)?
* **expected_key_points:**
  - id: KP7_1
    content: Chuẩn hóa 1NF, 2NF, 3NF
    keypoint_weight: 0.6
    description: 1NF: các thuộc tính phải là nguyên tử (atomic). 2NF: thỏa mãn 1NF và loại bỏ phụ thuộc hàm bán phần. 3NF: thỏa mãn 2NF và loại bỏ phụ thuộc bắc cầu, giúp giảm thiểu dư thừa dữ liệu.
  - id: KP7_2
    content: Kịch bản khử chuẩn hóa
    keypoint_weight: 0.4
    description: Khi hệ thống cần đọc nhiều, các câu lệnh JOIN quá phức tạp gây nghẽn hiệu năng; ta nhân bản dữ liệu để tối ưu hóa tốc độ đọc (Read Heavy).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp giải quyết hiện tượng tranh chấp khóa (Deadlock) trong cơ sở dữ liệu quan hệ khi có nhiều luồng thực thi ghi đồng thời.
* **expected_key_points:**
  - id: KP8_1
    content: Cơ chế phát sinh Deadlock
    keypoint_weight: 0.5
    description: Xảy ra khi luồng A giữ khóa 1 và đợi khóa 2, trong khi luồng B giữ khóa 2 và đợi khóa 1, tạo thành một chu kỳ chờ đợi vô tận.
  - id: KP8_2
    content: Phương pháp khắc phục và ngăn ngừa
    keypoint_weight: 0.5
    description: Đảm bảo các giao dịch cập nhật tài nguyên theo cùng một thứ tự nhất định; giảm thời gian giữ khóa bằng cách tối ưu transaction; cấu hình timeout giao dịch và viết mã ứng dụng có cơ chế retry tự động.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** So sánh sự khác nhau về bản chất và kịch bản áp dụng giữa Khóa lạc quan (Optimistic Locking) và Khóa bi quan (Pessimistic Locking) trong thiết kế CSDL.
* **expected_key_points:**
  - id: KP9_1
    content: Bản chất của hai loại khóa
    keypoint_weight: 0.5
    description: Optimistic Locking dựa trên số phiên bản (version column) kiểm tra khi ghi, không khóa tài nguyên lúc đọc. Pessimistic Locking sử dụng câu lệnh `FOR UPDATE` để khóa tài nguyên ngay từ khi đọc.
  - id: KP9_2
    content: Kịch bản áp dụng phù hợp
    keypoint_weight: 0.5
    description: Dùng Optimistic Locking khi tranh chấp ghi thấp (low contention) để tăng throughput. Dùng Pessimistic Locking khi tranh chấp ghi rất cao (high contention) để tránh xung đột rollback liên tục.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích tác động của 4 mức cô lập giao dịch (Read Uncommitted, Read Committed, Repeatable Read, Serializable) đến hiệu năng đọc/ghi và giải thích cách giải quyết hiện tượng Phantom Read.
* **expected_key_points:**
  - id: KP10_1
    content: Tác động của các Isolation Levels
    keypoint_weight: 0.6
    description: Mức cô lập càng cao (Serializable) thì tính toàn vẹn dữ liệu càng tốt nhưng hiệu năng ghi càng giảm do phải khóa nhiều tài nguyên. Read Committed là mức phổ biến dung hòa tốt nhất.
  - id: KP10_2
    content: Khắc phục hiện tượng Phantom Read
    keypoint_weight: 0.4
    description: Sử dụng mức cô lập Serializable hoặc dùng cơ chế khóa dải giá trị (Gap Locks/Next-Key Locks) trong công cụ lưu trữ như InnoDB của MySQL để chặn chèn dữ liệu mới vào dải đang truy vấn.

