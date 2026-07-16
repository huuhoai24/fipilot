# Bộ Câu Hỏi Phỏng Vấn Software Engineer (Level 1) - Tập Đề Mới (52)

* **Role:** Software Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế cơ sở dữ liệu, `Primary Key` khác gì với `Candidate Key`?
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa cơ bản
    keypoint_weight: 0.5
    description: `Candidate Key` là tập hợp các cột có thể định danh duy nhất một bản ghi. `Primary Key` là một trong số các `Candidate Key` được chọn làm khóa chính của bảng.
  - id: KP1_2
    content: Quy tắc ràng buộc
    keypoint_weight: 0.5
    description: `Primary Key` không được chứa giá trị NULL, trong khi các `Candidate Key` còn lại (không được chọn) có thể có các ràng buộc khác nhau tùy thiết kế.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Nguyên lý `Single Responsibility Principle` (S trong SOLID) yêu cầu gì ở code?
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa đơn nhiệm
    keypoint_weight: 0.7
    description: Một lớp hoặc module chỉ nên có một trách nhiệm duy nhất và chỉ có một lý do duy nhất để thay đổi.
  - id: KP2_2
    content: Lợi ích bảo trì
    keypoint_weight: 0.3
    description: Giúp mã nguồn tập trung, giảm thiểu rủi ro khi thay đổi chức năng này làm hỏng chức năng khác.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Git `Fetch` khác gì với `Pull`?
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế Fetch
    keypoint_weight: 0.5
    description: `Fetch` chỉ tải dữ liệu mới từ remote về local nhưng không hợp nhất (merge) vào nhánh hiện tại.
  - id: KP3_2
    content: Cơ chế Pull
    keypoint_weight: 0.5
    description: `Pull` thực chất là tổ hợp của `Fetch` và `Merge`, tải dữ liệu về và tự động hợp nhất vào nhánh làm việc.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là "Deadlock" và điều kiện cần để xảy ra?
* **expected_key_points:**
  - id: KP4_1
    content: Bản chất
    keypoint_weight: 0.4
    description: Tình trạng các tiến trình/luồng bị dừng lại vĩnh viễn do mỗi tiến trình đang giữ tài nguyên mà tiến trình khác cần.
  - id: KP4_2
    content: 4 điều kiện cần
    keypoint_weight: 0.6
    description: Mutual Exclusion (Loại trừ lẫn nhau), Hold and Wait (Nắm giữ và chờ đợi), No Preemption (Không chiếm quyền), Circular Wait (Chờ đợi vòng tròn).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `Database Indexing` và `Full Table Scan`.
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế Full Table Scan
    keypoint_weight: 0.5
    description: Hệ quản trị cơ sở dữ liệu duyệt qua từng dòng một của bảng để tìm kiếm, chi phí I/O cao khi bảng lớn.
  - id: KP5_2
    content: Cơ chế Indexing
    keypoint_weight: 0.5
    description: Sử dụng cấu trúc dữ liệu bổ sung (như B-Tree) để truy xuất dữ liệu trực tiếp, giảm độ phức tạp từ O(n) xuống O(log n).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Dependency Inversion Principle (D) trong SOLID đóng vai trò gì trong kiến trúc phần mềm?
* **expected_key_points:**
  - id: KP6_1
    content: Quy tắc phụ thuộc
    keypoint_weight: 0.5
    description: Phụ thuộc vào Abstraction (Interface) thay vì phụ thuộc vào Implementation cụ thể.
  - id: KP6_2
    content: Lợi ích
    keypoint_weight: 0.5
    description: Tạo ra kiến trúc lỏng (loose coupling), cho phép hoán đổi các module bên dưới mà không làm ảnh hưởng tới module chính.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt `Stack` và `Heap` trong cấp phát bộ nhớ.
* **expected_key_points:**
  - id: KP7_1
    content: Đặc điểm Stack
    keypoint_weight: 0.5
    description: Lưu trữ biến cục bộ, gọi hàm, quản lý LIFO, tốc độ cực nhanh, kích thước cố định.
  - id: KP7_2
    content: Đặc điểm Heap
    keypoint_weight: 0.5
    description: Lưu trữ đối tượng cấp phát động, kích thước linh hoạt, tốc độ chậm hơn, đòi hỏi quản lý bộ nhớ (GC hoặc free).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích Memory Leak do tham chiếu vòng (Circular Reference) và cách Mark-and-Sweep hoạt động.
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất tham chiếu vòng
    keypoint_weight: 0.5
    description: Các đối tượng trỏ lẫn nhau tạo thành nhóm cô lập, nếu dùng Reference Counting sẽ bị giữ lại vĩnh viễn.
  - id: KP8_2
    content: Thuật toán Mark-and-Sweep
    keypoint_weight: 0.5
    description: GC quét từ Root nodes, chỉ giữ lại các đối tượng có đường dẫn tới Root. Nhóm cô lập không có đường dẫn sẽ bị xóa bỏ.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** So sánh các Isolation Level trong Database Transactions.
* **expected_key_points:**
  - id: KP9_1
    content: Các cấp độ phổ biến
    keypoint_weight: 0.5
    description: Read Uncommitted, Read Committed, Repeatable Read, Serializable.
  - id: KP9_2
    content: Đánh đổi (Trade-off)
    keypoint_weight: 0.5
    description: Càng ở mức cao (Serializable) càng an toàn nhưng hiệu năng càng giảm do khóa dữ liệu chặt chẽ và kéo dài.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Nguyên lý "Liskov Substitution Principle" (L) - Các điều kiện để đảm bảo không vi phạm.
* **expected_key_points:**
  - id: KP10_1
    content: Điều kiện về hành vi
    keypoint_weight: 0.5
    description: Lớp con không được ném ra exception mà lớp cha không mong đợi, không được làm suy yếu điều kiện đầu vào (pre-conditions).
  - id: KP10_2
    content: Mục đích
    keypoint_weight: 0.5
    description: Đảm bảo tính nhất quán khi sử dụng đa hình (polymorphism), giúp chương trình hoạt động đúng khi thay thế lớp cha bằng lớp con.