# Bộ câu hỏi phỏng vấn Software Engineer (Level 1)

**Thông tin chung:**
* **Role:** Software Engineer
* **Level:** 1 (Junior/Fresher)
* **Experience:** 0 - 2 năm

---

## I. Nhóm câu hỏi dễ (Trọng số 0.15/câu)

### Câu 1: Giải thích sự khác biệt giữa HTTP GET và POST?
* **expected_key_points:**
  - id: KP1.1
    content: Mục đích sử dụng
    keypoint_weight: 0.5
    description: GET dùng để lấy dữ liệu (safe, idempotent), POST dùng để gửi dữ liệu tạo mới/thay đổi trạng thái.
  - id: KP1.2
    content: Cách truyền dữ liệu
    keypoint_weight: 0.3
    description: GET truyền qua URL, POST truyền trong body.
  - id: KP1.3
    content: Tính bảo mật
    keypoint_weight: 0.2
    description: GET hiển thị trên URL nên không dùng cho dữ liệu nhạy cảm, POST an toàn hơn (nhưng vẫn cần SSL).

### Câu 2: Trong lập trình hướng đối tượng (OOP), "Inheritance" và "Composition" khác nhau như thế nào?
* **expected_key_points:**
  - id: KP1.4
    content: Định nghĩa cơ bản
    keypoint_weight: 0.4
    description: Inheritance là quan hệ "is-a", Composition là quan hệ "has-a".
  - id: KP1.5
    content: Tính linh hoạt
    keypoint_weight: 0.4
    description: Inheritance gắn chặt các class, Composition linh hoạt hơn thông qua việc kết hợp các đối tượng.
  - id: KP1.6
    content: Ưu tiên thiết kế
    keypoint_weight: 0.2
    description: Nên ưu tiên "Composition over Inheritance".

### Câu 3: Git Flow cơ bản: Ý nghĩa của lệnh `git fetch` và `git pull`?
* **expected_key_points:**
  - id: KP1.7
    content: Định nghĩa git fetch
    keypoint_weight: 0.5
    description: Cập nhật metadata từ remote về local nhưng không merge.
  - id: KP1.8
    content: Định nghĩa git pull
    keypoint_weight: 0.5
    description: Là sự kết hợp của `fetch` và `merge` (cập nhật code và hợp nhất vào nhánh hiện tại).

---

## II. Nhóm câu hỏi trung bình (Trọng số 0.1/câu)

### Câu 4: Tại sao cần sử dụng Database Index và tác động của nó?
* **expected_key_points:**
  - id: KP2.1
    content: Tăng tốc truy vấn
    keypoint_weight: 0.6
    description: Giảm độ phức tạp từ O(N) xuống O(log N) cho các lệnh SELECT.
  - id: KP2.2
    content: Chi phí thực tế
    keypoint_weight: 0.4
    description: Làm chậm các lệnh INSERT/UPDATE/DELETE và tốn bộ nhớ lưu trữ.

### Câu 5: Phân biệt Process và Thread trong hệ điều hành?
* **expected_key_points:**
  - id: KP2.3
    content: Tài nguyên và không gian bộ nhớ
    keypoint_weight: 0.5
    description: Process độc lập, có không gian riêng; Thread chia sẻ không gian của Process.
  - id: KP2.4
    content: Khả năng giao tiếp
    keypoint_weight: 0.5
    description: Giao tiếp giữa các Thread nhanh hơn nhưng tiềm ẩn lỗi Race Condition.

### Câu 6: Làm sao để tối ưu hóa thời gian load của một ứng dụng Web?
* **expected_key_points:**
  - id: KP2.5
    content: Tối ưu frontend
    keypoint_weight: 0.4
    description: Minify code, sử dụng CDN, nén ảnh (Lazy loading).
  - id: KP2.6
    content: Tối ưu backend
    keypoint_weight: 0.4
    description: Caching (Redis), tối ưu truy vấn DB.
  - id: KP2.7
    content: HTTP performance
    keypoint_weight: 0.2
    description: Hỗ trợ HTTP/2 hoặc sử dụng Browser caching.

### Câu 7: Giải thích nguyên lý Dependency Inversion trong SOLID?
* **expected_key_points:**
  - id: KP2.8
    content: Định nghĩa
    keypoint_weight: 0.6
    description: Module cấp cao không nên phụ thuộc vào module cấp thấp, cả hai nên phụ thuộc vào abstraction (interface).
  - id: KP2.9
    content: Lợi ích
    keypoint_weight: 0.4
    description: Giảm sự gắn kết (decoupling), dễ bảo trì và unit test.

---

## III. Nhóm câu hỏi khó (Trọng số 0.05/câu)

### Câu 8: Khi hệ thống gặp vấn đề Memory Leak trong Python/Java, em sẽ debug như thế nào?
* **expected_key_points:**
  - id: KP3.1
    content: Công cụ giám sát
    keypoint_weight: 0.4
    description: Sử dụng Memory Profiler, VisualVM hoặc Heap dump để phân tích.
  - id: KP3.2
    content: Quy trình loại trừ
    keypoint_weight: 0.4
    description: Kiểm tra các object không được giải phóng, references vòng, hoặc global collections.
  - id: KP3.3
    content: Giải pháp
    keypoint_weight: 0.2
    description: Fix code, tối ưu logic quản lý tài nguyên.

### Câu 9: Sự khác biệt giữa mô hình xử lý bất đồng bộ (Async/Await) và đa luồng (Multi-threading) trong xử lý tác vụ I/O bound?
* **expected_key_points:**
  - id: KP3.4
    content: Bản chất xử lý
    keypoint_weight: 0.5
    description: Async là non-blocking, đơn luồng (event loop); Multi-threading là chạy song song thực sự.
  - id: KP3.5
    content: Hiệu năng/Tài nguyên
    keypoint_weight: 0.5
    description: Async nhẹ hơn, không tốn chi phí context switching như thread.

### Câu 10: Thiết kế hệ thống: Làm sao để đảm bảo tính nhất quán (Consistency) trong một hệ thống phân tán (Distributed System)?
* **expected_key_points:**
  - id: KP3.6
    content: Định luật CAP
    keypoint_weight: 0.5
    description: Hiểu sự đánh đổi giữa Consistency, Availability và Partition Tolerance.
  - id: KP3.7
    content: Cơ chế thực hiện
    keypoint_weight: 0.5
    description: Đề cập đến Two-Phase Commit (2PC), Saga Pattern hoặc Eventual Consistency.
