# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1) - Tập Đề Vòng Đời Lỗi và API Phân Trang (3)

* **Role:** Tester
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Vòng đời của một Bug (Bug Lifecycle) gồm các trạng thái cơ bản nào và vai trò của Tester trong từng trạng thái đó?
* **expected_key_points:**
  - id: KP1_1
    content: Các trạng thái cơ bản của Bug
    keypoint_weight: 0.6
    description: Nêu được các trạng thái chính: New (Phát hiện), Assigned (Giao cho Dev), Open/In Progress (Đang sửa), Fixed (Đã sửa xong), Reopen (Lỗi chưa hết sau khi test lại), Verified/Closed (Đã xác minh và đóng).
  - id: KP1_2
    content: Vai trò của Tester
    keypoint_weight: 0.4
    description: Tester tạo bug (New), kiểm thử lại khi dev báo đã sửa (Fixed) để quyết định Closed hoặc Reopen.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt Smoke Testing và Sanity Testing về mục đích và thời điểm áp dụng trong dự án.
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm Smoke Testing
    keypoint_weight: 0.5
    description: Thực hiện trên build mới để xác minh các chức năng cốt lõi (critical) hoạt động bình thường, quyết định có chấp nhận build đó để test tiếp hay không.
  - id: KP2_2
    content: Khái niệm Sanity Testing
    keypoint_weight: 0.5
    description: Thực hiện sau khi nhận được bản sửa lỗi (bug fix) để xác minh nhanh rằng lỗi đó đã được fix và không gây ảnh hưởng trực tiếp đến vùng lân cận.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong SQL, làm thế nào để lọc dữ liệu theo điều kiện cụ thể? Nêu sự khác nhau giữa toán tử `=` và toán tử `LIKE` kèm ví dụ.
* **expected_key_points:**
  - id: KP3_1
    content: Cách lọc dữ liệu và mệnh đề WHERE
    keypoint_weight: 0.4
    description: Sử dụng mệnh đề `WHERE` để lọc các bản ghi thỏa mãn điều kiện.
  - id: KP3_2
    content: Phân biệt toán tử = và LIKE
    keypoint_weight: 0.6
    description: Toán tử `=` dùng để so sánh khớp chính xác hoàn toàn. Toán tử `LIKE` kết hợp với các ký tự đại diện (`%`, `_`) để tìm kiếm khớp một phần (pattern matching).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết các test case (kịch bản kiểm thử) cho chức năng Upload File hình ảnh đại diện (avatar) của người dùng.
* **expected_key_points:**
  - id: KP4_1
    content: Kiểm thử chức năng và định dạng
    keypoint_weight: 0.5
    description: Kiểm tra upload thành công với định dạng ảnh cho phép (png, jpg), kích thước file hợp lệ; kiểm tra chặn file định dạng sai (pdf, exe, txt) hoặc file quá dung lượng.
  - id: KP4_2
    content: Kiểm thử giao diện và bảo mật
    keypoint_weight: 0.5
    description: Kiểm tra hiển thị ảnh sau khi upload, nút hủy, ảnh mặc định khi xóa; kiểm thử bảo mật cơ bản như upload file chứa mã độc để kiểm tra xem server có lọc hay không.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Làm thế nào để thiết kế test case cho một API GET có hỗ trợ phân trang (Pagination) với các tham số `page` và `limit`?
* **expected_key_points:**
  - id: KP5_1
    content: Kiểm thử trường hợp hợp lệ
    keypoint_weight: 0.5
    description: Kiểm tra API trả về đúng số lượng bản ghi tương ứng với `limit`, và đúng trang dữ liệu tương ứng với `page`.
  - id: KP5_2
    content: Kiểm thử giá trị biên và không hợp lệ
    keypoint_weight: 0.5
    description: Gửi các giá trị biên (limit = 0, limit âm, page = 0, page vượt quá tổng số trang) và kiểm tra mã lỗi trả về (thường là 400 Bad Request) hoặc hành vi xử lý mặc định của API.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy trình bày cách sử dụng Chrome DevTools để mô phỏng môi trường mạng chậm (Network Throttling) khi kiểm thử trải nghiệm ứng dụng Web.
* **expected_key_points:**
  - id: KP6_1
    content: Thao tác mô phỏng mạng chậm
    keypoint_weight: 0.5
    description: Mở F12 -> chọn tab Network -> click vào dropdown Throttling (mặc định là No throttling) -> chọn các cấu hình có sẵn như Fast 3G, Slow 3G hoặc Offline.
  - id: KP6_2
    content: Mục tiêu kiểm thử
    keypoint_weight: 0.5
    description: Đánh giá khả năng hiển thị của trang (hiển thị loading indicator, spinner), kiểm tra xem các API request có bị timeout và ứng dụng có xử lý lỗi timeout mượt mà hay không.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế các test case cơ bản cho chức năng Đăng nhập bằng mã OTP gửi qua tin nhắn SMS.
* **expected_key_points:**
  - id: KP7_1
    content: Kiểm thử luồng tích cực (Positive cases)
    keypoint_weight: 0.5
    description: Nhập số điện thoại hợp lệ -> nhận OTP -> nhập OTP đúng hạn -> đăng nhập thành công.
  - id: KP7_2
    content: Kiểm thử luồng tiêu cực và bảo mật (Negative/Security)
    keypoint_weight: 0.5
    description: Nhập OTP sai, nhập OTP hết hạn, nhấn gửi lại OTP nhiều lần liên tục (Spam), nhập số điện thoại sai định dạng.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản test hệ thống thanh toán khi kết nối mạng bị ngắt đúng lúc người dùng nhấn nút Thanh Toán (đã trừ tiền phía ngân hàng nhưng chưa cập nhật trạng thái đơn hàng trên hệ thống của bạn).
* **expected_key_points:**
  - id: KP8_1
    content: Kiểm tra tính nhất quán dữ liệu (Data Consistency)
    keypoint_weight: 0.5
    description: Kiểm tra xem hệ thống có cơ chế đối soát tự động (reconciliation) hoặc cơ chế Retry/Webhook từ cổng thanh toán để cập nhật lại trạng thái đơn hàng sau khi có mạng lại hay không.
  - id: KP8_2
    content: Xử lý trải nghiệm người dùng (UX)
    keypoint_weight: 0.5
    description: Hệ thống cần hiển thị thông báo rõ ràng về trạng thái thanh toán đang xử lý, không được cho phép người dùng nhấn thanh toán lại (tránh trùng đơn) và cung cấp kênh hỗ trợ khi có sự cố.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích cơ chế kiểm thử tải (Load Testing) cho API và cách bạn phối hợp theo dõi để phát hiện lỗi rò rỉ bộ nhớ (Memory Leak) trên máy chủ.
* **expected_key_points:**
  - id: KP9_1
    content: Thiết lập kiểm thử tải
    keypoint_weight: 0.5
    description: Sử dụng công cụ (JMeter, K6) gửi số lượng request đồng thời tăng dần đến API trong một khoảng thời gian dài.
  - id: KP9_2
    content: Theo dõi tài nguyên để phát hiện Memory Leak
    keypoint_weight: 0.5
    description: Quan sát biểu đồ sử dụng RAM của server qua các công cụ giám sát; nếu RAM tăng liên tục và không giảm về mức ban đầu sau khi ngừng tải, đó là dấu hiệu của rò rỉ bộ nhớ.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Cách kiểm thử bảo mật để phát hiện lỗ hổng IDOR (Insecure Direct Object Reference) trên API endpoint lấy thông tin người dùng.
* **expected_key_points:**
  - id: KP10_1
    content: Nguyên lý tấn công IDOR
    keypoint_weight: 0.4
    description: Xảy ra khi ứng dụng cho phép truy cập tài nguyên (ví dụ: thông tin người dùng) thông qua ID truyền trực tiếp trong URL/Body mà không kiểm tra quyền sở hữu của token hiện tại.
  - id: KP10_2
    content: Kịch bản kiểm thử IDOR
    keypoint_weight: 0.6
    description: Đăng nhập bằng User A -> lấy Token A -> gửi request lấy thông tin của User B bằng cách thay đổi ID của User B trong URL/Body. Nếu API trả về dữ liệu User B thay vì báo lỗi 403 Forbidden, hệ thống bị dính lỗi IDOR.

