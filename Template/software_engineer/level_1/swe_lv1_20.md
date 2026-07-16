# Bộ Câu Hỏi Phỏng Vấn Software Engineer (Level 1) - Tập Đề Tổng Hợp Hệ Thống (67)

* **Role:** Software Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế cơ sở dữ liệu, sự khác biệt giữa `Primary Key` và `Unique Key` là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Tính chất NULL
    keypoint_weight: 0.5
    description: `Primary Key` không được phép chứa giá trị NULL. `Unique Key` cho phép giá trị NULL (tùy vào hệ quản trị DB).
  - id: KP1_2
    content: Số lượng trong bảng
    keypoint_weight: 0.5
    description: Mỗi bảng chỉ có một `Primary Key`, nhưng có thể có nhiều `Unique Key` để đảm bảo tính duy nhất cho các cột khác nhau.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Nguyên lý `Single Responsibility Principle` (SRP) trong thiết kế hệ thống có ý nghĩa gì?
* **expected_key_points:**
  - id: KP2_1
    content: Phân tách trách nhiệm
    keypoint_weight: 0.7
    description: Một lớp/module chỉ nên tập trung xử lý một loại chức năng duy nhất để giảm sự phức tạp.
  - id: KP2_2
    content: Khả năng bảo trì
    keypoint_weight: 0.3
    description: Khi yêu cầu thay đổi, chỉ cần sửa một module, hạn chế ảnh hưởng dây chuyền lên các phần khác.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao cần sử dụng `Version Control` (như Git) trong phát triển phần mềm hệ thống?
* **expected_key_points:**
  - id: KP3_1
    content: Truy vết và phục hồi
    keypoint_weight: 0.6
    description: Giúp ghi lại lịch sử thay đổi của toàn bộ mã nguồn, cho phép quay lại trạng thái cũ (revert) khi hệ thống gặp lỗi.
  - id: KP3_2
    content: Hợp tác đa luồng
    keypoint_weight: 0.4
    description: Cho phép nhiều kỹ sư làm việc trên cùng một codebase thông qua cơ chế nhánh (branching) mà không ghi đè dữ liệu của nhau.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Hiện tượng `Race Condition` trong kiến trúc hệ thống là gì và cách xử lý?
* **expected_key_points:**
  - id: KP4_1
    content: Bản chất vấn đề
    keypoint_weight: 0.5
    description: Khi nhiều tiến trình truy cập đồng thời vào một tài nguyên chia sẻ, kết quả sai lệch do thứ tự thực thi không xác định.
  - id: KP4_2
    content: Giải pháp đồng bộ
    keypoint_weight: 0.5
    description: Sử dụng các cơ chế như `Mutex`, `Locks` hoặc các cấu trúc dữ liệu `atomic` để tuần tự hóa quyền truy cập tài nguyên.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh `Pass-by-value` và `Pass-by-reference` trong tư duy tối ưu bộ nhớ.
* **expected_key_points:**
  - id: KP5_1
    content: Pass-by-value
    keypoint_weight: 0.5
    description: Truyền bản sao, an toàn vì không làm thay đổi biến gốc nhưng tốn bộ nhớ do nhân bản dữ liệu.
  - id: KP5_2
    content: Pass-by-reference
    keypoint_weight: 0.5
    description: Truyền tham chiếu địa chỉ, tiết kiệm bộ nhớ nhưng yêu cầu kiểm soát chặt chẽ để tránh thay đổi dữ liệu ngoài ý muốn.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Ý nghĩa của `Dependency Inversion Principle` (D trong SOLID) trong hệ thống lớn?
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên lý đảo ngược
    keypoint_weight: 0.5
    description: Module cấp cao không phụ thuộc module cấp thấp, cả hai cùng phụ thuộc vào Abstraction (Interface).
  - id: KP6_2
    content: Tính tách rời (Decoupling)
    keypoint_weight: 0.5
    description: Cho phép thay đổi triển khai chi tiết mà không gây ảnh hưởng đến logic nghiệp vụ cốt lõi ở tầng trên.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao Database Transactions (ACID) là nền tảng của hệ thống dữ liệu tin cậy?
* **expected_key_points:**
  - id: KP7_1
    content: 4 đặc tính ACID
    keypoint_weight: 0.5
    description: Atomicity (Nguyên tử), Consistency (Nhất quán), Isolation (Cô lập), Durability (Bền vững).
  - id: KP7_2
    content: Ý nghĩa hệ thống
    keypoint_weight: 0.5
    description: Đảm bảo dữ liệu không bị hỏng hóc hoặc không nhất quán ngay cả khi có lỗi phần cứng hoặc xung đột giao dịch.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích Memory Leak do Circular References và cách GC (Mark-and-Sweep) xử lý.
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất tham chiếu vòng
    keypoint_weight: 0.5
    description: Các đối tượng trỏ qua lại tạo cấu trúc cô lập, nếu dùng Reference Counting sẽ bị giữ vĩnh viễn trong bộ nhớ.
  - id: KP8_2
    content: Thuật toán Mark-and-Sweep
    keypoint_weight: 0.5
    description:  GC quét từ Root nodes, đánh dấu các đối tượng có thể tiếp cận được (marked), sau đó quét và xóa (sweep) các đối tượng cô lập không thể tiếp cận.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** So sánh Strong Consistency vs Eventual Consistency trong hệ thống phân tán.
* **expected_key_points:**
  - id: KP9_1
    content: Strong Consistency
    keypoint_weight: 0.5
    description: Mọi node thấy dữ liệu giống nhau tức thì. Đánh đổi: Latency cao, Availability thấp khi node gặp lỗi.
  - id: KP9_2
    content: Eventual Consistency
    keypoint_weight: 0.5
    description: Dữ liệu khác biệt tạm thời, sẽ hội tụ sau. Ưu tiên: Hiệu năng và tính sẵn sàng cao (High Availability).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Nguyên lý "Liskov Substitution Principle" (L) - Điều kiện cần để không vi phạm trong thiết kế hệ thống.
* **expected_key_points:**
  - id: KP10_1
    content: Quy tắc thay thế
    keypoint_weight: 0.5
    description: Đối tượng của lớp con phải thay thế được lớp cha mà không làm sai lệch tính logic của chương trình.
  - id: KP10_2
    content: Kiểm soát hành vi
    keypoint_weight: 0.5
    description: Lớp con không được ném ra ngoại lệ bất ngờ và phải tuân thủ đúng các hợp đồng (hành vi/bất biến) đã định nghĩa ở lớp cha.