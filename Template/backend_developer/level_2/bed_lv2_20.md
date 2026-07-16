# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2) - Tập Đề Memory Management và Performance (20)

* **Role:** Backend Developer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Garbage Collection (Bộ dọn rác) trong lập trình backend (như Java JVM, Node.js V8) hoạt động như thế nào? Nêu vai trò của nó.
* **expected_key_points:**
  - id: KP1_1
    content: Nguyên lý hoạt động cơ bản của GC
    keypoint_weight: 0.5
    description: Bộ dọn rác chạy ngầm tự động theo dõi, phát hiện và thu hồi các vùng nhớ bộ nhớ (trên Heap) của các đối tượng không còn được tham chiếu sử dụng bởi chương trình.
  - id: KP1_2
    content: Vai trò của GC
    keypoint_weight: 0.5
    description: Giúp giải phóng lập trình viên khỏi việc cấp phát và giải phóng bộ nhớ thủ công; ngăn chặn lỗi tràn bộ nhớ (Out of Memory) cơ bản.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Thế nào là lỗi rò rỉ bộ nhớ (Memory Leak) trong ứng dụng Backend? Nêu 1 nguyên nhân phổ biến gây ra rò rỉ bộ nhớ.
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm Memory Leak
    keypoint_weight: 0.5
    description: Xảy ra khi các vùng bộ nhớ của đối tượng không còn sử dụng nhưng vẫn bị tham chiếu bởi ứng dụng, khiến Garbage Collector không thể dọn dẹp giải phóng.
  - id: KP2_2
    content: Nguyên nhân phổ biến
    keypoint_weight: 0.5
    description: Lưu trữ đối tượng vào mảng tĩnh toàn cục (Static collection) tăng dần theo thời gian mà không bao giờ xóa bỏ.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích vai trò của cơ chế nén dữ liệu đầu ra (Gzip Compression) cấu hình tại Web Server đối với hiệu năng tải trang của người dùng.
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế Gzip Compression
    keypoint_weight: 0.5
    description: Web Server tự động nén các file text (HTML, CSS, JS, JSON) thành file dung lượng nhỏ trước khi gửi qua mạng; trình duyệt của client nhận được sẽ giải nén tự động.
  - id: KP3_2
    content: Hiệu quả cải thiện hiệu năng
    keypoint_weight: 0.5
    description: Giảm dung lượng băng thông truyền tải mạng tới 70%, giúp tăng tốc độ phản hồi API và giảm thời gian hiển thị trang web của người dùng.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích sự khác nhau về vùng lưu trữ dữ liệu, kích thước và vòng đời giữa Stack Memory và Heap Memory bên trong tiến trình ứng dụng.
* **expected_key_points:**
  - id: KP4_1
    content: Đặc trưng Stack Memory
    keypoint_weight: 0.5
    description: Lưu trữ các biến cục bộ, tham chiếu đối tượng và lời gọi hàm. Kích thước nhỏ cố định, truy xuất rất nhanh, tự động giải phóng khi hàm kết thúc (LIFO).
  - id: KP4_2
    content: Đặc trưng Heap Memory
    keypoint_weight: 0.5
    description: Lưu trữ các đối tượng thực tế (objects). Kích thước lớn linh hoạt, truy xuất chậm hơn Stack và do bộ dọn rác (GC) quản lý giải phóng vòng đời.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là hiện tượng CPU Spikes (Bộ vi xử lý tăng vọt 100%) của ứng dụng Backend? Nêu 3 nguyên nhân phổ biến và cách kiểm tra xử lý.
* **expected_key_points:**
  - id: KP5_1
    content: Các nguyên nhân gây CPU Spikes
    keypoint_weight: 0.5
    description: Chạy vòng lặp vô tận (infinite loop); thực hiện mã hóa băm mật khẩu quá nặng liên tục; hoặc do DB truy vấn quét bảng lớn gây block luồng CPU xử lý I/O.
  - id: KP5_2
    content: Cách kiểm tra xử lý sự cố
    keypoint_weight: 0.5
    description: Sử dụng công cụ giám sát tiến trình hệ điều hành (Top, HTOP); sử dụng công cụ Profiler của ngôn ngữ để xem biểu đồ Flame Graph tìm hàm tiêu tốn nhiều thời gian xử lý nhất.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách sử dụng bộ nhớ đệm ứng dụng cục bộ (Local In-Memory Cache) so với bộ nhớ đệm phân tán (Distributed Cache như Redis) xét về hiệu năng và chia sẻ dữ liệu.
* **expected_key_points:**
  - id: KP6_1
    content: Đặc trưng Local In-Memory Cache
    keypoint_weight: 0.5
    description: Lưu trong RAM của chính instance ứng dụng (như Caffeine, Guava). Tốc độ đọc siêu nhanh (0ms) nhưng không thể chia sẻ dữ liệu giữa các instances khi scale ngang.
  - id: KP6_2
    content: Đặc trưng Distributed Cache (Redis)
    keypoint_weight: 0.5
    description: Đặt trên server độc lập kết nối qua mạng. Đọc chậm hơn local cache (tốn round-trip mạng) nhưng chia sẻ trạng thái chung hoàn hảo giữa tất cả các instances.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm Rò rỉ kết nối (Connection Leak) đối với Database Connection Pool. Làm thế nào để đảm bảo giải phóng kết nối trong mã nguồn ứng dụng?
* **expected_key_points:**
  - id: KP7_1
    content: Bản chất lỗi Connection Leak
    keypoint_weight: 0.5
    description: Xảy ra khi ứng dụng mở kết nối tới DB để thực hiện query nhưng quên đóng kết nối đó sau khi dùng xong, khiến connection pool cạn kiệt kết nối hợp lệ.
  - id: KP7_2
    content: Giải pháp giải phóng kết nối triệt để
    keypoint_weight: 0.5
    description: Đặt lệnh đóng kết nối trong khối `finally { connection.close(); }` hoặc sử dụng cú pháp tự động giải phóng tài nguyên (như `try-with-resources` trong Java).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp xử lý và phân tích một file dữ liệu log thô dung lượng 50GB trên một máy chủ ứng dụng Backend có cấu hình RAM giới hạn ở mức 2GB.
* **expected_key_points:**
  - id: KP8_1
    content: Sử dụng cơ chế Stream đọc dữ liệu từng dòng
    keypoint_weight: 0.5
    description: Không đọc toàn bộ file vào bộ nhớ RAM (gây lỗi Out of Memory). Sử dụng cơ chế đọc luồng (Stream/Line Reader) để nạp và xử lý tuần tự từng dòng dữ liệu log tại một thời điểm.
  - id: KP8_2
    content: Xử lý song song bằng hàng đợi đĩa (MapReduce cục bộ)
    keypoint_weight: 0.5
    description: Chia file 50GB thành các file nhỏ 500MB -> viết luồng xử lý song song trên các file nhỏ này -> gộp kết quả phân tích trung gian vào file kết quả cuối cùng.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản chuẩn đoán và xử lý lỗi Rò rỉ bộ nhớ (Memory Leak) đang xảy ra âm thầm trên môi trường Production, khiến ứng dụng Backend bị crash OOM sau mỗi 3 ngày hoạt động.
* **expected_key_points:**
  - id: KP9_1
    content: Cấu hình tự động chụp Heap Dump khi crash OOM
    keypoint_weight: 0.5
    description: Cấu hình JVM flag `-XX:+HeapDumpOnOutOfMemoryError` hoặc cấu hình Node.js để tự động xuất file Heap Snapshot khi ứng dụng cạn kiệt bộ nhớ.
  - id: KP9_2
    content: Phân tích Heap Dump bằng Eclipse Memory Analyzer (MAT)
    keypoint_weight: 0.5
    description: Nạp file Heap Dump vào công cụ phân tích; tìm kiếm các đối tượng chiếm giữ phần trăm bộ nhớ lớn nhất (Dominator Tree); truy vết chuỗi tham chiếu để xác định class rò rỉ.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp tối ưu hóa hiệu năng khởi chạy ứng dụng (Cold Start Optimization) chạy trên môi trường Serverless (như AWS Lambda) để thời gian trễ của request đầu tiên giảm xuống dưới 200ms.
* **expected_key_points:**
  - id: KP10_1
    content: Tối ưu hóa kích thước gói triển khai
    keypoint_weight: 0.5
    description: Giảm dung lượng code đóng gói bằng cách loại bỏ các thư viện phụ thuộc không dùng; sử dụng kỹ thuật tree-shaking; tránh dùng các framework khởi chạy nặng nề.
  - id: KP10_2
    content: Sử dụng Kế hoạch Giữ ấm (Provisioned Concurrency)
    keypoint_weight: 0.5
    description: Cấu hình Provisioned Concurrency để giữ tối thiểu N instance luôn ở trạng thái ấm (khởi động sẵn); hoặc viết cronjob định kỳ 5 phút gọi Lambda 1 lần để giữ ấm instance.

