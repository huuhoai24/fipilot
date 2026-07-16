# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 3) - Tập Đề Advanced Databases và MVCC (2)

* **Role:** Backend Developer
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Phân tích và so sánh sự khác nhau về nguyên lý cấu trúc và trường hợp áp dụng tối ưu giữa chỉ mục dạng B-Tree Index và Hash Index trong cơ sở dữ liệu quan hệ.
* **expected_key_points:**
  - id: KP1_1
    content: Cấu trúc dữ liệu và Độ phức tạp
    keypoint_weight: 0.5
    description: B-Tree Index sắp xếp dữ liệu theo dạng cây cân bằng, cho phép tìm kiếm trong $O(\log N)$. Hash Index sử dụng bảng băm để ánh xạ trực tiếp khóa tìm kiếm sang địa chỉ bản ghi, cho phép tìm kiếm trong $O(1)$.
  - id: KP1_2
    content: Trường hợp áp dụng tối ưu
    keypoint_weight: 0.5
    description: B-Tree cực kỳ mạnh mẽ cho các truy vấn phạm vi (range queries: `>`, `<`, `BETWEEN`) và sắp xếp dữ liệu (`ORDER BY`). Hash Index chỉ hỗ trợ tìm kiếm khớp chính xác (`=`, `IN`) và hoàn toàn không hỗ trợ tìm kiếm theo dải hay sắp xếp.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích bốn mức cô lập giao dịch (Transaction Isolation Levels): Read Uncommitted, Read Committed, Repeatable Read, và Serializable. Mỗi mức ngăn chặn được những lỗi đồng thời nào?
* **expected_key_points:**
  - id: KP2_1
    content: Đặc trưng các mức cô lập
    keypoint_weight: 0.6
    description: Read Uncommitted (cho phép đọc dữ liệu chưa commit). Read Committed (chỉ đọc dữ liệu đã commit). Repeatable Read (đảm bảo giá trị đọc không đổi trong suốt transaction). Serializable (cô lập hoàn toàn như thể chạy tuần tự).
  - id: KP2_2
    content: Các lỗi đồng thời được ngăn chặn
    keypoint_weight: 0.4
    description: Dirty Read (ngăn chặn từ mức Read Committed). Non-repeatable Read (ngăn chặn từ mức Repeatable Read). Phantom Read (ngăn chặn hoàn toàn ở mức Serializable).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Phân tích hiện tượng Đọc ảo (Phantom Read) trong cơ sở dữ liệu. Làm thế nào để ngăn chặn nó bằng cơ chế khóa?
* **expected_key_points:**
  - id: KP3_1
    content: Bản chất Phantom Read
    keypoint_weight: 0.5
    description: Xảy ra khi Transaction A thực hiện đọc một tập hợp các dòng thỏa mãn điều kiện, sau đó Transaction B thêm/bớt các dòng thỏa mãn điều kiện đó và commit; Transaction A đọc lại thấy xuất hiện thêm các dòng mới (phantom dòng).
  - id: KP3_2
    content: Ngăn chặn bằng cơ chế khóa
    keypoint_weight: 0.5
    description: Sử dụng khóa dải giá trị (Range Locks/Gap Locks) để khóa các khoảng trống giữa các chỉ mục, ngăn chặn không cho transaction khác chèn dữ liệu mới vào dải đang bị khóa.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích chi tiết cơ chế hoạt động của MVCC (Multi-Version Concurrency Control) trong PostgreSQL. Tại sao hệ thống lại cần tiến trình VACUUM?
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế hoạt động của MVCC
    keypoint_weight: 0.5
    description: PostgreSQL không ghi đè dữ liệu cũ khi UPDATE/DELETE. Thay vào đó, nó đánh dấu ẩn bản ghi cũ và tạo một bản ghi mới (tuple) gán kèm hai biến chỉ mục thời gian `xmin` và `xmax` để quản lý phiên bản cho từng transaction.
  - id: KP4_2
    content: Vai trò của tiến trình VACUUM
    keypoint_weight: 0.5
    description: Tiến trình VACUUM quét dọn các bản ghi cũ bị ẩn (dead tuples) đã chết để thu hồi không gian bộ nhớ đĩa cứng và tránh lỗi tràn số định danh transaction ID (transaction ID wraparound).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế giải pháp phân mảnh cơ sở dữ liệu (Database Sharding) cho hệ thống xử lý 1 tỷ bản ghi giao dịch bằng cách sử dụng Consistent Hashing.
* **expected_key_points:**
  - id: KP5_1
    content: Nguyên lý Consistent Hashing và Shard Key
    keypoint_weight: 0.5
    description: Consistent Hashing phân bổ các shard nodes và shard keys của dữ liệu lên cùng một vòng tròn băm logic (hash ring). Sử dụng ID khách hàng làm shard key để gom cụm dữ liệu liên quan.
  - id: KP5_2
    content: Tái cân bằng tải (Rebalancing) và Virtual Nodes
    keypoint_weight: 0.5
    description: Sử dụng các nút ảo (Virtual Nodes) để phân bổ đều khóa dữ liệu lên vòng tròn băm, tránh hiện tượng lệch tải; khi thêm/bớt shard node chỉ cần dịch chuyển một lượng cực nhỏ dữ liệu lân cận.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh ưu nhược điểm và kịch bản áp dụng thực tế giữa hai cơ chế khóa: Khóa lạc quan (Optimistic Locking) và Khóa bi quan (Pessimistic Locking).
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên lý khóa lạc quan vs bi quan
    keypoint_weight: 0.5
    description: Khóa lạc quan không khóa tài nguyên lúc đọc, chỉ kiểm tra số phiên bản (version column) trước khi update. Khóa bi quan khóa trực tiếp bản ghi bằng lệnh `SELECT ... FOR UPDATE` ngăn luồng khác ghi đọc.
  - id: KP6_2
    content: Trường hợp áp dụng
    keypoint_weight: 0.5
    description: Chọn khóa lạc quan khi tỷ lệ tranh chấp ghi thấp (low contention), giúp tối ưu băng thông. Chọn khóa bi quan khi tỷ lệ tranh chấp ghi cực cao (high contention) để tránh lãng phí chi phí rollback/retry.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế Write-Ahead Logging (WAL) và tại sao nó đảm bảo thuộc tính bền vững (Durability) của giao dịch ACID ngay cả khi server bị sập nguồn đột ngột.
* **expected_key_points:**
  - id: KP7_1
    content: Nguyên lý hoạt động của WAL
    keypoint_weight: 0.6
    description: Mọi thay đổi dữ liệu phải được ghi tuần tự vào file log WAL trên đĩa cứng trước khi ghi thực sự vào file dữ liệu chính (data blocks) trên RAM/disk.
  - id: KP7_2
    content: Khả năng phục hồi sau sự cố (Crash Recovery)
    keypoint_weight: 0.4
    description: Khi khởi động lại sau sập nguồn, cơ sở dữ liệu đọc file log WAL để chạy lại các giao dịch đã commit (Redo) và hoàn trả các giao dịch chưa commit (Undo) về trạng thái nhất quán.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống cơ sở dữ liệu phân tán tự động sharding hỗ trợ ghi tải cao, đảm bảo phân bổ dữ liệu đều trên các shard và tự động tái cân bằng (Auto-resharding) khi thêm/bớt nodes mà không làm gián đoạn dịch vụ.
* **expected_key_points:**
  - id: KP8_1
    content: Định tuyến truy vấn (Routing Layer) và metadata
    keypoint_weight: 0.5
    description: Thiết kế lớp Proxy định tuyến các câu lệnh dựa trên metadata của Shard Map (lưu trên Zookeeper/etcd); sử dụng Consistent Hashing để xác định vị trí shard của key.
  - id: KP8_2
    content: Cơ chế di trú dữ liệu online (Live Resharding)
    keypoint_weight: 0.5
    description: Khi scale out: thực hiện sao chép nền (background replication) dải keys cần di chuyển -> chạy CDC để đồng bộ các thay đổi delta thời gian thực -> switch metadata trỏ sang node mới -> xóa dữ liệu cũ bất đồng bộ.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống lưu trữ dữ liệu chuỗi thời gian (Time-Series) từ 10 triệu thiết bị IoT gửi về mỗi giây, tối ưu hóa tốc độ ghi và dung lượng đĩa sử dụng kiến trúc LSM-Tree.
* **expected_key_points:**
  - id: KP9_1
    content: Cấu trúc ghi của LSM-Tree (MemTable & SSTable)
    keypoint_weight: 0.5
    description: Dữ liệu mới ghi tuần tự vào Commit Log (WAL) và lưu vào bộ nhớ đệm MemTable (RAM). Khi MemTable đầy, thực hiện flush bất đồng bộ xuống đĩa dưới dạng file SSTable (Sorted String Table) được sắp xếp cố định.
  - id: KP9_2
    content: Nén dữ liệu và Compaction (Thu dọn)
    keypoint_weight: 0.5
    description: Áp dụng kỹ thuật nén nơ-ron (như Delta-encoding) cho chuỗi thời gian; thiết lập tiến trình Compaction định kỳ (Size-tiered hoặc Leveled Compaction) để gộp các file SSTables và loại bỏ bản ghi trùng lặp.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp khắc phục hiện tượng thắt nút cổ chai (Hotspotting) trên các key nóng trong hệ thống lưu trữ phân tán dạng Key-Value khi một lượng lớn request dồn vào một node cụ thể.
* **expected_key_points:**
  - id: KP10_1
    content: Phát hiện Hotspot key động
    keypoint_weight: 0.4
    description: Xây dựng cơ chế theo dõi số lượng requests (read/write frequency) tại mỗi node; khi phát hiện key vượt ngưỡng giới hạn, đánh dấu là Hotkey.
  - id: KP10_2
    content: Giải pháp phân tán tải và Caching
    keypoint_weight: 0.6
    description: Thêm hậu tố ngẫu nhiên (salt) vào Hotkey để phân tán nó sang nhiều shard khác nhau (ví dụ: `key` thành `key_1`, `key_2`); sử dụng Local Cache (L1 Cache) trực tiếp tại máy chủ ứng dụng để giảm 99% tải truy vấn xuống KV store.

