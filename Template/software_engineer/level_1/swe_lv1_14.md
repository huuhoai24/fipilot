# Bộ Câu Hỏi Phỏng Vấn Software Engineer (Level 1) - Tập Đề Mới (59)

* **Role:** Software Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế cơ sở dữ liệu, `Primary Key` có những ràng buộc bắt buộc nào?
* **expected_key_points:**
  - id: KP1_1
    content: Tính duy nhất (Uniqueness)
    keypoint_weight: 0.5
    description: Giá trị trong cột khóa chính phải là duy nhất, không được phép trùng lặp giữa các dòng trong bảng.
  - id: KP1_2
    content: Tính không rỗng (Non-NULL)
    keypoint_weight: 0.5
    description: Khóa chính không được phép chứa giá trị NULL, vì nó phải đại diện cho một định danh xác định cho bản ghi.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Nguyên lý `Interface Segregation Principle` (I) trong SOLID hướng tới điều gì?
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa
    keypoint_weight: 0.7
    description: Không nên ép buộc các lớp (classes) triển khai những phương thức mà chúng không sử dụng. Nên chia nhỏ các interface lớn thành những interface cụ thể.
  - id: KP2_2
    content: Lợi ích
    keypoint_weight: 0.3
    description: Tăng tính linh hoạt và dễ bảo trì, giúp code không bị phụ thuộc vào các thành phần thừa không liên quan.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao nên sử dụng `Version Control` (Git) thay vì quản lý thủ công (như copy file)?
* **expected_key_points:**
  - id: KP3_1
    content: Truy vết và phục hồi
    keypoint_weight: 0.6
    description: Git lưu lại lịch sử mọi thay đổi, cho phép khôi phục lại các phiên bản code cũ ngay lập tức khi phát hiện lỗi mới.
  - id: KP3_2
    content: Phối hợp hiệu quả
    keypoint_weight: 0.4
    description: Cho phép nhiều lập trình viên cùng làm việc trên một dự án thông qua các nhánh (branch) riêng biệt mà không ghi đè mất mát code của nhau.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là "Race Condition" và cách xử lý phổ biến?
* **expected_key_points:**
  - id: KP4_1
    content: Bản chất
    keypoint_weight: 0.5
    description: Tình trạng nhiều luồng truy cập đồng thời vào một tài nguyên chung, dẫn đến dữ liệu bị sai lệch vì phụ thuộc vào thứ tự chạy không định trước.
  - id: KP4_2
    content: Giải pháp
    keypoint_weight: 0.5
    description: Sử dụng cơ chế khóa như `Mutex` (Mutual Exclusion) để đảm bảo tại một thời điểm chỉ một luồng được thao tác với vùng dữ liệu đó.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt `Pass-by-value` và `Pass-by-reference`.
* **expected_key_points:**
  - id: KP5_1
    content: Pass-by-value
    keypoint_weight: 0.5
    description: Truyền một bản sao dữ liệu. Hàm chỉ thay đổi bản sao, không ảnh hưởng đến biến gốc bên ngoài.
  - id: KP5_2
    content: Pass-by-reference
    keypoint_weight: 0.5
    description: Truyền tham chiếu địa chỉ bộ nhớ. Mọi thay đổi trong hàm sẽ tác động trực tiếp lên đối tượng gốc.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Nguyên lý `Dependency Inversion Principle` (D) trong SOLID có ý nghĩa gì?
* **expected_key_points:**
  - id: KP6_1
    content: Quy tắc
    keypoint_weight: 0.5
    description: Module cấp cao không nên phụ thuộc module cấp thấp, cả hai nên phụ thuộc vào các Abstraction (Interface).
  - id: KP6_2
    content: Tác dụng
    keypoint_weight: 0.5
    description: Tách rời (decoupling) các thành phần, giúp dễ dàng thay thế/nâng cấp mà không làm đổ vỡ logic hệ thống chính.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao Database Transactions (ACID) là khái niệm sống còn?
* **expected_key_points:**
  - id: KP7_1
    content: Các thành phần ACID
    keypoint_weight: 0.5
    description: Atomicity, Consistency, Isolation, Durability.
  - id: KP7_2
    content: Ý nghĩa thực tế
    keypoint_weight: 0.5
    description: Đảm bảo dữ liệu luôn chính xác, nhất quán ngay cả khi hệ thống gặp lỗi đột ngột hoặc có nhiều giao dịch thực thi cùng lúc.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích Memory Leak do tham chiếu vòng và cách GC (Mark-and-Sweep) xử lý.
* **expected_key_points:**
  - id: KP8_1
    content: Tham chiếu vòng
    keypoint_weight: 0.5
    description: Đối tượng A trỏ B, B trỏ A tạo nhóm cô lập. Nếu chỉ đếm số lượng tham chiếu, bộ nhớ sẽ không bao giờ được giải phóng.
  - id: KP8_2
    content: Thuật toán Mark-and-Sweep
    keypoint_weight: 0.5
    description: GC quét từ Root, đánh dấu các đối tượng có thể tiếp cận được. Nhóm đối tượng cô lập sẽ bị quét và xóa (sweep) khỏi bộ nhớ.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** So sánh Strong Consistency vs Eventual Consistency.
* **expected_key_points:**
  - id: KP9_1
    content: Strong Consistency
    keypoint_weight: 0.5
    description: Mọi node thấy dữ liệu giống hệt nhau tức thì. Đánh đổi: latency cao, rủi ro availability khi mạng chập chờn.
  - id: KP9_2
    content: Eventual Consistency
    keypoint_weight: 0.5
    description: Dữ liệu giữa các node khác biệt tạm thời, sẽ hội tụ sau. Ưu tiên: hiệu năng và tính sẵn sàng cao.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Nguyên lý "Liskov Substitution Principle" (L) - Điều kiện không vi phạm.
* **expected_key_points:**
  - id: KP10_1
    content: Quy tắc thay thế
    keypoint_weight: 0.5
    description: Đối tượng lớp con phải thay thế được lớp cha mà không làm sai lệch tính logic của chương trình.
  - id: KP10_2
    content: Điều kiện kiểm tra
    keypoint_weight: 0.5
    description: Lớp con không được ném ra lỗi ngoài dự kiến và phải tuân thủ đúng hợp đồng hành vi đã định nghĩa ở lớp cha.