# Bộ Câu Hỏi Phỏng Vấn Software Engineer (Level 1) - Tập Đề Mới (49)

* **Role:** Software Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong lập trình, `Array` và `Linked List` khác nhau như thế nào về cách lưu trữ bộ nhớ?
* **expected_key_points:**
  - id: KP1_1
    content: Phân bổ bộ nhớ
    keypoint_weight: 0.6
    description: `Array` sử dụng vùng nhớ liên tục, cho phép truy cập ngẫu nhiên (random access) cực nhanh. `Linked List` sử dụng các nút (nodes) lưu trữ rải rác, kết nối qua con trỏ.
  - id: KP1_2
    content: Hiệu năng thao tác
    keypoint_weight: 0.4
    description: `Array` truy cập O(1) nhưng chèn/xóa chậm. `Linked List` truy cập O(n) nhưng chèn/xóa tại một vị trí (nếu đã có pointer) rất nhanh O(1).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Nguyên lý `Open/Closed Principle` (O trong SOLID) nghĩa là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa
    keypoint_weight: 0.7
    description: Các thực thể phần mềm (class, module) nên mở rộng cho việc mở rộng (open for extension) nhưng đóng lại đối với việc sửa đổi mã nguồn (closed for modification).
  - id: KP2_2
    content: Lợi ích
    keypoint_weight: 0.3
    description: Cho phép thêm tính năng mới mà không làm ảnh hưởng đến mã nguồn hiện có đã được kiểm thử ổn định.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao cần sử dụng `Hashing` thay vì lưu trữ mật khẩu ở dạng văn bản thuần (plain text)?
* **expected_key_points:**
  - id: KP3_1
    content: Tính một chiều (One-way)
    keypoint_weight: 0.6
    description: Hàm băm không thể đảo ngược, giúp bảo vệ mật khẩu ngay cả khi cơ sở dữ liệu bị lộ (leak).
  - id: KP3_2
    content: Salt/Pepper
    keypoint_weight: 0.4
    description: Thêm dữ liệu ngẫu nhiên (salt) vào trước khi băm để ngăn chặn tấn công từ điển hoặc bảng tra cứu (Rainbow tables).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là `Dependency Injection` và lợi ích chính của nó?
* **expected_key_points:**
  - id: KP4_1
    content: Cách thức triển khai
    keypoint_weight: 0.5
    description: Các phụ thuộc của một class được truyền (injected) từ bên ngoài (thường qua constructor) thay vì class tự khởi tạo các đối tượng phụ thuộc đó.
  - id: KP4_2
    content: Lợi ích kiểm thử
    keypoint_weight: 0.5
    description: Giúp dễ dàng mock các dịch vụ phụ thuộc khi viết Unit Test, đảm bảo tính cô lập của code.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích hiện tượng `Stack Overflow` và nguyên nhân gây ra nó.
* **expected_key_points:**
  - id: KP5_1
    content: Nguyên nhân
    keypoint_weight: 0.5
    description: Xảy ra khi ngăn xếp (stack) vượt quá dung lượng cho phép, thường do đệ quy vô tận hoặc quá sâu (infinite recursion).
  - id: KP5_2
    content: Quản lý Stack Frame
    keypoint_weight: 0.5
    description: Mỗi lời gọi hàm tạo ra một Stack Frame; đệ quy không có điểm dừng làm đầy bộ nhớ stack liên tục.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao Database Transaction Isolation Level `Serializable` lại gây ra vấn đề về hiệu năng?
* **expected_key_points:**
  - id: KP6_1
    content: Tính chất Serializable
    keypoint_weight: 0.5
    description: Đảm bảo giao dịch thực thi như thể chúng đang chạy tuần tự, ngăn chặn hoàn toàn mọi lỗi tranh chấp (read/write conflict).
  - id: KP6_2
    content: Đánh đổi hiệu năng
    keypoint_weight: 0.5
    description: Yêu cầu khóa (locking) dữ liệu ở phạm vi rộng và thời gian dài, gây nghẽn (contention) nghiêm trọng cho hệ thống cần xử lý đồng thời.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt `Process` và `Thread` trong hệ điều hành.
* **expected_key_points:**
  - id: KP7_1
    content: Bản chất
    keypoint_weight: 0.5
    description: `Process` là chương trình đang chạy với bộ nhớ riêng biệt. `Thread` là đơn vị thực thi nhỏ nhất bên trong process, chia sẻ chung bộ nhớ với các thread khác.
  - id: KP7_2
    content: Tài nguyên
    keypoint_weight: 0.5
    description: `Process` tốn tài nguyên khởi tạo hơn. Giao tiếp giữa các process khó hơn (IPC), còn các thread giao tiếp dễ dàng do chung vùng nhớ.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích cơ chế "Mark-and-Sweep" của Garbage Collector.
* **expected_key_points:**
  - id: KP8_1
    content: Giai đoạn Mark (Đánh dấu)
    keypoint_weight: 0.5
    description: GC quét từ các node gốc (Root) xuống, đánh dấu tất cả các đối tượng còn có thể tiếp cận được (reachable).
  - id: KP8_2
    content: Giai đoạn Sweep (Quét/Dọn)
    keypoint_weight: 0.5
    description: Quét toàn bộ bộ nhớ, những đối tượng không được đánh dấu sẽ bị giải phóng vì chúng không còn đường dẫn tới từ các Root.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** So sánh CAP Theorem trong hệ thống phân tán.
* **expected_key_points:**
  - id: KP9_1
    content: 3 yếu tố
    keypoint_weight: 0.5
    description: Consistency (Nhất quán), Availability (Sẵn sàng), Partition Tolerance (Chịu lỗi phân mảnh mạng).
  - id: KP9_2
    content: Định luật
    keypoint_weight: 0.5
    description: Hệ thống chỉ có thể đảm bảo 2 trong 3 tính chất đồng thời. Trong trường hợp có lỗi mạng (P), buộc phải chọn giữa Consistency hoặc Availability.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Nguyên lý "Liskov Substitution Principle" (L) trong SOLID là gì?
* **expected_key_points:**
  - id: KP10_1
    content: Quy tắc thay thế
    keypoint_weight: 0.5
    description: Các đối tượng của lớp con phải thay thế được lớp cha mà không làm hỏng tính logic của hệ thống.
  - id: KP10_2
    content: Hậu quả vi phạm
    keypoint_weight: 0.5
    description: Nếu lớp con thay đổi behavior (như ném lỗi unexpected) hoặc làm suy yếu tiền điều kiện (preconditions), nó vi phạm nguyên lý, dẫn đến code dễ lỗi khi mở rộng.