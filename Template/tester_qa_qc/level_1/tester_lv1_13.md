# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1) - Tập Đề Test Coverage và SQL CASE WHEN (13)

* **Role:** Tester
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Độ bao phủ kiểm thử (Test Coverage) là gì? Hãy nêu 2 chỉ số đo lường độ bao phủ kiểm thử phổ biến trong dự án.
* **expected_key_points:**
  - id: KP1_1
    content: Khái niệm Test Coverage
    keypoint_weight: 0.5
    description: Là thước đo đánh giá tỷ lệ các phần của phần mềm (mã nguồn, yêu cầu, luồng nghiệp vụ) được thực thi bởi các kịch bản kiểm thử.
  - id: KP1_2
    content: Hai chỉ số đo lường phổ biến
    keypoint_weight: 0.5
    description: Nêu được: Requirements Coverage (Bao phủ yêu cầu) và Code Coverage (Bao phủ dòng lệnh/nhánh code) kèm cách tính cơ bản.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa Static Code Analysis (Phân tích mã tĩnh) và Dynamic Testing (Kiểm thử động).
* **expected_key_points:**
  - id: KP2_1
    content: Đặc trưng Static Code Analysis
    keypoint_weight: 0.5
    description: Thực hiện kiểm tra mã nguồn, cấu trúc hoặc tài liệu mà không cần chạy chương trình (ví dụ: dùng tool SonarQube, review code).
  - id: KP2_2
    content: Đặc trưng Dynamic Testing
    keypoint_weight: 0.5
    description: Thực hiện chạy chương trình, nhập dữ liệu đầu vào và kiểm tra kết quả đầu ra thực tế so với kỳ vọng (chạy test cases).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** API Header là gì? Hãy liệt kê 3 HTTP Headers phổ biến thường gặp nhất trong quá trình gửi request kiểm thử API.
* **expected_key_points:**
  - id: KP3_1
    content: Khái niệm API Header
    keypoint_weight: 0.4
    description: Là phần chứa siêu dữ liệu (metadata) đi kèm với request hoặc response để gửi thông tin cấu hình, xác thực, loại nội dung.
  - id: KP3_2
    content: Liệt kê 3 Headers phổ biến
    keypoint_weight: 0.6
    description: Chỉ ra được: `Content-Type` (định dạng payload), `Authorization` (token xác thực), và `Accept` (định dạng mong muốn nhận về) hoặc `User-Agent`.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết kịch bản kiểm thử cho tính năng giỏ hàng thương mại điện tử (Shopping Cart) tích hợp quản lý số lượng tồn kho.
* **expected_key_points:**
  - id: KP4_1
    content: Kiểm thử tăng giảm số lượng sản phẩm
    keypoint_weight: 0.5
    description: Kiểm tra thêm sản phẩm vào giỏ, thay đổi số lượng, xóa sản phẩm, giá tổng đơn hàng tự động tính toán lại chính xác.
  - id: KP4_2
    content: Ràng buộc số lượng tồn kho (Stock limit)
    keypoint_weight: 0.5
    description: Kiểm tra không cho phép chọn số lượng vượt quá số lượng tồn kho của cửa hàng; hiển thị thông báo hết hàng khi số lượng tồn kho bằng 0.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết câu lệnh SQL sử dụng biểu thức điều kiện `CASE WHEN` để phân loại khách hàng dựa trên số tiền chi tiêu (total_spent) từ bảng `Customers`: Nếu total_spent > 1000 thì loại 'VIP', ngược lại thì loại 'Regular'.
* **expected_key_points:**
  - id: KP5_1
    content: Cú pháp CASE WHEN chính xác
    keypoint_weight: 0.6
    description: Viết câu lệnh SELECT chứa biểu thức `CASE WHEN total_spent > 1000 THEN 'VIP' ELSE 'Regular' END AS customer_tier`.
  - id: KP5_2
    content: Ràng buộc kết thúc biểu thức
    keypoint_weight: 0.4
    description: Đảm bảo biểu thức bắt đầu bằng `CASE` và kết thúc bằng từ khóa `END` kèm bí danh cột phù hợp.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách sử dụng tab Tests trong Postman để viết mã JavaScript tự động kiểm tra xem status code trả về có phải là 200 OK và thuộc tính `success` trong response body có giá trị là `true` hay không.
* **expected_key_points:**
  - id: KP6_1
    content: Viết test case kiểm tra Status Code
    keypoint_weight: 0.5
    description: Sử dụng cú pháp: `pm.test("Status code is 200", function () { pm.response.to.have.status(200); });`.
  - id: KP6_2
    content: Viết test case kiểm tra Response Body
    keypoint_weight: 0.5
    description: Sử dụng cú pháp parse JSON body: `var jsonData = pm.response.json(); pm.test("Success is true", function () { pm.expect(jsonData.success).to.eql(true); });`.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt giữa Sanity Testing và Regression Testing về mục tiêu và phạm vi kiểm thử.
* **expected_key_points:**
  - id: KP7_1
    content: Đặc trưng Sanity Testing
    keypoint_weight: 0.5
    description: Tập trung kiểm thử nhanh, có mục tiêu rất hẹp nhằm xác minh chức năng vừa sửa lỗi hoặc sửa đổi nhỏ hoạt động bình thường, không đi sâu chi tiết.
  - id: KP7_2
    content: Đặc trưng Regression Testing
    keypoint_weight: 0.5
    description: Kiểm thử trên phạm vi rộng hơn nhằm đảm bảo các thay đổi code không làm ảnh hưởng tiêu cực đến bất kỳ tính năng cũ nào hoạt động ổn định.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản kiểm thử cho thuật toán phân bổ tài xế tự động (Driver Allocation Algorithm) trong ứng dụng đặt xe công nghệ (Grab/Gojek).
* **expected_key_points:**
  - id: KP8_1
    content: Kiểm thử tiêu chí khoảng cách và trạng thái
    keypoint_weight: 0.6
    description: Xác minh hệ thống ưu tiên phân bổ tài xế gần khách hàng nhất (dựa trên tọa độ GPS) và tài xế đó phải ở trạng thái sẵn sàng (Available), không đang trong chuyến đi khác.
  - id: KP8_2
    content: Kiểm thử trường hợp tải cao và không có tài xế
    keypoint_weight: 0.4
    description: Giả lập hàng nghìn khách đặt xe cùng lúc tại một khu vực nhỏ; kiểm tra luồng xử lý của hệ thống khi không tìm thấy tài xế nào (hủy chuyến, đề xuất tăng giá hoặc tiếp tục tìm kiếm).

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích cách kiểm thử khả năng chịu lỗi và tự phục hồi (Fault Tolerance / Disaster Recovery) của hệ thống cơ sở dữ liệu khi có một database node bị sập đột ngột.
* **expected_key_points:**
  - id: KP9_1
    content: Kiểm thử cơ chế chuyển vùng lỗi (Failover)
    keypoint_weight: 0.6
    description: Xác minh khi Master Node bị ngắt kết nối, hệ thống tự động bầu chọn một Slave Node lên làm Master mới mà không gây gián đoạn ghi dữ liệu quá lâu.
  - id: KP9_2
    content: Kiểm thử phục hồi dữ liệu (Recovery)
    keypoint_weight: 0.4
    description: Đưa Node bị lỗi hoạt động trở lại và xác minh Node đó đồng bộ thành công dữ liệu mới nhất được ghi trong thời gian nó ngoại tuyến.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Kiểm thử bảo mật: Làm thế nào để phát hiện lỗ hổng Path Traversal (truy cập file hệ thống trái phép) trên tính năng tải tài liệu từ server.
* **expected_key_points:**
  - id: KP10_1
    content: Nguyên lý lỗ hổng Path Traversal
    keypoint_weight: 0.5
    description: Xảy ra khi ứng dụng sử dụng input từ người dùng để xây dựng đường dẫn file tải về mà không lọc các ký tự điều hướng thư mục (như `../`).
  - id: KP10_2
    content: Cách thức kiểm thử thực tế
    keypoint_weight: 0.5
    description: Thay đổi tham số tên file thành các chuỗi như `../../../../etc/passwd` (Linux) hoặc `..\..\..\..\Windows\win.ini` (Windows) để xem server có trả về file hệ thống nhạy cảm không.

