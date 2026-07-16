# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1) - Tập Đề Grey Box Testing và SQL UNION (17)

* **Role:** Tester
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Cấu hình môi trường kiểm thử (Test Environment Configuration) bị sai lệch so với môi trường thật (Production) có thể gây ra những hậu quả gì? Hãy nêu 2 lỗi môi trường phổ biến.
* **expected_key_points:**
  - id: KP1_1
    content: Hậu quả sai lệch cấu hình
    keypoint_weight: 0.5
    description: Gây ra lỗi lọt bug nghiêm trọng lên production (bug lọt lưới), hoặc tạo ra các lỗi giả (false bugs) chỉ có trên môi trường test gây mất thời gian điều tra.
  - id: KP1_2
    content: Hai lỗi cấu hình môi trường phổ biến
    keypoint_weight: 0.5
    description: Sai lệch phiên bản database/hệ điều hành, thiếu cờ cấu hình môi trường trong file `.env`, hoặc quyền truy cập kết nối API/mạng bị chặn.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa Black Box Testing (Kiểm thử hộp đen) và Grey Box Testing (Kiểm thử hộp xám).
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm Grey Box Testing
    keypoint_weight: 0.5
    description: Là phương pháp kiểm thử kết hợp: Tester có một phần kiến thức về cấu trúc bên trong (như cấu trúc database, sơ đồ luồng dữ liệu) để thiết kế test case, nhưng thực thi tương tác ngoài giao diện.
  - id: KP2_2
    content: Sự khác biệt với Black Box Testing
    keypoint_weight: 0.5
    description: Black Box hoàn toàn không biết cấu trúc bên trong phần mềm, chỉ dựa vào đầu vào đầu ra giao diện/API.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Làm thế nào để kiểm tra danh sách các cookies đang lưu trên trình duyệt của trang web bạn đang test bằng Chrome DevTools?
* **expected_key_points:**
  - id: KP3_1
    content: Vị trí xem cookies
    keypoint_weight: 0.5
    description: Mở DevTools (F12) -> chọn tab Application -> menu trái tìm mục Storage -> mở rộng Cookies -> click vào URL trang web hiện tại.
  - id: KP3_2
    content: Các thông số cơ bản hiển thị
    keypoint_weight: 0.5
    description: Xem danh sách các khóa Name, Value, Domain, Path, thời hạn Expires/Max-Age, kích thước Size và cờ HttpOnly/Secure.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết kịch bản kiểm thử (Test Scenario) cho chức năng đặt lịch hẹn khám bệnh trực tuyến (chọn khoa, bác sĩ, khung giờ trống, thanh toán phí giữ chỗ).
* **expected_key_points:**
  - id: KP4_1
    content: Kiểm thử chọn bác sĩ và thời gian trống
    keypoint_weight: 0.5
    description: Kiểm tra hệ thống hiển thị đúng danh sách bác sĩ thuộc khoa đã chọn; các khung giờ đã có người đặt trước phải bị ẩn đi/không cho phép chọn.
  - id: KP4_2
    content: Kiểm thử luồng thanh toán giữ chỗ
    keypoint_weight: 0.5
    description: Thanh toán thành công -> hệ thống tạo lịch hẹn, trừ đúng số tiền, hiển thị thông báo thành công và gửi thông tin xác nhận qua SMS/Email.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết câu lệnh SQL sử dụng mệnh đề `UNION` và `UNION ALL` để gộp kết quả lấy danh sách mã người dùng (user_id) từ hai bảng `Customers` và `Employees`. Hãy phân biệt sự khác nhau giữa chúng.
* **expected_key_points:**
  - id: KP5_1
    content: Viết câu lệnh SQL chính xác
    keypoint_weight: 0.5
    description: Viết đúng cú pháp: `SELECT user_id FROM Customers UNION SELECT user_id FROM Employees` (hoặc `UNION ALL`).
  - id: KP5_2
    content: Phân biệt UNION và UNION ALL
    keypoint_weight: 0.5
    description: `UNION` tự động loại bỏ các bản ghi trùng lặp (distinct) và sắp xếp kết quả nên chạy chậm hơn. `UNION ALL` giữ nguyên toàn bộ các bản ghi trùng lặp và không sắp xếp nên chạy nhanh hơn.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách viết test assertion trong Postman để xác minh thời gian phản hồi (Response Time) của API phải nhỏ hơn 500ms.
* **expected_key_points:**
  - id: KP6_1
    content: Cú pháp viết assertion trong tab Tests
    keypoint_weight: 0.6
    description: Sử dụng hàm pm.test kết hợp thuộc tính responseTime: `pm.test("Response time is less than 500ms", function () { pm.expect(pm.response.responseTime).to.be.below(500); });`.
  - id: KP6_2
    content: Ý nghĩa việc kiểm thử thời gian phản hồi
    keypoint_weight: 0.4
    description: Đảm bảo API đáp ứng đúng yêu cầu hiệu năng cơ bản phi chức năng của hệ thống dưới tải bình thường.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Kiểm thử hiệu năng: Phân biệt sự khác nhau giữa Spike Testing (Kiểm thử đột biến tải) và Volume Testing (Kiểm thử thể tích dữ liệu lớn).
* **expected_key_points:**
  - id: KP7_1
    content: Đặc trưng Spike Testing
    keypoint_weight: 0.5
    description: Mục đích kiểm tra phản ứng của hệ thống khi lượng người dùng đồng thời tăng lên đột ngột trong thời gian rất ngắn rồi giảm nhanh.
  - id: KP7_2
    content: Đặc trưng Volume Testing
    keypoint_weight: 0.5
    description: Mục đích kiểm tra khả năng hoạt động ổn định của hệ thống khi cơ sở dữ liệu bị phình to (ví dụ database chứa hàng triệu bản ghi).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản kiểm thử cho hệ thống CRM đồng bộ danh bạ khách hàng tự động từ điện thoại của người dùng lên Cloud theo thời gian thực.
* **expected_key_points:**
  - id: KP8_1
    content: Kiểm thử luồng phát hiện thay đổi và đồng bộ
    keypoint_weight: 0.6
    description: Khi người dùng thêm, sửa hoặc xóa 1 liên hệ trong danh bạ điện thoại -> hệ thống phát hiện thay đổi và đẩy cập nhật lên Cloud ngay lập tức khi có kết nối mạng.
  - id: KP8_2
    content: Đồng bộ đa thiết bị và xử lý trùng lặp
    keypoint_weight: 0.4
    description: Nếu người dùng đăng nhập tài khoản CRM trên 2 điện thoại khác nhau và cùng sửa 1 liên hệ, hệ thống phải giải quyết xung đột thông tin (conflict resolution) dựa trên dấu thời gian mới nhất (last-write-wins).

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích lỗi không đồng nhất dữ liệu (Data Inconsistency) giữa Read-Database và Write-Database trong hệ thống sử dụng kiến trúc CQRS (Command Query Responsibility Segregation).
* **expected_key_points:**
  - id: KP9_1
    content: Nguyên nhân gây lệch dữ liệu trong CQRS
    keypoint_weight: 0.5
    description: Dữ liệu được ghi vào Write-DB nhưng cơ chế đồng bộ sang Read-DB (qua Message Queue/Replication) bị lỗi hoặc bị trễ (Sync Delay), khiến người dùng đọc thấy thông tin cũ.
  - id: KP9_2
    content: Kịch bản kiểm thử phát hiện lỗi
    keypoint_weight: 0.5
    description: Gửi request cập nhật thông tin -> gửi liên tiếp các request đọc thông tin để đo khoảng thời gian dữ liệu đồng nhất; giả lập sập kênh sync để xem hệ thống báo lỗi thế nào.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Kiểm thử bảo mật: Phát hiện lỗi phân quyền Broken Function Level Authorization (BFLA) bằng cách thay đổi URL hoặc tham số trên API.
* **expected_key_points:**
  - id: KP10_1
    content: Bản chất lỗ hổng BFLA
    keypoint_weight: 0.5
    description: Xảy ra khi server không kiểm tra quyền của người dùng đối với các chức năng nhạy cảm, chỉ ẩn nút bấm trên giao diện khiến user thường có thể gọi API quản trị nếu biết URL.
  - id: KP10_2
    content: Kịch bản kiểm thử thực tế
    keypoint_weight: 0.5
    description: Đăng nhập bằng tài khoản User thường -> lấy token -> gửi request trực tiếp đến các endpoint quản trị (ví dụ: `/api/admin/delete-user/123`). Nếu server thực hiện xóa thành công thay vì báo lỗi 403 Forbidden, hệ thống dính lỗi BFLA.

