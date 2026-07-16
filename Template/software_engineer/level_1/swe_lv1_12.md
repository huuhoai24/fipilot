# Bộ Câu Hỏi Phỏng Vấn Software Engineer (Level 1) - Tập Đề Mới (57)

* **Role:** Software Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong lập trình hướng đối tượng, sự khác biệt chính giữa `Interface` và `Abstract Class` là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Tính kế thừa
    keypoint_weight: 0.5
    description: Một class có thể implement nhiều `Interface` (đa kế thừa hành vi), nhưng chỉ được kế thừa từ một `Abstract Class`.
  - id: KP1_2
    content: Mục đích sử dụng
    keypoint_weight: 0.5
    description: `Interface` định nghĩa giao tiếp/hành vi. `Abstract Class` cung cấp một nền tảng code dùng chung cho các đối tượng có quan hệ huyết thống.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Nguyên lý `Single Responsibility Principle` (SRP) trong SOLID yêu cầu gì ở code?
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa trách nhiệm
    keypoint_weight: 0.7
    description: Một lớp hoặc module chỉ nên có duy nhất một trách nhiệm và chỉ có một lý do duy nhất để thay đổi.
  - id: KP2_2
    content: Lợi ích bảo trì
    keypoint_weight: 0.3
    description: Giúp mã nguồn tập trung, dễ kiểm thử và giảm thiểu tác động lan truyền khi sửa đổi chức năng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Git `Fetch` và `Pull` khác nhau ra sao?
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế Fetch
    keypoint_weight: 0.5
    description: Tải dữ liệu mới từ remote về local nhưng không hợp nhất (merge) vào nhánh hiện tại.
  - id: KP3_2
    content: Cơ chế Pull
    keypoint_weight: 0.5
    description: Thực hiện `Fetch` và ngay lập tức `Merge` dữ liệu đó vào nhánh làm việc hiện tại của bạn.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích hiện tượng "Race Condition" và cách ngăn chặn trong đa luồng.
* **expected_key_points:**
  - id: KP4_1
    content: Bản chất vấn đề
    keypoint_weight: 0.5
    description: Xảy ra khi nhiều luồng truy cập và thay đổi tài nguyên chia sẻ cùng lúc, khiến kết quả cuối cùng phụ thuộc vào thứ tự thực thi không xác định.
  - id: KP4_2
    content: Cách xử lý
    keypoint_weight: 0.5
    description: Sử dụng các cơ chế đồng bộ hóa (synchronization) như `Mutex`, `Semaphore`, hoặc `Locks` để đảm bảo quyền truy cập độc quyền.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `Pass-by-value` và `Pass-by-reference`?
* **expected_key_points:**
  - id: KP5_1
    content: Pass-by-value
    keypoint_weight: 0.5
    description: Truyền bản sao của giá trị. Hàm làm việc trên vùng nhớ riêng, biến gốc không thay đổi.
  - id: KP5_2
    content: Pass-by-reference
    keypoint_weight: 0.5
    description: Truyền địa chỉ tham chiếu. Thay đổi trong hàm sẽ tác động trực tiếp lên đối tượng gốc ban đầu.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Nguyên lý `Dependency Inversion Principle` (D) trong SOLID đóng vai trò gì?
* **expected_key_points:**
  - id: KP6_1
    content: Quy tắc phụ thuộc
    keypoint_weight: 0.5
    description: Module cấp cao không phụ thuộc module cấp thấp, cả hai nên phụ thuộc vào các Abstraction (Interface).
  - id: KP6_2
    content: Tác dụng
    keypoint_weight: 0.5
    description: Giúp tách rời (decouple) các thành phần, cho phép thay đổi triển khai chi tiết mà không làm ảnh hưởng logic chính.

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
    description: Đảm bảo dữ liệu luôn chính xác, nhất quán, không xảy ra sai lệch trong các tình huống thực thi lỗi hoặc đồng thời.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích "Memory Leak" do Circular References và cách GC (Mark-and-Sweep) xử lý.
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất tham chiếu vòng
    keypoint_weight: 0.5
    description: Các đối tượng trỏ qua lại tạo nhóm cô lập, nếu dùng Reference Counting thì không thể giải phóng bộ nhớ.
  - id: KP8_2
    content: Thuật toán Mark-and-Sweep
    keypoint_weight: 0.5
    description: GC quét từ Root, chỉ đối tượng có đường dẫn từ Root được đánh dấu (mark) và giữ lại, các nhóm cô lập sẽ bị quét và xóa (sweep).

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** So sánh Strong Consistency vs Eventual Consistency.
* **expected_key_points:**
  - id: KP9_1
    content: Strong Consistency
    keypoint_weight: 0.5
    description: Mọi node đều thấy dữ liệu đồng bộ tức thì. Đánh đổi bằng độ trễ cao và rủi ro Availability thấp khi mạng chập chờn.
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
    description: Đối tượng của lớp con phải thay thế được lớp cha mà không làm thay đổi tính đúng đắn của chương trình.
  - id: KP10_2
    content: Kiểm tra điều kiện
    keypoint_weight: 0.5
    description: Lớp con không được ném ra exception không mong đợi hoặc thay đổi hành vi cốt lõi của lớp cha.