# Bộ Câu Hỏi Phỏng Vấn Software Engineer (Level 1) - Tập Đề Mới (Python & Hệ Thống)

* **Role:** Software Engineer
* **Level:** Level 1 (Junior)
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1: Sự khác biệt giữa Interface và Abstract Class trong OOP
* **expected_key_points:**
  - id: KP1_1
    content: Mục đích kế thừa
    keypoint_weight: 0.5
    description: Interface định nghĩa hành vi (hợp đồng) mà các class khác phải triển khai. Abstract Class cung cấp khung sườn (cơ sở) cho các class con có chung bản chất.
  - id: KP1_2
    content: Tính đa kế thừa
    keypoint_weight: 0.5
    description: Một class có thể implement nhiều Interface, nhưng chỉ có thể kế thừa từ một Abstract Class.

### Câu 2: Giải thích độ phức tạp thời gian O(1) và O(n)
* **expected_key_points:**
  - id: KP2_1
    content: O(1) - Thời gian hằng số
    keypoint_weight: 0.5
    description: Thời gian thực thi không phụ thuộc vào kích thước dữ liệu (ví dụ: truy cập phần tử mảng theo index).
  - id: KP2_2
    content: O(n) - Thời gian tuyến tính
    keypoint_weight: 0.5
    description: Thời gian tăng tỷ lệ thuận với số lượng phần tử (ví dụ: duyệt qua một danh sách).

### Câu 3: Cách thức hoạt động của cơ bản của HTTP Method GET vs POST
* **expected_key_points:**
  - id: KP3_1
    content: GET
    keypoint_weight: 0.5
    description: Dùng để truy xuất dữ liệu, tham số được gửi qua URL, có thể cache.
  - id: KP3_2
    content: POST
    keypoint_weight: 0.5
    description: Dùng để gửi dữ liệu tạo mới, dữ liệu nằm trong body, bảo mật hơn (không lưu trên URL).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4: Sự khác biệt giữa Shallow Copy và Deep Copy
* **expected_key_points:**
  - id: KP4_1
    content: Shallow Copy
    keypoint_weight: 0.5
    description: Sao chép các tham chiếu của các đối tượng con. Nếu đối tượng con thay đổi, bản copy cũng thay đổi.
  - id: KP4_2
    content: Deep Copy
    keypoint_weight: 0.5
    description: Sao chép toàn bộ cây đối tượng, tạo ra các bản sao độc lập hoàn toàn.

### Câu 5: Lỗi phổ biến NullPointerException và cách phòng tránh
* **expected_key_points:**
  - id: KP5_1
    content: Nguyên nhân
    keypoint_weight: 0.5
    description: Truy cập phương thức hoặc thuộc tính của một đối tượng chưa được khởi tạo (giá trị là null).
  - id: KP5_2
    content: Cách phòng tránh
    keypoint_weight: 0.5
    description: Sử dụng kiểm tra null (if != null), Optional class (trong Java), hoặc null-safe operators.

### Câu 6: Thế nào là tính ACID trong Database?
* **expected_key_points:**
  - id: KP6_1
    content: Atomicity & Consistency
    keypoint_weight: 0.5
    description: Atomicity (Giao dịch phải hoàn thành tất cả hoặc không gì cả), Consistency (Dữ liệu phải nhất quán sau giao dịch).
  - id: KP6_2
    content: Isolation & Durability
    keypoint_weight: 0.5
    description: Isolation (Các giao dịch không ảnh hưởng lẫn nhau), Durability (Dữ liệu đã commit phải được lưu vĩnh viễn).

### Câu 7: Giải thích về cơ chế Event Loop trong lập trình Async
* **expected_key_points:**
  - id: KP7_1
    content: Event Loop là gì?
    keypoint_weight: 0.5
    description: Là vòng lặp điều phối các tác vụ bất đồng bộ, giúp chương trình đơn luồng xử lý nhiều tác vụ I/O cùng lúc mà không bị chặn (blocking).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8: Tại sao tham chiếu vòng (Reference Cycles) gây lỗi cho Garbage Collector?
* **expected_key_points:**
  - id: KP8_1
    content: Nguyên nhân
    keypoint_weight: 0.5
    description: Đối tượng A tham chiếu đối tượng B, và B tham chiếu lại A. Khi cả hai không còn sử dụng, Reference Counting vẫn không về 0.
  - id: KP8_2
    content: Cách khắc phục
    keypoint_weight: 0.5
    description: Sử dụng `WeakReference` hoặc các thuật toán GC hiện đại (như Mark-and-Sweep).

### Câu 9: So sánh Strong Consistency và Eventual Consistency
* **expected_key_points:**
  - id: KP9_1
    content: Strong Consistency
    keypoint_weight: 0.5
    description: Mọi node thấy dữ liệu giống hệt nhau tại cùng thời điểm. Đánh đổi độ trễ cao.
  - id: KP9_2
    content: Eventual Consistency
    keypoint_weight: 0.5
    description: Dữ liệu giữa các node có thể khác nhau tạm thời, nhưng sẽ hội tụ về trạng thái cuối cùng. Ưu tiên sẵn sàng (Availability).

### Câu 10: Điều kiện cần để xảy ra Deadlock là gì?
* **expected_key_points:**
  - id: KP10_1
    content: 4 điều kiện Deadlock
    keypoint_weight: 0.5
    description: Mutual Exclusion (Loại trừ lẫn nhau), Hold and Wait (Giữ và chờ), No Preemption (Không chiếm quyền), Circular Wait (Chờ đợi vòng tròn).
