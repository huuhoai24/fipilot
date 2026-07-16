# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1) - Tập Đề Regression Testing và SQL String Functions (12)

* **Role:** Tester
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Khi nào thì cần thực hiện Regression Testing (Kiểm thử hồi quy)? Có phải lúc nào cũng cần chạy lại toàn bộ bộ Test Case (Full Regression Suite) không?
* **expected_key_points:**
  - id: KP1_1
    content: Thời điểm chạy Regression Testing
    keypoint_weight: 0.5
    description: Chạy khi có bất kỳ thay đổi nào trong code: sửa bug, thêm tính năng mới, nâng cấp thư viện hệ thống hoặc thay đổi môi trường cấu hình.
  - id: KP1_2
    content: Phạm vi kiểm thử hồi quy
    keypoint_weight: 0.5
    description: Không nhất thiết chạy toàn bộ. Có thể chọn lọc chạy các test case thuộc vùng bị tác động trực tiếp/gián tiếp bởi code thay đổi để tiết kiệm thời gian, chỉ chạy full suite trước các đợt release lớn.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt lỗi giao diện (UI Bug) và lỗi chức năng (Functional Bug). Cho ví dụ minh họa từng loại.
* **expected_key_points:**
  - id: KP2_1
    content: Đặc trưng UI Bug
    keypoint_weight: 0.5
    description: Lỗi liên quan đến hiển thị, bố cục, màu sắc, font chữ không khớp thiết kế (ví dụ: nút bấm bị che khuất một nửa trên điện thoại màn hình nhỏ).
  - id: KP2_2
    content: Đặc trưng Functional Bug
    keypoint_weight: 0.5
    description: Lỗi liên quan đến logic xử lý, nghiệp vụ hệ thống (ví dụ: người dùng nhập đúng thông tin đăng nhập nhưng hệ thống báo tài khoản không tồn tại).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong SQL, làm thế nào để so sánh giá trị số trong mệnh đề WHERE? Nêu cách sử dụng toán tử so sánh lớn hơn (>), nhỏ hơn (<), khác (!=) kèm ví dụ.
* **expected_key_points:**
  - id: KP3_1
    content: Sử dụng toán tử so sánh số học
    keypoint_weight: 0.5
    description: Dùng trực tiếp các toán tử `>`, `<`, `>=`, `<=`, `=`, `!=` (hoặc `<>`) sau tên cột trong mệnh đề WHERE để lọc dữ liệu kiểu số.
  - id: KP3_2
    content: Ví dụ truy vấn thực tế
    keypoint_weight: 0.5
    description: Ví dụ: `SELECT * FROM products WHERE price > 100 AND quantity < 10 AND status != 'inactive'`.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết kịch bản kiểm thử (Test Scenario) cho tính năng đăng ký tài khoản yêu cầu xác thực định danh KYC (chụp ảnh thẻ CCCD hai mặt và quét khuôn mặt).
* **expected_key_points:**
  - id: KP4_1
    content: Kiểm thử luồng chụp ảnh và phân tích OCR
    keypoint_weight: 0.5
    description: Chụp ảnh CCCD rõ nét -> hệ thống trích xuất thông tin (họ tên, số CCCD) chính xác; kiểm tra chụp ảnh mờ, mất góc, chụp ảnh giả lập từ màn hình khác phải bị từ chối.
  - id: KP4_2
    content: Kiểm thử quét khuôn mặt (Liveness Detection)
    keypoint_weight: 0.5
    description: Quét khuôn mặt trực tiếp trùng khớp với ảnh trên CCCD -> duyệt thành công; quét khuôn mặt không khớp hoặc dùng ảnh chụp tĩnh để quét -> báo lỗi định danh.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết câu lệnh SQL sử dụng các hàm xử lý chuỗi cơ bản (CONCAT, SUBSTRING, UPPER, LOWER) để chuyển đổi định dạng hiển thị họ và tên của khách hàng thành chữ in hoa toàn bộ và ghép cột `first_name` với `last_name`.
* **expected_key_points:**
  - id: KP5_1
    content: Sử dụng hàm ghép chuỗi và đổi chữ hoa
    keypoint_weight: 0.6
    description: Sử dụng kết hợp hàm CONCAT (hoặc toán tử `||` tùy DB) và hàm UPPER/LOWER (ví dụ: `SELECT UPPER(CONCAT(first_name, ' ', last_name)) AS full_name FROM customers`).
  - id: KP5_2
    content: Đặt tên alias cho cột kết quả
    keypoint_weight: 0.4
    description: Sử dụng từ khóa `AS` để đặt lại tên cột hiển thị đại diện tránh để tên hàm mặc định khó đọc.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách sử dụng tab Elements trong Chrome DevTools để chỉnh sửa trực tiếp HTML/CSS phục vụ cho việc kiểm thử nhanh giao diện và layout web.
* **expected_key_points:**
  - id: KP6_1
    content: Chỉnh sửa HTML trực tiếp
    keypoint_weight: 0.5
    description: Mở tab Elements -> double-click vào thẻ HTML hoặc đoạn text để thay đổi nội dung; hoặc chuột phải chọn Edit as HTML để thêm bớt thẻ nhằm xem layout thay đổi.
  - id: KP6_2
    content: Chỉnh sửa thuộc tính CSS
    keypoint_weight: 0.5
    description: Xem bảng Styles bên phải -> click chọn/bỏ chọn thuộc tính CSS hiện có hoặc thêm thuộc tính mới (như padding, color) để kiểm tra căn lề giao diện.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế các test case để kiểm tra hoạt động của ứng dụng di động khi thiết bị thay đổi kết nối mạng liên tục (Network Switching).
* **expected_key_points:**
  - id: KP7_1
    content: Chuyển đổi các loại kết nối
    keypoint_weight: 0.5
    description: Kiểm tra khi thiết bị chuyển đổi từ Wifi sang 4G và ngược lại trong khi app đang tải dữ liệu hoặc gửi request xem có bị gián đoạn hay mất phiên làm việc (session) không.
  - id: KP7_2
    content: Xử lý mất mạng hoàn toàn và kết nối lại
    keypoint_weight: 0.5
    description: Kiểm tra chuyển sang chế độ máy bay (Airplane mode) -> app báo mất mạng rõ ràng; tắt chế độ máy bay -> app tự động phục hồi và tiếp tục luồng công việc.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản kiểm thử tính năng tự động khôi phục dữ liệu nháp (Auto-save / Auto-recovery) của một ứng dụng soạn thảo văn bản online (như Google Docs) khi gặp sự cố sập nguồn điện hoặc mất kết nối đột ngột.
* **expected_key_points:**
  - id: KP8_1
    content: Kiểm tra cơ chế lưu nháp định kỳ (Auto-save)
    keypoint_weight: 0.6
    description: Xác minh ứng dụng tự động gửi bản lưu nháp lên server hoặc Local Storage sau mỗi khoảng thời gian (ví dụ 10 giây) hoặc sau mỗi ký tự gõ mà không làm đơ giao diện.
  - id: KP8_2
    content: Khôi phục dữ liệu sau sự cố (Recovery)
    keypoint_weight: 0.4
    description: Tắt nguồn máy tính đột ngột hoặc tắt trình duyệt -> mở lại trang web -> kiểm tra xem hệ thống có đưa ra tùy chọn khôi phục bản lưu gần nhất và dữ liệu được phục hồi đầy đủ không.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích cách kiểm thử tích hợp (Integration Testing) giữa hai dịch vụ độc lập giao tiếp qua giao thức truyền thông điệp bất đồng bộ (Asynchronous Messaging) sử dụng AMQP (như RabbitMQ).
* **expected_key_points:**
  - id: KP9_1
    content: Đảm bảo định dạng payload tin nhắn (Schema Validation)
    keypoint_weight: 0.5
    description: Kiểm tra xem dữ liệu JSON/XML được gửi từ Service A (Producer) có khớp hoàn toàn với cấu trúc mong đợi của Service B (Consumer) không.
  - id: KP9_2
    content: Kiểm thử xử lý lỗi và hàng đợi lỗi (Dead Letter Queue)
    keypoint_weight: 0.5
    description: Nếu Service B nhận tin nhắn bị lỗi logic hoặc không đúng cấu trúc, xác minh tin nhắn đó được đẩy sang Dead Letter Queue (DLQ) để xử lý sau thay vì làm nghẽn hàng đợi chính.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Kiểm thử bảo mật: Trình bày cơ chế kiểm tra và ngăn chặn lỗ hổng HTML-to-PDF Injection khi hệ thống có tính năng xuất hóa đơn PDF từ nội dung HTML do người dùng nhập.
* **expected_key_points:**
  - id: KP10_1
    content: Nguyên lý tấn công HTML-to-PDF Injection
    keypoint_weight: 0.5
    description: Xảy ra khi công cụ sinh PDF thực thi mã HTML hoặc script được chèn vào dữ liệu đầu vào, dẫn đến việc đọc file cục bộ của server hoặc thực thi mã từ xa.
  - id: KP10_2
    content: Cách thức kiểm thử phát hiện lỗ hổng
    keypoint_weight: 0.5
    description: Nhập các thẻ HTML đặc biệt (như `<iframe src="file:///etc/passwd">` hoặc `<script>document.write(window.location)</script>`) vào trường thông tin khách hàng, sau đó xuất file PDF và kiểm tra xem nội dung PDF có chứa thông tin file hệ thống hay không.

