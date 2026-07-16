# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1) - Tập Đề Lỗi Hệ Thống và SQL GROUP BY (6)

* **Role:** Tester
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa các khái niệm: Error (Lỗi con người), Defect/Bug (Khuyết tật mã nguồn) và Failure (Sự cố hệ thống).
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa Error và Defect
    keypoint_weight: 0.5
    description: `Error` là hành động sai lầm của con người (developer viết nhầm code, BA hiểu sai spec). `Defect` hoặc `Bug` là khuyết tật trong mã nguồn hoặc tài liệu do Error gây ra.
  - id: KP1_2
    content: Định nghĩa Failure
    keypoint_weight: 0.5
    description: `Failure` là sự chệch hướng của phần mềm so với hành vi mong đợi khi thực thi, tức là khi bug được kích hoạt trong môi trường chạy thực tế.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Kỹ thuật kiểm thử chuyển đổi trạng thái (State Transition Testing) là gì? Cho ví dụ minh họa thực tế.
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm kỹ thuật
    keypoint_weight: 0.5
    description: Là kỹ thuật hộp đen dùng khi hành vi hệ thống thay đổi tùy thuộc vào trạng thái hiện tại và lịch sử tương tác trước đó (mô tả qua sơ đồ trạng thái).
  - id: KP2_2
    content: Ví dụ thực tế
    keypoint_weight: 0.5
    description: Ví dụ: Nhập sai mã PIN thẻ ATM. Trạng thái 1: Nhập sai lần 1 -> Đăng nhập lại. Trạng thái 2: Nhập sai lần 2 -> Đăng nhập lại. Trạng thái 3: Nhập sai lần 3 -> Khóa thẻ.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Sử dụng Git: Làm thế nào để tạo một nhánh mới (branch) và đẩy code từ nhánh đó lên repository trên GitHub?
* **expected_key_points:**
  - id: KP3_1
    content: Lệnh tạo và chuyển nhánh
    keypoint_weight: 0.5
    description: Sử dụng câu lệnh `git checkout -b <tên_nhánh>` hoặc `git branch <tên_nhánh>` và `git checkout <tên_nhánh>`.
  - id: KP3_2
    content: Lệnh push code
    keypoint_weight: 0.5
    description: Sử dụng câu lệnh `git push origin <tên_nhánh>` để đẩy code lên server.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế test case kiểm thử giao diện (UI) và tính năng cho một form đăng ký tài khoản có yêu cầu xác thực bằng mã Captcha.
* **expected_key_points:**
  - id: KP4_1
    content: Kiểm thử luồng Captcha đúng/sai
    keypoint_weight: 0.5
    description: Kiểm tra nhập đúng captcha đăng ký thành công; nhập sai captcha báo lỗi; nhấn reload captcha thay đổi ảnh mới.
  - id: KP4_2
    content: Kiểm thử bảo mật captcha
    keypoint_weight: 0.5
    description: Đảm bảo captcha không hiển thị dưới dạng text thuần trong HTML (dễ bị bypass bằng tool); thử bỏ trống captcha hoặc submit form nhiều lần.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết câu lệnh SQL sử dụng GROUP BY và COUNT để thống kê số lượng đơn hàng (orders) theo từng trạng thái (status). Bảng orders gồm các cột: id, status, customer_id.
* **expected_key_points:**
  - id: KP5_1
    content: Cú pháp GROUP BY và COUNT
    keypoint_weight: 0.6
    description: Viết đúng câu lệnh: `SELECT status, COUNT(id) FROM orders GROUP BY status`.
  - id: KP5_2
    content: Vị trí đặt cột SELECT
    keypoint_weight: 0.4
    description: Đảm bảo cột được SELECT không nằm trong hàm gom cụm thì bắt buộc phải có trong mệnh đề GROUP BY.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Làm thế nào để giả lập lỗi HTTP 500 Internal Server Error từ API bằng công cụ Postman Mock Server hoặc Charles Proxy nhằm test khả năng xử lý lỗi của client?
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế giả lập lỗi API
    keypoint_weight: 0.5
    description: Tạo một mock server trong Postman để cấu hình endpoint trả về status 500 kèm payload lỗi mong muốn; hoặc dùng map local/breakpoints trong Charles Proxy/Fiddler để intercept request và thay đổi response thành 500.
  - id: KP6_2
    content: Kiểm tra phản ứng của Client-side
    keypoint_weight: 0.5
    description: Xác minh ứng dụng web/mobile hiển thị thông báo lỗi hệ thống phù hợp, không bị đơ màn hình hoặc crash.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Kiểm thử hành vi của ứng dụng di động khi xảy ra các sự kiện ngắt đột ngột (Interrupt Testing) trong lúc app đang thực hiện giao dịch.
* **expected_key_points:**
  - id: KP7_1
    content: Các trường hợp ngắt (Interrupts) phổ biến
    keypoint_weight: 0.5
    description: Cuộc gọi đến, tin nhắn SMS/Zalo hiện pop-up, điện thoại báo pin yếu (20%), mất kết nối mạng đột ngột hoặc cắm sạc pin.
  - id: KP7_2
    content: Kết quả mong đợi sau khi ngắt kết thúc
    keypoint_weight: 0.5
    description: App phải quay lại đúng trạng thái trước khi bị ngắt, dữ liệu giao dịch không bị trùng lặp hoặc mất mát và không bị crash app.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản kiểm thử cho hệ thống thanh toán định kỳ tự động (Subscription/Recurring Billing) hàng tháng của dịch vụ SaaS.
* **expected_key_points:**
  - id: KP8_1
    content: Kiểm tra luồng gia hạn thành công và thất bại
    keypoint_weight: 0.6
    description: Xác minh tiền được trừ đúng định kỳ, gửi hóa đơn email; nếu tài khoản hết tiền/thẻ hết hạn, hệ thống cần gửi thông báo và chuyển trạng thái subscription thành 'Past Due' hoặc tạm ngưng dịch vụ.
  - id: KP8_2
    content: Kiểm tra việc thay đổi múi giờ và ngày thanh toán đặc biệt
    keypoint_weight: 0.4
    description: Test các trường hợp đặc biệt như thanh toán rơi vào ngày 29, 30, 31 của tháng hoặc xử lý thay đổi chu kỳ thanh toán (upgrade/downgrade plan).

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích cách kiểm thử lỗ hổng bảo mật CSRF (Cross-Site Request Forgery) trên các form giao dịch tài chính.
* **expected_key_points:**
  - id: KP9_1
    content: Nguyên lý tấn công CSRF
    keypoint_weight: 0.5
    description: Kẻ tấn công lừa trình duyệt của người dùng gửi các request ngoài ý muốn (như chuyển tiền) đến một trang web mà người dùng đã đăng nhập trước đó và vẫn còn lưu session cookie.
  - id: KP9_2
    content: Kiểm thử tính năng chống CSRF
    keypoint_weight: 0.5
    description: Kiểm tra xem hệ thống có sử dụng và validate mã CSRF Token duy nhất cho mỗi phiên làm việc hoặc thuộc tính cookie `SameSite=Strict/Lax` hay không bằng cách xóa/sửa đổi token rồi gửi request.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết lập chiến lược kiểm thử cho hệ thống đa ngôn ngữ (Localization Testing) xử lý các múi giờ khác nhau và định dạng ngày tháng của từng quốc gia.
* **expected_key_points:**
  - id: KP10_1
    content: Kiểm thử hiển thị và tràn chữ (UI Localization)
    keypoint_weight: 0.5
    description: Kiểm tra hiển thị giao diện khi dịch sang ngôn ngữ dài (ví dụ tiếng Đức, tiếng Pháp), xem các nhãn (labels) có bị tràn, đè chữ hoặc vỡ khung hình không.
  - id: KP10_2
    content: Kiểm thử định dạng ngày giờ và múi giờ (Timezone)
    keypoint_weight: 0.5
    description: Xác minh dữ liệu lưu ở múi giờ UTC nhưng hiển thị đúng múi giờ local của người dùng; kiểm tra định dạng ngày tháng như DD/MM/YYYY vs MM/DD/YYYY.

