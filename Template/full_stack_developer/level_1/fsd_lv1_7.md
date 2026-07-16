# Bộ Câu Hỏi Phỏng Vấn Full Stack Developer (Level 1)

* **Role:** Full Stack Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong phát triển web, sự khác biệt chính giữa HTTP GET và HTTP POST là gì? Khi nào nên sử dụng phương thức nào?
* **expected_key_points:**
  - id: KP1_1
    content: Bản chất phương thức GET và POST
    keypoint_weight: 0.6
    description: GET được sử dụng để truy xuất dữ liệu từ server và không làm thay đổi trạng thái server (idempotent), tham số truyền qua URL. POST được sử dụng để gửi dữ liệu đến server để tạo hoặc cập nhật tài nguyên, dữ liệu nằm trong body của request.
  - id: KP1_2
    content: Tính bảo mật và hạn chế
    keypoint_weight: 0.4
    description: GET bị giới hạn về độ dài URL và không dùng cho dữ liệu nhạy cảm. POST không bị giới hạn độ dài và an toàn hơn cho dữ liệu nhạy cảm vì không hiển thị trên URL.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích khái niệm DOM (Document Object Model) trong phát triển Front-end.
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa DOM là cây cấu trúc của trang web
    keypoint_weight: 0.5
    description: DOM là giao diện lập trình cho các tài liệu HTML và XML, biểu diễn tài liệu dưới dạng một cấu trúc cây các đối tượng (nodes).
  - id: KP2_2
    content: Vai trò của DOM đối với JavaScript
    keypoint_weight: 0.5
    description: DOM cho phép JavaScript truy cập, chỉnh sửa nội dung, cấu trúc và kiểu dáng của trang web một cách động.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Sự khác biệt giữa `let`, `const` và `var` trong JavaScript là gì?
* **expected_key_points:**
  - id: KP3_1
    content: Phạm vi hoạt động (Scope)
    keypoint_weight: 0.5
    description: `var` có phạm vi function-scope, trong khi `let` và `const` có phạm vi block-scope.
  - id: KP3_2
    content: Khả năng gán lại giá trị (Reassignment)
    keypoint_weight: 0.5
    description: `var` và `let` cho phép gán lại giá trị, còn `const` khai báo hằng số không thể gán lại sau khi đã khởi tạo.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Cơ chế hoạt động của Asynchronous JavaScript (Async/Await) là gì so với Callback?
* **expected_key_points:**
  - id: KP4_1
    content: Tránh Callback Hell
    keypoint_weight: 0.4
    description: Async/Await làm cho code bất đồng bộ trông giống như code đồng bộ, giúp dễ đọc và bảo trì hơn thay vì lồng ghép các callback (Callback Hell).
  - id: KP4_2
    content: Cơ chế Promise
    keypoint_weight: 0.3
    description: Async/Await thực chất là cú pháp rút gọn của Promise, giúp xử lý các tác vụ bất đồng bộ một cách tuần tự.
  - id: KP4_3
    content: Xử lý lỗi (Error Handling)
    keypoint_weight: 0.3
    description: Sử dụng `try/catch` để xử lý lỗi trong Async/Await thay vì phải kiểm tra lỗi trong từng hàm callback.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong thiết kế cơ sở dữ liệu, sự khác biệt giữa SQL và NoSQL là gì?
* **expected_key_points:**
  - id: KP5_1
    content: Cấu trúc dữ liệu
    keypoint_weight: 0.4
    description: SQL dựa trên bảng (relational) với schema cố định, NoSQL linh hoạt (document, key-value, graph) với schema động.
  - id: KP5_2
    content: Khả năng mở rộng (Scalability)
    keypoint_weight: 0.3
    description: SQL thường mở rộng theo chiều dọc (vertical), NoSQL mở rộng tốt theo chiều ngang (horizontal).
  - id: KP5_3
    content: Tính nhất quán (ACID vs BASE)
    keypoint_weight: 0.3
    description: SQL ưu tiên ACID (tính nhất quán), NoSQL thường ưu tiên tính sẵn sàng và hiệu suất (BASE).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Middleware trong Express.js (hoặc backend framework) có ý nghĩa gì trong một request/response cycle?
* **expected_key_points:**
  - id: KP6_1
    content: Chức năng xử lý trung gian
    keypoint_weight: 0.5
    description: Middleware là các hàm đứng giữa request và response, có khả năng sửa đổi request/response hoặc dừng chu trình xử lý.
  - id: KP6_2
    content: Các trường hợp sử dụng phổ biến
    keypoint_weight: 0.5
    description: Dùng cho xác thực (Authentication), logging, parse body, hoặc kiểm tra quyền hạn (Authorization).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa Server-side rendering (SSR) và Client-side rendering (CSR) trong các ứng dụng web hiện đại?
* **expected_key_points:**
  - id: KP7_1
    content: SSR xử lý tại server
    keypoint_weight: 0.5
    description: Server tạo HTML hoàn chỉnh và gửi về browser, cải thiện SEO và tốc độ tải trang ban đầu.
  - id: KP7_2
    content: CSR xử lý tại client
    keypoint_weight: 0.5
    description: Browser tải file JS trống rồi thực thi để render giao diện, giúp trải nghiệm người dùng sau khi tải trang mượt mà hơn nhưng kém SEO hơn.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích khái niệm RESTful API và các nguyên tắc cốt lõi để một API được coi là RESTful.
* **expected_key_points:**
  - id: KP8_1
    content: Statelessness
    keypoint_weight: 0.4
    description: Server không lưu trạng thái client giữa các request; mỗi request phải chứa đủ thông tin để xử lý.
  - id: KP8_2
    content: Resource-based
    keypoint_weight: 0.3
    description: Tài nguyên được định nghĩa qua URI (đường dẫn tài nguyên).
  - id: KP8_3
    content: Uniform Interface
    keypoint_weight: 0.3
    description: Sử dụng chuẩn các HTTP methods (GET, POST, PUT, DELETE) và các trạng thái phản hồi chuẩn.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Làm thế nào để tối ưu hiệu năng cho ứng dụng web (Frontend)?
* **expected_key_points:**
  - id: KP9_1
    content: Tối ưu tài nguyên (Assets)
    keypoint_weight: 0.4
    description: Nén ảnh, minify JS/CSS, sử dụng lazy loading, CDN để phân phối nội dung.
  - id: KP9_2
    content: Tối ưu code và render
    keypoint_weight: 0.3
    description: Code splitting, tree shaking, sử dụng virtual DOM, tránh re-render không cần thiết.
  - id: KP9_3
    content: Caching
    keypoint_weight: 0.3
    description: Sử dụng Browser caching, Service Worker, hoặc HTTP caching để giảm thời gian tải lại trang.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích về Cross-Origin Resource Sharing (CORS) và cách xử lý lỗi CORS trong ứng dụng thực tế.
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế bảo mật trình duyệt
    keypoint_weight: 0.4
    description: CORS là một cơ chế bảo mật cho phép trình duyệt chặn các request từ domain này tới domain khác nếu server không cho phép.
  - id: KP10_2
    content: Cấu hình Header phía Server
    keypoint_weight: 0.3
    description: Server cần gửi kèm Header `Access-Control-Allow-Origin` để chỉ định domain nào được phép truy cập.
  - id: KP10_3
    content: Preflight Request
    keypoint_weight: 0.3
    description: Hiểu về request OPTIONS được trình duyệt gửi trước để hỏi server về quyền truy cập trước khi thực hiện các hành động thay đổi dữ liệu.