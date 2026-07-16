# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1) - Tập Đề Test Deliverables và SQL Aggregate Functions (19)

* **Role:** Tester
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Các sản phẩm kiểm thử bàn giao (Test Deliverables) của dự án phần mềm gồm những tài liệu và thành phần gì trước, trong và sau quá trình kiểm thử?
* **expected_key_points:**
  - id: KP1_1
    content: Sản phẩm trước và trong khi test
    keypoint_weight: 0.5
    description: Tài liệu Kế hoạch kiểm thử (Test Plan), Kịch bản kiểm thử (Test Cases/Scenarios), Dữ liệu kiểm thử (Test Data).
  - id: KP1_2
    content: Sản phẩm sau khi test xong
    keypoint_weight: 0.5
    description: Báo cáo lỗi (Bug Reports), Báo cáo kết quả kiểm thử (Test Summary Report), tài liệu hướng dẫn cài đặt/môi trường nếu có.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Thế nào là Ad-hoc Testing? Cho ví dụ về tình huống thực tế dự án nên sử dụng phương pháp kiểm thử này.
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa Ad-hoc Testing
    keypoint_weight: 0.5
    description: Là phương pháp kiểm thử không chính quy, không có kế hoạch hay tài liệu kịch bản trước, kiểm thử tự do để tìm lỗi nhanh.
  - id: KP2_2
    content: Tình huống áp dụng thực tế
    keypoint_weight: 0.5
    description: Dùng khi thời gian kiểm thử dự án còn rất ít (gần đến giờ release), hoặc khi đã chạy hết toàn bộ test case chính thức và muốn tìm thêm lỗi ẩn.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày cách kiểm tra dung lượng bộ nhớ RAM và bộ nhớ trong còn trống của thiết bị di động (Android hoặc iOS) khi chuẩn bị môi trường cài đặt ứng dụng để test.
* **expected_key_points:**
  - id: KP3_1
    content: Thao tác kiểm tra trên Android
    keypoint_weight: 0.5
    description: Vào Cài đặt (Settings) -> Chăm sóc thiết bị (Device Care) hoặc Giới thiệu điện thoại -> Lưu trữ (Storage) và Bộ nhớ (RAM) để xem dung lượng trống.
  - id: KP3_2
    content: Thao tác kiểm tra trên iOS
    keypoint_weight: 0.5
    description: Vào Cài đặt (Settings) -> Cài đặt chung (General) -> Dung lượng iPhone để kiểm tra dung lượng bộ nhớ trong còn lại.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết kịch bản kiểm thử cho chức năng Tự động gợi ý từ khóa tìm kiếm (Search Suggestion) dựa trên lịch sử tìm kiếm cá nhân hóa của người dùng.
* **expected_key_points:**
  - id: KP4_1
    content: Kiểm thử hiển thị lịch sử tìm kiếm cá nhân
    keypoint_weight: 0.5
    description: Click vào ô search -> hiển thị danh sách các từ khóa người dùng này đã tìm kiếm gần đây theo thứ tự thời gian mới nhất lên đầu.
  - id: KP4_2
    content: Kiểm thử gợi ý kết hợp lịch sử và hệ thống
    keypoint_weight: 0.5
    description: Nhập ký tự đầu tiên -> ưu tiên hiển thị từ khóa trong lịch sử cá nhân trước, sau đó mới đến các từ khóa phổ biến của hệ thống.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết câu lệnh SQL truy vấn sử dụng các hàm gom cụm toán học (SUM, AVG, MIN, MAX) kết hợp GROUP BY để tính toán doanh thu trung bình (average) và tổng doanh thu (sum) của các đơn hàng theo từng tháng trong năm 2026.
* **expected_key_points:**
  - id: KP5_1
    content: Cú pháp gom cụm và GROUP BY chính xác
    keypoint_weight: 0.6
    description: Viết câu lệnh dạng: `SELECT MONTH(order_date) AS month, SUM(total_amount), AVG(total_amount) FROM orders WHERE YEAR(order_date) = 2026 GROUP BY MONTH(order_date)`.
  - id: KP5_2
    content: Lọc điều kiện năm chính xác
    keypoint_weight: 0.4
    description: Đảm bảo mệnh đề WHERE lọc chính xác dữ liệu trong năm 2026 trước khi gom nhóm theo tháng.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách sử dụng tính năng Collection Runner trong Postman để chạy tự động một bộ API test case từ file dữ liệu JSON đầu vào (Data-driven testing).
* **expected_key_points:**
  - id: KP6_1
    content: Cách thiết lập Collection Runner
    keypoint_weight: 0.5
    description: Chọn Collection -> click Run -> chọn file dữ liệu (JSON/CSV) chứa danh sách các biến test đầu vào -> kiểm tra số lượng vòng lặp (iterations) tương ứng.
  - id: KP6_2
    content: Sử dụng biến từ file dữ liệu
    keypoint_weight: 0.5
    description: Trong API request, sử dụng cú pháp hai ngoặc nhọn `{{variable_name}}` khớp với tên cột trong file dữ liệu để Postman tự động map giá trị qua từng vòng lặp.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt sự khác nhau giữa Static Testing (Kiểm thử tĩnh) và Dynamic Testing (Kiểm thử động) về thời điểm bắt đầu và hiệu quả tìm lỗi.
* **expected_key_points:**
  - id: KP7_1
    content: So sánh thời điểm bắt đầu
    keypoint_weight: 0.5
    description: Static testing bắt đầu rất sớm từ giai đoạn phân tích yêu cầu (review tài liệu spec, review code). Dynamic testing bắt đầu muộn hơn khi đã có bản build chạy được.
  - id: KP7_2
    content: So sánh hiệu quả tìm lỗi
    keypoint_weight: 0.5
    description: Static testing giúp phát hiện lỗi logic thiết kế và ngăn chặn lỗi sớm (tiết kiệm chi phí). Dynamic testing phát hiện lỗi thực thi, lỗi tích hợp và hiệu năng thực tế.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản kiểm thử cho hệ thống giới hạn tần suất yêu cầu (Rate Limiting) sử dụng thuật toán Token Bucket để chống tấn công Spam API/DDoS.
* **expected_key_points:**
  - id: KP8_1
    content: Kiểm thử trong ngưỡng giới hạn cho phép
    keypoint_weight: 0.5
    description: Gửi số lượng request liên tục dưới mức cấu hình (ví dụ: dưới 10 request/giây) -> hệ thống phản hồi bình thường với HTTP status 200 OK.
  - id: KP8_2
    content: Kiểm thử vượt ngưỡng giới hạn
    keypoint_weight: 0.5
    description: Gửi request thứ 11 trong cùng 1 giây -> hệ thống chặn ngay lập tức, trả về HTTP status 429 Too Many Requests và header `Retry-After` chỉ rõ thời gian chờ.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích nguyên nhân và cách kiểm thử phát hiện lỗi rò rỉ bộ nhớ ở phía người dùng (Frontend Memory Leak) trong ứng dụng Single Page Application (SPA).
* **expected_key_points:**
  - id: KP9_1
    content: Nguyên nhân rò rỉ bộ nhớ ở SPA
    keypoint_weight: 0.5
    description: Do các component bị hủy (unmount) nhưng các subscription, setTimeout, hoặc event listener lắng nghe window/document không được dọn dẹp (clear).
  - id: KP9_2
    content: Phương pháp đo đạc và tái hiện lỗi
    keypoint_weight: 0.5
    description: Dùng Chrome DevTools tab Performance/Memory; chụp snapshot trước và sau khi click chuyển qua lại giữa các màn hình nhiều lần. Nếu bộ nhớ RAM của tab trình duyệt tăng dần và không giảm, xác định vị trí component bị rò rỉ.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Kiểm thử bảo mật: Làm thế nào để phát hiện lỗ hổng Local File Inclusion (LFI) trên ứng dụng web thông qua thanh địa chỉ URL?
* **expected_key_points:**
  - id: KP10_1
    content: Nguyên lý lỗ hổng LFI
    keypoint_weight: 0.5
    description: Xảy ra khi ứng dụng cho phép truyền đường dẫn file cục bộ vào tham số URL để load nội dung (ví dụ: `?page=about.html`) mà không kiểm tra tính hợp lệ của thư mục nguồn.
  - id: KP10_2
    content: Cách thức kiểm thử thực tế
    keypoint_weight: 0.5
    description: Thay đổi giá trị tham số thành đường dẫn tuyệt đối hoặc tương đối của file hệ thống (ví dụ: `?page=../../../../etc/passwd` hoặc `?page=C:\Windows\system.ini`). Nếu nội dung file đó hiển thị trên trang web, hệ thống dính lỗi LFI.

