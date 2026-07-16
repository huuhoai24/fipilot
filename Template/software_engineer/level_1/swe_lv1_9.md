# Bộ Câu Hỏi Phỏng Vấn Software Engineer (Level 1) - Tập Đề Mới (54)

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
    description: Một class có thể implement nhiều `Interface`, nhưng chỉ được kế thừa từ một `Abstract Class`.
  - id: KP1_2
    content: Mục đích sử dụng
    keypoint_weight: 0.5
    description: `Interface` định nghĩa hành vi (khả năng). `Abstract Class` định nghĩa cấu trúc/trạng thái chung cho các đối tượng có quan hệ huyết thống.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Nguyên lý `Single Responsibility Principle` (SRP) trong SOLID yêu cầu gì?
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa trách nhiệm
    keypoint_weight: 0.7
    description: Một class hoặc module chỉ nên đảm nhận duy nhất một trách nhiệm và có duy nhất một lý do để thay đổi.
  - id: KP2_2
    content: Lợi ích bảo trì
    keypoint_weight: 0.3
    description: Tăng tính tập trung của code, giảm thiểu rủi ro khi sửa đổi một tính năng này ảnh hưởng đến tính năng khác.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao nên sử dụng Git trong phát triển phần mềm?
* **expected_key_points:**
  - id: KP3_1
    content: Quản lý lịch sử thay đổi
    keypoint_weight: 0.6
    description: Lưu vết mọi thay đổi của mã nguồn, cho phép hoàn tác về các phiên bản trước đó khi gặp lỗi.
  - id: KP3_2
    content: Hợp tác nhóm
    keypoint_weight: 0.4
    description: Hỗ trợ làm việc trên nhiều nhánh (branching) và hợp nhất (merging) code hiệu quả mà không bị ghi đè dữ liệu của nhau.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích hiện tượng "Race Condition" trong đa luồng.
* **expected_key_points:**
  - id: KP4_1
    content: Bản chất vấn đề
    keypoint_weight: 0.5
    description: Xảy ra khi nhiều luồng cùng truy cập và thay đổi tài nguyên chia sẻ, dẫn đến kết quả sai lệch tùy thuộc vào thứ tự thực thi không xác định.
  - id: KP4_2
    content: Cách xử lý
    keypoint_weight: 0.5
    description: Sử dụng các cơ chế đồng bộ hóa (synchronization) như `Mutex`, `Semaphore`, hoặc `Locks`.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `Pass-by-value` và `Pass-by-reference`?
* **expected_key_points:**
  - id: KP5_1
    content: Pass-by-value
    keypoint_weight: 0.5
    description: Truyền bản sao của giá trị, hàm nhận giá trị độc lập, thay đổi trong hàm không ảnh hưởng biến gốc.
  - id: KP5_2
    content: Pass-by-reference
    keypoint_weight: 0.5
    description: Truyền địa chỉ tham chiếu, thay đổi bên trong hàm sẽ tác động trực tiếp đến đối tượng ban đầu.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Nguyên lý `Dependency Inversion Principle` (D) trong SOLID đóng vai trò gì?
* **expected_key_points:**
  - id: KP6_1
    content: Quy tắc phụ thuộc
    keypoint_weight: 0.5
    description: Module cấp cao không nên phụ thuộc module cấp thấp, cả hai nên phụ thuộc vào các Abstraction (Interface/Abstract Class).
  - id: KP6_2
    content: Tác dụng
    keypoint_weight: 0.5
    description: Giúp hệ thống lỏng lẻo hơn (decoupling), dễ dàng hoán đổi các module bên dưới mà không làm ảnh hưởng logic chính.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao Database Transactions (ACID) quan trọng trong hệ thống?
* **expected_key_points:**
  - id: KP7_1
    content: Các thuộc tính chính
    keypoint_weight: 0.5
    description: Atomicity, Consistency, Isolation, Durability.
  - id: KP7_2
    content: Ý nghĩa thực tế
    keypoint_weight: 0.5
    description: Đảm bảo dữ liệu luôn chính xác và nhất quán, tránh tình trạng dữ liệu lỗi do gián đoạn giữa chừng.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng Memory Leak do Circular References và cách GC hiện đại xử lý.
* **expected_key_points:**
  - id: KP8_1
    content: Tham chiếu vòng
    keypoint_weight: 0.5
    description: Object trỏ lẫn nhau tạo nhóm cô lập, Reference Counting không thể xóa vì tham chiếu không về 0.
  - id: KP8_2
    content: Thuật toán Mark-and-Sweep
    keypoint_weight: 0.5
    description: GC quét từ Root, chỉ các đối tượng có đường dẫn từ Root được giữ lại, các nhóm cô lập bị dọn dẹp.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** So sánh Strong Consistency và Eventual Consistency.
* **expected_key_points:**
  - id: KP9_1
    content: Strong Consistency
    keypoint_weight: 0.5
    description: Mọi node thấy dữ liệu giống nhau tức thì. Đánh đổi: latency cao, rủi ro availability khi node gặp lỗi.
  - id: KP9_2
    content: Eventual Consistency
    keypoint_weight: 0.5
    description: Dữ liệu giữa các node khác biệt tạm thời, sẽ hội tụ sau. Ưu tiên hiệu năng và khả năng sẵn sàng cao.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Nguyên lý "Liskov Substitution Principle" (L) - Điều kiện thay thế.
* **expected_key_points:**
  - id: KP10_1
    content: Quy tắc thay thế
    keypoint_weight: 0.5
    description: Đối tượng của lớp con phải thay thế được đối tượng lớp cha mà không làm thay đổi tính đúng đắn của chương trình.
  - id: KP10_2
    content: Hậu quả vi phạm
    keypoint_weight: 0.5
    description: Lớp con không được ném ra exception không mong đợi hoặc làm thay đổi logic hành vi cốt lõi của cha.