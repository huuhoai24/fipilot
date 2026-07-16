# Bộ Câu Hỏi Phỏng Vấn Software Engineer (Level 1) - Tập Đề Mới (56)

* **Role:** Software Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong lập trình hướng đối tượng, `Interface` khác gì với `Abstract Class`?
* **expected_key_points:**
  - id: KP1_1
    content: Tính đa kế thừa
    keypoint_weight: 0.5
    description: Một lớp có thể implement nhiều `Interface` để hỗ trợ đa kế thừa hành vi, nhưng chỉ được kế thừa từ một `Abstract Class`.
  - id: KP1_2
    content: Bản chất thiết kế
    keypoint_weight: 0.5
    description: `Interface` định nghĩa giao tiếp/hành vi bên ngoài. `Abstract Class` cung cấp một nền tảng code dùng chung (trạng thái hoặc phương thức) cho các đối tượng có quan hệ huyết thống.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Nguyên lý `Single Responsibility Principle` (SRP) trong SOLID là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa đơn nhiệm
    keypoint_weight: 0.7
    description: Một lớp hoặc module chỉ nên có duy nhất một trách nhiệm và chỉ có một lý do duy nhất để thay đổi.
  - id: KP2_2
    content: Lợi ích bảo trì
    keypoint_weight: 0.3
    description: Tránh việc code bị "phình to" theo thời gian, giúp việc kiểm thử và sửa lỗi tập trung hơn.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Git `Fetch` và `Pull` khác nhau ra sao?
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế Fetch
    keypoint_weight: 0.5
    description: Tải dữ liệu từ remote về local nhưng không ảnh hưởng đến nhánh đang làm việc (không merge).
  - id: KP3_2
    content: Cơ chế Pull
    keypoint_weight: 0.5
    description: Thực hiện `Fetch` và ngay lập tức `Merge` dữ liệu đó vào nhánh hiện tại.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Race Condition là gì và cách giải quyết trong đa luồng?
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Xảy ra khi nhiều luồng truy cập và thay đổi tài nguyên dùng chung cùng lúc, dẫn đến kết quả phụ thuộc vào thời điểm thực thi.
  - id: KP4_2
    content: Cơ chế đồng bộ
    keypoint_weight: 0.5
    description: Sử dụng `Mutex`, `Semaphore` hoặc `Locks` để đảm bảo quyền truy cập độc quyền vào vùng dữ liệu nhạy cảm.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt `Pass-by-value` và `Pass-by-reference`.
* **expected_key_points:**
  - id: KP5_1
    content: Pass-by-value
    keypoint_weight: 0.5
    description: Truyền một bản sao dữ liệu. Hàm chỉ thay đổi bản sao, giá trị gốc không thay đổi.
  - id: KP5_2
    content: Pass-by-reference
    keypoint_weight: 0.5
    description: Truyền tham chiếu địa chỉ bộ nhớ. Hàm thay đổi trực tiếp lên đối tượng gốc.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Nguyên lý `Dependency Inversion Principle` (D) trong SOLID là gì?
* **expected_key_points:**
  - id: KP6_1
    content: Quy tắc chính
    keypoint_weight: 0.5
    description: Module cấp cao không phụ thuộc module cấp thấp, cả hai đều phụ thuộc vào Abstraction (Interface).
  - id: KP6_2
    content: Lợi ích kiến trúc
    keypoint_weight: 0.5
    description: Giảm tính liên kết chặt chẽ (decoupling), cho phép thay thế triển khai dễ dàng mà không phá vỡ logic chính.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Database Transactions (ACID) có ý nghĩa gì?
* **expected_key_points:**
  - id: KP7_1
    content: 4 thuộc tính ACID
    keypoint_weight: 0.5
    description: Atomicity (Nguyên tử), Consistency (Nhất quán), Isolation (Cô lập), Durability (Bền vững).
  - id: KP7_2
    content: Tầm quan trọng
    keypoint_weight: 0.5
    description: Đảm bảo dữ liệu không bị hỏng, lỗi trạng thái trong các kịch bản thực thi phức tạp hoặc có sự cố.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" do Circular References và cách GC xử lý.
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất
    keypoint_weight: 0.5
    description: Nhóm đối tượng trỏ lẫn nhau tạo cấu trúc cô lập, nếu dùng đếm tham chiếu sẽ không bao giờ được giải phóng.
  - id: KP8_2
    content: Thuật toán Mark-and-Sweep
    keypoint_weight: 0.5
    description: GC quét từ Root, chỉ đối tượng truy cập được mới giữ lại. Cấu trúc cô lập bị quét và dọn dẹp (sweep) hoàn toàn.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** So sánh Strong Consistency vs Eventual Consistency.
* **expected_key_points:**
  - id: KP9_1
    content: Strong Consistency
    keypoint_weight: 0.5
    description: Dữ liệu đồng bộ tức thì trên toàn bộ node. Đánh đổi: Trễ cao, khả năng sẵn sàng thấp.
  - id: KP9_2
    content: Eventual Consistency
    keypoint_weight: 0.5
    description: Node có dữ liệu khác biệt tạm thời, sẽ hội tụ sau. Ưu tiên: Tốc độ và tính sẵn sàng cao.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Nguyên lý "Liskov Substitution Principle" (L) - Các điều kiện kiểm tra.
* **expected_key_points:**
  - id: KP10_1
    content: Quy tắc thay thế
    keypoint_weight: 0.5
    description: Lớp con phải thay thế được lớp cha mà không làm hỏng logic của chương trình.
  - id: KP10_2
    content: Kiểm soát lỗi
    keypoint_weight: 0.5
    description: Lớp con không được tăng cường điều kiện đầu vào hoặc thay đổi hợp đồng (hành vi) của lớp cha một cách bất ngờ.