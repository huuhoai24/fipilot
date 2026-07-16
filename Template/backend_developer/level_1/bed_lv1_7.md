# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 1)

* **Role:** Backend Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt điểm khác biệt cốt lõi về mặt kiến trúc dữ liệu (Schema) và khả năng mở rộng hệ thống (Scaling) giữa hai nhóm cơ sở dữ liệu: Relational Database (SQL) và Non-relational Database (NoSQL).
* **expected_key_points:**
  - id: KP1_1
    content: Phân biệt cấu trúc dữ liệu Schema chặt chẽ và linh hoạt
    keypoint_weight: 0.5
    description: SQL dựa trên cấu trúc bảng dữ liệu nghiêm ngặt cố định (Strict Schema) với các hàng và cột, tuân thủ tính chất ACID. NoSQL dựa trên cấu trúc linh hoạt (Dynamic Schema) dưới dạng Document, Key-Value, Graph hoặc Wide-column, ưu tiên hiệu năng mở rộng.
  - id: KP1_2
    content: Phân biệt cơ chế mở rộng hệ thống theo chiều dọc và chiều ngang
    keypoint_weight: 0.5
    description: SQL tối ưu cho việc mở rộng theo chiều dọc (Vertical Scaling - nâng cấp CPU/RAM máy chủ). NoSQL được thiết kế để mở rộng theo chiều ngang (Horizontal Scaling - thêm nhiều máy chủ phổ thông vào cụm hệ thống phân tán nhờ hạn chế phép toán JOIN phức tạp).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế API theo chuẩn HTTP, hai mã lỗi trạng thái phản hồi `401 Unauthorized` và `403 Forbidden` khác nhau như thế nào về mặt logic xử lý phân quyền?
* **expected_key_points:**
  - id: KP2_1
    content: Ý nghĩa lỗi xác thực của mã lỗi 401 (Authentication Failure)
    keypoint_weight: 0.5
    description: Mã 401 xảy ra khi Client chưa thực hiện xác thực thông tin danh tính (chưa đăng nhập) hoặc thông tin xác thực gửi lên (như Token/Session) không hợp lệ hoặc đã hết hạn. Hệ thống yêu cầu kiểm tra lại danh tính.
  - id: KP2_2
    content: Ý nghĩa lỗi phân quyền của mã lỗi 403 (Authorization Failure)
    keypoint_weight: 0.5
    description: Mã 403 xảy ra khi Client đã đăng nhập thành công và Server đã nhận biết được danh tính chính xác, nhưng tài khoản của người dùng hiện tại không có đủ quyền hạn logic để truy cập vào tài nguyên yêu cầu (ví dụ tài khoản khách cố truy cập API của Admin).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Lỗ hổng bảo mật ứng dụng Web "Cross-Site Scripting" (XSS) xảy ra do nguyên nhân gì ở Backend và giải pháp phòng tránh cốt lõi nhất là gì?
* **expected_key_points:**
  - id: KP3_1
    content: Nguyên nhân do thiếu kiểm tra dữ liệu đầu vào và lưu trữ mã độc
    keypoint_weight: 0.5
    description: Xảy ra khi Backend nhận dữ liệu chứa các thẻ script JavaScript độc hại từ một người dùng, lưu thẳng vào Database mà không thực hiện kiểm tra, làm sạch, sau đó trả nguyên văn chuỗi đó về trình duyệt của người dùng khác.
  - id: KP3_2
    content: Giải pháp mã hóa dữ liệu đầu ra biến đổi ký tự đặc biệt
    keypoint_weight: 0.5
    description: Sử dụng các thư viện tiền xử lý làm sạch đầu vào và thực hiện kỹ thuật mã hóa dữ liệu đầu ra (HTML Escaping như chuyển `<` thành `&lt;`, `>` thành `&gt;`) trước khi trả về phía Client để biến mã độc thành văn bản thuần không thể thực thi.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong bộ nguyên lý SOLID, hai nguyên lý "L" (Liskov Substitution Principle - LSP) và "I" (Interface Segregation Principle - ISP) quy định quy tắc viết code như thế nào?
* **expected_key_points:**
  - id: KP4_1
    content: Quy tắc thay thế đối tượng của nguyên lý Liskov
    keypoint_weight: 0.5
    description: Quy định các đối tượng của lớp con (Subclass) phải có khả năng thay thế hoàn toàn cho đối tượng của lớp cha (Superclass) mà không làm thay đổi tính đúng đắn hoặc phá vỡ các logic hoạt động sẵn có của chương trình.
  - id: KP4_2
    content: Quy tắc chia nhỏ giao diện của nguyên lý Interface Segregation
    keypoint_weight: 0.5
    description: Quy định không nên ép buộc một Class phải triển khai các hàm hoặc phương thức của một Giao diện (Interface) mà nó không sử dụng đến. Nên tách nhỏ một Interface lớn thành nhiều Interface cụ thể theo từng vai trò độc lập.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi thiết kế cơ sở dữ liệu quan hệ, việc thực hiện quy trình Chuẩn hóa dữ liệu (Database Normalization) đến cấp độ 3NF nhằm giải quyết bài toán gì và điểm đánh đổi tiêu cực của nó là gì?
* **expected_key_points:**
  - id: KP5_1
    content: Lợi ích loại bỏ dữ liệu dư thừa và lỗi bất thường (Redundancy & Anomalies)
    keypoint_weight: 0.5
    description: Phân tách dữ liệu thành các bảng chuyên biệt nhằm triệt tiêu việc lưu trữ trùng lặp dữ liệu dư thừa, ngăn chặn các lỗi bất thường khi thực hiện thêm mới, cập nhật hoặc xóa dữ liệu (Insertion, Update, Deletion Anomalies).
  - id: KP5_2
    content: Đánh đổi chi phí hiệu năng tính toán phép toán JOIN (Performance Overhead)
    keypoint_weight: 0.5
    description: Việc chia nhỏ dữ liệu ra quá nhiều bảng khiến câu lệnh truy vấn phức tạp hơn, ép Database Engine phải tốn thêm tài nguyên tính toán và thời gian thực hiện liên kết nhiều bảng (JOINs), làm giảm tốc độ đọc dữ liệu.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy giải thích hiện tượng "Cache Stampede" (hay còn gọi là hiện tượng thủng kho bộ đệm) xảy ra do nguyên nhân gì và nêu một phương pháp kỹ thuật xử lý ở Backend.
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên nhân do từ khóa dữ liệu hot bị hết hạn đồng thời (Hot Key Expiration)
    keypoint_weight: 0.5
    description: Xảy ra khi một key dữ liệu có lượng truy cập cực kỳ lớn (Hot Key) bất ngờ bị hết hạn trong Cache. Tại khoảnh khắc đó, hàng vạn request đọc song song đồng loạt bị Cache Miss và tràn thẳng xuống Database gốc để lấy dữ liệu, gây quá tải sập hệ thống DB.
  - id: KP6_2
    content: Giải pháp sử dụng cơ chế Khóa hoặc ngẫu nhiên hóa thời gian sống (Mutex Lock / Jitter)
    keypoint_weight: 0.5
    description: Áp dụng Mutex Lock (chỉ cho phép request đầu tiên xuống DB lấy dữ liệu và cập nhật lại cache, các request khác phải đợi); hoặc cấu hình thời gian hết hạn ngẫu nhiên (Jitter/Random TTL) cho các key để tránh việc chúng bị xóa bỏ đồng thời.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt về mặt cơ chế hoạt động mạng và ngữ cảnh áp dụng hiệu quả giữa phương pháp giao tiếp thời gian thực WebSockets và phương pháp Polling truyền thống là gì?
* **expected_key_points:**
  - id: KP7_1
    content: Cơ chế kết nối duy nhất hai chiều của WebSockets (Full-duplex)
    keypoint_weight: 0.5
    description: WebSockets thiết lập một kết nối TCP duy nhất và duy trì trạng thái sống vĩnh viễn (Persistent connection). Cả Client và Server đều có thể chủ động đẩy dữ liệu cho nhau bất cứ lúc nào (Full-duplex), phù hợp cho ứng dụng chat, chứng khoán.
  - id: KP7_2
    content: Cơ chế gửi request lặp lại liên tục định kỳ của Polling
    keypoint_weight: 0.5
    description: Polling bắt Client phải liên tục gửi các HTTP Request định kỳ theo khoảng thời gian cố định để hỏi Server xem có dữ liệu mới hay không. Phương pháp này gây lãng phí tài nguyên băng thông mạng và tạo ra độ trễ (Latency).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong kiến trúc hệ thống phân tán hoặc Microservices, tại sao mô hình giao dịch "Two-Phase Commit" (2PC) lại gặp khó khăn về mặt mở rộng hiệu năng hệ thống? Kiến trúc "Saga Pattern" giải quyết bài toán giao dịch phân tán dựa trên nguyên lý nào?
* **expected_key_points:**
  - id: KP8_1
    content: Khuyết điểm nghẽn mạch khóa đồng bộ và nguy cơ Deadlock của mô hình 2PC
    keypoint_weight: 0.4
    description: 2PC là cơ chế đồng bộ (Synchronous), yêu cầu node điều phối trung tâm phải khóa (Lock) tài nguyên trên tất cả các dịch vụ tham gia xuyên suốt hai giai đoạn. Nếu một dịch vụ phản hồi chậm hoặc mất mạng, toàn bộ hệ thống sẽ bị treo luồng tính toán lãng phí tài nguyên và dễ xảy ra Deadlock.
  - id: KP8_2
    content: Nguyên lý chuỗi giao dịch cục bộ độc lập tuần tự của cấu trúc Saga
    keypoint_weight: 0.3
    description: Saga chuyển đổi giao dịch phân tán thành một chuỗi các giao dịch nội bộ độc lập tuần tự trên từng service. Mỗi service thực hiện xong phần việc của mình sẽ commit dữ liệu ngay lập tức và phát ra một Sự kiện (Event/Message) để kích hoạt service tiếp theo chạy.
  - id: KP8_3
    content: Cơ chế thực thi giao dịch bù hoàn tác dữ liệu khi xảy ra lỗi (Compensating Transactions)
    keypoint_weight: 0.3
    description: Saga là kiến trúc phi đồng bộ chấp nhận tính nhất quán muộn (Eventual Consistency). Nếu một bước trong chuỗi bị lỗi, Saga sẽ tự động kích hoạt một loạt các giao dịch bù (Compensating Transactions) chạy ngược lại để hoàn tác dữ liệu, đưa hệ thống về trạng thái cân bằng mà không cần dùng đến lệnh khóa tài nguyên diện rộng.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Khi thiết kế một hệ thống lưu trữ có thông lượng ghi cực kỳ lớn (High-throughput Write Operations), tại sao cấu trúc lưu trữ dựa trên cây LSM-Tree (Log-Structured Merge-Tree) lại vượt trội hơn cấu trúc cây B-Tree truyền thống? Hãy giải thích quy trình ghi dữ liệu của LSM-Tree.
* **expected_key_points:**
  - id: KP9_1
    content: Tận dụng cơ chế ghi tuần tự liên tục thay vì ghi ngẫu nhiên trên đĩa
    keypoint_weight: 0.4
    description: B-Tree thực hiện cập nhật dữ liệu trực tiếp trên các trang đĩa tại các vị trí rải rác, tạo ra các phép toán ghi ngẫu nhiên (Random Writes) rất chậm. LSM-Tree chuyển đổi mọi thao tác ghi thành phép ghi tuần tự nối đuôi liên tục (Sequential Writes) vào bộ nhớ nền, tăng tốc độ ghi lên hàng trăm lần.
  - id: KP9_2
    content: Quy trình ghi dữ liệu qua hai tầng lưu trữ MemTable và file SSTable
    keypoint_weight: 0.4
    description: Dữ liệu mới ghi vào sẽ được nạp trực tiếp vào một cấu trúc dữ liệu cây trên bộ nhớ RAM gọi là MemTable (đồng thời ghi vào file Log WAL phòng sự cố). Khi MemTable đầy, nó sẽ được đóng băng và ghi súc (Flush) tuần tự xuống ổ đĩa cứng thành các file tĩnh đã sắp xếp thứ tự gọi là SSTable (Sorted String Table).
  - id: KP9_3
    content: Tiến trình dọn dẹp chạy ngầm gộp file Compaction
    keypoint_weight: 0.2
    description: Do dữ liệu được ghi nối đuôi liên tục nên sẽ tồn tại nhiều phiên bản cũ của cùng một key dữ liệu nằm rải rác trên các file SSTable. LSM-Tree sử dụng tiến trình chạy ngầm gọi là Compaction để liên tục gộp, loại bỏ dữ liệu trùng lặp/đã xóa và sắp xếp lại các file SSTable theo các phân tầng (Levels).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích nguyên lý hoạt động kỹ thuật của thuật toán định tuyến "Consistent Hashing" (Băm nhất quán) dùng trong thiết kế cụm Caching phân tán. Thuật toán này giải quyết triệt để lỗi gì của phép băm Modulo truyền thống khi thay đổi số lượng Node?
* **expected_key_points:**
  - id: KP10_1
    content: Lỗi mất dấu dữ liệu hàng loạt của phép toán băm Modulo ($h(x) \pmod N$)
    keypoint_weight: 0.4
    description: Phép băm Modulo truyền thống xác định vị trí node lưu trữ dựa trên tổng số lượng node $N$. Khi ta thực hiện thêm một node mới hoặc một node bị sập ($N$ thay đổi), kết quả băm của hầu hết các key cũ bị thay đổi lập tức, dẫn đến hiện tượng mất dấu dữ liệu hàng loạt (Cache Miss diện rộng) làm sập hệ thống.
  - id: KP10_2
    content: Nguyên lý ánh xạ không gian khóa và địa chỉ node lên vòng tròn logic (Hash Ring)
    keypoint_weight: 0.4
    description: Consistent Hashing băm cả Key dữ liệu lẫn Địa chỉ các Node vật lý về cùng một không gian số thực lớn nằm trên một vòng tròn logic gọi là Hash Ring. Vị trí lưu trữ của Key được xác định bằng cách di chuyển theo chiều kim đồng hồ từ điểm băm của key cho đến khi gặp Node đầu tiên xuất hiện. Khi thêm/bớt node, hệ thống chỉ cần phân phối chuyển dịch một lượng rất nhỏ số key nằm sát node đó mà không ảnh hưởng toàn cục.
  - id: KP10_3
    content: Kỹ thuật sử dụng Node ảo (Virtual Nodes / Vnodes) để cân bằng tải chia đều dữ liệu
    keypoint_weight: 0.2
    description: Nếu số lượng node vật lý quá ít, các node dễ phân bổ không đều trên vòng tròn logic, dẫn đến hiện tượng một node phải gánh lượng dữ liệu quá lớn (Hotspot node). Thuật toán giải quyết bằng cách tạo ra nhiều Node ảo (Virtual Nodes) đại diện cho một node vật lý băm rải rác khắp vòng tròn để chia đều dữ liệu.