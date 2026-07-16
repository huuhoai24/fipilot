# Bộ Câu Hỏi Phỏng Vấn Software Engineer (Level 1) - Tập Đề Mới (53)

* **Role:** Software Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong lập trình, sự khác biệt giữa `Interface` và `Abstract Class` là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Tính đa kế thừa
    keypoint_weight: 0.5
    description: Một class có thể implement nhiều `Interface`, nhưng chỉ được kế thừa từ duy nhất một `Abstract Class`.
  - id: KP1_2
    content: Mục đích sử dụng
    keypoint_weight: 0.5
    description: `Interface` định nghĩa hành vi (khả năng). `Abstract Class` định nghĩa cấu trúc/trạng thái chung cho các đối tượng có quan hệ huyết thống.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Nguyên lý `Open/Closed Principle` (O) trong SOLID là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa
    keypoint_weight: 0.7
    description: Các thực thể phần mềm nên mở rộng cho việc mở rộng (open for extension) nhưng đóng lại đối với việc sửa đổi mã nguồn (closed for modification).
  - id: KP2_2
    content: Lợi ích
    keypoint_weight: 0.3
    description: Hạn chế rủi ro phá vỡ các chức năng đã hoạt động ổn định khi cần thêm tính năng mới.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao cần sử dụng `Git` trong phát triển phần mềm?
* **expected_key_points:**
  - id: KP3_1
    content: Quản lý phiên bản (Version Control)
    keypoint_weight: 0.6
    description: Lưu trữ toàn bộ lịch sử thay đổi của code, cho phép khôi phục về trạng thái cũ khi gặp lỗi.
  - id: KP3_2
    content: Phối hợp nhóm
    keypoint_weight: 0.4
    description: Hỗ trợ làm việc trên các nhánh (branches) riêng biệt và hợp nhất (merge) code hiệu quả mà không xung đột.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Race Condition là gì và làm thế nào để ngăn chặn?
* **expected_key_points:**
  - id: KP4_1
    content: Bản chất vấn đề
    keypoint_weight: 0.5
    description: Xảy ra khi nhiều luồng truy cập và thay đổi tài nguyên chia sẻ cùng lúc mà không có cơ chế đồng bộ, dẫn đến kết quả không xác định.
  - id: KP4_2
    content: Cách xử lý
    keypoint_weight: 0.5
    description: Sử dụng các cơ chế khóa (Locking) như `Mutex` (Mutual Exclusion) hoặc `Semaphore` để bảo vệ tài nguyên dùng chung.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `Pass-by-value` và `Pass-by-reference`?
* **expected_key_points:**
  - id: KP5_1
    content: Pass-by-value
    keypoint_weight: 0.5
    description: Truyền bản sao của giá trị. Mọi thay đổi bên trong hàm không ảnh hưởng đến biến gốc ngoài hàm.
  - id: KP5_2
    content: Pass-by-reference
    keypoint_weight: 0.5
    description: Truyền địa chỉ của tham chiếu gốc. Mọi thay đổi trong hàm sẽ tác động trực tiếp tới đối tượng ban đầu.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Dependency Inversion Principle (D) trong SOLID có nghĩa là gì?
* **expected_key_points:**
  - id: KP6_1
    content: Quy tắc phụ thuộc
    keypoint_weight: 0.5
    description: Module cấp cao không nên phụ thuộc trực tiếp vào module cấp thấp, cả hai nên phụ thuộc vào các Abstraction (Interface).
  - id: KP6_2
    content: Lợi ích
    keypoint_weight: 0.5
    description: Giúp hệ thống lỏng lẻo hơn (loose coupling), dễ dàng hoán đổi/thay thế các triển khai chi tiết.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao Database Transactions (ACID) quan trọng?
* **expected_key_points:**
  - id: KP7_1
    content: Các thuộc tính chính
    keypoint_weight: 0.5
    description: Atomicity, Consistency, Isolation, Durability.
  - id: KP7_2
    content: Ý nghĩa thực tế
    keypoint_weight: 0.5
    description: Đảm bảo dữ liệu luôn chính xác và nhất quán ngay cả khi xảy ra lỗi hệ thống bất ngờ giữa chừng.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" do Circular References và cách GC hiện đại (Mark-and-Sweep) xử lý.
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất tham chiếu vòng
    keypoint_weight: 0.5
    description: Các đối tượng trỏ qua lại tạo thành nhóm cô lập, nếu dùng Reference Counting sẽ không thể dọn dẹp.
  - id: KP8_2
    content: Cơ chế Mark-and-Sweep
    keypoint_weight: 0.5
    description: GC quét từ Root, chỉ những đối tượng có đường dẫn từ Root mới được đánh dấu (mark) và giữ lại, các đối tượng cô lập sẽ bị quét và xóa (sweep).

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** So sánh Strong Consistency vs Eventual Consistency trong hệ thống phân tán.
* **expected_key_points:**
  - id: KP9_1
    content: Strong Consistency
    keypoint_weight: 0.5
    description: Đảm bảo dữ liệu nhất quán tức thì trên mọi node. Đánh đổi bằng độ trễ cao và rủi ro ngừng hoạt động khi node gặp lỗi.
  - id: KP9_2
    content: Eventual Consistency
    keypoint_weight: 0.5
    description: Dữ liệu giữa các node có thể khác nhau tạm thời, nhưng sẽ đồng bộ sau một thời gian. Ưu tiên hiệu năng và tính sẵn sàng cao.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Nguyên lý "Liskov Substitution Principle" (L) - Điều kiện không vi phạm.
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Đối tượng của lớp con phải thay thế được lớp cha mà không làm sai lệch chương trình.
  - id: KP10_2
    content: Điều kiện cần
    keypoint_weight: 0.5
    description: Lớp con không được ném thêm ngoại lệ ngoài dự kiến và phải tuân thủ các hợp đồng (hành vi) của lớp cha.