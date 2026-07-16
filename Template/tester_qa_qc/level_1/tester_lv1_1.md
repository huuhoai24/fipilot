# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1) - Tập Đề Tổng Hợp (68)

* **Role:** Tester
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong kiểm thử phần mềm, sự khác biệt giữa `Verification` (Xác minh) và `Validation` (Xác nhận) là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Câu hỏi cốt lõi
    keypoint_weight: 0.5
    description: `Verification` trả lời câu hỏi: "Chúng ta đang xây dựng sản phẩm đúng cách không?" (thường là review, walkthrough). `Validation` trả lời: "Chúng ta có đang xây dựng đúng sản phẩm người dùng cần không?" (thực thi phần mềm).
  - id: KP1_2
    content: Thời điểm thực hiện
    keypoint_weight: 0.5
    description: `Verification` thực hiện xuyên suốt quá trình (tĩnh). `Validation` thực hiện khi đã có phần mềm chạy được (động).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao cần phải thực hiện `Regression Testing` (Kiểm thử hồi quy) sau khi sửa lỗi?
* **expected_key_points:**
  - id: KP2_1
    content: Mục đích
    keypoint_weight: 0.7
    description: Đảm bảo các thay đổi, sửa lỗi hoặc cập nhật tính năng mới không gây ra lỗi (side-effects) cho các tính năng đã hoạt động ổn định trước đó.
  - id: KP2_2
    content: Phạm vi
    keypoint_weight: 0.3
    description: Kiểm thử lại toàn bộ hoặc một phần các test case đã chạy trước đây để đảm bảo hệ thống không bị suy giảm chất lượng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Một `Bug Report` tốt cần chứa những thành phần cơ bản nào?
* **expected_key_points:**
  - id: KP3_1
    content: Các trường bắt buộc
    keypoint_weight: 0.6
    description: ID, Tiêu đề, Môi trường (OS, Browser), Các bước tái hiện (Steps to reproduce), Kết quả mong đợi (Expected result) và Kết quả thực tế (Actual result).
  - id: KP3_2
    content: Bằng chứng
    keypoint_weight: 0.4
    description: Cần đính kèm hình ảnh (screenshots) hoặc video ghi lại quá trình tái hiện lỗi để lập trình viên dễ hình dung.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt `White Box Testing` và `Black Box Testing` trong chiến lược kiểm thử.
* **expected_key_points:**
  - id: KP4_1
    content: Bản chất phương pháp
    keypoint_weight: 0.5
    description: `Black Box` kiểm thử dựa trên yêu cầu/đặc tả mà không biết cấu trúc code. `White Box` kiểm thử dựa trên logic, cấu trúc mã nguồn bên trong.
  - id: KP4_2
    content: Đối tượng thực hiện
    keypoint_weight: 0.5
    description: `Black Box` thường do Tester thực hiện. `White Box` thường do Developer hoặc Tester có kỹ năng đọc code thực hiện.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là kỹ thuật `Boundary Value Analysis` (Phân tích giá trị biên) và tại sao nó quan trọng?
* **expected_key_points:**
  - id: KP5_1
    content: Định nghĩa kỹ thuật
    keypoint_weight: 0.5
    description: Là kỹ thuật kiểm thử các giá trị tại biên (min, max, min-1, max+1) của miền dữ liệu đầu vào.
  - id: KP5_2
    content: Hiệu quả kiểm thử
    keypoint_weight: 0.5
    description: Lỗi hệ thống thường xảy ra ở các giá trị biên thay vì ở các giá trị nằm giữa miền dữ liệu. 

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong vòng đời phần mềm (SDLC), vai trò của Tester khi tham gia vào quá trình phân tích yêu cầu (Requirement Analysis) là gì?
* **expected_key_points:**
  - id: KP6_1
    content: Phát hiện sớm
    keypoint_weight: 0.5
    description: Giúp phát hiện các lỗi logic, yêu cầu mơ hồ hoặc thiếu sót trong tài liệu yêu cầu ngay từ sớm (khi chưa code).
  - id: KP6_2
    content: Lập kế hoạch kiểm thử
    keypoint_weight: 0.5
    description: Dựa vào yêu cầu để xác định các test scenarios và chuẩn bị test data ngay từ giai đoạn đầu.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `Priority` (Mức độ ưu tiên) và `Severity` (Mức độ nghiêm trọng) của một Bug.
* **expected_key_points:**
  - id: KP7_1
    content: Định nghĩa Severity
    keypoint_weight: 0.5
    description: Phản ánh tác động kỹ thuật của lỗi tới chức năng hệ thống (ví dụ: treo app, crash).
  - id: KP7_2
    content: Định nghĩa Priority
    keypoint_weight: 0.5
    description: Phản ánh thời điểm cần phải sửa lỗi đó dựa trên nhu cầu kinh doanh hoặc yêu cầu quản lý (ví dụ: lỗi nhỏ nhưng ảnh hưởng thanh toán cần fix gấp).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích khái niệm "Test Oracle" và tại sao nó là thách thức trong kiểm thử hệ thống phức tạp.
* **expected_key_points:**
  - id: KP8_1
    content: Định nghĩa Oracle
    keypoint_weight: 0.5
    description: Là cơ chế hoặc nguồn thông tin dùng để quyết định liệu một test case đã pass hay fail (đáp án đúng).
  - id: KP8_2
    content: Thách thức hệ thống
    keypoint_weight: 0.5
    description: Trong hệ thống phức tạp, khó xác định chính xác hành vi mong đợi tuyệt đối, hoặc không có tài liệu/công cụ để đối chứng kết quả tự động.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích sự khác biệt giữa `Positive Testing` và `Negative Testing` trong việc đảm bảo chất lượng.
* **expected_key_points:**
  - id: KP9_1
    content: Positive Testing
    keypoint_weight: 0.5
    description: Kiểm thử hệ thống với dữ liệu đúng/hợp lệ để đảm bảo hệ thống làm việc như mong đợi.
  - id: KP9_2
    content: Negative Testing
    keypoint_weight: 0.5
    description: Kiểm thử với dữ liệu sai/không hợp lệ để đảm bảo hệ thống xử lý lỗi đúng cách và không bị crash.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích tại sao "100% Coverage" trong kiểm thử không đồng nghĩa với "0% Bug".
* **expected_key_points:**
  - id: KP10_1
    content: Giới hạn của bao phủ
    keypoint_weight: 0.5
    description: Code coverage/Test coverage chỉ đo lường đường đi của mã nguồn được thực thi, không kiểm tra được lỗi logic, lỗi thiếu yêu cầu hoặc lỗi tích hợp hệ thống.
  - id: KP10_2
    content: Yếu tố con người
    keypoint_weight: 0.5
    description: Các test case có thể bao phủ 100% code nhưng vẫn được thiết kế sai hoặc dựa trên các giả định không chính xác về người dùng.