# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1) - Tập Đề Entry/Exit Criteria và SQL Correlated Subquery (20)

* **Role:** Tester
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Khái niệm Entry Criteria (Tiêu chí bắt đầu) và Exit Criteria (Tiêu chí kết thúc) của một giai đoạn kiểm thử là gì? Cho ví dụ.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa và ví dụ Entry Criteria
    keypoint_weight: 0.5
    description: Là các điều kiện cần thiết phải thỏa mãn trước khi bắt đầu giai đoạn test (ví dụ: có đủ tài liệu test case được duyệt, môi trường test đã sẵn sàng, đã build code xong).
  - id: KP1_2
    content: Định nghĩa và ví dụ Exit Criteria
    keypoint_weight: 0.5
    description: Là các điều kiện bắt buộc phải đạt được trước khi kết thúc giai đoạn test (ví dụ: 100% test case đã chạy, không còn bug nghiêm trọng mức Critical/Blocker chưa sửa).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa White Box Testing (Kiểm thử hộp trắng) và Structural Testing (Kiểm thử cấu trúc).
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm White Box Testing
    keypoint_weight: 0.5
    description: Là phương pháp kiểm thử dựa trên việc đọc hiểu cấu trúc logic code bên trong, thiết kế test case dựa trên thuật toán và các nhánh rẻ của code.
  - id: KP2_2
    content: Khái niệm Structural Testing
    keypoint_weight: 0.5
    description: Là một tên gọi khác hoặc tập con của White Box, tập trung đo lường độ bao phủ (coverage) cấu trúc hệ thống (câu lệnh, nhánh, quyết định) bởi các test case.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Mã trạng thái HTTP 201 Created và HTTP 204 No Content khác nhau như thế nào? Nêu thời điểm sử dụng từng mã khi kiểm thử API.
* **expected_key_points:**
  - id: KP3_1
    content: Phân biệt ý nghĩa hai mã lỗi
    keypoint_weight: 0.5
    description: HTTP 201 biểu thị yêu cầu thành công và một tài nguyên mới đã được tạo ra. HTTP 204 biểu thị yêu cầu thành công nhưng không có nội dung nào trả về trong response body.
  - id: KP3_2
    content: Thời điểm sử dụng thực tế
    keypoint_weight: 0.5
    description: Dùng 201 sau khi gọi API POST tạo user mới thành công. Dùng 204 sau khi gọi API DELETE xóa user thành công hoặc API PUT cập nhật mà không cần trả về data.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết kịch bản kiểm thử (Test Scenario) cho tính năng tính toán phí vận chuyển tự động trong giỏ hàng dựa trên khoảng cách địa lý (tích hợp API Google Maps).
* **expected_key_points:**
  - id: KP4_1
    content: Kiểm thử tính toán khoảng cách và giá tiền
    keypoint_weight: 0.5
    description: Nhập địa chỉ giao hàng hợp lệ -> Google Maps API trả về khoảng cách chính xác -> hệ thống tính phí vận chuyển đúng theo bảng giá quy định (ví dụ: 5,000 VND/km).
  - id: KP4_2
    content: Kiểm thử lỗi kết nối địa lý và địa chỉ lạ
    keypoint_weight: 0.5
    description: Nhập địa chỉ không tồn tại/địa chỉ nước ngoài -> hệ thống báo lỗi rõ ràng; giả lập API Google Maps bị timeout/lỗi -> hệ thống tự chuyển sang tính phí đồng giá mặc định.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết câu lệnh SQL truy vấn sử dụng Correlated Subquery (Truy vấn con tương quan) để tìm ra những nhân viên có mức lương (salary) cao hơn mức lương trung bình của phòng ban (department_id) mà họ đang làm việc.
* **expected_key_points:**
  - id: KP5_1
    content: Cú pháp Correlated Subquery chính xác
    keypoint_weight: 0.6
    description: Viết câu lệnh dạng: `SELECT * FROM Employees e WHERE salary > (SELECT AVG(salary) FROM Employees WHERE department_id = e.department_id)`.
  - id: KP5_2
    content: Cơ chế hoạt động tương quan
    keypoint_weight: 0.4
    description: Đảm bảo truy vấn con tham chiếu trực tiếp đến giá trị `e.department_id` từ bảng ngoài để tính lương trung bình riêng cho từng phòng ban.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách sử dụng tab Security trong Chrome DevTools để kiểm tra thông tin chứng chỉ bảo mật SSL/TLS của trang web bạn đang kiểm thử.
* **expected_key_points:**
  - id: KP6_1
    content: Định vị tab Security
    keypoint_weight: 0.4
    description: F12 -> chọn tab Security trên menu chính (nếu không thấy thì click dấu >> để mở rộng).
  - id: KP6_2
    content: Xác minh thông tin bảo mật
    keypoint_weight: 0.6
    description: Xem trạng thái kết nối có an toàn không (HTTPS), kiểm tra nhà phát hành chứng chỉ (Certificate Authority - CA), thời hạn hiệu lực của chứng chỉ và giao thức mã hóa TLS sử dụng.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt sự khác nhau giữa Kiểm thử hiệu năng (Performance Testing) và Kiểm thử chức năng (Functional Testing) về mục tiêu và kết quả kỳ vọng.
* **expected_key_points:**
  - id: KP7_1
    content: Khác biệt về mục tiêu kiểm thử
    keypoint_weight: 0.5
    description: Functional Testing tập trung vào tính đúng đắn của nghiệp vụ (chức năng có chạy đúng không). Performance Testing tập trung vào tốc độ phản hồi và độ ổn định của hệ thống dưới các mức tải khác nhau.
  - id: KP7_2
    content: Khác biệt về kết quả mong đợi
    keypoint_weight: 0.5
    description: Functional kỳ vọng đầu ra khớp thiết kế. Performance kỳ vọng thời gian phản hồi thấp (ví dụ <2s), CPU/RAM dưới ngưỡng giới hạn và không sập hệ thống.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản kiểm thử tích hợp (Integration Test) cho hệ thống Nhà thông minh (Smart Home) điều khiển điều hòa, đèn chiếu sáng, và khóa cửa thông qua ứng dụng di động kết nối với IoT Hub trung tâm.
* **expected_key_points:**
  - id: KP8_1
    content: Kiểm thử truyền nhận lệnh điều khiển
    keypoint_weight: 0.6
    description: Nhấn nút bật/tắt thiết bị trên app di động -> lệnh truyền qua IoT Hub -> thiết bị thực tế thay đổi trạng thái và gửi phản hồi trạng thái mới về app hiển thị đúng trong vòng dưới 1 giây.
  - id: KP8_2
    content: Kiểm thử mất kết nối và đồng bộ cục bộ
    keypoint_weight: 0.4
    description: Kiểm thử điều khiển khi điện thoại mất mạng internet nhưng kết nối cùng mạng Wifi nội bộ với IoT Hub (chế độ LAN control); kiểm tra đồng bộ trạng thái khi thiết bị tắt nguồn đột ngột.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích rủi ro hệ thống và kịch bản kiểm thử phục hồi sau thảm họa (Disaster Recovery Testing) khi trung tâm dữ liệu chính (Primary Data Center) bị sập hoàn toàn và phải chuyển đổi sang trung tâm dữ liệu dự phòng (DR Site).
* **expected_key_points:**
  - id: KP9_1
    content: Kiểm thử luồng kích hoạt chuyển đổi (Failover flow)
    keypoint_weight: 0.6
    description: Xác minh khi ngắt kết nối trung tâm dữ liệu chính đột ngột, hệ thống giám sát tự động kích hoạt chuyển hướng toàn bộ traffic sang DR Site trong thời gian cho phép (RTO) mà không làm mất phiên làm việc của người dùng.
  - id: KP9_2
    content: Đảm bảo điểm phục hồi dữ liệu (RPO)
    keypoint_weight: 0.4
    description: Truy vấn và đối chiếu dữ liệu tại DR Site sau khi failover để đảm bảo lượng dữ liệu bị mất (nếu có) nằm trong giới hạn cho phép của RPO.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Kiểm thử bảo mật: Trình bày cách kiểm tra và khai thác lỗ hổng bảo mật liên quan đến phiên làm việc: Session Fixation và Session Hijacking trên ứng dụng web.
* **expected_key_points:**
  - id: KP10_1
    content: Kiểm thử Session Fixation (Cố định phiên)
    keypoint_weight: 0.5
    description: Lấy Session ID trước khi đăng nhập -> Đăng nhập thành công -> Kiểm tra xem Session ID có được thay đổi mới hoàn toàn không. Nếu Session ID giữ nguyên, hệ thống dính lỗi Session Fixation.
  - id: KP10_2
    content: Kiểm thử Session Hijacking (Cướp phiên)
    keypoint_weight: 0.5
    description: Đăng nhập bên máy A -> sao chép Session Cookie -> paste vào trình duyệt bên máy B và F5. Nếu máy B đăng nhập thành công vào tài khoản mà không cần nhập username/password, hệ thống dính lỗi cướp phiên do thiếu cờ bảo mật.

