# Bộ Câu Hỏi Phỏng Vấn Software Engineer (Level 1) - Tập Đề Mới (55)

* **Role:** Software Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong OOP, tại sao nên ưu tiên `Composition` (tập hợp) thay vì `Inheritance` (kế thừa)?
* **expected_key_points:**
  - id: KP1_1
    content: Tính linh hoạt (Loose Coupling)
    keypoint_weight: 0.6
    description: `Composition` cho phép thay đổi hành vi đối tượng tại runtime bằng cách thay đổi thành phần chứa, trong khi `Inheritance` cố định hành vi tại thời điểm biên dịch.
  - id: KP1_2
    content: Tránh "Fragile Base Class"
    keypoint_weight: 0.4
    description: Kế thừa sâu dễ gây lỗi khi thay đổi lớp cha. `Composition` tách biệt hành vi, giúp code độc lập và ít rủi ro hơn.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Git `Reset` và Git `Revert` khác nhau như thế nào?
* **expected_key_points:**
  - id: KP2_1
    content: Tác động đến lịch sử
    keypoint_weight: 0.5
    description: `Reset` di chuyển con trỏ nhánh về commit cũ (thực tế là xóa lịch sử commit sau đó). `Revert` tạo ra một commit mới để đảo ngược thay đổi của commit cũ (giữ nguyên lịch sử).
  - id: KP2_2
    content: Độ an toàn
    keypoint_weight: 0.5
    description: `Reset` nguy hiểm trên nhánh đã public (shared branch). `Revert` an toàn tuyệt đối cho mọi tình huống.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Nguyên lý `Interface Segregation Principle` (I trong SOLID) hướng tới mục tiêu gì?
* **expected_key_points:**
  - id: KP3_1
    content: Định nghĩa
    keypoint_weight: 0.7
    description: Một client không nên bị ép buộc phải phụ thuộc vào các phương thức mà nó không sử dụng. Tách các interface lớn thành nhiều interface nhỏ chuyên biệt.
  - id: KP3_2
    content: Lợi ích
    keypoint_weight: 0.3
    description: Giảm thiểu sự phụ thuộc thừa, giúp code rõ ràng và dễ thay thế triển khai cụ thể hơn.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Race Condition trong đa luồng là gì và cách xử lý phổ biến?
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Khi nhiều luồng cùng đọc/ghi tài nguyên dùng chung dẫn tới trạng thái dữ liệu không nhất quán do thứ tự thực thi không xác định.
  - id: KP4_2
    content: Giải pháp
    keypoint_weight: 0.5
    description: Sử dụng các cơ chế đồng bộ hóa (synchronization) như `Locks`, `Mutex`, hoặc dùng các cấu trúc dữ liệu `Thread-safe`.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt `Pass-by-value` và `Pass-by-reference` trong bộ nhớ.
* **expected_key_points:**
  - id: KP5_1
    content: Pass-by-value
    keypoint_weight: 0.5
    description: Truyền bản sao giá trị, hàm làm việc trên vùng nhớ riêng, biến gốc không thay đổi.
  - id: KP5_2
    content: Pass-by-reference
    keypoint_weight: 0.5
    description: Truyền địa chỉ (con trỏ/tham chiếu) đến vùng nhớ, mọi tác động trong hàm ảnh hưởng trực tiếp đến dữ liệu gốc.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Dependency Inversion Principle (D) trong SOLID có ý nghĩa gì?
* **expected_key_points:**
  - id: KP6_1
    content: Quy tắc
    keypoint_weight: 0.5
    description: Module cấp cao không phụ thuộc module cấp thấp, cả hai cùng phụ thuộc vào Abstraction.
  - id: KP6_2
    content: Lợi ích
    keypoint_weight: 0.5
    description: Tách rời (decoupling) các thành phần, giúp thay thế triển khai (Implementation) mà không ảnh hưởng logic cấp cao.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao Database Transactions (ACID) quan trọng?
* **expected_key_points:**
  - id: KP7_1
    content: Các thành phần ACID
    keypoint_weight: 0.5
    description: Atomicity, Consistency, Isolation, Durability.
  - id: KP7_2
    content: Ý nghĩa
    keypoint_weight: 0.5
    description: Đảm bảo dữ liệu nguyên vẹn, nhất quán, không xảy ra sai lệch trong các tình huống thực thi lỗi hoặc đồng thời.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" do tham chiếu vòng (Circular Reference) và cách GC (Mark-and-Sweep) xử lý.
* **expected_key_points:**
  - id: KP8_1
    content: Tham chiếu vòng
    keypoint_weight: 0.5
    description: Các đối tượng trỏ qua lại tạo nhóm cô lập, Reference Counting sẽ không dọn dẹp được vì tham chiếu không về 0.
  - id: KP8_2
    content: Cơ chế Mark-and-Sweep
    keypoint_weight: 0.5
    description: GC quét từ Root, chỉ các đối tượng có đường dẫn từ Root được giữ lại, nhóm cô lập sẽ bị quét và xóa (sweep) hoàn toàn.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Strong Consistency vs Eventual Consistency trong hệ thống phân tán.
* **expected_key_points:**
  - id: KP9_1
    content: Strong Consistency
    keypoint_weight: 0.5
    description: Đảm bảo mọi node thấy dữ liệu đồng bộ tức thì. Đánh đổi: latency cao, rủi ro availability.
  - id: KP9_2
    content: Eventual Consistency
    keypoint_weight: 0.5
    description: Dữ liệu giữa các node có thể khác biệt tạm thời và sẽ đồng nhất sau một khoảng thời gian. Ưu tiên hiệu năng và sẵn sàng.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Nguyên lý "Liskov Substitution Principle" (L) - Điều kiện cần.
* **expected_key_points:**
  - id: KP10_1
    content: Quy tắc thay thế
    keypoint_weight: 0.5
    description: Đối tượng lớp con phải thay thế hoàn hảo lớp cha mà không làm thay đổi tính logic của chương trình.
  - id: KP10_2
    content: Điều kiện kiểm tra
    keypoint_weight: 0.5
    description: Lớp con không ném ngoại lệ bất ngờ, không làm suy yếu các cam kết (pre-conditions/post-conditions) của lớp cha.