# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1) - Tập Đề Defect Density và SQL GROUP BY HAVING (15)

* **Role:** Tester
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Mật độ lỗi (Defect Density) là gì? Công thức tính và ý nghĩa của chỉ số này trong quản lý chất lượng phần mềm.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa và công thức tính
    keypoint_weight: 0.6
    description: Là số lượng lỗi được xác nhận tìm thấy trên một đơn vị kích thước phần mềm (ví dụ: số lỗi/1000 dòng code - KLOC, hoặc số lỗi/Function Point). Công thức: `Mật độ lỗi = Tổng số lỗi / Kích thước phần mềm`.
  - id: KP1_2
    content: Ý nghĩa chỉ số
    keypoint_weight: 0.4
    description: Giúp so sánh chất lượng giữa các module khác nhau, xác định vùng code có nguy cơ cao để tập trung tài nguyên kiểm thử.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Thế nào là kiểm thử độ khả dụng (Usability Testing)? Hãy nêu 3 tiêu chí đánh giá độ khả dụng của một ứng dụng di động.
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm Usability Testing
    keypoint_weight: 0.5
    description: Là phương pháp kiểm thử đánh giá mức độ dễ sử dụng, thân thiện và trực quan của ứng dụng đối với người dùng cuối.
  - id: KP2_2
    content: Ba tiêu chí đánh giá phổ biến
    keypoint_weight: 0.5
    description: Nêu được: Tính dễ học (Learnability), Hiệu quả thao tác (Efficiency), Khả năng nhớ cách sử dụng (Memorability), hoặc Mức độ hài lòng của người dùng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Sử dụng Git: Làm thế nào để giải quyết một xung đột code (Merge Conflict) cơ bản khi gộp nhánh?
* **expected_key_points:**
  - id: KP3_1
    content: Nguyên nhân xung đột code
    keypoint_weight: 0.4
    description: Xảy ra khi hai lập trình viên cùng sửa đổi trên cùng một dòng code ở hai nhánh khác nhau và gộp chung vào một nhánh.
  - id: KP3_2
    content: Quy trình giải quyết
    keypoint_weight: 0.6
    description: Mở file bị conflict -> tìm các thẻ đánh dấu conflict (`<<<<<<<`, `=======`, `>>>>>>>`) -> thảo luận với Dev liên quan để chọn giữ code của ai (hoặc gộp cả hai) -> xóa thẻ đánh dấu -> `git add` -> `git commit`.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết kịch bản kiểm thử cho tính năng thanh toán bằng quét mã QR Code trên ứng dụng ngân hàng di động (Mobile Banking).
* **expected_key_points:**
  - id: KP4_1
    content: Kiểm thử nhận diện QR Code
    keypoint_weight: 0.5
    description: Quét mã QR hợp lệ (từ camera hoặc ảnh trong album) -> hiển thị chính xác thông tin giao dịch (người nhận, số tiền, nội dung); quét mã QR sai định dạng báo lỗi rõ ràng.
  - id: KP4_2
    content: Kiểm thử luồng thanh toán và số dư
    keypoint_weight: 0.5
    description: Kiểm tra thanh toán thành công khi tài khoản đủ tiền (trừ tiền tài khoản nguồn, gửi thông báo OTP, màn hình thành công); chặn thanh toán khi tài khoản không đủ số dư.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết câu lệnh SQL tìm kiếm những địa chỉ email bị trùng lặp trong bảng `Users` và hiển thị số lần trùng lặp đó sử dụng GROUP BY và HAVING.
* **expected_key_points:**
  - id: KP5_1
    content: Sử dụng GROUP BY và HAVING chính xác
    keypoint_weight: 0.6
    description: Viết câu lệnh: `SELECT email, COUNT(id) FROM Users GROUP BY email HAVING COUNT(id) > 1`.
  - id: KP5_2
    content: Lọc các email duy nhất
    keypoint_weight: 0.4
    description: Xác minh điều kiện `COUNT(id) > 1` lọc bỏ các email chỉ xuất hiện 1 lần duy nhất trong DB.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Làm thế nào để sử dụng Postman kiểm thử một API yêu cầu xác thực bằng Bearer Token đi kèm trong Authorization Header?
* **expected_key_points:**
  - id: KP6_1
    content: Cấu hình Bearer Token trong tab Authorization
    keypoint_weight: 0.5
    description: Mở request -> chọn tab Authorization -> chọn Type là 'Bearer Token' -> nhập chuỗi token JWT vào trường Token tương ứng.
  - id: KP6_2
    content: Kiểm tra cấu trúc Headers gửi đi
    keypoint_weight: 0.5
    description: Xác minh trong tab Headers gửi đi tự động sinh ra header `Authorization` có giá trị bắt đầu bằng tiền tố `Bearer <chuỗi_token>`.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt Smoke Testing và Sanity Testing thông qua mục đích, phạm vi và thời điểm thực thi trong dự án thực tế.
* **expected_key_points:**
  - id: KP7_1
    content: So sánh về mục đích và thời điểm
    keypoint_weight: 0.5
    description: Smoke test chạy trên build mới để quyết định chấp nhận build (rộng, nông). Sanity test chạy sau khi sửa lỗi để xác minh nhanh lỗi đã sửa (hẹp, sâu).
  - id: KP7_2
    content: So sánh về phạm vi chạy
    keypoint_weight: 0.5
    description: Smoke test bao phủ toàn bộ các tính năng chính của hệ thống. Sanity test chỉ bao phủ tính năng được thay đổi và các tính năng liên quan trực tiếp.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế chiến lược kiểm thử cho hệ thống quản lý kho hàng (WMS) tích hợp thiết bị quét mã vạch (Barcode Scanner) cầm tay hoạt động trong điều kiện kho sóng Wifi yếu hoặc mất kết nối mạng.
* **expected_key_points:**
  - id: KP8_1
    content: Cơ chế đệm dữ liệu trên thiết bị cầm tay (Local buffer)
    keypoint_weight: 0.6
    description: Xác minh thiết bị quét lưu dữ liệu quét được vào bộ nhớ đệm nội bộ khi offline; có cơ chế rung/bíp báo hiệu quét thành công mặc dù chưa gửi lên server.
  - id: KP8_2
    content: Đồng bộ hóa dữ liệu hàng loạt (Batch sync)
    keypoint_weight: 0.4
    description: Khi thiết bị kết nối lại Wifi ổn định, hệ thống tự động đồng bộ hàng loạt (batch update) dữ liệu lên server theo đúng trình tự thời gian và giải quyết xung đột tồn kho.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích rủi ro hệ thống và kịch bản kiểm thử khi thực hiện nâng cấp cấu trúc cơ sở dữ liệu lớn (Database Migration) mà không làm dừng dịch vụ (Zero-downtime Migration).
* **expected_key_points:**
  - id: KP9_1
    content: Chiến lược Schema tương thích ngược (Backward Compatibility)
    keypoint_weight: 0.5
    description: Kiểm tra xem schema mới và cũ có thể chạy song song không (ví dụ: dùng phương pháp Expand-Contract: thêm cột mới, sao chép dữ liệu, sau đó mới xóa cột cũ).
  - id: KP9_2
    content: Kịch bản kiểm thử dữ liệu trong quá trình chuyển đổi
    keypoint_weight: 0.5
    description: Thực hiện viết/đọc dữ liệu liên tục trong khi script migration đang chạy; xác minh không xảy ra lỗi ghi đè dữ liệu hoặc mất mát dữ liệu.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Kiểm thử bảo mật: Làm thế nào để phát hiện lỗi rò rỉ thông tin nhạy cảm (Sensitive Data Exposure) qua các API response headers và logs hệ thống?
* **expected_key_points:**
  - id: KP10_1
    content: Rò rỉ thông tin qua HTTP Headers và Response Body
    keypoint_weight: 0.5
    description: Kiểm tra xem API response có trả về các thông tin nhạy cảm (như password hash, token mật, thông tin thẻ tín dụng đầy đủ) hoặc các Header tiết lộ chi tiết công nghệ (ví dụ `Server: Apache/2.4.41 (Ubuntu)`).
  - id: KP10_2
    content: Rò rỉ thông tin qua Logs hệ thống
    keypoint_weight: 0.5
    description: Kiểm tra logs của ứng dụng trên server xem có vô tình ghi lại mật khẩu dạng plain text hoặc token xác thực của người dùng khi họ thực hiện API request không.

