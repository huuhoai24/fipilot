# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 1)

* **Role:** Backend Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong phát triển Backend, hãy phân biệt điểm khác biệt cơ bản về mục đích sử dụng và tính chất lưu trữ giữa biến Local (Cục bộ) và biến Global (Toàn cục).
* **expected_key_points:**
  - id: KP1_1
    content: Phạm vi truy cập (Scope) và Vị trí khai báo
    keypoint_weight: 0.5
    description: Biến Local được khai báo bên trong một hàm hoặc block code, chỉ có thể truy cập từ bên trong hàm đó. Biến Global được khai báo ngoài mọi hàm, có thể truy cập từ bất kỳ vị trí nào trong toàn bộ mã nguồn chương trình.
  - id: KP1_2
    content: Vòng đời dữ liệu (Lifecycle) và vùng nhớ cấp phát
    keypoint_weight: 0.5
    description: Biến Local sinh ra khi hàm được gọi và lập tức bị giải phóng khỏi Stack khi hàm kết thúc. Biến Global tồn tại xuyên suốt vòng đời chạy của ứng dụng, tiêu tốn không gian bộ nhớ lâu dài và dễ gây ra lỗi khó debug (Side effects).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Khi viết câu lệnh truy vấn dữ liệu SQL, mệnh đề `WHERE` và mệnh đề `HAVING` khác nhau như thế nào về thứ tự thực thi và logic lọc dữ liệu?
* **expected_key_points:**
  - id: KP2_1
    content: Logic và đối tượng lọc dữ liệu của WHERE
    keypoint_weight: 0.5
    description: Mệnh đề WHERE thực hiện lọc trực tiếp trên từng hàng dữ liệu thô (Raw rows) trước khi các phép toán gộp nhóm (GROUP BY) được diễn ra. WHERE không thể đi kèm với các hàm gộp (Aggregate functions).
  - id: KP2_2
    content: Logic và đối tượng lọc dữ liệu của HAVING
    keypoint_weight: 0.5
    description: Mệnh đề HAVING thực hiện lọc dữ liệu sau khi dữ liệu đã được gộp nhóm bởi GROUP BY. HAVING làm việc trực tiếp trên các kết quả của nhóm và thường xuyên sử dụng kết hợp với các hàm gộp (như SUM, COUNT, AVG).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế cơ sở dữ liệu quan hệ (RDBMS), ràng buộc "Unique Constraint" đóng vai trò logic gì và nó khác gì so với thuộc tính "Primary Key"?
* **expected_key_points:**
  - id: KP3_1
    content: Ý nghĩa logic của Unique Constraint
    keypoint_weight: 0.5
    description: Đảm bảo tất cả các giá trị trong cột (hoặc tổ hợp cột) đó phải duy nhất, không được trùng lặp giữa các hàng dữ liệu trong bảng.
  - id: KP3_2
    content: Phân biệt khả năng chứa giá trị NULL và số lượng giới hạn
    keypoint_weight: 0.5
    description: Một bảng chỉ được phép có duy nhất 1 Primary Key và cột đó tuyệt đối không được phép chứa giá trị NULL. Trong khi đó, một bảng có thể cấu hình nhiều Unique Constraint độc lập và cột Unique vẫn được phép chứa giá trị NULL (tùy thuộc vào RDBMS).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong bộ nguyên lý thiết kế SOLID, hãy giải thích ý nghĩa logic kỹ thuật của nguyên lý "L" - Liskov Substitution Principle (Nguyên lý thay thế Liskov).
* **expected_key_points:**
  - id: KP4_1
    content: Quy tắc thay thế đối tượng không làm thay đổi tính đúng đắn của chương trình
    keypoint_weight: 0.5
    description: Quy định các đối tượng thuộc lớp con (Subclass) phải có khả năng thay thế hoàn toàn cho đối tượng của lớp cha (Superclass) mà không làm thay đổi hay phá vỡ tính đúng đắn logic của hệ thống.
  - id: KP4_2
    content: Dấu hiệu vi phạm qua hành vi thay đổi kỳ vọng (Ném ngoại lệ)
    keypoint_weight: 0.5
    description: Vi phạm xảy ra khi lớp con ghi đè một hàm của lớp cha nhưng lại ném ra một ngoại lệ không mong muốn (ví dụ: NotImplementedException), hoặc thu hẹp/làm rỗng logic xử lý, ép Client phải dùng phép kiểm tra kiểu dữ liệu trước khi gọi hàm.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi sử dụng các công cụ ORM (Object-Relational Mapping), hãy phân biệt cơ chế hoạt động, ưu điểm và nhược điểm của hai chiến lược tải dữ liệu liên quan: Eager Loading và Lazy Loading.
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế lấy dữ liệu đồng thời của Eager Loading
    keypoint_weight: 0.5
    description: Eager Loading tự động truy vấn và tải toàn bộ dữ liệu quan hệ liên quan (cha và con) ngay trong câu lệnh đầu tiên thông qua phép JOIN. Giúp triệt tiêu lỗi N+1 Query, nhưng tiêu tốn RAM và làm chậm câu lệnh nếu dữ liệu con khổng lồ mà không dùng đến.
  - id: KP5_2
    content: Cơ chế trì hoãn tải dữ liệu của Lazy Loading
    keypoint_weight: 0.5
    description: Lazy Loading trì hoãn việc tải dữ liệu con; dữ liệu con chỉ thực sự được gọi truy vấn từ DB khi mã nguồn Backend truy cập trực tiếp vào thuộc tính của nó. Tiết kiệm tài nguyên ban đầu nhưng dễ phát sinh lỗi N+1 Query nếu gọi lặp trong vòng lặp.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Lỗ hổng bảo mật logic API "Broken Object Level Authorization" (BOLA / IDOR) xảy ra do lỗi lập trình nào ở Backend và giải pháp xử lý triệt để là gì?
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên nhân thiếu kiểm tra quyền sở hữu đối với tài nguyên cụ thể (Object Check)
    keypoint_weight: 0.5
    description: Xảy ra khi Backend đã xác thực thành công danh tính người dùng (Authentication), nhưng tại Endpoint xử lý lại tin tưởng hoàn toàn vào ID tài nguyên do Client truyền lên mà không kiểm tra xem người dùng hiện tại có quyền sở hữu hoặc thao tác trên tài nguyên cụ thể đó hay không.
  - id: KP6_2
    content: Giải pháp phòng chống bằng cách tích hợp truy vấn phân quyền dựa trên User Context
    keypoint_weight: 0.5
    description: Tại mỗi logic xử lý API liên quan đến ID tài nguyên, Backend bắt buộc phải trích xuất User ID an toàn từ Session/Token bảo mật, sau đó thực hiện câu lệnh truy vấn đối chiếu quyền hạn thực tế trên bản ghi dữ liệu yêu cầu trước khi trả về kết quả.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong quy trình phát triển và vận hành hệ thống, công cụ "Database Migration" đóng vai trò quản lý gì trong mô hình làm việc nhóm (Teamwork)?
* **expected_key_points:**
  - id: KP7_1
    content: Quản lý phiên bản cho cấu trúc cơ sở dữ liệu (Version Control for DB)
    keypoint_weight: 0.5
    description: Migration lưu trữ các thay đổi về cấu trúc Database (tạo bảng, thêm cột, sửa kiểu dữ liệu) dưới dạng các file mã nguồn có thứ tự thời gian, giúp theo dõi và quản lý lịch sử biến đổi của DB giống như Git quản lý mã nguồn.
  - id: KP7_2
    content: Đồng bộ hóa tính nhất quán môi trường tự động (CI/CD)
    keypoint_weight: 0.5
    description: Giúp tất cả lập trình viên trong đội ngũ và các môi trường chạy thử, môi trường thật (Staging, Production) dễ dàng đồng bộ cấu trúc DB một cách chính xác bằng câu lệnh tự động, tránh việc sửa tay gây sai lệch dữ liệu.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Khi xây dựng hệ thống phân tán đa máy chủ, định lý "CAP Theorem" khẳng định điều gì về sự đánh đổi kỹ thuật khi hiện tượng lỗi phân đoạn mạng (Network Partition) xảy ra?
* **expected_key_points:**
  - id: KP8_1
    content: Giới hạn tối đa 2 trên 3 yếu tố của hệ thống phân tán
    keypoint_weight: 0.4
    description: Khẳng định một hệ thống dữ liệu phân tán chỉ có thể đáp ứng tối đa 2 trong 3 tính chất tại một thời điểm: Nhất quán dữ liệu (C - Consistency), Sẵn sàng phản hồi (A - Availability), và Chịu lỗi phân đoạn mạng (P - Partition Tolerance).
  - id: KP8_2
    content: Tính bắt buộc của yếu tố P trong môi trường mạng thực tế
    keypoint_weight: 0.2
    description: Môi trường mạng vật lý luôn tiềm ẩn rủi ro mất kết nối hoặc đứt cáp giữa các Node (Network Partition), nên yếu tố P là bắt buộc phải lựa chọn trong thiết kế hệ thống phân tán thực tế.
  - id: KP8_3
    content: Sự đánh đổi bắt buộc giữa cấu trúc CP và AP khi xảy ra sự cố mạng
    keypoint_weight: 0.4
    description: Khi có lỗi mạng, hệ thống buộc phải chọn: Hoặc bảo toàn Consistency (Mô hình CP) bằng cách từ chối request để tránh sai lệch dữ liệu giữa các node; Hoặc bảo toàn Availability (Mô hình AP) bằng cách chấp nhận phản hồi dữ liệu cũ/sai lệch từ các node bị cô lập để hệ thống luôn sẵn sàng sống.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích cấu trúc toán học logic và nguyên lý hoạt động của cấu trúc dữ liệu Bloom Filter. Tại sao nó được ứng dụng làm bộ lọc chặn trước Database lớn?
* **expected_key_points:**
  - id: KP9_1
    content: Nguyên lý mảng Bit toán học và tập hợp hàm băm độc lập (Probabilistic Structure)
    keypoint_weight: 0.4
    description: Bloom Filter sử dụng một mảng bit ban đầu bằng 0 và $k$ hàm băm độc lập. Khi nạp phần tử, chuỗi qua $k$ hàm băm để tìm vị trí và chuyển bit thành 1. Khi kiểm tra, nếu có ít nhất một vị trí bit bằng 0, phần tử chắc chắn 100% chưa tồn tại (Không bao giờ có lỗi False Negative).
  - id: KP9_2
    content: Ứng dụng tối ưu hóa hiệu năng đọc và đánh chặn truy vấn lãng phí (Chặn Cache Penetration)
    keypoint_weight: 0.4
    description: Đặt Bloom Filter nằm trước Database. Khi nhận request tìm kiếm ID, hệ thống kiểm tra qua Bloom Filter trước; nếu trả về "Không tồn tại", Backend phản hồi lỗi ngay lập tức mà không cần tốn chi phí thực hiện câu lệnh truy vấn đọc đĩa cứng IO của Database, giúp bảo vệ DB khỏi các cuộc tấn công quét ID rác.
  - id: KP9_3
    content: Đánh đổi rủi ro xảy ra hiện tượng False Positive (Dương tính giả)
    keypoint_weight: 0.2
    description: Do xung đột băm (Collision), Bloom Filter có xác suất nhỏ báo một phần tử "đã tồn tại" dù thực tế chưa có. Khi đó request vẫn xuống DB tìm kiếm (trả về rỗng), hệ thống chấp nhận sự đánh đổi này để đổi lấy tốc độ và không gian nhớ cực nhỏ $O(1)$.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong thiết kế kiến trúc Microservices hướng sự kiện (Event-Driven Architecture), hãy giải thích nguyên lý hoạt động kỹ thuật và mục đích sử dụng của mẫu thiết kế "Transactional Outbox Pattern".
* **expected_key_points:**
  - id: KP10_1
    content: Giải quyết bài toán không đồng bộ giữa ghi DB nội bộ và bắn Message Broker
    keypoint_weight: 0.4
    description: Đảm bảo tính toàn vẹn dữ liệu khi một Service cần đồng thời thực hiện hai hành động: Cập nhật Database nội bộ của riêng nó và gửi một sự kiện (Event) sang Message Broker (như Kafka). Nếu không có mẫu thiết kế này, một trong hai hành động lỗi sẽ gây mất đồng bộ hệ thống.
  - id: KP10_2
    content: Cơ chế sử dụng bảng Outbox trung gian trong cùng một Database Transaction
    keypoint_weight: 0.4
    description: Thay vì gửi trực tiếp sự kiện sang Message Broker trong lúc xử lý, Service sẽ lưu thông tin sự kiện đó dưới dạng một bản ghi vào một bảng trung gian gọi là bảng `Outbox` nằm ngay trong cùng một giao dịch cơ sở dữ liệu (Database Transaction) của nghiệp vụ chính. Điều này đảm bảo cả hai hành động ghi dữ liệu nghiệp vụ và ghi sự kiện đều cùng thành công hoặc cùng thất bại (ACID).
  - id: KP10_3
    content: Tiến trình quét độc lập chuyển tiếp sự kiện