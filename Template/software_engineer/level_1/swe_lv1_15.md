# Bộ Câu Hỏi Phỏng Vấn Software Engineer (Level 1) - Tập Đề Mới (61)

* **Role:** Software Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong các cấu trúc dữ liệu, `Stack` và `Queue` khác biệt như thế nào về thứ tự truy xuất dữ liệu?
* **expected_key_points:**
  - id: KP1_1
    content: Nguyên lý Stack
    keypoint_weight: 0.5
    description: Stack hoạt động theo LIFO (Last-In, First-Out), phần tử vào sau cùng sẽ được lấy ra đầu tiên.
  - id: KP1_2
    content: Nguyên lý Queue
    keypoint_weight: 0.5
    description: Queue hoạt động theo FIFO (First-In, First-Out), phần tử vào trước sẽ được xử lý trước.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Nguyên lý `Single Responsibility Principle` (S trong SOLID) yêu cầu gì ở code?
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa trách nhiệm
    keypoint_weight: 0.7
    description: Một lớp hoặc module chỉ nên có duy nhất một trách nhiệm và chỉ có một lý do duy nhất để thay đổi.
  - id: KP2_2
    content: Lợi ích
    keypoint_weight: 0.3
    description: Giúp code dễ hiểu, dễ cô lập khi sửa lỗi và tăng tính tái sử dụng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao cần sử dụng `Version Control` (Git) thay vì lưu code thủ công?
* **expected_key_points:**
  - id: KP3_1
    content: Kiểm soát lịch sử
    keypoint_weight: 0.6
    description: Cho phép truy vết mọi thay đổi, phục hồi lại các bản trước đó khi xảy ra sự cố (revert).
  - id: KP3_2
    content: Cộng tác đội ngũ
    keypoint_weight: 0.4
    description: Hỗ trợ làm việc nhóm song song trên nhiều nhánh mà không làm hỏng code của nhau.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là "Race Condition" trong đa luồng?
* **expected_key_points:**
  - id: KP4_1
    content: Bản chất
    keypoint_weight: 0.5
    description: Xảy ra khi nhiều luồng truy cập và thay đổi tài nguyên chung đồng thời, kết quả phụ thuộc vào thứ tự thực thi không xác định.
  - id: KP4_2
    content: Giải pháp
    keypoint_weight: 0.5
    description: Sử dụng cơ chế đồng bộ hóa như `Mutex` (Mutual Exclusion) hoặc `Locks` để đảm bảo quyền truy cập tuần tự.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt `Pass-by-value` và `Pass-by-reference` khi gọi hàm.
* **expected_key_points:**
  - id: KP5_1
    content: Pass-by-value
    keypoint_weight: 0.5
    description: Hàm nhận một bản sao dữ liệu, thay đổi bên trong không ảnh hưởng tới biến gốc bên ngoài.
  - id: KP5_2
    content: Pass-by-reference
    keypoint_weight: 0.5
    description: Hàm nhận tham chiếu (địa chỉ) tới dữ liệu, mọi thay đổi trong hàm đều tác động tới dữ liệu gốc.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Ý nghĩa của `Dependency Inversion Principle` (D) trong SOLID.
* **expected_key_points:**
  - id: KP6_1
    content: Quy tắc phụ thuộc
    keypoint_weight: 0.5
    description: Các module cấp cao không nên phụ thuộc trực tiếp module cấp thấp; cả hai nên phụ thuộc vào các Abstraction (Interface).
  - id: KP6_2
    content: Lợi ích
    keypoint_weight: 0.5
    description: Giúp tách rời (decouple) các thành phần, giúp thay đổi lớp con dễ dàng mà không làm ảnh hưởng logic lớp cha.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao Database Transactions (ACID) là khái niệm quan trọng?
* **expected_key_points:**
  - id: KP7_1
    content: Các thuộc tính ACID
    keypoint_weight: 0.5
    description: Atomicity, Consistency, Isolation, Durability.
  - id: KP7_2
    content: Ý nghĩa
    keypoint_weight: 0.5
    description: Đảm bảo dữ liệu nhất quán, không xảy ra sai lệch trong các tình huống thực thi phức tạp hoặc có lỗi hệ thống.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" do tham chiếu vòng và cách GC (Mark-and-Sweep) xử lý.
* **expected_key_points:**
  - id: KP8_1
    content: Tham chiếu vòng
    keypoint_weight: 0.5
    description: Đối tượng A trỏ B, B trỏ A tạo nhóm cô lập. Nếu chỉ dùng đếm tham chiếu, chúng sẽ không bao giờ được giải phóng.
  - id: KP8_2
    content: Cơ chế Mark-and-Sweep
    keypoint_weight: 0.5
    description: GC quét từ các Root, chỉ những đối tượng có đường dẫn từ Root mới được đánh dấu (mark) và giữ lại, các đối tượng bị cô lập sẽ bị quét và xóa (sweep). 

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** So sánh Strong Consistency và Eventual Consistency.
* **expected_key_points:**
  - id: KP9_1
    content: Strong Consistency
    keypoint_weight: 0.5
    description: Đảm bảo dữ liệu đồng bộ tức thì trên toàn node. Đánh đổi: Latency cao, Availability thấp khi node gặp lỗi.
  - id: KP9_2
    content: Eventual Consistency
    keypoint_weight: 0.5
    description: Dữ liệu khác biệt tạm thời và sẽ đồng bộ sau một khoảng thời gian. Ưu tiên: Hiệu năng và tính sẵn sàng cao.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Nguyên lý "Liskov Substitution Principle" (L) - Điều kiện không vi phạm.
* **expected_key_points:**
  - id: KP10_1
    content: Quy tắc thay thế
    keypoint_weight: 0.5
    description: Đối tượng của lớp con phải thay thế được lớp cha mà không làm thay đổi tính đúng đắn của chương trình.
  - id: KP10_2
    content: Kiểm soát hành vi
    keypoint_weight: 0.5
    description: Lớp con không được ném ra exception không mong đợi và phải tuân thủ đúng các hợp đồng (hành vi) đã định nghĩa ở lớp cha.