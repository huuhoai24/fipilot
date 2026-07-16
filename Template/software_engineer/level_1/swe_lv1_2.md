# Bộ Câu Hỏi Phỏng Vấn Software Engineer (Level 1) - Tập Đề Mới (47)

* **Role:** Software Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong lập trình, sự khác biệt giữa `Stack` và `Heap` là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Cách thức quản lý bộ nhớ
    keypoint_weight: 0.6
    description: `Stack` lưu trữ các biến cục bộ, gọi hàm, quản lý theo LIFO (Last In First Out). `Heap` dùng để cấp phát động cho các đối tượng có kích thước không xác định trước.
  - id: KP1_2
    content: Tốc độ và quyền truy cập
    keypoint_weight: 0.4
    description: `Stack` nhanh hơn, có kích thước cố định và được quản lý tự động. `Heap` chậm hơn, kích thước lớn và lập trình viên phải chú ý quản lý (trong các ngôn ngữ bậc thấp).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Định nghĩa "Big O Notation" là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Mục đích sử dụng
    keypoint_weight: 0.5
    description: Dùng để đo lường độ phức tạp (thời gian hoặc không gian) của thuật toán khi quy mô dữ liệu đầu vào tăng lên.
  - id: KP2_2
    content: Ý nghĩa thực tế
    keypoint_weight: 0.5
    description: Cung cấp cận trên (upper bound) của độ tăng trưởng thuật toán, giúp lập trình viên so sánh hiệu năng các hướng tiếp cận khác nhau.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Nguyên lý `Single Responsibility Principle` (SRP) trong SOLID là gì?
* **expected_key_points:**
  - id: KP3_1
    content: Định nghĩa
    keypoint_weight: 0.7
    description: Một lớp (class) hoặc module chỉ nên đảm nhận một chức năng duy nhất và chỉ có một lý do duy nhất để thay đổi.
  - id: KP3_2
    content: Lợi ích
    keypoint_weight: 0.3
    description: Giúp mã nguồn dễ bảo trì, dễ kiểm thử và giảm thiểu tác động lan truyền khi sửa đổi chức năng.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** "Deadlock" trong lập trình đa luồng là gì?
* **expected_key_points:**
  - id: KP4_1
    content: Hiện tượng bế tắc
    keypoint_weight: 0.5
    description: Hai hoặc nhiều luồng chờ đợi lẫn nhau để giải phóng tài nguyên mà đối phương đang nắm giữ, dẫn đến việc không luồng nào thực thi tiếp được.
  - id: KP4_2
    content: Các điều kiện cần (Coffman conditions)
    keypoint_weight: 0.5
    description: Bao gồm: Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong database, `Transaction` đảm bảo các thuộc tính `ACID` nào?
* **expected_key_points:**
  - id: KP5_1
    content: Các thành phần ACID
    keypoint_weight: 0.6
    description: Atomicity (Nguyên tử - hoàn thành tất cả hoặc không gì cả), Consistency (Nhất quán - đúng quy tắc), Isolation (Cô lập), Durability (Bền vững).
  - id: KP5_2
    content: Tầm quan trọng
    keypoint_weight: 0.4
    description: Đảm bảo tính toàn vẹn dữ liệu trong các kịch bản thực thi đồng thời hoặc khi xảy ra sự cố hệ thống.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `Pass-by-value` và `Pass-by-reference`.
* **expected_key_points:**
  - id: KP6_1
    content: Pass-by-value
    keypoint_weight: 0.5
    description: Truyền bản sao của dữ liệu. Hàm nhận được một giá trị độc lập, mọi thay đổi không ảnh hưởng đến biến gốc.
  - id: KP6_2
    content: Pass-by-reference
    keypoint_weight: 0.5
    description: Truyền địa chỉ bộ nhớ. Hàm nhận được tham chiếu, mọi thay đổi sẽ trực tiếp tác động lên dữ liệu gốc.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Dependency Inversion Principle (D) trong SOLID đóng vai trò gì?
* **expected_key_points:**
  - id: KP7_1
    content: Quy tắc chính
    keypoint_weight: 0.5
    description: Module cấp cao không nên phụ thuộc module cấp thấp, mà cả hai nên phụ thuộc vào các Abstraction (Interface/Abstract Class).
  - id: KP7_2
    content: Tác dụng
    keypoint_weight: 0.5
    description: Giảm sự liên kết chặt chẽ (decoupling), cho phép dễ dàng thay thế các module con mà không làm thay đổi logic module chính.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích "Memory Leak" do Circular Reference và cách GC (Garbage Collector) xử lý.
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất tham chiếu vòng
    keypoint_weight: 0.5
    description: Object A trỏ tới B, B trỏ tới A. Nếu không có biến nào khác trỏ tới chúng, chúng vẫn tồn tại trong bộ nhớ vì tham chiếu lẫn nhau.
  - id: KP8_2
    content: Cách GC hiện đại xử lý
    keypoint_weight: 0.5
    description: GC dùng kỹ thuật "Mark-and-Sweep" (đánh dấu và quét) để xác định các object có thể tiếp cận được từ gốc (Root), giúp dọn dẹp các nhóm object cô lập này.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** So sánh Strong Consistency và Eventual Consistency trong hệ thống phân tán.
* **expected_key_points:**
  - id: KP9_1
    content: Strong Consistency
    keypoint_weight: 0.5
    description: Đảm bảo mọi node luôn thấy cùng một dữ liệu ngay sau khi cập nhật, đổi lại tốc độ phản hồi chậm hơn và rủi ro Availability thấp khi có lỗi node.
  - id: KP9_2
    content: Eventual Consistency
    keypoint_weight: 0.5
    description: Node có thể trả về dữ liệu cũ tạm thời, sau đó sẽ đồng bộ hóa sau. Ưu tiên độ sẵn sàng và tốc độ xử lý.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Nguyên lý "Liskov Substitution Principle" (L) trong SOLID là gì?
* **expected_key_points:**
  - id: KP10_1
    content: Nội dung chính
    keypoint_weight: 0.5
    description: Một object thuộc lớp con phải có khả năng thay thế object thuộc lớp cha mà không làm thay đổi tính đúng đắn của chương trình.
  - id: KP10_2
    content: Ví dụ vi phạm
    keypoint_weight: 0.5
    description: Nếu lớp con ném lỗi ngoại lệ (exception) hoặc thay đổi behavior mà lớp cha không mong đợi, nó đã vi phạm nguyên lý này.