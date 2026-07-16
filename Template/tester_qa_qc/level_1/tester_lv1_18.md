# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1) - Tập Đề Defect Leakage và SQL Subquery nâng cao (18)

* **Role:** Tester
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Định nghĩa chỉ số lọt lỗi (Defect Leakage). Viết công thức tính và giải thích ý nghĩa của nó đối với đội ngũ QC.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa và công thức
    keypoint_weight: 0.6
    description: Là tỷ lệ lỗi bị bỏ sót trong giai đoạn kiểm thử và chỉ được phát hiện bởi khách hàng trên môi trường Production. Công thức: `Defect Leakage = (Số lỗi phát hiện ở Production / Tổng số lỗi phát hiện ở UAT & Production) * 100%`.
  - id: KP1_2
    content: Ý nghĩa đối với QC
    keypoint_weight: 0.4
    description: Đo lường mức độ hiệu quả của quy trình kiểm thử và chất lượng của bộ test case; tỷ lệ này càng thấp chứng tỏ QC test càng kỹ.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Bảng quyết định (Decision Table) giúp giải quyết vấn đề gì trong thiết kế test case chức năng?
* **expected_key_points:**
  - id: KP2_1
    content: Vấn đề giải quyết
    keypoint_weight: 0.5
    description: Giúp bao phủ toàn bộ các trường hợp kết hợp logic phức tạp của dữ liệu đầu vào mà nếu viết test case thông thường dễ bị bỏ sót các trường hợp biên hoặc phi logic.
  - id: KP2_2
    content: Hiệu quả trình bày
    keypoint_weight: 0.5
    description: Giúp trình bày các quy tắc nghiệp vụ rõ ràng dưới dạng bảng để cả Dev, BA và Tester dễ dàng đối chiếu và thống nhất hành vi hệ thống.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Nêu 2 câu lệnh cơ bản trong MySQL dùng để quản lý cấu trúc bảng cơ sở dữ liệu (DDL) kèm ví dụ.
* **expected_key_points:**
  - id: KP3_1
    content: Câu lệnh CREATE TABLE
    keypoint_weight: 0.5
    description: Dùng để tạo bảng mới trong database kèm định nghĩa tên cột và kiểu dữ liệu (ví dụ: `CREATE TABLE users (id INT, name VARCHAR(50))`)
  - id: KP3_2
    content: Câu lệnh ALTER TABLE
    keypoint_weight: 0.5
    description: Dùng để sửa đổi cấu trúc bảng đang tồn tại (thêm/xóa cột, đổi kiểu dữ liệu) (ví dụ: `ALTER TABLE users ADD email VARCHAR(100)`)

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết kịch bản kiểm thử (Test Scenario) cho tính năng xem bản đồ dẫn đường (GPS định vị vị trí hiện tại, tính toán lộ trình di chuyển, hiển thị thời gian dự kiến đến).
* **expected_key_points:**
  - id: KP4_1
    content: Kiểm thử định vị GPS và vẽ lộ trình
    keypoint_weight: 0.5
    description: Xác minh app định vị chính xác vị trí hiện tại trên bản đồ; nhập điểm đến -> vẽ đường đi tối ưu kèm thông số khoảng cách và thời gian dự kiến đến (ETA).
  - id: KP4_2
    content: Kiểm thử đi sai hướng và mất sóng
    keypoint_weight: 0.5
    description: Kiểm tra khi tài xế đi lệch lộ trình vẽ sẵn -> bản đồ tự động tính toán lại đường đi mới (Rerouting); kiểm tra khi đi vào đường hầm mất sóng GPS.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết câu lệnh SQL để truy vấn và tìm ra bản ghi có giá trị lớn thứ hai (ví dụ mức lương lớn thứ hai từ bảng Employees) mà không sử dụng mệnh đề LIMIT.
* **expected_key_points:**
  - id: KP5_1
    content: Sử dụng truy vấn con lồng nhau
    keypoint_weight: 0.6
    description: Viết câu lệnh SELECT giá trị MAX nhỏ hơn giá trị MAX tuyệt đối: `SELECT MAX(salary) FROM Employees WHERE salary < (SELECT MAX(salary) FROM Employees)`.
  - id: KP5_2
    content: Tính bao quát của câu lệnh
    keypoint_weight: 0.4
    description: Đảm bảo câu lệnh hoạt động chính xác ngay cả khi có nhiều bản ghi có cùng giá trị lớn nhất.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách sử dụng tab Network trong Chrome DevTools để xuất (export) file HAR chứa toàn bộ lịch sử request phục vụ cho việc gửi thông tin lỗi chi tiết cho lập trình viên.
* **expected_key_points:**
  - id: KP6_1
    content: Thao tác xuất file HAR
    keypoint_weight: 0.5
    description: F12 -> tab Network -> click chuột phải vào bất kỳ request nào trong danh sách -> chọn 'Save all as HAR with content' để tải file về máy.
  - id: KP6_2
    content: Giá trị của file HAR đối với Dev
    keypoint_weight: 0.5
    description: File HAR chứa đầy đủ thông tin về request/response headers, cookies, payload dữ liệu và thời gian tải giúp dev dễ dàng import lại để tái hiện lỗi.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt sự khác nhau giữa Re-testing (Kiểm thử lại) và Smoke Testing về mục đích và đối tượng kiểm thử.
* **expected_key_points:**
  - id: KP7_1
    content: Khác biệt về mục đích
    keypoint_weight: 0.5
    description: Re-testing kiểm tra xem một lỗi cụ thể đã được sửa thành công hay chưa. Smoke Testing kiểm tra xem build mới có đủ ổn định để thực hiện kiểm thử sâu hay không.
  - id: KP7_2
    content: Khác biệt về đối tượng và phạm vi
    keypoint_weight: 0.5
    description: Re-testing chỉ chạy lại các test case bị lỗi trước đó. Smoke Testing chạy một tập hợp các test case quan trọng bao phủ toàn bộ hệ thống.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản kiểm thử bảo mật cho ứng dụng chat nhóm có tích hợp mã hóa đầu cuối (End-to-End Encryption - E2EE) đảm bảo bảo mật nội dung tin nhắn gửi đi.
* **expected_key_points:**
  - id: KP8_1
    content: Xác minh mã hóa tin nhắn tại thiết bị gửi
    keypoint_weight: 0.5
    description: Kiểm tra xem tin nhắn có được mã hóa ngay tại thiết bị gửi trước khi truyền đi qua mạng không (nội dung lưu ở server trung gian bắt buộc phải là chuỗi mã hóa vô nghĩa).
  - id: KP8_2
    content: Xác minh giải mã tại thiết bị nhận
    keypoint_weight: 0.5
    description: Chỉ thiết bị của người nhận nằm trong nhóm chat có khóa giải mã (private key) mới hiển thị được nội dung text thuần; kiểm tra khi thay đổi thiết bị nhận.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích rủi ro hệ thống và kịch bản kiểm thử khi thay đổi cấu trúc dữ liệu cơ sở dữ liệu NoSQL (như MongoDB) từ dạng không ràng buộc sang có schema ràng buộc (Schema Validation).
* **expected_key_points:**
  - id: KP9_1
    content: Kiểm thử tính tương thích dữ liệu cũ
    keypoint_weight: 0.5
    description: Xác minh các bản ghi cũ không tuân thủ schema mới có gây lỗi crash hệ thống khi đọc dữ liệu hay không, và kịch bản xử lý dữ liệu legacy.
  - id: KP9_2
    content: Kiểm thử ghi dữ liệu mới theo schema
    keypoint_weight: 0.5
    description: Kiểm tra ghi thành công khi dữ liệu tuân thủ schema; chặn ghi và báo lỗi chính xác khi thiếu trường bắt buộc hoặc sai kiểu dữ liệu theo schema mới.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Kiểm thử bảo mật: Cách phát hiện lỗ hổng SSRF (Server-Side Request Forgery) thông qua tính năng xuất/chuyển đổi file từ URL (ví dụ: HTML to PDF, Image Converter).
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế khai thác SSRF qua bộ convert
    keypoint_weight: 0.5
    description: Kẻ tấn công truyền các địa chỉ IP nội bộ hoặc schema đặc biệt (`file://`, `gopher://`) vào tham số URL để bắt server tải file nội bộ hoặc tương tác với cổng dịch vụ nội bộ.
  - id: KP10_2
    content: Thiết kế kịch bản kiểm thử
    keypoint_weight: 0.5
    description: Nhập URL dạng `file:///etc/passwd` hoặc `http://169.254.169.254/latest/meta-data/` (AWS metadata) vào ô convert. Nếu file PDF xuất ra hiển thị thông tin nhạy cảm của server, hệ thống dính lỗi.

