# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 1)

* **Role:** Backend Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy giải thích điểm khác biệt cốt lõi về mặt kiến trúc dữ liệu và cơ chế truy vấn giữa hai nhóm cơ sở dữ liệu: Relational Database (SQL) và Non-relational Database (NoSQL).
* **expected_key_points:**
  - id: KP1_1
    content: Phân biệt cấu trúc dữ liệu (Schema) và tính nhất quán
    keypoint_weight: 0.5
    description: SQL dựa trên cấu trúc bảng dữ liệu nghiêm ngặt (Strict Schema) với các hàng và cột, tuân thủ chặt chẽ tính chất ACID. NoSQL dựa trên cấu trúc linh hoạt (Dynamic Schema) dưới dạng Document, Key-Value, Graph hoặc Wide-column, ưu tiên khả năng mở rộng (Scalability).
  - id: KP1_2
    content: Cơ chế liên kết và mở rộng hệ thống (JOINs & Scaling)
    keypoint_weight: 0.5
    description: SQL sử dụng mệnh đề JOIN để liên kết các bảng có mối quan hệ và thường mở rộng theo chiều dọc (Vertical Scaling). NoSQL hạn chế phép toán JOIN, lưu trữ dữ liệu phi tập trung hoặc lặp lại (Denormalization) và tối ưu cho việc mở rộng theo chiều ngang (Horizontal Scaling).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong giao thức HTTP, hai mã trạng thái (HTTP Status Codes) `401 Unauthorized` và `403 Forbidden` khác nhau như thế nào về mặt logic xử lý quyền hạn?
* **expected_key_points:**
  - id: KP2_1
    content: Ý nghĩa lỗi xác thực của mã 401 (Authentication)
    keypoint_weight: 0.5
    description: Mã 401 xảy ra khi Client chưa thực hiện xác thực thông tin danh tính (chưa login) hoặc thông tin xác thực gửi lên (Token/Session) không hợp lệ/đã hết hạn. Hệ thống yêu cầu người dùng phải xác thực lại.
  - id: KP2_2
    content: Ý nghĩa lỗi phân quyền của mã 403 (Authorization)
    keypoint_weight: 0.5
    description: Mã 403 xảy ra khi Client đã đăng nhập thành công và Server đã nhận biết được danh tính, nhưng tài khoản của người dùng hiện tại không có đủ quyền hạn để truy cập vào tài nguyên yêu cầu (ví dụ: tài khoản User cố tình truy cập API của Admin).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Lỗ hổng bảo mật ứng dụng Web "Cross-Site Scripting" (XSS) xảy ra do nguyên nhân gì ở Backend và phương pháp phòng tránh cơ bản nhất là gì?
* **expected_key_points:**
  - id: KP3_1
    content: Nguyên nhân do thiếu kiểm tra và làm sạch dữ liệu đầu vào (Input Sanitization)
    keypoint_weight: 0.5
    description: Xảy ra khi Backend nhận dữ liệu độc hại chứa các thẻ script JavaScript từ người dùng, lưu vào Database và trả nguyên văn chuỗi đó về cho trình duyệt của người dùng khác thực thi mà không có sự kiểm tra.
  - id: KP3_2
    content: Giải pháp mã hóa dữ liệu đầu ra (Data Encoding/Escaping)
    keypoint_weight: 0.5
    description: Sử dụng các thư viện làm sạch dữ liệu đầu vào và thực hiện mã hóa các ký tự đặc biệt (HTML Escaping như chuyển `<` thành `&lt;`, `>` thành `&gt;`) trước khi render hoặc trả dữ liệu về phía Client, biến mã script thành chuỗi văn bản thuần túy.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong kiến trúc phát triển Backend, nguyên lý "L" (Liskov Substitution Principle - LSP) và "I" (Interface Segregation Principle - ISP) trong bộ nguyên lý SOLID quy định quy tắc viết code như thế nào?
* **expected_key_points:**
  - id: KP4_1
    content: Nguyên lý thay thế Liskov (Liskov Substitution Principle)
    keypoint_weight: 0.5
    description: Quy định các đối tượng của lớp con (Subclass) phải có khả năng thay thế hoàn toàn cho đối tượng của lớp cha (Superclass) mà không làm thay đổi tính đúng đắn hay phá vỡ logic hoạt động của chương trình phần mềm.
  - id: KP4_2
    content: Nguyên lý phân tách Giao diện (Interface Segregation Principle)
    keypoint_weight: 0.5
    description: Quy định không nên ép buộc một Class phải triển khai (implement) các hàm hoặc giao diện (Interfaces) mà nó không sử dụng đến. Thay vì tạo một Interface lớn chứa quá nhiều hàm, nên tách nhỏ thành nhiều Interface cụ thể, tập trung vào từng vai trò độc lập.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi thiết kế cơ sở dữ liệu quan hệ, việc thực hiện quy trình Chuẩn hóa dữ liệu (Database Normalization) cấp độ 1NF, 2NF, và 3NF nhằm giải quyết bài toán gì và điểm đánh đổi tiêu cực của nó là gì?
* **expected_key_points:**
  - id: KP5_1
    content: Lợi ích loại bỏ dữ liệu dư thừa và bất thường (Redundancy & Anomaly)
    keypoint_weight: 0.5
    description: Phân tách dữ liệu thành các bảng có mối quan hệ chặt chẽ nhằm triệt tiêu việc lưu trữ trùng lặp dữ liệu dư thừa, từ đó ngăn chặn các lỗi bất thường khi thực hiện thêm mới, cập nhật hoặc xóa dữ liệu (Insertion, Update, Deletion Anomalies).
  - id: KP5_2
    content: Đánh đổi chi phí tính toán khi truy vấn (Performance Overhead)
    keypoint_weight: 0.5
    description: Việc chia nhỏ dữ liệu ra quá nhiều bảng khiến câu lệnh truy vấn phức tạp hơn, ép Database Engine phải tốn thêm tài nguyên và thời gian thực hiện rất nhiều phép toán liên kết bảng (JOINs), làm giảm tốc độ đọc dữ liệu đối với các bảng có kích thước lớn.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi sử dụng bộ đệm (Caching) cho hệ thống, hãy giải thích nguyên nhân xảy ra hiện tượng "Cache Stampede" (hay còn gọi là Cache Avalanche / Thủng kho bộ đệm) và một giải pháp kỹ thuật để xử lý.
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên nhân do một key dữ liệu hot bị hết hạn đồng thời
    keypoint_weight: 0.5
    description: Xảy ra khi một key dữ liệu có lượng truy cập cực kỳ lớn (Hot Key) bất ngờ bị hết hạn (Expired) trong Cache, hoặc khi toàn bộ Cache bị sập đột ngột. Tại thời điểm đó, hàng vạn request đọc song song đồng loạt bị Cache Miss và tràn thẳng xuống Database gốc cùng một lúc để lấy dữ liệu, làm sập hoàn toàn hệ thống Database.
  - id: KP6_2
    content: Giải pháp sử dụng cơ chế Khóa hoặc tính toán ngẫu nhiên (Mutex Lock / Random TTL)
    keypoint_weight: 0.5
    description: Áp dụng Mutex Lock (chỉ cho phép request đầu tiên bị lỡ cache được quyền xuống DB lấy dữ liệu và ghi lại vào cache, các request khác phải xếp hàng đợi); hoặc cấu hình thời gian hết hạn ngẫu nhiên (Jitter/Random TTL) cho các key để tránh việc chúng bị xóa bỏ đồng thời.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt về cơ chế hoạt động mạng và ngữ cảnh áp dụng giữa phương pháp giao tiếp thời gian thực WebSockets và phương pháp Polling truyền thống là gì?
* **expected_key_points:**
  - id: KP7_1
    content: Cơ chế kết nối một lần và hai chiều của WebSockets (Bi-directional)
    keypoint_weight: 0.5
    description: WebSockets thiết lập một kết nối TCP duy nhất và duy trì trạng thái sống vĩnh viễn (Persistent connection). Cả Client và Server đều có thể chủ động tự do đẩy dữ liệu cho nhau bất cứ lúc nào (Full-duplex), phù hợp cho ứng dụng chat, chứng khoán thời gian thực.
  - id: KP7_2
    content: Cơ chế gửi yêu cầu lặp lại liên tục của Polling (Request-Response)
    keypoint_weight: 0.5
    description: Polling bắt Client phải liên tục chủ động gửi các HTTP Request định kỳ theo khoảng thời gian cố định (ví dụ cứ 5 giây một lần) để hỏi Server xem có dữ liệu mới hay không. Phương pháp này gây lãng phí tài nguyên băng thông đường truyền và tạo ra độ trễ (Latency) nhận thông tin.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong kiến trúc hệ thống phân tán hoặc Microservices, tại sao mô hình giao dịch "Two-Phase Commit" (2PC) lại gặp khó khăn về mặt hiệu năng mở rộng hệ thống? Kiến trúc "Saga Pattern" giải quyết bài toán giao dịch phân tán dựa trên nguyên lý nào?
* **expected_key_points:**
  - id: KP8_1
    content: Khuyết điểm nghẽn mạch đồng bộ và nguy cơ Deadlock của 2PC
    keypoint_weight: 0.4
    description: 2PC là cơ chế đồng bộ (Synchronous). Nó yêu cầu một node điều phối trung tâm khóa (Lock) tài nguyên trên tất cả các dịch vụ tham gia xuyên suốt hai giai đoạn (Prepare và Commit). Nếu một dịch vụ phản hồi chậm hoặc mất kết nối, toàn bộ hệ thống sẽ bị treo luồng tính toán, tiêu tốn tài nguyên và cực kỳ dễ xảy ra hiện tượng Deadlock.
  - id: KP8_2
    content: Nguyên