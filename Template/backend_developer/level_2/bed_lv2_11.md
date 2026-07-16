# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2) - Tập Đề SQL Query Optimization (11)

* **Role:** Backend Developer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích vai trò của câu lệnh EXPLAIN trong tối ưu hóa truy vấn SQL. Những thông số nào trong kết quả EXPLAIN là quan trọng nhất?
* **expected_key_points:**
  - id: KP1_1
    content: Vai trò của EXPLAIN
    keypoint_weight: 0.5
    description: EXPLAIN hiển thị kế hoạch thực thi (Execution Plan) của hệ quản trị cơ sở dữ liệu đối với câu query, chỉ ra cách quét bảng và sử dụng index.
  - id: KP1_2
    content: Các thông số quan trọng cần lưu ý
    keypoint_weight: 0.5
    description: Type (phương thức quét: ALL, index, range, const), key (index thực tế được chọn), rows (ước lượng số dòng phải quét) và Extra (Using filesort, Using temporary).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Thế nào là chỉ mục hỗn hợp (Composite Index) trong CSDL quan hệ? Giải thích nguyên lý hoạt động của Leftmost Prefix Rule.
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa Composite Index
    keypoint_weight: 0.5
    description: Là chỉ mục được tạo trên sự kết hợp của nhiều cột khác nhau trong cùng một bảng (ví dụ: index trên `(col1, col2)`).
  - id: KP2_2
    content: Nguyên lý Leftmost Prefix Rule
    keypoint_weight: 0.5
    description: Chỉ mục chỉ có hiệu lực khi câu query tìm kiếm sử dụng các cột theo thứ tự từ trái sang phải. Nếu tìm kiếm bằng `col2` mà không có `col1`, index sẽ bị bỏ qua.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao việc sử dụng toán tử wildcards ở đầu chuỗi (ví dụ: `LIKE '%keyword%'`) lại gây chậm hiệu năng truy vấn nghiêm trọng? Giải pháp thay thế là gì?
* **expected_key_points:**
  - id: KP3_1
    content: Nguyên nhân gây chậm truy vấn
    keypoint_weight: 0.6
    description: Toán tử `LIKE '%keyword'` phá vỡ cấu trúc B-Tree Index, bắt buộc hệ thống phải quét toàn bộ bảng (Full Table Scan) để so khớp chuỗi.
  - id: KP3_2
    content: Các giải pháp thay thế hiệu quả
    keypoint_weight: 0.4
    description: Sử dụng các giải pháp tìm kiếm toàn văn chuyên dụng như Full-Text Search của DB hoặc tích hợp công cụ chuyên biệt như Elasticsearch.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là hiện tượng index bị ghi đè hoặc không được sử dụng (Index Scan vs Index Seek) trong SQL? Chỉ ra 3 trường hợp viết query làm mất tác dụng của index.
* **expected_key_points:**
  - id: KP4_1
    content: Phân biệt Index Scan và Index Seek
    keypoint_weight: 0.4
    description: Index Seek là duyệt trực tiếp đến bản ghi mong muốn (nhanh). Index Scan là duyệt qua toàn bộ cấu trúc index (chậm hơn).
  - id: KP4_2
    content: Các trường hợp viết query làm vô hiệu hóa index
    keypoint_weight: 0.6
    description: Sử dụng hàm trên cột index (ví dụ: `WHERE YEAR(created_at) = 2026`); thực hiện tính toán trên cột index (ví dụ: `WHERE price + 10 > 100`); so sánh khác kiểu dữ liệu (implicit type conversion).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích sự khác nhau giữa việc sử dụng truy vấn con `IN` và `EXISTS` trong SQL. Khi nào nên dùng loại nào?
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế hoạt động IN vs EXISTS
    keypoint_weight: 0.5
    description: `IN` quét toàn bộ kết quả của subquery rồi so khớp với outer query. `EXISTS` dừng quét ngay lập tức khi tìm thấy bản ghi đầu tiên khớp (trả về boolean).
  - id: KP5_2
    content: Kịch bản sử dụng tối ưu
    keypoint_weight: 0.5
    description: Dùng `IN` khi kết quả của subquery nhỏ. Dùng `EXISTS` khi kết quả của subquery lớn và bảng outer query nhỏ, giúp tối ưu thời gian xử lý.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao việc sử dụng phân trang bằng lệnh `OFFSET` lớn (ví dụ: `LIMIT 10 OFFSET 100000`) lại gây chậm hệ thống? Giải pháp phân trang tối ưu cho dữ liệu lớn là gì?
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên nhân chậm khi dùng OFFSET lớn
    keypoint_weight: 0.5
    description: DB vẫn phải quét qua 100,000 dòng dữ liệu trước đó, nạp vào bộ nhớ rồi mới bỏ đi và lấy ra 10 dòng cuối, gây lãng phí CPU và I/O đĩa.
  - id: KP6_2
    content: Giải pháp phân trang con trỏ (Cursor-based Pagination)
    keypoint_weight: 0.5
    description: Sử dụng con trỏ (ví dụ: `WHERE id > last_seen_id LIMIT 10`) để nhảy trực tiếp tới dòng dữ liệu cần lấy thông qua index, không cần dùng OFFSET.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là lỗi kết nối không đồng bộ (Connection Pool Exhaustion)? Lập trình viên Backend có thể cấu hình connection pool của DB ra sao để ngăn chặn nó?
* **expected_key_points:**
  - id: KP7_1
    content: Bản chất lỗi cạn kiệt Connection Pool
    keypoint_weight: 0.5
    description: Xảy ra khi toàn bộ các kết nối trong pool đều đang bận xử lý câu query dài hoặc bị treo, khiến các request mới phải xếp hàng chờ và gây ra timeout.
  - id: KP7_2
    content: Cấu hình tối ưu hóa Connection Pool
    keypoint_weight: 0.5
    description: Thiết lập kích thước pool hợp lý (`maxActive`, `minIdle`); cấu hình thời gian chờ tối đa (`connectionTimeout`); thiết lập thời gian tự động hủy câu query bị treo (`statementTimeout`).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp tối ưu hóa một câu lệnh JOIN phức tạp qua 4 bảng lớn (mỗi bảng hơn 10 triệu bản ghi) đang gây nghẽn hiệu năng hệ thống nặng nề.
* **expected_key_points:**
  - id: KP8_1
    content: Tối ưu hóa các điều kiện JOIN và Index
    keypoint_weight: 0.5
    description: Đảm bảo tất cả các cột tham gia điều kiện JOIN đều được đánh index đầy đủ và trùng kiểu dữ liệu; lọc bớt dữ liệu ở từng bảng con bằng WHERE trước khi thực hiện JOIN.
  - id: KP8_2
    content: Sử dụng Denormalization và Caching
    keypoint_weight: 0.5
    description: Nếu tối ưu index không đủ, thực hiện khử chuẩn hóa (Denormalization) gộp các trường hay hiển thị vào chung 1 bảng chính; hoặc lưu trữ kết quả của câu query phức tạp vào Redis Cache với TTL phù hợp.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống cơ sở dữ liệu hỗ trợ lưu trữ và truy vấn nhanh dữ liệu lịch sử log giao dịch của khách hàng tăng trưởng 50 triệu bản ghi mỗi tháng.
* **expected_key_points:**
  - id: KP9_1
    content: Giải pháp phân vùng bảng (Table Partitioning)
    keypoint_weight: 0.5
    description: Phân chia bảng giao dịch lớn thành các bảng phân vùng vật lý nhỏ dựa trên cột thời gian (Partition by Range trên cột `created_at` theo tháng).
  - id: KP9_2
    content: Quản lý vòng đời dữ liệu và nén
    keypoint_weight: 0.5
    description: Tách dữ liệu cũ (Cold Data) sang cơ sở dữ liệu lưu trữ giá rẻ hơn hoặc nén bảng chỉ đọc; thiết lập tiến trình tự động archive các bản ghi thọ > 1 năm.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp tối ưu hóa hiệu năng ghi (Write Heavy) cho cơ sở dữ liệu quan hệ khi hệ thống nhận hàng nghìn bản ghi INSERT mỗi giây từ các thiết bị IoT.
* **expected_key_points:**
  - id: KP10_1
    content: Sử dụng cơ chế Batch Insert và tắt constraints
    keypoint_weight: 0.5
    description: Gộp các câu lệnh INSERT đơn lẻ thành các câu lệnh bulk insert dạng lô lớn (batch size = 500-1000) trong một transaction duy nhất để giảm thiểu overhead mở/đóng kết nối.
  - id: KP10_2
    content: Kiến trúc hàng đệm ghi bất đồng bộ
    keypoint_weight: 0.5
    description: Đẩy dữ liệu IoT từ các thiết bị vào hàng đợi Message Broker (Kafka) -> viết các Worker tiêu thụ tin nhắn theo lô lớn để ghi bất đồng bộ vào DB chính, tránh nghẽn trực tiếp.

