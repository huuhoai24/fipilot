# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 1)

* **Role:** Backend Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong kiến trúc Web, cookie và session khác nhau như thế nào về vị trí lưu trữ và mục đích sử dụng cơ bản?
* **expected_key_points:**
  - id: KP1_1
    content: Vị trí lưu trữ dữ liệu (Storage Location)
    keypoint_weight: 0.5
    description: Cookie được lưu trữ trực tiếp tại trình duyệt của người dùng (Client-side). Session được lưu trữ và quản lý an toàn trên máy chủ (Server-side).
  - id: KP1_2
    content: Mục đích sử dụng và tính bảo mật (Security & Purpose)
    keypoint_weight: 0.5
    description: Cookie thường dùng để lưu tùy chọn giao diện, ghi nhớ đăng nhập và có tính bảo mật thấp hơn. Session dùng để lưu trạng thái phiên làm việc nhạy cảm (nhũ thông tin đăng nhập, giỏ hàng) và có độ bảo mật cao hơn do Client không thể chỉnh sửa trực tiếp dữ liệu gốc.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt điểm khác nhau về mặt logic hoạt động và kết quả trả về giữa hai mệnh đề liên kết bảng `INNER JOIN` và `LEFT JOIN` trong SQL.
* **expected_key_points:**
  - id: KP2_1
    content: Cơ chế hoạt động của INNER JOIN
    keypoint_weight: 0.5
    description: Chỉ trả về các bản ghi có giá trị khớp nhau ở cả hai bảng dựa trên điều kiện liên kết; các hàng không khớp ở một trong hai bảng sẽ bị loại bỏ hoàn toàn.
  - id: KP2_2
    content: Cơ chế hoạt động của LEFT JOIN
    keypoint_weight: 0.5
    description: Trả về toàn bộ các bản ghi của bảng bên trái (Left table) bất kể có khớp hay không, và điền giá trị `NULL` vào các cột tương ứng của bảng bên phải nếu không tìm thấy bản ghi trùng khớp.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Mạng trạng thái phản hồi HTTP (HTTP Status Codes) nhóm 2xx, 4xx và 5xx đại diện cho các tình huống logic chung nào trong giao tiếp mạng?
* **expected_key_points:**
  - id: KP3_1
    content: Ý nghĩa nhóm mã 2xx và 4xx
    keypoint_weight: 0.6
    description: 2xx biểu thị yêu cầu được tiếp nhận và xử lý thành công (ví dụ: 200 OK, 201 Created). 4xx biểu thị lỗi từ phía Client do gửi sai cú pháp, thiếu quyền truy cập hoặc sai tài nguyên (ví dụ: 400 Bad Request, 404 Not Found).
  - id: KP3_2
    content: Ý nghĩa nhóm mã 5xx
    keypoint_weight: 0.4
    description: 5xx biểu thị lỗi từ phía Server, khi máy chủ Backend gặp trục trặc nội bộ hoặc không thể hoàn thành một yêu cầu hoàn toàn hợp lệ từ Client (ví dụ: 500 Internal Server Error).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong bộ nguyên lý SOLID, chữ cái "D" đại diện cho nguyên lý Dependency Inversion Principle (Đảo ngược phụ thuộc). Nguyên lý này quy định quy tắc thiết kế mã nguồn như thế nào?
* **expected_key_points:**
  - id: KP4_1
    content: Module cấp cao không phụ thuộc module cấp thấp
    keypoint_weight: 0.5
    description: Các module tầng logic cao (High-level modules) không được phụ thuộc trực tiếp vào các chi tiết triển khai cụ thể của module tầng thấp (Low-level modules). Cả hai đều phải phụ thuộc vào sự trừu tượng (Abstractions).
  - id: KP4_2
    content: Sự trừu tượng không phụ thuộc vào chi tiết
    keypoint_weight: 0.5
    description: Abstractions (như Interface hoặc Abstract Class) không được phụ thuộc vào chi tiết triển khai (Details/Concrete Classes). Ngược lại, chi tiết triển khai phải phụ thuộc vào sự trừu tượng. Kỹ thuật này giúp giảm sự phụ thuộc cứng (Loose Coupling).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi xây dựng các ứng dụng có nhiều người dùng đồng thời, hiện tượng Race Condition là gì và lập trình viên Backend thường dùng giải pháp gì để kiểm soát hiện tượng này ở cấp độ Database?
* **expected_key_points:**
  - id: KP5_1
    content: Bản chất bất đồng bộ gây tranh chấp tài nguyên (Race Condition)
    keypoint_weight: 0.5
    description: Xảy ra khi nhiều luồng (Threads/Processes) hoặc yêu cầu song song cùng truy cập và cố gắng sửa đổi một tài nguyên dữ liệu dùng chung tại cùng một thời điểm, dẫn đến kết quả dữ liệu cuối cùng bị sai lệch không nhất quán.
  - id: KP5_2
    content: Các giải pháp khóa dữ liệu (Pessimistic Locking & Optimistic Locking)
    keypoint_weight: 0.5
    description: Sử dụng Pessimistic Locking (Khóa bi quan - dùng `SELECT ... FOR UPDATE` để chặn các tiến trình khác đọc/ghi cho đến khi hoàn thành transaction) hoặc Optimistic Locking (Khóa lạc quan - sử dụng cột `version` hoặc `timestamp` để kiểm tra xung đột dữ liệu tại thời điểm commit).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Lỗ hổng bảo mật "Broken Object Level Authorization" (BOLA / IDOR) trong thiết kế API Backend xảy ra do lỗi logic nào và hướng khắc phục là gì?
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên nhân do thiếu kiểm tra quyền sở hữu đối tượng (Access Control Check)
    keypoint_weight: 0.5
    description: Xảy ra khi Backend chỉ kiểm tra xem người dùng đã đăng nhập hay chưa (Authentication), nhưng lại bỏ quên việc kiểm tra xem người dùng đó có thực sự sở hữu hoặc có quyền thao tác trên ID đối tượng cụ thể được gửi lên trong request hay không (ví dụ: sửa ID trên URL để xem hóa đơn người khác).
  - id: KP6_2
    content: Giải pháp thiết lập quy trình kiểm tra quyền hạn chặt chẽ
    keypoint_weight: 0.5
    description: Tại mỗi API endpoint xử lý dữ liệu theo ID, Backend bắt buộc phải chạy câu lệnh kiểm tra (Authorization query) để xác thực ID của người dùng hiện tại (lấy từ session/token) có quyền sở hữu đối với ID tài nguyên yêu cầu hay không trước khi thực thi nghiệp vụ.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Khái niệm "Connection Pooling" (như Database Connection Pool) giải quyết bài toán hiệu năng nào cho hệ thống Backend?
* **expected_key_points:**
  - id: KP7_1
    content: Chi phí tài nguyên và thời gian khởi tạo kết nối liên tục
    keypoint_weight: 0.5
    description: Việc liên tục mở và đóng kết nối TCP/IP tới Database cho mỗi request của người dùng tiêu tốn rất nhiều tài nguyên CPU, bộ nhớ của máy chủ và gây ra độ trễ (Latency) lớn cho hệ thống.
  - id: KP7_2
    content: Cơ chế tái sử dụng các kết nối có sẵn (Pool)
    keypoint_weight: 0.5
    description: Connection Pool duy trì sẵn một số lượng kết nối cố định chạy ngầm. Khi Backend cần truy vấn, nó mượn một kết nối rảnh trong pool để dùng và trả lại ngay sau khi xong tác vụ thay vì đóng kết nối, giúp triệt tiêu chi phí khởi tạo và tăng tốc độ xử lý request.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Khi thực hiện câu lệnh kiểm tra xem dữ liệu đã tồn tại hay chưa trong một tập dữ liệu khổng lồ (hàng tỷ bản ghi), cấu trúc dữ liệu Bloom Filter hoạt động dựa trên nguyên lý toán học nào? Hãy phân tích rủi ro về mặt False Positive và False Negative của cấu trúc này.
* **expected_key_points:**
  - id: KP8_1
    content: Nguyên lý mảng Bit và hàm băm độc lập (Probabilistic Data Structure)
    keypoint_weight: 0.4
    description: Bloom Filter sử dụng một mảng bit kích hoạt ban đầu bằng 0 và $k$ hàm băm độc lập. Khi thêm một phần tử, phần tử đó đi qua $k$ hàm băm để tìm ra các vị trí chỉ số mảng và chuyển các bit tại đó thành 1. Khi kiểm tra, nếu có bất kỳ bit nào trong số $k$ vị trí bằng 0, phần tử chắc chắn chưa tồn tại.
  - id: KP8_2
    content: Hiện tượng xác suất xảy ra False Positive (Dương tính giả)
    keypoint_weight: 0.4
    description: Do hiện tượng xung đột băm (Collision), nhiều phần tử khác nhau có thể vô tình bật chung các vị trí bit lên 1. Vì vậy, Bloom Filter có thể trả về kết quả phần tử đã tồn tại dù thực tế chưa có (False Positive). Lập trình viên phải chấp nhận sự đánh đổi này để đổi lấy tốc độ và không gian nhớ cực nhỏ $O(1)$.
  - id: KP8_3
    content: Đảm bảo tuyệt đối không có False Negative (Âm tính giả)
    keypoint_weight: 0.2
    description: Bloom Filter cam kết tuyệt đối không bao giờ xảy ra lỗi False Negative. Nếu cấu trúc dữ liệu báo phần tử "không tồn tại" (tức là có ít nhất một vị trí bit bằng 0), kết quả đó chính xác 100%.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong Cơ sở dữ liệu quan hệ (RDBMS), hãy phân biệt sự khác nhau về mặt logic hiển thị dữ liệu và mức độ khóa tài nguyên giữa ba mức độ cô lập giao dịch (Transaction Isolation Levels): Read Committed, Repeatable Read, và Serializable.
* **expected_key_points:**
  - id: KP9_1
    content: Logic và lỗi của Read Committed và Repeatable Read
    keypoint_weight: 0.5
    description: Read Committed chỉ đọc được dữ liệu đã commit chính thức, tránh được Dirty Read nhưng vẫn gặp lỗi Non-repeatable Read (dữ liệu thay đổi nếu đọc lại trong cùng 1 transaction). Repeatable Read khóa các hàng được đọc để đảm bảo đọc lại luôn ra kết quả cũ, giải quyết được Non-repeatable Read nhưng vẫn có thể gặp hiện tượng Phantom Read (xuất hiện hàng mới do transaction khác chèn vào).
  - id: KP9_2
    content: Bản chất khóa nghiêm ngặt nhất của Serializable
    keypoint_weight: 0.5
    description: Serializable cung cấp mức độ cô lập cao nhất bằng cách bắt các giao dịch thực thi tuần tự hoàn toàn hoặc áp dụng Range-locks/Predicate-locks trên toàn bộ vùng dữ liệu truy vấn. Nó ngăn chặn tuyệt đối tất cả các lỗi đồng thời (kể cả Phantom Read) nhưng làm giảm mạnh hiệu năng xử lý song song và dễ gây ra hiện tượng nghẽn mạch Deadlock.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích nguyên lý hoạt động kỹ thuật của cơ chế Rate Limiting sử dụng giải pháp thuật toán Token Bucket (Thùng thẻ bài). Thuật toán này xử lý tình huống lưu lượng truy cập tăng đột biến (Bursting traffic) như thế nào?
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế tích lũy thẻ bài theo thời gian cố định
    keypoint_weight: 0.4
    description: Một chiếc thùng có dung lượng lưu trữ tối đa là $B$ tokens. Hệ thống tự động nạp thêm tokens vào thùng với một tốc độ không đổi là $R$ tokens mỗi giây. Nếu thùng đầy, tokens nạp thêm sẽ bị tràn và bỏ qua.
  - id: KP10_2
    content: Logic kiểm tra và tiêu thụ token của mỗi Request
    keypoint_weight: 0.3
    description: Khi có một request gửi đến, hệ thống kiểm tra xem trong thùng còn token hay không. Nếu còn, request được cấp phép xử lý đồng thời thùng bị trừ đi 1 token. Nếu thùng trống rỗng (0 token), request sẽ bị từ chối lập tức và trả về mã lỗi HTTP 429 Too Many Requests.
  - id: KP10_3
    content: Khả năng xử lý thông minh lưu lượng tăng đột biến (Burst Capacity)
    keypoint_weight: 0.3
    description: Thuật toán này vượt trội nhờ cho phép hệ thống chịu được các đợt lưu lượng phình to đột biến (Bursting Traffic). Nếu hệ thống đang rảnh rỗi, thùng sẽ tích lũy đầy $B$ tokens. Khi có một đợt bùng nổ truy cập diễn ra cùng lúc, hệ thống có thể xử lý mượt mà tối đa đúng $B$ requests ngay lập tức trước khi bắt đầu áp dụng giới hạn chặt chẽ theo tốc độ $R$.