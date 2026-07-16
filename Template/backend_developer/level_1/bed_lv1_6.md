# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 1)

* **Role:** Backend Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong kiến trúc phát triển ứng dụng Web, hai thành phần Cookie và Session khác nhau như thế nào về vị trí lưu trữ thông tin và mức độ bảo mật?
* **expected_key_points:**
  - id: KP1_1
    content: Khác biệt về vị trí lưu trữ (Storage Location)
    keypoint_weight: 0.5
    description: Cookie được lưu trữ trực tiếp trên trình duyệt của người dùng (Client-side). Session được khởi tạo, lưu trữ và quản lý tập trung trên máy chủ Backend (Server-side).
  - id: KP1_2
    content: Khác biệt về tính bảo mật và kiểm soát (Security Control)
    keypoint_weight: 0.5
    description: Cookie có độ bảo mật thấp hơn vì người dùng có thể can thiệp, sửa đổi hoặc bị tấn công đánh cắp. Session có độ bảo mật cao hơn do dữ liệu gốc nằm trên server, Client chỉ giữ một chuỗi định danh Session ID duy nhất để đối chiếu.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt điểm khác nhau về mặt logic tập hợp dữ liệu trả về giữa hai mệnh đề liên kết bảng `INNER JOIN` và `LEFT JOIN` trong SQL.
* **expected_key_points:**
  - id: KP2_1
    content: Logic lọc dữ liệu của INNER JOIN
    keypoint_weight: 0.5
    description: Chỉ trả về các bản ghi có giá trị trùng khớp ở cả hai bảng dựa trên điều kiện liên kết (giao giữa hai tập hợp); các hàng không khớp sẽ bị loại bỏ hoàn toàn khỏi kết quả.
  - id: KP2_2
    content: Logic giữ dữ liệu của LEFT JOIN
    keypoint_weight: 0.5
    description: Trả về toàn bộ các bản ghi thuộc bảng bên trái (Left table) bất kể có khớp hay không, và tự động điền giá trị `NULL` vào các cột tương ứng của bảng bên phải nếu không tìm thấy dữ liệu trùng khớp.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Khi xây dựng API, các mã trạng thái phản hồi HTTP (HTTP Status Codes) nhóm 2xx, 4xx và 5xx đại diện cho những tình huống logic kỹ thuật nào?
* **expected_key_points:**
  - id: KP3_1
    content: Ý nghĩa nhóm mã thành công 2xx và nhóm lỗi phía Client 4xx
    keypoint_weight: 0.6
    description: 2xx biểu thị yêu cầu được tiếp nhận và xử lý thành công (ví dụ: 200 OK, 201 Created). 4xx biểu thị lỗi từ phía Client gửi lên do sai cú pháp, thiếu quyền hoặc sai tài nguyên (ví dụ: 400 Bad Request, 404 Not Found).
  - id: KP3_2
    content: Ý nghĩa nhóm lỗi phía máy chủ 5xx
    keypoint_weight: 0.4
    description: 5xx biểu thị lỗi từ phía hệ thống máy chủ Backend gặp trục trặc nội bộ hoặc không thể xử lý một yêu cầu hoàn toàn hợp lệ từ Client (ví dụ: 500 Internal Server Error).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong các nguyên lý thiết kế SOLID, chữ cái "D" đại diện cho nguyên lý Dependency Inversion Principle (Đảo ngược phụ thuộc). Nguyên lý này quy định quy tắc viết code như thế nào?
* **expected_key_points:**
  - id: KP4_1
    content: Module cấp cao không phụ thuộc trực tiếp vào module cấp thấp
    keypoint_weight: 0.5
    description: Các module tầng logic nghiệp vụ cao (High-level) không được phụ thuộc trực tiếp vào các module triển khai chi tiết kỹ thuật ở tầng thấp (Low-level). Cả hai đều phải phụ thuộc vào sự trừu tượng.
  - id: KP4_2
    content: Sự trừu tượng không phụ thuộc vào chi tiết triển khai
    keypoint_weight: 0.5
    description: Sự trừu tượng (như Interface/Abstract Class) không được phụ thuộc vào chi tiết. Ngược lại, các chi tiết triển khai cụ thể (Concrete classes) phải phụ thuộc vào sự trừu tượng để giảm liên kết cứng (Loose Coupling).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi hệ thống tiếp nhận nhiều yêu cầu ghi dữ liệu đồng thời (Concurrent Write Requests), hiện tượng Race Condition là gì? Hãy nêu hai giải pháp khóa dữ liệu ở cấp độ Database để kiểm soát lỗi này.
* **expected_key_points:**
  - id: KP5_1
    content: Bản chất tranh chấp dữ liệu bất đồng bộ (Race Condition)
    keypoint_weight: 0.4
    description: Xảy ra khi nhiều luồng hoặc tiến trình song song cùng truy cập và cố gắng sửa đổi một tài nguyên dữ liệu dùng chung tại cùng một thời điểm, dẫn đến kết quả dữ liệu cuối cùng bị sai lệch, không nhất quán.
  - id: KP5_2
    content: Cơ chế của Pessimistic Locking (Khóa bi quan)
    keypoint_weight: 0.3
    description: Khóa cứng bản ghi ngay khi dòng code đọc dữ liệu chạy (ví dụ dùng `SELECT ... FOR UPDATE`), chặn toàn bộ các tiến trình khác không cho đọc/ghi cho đến khi giao dịch hiện tại hoàn thành (Commit/Rollback).
  - id: KP5_3
    content: Cơ chế của Optimistic Locking (Khóa lạc quan)
    keypoint_weight: 0.3
    description: Không khóa tài nguyên trong lúc đọc, nhưng khi ghi dữ liệu (`UPDATE`) sẽ kiểm tra một cột trạng thái như `version` hoặc `timestamp`. Nếu version đã bị tiến trình khác thay đổi trước đó, hệ thống từ chối commit và thực hiện rollback.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Lỗ hổng bảo mật API nghiêm trọng "Broken Object Level Authorization" (BOLA / IDOR) xảy ra do lỗi logic nào ở Backend và giải pháp phòng chống là gì?
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên nhân do thiếu kiểm tra quyền sở hữu đối tượng (Access Control Check)
    keypoint_weight: 0.5
    description: Xảy ra khi Backend chỉ kiểm tra xem người dùng đã đăng nhập hay chưa (Authentication thành công), nhưng lại bỏ quên việc kiểm tra xem tài khoản đó có thực sự có quyền sở hữu hoặc có quyền thao tác trên ID của tài nguyên cụ thể gửi lên trong request hay không.
  - id: KP6_2
    content: Giải pháp xác thực quyền hạn dựa trên ngữ cảnh người dùng hiện tại
    keypoint_weight: 0.5
    description: Tại mỗi câu lệnh xử lý API theo ID, Backend bắt buộc phải tích hợp logic kiểm tra (Authorization query), đối chiếu ID người dùng trích xuất từ Session/Token bảo mật với quyền hạn thực tế trên bản ghi dữ liệu yêu cầu trước khi thực thi.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong thiết kế hạ tầng Backend, cơ chế "Connection Pooling" (như Database Connection Pool) giải quyết bài toán hiệu năng nào cho hệ thống?
* **expected_key_points:**
  - id: KP7_1
    content: Chi phí tài nguyên của việc khởi tạo/đóng kết nối liên tục
    keypoint_weight: 0.5
    description: Việc liên tục mở và đóng kết nối TCP/IP tới Database cho mỗi request độc lập tiêu tốn rất nhiều CPU, RAM của máy chủ và tạo ra độ trễ mạng (Latency) lớn cho hệ thống.
  - id: KP7_2
    content: Cơ chế tái sử dụng các kết nối được duy trì sẵn
    keypoint_weight: 0.5
    description: Connection Pool khởi tạo và duy trì sẵn một số lượng kết nối chạy ngầm cố định. Khi Backend cần tương tác dữ liệu, nó sẽ mượn một kết nối rảnh trong pool và trả lại ngay sau khi dùng xong, triệt tiêu chi phí tạo mới kết nối.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Khi cần kiểm tra nhanh sự tồn tại của một phần tử trong tập dữ liệu khổng lồ (hàng tỷ bản ghi), cấu trúc dữ liệu xác suất Bloom Filter hoạt động theo nguyên lý toán học nào? Hãy phân tích rủi ro về mặt False Positive và False Negative của cấu trúc này.
* **expected_key_points:**
  - id: KP8_1
    content: Nguyên lý mảng Bit và tập hợp các hàm băm độc lập
    keypoint_weight: 0.4
    description: Bloom Filter sử dụng một mảng bit ban đầu bằng 0 và $k$ hàm băm độc lập. Khi nạp một phần tử, chuỗi đi qua $k$ hàm băm để tìm ra các vị trí và chuyển bit tại đó thành 1. Khi kiểm tra, nếu có ít nhất một vị trí bit bằng 0, phần tử chắc chắn chưa tồn tại.
  - id: KP8_2
    content: Rủi ro xảy ra hiện tượng False Positive (Dương tính giả)
    keypoint_weight: 0.4
    description: Do hiện tượng xung đột băm (Hash Collision), nhiều phần tử khác nhau có thể vô tình bật chung các vị trí bit lên 1. Vì vậy, Bloom Filter có thể báo phần tử "đã tồn tại" dù thực tế chưa có. Đổi lại, nó cho tốc độ tối ưu $O(1)$ và không gian nhớ cực nhỏ.
  - id: KP8_3
    content: Đảm bảo tuyệt đối không có False Negative (Âm tính giả)
    keypoint_weight: 0.2
    description: Bloom Filter cam kết tuyệt đối không bao giờ xảy ra lỗi False Negative. Nếu hệ thống báo phần tử "không tồn tại" (tức có bit bằng 0), kết quả đó chính xác 100%.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong cơ sở dữ liệu quan hệ (RDBMS), hãy phân biệt sự khác nhau về mặt logic hiển thị dữ liệu đồng thời và mức độ khóa tài nguyên giữa ba mức độ cô lập giao dịch (Transaction Isolation Levels): Read Committed, Repeatable Read, và Serializable.
* **expected_key_points:**
  - id: KP9_1
    content: Phân biệt cơ chế xử lý lỗi của Read Committed và Repeatable Read
    keypoint_weight: 0.5
    description: Read Committed chỉ đọc được dữ liệu đã commit, tránh được Dirty Read nhưng vẫn gặp lỗi Non-repeatable Read (dữ liệu bị sửa đổi nếu đọc lại trong cùng 1 transaction). Repeatable Read khóa các hàng được đọc để đảm bảo đọc lại luôn ra kết quả cũ, giải quyết được Non-repeatable Read nhưng vẫn gặp lỗi Phantom Read (xuất hiện thêm hàng mới do transaction khác chèn vào).
  - id: KP9_2
    content: Bản chất khóa nghiêm ngặt nhất của mức độ Serializable
    keypoint_weight: 0.5
    description: Serializable cung cấp mức độ cô lập cao nhất bằng cách ép các giao dịch thực thi tuần tự hoàn toàn hoặc áp dụng Range-locks/Predicate-locks trên toàn bộ vùng dữ liệu truy vấn. Nó ngăn chặn tuyệt đối tất cả các lỗi đồng thời nhưng làm giảm mạnh hiệu năng xử lý song song và rất dễ gây ra hiện tượng Deadlock.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích nguyên lý hoạt động kỹ thuật của thuật toán giới hạn băng thông Rate Limiting dùng giải pháp Token Bucket (Thùng thẻ bài). Thuật toán này xử lý tình huống lưu lượng truy cập tăng đột biến (Bursting traffic) dựa trên cơ chế nào?
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế tích lũy thẻ bài theo tốc độ cố định
    keypoint_weight: 0.4
    description: Một chiếc thùng có dung lượng lưu trữ tối đa là $B$ tokens. Hệ thống tự động nạp thêm tokens vào thùng với một tốc độ không đổi là $R$ tokens mỗi giây. Nếu thùng đầy, tokens nạp thêm sẽ bị tràn và bỏ qua.
  - id: KP10_2
    content: Logic kiểm tra và tiêu thụ token của mỗi Request
    keypoint_weight: 0.3
    description: Khi có một request gửi đến, hệ thống kiểm tra xem trong thùng còn token hay không. Nếu còn, request được cấp phép đi qua đồng thời thùng bị trừ đi 1 token. Nếu thùng trống rỗng, request sẽ bị từ chối lập tức và trả về mã lỗi HTTP 429 Too Many Requests.
  - id: KP10_3
    content: Khả năng xử lý lưu lượng phình to đột biến (Burst Capacity)
    keypoint_weight: 0.3
    description: Thuật toán này cho phép hệ thống chịu được các đợt lưu lượng phình to đột biến (Bursting Traffic). Nếu hệ thống đang rảnh rỗi, thùng sẽ tích lũy đầy $B$ tokens. Khi có một đợt bùng nổ truy cập diễn ra cùng lúc, hệ thống có thể xử lý mượt mà tối đa đúng $B$ requests ngay lập tức trước khi bắt đầu áp dụng giới hạn chặt chẽ theo tốc độ $R$.