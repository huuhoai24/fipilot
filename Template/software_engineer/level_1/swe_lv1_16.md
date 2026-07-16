# Bộ Câu Hỏi Phỏng Vấn Software Engineer (Level 1) - Tổng Hợp (Đề 63)

* **Role:** Software Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong lập trình hướng đối tượng (OOP), sự khác biệt giữa `Interface` và `Abstract Class` là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Tính đa kế thừa
    keypoint_weight: 0.5
    description: Một lớp có thể implement nhiều `Interface`, nhưng chỉ được kế thừa từ một `Abstract Class`.
  - id: KP1_2
    content: Mục đích sử dụng
    keypoint_weight: 0.5
    description: `Interface` định nghĩa hành vi (bản hợp đồng). `Abstract Class` định nghĩa cấu trúc/trạng thái chung cho các đối tượng cùng bản chất.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Nguyên lý `Single Responsibility Principle` (SRP) trong SOLID yêu cầu gì?
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa trách nhiệm
    keypoint_weight: 0.7
    description: Một lớp hoặc module chỉ nên có duy nhất một trách nhiệm và chỉ có một lý do duy nhất để thay đổi.
  - id: KP2_2
    content: Lợi ích bảo trì
    keypoint_weight: 0.3
    description: Giúp code dễ hiểu, dễ kiểm thử và giảm thiểu rủi ro khi sửa đổi một tính năng này ảnh hưởng đến tính năng khác.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao cần sử dụng `Git` trong dự án phần mềm thay vì quản lý thủ công?
* **expected_key_points:**
  - id: KP3_1
    content: Kiểm soát phiên bản
    keypoint_weight: 0.6
    description: Lưu trữ lịch sử thay đổi, cho phép khôi phục về các phiên bản trước khi xảy ra lỗi.
  - id: KP3_2
    content: Phối hợp nhóm
    keypoint_weight: 0.4
    description: Hỗ trợ làm việc song song trên nhiều nhánh (branch) mà không làm mất mát code của nhau.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Race Condition là gì và cách ngăn chặn trong đa luồng?
* **expected_key_points:**
  - id: KP4_1
    content: Bản chất vấn đề
    keypoint_weight: 0.5
    description: Nhiều luồng truy cập/thay đổi tài nguyên chung đồng thời dẫn đến kết quả sai lệch do thứ tự thực thi không xác định.
  - id: KP4_2
    content: Giải pháp đồng bộ
    keypoint_weight: 0.5
    description: Sử dụng `Mutex`, `Locks` hoặc `Semaphores` để đảm bảo quyền truy cập độc quyền vào vùng dữ liệu nhạy cảm.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt `Pass-by-value` và `Pass-by-reference`.
* **expected_key_points:**
  - id: KP5_1
    content: Pass-by-value
    keypoint_weight: 0.5
    description: Truyền bản sao của giá trị. Hàm làm việc trên dữ liệu độc lập, không ảnh hưởng biến gốc.
  - id: KP5_2
    content: Pass-by-reference
    keypoint_weight: 0.5
    description: Truyền tham chiếu địa chỉ bộ nhớ. Mọi tác động trong hàm thay đổi trực tiếp đối tượng gốc.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Nguyên lý `Dependency Inversion Principle` (D) trong SOLID có ý nghĩa gì?
* **expected_key_points:**
  - id: KP6_1
    content: Quy tắc phụ thuộc
    keypoint_weight: 0.5
    description: Module cấp cao không phụ thuộc module cấp thấp, cả hai phụ thuộc vào Abstraction (Interface).
  - id: KP6_2
    content: Tác dụng
    keypoint_weight: 0.5
    description: Giúp tách rời các thành phần (decoupling), dễ dàng thay đổi triển khai mà không làm đổ vỡ logic hệ thống.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao Database Transactions (ACID) quan trọng?
* **expected_key_points:**
  - id: KP7_1
    content: 4 thuộc tính ACID
    keypoint_weight: 0.5
    description: Atomicity, Consistency, Isolation, Durability.
  - id: KP7_2
    content: Ý nghĩa thực tế
    keypoint_weight: 0.5
    description: Đảm bảo dữ liệu nhất quán, không xảy ra sai lệch trong các tình huống thực thi phức tạp hoặc có lỗi hệ thống.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" do tham chiếu vòng và cách GC hiện đại xử lý.
* **expected_key_points:**
  - id: KP8_1
    content: Tham chiếu vòng
    keypoint_weight: 0.5
    description: Các đối tượng trỏ qua lại tạo cấu trúc cô lập, nếu chỉ đếm tham chiếu sẽ không giải phóng được.
  - id: KP8_2
    content: Thuật toán Mark-and-Sweep
    keypoint_weight: 0.5
    description:  GC quét từ Root, chỉ những đối tượng có đường dẫn từ Root được giữ lại, các cấu trúc cô lập sẽ bị quét và xóa (sweep).

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** So sánh Strong Consistency vs Eventual Consistency.
* **expected_key_points:**
  - id: KP9_1
    content: Strong Consistency
    keypoint_weight: 0.5
    description: Mọi node thấy dữ liệu đồng bộ tức thì. Đánh đổi bằng độ trễ cao và rủi ro Availability thấp.
  - id: KP9_2
    content: Eventual Consistency
    keypoint_weight: 0.5
    description: Dữ liệu giữa các node khác biệt tạm thời, sẽ hội tụ sau. Ưu tiên hiệu năng và tính sẵn sàng cao.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Nguyên lý "Liskov Substitution Principle" (L) - Điều kiện không vi phạm.
* **expected_key_points:**
  - id: KP10_1
    content: Quy tắc thay thế
    keypoint_weight: 0.5
    description: Đối tượng lớp con phải thay thế được lớp cha mà không làm sai lệch tính logic của chương trình.
  - id: KP10_2
    content: Điều kiện kiểm tra
    keypoint_weight: 0.5
    description: Lớp con không được ném ra lỗi ngoài dự kiến và phải tuân thủ đúng các hợp đồng hành vi đã định nghĩa ở lớp cha.