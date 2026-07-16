# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1) - Tập Đề Exploratory Testing và HTTP API Methods (5)

* **Role:** Tester
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Khái niệm và mục đích của Exploratory Testing (Kiểm thử khám phá) là gì? Nó khác gì so với Scripted Testing?
* **expected_key_points:**
  - id: KP1_1
    content: Khái niệm Exploratory Testing
    keypoint_weight: 0.5
    description: Là quá trình kiểm thử mà Tester đồng thời học hỏi về hệ thống, thiết kế test case và thực thi test case đó mà không có kịch bản định nghĩa sẵn.
  - id: KP1_2
    content: Sự khác biệt với Scripted Testing
    keypoint_weight: 0.5
    description: Scripted Testing yêu cầu thiết kế toàn bộ test case chi tiết trước khi chạy. Exploratory Testing linh hoạt và dựa trên kinh nghiệm của Tester để tìm bug nhanh.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày các mức độ kiểm thử (Levels of Testing) cơ bản từ thấp đến cao trong vòng đời phát triển phần mềm.
* **expected_key_points:**
  - id: KP2_1
    content: Tên các mức độ kiểm thử
    keypoint_weight: 0.5
    description: Nêu đúng thứ tự: Unit Testing (Kiểm thử đơn vị), Integration Testing (Kiểm thử tích hợp), System Testing (Kiểm thử hệ thống), Acceptance Testing (Kiểm thử chấp nhận).
  - id: KP2_2
    content: Mục tiêu cơ bản từng mức
    keypoint_weight: 0.5
    description: Unit test tập trung vào hàm/class; Integration kiểm tra tích hợp các module; System kiểm tra toàn bộ hệ thống; Acceptance đảm bảo nghiệp vụ đáp ứng khách hàng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Viết câu lệnh SQL INSERT để thêm một khách hàng mới vào bảng `Customers` (chứa các cột: id, name, email, phone).
* **expected_key_points:**
  - id: KP3_1
    content: Cú pháp INSERT INTO chính xác
    keypoint_weight: 0.6
    description: Viết đúng cú pháp: `INSERT INTO Customers (name, email, phone) VALUES ('Nguyen Van A', 'a@gmail.com', '0912345678')`.
  - id: KP3_2
    content: Định dạng kiểu dữ liệu
    keypoint_weight: 0.4
    description: Giá trị chuỗi (varchar) phải được đặt trong nháy đơn, số điện thoại dạng chuỗi cũng cần nháy đơn.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt sự khác nhau giữa các phương thức HTTP: POST, PUT và PATCH trong việc thiết kế và kiểm thử API.
* **expected_key_points:**
  - id: KP4_1
    content: POST vs PUT
    keypoint_weight: 0.5
    description: POST dùng để tạo mới một tài nguyên (không idempotent). PUT dùng để thay thế/cập nhật toàn bộ tài nguyên hiện có hoặc tạo mới nếu chưa tồn tại (idempotent).
  - id: KP4_2
    content: PUT vs PATCH
    keypoint_weight: 0.5
    description: PUT cập nhật đè toàn bộ đối tượng (gửi tất cả trường). PATCH chỉ cập nhật một phần (partial update) tài nguyên (chỉ gửi các trường thay đổi).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Kiểm thử tính năng áp dụng mã giảm giá (Coupon Code) trong giỏ hàng khi người dùng nhập nhiều mã giảm giá cùng lúc hoặc mã đã hết hạn.
* **expected_key_points:**
  - id: KP5_1
    content: Kịch bản kiểm thử mã giảm giá hợp lệ và hết hạn
    keypoint_weight: 0.5
    description: Kiểm tra áp dụng mã còn hạn hoạt động bình thường, mã hết hạn/đã dùng rồi/chưa đạt giá trị đơn hàng tối thiểu phải báo lỗi rõ ràng.
  - id: KP5_2
    content: Kịch bản áp dụng nhiều mã (Coupon Stackability)
    keypoint_weight: 0.5
    description: Kiểm tra xem hệ thống có cho phép cộng dồn mã hay không. Nếu không, phải tự động chọn mã tốt nhất hoặc thông báo chỉ dùng 1 mã duy nhất.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Làm thế nào để sử dụng DevTools Console để xem log, bắt lỗi JavaScript (Errors) và kiểm tra cookies lưu trữ?
* **expected_key_points:**
  - id: KP6_1
    content: Xem log và lỗi JS trong Console
    keypoint_weight: 0.5
    description: Mở tab Console, lọc mức độ lỗi (Errors) màu đỏ, đọc stack trace để biết file nguồn và dòng code phát sinh lỗi khi tương tác trên UI.
  - id: KP6_2
    content: Kiểm tra cookies và lưu trữ
    keypoint_weight: 0.5
    description: Dùng lệnh `document.cookie` trong console hoặc mở tab Application -> Cookies để xem danh sách khóa-giá trị, cờ HttpOnly, Secure.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế các test case cơ bản cho tính năng "Quên mật khẩu" gửi link reset mật khẩu qua Email người dùng.
* **expected_key_points:**
  - id: KP7_1
    content: Kiểm thử luồng tích cực
    keypoint_weight: 0.5
    description: Nhập email đã đăng ký -> kiểm tra email nhận link reset -> click link đổi mật khẩu thành công và đăng nhập được bằng mật khẩu mới.
  - id: KP7_2
    content: Kiểm thử luồng tiêu cực và bảo mật
    keypoint_weight: 0.5
    description: Nhập email chưa đăng ký, link reset hết hạn (timeout), sử dụng link reset 2 lần liên tiếp, thay đổi ID tài khoản trên link reset.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản kiểm thử tính năng đồng bộ hóa dữ liệu ngoại tuyến (Offline Synchronization) cho ứng dụng di động khi mất kết nối mạng và kết nối lại.
* **expected_key_points:**
  - id: KP8_1
    content: Lưu trữ dữ liệu tạm thời (Offline cache)
    keypoint_weight: 0.5
    description: Xác minh các thao tác của người dùng khi offline được lưu trữ an toàn trong Local DB của điện thoại (SQLite, Realm) mà không bị mất hoặc crash app.
  - id: KP8_2
    content: Quy trình đồng bộ khi online lại
    keypoint_weight: 0.5
    description: Khi có mạng lại, hệ thống tự động đẩy dữ liệu lên server theo đúng thứ tự thời gian; xử lý thông minh khi có xung đột dữ liệu (data conflict) giữa server và client.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích rủi ro hệ thống và thiết lập chiến lược kiểm thử cho một hệ thống Microservices khi một dịch vụ trung gian bị sập (Service Dependency Failure).
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế chịu lỗi (Fault Tolerance) và Circuit Breaker
    keypoint_weight: 0.5
    description: Kiểm tra xem hệ thống có trả về dữ liệu mặc định (fallback) hoặc ngắt kết nối an toàn (circuit breaker) để tránh làm sập toàn bộ chuỗi dịch vụ hay không.
  - id: KP9_2
    content: Kiểm tra trải nghiệm người dùng khi lỗi
    keypoint_weight: 0.5
    description: Hệ thống cần hiển thị thông báo lỗi thân thiện thay vì crash giao diện hoặc xoay loading vô tận.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Làm thế nào để thiết kế kịch bản và đo lường hiệu năng của hệ thống khi gặp spike load (lượng truy cập tăng đột biến trong thời gian cực ngắn)?
* **expected_key_points:**
  - id: KP10_1
    content: Đặc trưng của Spike Testing
    keypoint_weight: 0.5
    description: Spike testing tăng lượng ảo (virtual users) đột ngột từ bình thường lên cực đại rồi giảm nhanh về bình thường để kiểm tra độ ổn định của hệ thống.
  - id: KP10_2
    content: Chỉ số đo lường hiệu năng
    keypoint_weight: 0.5
    description: Theo dõi tỷ lệ lỗi (Error Rate), Thời gian phản hồi (Response Time), và khả năng tự động co giãn tài nguyên (Auto-scaling) của server.

