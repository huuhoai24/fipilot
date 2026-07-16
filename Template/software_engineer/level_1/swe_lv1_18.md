# Bộ Câu Hỏi Phỏng Vấn Software Engineer (Java) - Level 1

* **Role:** Software Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong Java, sự khác biệt giữa `String`, `StringBuilder` và `StringBuffer` là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Tính bất biến (Immutability)
    keypoint_weight: 0.5
    description: `String` là bất biến (mỗi lần sửa đổi sẽ tạo object mới). `StringBuilder` và `StringBuffer` là có thể thay đổi (mutable).
  - id: KP1_2
    content: Tính an toàn luồng (Thread-safety)
    keypoint_weight: 0.5
    description: `StringBuffer` an toàn với đa luồng (synchronized), còn `StringBuilder` không an toàn nhưng nhanh hơn.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích ý nghĩa của từ khóa `static` trong Java.
* **expected_key_points:**
  - id: KP2_1
    content: Phạm vi bộ nhớ
    keypoint_weight: 0.5
    description: `static` dùng cho biến hoặc phương thức thuộc về class chứ không thuộc về bất kỳ instance (đối tượng) cụ thể nào.
  - id: KP2_2
    content: Cách sử dụng
    keypoint_weight: 0.5
    description: Có thể truy cập trực tiếp bằng tên class mà không cần khởi tạo đối tượng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Sự khác biệt giữa `ArrayList` và `LinkedList`?
* **expected_key_points:**
  - id: KP3_1
    content: Cấu trúc dữ liệu
    keypoint_weight: 0.5
    description: `ArrayList` dựa trên mảng động (dynamic array), `LinkedList` dựa trên danh sách liên kết kép (doubly linked list).
  - id: KP3_2
    content: Hiệu năng
    keypoint_weight: 0.5
    description: `ArrayList` truy cập phần tử nhanh ($O(1)$), `LinkedList` chèn/xóa phần tử nhanh hơn nếu đã ở vị trí đó.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Khái niệm `Exception Handling` trong Java: Sự khác biệt giữa `Checked` và `Unchecked Exception`?
* **expected_key_points:**
  - id: KP4_1
    content: Checked Exception
    keypoint_weight: 0.5
    description: Phải được xử lý (try-catch) hoặc khai báo (throws) tại thời điểm biên dịch (ví dụ: IOException).
  - id: KP4_2
    content: Unchecked Exception
    keypoint_weight: 0.5
    description: Xảy ra tại runtime, không bắt buộc phải xử lý (ví dụ: NullPointerException).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là `Dependency Injection` (DI) và tại sao nó lại quan trọng trong Spring Framework?
* **expected_key_points:**
  - id: KP5_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Là kỹ thuật cung cấp các đối tượng phụ thuộc (dependencies) từ bên ngoài thay vì tự tạo bên trong class.
  - id: KP5_2
    content: Lợi ích
    keypoint_weight: 0.5
    description: Giúp code dễ bảo trì, dễ unit test và giảm sự phụ thuộc (loose coupling).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cách hoạt động của `HashMap` trong Java?
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế Hash
    keypoint_weight: 0.5
    description: Dựa trên mã băm (hash code) của Key để xác định vị trí lưu trữ (bucket).
  - id: KP6_2
    content: Xử lý va chạm
    keypoint_weight: 0.5
    description: Xử lý va chạm bằng cách sử dụng Linked List hoặc Red-Black Tree khi nhiều key có cùng hash.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tính đa hình (Polymorphism) trong Java được thể hiện như thế nào (Overloading vs Overriding)?
* **expected_key_points:**
  - id: KP7_1
    content: Overloading (Đa hình tĩnh)
    keypoint_weight: 0.5
    description: Cùng tên phương thức nhưng khác tham số trong cùng một class.
  - id: KP7_2
    content: Overriding (Đa hình động)
    keypoint_weight: 0.5
    description: Class con định nghĩa lại phương thức của class cha.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Cơ chế hoạt động của `Garbage Collector` (GC) trong JVM và khái niệm "Stop-the-world"?
* **expected_key_points:**
  - id: KP8_1
    content: Quản lý bộ nhớ
    keypoint_weight: 0.5
    description: GC tự động nhận diện các đối tượng không còn tham chiếu và giải phóng bộ nhớ.
  - id: KP8_2
    content: Stop-the-world
    keypoint_weight: 0.5
    description: Là trạng thái JVM dừng mọi luồng ứng dụng để thực hiện việc dọn dẹp bộ nhớ an toàn.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao nên ghi đè (`override`) cả `equals()` và `hashCode()` cùng nhau?
* **expected_key_points:**
  - id: KP9_1
    content: Hợp đồng (Contract)
    keypoint_weight: 0.5
    description: Nếu hai đối tượng bằng nhau qua `equals()`, chúng phải có cùng giá trị `hashCode()`.
  - id: KP9_2
    content: Hệ quả
    keypoint_weight: 0.5
    description: Nếu không tuân thủ, các Collection như `HashMap`, `HashSet` sẽ không thể tìm kiếm hoặc lưu trữ đối tượng đúng cách.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Khái niệm `Generics` trong Java giúp ích gì và cơ chế "Type Erasure" là gì?
* **expected_key_points:**
  - id: KP10_1
    content: Lợi ích của Generics
    keypoint_weight: 0.5
    description: Cung cấp kiểm tra kiểu dữ liệu mạnh mẽ tại thời điểm biên dịch, tránh ép kiểu thủ công.
  - id: KP10_2
    content: Type Erasure
    keypoint_weight: 0.5
    description: Là quá trình JVM loại bỏ thông tin kiểu Generics sau khi biên dịch để đảm bảo tương thích ngược với các phiên bản Java cũ.
