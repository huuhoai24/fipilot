# Bộ Câu Hỏi Phỏng Vấn Software Engineer (Level 1) - Tập Đề Mới (58)

* **Role:** Software Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế cơ sở dữ liệu, sự khác biệt giữa `Primary Key` và `Foreign Key` là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa và vai trò
    keypoint_weight: 0.6
    description: `Primary Key` định danh duy nhất cho một bản ghi trong bảng. `Foreign Key` là trường liên kết đến `Primary Key` của một bảng khác để tạo mối quan hệ giữa các bảng.
  - id: KP1_2
    content: Quy tắc ràng buộc
    keypoint_weight: 0.4
    description: `Primary Key` không được NULL và phải duy nhất. `Foreign Key` có thể NULL (tùy thiết kế) và chấp nhận giá trị trùng lặp.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Nguyên lý `Open/Closed Principle` (O trong SOLID) yêu cầu gì?
* **expected_key_points:**
  - id: KP2_1
    content: Quy tắc thiết kế
    keypoint_weight: 0.7
    description: Các thành phần phần mềm (lớp, module) nên mở rộng để bổ sung tính năng (open for extension) nhưng đóng để sửa đổi mã nguồn (closed for modification).
  - id: KP2_2
    content: Lợi ích
    keypoint_weight: 0.3
    description: Giúp hệ thống ổn định, tránh lỗi phát sinh trên các module đã chạy tốt khi nâng cấp tính năng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao nên dùng `Version Control` (Git) trong dự án?
* **expected_key_points:**
  - id: KP3_1
    content: Quản lý lịch sử và phục hồi
    keypoint_weight: 0.6
    description: Cho phép theo dõi thay đổi, khôi phục code về phiên bản cũ khi gặp lỗi nghiêm trọng.
  - id: KP3_2
    content: Hợp tác nhóm
    keypoint_weight: 0.4
    description: Hỗ trợ nhiều người cùng làm việc trên một dự án thông qua cơ chế nhánh và hợp nhất code an toàn.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là "Race Condition" trong lập trình đa luồng?
* **expected_key_points:**
  - id: KP4_1
    content: Bản chất vấn đề
    keypoint_weight: 0.5
    description: Xảy ra khi kết quả của chương trình phụ thuộc vào thứ tự thực thi không xác định của nhiều luồng đang truy cập dữ liệu dùng chung.
  - id: KP4_2
    content: Giải pháp
    keypoint_weight: 0.5
    description: Cần dùng cơ chế đồng bộ hóa như `Locks` hoặc `Mutex` để bảo vệ các vùng dữ liệu chia sẻ (critical sections).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt `Pass-by-value` và `Pass-by-reference`.
* **expected_key_points:**
  - id: KP5_1
    content: Pass-by-value
    keypoint_weight: 0.5
    description: Truyền bản sao dữ liệu, thay đổi trong hàm không ảnh hưởng biến gốc.
  - id: KP5_2
    content: Pass-by-reference
    keypoint_weight: 0.5
    description: Truyền địa chỉ tham chiếu, thay đổi trong hàm tác động trực tiếp lên biến gốc.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Nguyên lý `Dependency Inversion Principle` (D) trong SOLID có nghĩa gì?
* **expected_key_points:**
  - id: KP6_1
    content: Quy tắc phụ thuộc
    keypoint_weight: 0.5
    description: Module cấp cao không nên phụ thuộc trực tiếp vào module cấp thấp, cả hai nên phụ thuộc vào các Abstraction (Interface).
  - id: KP6_2
    content: Tác dụng
    keypoint_weight: 0.5
    description: Giảm sự ràng buộc (decoupling), cho phép thay thế triển khai chi tiết dễ dàng mà không phá vỡ logic hệ thống.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao Database Transactions (ACID) quan trọng?
* **expected_key_points:**
  - id: KP7_1
    content: 4 thuộc tính ACID
    keypoint_weight: 0.5
    description: Atomicity, Consistency, Isolation, Durability.
  - id: KP7_2
    content: Ý nghĩa
    keypoint_weight: 0.5
    description: Đảm bảo dữ liệu luôn toàn vẹn và nhất quán, ngay cả khi gặp sự cố hệ thống trong lúc thực thi.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích "Memory Leak" do tham chiếu vòng và cách GC (Mark-and-Sweep) xử lý.
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất tham chiếu vòng
    keypoint_weight: 0.5
    description: Các đối tượng trỏ qua lại tạo nhóm cô lập, Reference Counting sẽ không dọn dẹp được vì tham chiếu không về 0.
  - id: KP8_2
    content: Thuật toán Mark-and-Sweep
    keypoint_weight: 0.5
    description: GC quét từ Root, chỉ những đối tượng có đường dẫn tới Root được giữ lại, các nhóm cô lập sẽ bị dọn dẹp.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** So sánh Strong Consistency vs Eventual Consistency.
* **expected_key_points:**
  - id: KP9_1
    content: Strong Consistency
    keypoint_weight: 0.5
    description: Dữ liệu đồng bộ tức thì trên toàn hệ thống. Đánh đổi: latency cao, rủi ro availability khi node lỗi.
  - id: KP9_2
    content: Eventual Consistency
    keypoint_weight: 0.5
    description: Dữ liệu có thể khác biệt tạm thời và sẽ đồng bộ sau. Ưu tiên: hiệu năng và tính sẵn sàng cao.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Nguyên lý "Liskov Substitution Principle" (L) - Các điều kiện cần kiểm tra.
* **expected_key_points:**
  - id: KP10_1
    content: Quy tắc thay thế
    keypoint_weight: 0.5
    description: Lớp con phải thay thế hoàn hảo lớp cha mà không làm thay đổi tính đúng đắn của chương trình.
  - id: KP10_2
    content: Kiểm tra hành vi
    keypoint_weight: 0.5
    description: Lớp con không ném ngoại lệ bất ngờ và phải tuân thủ mọi hợp đồng (hành vi) mà lớp cha đã cam kết.