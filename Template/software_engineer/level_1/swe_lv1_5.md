# Bộ Câu Hỏi Phỏng Vấn Software Engineer (Level 1) - Tập Đề Mới (50)

* **Role:** Software Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong cấu trúc dữ liệu, `Stack` và `Queue` khác nhau như thế nào?
* **expected_key_points:**
  - id: KP1_1
    content: Nguyên tắc hoạt động
    keypoint_weight: 0.6
    description: `Stack` tuân theo nguyên tắc LIFO (Last In First Out - vào sau ra trước). `Queue` tuân theo nguyên tắc FIFO (First In First Out - vào trước ra trước).
  - id: KP1_2
    content: Ứng dụng tiêu biểu
    keypoint_weight: 0.4
    description: `Stack` dùng trong quản lý lời gọi hàm (call stack) và undo/redo. `Queue` dùng trong quản lý tiến trình chờ (task scheduling) hoặc buffering.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Nguyên lý `Interface Segregation Principle` (I trong SOLID) nghĩa là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa
    keypoint_weight: 0.7
    description: Không nên ép buộc một lớp (class) phải triển khai các phương thức mà nó không sử dụng. Nên tách các interface lớn thành nhiều interface nhỏ hơn và chuyên biệt hơn.
  - id: KP2_2
    content: Lợi ích
    keypoint_weight: 0.3
    description: Giúp mã nguồn dễ bảo trì, tránh sự phụ thuộc không cần thiết và giảm rủi ro khi thay đổi code.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao nên dùng `Git Branching` trong quá trình phát triển phần mềm?
* **expected_key_points:**
  - id: KP3_1
    content: Cô lập tính năng
    keypoint_weight: 0.6
    description: Cho phép phát triển song song nhiều tính năng hoặc sửa lỗi trên các nhánh riêng biệt mà không làm ảnh hưởng đến nhánh chính (main/master).
  - id: KP3_2
    content: Kiểm soát chất lượng
    keypoint_weight: 0.4
    description: Dễ dàng thực hiện Code Review và kiểm thử độc lập trước khi hợp nhất (merge) code vào hệ thống chính thức.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm "Race Condition" trong đa luồng.
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Trạng thái khi nhiều luồng truy cập và thay đổi tài nguyên chia sẻ cùng lúc, khiến kết quả cuối cùng phụ thuộc vào thứ tự thực thi không xác định.
  - id: KP4_2
    content: Cách xử lý
    keypoint_weight: 0.5
    description: Cần sử dụng các cơ chế đồng bộ như `Mutex`, `Semaphore` hoặc các atomic operation để bảo vệ vùng dữ liệu dùng chung (critical section).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `Pass-by-value` và `Pass-by-reference`?
* **expected_key_points:**
  - id: KP5_1
    content: Pass-by-value
    keypoint_weight: 0.5
    description: Truyền bản sao giá trị. Thay đổi giá trị biến cục bộ trong hàm không ảnh hưởng đến biến gốc bên ngoài.
  - id: KP5_2
    content: Pass-by-reference
    keypoint_weight: 0.5
    description: Truyền địa chỉ tham chiếu. Mọi thay đổi nội dung thông qua tham chiếu đó sẽ tác động trực tiếp tới đối tượng gốc.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Nguyên lý `Dependency Inversion Principle` (D trong SOLID) có ý nghĩa gì?
* **expected_key_points:**
  - id: KP6_1
    content: Quy tắc chính
    keypoint_weight: 0.5
    description: Module cấp cao không nên phụ thuộc module cấp thấp, cả hai nên phụ thuộc vào các Abstraction (Interface/Abstract Class).
  - id: KP6_2
    content: Tác dụng
    keypoint_weight: 0.5
    description: Giúp giảm sự ràng buộc (decoupling) giữa các thành phần, cho phép thay thế triển khai chi tiết dễ dàng hơn mà không ảnh hưởng logic chính.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao Database Transaction Isolation Level lại quan trọng?
* **expected_key_points:**
  - id: KP7_1
    content: Mục đích
    keypoint_weight: 0.5
    description: Kiểm soát sự hiển thị của thay đổi dữ liệu từ một giao dịch này đối với giao dịch khác đang thực thi đồng thời.
  - id: KP7_2
    content: Các vấn đề ngăn chặn
    keypoint_weight: 0.5
    description: Ngăn chặn các lỗi như Dirty Read, Non-repeatable Read, và Phantom Read để đảm bảo tính nhất quán dữ liệu.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" do Circular References và cách GC hiện đại xử lý.
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất
    keypoint_weight: 0.5
    description: Object A trỏ B, B trỏ A tạo thành một nhóm cô lập. Nếu không có biến ngoài trỏ tới, chúng vẫn bị giữ lại trong bộ nhớ nếu dùng Reference Counting.
  - id: KP8_2
    content: Cách GC hiện đại
    keypoint_weight: 0.5
    description: Sử dụng kỹ thuật Mark-and-Sweep, chỉ những đối tượng có thể truy cập từ gốc (Root) mới được giữ lại, nhóm cô lập sẽ bị dọn dẹp.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** So sánh Strong Consistency vs Eventual Consistency trong hệ thống phân tán.
* **expected_key_points:**
  - id: KP9_1
    content: Strong Consistency
    keypoint_weight: 0.5
    description: Mọi node đều thấy dữ liệu giống nhau tức thì. Đổi lại độ trễ cao và rủi ro Availability thấp khi mạng chập chờn.
  - id: KP9_2
    content: Eventual Consistency
    keypoint_weight: 0.5
    description: Dữ liệu giữa các node có thể khác biệt tạm thời và sẽ hội tụ sau một khoảng thời gian. Ưu tiên Availability và hiệu năng cao.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Nguyên lý "Liskov Substitution Principle" (L) là gì?
* **expected_key_points:**
  - id: KP10_1
    content: Quy tắc thay thế
    keypoint_weight: 0.5
    description: Đối tượng của lớp con phải thay thế được đối tượng lớp cha mà không làm thay đổi tính đúng đắn của chương trình.
  - id: KP10_2
    content: Hệ quả
    keypoint_weight: 0.5
    description: Nếu lớp con ném lỗi hoặc thay đổi hành vi mà lớp cha không mong đợi, nó vi phạm nguyên lý này, gây lỗi khó kiểm soát khi mở rộng.