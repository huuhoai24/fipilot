# Bộ Câu Hỏi Phỏng Vấn Software Engineer (Level 1) - Tập Đề Mới (48)

* **Role:** Software Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong lập trình, sự khác biệt chính giữa `Interface` và `Abstract Class` là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Tính kế thừa
    keypoint_weight: 0.5
    description: Một class có thể implement nhiều `Interface`, nhưng chỉ được kế thừa từ một `Abstract Class`.
  - id: KP1_2
    content: Mục đích sử dụng
    keypoint_weight: 0.5
    description: `Interface` dùng để định nghĩa "hành vi" (khả năng). `Abstract Class` dùng để định nghĩa "bản chất" (cấu trúc dùng chung).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích độ phức tạp `O(n log n)` thường xuất hiện trong thuật toán nào?
* **expected_key_points:**
  - id: KP2_1
    content: Thuật toán tiêu biểu
    keypoint_weight: 0.5
    description: Thường gặp ở các thuật toán sắp xếp hiệu quả như `Merge Sort` hoặc `Quick Sort`.
  - id: KP2_2
    content: Ý nghĩa
    keypoint_weight: 0.5
    description: Tốc độ tăng trưởng không còn là tuyến tính đơn thuần mà bị ảnh hưởng bởi quá trình chia để trị (divide and conquer).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao cần sử dụng Version Control (như Git)?
* **expected_key_points:**
  - id: KP3_1
    content: Quản lý lịch sử và phục hồi
    keypoint_weight: 0.6
    description: Theo dõi mọi thay đổi trong code, cho phép hoàn tác (revert) về các phiên bản cũ khi xảy ra lỗi.
  - id: KP3_2
    content: Hợp tác nhóm
    keypoint_weight: 0.4
    description: Hỗ trợ làm việc đồng thời qua các nhánh (branch) và hợp nhất (merge) code mà không làm ghi đè mất mát của nhau.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là "Race Condition" trong lập trình đa luồng?
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Tình trạng nhiều luồng tranh chấp quyền truy cập và thay đổi cùng một tài nguyên dẫn đến kết quả sai lệch tùy thuộc vào thứ tự thực thi.
  - id: KP4_2
    content: Cách xử lý
    keypoint_weight: 0.5
    description: Sử dụng các cơ chế đồng bộ hóa (synchronization) như `Mutex` (Mutual Exclusion) hoặc `Semaphores`.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `Pass-by-value` và `Pass-by-reference`?
* **expected_key_points:**
  - id: KP5_1
    content: Pass-by-value
    keypoint_weight: 0.5
    description: Truyền bản sao của dữ liệu. Mọi thay đổi trong hàm không tác động đến biến ban đầu ngoài hàm.
  - id: KP5_2
    content: Pass-by-reference
    keypoint_weight: 0.5
    description: Truyền tham chiếu địa chỉ bộ nhớ. Thay đổi trong hàm sẽ tác động trực tiếp vào đối tượng gốc.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** SOLID - Nguyên lý Dependency Inversion Principle (D) là gì?
* **expected_key_points:**
  - id: KP6_1
    content: Quy tắc
    keypoint_weight: 0.5
    description: Module cấp cao không nên phụ thuộc module cấp thấp, cả hai đều phụ thuộc vào Abstraction.
  - id: KP6_2
    content: Lợi ích
    keypoint_weight: 0.5
    description: Giúp giảm sự ràng buộc (decoupling), cho phép thay đổi triển khai chi tiết mà không làm hỏng logic của hệ thống.

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
    description: Đảm bảo dữ liệu luôn ở trạng thái nhất quán, tránh mất mát dữ liệu hoặc dữ liệu lỗi trong các kịch bản thực thi lỗi.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích "Memory Leak" do Circular Reference và cách GC (Garbage Collector) xử lý.
* **expected_key_points:**
  - id: KP8_1
    content: Tham chiếu vòng
    keypoint_weight: 0.5
    description: Object A trỏ B, B trỏ A. Nếu không ai trỏ tới chúng, bộ đếm tham chiếu sẽ không về 0.
  - id: KP8_2
    content: Cách GC hiện đại (Mark-and-Sweep)
    keypoint_weight: 0.5
    description: GC quét từ các node gốc (roots) để đánh dấu các object còn tiếp cận được. Những object bị cô lập (dù tham chiếu vòng) sẽ bị quét và xóa.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Strong Consistency vs Eventual Consistency trong hệ thống phân tán.
* **expected_key_points:**
  - id: KP9_1
    content: Strong Consistency
    keypoint_weight: 0.5
    description: Mọi node đều thấy cùng dữ liệu ngay lập tức. Đánh đổi: latency cao, khả năng sẵn sàng thấp khi lỗi node.
  - id: KP9_2
    content: Eventual Consistency
    keypoint_weight: 0.5
    description: Dữ liệu giữa các node có thể khác biệt tạm thời, sẽ hội tụ sau. Đánh đổi: trải nghiệm người dùng không đồng nhất ngay lập tức.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Deadlock - Các điều kiện cần (Coffman conditions).
* **expected_key_points:**
  - id: KP10_1
    content: 4 điều kiện
    keypoint_weight: 0.6
    description: Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait.
  - id: KP10_2
    content: Giải pháp phòng ngừa
    keypoint_weight: 0.4
    description: Đánh số tài nguyên để tránh Circular Wait hoặc dùng timeout cho các khóa.