# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1) - Tập Đề Acceptance Criteria và SQL EXISTS (14)

* **Role:** Tester
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Tiêu chí nghiệm thu (Acceptance Criteria) trong User Story là gì? Ai là người viết và vai trò của nó đối với Tester là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Khái niệm và người viết Acceptance Criteria
    keypoint_weight: 0.5
    description: Là tập hợp các điều kiện biên và yêu cầu chức năng mà sản phẩm phải thỏa mãn để được khách hàng chấp nhận nghiệm thu. Thường do Product Owner (PO) hoặc Business Analyst (BA) viết.
  - id: KP1_2
    content: Vai trò đối với Tester
    keypoint_weight: 0.5
    description: Là căn cứ chính xác để Tester thiết kế các kịch bản kiểm thử nghiệm thu (Acceptance Test Cases) nhằm quyết định User Story đã hoàn thành chưa.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày kỹ thuật đoán lỗi (Error Guessing) trong kiểm thử phần mềm. Khi nào kỹ thuật này phát huy hiệu quả tốt nhất?
* **expected_key_points:**
  - id: KP2_1
    content: Nguyên lý kỹ thuật đoán lỗi
    keypoint_weight: 0.5
    description: Là kỹ thuật hộp đen dựa trên kinh nghiệm, kiến thức về hệ thống và trực giác của Tester để dự đoán các vùng code dễ xảy ra lỗi và thiết kế test case tập trung.
  - id: KP2_2
    content: Điều kiện phát huy hiệu quả
    keypoint_weight: 0.5
    description: Phát huy tốt nhất khi Tester đã có nhiều kinh nghiệm kiểm thử hệ thống tương tự, hiểu rõ thói quen viết code của lập trình viên và các lỗi thường gặp trong lịch sử dự án.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa hai HTTP Method: GET và POST khi gửi dữ liệu lên server.
* **expected_key_points:**
  - id: KP3_1
    content: Đặc trưng của phương thức GET
    keypoint_weight: 0.5
    description: Dùng để lấy dữ liệu từ server, tham số gửi đi hiển thị trực tiếp trên thanh địa chỉ URL (Query String), bị giới hạn độ dài và có thể lưu cache/lịch sử.
  - id: KP3_2
    content: Đặc trưng của phương thức POST
    keypoint_weight: 0.5
    description: Dùng để gửi dữ liệu lên server để tạo mới tài nguyên, tham số nằm ẩn trong Request Body, không giới hạn độ dài và bảo mật hơn GET.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết kịch bản kiểm thử (Test Scenario) cho chức năng xuất báo cáo tài chính định kỳ theo tuần/tháng/quý của một hệ thống quản lý ERP.
* **expected_key_points:**
  - id: KP4_1
    content: Kiểm thử độ chính xác số liệu báo cáo
    keypoint_weight: 0.5
    description: Xác minh số liệu trên file báo cáo xuất ra khớp hoàn toàn với dữ liệu thực tế trong DB tại thời điểm tương ứng; kiểm tra công thức tính tổng và lọc theo thời gian.
  - id: KP4_2
    content: Kiểm thử định dạng báo cáo và phân quyền
    keypoint_weight: 0.5
    description: Kiểm tra hiển thị biểu đồ, định dạng cột tiền tệ; xác minh chỉ những người dùng có quyền quản trị tài chính (Role) mới xuất được báo cáo.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết câu lệnh SQL sử dụng toán tử `EXISTS` để liệt kê thông tin của tất cả khách hàng (Customers) có ít nhất một đơn hàng (Orders) được tạo trong năm 2026.
* **expected_key_points:**
  - id: KP5_1
    content: Cú pháp SQL sử dụng EXISTS
    keypoint_weight: 0.6
    description: Viết câu lệnh: `SELECT * FROM Customers c WHERE EXISTS (SELECT 1 FROM Orders o WHERE o.customer_id = c.id AND o.order_date >= '2026-01-01')`.
  - id: KP5_2
    content: Tối ưu hóa câu lệnh con
    keypoint_weight: 0.4
    description: Sử dụng `SELECT 1` hoặc `SELECT *` trong truy vấn con của EXISTS để kiểm tra sự tồn tại (hiệu năng tối ưu vì dừng lại ngay khi tìm thấy bản ghi đầu tiên khớp).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách sử dụng tính năng Geolocation Mocking trong Chrome DevTools để giả lập thiết bị đang ở các vị trí địa lý khác nhau phục vụ kiểm thử ứng dụng bản đồ.
* **expected_key_points:**
  - id: KP6_1
    content: Cách mở bảng Console Sensors
    keypoint_weight: 0.5
    description: F12 -> click icon 3 chấm ở góc trên bên phải DevTools -> chọn More tools -> chọn Sensors.
  - id: KP6_2
    content: Giả lập và chọn tọa độ
    keypoint_weight: 0.5
    description: Trong mục Geolocation, chọn các thành phố có sẵn (như Tokyo, London) hoặc chọn Custom location rồi nhập tọa độ Latitude và Longitude tùy ý để xem trang web hiển thị nội dung theo vị trí đó.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Kiểm thử độ bền (Endurance Testing) là gì và làm thế nào để Tester thiết lập kịch bản kiểm thử độ bền cho một ứng dụng Backend?
* **expected_key_points:**
  - id: KP7_1
    content: Định nghĩa Endurance Testing
    keypoint_weight: 0.5
    description: Là loại kiểm thử phi chức năng thực hiện chạy hệ thống dưới mức tải bình thường trong một khoảng thời gian dài liên tục (ví dụ 24/7 hoặc 48 giờ) để phát hiện lỗi tích lũy.
  - id: KP7_2
    content: Thiết lập kịch bản kiểm thử
    keypoint_weight: 0.5
    description: Sử dụng tool tự động gửi request đều đặn trong thời gian dài; giám sát rò rỉ tài nguyên (memory leak, database connection leak, storage full).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản kiểm thử tích hợp cho hệ thống đặt đồ ăn trực tuyến (Food Delivery) có sự tham gia của 3 bên: Khách hàng (User App), Cửa hàng (Merchant Web), và Tài xế (Driver App).
* **expected_key_points:**
  - id: KP8_1
    content: Luồng tương tác tích hợp toàn trình (End-to-End)
    keypoint_weight: 0.6
    description: Khách đặt đơn -> Cửa hàng nhận đơn và chuẩn bị -> Tài xế nhận đơn và đi giao -> Khách nhận hàng thành công. Xác minh dữ liệu đồng bộ tức thời giữa 3 nền tảng qua WebSocket/Push Notification.
  - id: KP8_2
    content: Xử lý các tình huống hủy đơn đột ngột
    keypoint_weight: 0.4
    description: Kiểm thử luồng hủy đơn bởi khách hàng khi tài xế đã lấy hàng; hoặc cửa hàng từ chối đơn hàng do hết món; đảm bảo hoàn tiền và thông báo đúng trạng thái cho các bên.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích nguyên nhân và cách kiểm thử lỗi tràn bộ nhớ (Out of Memory - OOM) của Java Virtual Machine (JVM) chạy ứng dụng server.
* **expected_key_points:**
  - id: KP9_1
    content: Nguyên nhân gây ra OOM trên JVM
    keypoint_weight: 0.5
    description: Do cấp phát quá nhiều đối tượng lớn mà không được Garbage Collector thu hồi (rò rỉ bộ nhớ), cấu hình Heap Size quá nhỏ, hoặc xử lý file dung lượng lớn trực tiếp trên bộ nhớ.
  - id: KP9_2
    content: Cách kiểm thử phát hiện lỗi
    keypoint_weight: 0.5
    description: Gửi các file dung lượng lớn vượt giới hạn cấu hình; tăng tải lượng truy cập đồng thời đột biến; thu thập Heap Dump bằng jmap và phân tích bằng Eclipse Memory Analyzer (MAT).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Kiểm thử bảo mật: Phân tích lỗ hổng XML External Entity (XXE) và cách kiểm tra lỗi này trên hệ thống API nhận payload dữ liệu XML.
* **expected_key_points:**
  - id: KP10_1
    content: Bản chất lỗ hổng XXE
    keypoint_weight: 0.5
    description: Xảy ra khi ứng dụng phân tích cú pháp XML (XML Parser) cấu hình không an toàn, cho phép tham chiếu đến các thực thể bên ngoài (external entities) để truy cập file hệ thống hoặc tấn công mạng nội bộ.
  - id: KP10_2
    content: Cách thức kiểm thử thủ công
    keypoint_weight: 0.5
    description: Gửi request chứa payload XML định nghĩa ENTITY trỏ đến file nhạy cảm (ví dụ: `<!ENTITY xxe SYSTEM "file:///etc/passwd">`). Nếu API trả về nội dung file đó trong response body, hệ thống dính lỗ hổng XXE.

