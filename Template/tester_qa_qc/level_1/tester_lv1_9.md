# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1) - Tập Đề Test Plan và SQL Subquery (9)

* **Role:** Tester
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Kế hoạch kiểm thử (Test Plan) là gì và những thành phần quan trọng nào bắt buộc phải có trong một tài liệu Test Plan chuẩn?
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa Test Plan
    keypoint_weight: 0.5
    description: Là tài liệu tổng quan mô tả phạm vi, hướng tiếp cận, tài nguyên và lịch trình của các hoạt động kiểm thử dự kiến.
  - id: KP1_2
    content: Thành phần bắt buộc
    keypoint_weight: 0.5
    description: Phạm vi kiểm thử (Scope), Môi trường test, Tiêu chí bắt đầu/kết thúc (Entry/Exit criteria), Kế hoạch bàn giao (Deliverables), Quản lý rủi ro (Risk management).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày kỹ thuật kiểm thử dựa trên Use Case (Use Case Testing) và lợi ích của nó.
* **expected_key_points:**
  - id: KP2_1
    content: Nguyên lý Use Case Testing
    keypoint_weight: 0.5
    description: Thiết kế test case dựa trên các kịch bản tương tác (luồng chính, luồng phụ, luồng lỗi) giữa người dùng (actor) và hệ thống để hoàn thành một mục tiêu nghiệp vụ.
  - id: KP2_2
    content: Lợi ích kiểm thử
    keypoint_weight: 0.5
    description: Giúp bao phủ được các luồng nghiệp vụ thực tế (business flows), phát hiện sớm lỗi tích hợp giữa các màn hình chức năng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Làm thế nào để sử dụng Postman gửi một request HTTP GET và kiểm tra mã trạng thái trả về có đúng là 200 OK không?
* **expected_key_points:**
  - id: KP3_1
    content: Thao tác gửi request GET
    keypoint_weight: 0.5
    description: Chọn phương thức GET từ dropdown, nhập địa chỉ URL của API -> nhấn nút Send.
  - id: KP3_2
    content: Kiểm tra mã trạng thái (Status Code)
    keypoint_weight: 0.5
    description: Xem góc dưới bên phải phần Response để xác nhận status code là 200 OK, hoặc viết script kiểm thử tự động trong tab Tests: `pm.response.to.have.status(200);`.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết kịch bản kiểm thử cho tính năng Chat trực tuyến (Real-time Chat) giữa Khách hàng và nhân viên CSKH trên trang web.
* **expected_key_points:**
  - id: KP4_1
    content: Kiểm thử gửi/nhận tin nhắn tức thời
    keypoint_weight: 0.5
    description: Khách hàng gửi -> nhân viên nhận ngay lập tức và ngược lại; hiển thị đúng nội dung tin nhắn, biểu tượng cảm xúc, hình ảnh đại diện, trạng thái đã đọc/đang gõ.
  - id: KP4_2
    content: Kiểm thử khi ngắt kết nối mạng
    keypoint_weight: 0.5
    description: Kiểm tra gửi tin nhắn khi mạng chập chờn hoặc mất mạng (hiển thị icon gửi lỗi và nút gửi lại); tự động kết nối lại khi có mạng.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết câu lệnh SQL truy vấn sử dụng Subquery (Truy vấn con) để tìm kiếm những khách hàng có đơn hàng trị giá lớn hơn 10,000 USD từ bảng Customers và Orders.
* **expected_key_points:**
  - id: KP5_1
    content: Cú pháp Subquery chính xác
    keypoint_weight: 0.6
    description: Sử dụng truy vấn con trong mệnh đề WHERE (ví dụ: `SELECT * FROM Customers WHERE id IN (SELECT customer_id FROM Orders WHERE total_amount > 10000)`).
  - id: KP5_2
    content: Tính tối ưu của câu lệnh
    keypoint_weight: 0.4
    description: Sử dụng toán tử `IN` hoặc `EXISTS` phù hợp để tối ưu hóa hiệu năng truy vấn của database.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách kiểm thử tính năng thông báo (Push Notification) trên thiết bị di động (Android/iOS).
* **expected_key_points:**
  - id: KP6_1
    content: Kiểm thử hiển thị thông báo các trạng thái app
    keypoint_weight: 0.5
    description: Xác minh thông báo hiển thị đúng khi app đang mở (foreground), đang chạy ngầm (background) hoặc đã bị tắt hoàn toàn (closed).
  - id: KP6_2
    content: Kiểm thử hành vi khi click thông báo
    keypoint_weight: 0.5
    description: Khi người dùng click vào thông báo, app phải mở ra và điều hướng chính xác đến màn hình chi tiết của nội dung thông báo đó.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Làm thế nào một Tester có thể áp dụng kỹ thuật Boundary Value Analysis (BVA) để kiểm thử một ô nhập mật khẩu yêu cầu từ 8 đến 16 ký tự?
* **expected_key_points:**
  - id: KP7_1
    content: Xác định các giá trị biên
    keypoint_weight: 0.5
    description: Biên dưới là 8, biên trên là 16. Các giá trị kiểm thử biên tương ứng gồm: 7 (không hợp lệ), 8 (hợp lệ), 9 (hợp lệ) và 15 (hợp lệ), 16 (hợp lệ), 17 (không hợp lệ).
  - id: KP7_2
    content: Kịch bản kiểm thử thực tế
    keypoint_weight: 0.5
    description: Nhập chuỗi mật khẩu có độ dài đúng bằng các giá trị biên đã xác định để kiểm tra phản hồi thông báo lỗi của hệ thống.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế chiến lược kiểm thử cho hệ thống bán vé máy bay trực tuyến chuẩn bị cho sự kiện bán vé giá rẻ giờ vàng (Flash Sale) với tải lượng truy cập dự kiến gấp 50 lần bình thường.
* **expected_key_points:**
  - id: KP8_1
    content: Chiến lược kiểm thử hiệu năng trước sự kiện
    keypoint_weight: 0.6
    description: Tổ chức thực hiện Load Testing và Stress Testing để tìm giới hạn chịu đựng tối đa của hệ thống, kiểm tra tính năng tự động co giãn tài nguyên (Auto-scaling) và cơ chế xếp hàng chờ (Queueing).
  - id: KP8_2
    content: Giải pháp dự phòng sự cố (Failover)
    keypoint_weight: 0.4
    description: Kiểm tra xem khi hệ thống quá tải, trang web có hiển thị trang chờ thân thiện hoặc cơ chế giảm tải (rate-limiting) để bảo vệ database không bị crash hay không.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích và kiểm thử lỗi lệch đồng bộ dữ liệu giữa Elasticsearch (dùng để tìm kiếm sản phẩm nhanh) và Database chính (SQL) khi cập nhật thông tin sản phẩm.
* **expected_key_points:**
  - id: KP9_1
    content: Nguyên nhân lệch đồng bộ dữ liệu
    keypoint_weight: 0.5
    description: Do cơ chế Sync bất đồng bộ (async sync) bị trễ, lỗi worker hàng đợi (job queue), hoặc lỗi mạng giữa Database và Elasticsearch làm mất message đồng bộ.
  - id: KP9_2
    content: Kịch bản kiểm thử phát hiện lỗi
    keypoint_weight: 0.5
    description: Cập nhật sản phẩm trong DB -> thực hiện tìm kiếm trên giao diện ngay lập tức và sau một khoảng thời gian để đo độ trễ đồng bộ (Sync Latency); kiểm tra logs đồng bộ khi tắt kết nối Elasticsearch.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Làm thế nào để kiểm thử hệ thống tích hợp bên thứ ba (ví dụ: Cổng thanh toán) khi họ không cung cấp môi trường Sandbox ổn định cho bạn kiểm thử?
* **expected_key_points:**
  - id: KP10_1
    content: Xây dựng Mock API/Stub
    keypoint_weight: 0.6
    description: Tester phối hợp với Developer để xây dựng một Mock Server giả lập các API response thành công, thất bại, timeout của bên thứ ba để chủ động kiểm thử hệ thống nội bộ.
  - id: KP10_2
    content: Sử dụng các công cụ thay đổi dữ liệu HTTP
    keypoint_weight: 0.4
    description: Dùng công cụ proxy (Fiddler/Charles Proxy) để sửa đổi gói tin response từ bên thứ ba về client nhằm tạo ra các kịch bản lỗi mong muốn.

