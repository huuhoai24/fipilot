# Bộ Câu Hỏi Phỏng Vấn Software Engineer (Level 1) - Tập Đề Mới (51)

* **Role:** Software Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong lập trình hướng đối tượng, sự khác biệt giữa `Encapsulation` (đóng gói) và `Abstraction` (trừu tượng) là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Encapsulation
    keypoint_weight: 0.5
    description: Là kỹ thuật che giấu dữ liệu bên trong lớp (thông qua access modifier như private), chỉ cho phép truy cập qua các phương thức public để bảo vệ trạng thái của đối tượng.
  - id: KP1_2
    content: Abstraction
    keypoint_weight: 0.5
    description: Là việc lược bỏ các chi tiết phức tạp, chỉ hiển thị những thông tin thiết yếu ra bên ngoài (thông qua interface hoặc abstract class) để giảm độ phức tạp khi sử dụng.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt `Deep Copy` và `Shallow Copy` của một đối tượng?
* **expected_key_points:**
  - id: KP2_1
    content: Shallow Copy
    keypoint_weight: 0.5
    description: Chỉ sao chép các thuộc tính ở cấp độ cao nhất. Nếu thuộc tính là object con, nó chỉ sao chép tham chiếu (cả hai bản sao vẫn trỏ chung đối tượng con).
  - id: KP2_2
    content: Deep Copy
    keypoint_weight: 0.5
    description: Sao chép đệ quy mọi thuộc tính, tạo ra đối tượng hoàn toàn mới độc lập với đối tượng gốc ở mọi cấp độ.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Nguyên lý `Interface Segregation Principle` (I) trong SOLID có nghĩa là gì?
* **expected_key_points:**
  - id: KP3_1
    content: Bản chất
    keypoint_weight: 0.7
    description: Không nên ép buộc lớp triển khai các phương thức không cần thiết. Nên chia các interface lớn thành nhiều interface nhỏ hơn, chuyên biệt hơn.
  - id: KP3_2
    content: Lợi ích
    keypoint_weight: 0.3
    description: Giúp code trở nên linh hoạt hơn, tránh việc thay đổi một phần nhỏ của hệ thống gây ảnh hưởng đến tất cả các lớp triển khai interface lớn.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích hiện tượng "Race Condition" và cách ngăn chặn trong đa luồng.
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Xảy ra khi kết quả của một chương trình phụ thuộc vào thứ tự thực thi không dự đoán trước được của các luồng truy cập dữ liệu dùng chung.
  - id: KP4_2
    content: Ngăn chặn
    keypoint_weight: 0.5
    description: Sử dụng các cơ chế đồng bộ hóa như `Mutex` (Mutual Exclusion), `Semaphore` hoặc `Locks` để đảm bảo quyền truy cập tuần tự.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao Database Transaction cần tuân thủ ACID?
* **expected_key_points:**
  - id: KP5_1
    content: Các thành phần ACID
    keypoint_weight: 0.6
    description: Atomicity (Nguyên tử), Consistency (Nhất quán), Isolation (Cô lập), Durability (Bền vững).
  - id: KP5_2
    content: Ý nghĩa
    keypoint_weight: 0.4
    description: Đảm bảo dữ liệu không bị hỏng hoặc trạng thái không nhất quán ngay cả khi xảy ra lỗi hệ thống hoặc thực thi đồng thời.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt `Process` và `Thread`.
* **expected_key_points:**
  - id: KP6_1
    content: Bản chất và bộ nhớ
    keypoint_weight: 0.5
    description: `Process` là chương trình đang thực thi với vùng nhớ riêng. `Thread` là đơn vị nhỏ nằm trong process và chia sẻ chung vùng nhớ của process cha.
  - id: KP6_2
    content: Hiệu năng và giao tiếp
    keypoint_weight: 0.5
    description: `Thread` nhẹ hơn, khởi tạo nhanh hơn và giao tiếp giữa các thread dễ dàng hơn do chia sẻ bộ nhớ.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Ý nghĩa của `Dependency Inversion Principle` (D) trong SOLID.
* **expected_key_points:**
  - id: KP7_1
    content: Quy tắc
    keypoint_weight: 0.5
    description: Module cấp cao không nên phụ thuộc module cấp thấp, cả hai nên phụ thuộc vào các Abstraction (Interface/Abstract Class).
  - id: KP7_2
    content: Lợi ích
    keypoint_weight: 0.5
    description: Giúp tách rời (decouple) các thành phần hệ thống, giúp thay đổi lớp con mà không ảnh hưởng lớp cha.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" do tham chiếu vòng (Circular Reference) và cơ chế dọn dẹp của GC.
* **expected_key_points:**
  - id: KP8_1
    content: Tham chiếu vòng
    keypoint_weight: 0.5
    description: A trỏ B, B trỏ A, dẫn đến số lượng tham chiếu không về 0 dù không còn biến nào sử dụng.
  - id: KP8_2
    content: Mark-and-Sweep
    keypoint_weight: 0.5
    description: Thuật toán quét từ các node gốc (Root). Mọi object không được đánh dấu sẽ bị xóa, giải quyết triệt để tham chiếu vòng.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** So sánh Strong Consistency và Eventual Consistency.
* **expected_key_points:**
  - id: KP9_1
    content: Strong Consistency
    keypoint_weight: 0.5
    description: Mọi node đều thấy dữ liệu như nhau tại thời điểm T. Đánh đổi: latency cao, rủi ro availability khi mạng phân mảnh.
  - id: KP9_2
    content: Eventual Consistency
    keypoint_weight: 0.5
    description: Dữ liệu khác nhau tạm thời, nhưng sẽ đồng nhất sau một khoảng thời gian. Ưu tiên hiệu năng và khả năng sẵn sàng.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích các điều kiện cần để xảy ra Deadlock (Coffman conditions).
* **expected_key_points:**
  - id: KP10_1
    content: Liệt kê các điều kiện
    keypoint_weight: 0.6
    description: Mutual Exclusion (Loại trừ), Hold and Wait (Nắm giữ và chờ), No Preemption (Không chiếm quyền), Circular Wait (Chờ đợi vòng tròn).
  - id: KP10_2
    content: Giải pháp
    keypoint_weight: 0.4
    description: Xóa bỏ một trong các điều kiện trên (ví dụ đặt thứ tự tài nguyên để tránh Circular Wait).