# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1) - Tập Đề Alpha/Beta Testing và SQL DELETE (10)

* **Role:** Tester
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Thế nào là "Test Scenario" (Kịch bản kiểm thử) và nó khác gì với "Test Case"? Nêu ví dụ.
* **expected_key_points:**
  - id: KP1_1
    content: Khái niệm Test Scenario
    keypoint_weight: 0.5
    description: Là một phân loại cấp cao mô tả những gì cần kiểm thử (ví dụ: Kiểm thử tính năng đăng nhập bằng thẻ tín dụng). Một Test Scenario có thể bao gồm nhiều Test Case.
  - id: KP1_2
    content: Khái niệm Test Case
    keypoint_weight: 0.5
    description: Là tài liệu chi tiết mô tả các bước thực hiện cụ thể, dữ liệu đầu vào và kết quả mong đợi (ví dụ: Test Case đăng nhập thẻ tín dụng hết hạn, thẻ đúng định dạng).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa hai hình thức kiểm thử: Alpha Testing và Beta Testing.
* **expected_key_points:**
  - id: KP2_1
    content: Đặc điểm Alpha Testing
    keypoint_weight: 0.5
    description: Thực hiện ở giai đoạn cuối của dự án bởi đội ngũ Tester và nhân viên nội bộ của công ty phát triển ngay tại môi trường phát triển (staging/lab).
  - id: KP2_2
    content: Đặc điểm Beta Testing
    keypoint_weight: 0.5
    description: Thực hiện sau Alpha Testing bởi chính người dùng cuối (end-users) ngoài thực tế trên môi trường của họ để nhận phản hồi trước khi phát hành chính thức.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong SQL, câu lệnh DELETE và TRUNCATE khác nhau như thế nào khi dùng để xóa dữ liệu?
* **expected_key_points:**
  - id: KP3_1
    content: Bản chất câu lệnh DELETE
    keypoint_weight: 0.5
    description: DELETE là lệnh DML, xóa từng dòng dữ liệu dựa trên điều kiện WHERE, có ghi logs chi tiết nên có thể rollback và chạy chậm hơn đối với bảng lớn.
  - id: KP3_2
    content: Bản chất câu lệnh TRUNCATE
    keypoint_weight: 0.5
    description: TRUNCATE là lệnh DDL, xóa toàn bộ các dòng trong bảng bằng cách giải phóng các trang dữ liệu, không dùng điều kiện WHERE, ghi log tối giản và chạy nhanh.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi kiểm thử API, làm thế nào để đọc và xác minh cấu trúc dữ liệu JSON trả về so với XML?
* **expected_key_points:**
  - id: KP4_1
    content: Đọc cấu trúc JSON và XML
    keypoint_weight: 0.5
    description: JSON tổ chức theo cặp key-value và mảng dữ liệu. XML dùng các thẻ mở/đóng dạng lồng nhau để lưu dữ liệu.
  - id: KP4_2
    content: Xác minh cấu trúc dữ liệu (Schema Validation)
    keypoint_weight: 0.5
    description: Kiểm tra tính đúng đắn của kiểu dữ liệu (chuỗi, số, boolean) và sự hiện diện của các thuộc tính bắt buộc bằng JSON Schema Validator hoặc XML DTD/XSD.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết kịch bản kiểm thử cho tính năng nhập dữ liệu (Import) danh sách học sinh từ file Excel (.xlsx) vào hệ thống quản lý trường học.
* **expected_key_points:**
  - id: KP5_1
    content: Kiểm thử định dạng file và dữ liệu hợp lệ
    keypoint_weight: 0.5
    description: Import file Excel đúng mẫu, đầy đủ dữ liệu -> hệ thống ghi nhận thành công và hiển thị đúng danh sách trên màn hình UI.
  - id: KP5_2
    content: Kiểm thử các trường hợp file lỗi và rỗng
    keypoint_weight: 0.5
    description: Import file trống, file sai mẫu cột, file chứa dòng dữ liệu lỗi định dạng (ví dụ ngày sinh sai cấu trúc) -> hệ thống báo lỗi chi tiết ở dòng nào để người dùng sửa.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách sử dụng tab Application trong Chrome DevTools để xem và chỉnh sửa dữ liệu lưu ở Local Storage và Session Storage.
* **expected_key_points:**
  - id: KP6_1
    content: Định vị Local/Session Storage trong DevTools
    keypoint_weight: 0.5
    description: F12 -> tab Application -> menu bên trái mở rộng mục Storage -> click chọn Local Storage hoặc Session Storage tương ứng với tên miền trang web.
  - id: KP6_2
    content: Thao tác xem và sửa đổi dữ liệu
    keypoint_weight: 0.5
    description: Xem danh sách các cặp Key-Value; click đúp để chỉnh sửa giá trị của một Key (ví dụ thay đổi giá trị cờ flag đăng nhập) hoặc xóa key để kiểm tra phản ứng của web.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế test case cho tính năng tìm kiếm sản phẩm theo khoảng giá từ min_price đến max_price.
* **expected_key_points:**
  - id: KP7_1
    content: Kiểm thử khoảng giá hợp lệ
    keypoint_weight: 0.5
    description: Nhập min_price < max_price (ví dụ 100 đến 500) -> kiểm tra sản phẩm trả về có giá nằm đúng trong khoảng đó.
  - id: KP7_2
    content: Kiểm thử các giá trị biên và phi logic
    keypoint_weight: 0.5
    description: Nhập min_price = max_price; nhập min_price > max_price; để trống một trong hai ô hoặc nhập số âm.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản kiểm thử cho hệ thống ví điện tử có tính năng hoàn tiền (Refund) một phần hoặc toàn bộ số tiền đơn hàng sau khi thanh toán thành công.
* **expected_key_points:**
  - id: KP8_1
    content: Kiểm tra tính toán số tiền hoàn và số dư ví
    keypoint_weight: 0.6
    description: Xác minh số tiền hoàn đúng bằng số tiền yêu cầu hoàn (không vượt quá giá trị đơn gốc), số dư ví người dùng tăng đúng lượng và tài khoản của shop bị trừ đúng lượng tương ứng.
  - id: KP8_2
    content: Kiểm thử trạng thái giao dịch và bảo mật hoàn tiền
    keypoint_weight: 0.4
    description: Đảm bảo đơn hàng đã hoàn tiền toàn bộ không được phép yêu cầu hoàn tiếp; kiểm thử hoàn tiền đồng thời (Concurrency Refund) để tránh lỗi nhân đôi số tiền hoàn.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Làm thế nào để kiểm thử hệ thống sử dụng kiến trúc Hướng Sự Kiện (Event-Driven Architecture) để đảm bảo các sự kiện (Events) được xử lý đúng thứ tự?
* **expected_key_points:**
  - id: KP9_1
    content: Kiểm tra tính tuần tự của sự kiện (Event Sequencing)
    keypoint_weight: 0.6
    description: Xác minh hệ thống xử lý các event theo đúng thứ tự được tạo ra (ví dụ: Event 'Tạo đơn hàng' -> Event 'Thanh toán' -> Event 'Giao hàng') thông qua cơ chế phân vùng/key của Queue (như Kafka Partition Key).
  - id: KP9_2
    content: Kiểm thử trường hợp mất thứ tự hoặc sự kiện trùng lặp
    keypoint_weight: 0.4
    description: Giả lập sự kiện đến muộn hoặc gửi lặp lại (Idempotency) để kiểm tra xem hệ thống có xử lý lỗi hoặc bỏ qua một cách an toàn không.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Kiểm thử bảo mật: Trình bày cơ chế phát hiện lỗ hổng SSRF (Server-Side Request Forgery) trên các chức năng tải ảnh từ URL do người dùng cung cấp.
* **expected_key_points:**
  - id: KP10_1
    content: Nguyên lý lỗ hổng SSRF
    keypoint_weight: 0.5
    description: Xảy ra khi ứng dụng nhận một URL từ client và thực hiện tải tài nguyên từ URL đó mà không validate, cho phép kẻ tấn công yêu cầu server gửi request nội bộ đến chính nó hoặc mạng LAN.
  - id: KP10_2
    content: Kịch bản kiểm thử phát hiện lỗ hổng
    keypoint_weight: 0.5
    description: Truyền các địa chỉ nội bộ như `http://localhost:8080` hoặc `http://192.168.1.1` vào ô nhập URL tải ảnh. Nếu server trả về thông tin hệ thống nội bộ hoặc quét được cổng mở, hệ thống bị dính lỗi SSRF.

