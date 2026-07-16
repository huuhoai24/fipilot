# Bộ Câu Hỏi Phỏng Vấn Software Engineer (Level 1) - Tập Đề Mới (43)

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
    content: Mục đích kế thừa
    keypoint_weight: 0.5
    description: `Interface` định nghĩa một "hợp đồng" (hành vi) mà các class khác phải triển khai. `Abstract Class` cung cấp một khung sườn (cơ sở) cho các class con có chung bản chất.
  - id: KP1_2
    content: Tính đa kế thừa
    keypoint_weight: 0.5
    description: Một class có thể implement nhiều `Interface` (hỗ trợ đa kế thừa hành vi), nhưng chỉ có thể kế thừa từ một `Abstract Class`.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích khái niệm độ phức tạp thời gian `O(1)` và `O(n)` với ví dụ đơn giản.
* **expected_key_points:**
  - id: KP2_1
    content: O(1) - Thời gian hằng số
    keypoint_weight: 0.5
    description: Thời gian thực thi không phụ thuộc vào kích thước dữ liệu (ví dụ: truy cập phần tử trong mảng theo chỉ số).
  - id: KP2_2
    content: O(n) - Thời gian tuyến tính
    keypoint_weight: 0.5
    description: Thời gian thực thi tăng tỷ lệ thuận với số lượng phần tử đầu vào (ví dụ: duyệt qua tất cả phần tử trong danh sách).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Git `rebase` và `merge` khác nhau như thế nào?
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế lịch sử
    keypoint_weight: 0.6
    description: `merge` tạo ra một commit mới để hợp nhất lịch sử. `rebase` viết lại lịch sử commit bằng cách di chuyển các commit hiện tại lên đỉnh của nhánh đích.
  - id: KP3_2
    content: Tính sạch sẽ
    keypoint_weight: 0.4
    description: `rebase` tạo ra lịch sử tuyến tính, dễ nhìn nhưng nguy hiểm nếu làm trên nhánh công cộng. `merge` bảo toàn lịch sử thực tế của các nhánh.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là "Race Condition" trong đa luồng (multi-threading)?
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Xảy ra khi nhiều luồng cùng truy cập và thay đổi dữ liệu dùng chung, kết quả cuối cùng phụ thuộc vào thứ tự thực thi không dự đoán được.
  - id: KP4_2
    content: Cách phòng tránh
    keypoint_weight: 0.5
    description: Sử dụng các cơ chế đồng bộ hóa như `Mutex`, `Semaphore`, hoặc `Locks` để đảm bảo quyền truy cập độc quyền vào tài nguyên.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế truyền tham số `pass-by-value` và `pass-by-reference`.
* **expected_key_points:**
  - id: KP5_1
    content: Pass-by-value
    keypoint_weight: 0.5
    description: Truyền bản sao của giá trị. Thay đổi giá trị trong hàm không ảnh hưởng đến biến gốc bên ngoài.
  - id: KP5_2
    content: Pass-by-reference
    keypoint_weight: 0.5
    description: Truyền tham chiếu (địa chỉ bộ nhớ). Thay đổi nội dung bên trong hàm sẽ tác động trực tiếp lên đối tượng gốc bên ngoài.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là SOLID principles? Hãy nêu ý nghĩa của chữ 'D' (Dependency Inversion).
* **expected_key_points:**
  - id: KP6_1
    content: Tổng quan SOLID
    keypoint_weight: 0.3
    description: Tập hợp 5 nguyên lý thiết kế giúp code dễ bảo trì, linh hoạt và dễ mở rộng.
  - id: KP6_2
    content: Nguyên lý D (Dependency Inversion)
    keypoint_weight: 0.7
    description: Các module cấp cao không nên phụ thuộc vào module cấp thấp, cả hai nên phụ thuộc vào abstraction (interface). Giúp giảm sự phụ thuộc chặt chẽ giữa các thành phần.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao Database Transactions (giao dịch) cần đạt chuẩn ACID?
* **expected_key_points:**
  - id: KP7_1
    content: Các thành phần ACID
    keypoint_weight: 0.5
    description: Atomicity (Tính nguyên tử), Consistency (Tính nhất quán), Isolation (Tính cô lập), Durability (Tính bền vững).
  - id: KP7_2
    content: Ý nghĩa
    keypoint_weight: 0.5
    description: Đảm bảo dữ liệu luôn chính xác và hệ thống có khả năng phục hồi tốt ngay cả khi xảy ra lỗi đột ngột trong quá trình xử lý.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" do Circular References (Tham chiếu vòng) trong các ngôn ngữ có GC (Garbage Collector).
* **expected_key_points:**
  - id: KP8_1
    content: Định nghĩa tham chiếu vòng
    keypoint_weight: 0.5
    description: Object A trỏ đến B, B trỏ ngược lại A, khiến GC đếm tham chiếu (Reference Counting) không về 0 dù không còn biến nào ngoài phạm vi trỏ đến chúng.
  - id: KP8_2
    content: Cách khắc phục
    keypoint_weight: 0.5
    description: Sử dụng `WeakReference` hoặc cấu trúc dữ liệu không có tham chiếu vòng để GC có thể dọn dẹp các đối tượng không còn sử dụng.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** So sánh cơ chế Consistency trong hệ thống phân tán: Strong Consistency vs Eventual Consistency.
* **expected_key_points:**
  - id: KP9_1
    content: Strong Consistency
    keypoint_weight: 0.5
    description: Mọi node đều thấy dữ liệu giống hệt nhau tại cùng một thời điểm. Đánh đổi bằng độ trễ (latency) cao hơn do phải đồng bộ hóa.
  - id: KP9_2
    content: Eventual Consistency
    keypoint_weight: 0.5
    description: Dữ liệu giữa các node có thể khác nhau tạm thời, nhưng sẽ hội tụ về cùng trạng thái sau một khoảng thời gian. Ưu tiên tính sẵn sàng (Availability).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Cơ chế "Deadlock" xảy ra khi nào và các điều kiện cần để xảy ra Deadlock là gì?
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa Deadlock
    keypoint_weight: 0.5
    description: Hai hoặc nhiều luồng dừng hoạt động mãi mãi vì mỗi luồng đang chờ tài nguyên mà luồng kia đang nắm giữ.
  - id: KP10_2
    content: 4 điều kiện cần (Coffman conditions)
    keypoint_weight: 0.5
    description: Mutual Exclusion (Loại trừ lẫn nhau), Hold and Wait (Nắm giữ và chờ đợi), No Preemption (Không chiếm quyền), Circular Wait (Chờ đợi vòng tròn).