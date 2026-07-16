# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2) - Tập Đề Coding Principles và OOP (9)

* **Role:** Backend Developer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích ý nghĩa và vai trò của nguyên lý Single Responsibility Principle (SRP) trong thiết kế phần mềm. Cho ví dụ vi phạm và cách sửa.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa nguyên lý SRP
    keypoint_weight: 0.5
    description: Mỗi lớp/module chỉ nên đảm nhận một trách nhiệm duy nhất và chỉ có duy nhất một lý do để thay đổi.
  - id: KP1_2
    content: Ví dụ vi phạm và cách khắc phục
    keypoint_weight: 0.5
    description: Lớp `UserService` vừa xử lý nghiệp vụ người dùng vừa định dạng in file PDF. Cách sửa: Tách phần tạo file PDF sang lớp `UserReportPdfExporter` độc lập.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Dependency Injection (DI) là gì? Việc áp dụng DI mang lại những lợi ích gì cho việc bảo trì mã nguồn ứng dụng?
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa Dependency Injection
    keypoint_weight: 0.5
    description: Là một kỹ thuật thiết kế phần mềm trong đó các phụ thuộc (dependencies) của một đối tượng được truyền vào từ bên ngoài thay vì tự khởi tạo bên trong lớp đó.
  - id: KP2_2
    content: Lợi ích đối với bảo trì và kiểm thử
    keypoint_weight: 0.5
    description: Giúp giảm tính liên kết lỏng lẻo (loose coupling) giữa các thành phần; dễ dàng thay thế triển khai mới; cực kỳ thuận tiện cho việc Mocking dữ liệu khi viết Unit Test.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích khái niệm Đa hình (Polymorphism) trong lập trình hướng đối tượng. Phân biệt sự khác nhau giữa Overloading (Nạp chồng) và Overriding (Ghi đè).
* **expected_key_points:**
  - id: KP3_1
    content: Bản chất của Đa hình
    keypoint_weight: 0.5
    description: Cho phép các đối tượng thuộc các lớp khác nhau phản hồi theo cách riêng của chúng với cùng một thông điệp/hàm.
  - id: KP3_2
    content: Phân biệt Overloading và Overriding
    keypoint_weight: 0.5
    description: Overloading xảy ra trong cùng một lớp (các hàm trùng tên nhưng khác chữ ký/tham số). Overriding xảy ra giữa lớp con và lớp cha (lớp con định nghĩa lại hàm đã có ở lớp cha).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích nguyên lý Liskov Substitution Principle (LSP) trong SOLID. Hãy chỉ ra ví dụ cổ điển về hình vuông kế thừa hình chữ nhật vi phạm nguyên lý này ra sao.
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa nguyên lý LSP
    keypoint_weight: 0.5
    description: Các đối tượng của lớp con phải có khả năng thay thế hoàn toàn cho đối tượng của lớp cha mà không làm thay đổi tính đúng đắn của chương trình.
  - id: KP4_2
    content: Ví dụ hình vuông kế thừa hình chữ nhật
    keypoint_weight: 0.5
    description: Nếu cho hình vuông kế thừa hình chữ nhật: khi ta thay đổi chiều rộng của hình vuông, chiều cao cũng tự thay đổi theo làm phá vỡ logic tính diện tích của hình chữ nhật cha.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh sự khác nhau về bản chất và kịch bản sử dụng giữa hai thành phần: Abstract Class (Lớp trừu tượng) và Interface (Giao diện).
* **expected_key_points:**
  - id: KP5_1
    content: Sự khác biệt về cấu trúc
    keypoint_weight: 0.5
    description: Abstract Class có thể chứa cả các phương thức trừu tượng và phương thức có thân hàm cụ thể, hỗ trợ kế thừa đơn. Interface chỉ khai báo chữ ký hàm (trong ngôn ngữ hiện đại có default method), hỗ trợ đa kế thừa.
  - id: KP5_2
    content: Kịch bản sử dụng phù hợp
    keypoint_weight: 0.5
    description: Dùng Abstract Class khi các lớp con chia sẻ chung bản chất/thuộc tính và hành vi nền tảng. Dùng Interface khi muốn định nghĩa một hành vi chung cho các lớp không liên quan về bản chất.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cơ chế hoạt động và lợi ích của mẫu thiết kế Singleton Pattern. Trong môi trường đa luồng (Multi-threading), Singleton Pattern cần lưu ý điều gì?
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên lý hoạt động và lợi ích
    keypoint_weight: 0.5
    description: Đảm bảo một lớp chỉ có duy nhất một đối tượng thực thể (instance) trong suốt vòng đời ứng dụng và cung cấp điểm truy cập toàn cục tới nó (ví dụ dùng cho Database Connection Pool).
  - id: KP6_2
    content: Đa luồng và cơ chế Double-Checked Locking
    keypoint_weight: 0.5
    description: Trong đa luồng, nhiều thread gọi cùng lúc có thể tạo ra nhiều instances. Cần sử dụng cơ chế đồng bộ hóa (synchronization) kết hợp Double-Checked Locking hoặc sử dụng Lazy Initialization an toàn luồng.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là mẫu thiết kế Repository Pattern? Giải thích vai trò của nó trong việc tách biệt lớp nghiệp vụ (Business Logic) và lớp truy cập dữ liệu (Data Access Layer).
* **expected_key_points:**
  - id: KP7_1
    content: Định nghĩa Repository Pattern
    keypoint_weight: 0.5
    description: Đóng vai trò như một lớp trung gian làm nhiệm vụ ánh xạ giữa nguồn dữ liệu thực tế (DB, Web API) sang các mô hình nghiệp vụ của ứng dụng.
  - id: KP7_2
    content: Tách biệt Business Logic và Data Access
    keypoint_weight: 0.5
    description: Giúp lớp nghiệp vụ không cần biết cụ thể CSDL đang dùng là gì hay viết câu query SQL thế nào, hỗ trợ chuyển đổi DB hoặc Mocking dữ liệu cực kỳ dễ dàng.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp giải quyết sự phụ thuộc vòng (Circular Dependency) giữa hai Service trong dự án sử dụng Dependency Injection Framework (như Spring Boot hoặc NestJS).
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất lỗi Circular Dependency
    keypoint_weight: 0.5
    description: Xảy ra khi Service A yêu cầu khởi tạo Service B, trong khi Service B lại yêu cầu khởi tạo Service A ở hàm constructor, tạo thành vòng lặp vô tận khi build app.
  - id: KP8_2
    content: Các giải pháp khắc phục
    keypoint_weight: 0.5
    description: Sử dụng lazy initialization (ví dụ annotation `@Lazy` trong Spring hoặc `@Inject(forwardRef(...))` trong NestJS); giải pháp tốt nhất là refactor tách phần code phụ thuộc chung sang một Service thứ ba độc lập.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Áp dụng mẫu thiết kế Factory Pattern kết hợp Strategy Pattern để xây dựng module tính toán phí vận chuyển linh hoạt cho nhiều đối tác vận chuyển khác nhau (GHTK, GHN, ViettelPost) trong e-commerce.
* **expected_key_points:**
  - id: KP9_1
    content: Thiết kế các Strategies tính phí
    keypoint_weight: 0.5
    description: Định nghĩa interface `ShippingStrategy` có hàm `calculateFee(...)`. Viết các lớp triển khai cụ thể: `GhtkShippingStrategy`, `GhnShippingStrategy` tính phí theo thuật toán riêng.
  - id: KP9_2
    content: Xây dựng ShippingFactory định tuyến động
    keypoint_weight: 0.5
    description: Thiết kế lớp `ShippingFactory` chứa map các strategies; dựa trên cấu hình đối tác đầu vào, Factory trả về đúng Strategy tương ứng giúp ứng dụng dễ dàng thêm đối tác mới không cần sửa code cũ.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống áp dụng mẫu thiết kế Command Query Responsibility Segregation (CQRS) ở mức cơ bản ở tầng code ứng dụng, tách biệt luồng ghi và đọc dữ liệu.
* **expected_key_points:**
  - id: KP10_1
    content: Tách biệt Model Ghi (Command) và Đọc (Query)
    keypoint_weight: 0.5
    description: Xây dựng các lớp xử lý lệnh ghi (Commands) sửa đổi trạng thái hệ thống và trả về void; xây dựng các lớp xử lý truy vấn đọc (Queries) không làm thay đổi trạng thái và trả về DTOs.
  - id: KP10_2
    content: Lợi ích hiệu năng và phân chia luồng code
    keypoint_weight: 0.5
    description: Giúp tối ưu hóa lớp đọc (chỉ lấy các trường cần thiết, dùng caching mạnh mẽ) và lớp ghi (bảo vệ toàn vẹn nghiệp vụ); cho phép scale độc lập luồng đọc/ghi dễ dàng.

