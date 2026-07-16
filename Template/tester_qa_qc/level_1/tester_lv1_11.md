# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1) - Tập Đề Bug Priority/Severity và SQL LEFT JOIN (11)

* **Role:** Tester
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy giải thích sự khác biệt giữa Bug Severity (Mức độ nghiêm trọng) và Bug Priority (Mức độ ưu tiên). Cho ví dụ thực tế về một lỗi có Severity Cao nhưng Priority Thấp.
* **expected_key_points:**
  - id: KP1_1
    content: Phân biệt Severity và Priority
    keypoint_weight: 0.5
    description: `Severity` phản ánh mức độ ảnh hưởng của lỗi tới kỹ thuật/chức năng phần mềm. `Priority` phản ánh mức độ khẩn cấp cần sửa lỗi dựa trên góc độ kinh doanh/khách hàng.
  - id: KP1_2
    content: Ví dụ thực tế phù hợp
    keypoint_weight: 0.5
    description: Ví dụ: Lỗi crash ứng dụng khi chạy trên một dòng điện thoại cổ/hệ điều hành lỗi thời ít người dùng (Severity Cao vì gây crash, nhưng Priority Thấp vì lượng khách hàng bị ảnh hưởng rất nhỏ).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Kỹ thuật phân tích giá trị biên 2-point và 3-point khác nhau như thế nào trong thực hành thiết kế test case?
* **expected_key_points:**
  - id: KP2_1
    content: Kỹ thuật phân tích biên 2-point
    keypoint_weight: 0.5
    description: Chọn 2 giá trị cho mỗi điểm biên: chính giá trị biên (Boundary) và giá trị ngay sát ngoài biên (nhỏ hơn biên dưới 1 đơn vị hoặc lớn hơn biên trên 1 đơn vị).
  - id: KP2_2
    content: Kỹ thuật phân tích biên 3-point
    keypoint_weight: 0.5
    description: Chọn 3 giá trị cho mỗi điểm biên: chính giá trị biên, giá trị sát dưới biên và giá trị sát trên biên (ví dụ với biên 10: chọn 9, 10, 11).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Sử dụng Git: Phân biệt sự khác nhau và thời điểm dùng hai lệnh `git clone` và `git pull`.
* **expected_key_points:**
  - id: KP3_1
    content: Bản chất git clone
    keypoint_weight: 0.5
    description: Dùng để tải toàn bộ mã nguồn của một repository từ server về máy local lần đầu tiên, tự động tạo thư mục dự án và liên kết remote.
  - id: KP3_2
    content: Bản chất git pull
    keypoint_weight: 0.5
    description: Dùng để cập nhật và gộp các thay đổi mới nhất từ repository trên server về nhánh hiện tại trên máy local khi đã có sẵn thư mục dự án.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế các kịch bản kiểm thử chức năng cho tính năng xem video streaming trực tuyến (như Netflix hay YouTube).
* **expected_key_points:**
  - id: KP4_1
    content: Kiểm thử các phím điều khiển và tua video
    keypoint_weight: 0.5
    description: Kiểm tra dừng/phát (play/pause), tua nhanh (forward), tua lại (rewind), phóng to thu nhỏ màn hình hoạt động mượt mà.
  - id: KP4_2
    content: Kiểm thử điều chỉnh độ phân giải theo băng thông
    keypoint_weight: 0.5
    description: Xác minh video tự động chuyển đổi chất lượng (360p, 720p, 1080p) tương ứng khi băng thông mạng thay đổi mà không làm gián đoạn luồng video.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết câu lệnh SQL sử dụng LEFT JOIN để tìm kiếm danh sách tất cả khách hàng (Customers) kèm thông tin đơn hàng (Orders) của họ, hiển thị cả những khách hàng chưa từng mua hàng.
* **expected_key_points:**
  - id: KP5_1
    content: Cú pháp LEFT JOIN chính xác
    keypoint_weight: 0.6
    description: Viết câu lệnh SELECT kết hợp bảng Customers nằm bên trái LEFT JOIN bảng Orders thông qua khóa ngoại (ví dụ: `ON Customers.id = Orders.customer_id`).
  - id: KP5_2
    content: Đặc trưng của kết quả trả về
    keypoint_weight: 0.4
    description: Xác nhận đối với khách hàng chưa mua hàng, các cột thông tin lấy từ bảng Orders sẽ có giá trị hiển thị là `NULL`.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách thiết lập và sử dụng biến môi trường (Environment Variables) trong Postman để dễ dàng chuyển đổi kiểm thử giữa môi trường Dev và Staging.
* **expected_key_points:**
  - id: KP6_1
    content: Cách tạo Environment trong Postman
    keypoint_weight: 0.5
    description: Tạo hai môi trường Dev và Staging; định nghĩa biến `url` chứa địa chỉ API tương ứng của từng môi trường.
  - id: KP6_2
    content: Sử dụng biến trong Request URL
    keypoint_weight: 0.5
    description: Thay thế địa chỉ cứng bằng cú pháp hai ngoặc nhọn `{{url}}/api/users` trong trường URL, chọn môi trường mong muốn từ dropdown ở góc trên bên phải trước khi gửi request.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy so sánh sự khác nhau giữa Black-box Testing (Kiểm thử hộp đen) và White-box Testing (Kiểm thử hộp trắng) về đối tượng và kỹ thuật áp dụng.
* **expected_key_points:**
  - id: KP7_1
    content: Đặc trưng Black-box Testing
    keypoint_weight: 0.5
    description: Không cần biết cấu trúc code bên trong, kiểm thử dựa trên yêu cầu đặc tả chức năng hệ thống (kỹ thuật: phân vùng tương đương, phân tích biên).
  - id: KP7_2
    content: Đặc trưng White-box Testing
    keypoint_weight: 0.5
    description: Kiểm thử dựa trên cấu trúc logic mã nguồn bên trong, yêu cầu khả năng đọc hiểu code (kỹ thuật: bao phủ câu lệnh, bao phủ nhánh, bao phủ đường đi).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản kiểm thử tải trọng lớn (Stress Testing) cho hệ thống trò chuyện thời gian thực (Real-time Chat) sử dụng WebSockets để xác định giới hạn chịu tải tối đa của máy chủ.
* **expected_key_points:**
  - id: KP8_1
    content: Giả lập số lượng kết nối WebSocket đồng thời
    keypoint_weight: 0.6
    description: Sử dụng công cụ kiểm thử tải (như Artillery hoặc JMeter) để tạo và duy trì hàng vạn kết nối WebSocket đồng thời (concurrent connections), gửi tin nhắn liên tục giữa các user để đo thời gian trễ (latency).
  - id: KP8_2
    content: Giám sát tài nguyên máy chủ và kết nối
    keypoint_weight: 0.4
    description: Đo lường mức độ sử dụng CPU/RAM của server, số lượng file descriptors mở tối đa và khả năng tự động ngắt/kết nối lại của client khi server quá tải.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích nguyên nhân xảy ra lỗi Deadlock trong hệ quản trị cơ sở dữ liệu và đề xuất cách thiết kế kịch bản test để phát hiện lỗi này khi chạy đa luồng.
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế gây ra Deadlock
    keypoint_weight: 0.5
    description: Xảy ra khi hai hoặc nhiều tiến trình (transactions) cùng chờ đợi để lấy khóa (lock) tài nguyên mà tiến trình kia đang nắm giữ, dẫn đến trạng thái đóng băng vô tận.
  - id: KP9_2
    content: Cách thiết kế kịch bản test phát hiện
    keypoint_weight: 0.5
    description: Giả lập 2 luồng cập nhật chéo dữ liệu đồng thời (ví dụ: Luồng A sửa Row 1 rồi Row 2; Luồng B sửa Row 2 rồi Row 1 trong cùng một thời điểm) để kiểm tra xem DB có phát hiện deadlock và tự động hủy (abort/rollback) một luồng không.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Kiểm thử bảo mật: Phân tích lỗi cấu hình CORS (Cross-Origin Resource Sharing) sai và cách Tester có thể khai thác thủ công để kiểm chứng lỗi này trên hệ thống API.
* **expected_key_points:**
  - id: KP10_1
    content: Bản chất lỗi cấu hình CORS
    keypoint_weight: 0.5
    description: Xảy ra khi API server cấu hình header `Access-Control-Allow-Origin: *` kết hợp với `Access-Control-Allow-Credentials: true`, cho phép trang web từ domain lạ truy cập và đọc dữ liệu nhạy cảm của user.
  - id: KP10_2
    content: Cách kiểm thử thủ công
    keypoint_weight: 0.5
    description: Gửi API request sử dụng Curl hoặc Postman với Header `Origin: http://evil-domain.com`. Nếu response trả về chứa header `Access-Control-Allow-Origin: http://evil-domain.com` (hoặc `*`), hệ thống dính lỗi cấu hình CORS.

