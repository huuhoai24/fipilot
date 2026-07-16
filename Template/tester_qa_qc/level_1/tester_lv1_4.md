# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1) - Tập Đề Kiểm Thử Phi Chức Năng và SQL JOIN (4)

* **Role:** Tester
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Sự khác biệt cơ bản giữa Functional Testing (Kiểm thử chức năng) và Non-functional Testing (Kiểm thử phi chức năng) là gì? Cho ví dụ.
* **expected_key_points:**
  - id: KP1_1
    content: Khái niệm Functional Testing
    keypoint_weight: 0.5
    description: Kiểm tra hệ thống có làm đúng những gì được yêu cầu chức năng (ví dụ: đăng nhập thành công với tài khoản đúng, tính toán đúng tiền).
  - id: KP1_2
    content: Khái niệm Non-functional Testing
    keypoint_weight: 0.5
    description: Kiểm tra chất lượng hoạt động của hệ thống (ví dụ: trang web tải dưới 2 giây, hệ thống bảo mật an toàn, chịu tải được 1000 người dùng đồng thời).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Kỹ thuật phân tích bảng quyết định (Decision Table Testing) là gì và khi nào nên áp dụng trong thiết kế test case?
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa bảng quyết định
    keypoint_weight: 0.5
    description: Là kỹ thuật thiết kế test case dưới dạng bảng biểu thị sự kết hợp của các điều kiện đầu vào khác nhau để sinh ra các hành động/kết quả tương ứng.
  - id: KP2_2
    content: Thời điểm áp dụng
    keypoint_weight: 0.5
    description: Nên dùng khi hệ thống có các quy tắc nghiệp vụ phức tạp phụ thuộc vào sự kết hợp của nhiều điều kiện đầu vào (ví dụ: duyệt vay ngân hàng dựa trên tuổi, thu nhập, lịch sử tín dụng).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Làm thế nào để kiểm tra Session và Cookie của ứng dụng Web trên trình duyệt bằng DevTools?
* **expected_key_points:**
  - id: KP3_1
    content: Vị trí kiểm tra Cookies và Session Storage
    keypoint_weight: 0.5
    description: Mở DevTools -> chọn tab Application -> trong menu bên trái tìm mục Storage -> click Cookies hoặc Local Storage / Session Storage.
  - id: KP3_2
    content: Mục tiêu kiểm tra
    keypoint_weight: 0.5
    description: Kiểm tra xem thông tin đăng nhập, token phiên làm việc có được lưu đúng khóa không và có bị mất đi khi đăng xuất hoặc xóa cookie hay không.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết kịch bản kiểm thử (Test Scenario) cho chức năng tìm kiếm (Search) có gợi ý tự động (Auto-complete) trên trang web.
* **expected_key_points:**
  - id: KP4_1
    content: Kiểm thử luồng hiển thị gợi ý
    keypoint_weight: 0.5
    description: Kiểm tra nhập từ khóa -> dropdown hiển thị gợi ý liên quan ngay lập tức; tốc độ gợi ý mượt mà; từ khóa gợi ý trùng khớp nội dung nhập.
  - id: KP4_2
    content: Kiểm thử các phím điều khiển và ký tự đặc biệt
    keypoint_weight: 0.5
    description: Kiểm tra dùng phím mũi tên lên/xuống và Enter để chọn gợi ý; kiểm tra nhập ký tự đặc biệt, để trống, hoặc nhập từ không có trong cơ sở dữ liệu.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết câu lệnh SQL truy vấn kết hợp hai bảng để lấy ra danh sách đơn hàng gồm: Mã đơn hàng (order_id), Ngày tạo (created_date) và Tên khách hàng (customer_name) sử dụng INNER JOIN.
* **expected_key_points:**
  - id: KP5_1
    content: Sử dụng cú pháp INNER JOIN chính xác
    keypoint_weight: 0.6
    description: Viết câu lệnh SELECT với INNER JOIN kết nối bảng Orders và Customers thông qua khóa ngoại (ví dụ: `ON Orders.customer_id = Customers.id`).
  - id: KP5_2
    content: Chỉ định rõ cột và alias
    keypoint_weight: 0.4
    description: Lựa chọn đúng các cột cần hiển thị và đặt alias cho bảng nếu cần thiết để tránh xung đột tên cột.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày quy trình kiểm thử giao diện Responsive Web trên thiết bị di động.
* **expected_key_points:**
  - id: KP6_1
    content: Giả lập responsive bằng trình duyệt
    keypoint_weight: 0.5
    description: Dùng tính năng Toggle Device Toolbar (Ctrl+Shift+M) trên Chrome DevTools, thay đổi kích thước và chọn các thiết bị di động phổ biến để kiểm tra nhanh.
  - id: KP6_2
    content: Kiểm thử trên thiết bị thật
    keypoint_weight: 0.5
    description: Test trực tiếp trên màn hình điện thoại thật để đánh giá font chữ, sự chồng chéo nút bấm, và trải nghiệm vuốt/chạm (touch targets) thực tế.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích sự khác biệt và mối quan hệ giữa các khái niệm: Test Case, Test Suite và Test Run.
* **expected_key_points:**
  - id: KP7_1
    content: Khái niệm Test Case và Test Suite
    keypoint_weight: 0.6
    description: Test Case là các bước thực hiện đơn lẻ có dữ liệu và kết quả mong đợi. Test Suite là tập hợp các Test Case có cùng chủ đề hoặc mục đích kiểm thử (ví dụ: Suite đăng nhập, Suite thanh toán).
  - id: KP7_2
    content: Khái niệm Test Run
    keypoint_weight: 0.4
    description: Test Run là một phiên thực thi cụ thể một nhóm Test Case tại một thời điểm nhất định trên một môi trường/build cụ thể để ghi nhận kết quả Pass/Fail.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiểm thử cho một hệ thống hàng đợi tin nhắn (Message Queue như RabbitMQ/Kafka) để đảm bảo không bị mất tin nhắn (No message loss) khi dịch vụ gặp sự cố mạng.
* **expected_key_points:**
  - id: KP8_1
    content: Kiểm tra cơ chế Ack (Acknowledgment) và Persist
    keypoint_weight: 0.6
    description: Xác minh tin nhắn được lưu trữ bền vững (persistent) trên đĩa cứng của Broker và Consumer chỉ gửi tín hiệu Ack sau khi đã hoàn thành xử lý tin nhắn thành công.
  - id: KP8_2
    content: Giả lập sự cố mất kết nối
    keypoint_weight: 0.4
    description: Ngắt kết nối mạng của Consumer hoặc sập Broker đột ngột giữa chừng để đảm bảo tin nhắn không bị mất và được chuyển hướng (redelivered) sang consumer khác hoặc xử lý lại sau khi hồi phục.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích nguyên nhân và cách tái hiện lỗi "Race Condition" khi hai nhân viên cùng chỉnh sửa thông tin của một khách hàng vào cùng một thời điểm.
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế xảy ra lỗi Race Condition
    keypoint_weight: 0.5
    description: Xảy ra do hệ thống xử lý bất đồng bộ hoặc thiếu khóa dữ liệu (database lock), khiến request sau đè lên request trước mà không kiểm tra phiên bản dữ liệu cũ (version/timestamp).
  - id: KP9_2
    content: Cách tái hiện lỗi
    keypoint_weight: 0.5
    description: Dùng 2 tài khoản đăng nhập đồng thời chỉnh sửa cùng 1 record dữ liệu, nhấn lưu cùng một thời điểm (có thể dùng script gửi API song song hoặc click thủ công thật nhanh).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Kiểm thử bảo mật: Phát hiện lỗ hổng Parameter Tampering (Sửa đổi tham số trên URL/Request payload) để trục lợi trong giao dịch.
* **expected_key_points:**
  - id: KP10_1
    content: Bản chất Parameter Tampering
    keypoint_weight: 0.5
    description: Kẻ tấn công sửa đổi giá trị tham số nhạy cảm trong request (URL query, form data, hidden field) gửi lên server (ví dụ: sửa `price=1000` thành `price=1` hoặc `discount=0` thành `discount=90`).
  - id: KP10_2
    content: Cách kiểm thử
    keypoint_weight: 0.5
    description: Dùng công cụ proxy (Burp Suite, Fiddler) chặn request gửi đi, thay đổi giá trị tham số rồi gửi lên server. Kiểm tra xem server có validate lại thông tin đó hay không.

