# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1) - Tập Đề E2E Testing và SQL Date Functions (16)

* **Role:** Tester
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Kiểm thử đầu cuối (End-to-End Testing) là gì? Hãy mô tả ví dụ về một quy trình kiểm thử đầu cuối của chức năng mua hàng online.
* **expected_key_points:**
  - id: KP1_1
    content: Khái niệm End-to-End Testing
    keypoint_weight: 0.5
    description: Là phương pháp kiểm thử toàn bộ luồng hoạt động của phần mềm từ điểm bắt đầu đến điểm kết thúc, mô phỏng đúng hành trình của người dùng thực tế trên mọi hệ thống liên kết.
  - id: KP1_2
    content: Ví dụ luồng mua hàng online
    keypoint_weight: 0.5
    description: Luồng: Đăng nhập -> Tìm kiếm sản phẩm -> Thêm vào giỏ -> Nhập địa chỉ giao hàng -> Thanh toán qua cổng thanh toán -> Kiểm tra trạng thái đơn hàng -> Kiểm tra email xác nhận gửi về.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Kỹ thuật phân tích giá trị biên 2-point và 3-point khác nhau như thế nào? Nêu ví dụ cho một biên số nguyên từ 1 đến 10.
* **expected_key_points:**
  - id: KP2_1
    content: Sự khác nhau về số lượng điểm test
    keypoint_weight: 0.5
    description: 2-point chọn 2 giá trị tại mỗi điểm biên (Biên và ngoài biên). 3-point chọn 3 giá trị tại mỗi điểm biên (Biên, sát trong biên, sát ngoài biên).
  - id: KP2_2
    content: Ví dụ cụ thể với biên [1, 10]
    keypoint_weight: 0.5
    description: Với 2-point chọn: {0, 1} và {10, 11}. Với 3-point chọn: {0, 1, 2} và {9, 10, 11}.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa Query Parameter và Path Parameter trong cấu trúc đường dẫn URL của API.
* **expected_key_points:**
  - id: KP3_1
    content: Đặc trưng Query Parameter
    keypoint_weight: 0.5
    description: Dùng để lọc/sắp xếp dữ liệu, bắt đầu sau dấu chấm hỏi `?` và nối với nhau bằng dấu `&` (ví dụ: `/products?category=shoes&sort=price`).
  - id: KP3_2
    content: Đặc trưng Path Parameter
    keypoint_weight: 0.5
    description: Dùng để định danh một tài nguyên cụ thể, là một phần của đường dẫn URL (ví dụ: `/products/101` để chỉ sản phẩm có ID 101).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết kịch bản kiểm thử (Test Scenario) cho chức năng Tạo chiến dịch quảng cáo trực tuyến (chọn đối tượng mục tiêu, cấu hình ngân sách, đặt thời gian chạy, và upload ảnh thiết kế).
* **expected_key_points:**
  - id: KP4_1
    content: Kiểm thử cấu hình thông số chiến dịch
    keypoint_weight: 0.5
    description: Kiểm tra cấu hình ngân sách tối thiểu/tối đa, thiết lập thời gian bắt đầu lớn hơn thời gian hiện tại, chọn tệp đối tượng theo đúng vùng miền/tuổi.
  - id: KP4_2
    content: Kiểm thử lưu nháp và xuất bản
    keypoint_weight: 0.5
    description: Xác minh lưu nháp chiến dịch thành công khi thiếu thông tin bắt buộc; xuất bản thành công khi đầy đủ thông tin và chuyển trạng thái thành 'Active' đúng lịch.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết câu lệnh SQL sử dụng các hàm xử lý ngày tháng để tìm danh sách tất cả hóa đơn (Invoices) chưa được thanh toán và đã quá hạn thanh toán hơn 30 ngày so với ngày hiện tại (due_date < current_date - 30).
* **expected_key_points:**
  - id: KP5_1
    content: Sử dụng hàm ngày tháng chính xác
    keypoint_weight: 0.6
    description: Sử dụng các hàm tương ứng của hệ quản trị DB (ví dụ MySQL: `DATEDIFF(NOW(), due_date) > 30` hoặc SQL Server: `DATEDIFF(day, due_date, GETDATE()) > 30`).
  - id: KP5_2
    content: Ràng buộc trạng thái hóa đơn
    keypoint_weight: 0.4
    description: Đảm bảo có điều kiện lọc trạng thái hóa đơn chưa thanh toán (ví dụ: `AND status = 'unpaid'`).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách sử dụng tab Performance trong Chrome DevTools để ghi lại tốc độ render giao diện và phát hiện các khung hình bị giật (Jank) khi cuộn trang.
* **expected_key_points:**
  - id: KP6_1
    content: Cách ghi lại biểu đồ khung hình (Frame Chart)
    keypoint_weight: 0.5
    description: Mở tab Performance -> click Record -> cuộn trang web liên tục -> click Stop -> xem biểu đồ tốc độ khung hình (Frames).
  - id: KP6_2
    content: Phát hiện khung hình đỏ (Jank)
    keypoint_weight: 0.5
    description: Tìm các cột mốc khung hình hiển thị màu đỏ (tốc độ khung hình giảm xuống dưới 60 FPS, block luồng chính lâu) để báo dev tối ưu lại CSS/JS animation.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy so sánh ưu nhược điểm của Kiểm thử tự động (Automation Testing) và Kiểm thử thủ công (Manual Testing). Khi nào nên áp dụng loại nào?
* **expected_key_points:**
  - id: KP7_1
    content: So sánh ưu nhược điểm
    keypoint_weight: 0.6
    description: Manual kiểm thử linh hoạt, dễ tìm bug mới bằng trực giác nhưng tốn thời gian. Automation chạy nhanh, nhất quán, lặp lại tốt nhưng tốn chi phí viết/bảo trì code test.
  - id: KP7_2
    content: Thời điểm áp dụng phù hợp
    keypoint_weight: 0.4
    description: Dùng Automation cho kiểm thử hồi quy (Regression), kiểm thử hiệu năng (Performance). Dùng Manual cho kiểm thử khám phá (Exploratory), kiểm thử giao diện (UI) thay đổi liên tục.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản kiểm thử cho hệ thống đấu giá trực tuyến thời gian thực (Real-time Auction System) đảm bảo ghi nhận người trả giá cao nhất và nhanh nhất ở mili-giây cuối cùng.
* **expected_key_points:**
  - id: KP8_1
    content: Kiểm thử xử lý tranh chấp đồng thời (Concurrency bidding)
    keypoint_weight: 0.6
    description: Giả lập nhiều người dùng cùng nhấn nút đấu giá tại cùng một mili-giây cuối cùng trước khi đóng phiên; xác minh hệ thống chỉ ghi nhận duy nhất người có request đến server trước và số tiền phải lớn hơn giá hiện tại.
  - id: KP8_2
    content: Đồng bộ hóa giao diện thời gian thực
    keypoint_weight: 0.4
    description: Đảm bảo giá mới hiển thị tức thời lên màn hình của toàn bộ người tham gia khác thông qua kết nối WebSocket/Server-Sent Events mà không cần load lại trang.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích cách kiểm thử tích hợp cho hệ thống Đăng nhập một lần (SSO - Single Sign-On) tích hợp giữa nhiều ứng dụng sử dụng giao thức SAML 2.0 hoặc OIDC.
* **expected_key_points:**
  - id: KP9_1
    content: Kiểm thử luồng Token và Chuyển hướng (Redirect flow)
    keypoint_weight: 0.6
    description: Xác minh khi đăng nhập tại App A thành công -> truy cập App B tự động đăng nhập (nhận token hợp lệ, giải mã đúng); kiểm tra chuyển hướng an toàn về URL nguồn gốc sau khi đăng nhập.
  - id: KP9_2
    content: Kiểm thử luồng Đăng xuất một lần (Single Logout - SLO)
    keypoint_weight: 0.4
    description: Xác minh khi người dùng nhấn Đăng xuất (Logout) tại bất kỳ ứng dụng nào trong hệ thống liên kết, phiên làm việc (session) của toàn bộ các ứng dụng khác cũng bị vô hiệu hóa lập tức.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Kiểm thử bảo mật: Phát hiện lỗ hổng Server-Side Template Injection (SSTI) trên các ứng dụng sử dụng công cụ sinh template (như Jinja2, Thymeleaf).
* **expected_key_points:**
  - id: KP10_1
    content: Nguyên lý lỗ hổng SSTI
    keypoint_weight: 0.5
    description: Xảy ra khi dữ liệu đầu vào của người dùng được nối trực tiếp vào chuỗi template mà không sanitize, dẫn đến việc engine thực thi mã nguy hiểm trên máy chủ.
  - id: KP10_2
    content: Cách thức kiểm thử thủ công
    keypoint_weight: 0.5
    description: Nhập các biểu thức toán học đặc thù của template engine (ví dụ: `{{7*7}}` hoặc `${7*7}`) vào ô nhập liệu. Nếu giao diện hiển thị kết quả là `49`, hệ thống dính lỗ hổng SSTI.

