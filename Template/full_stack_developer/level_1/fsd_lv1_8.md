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
    description: GET được sử dụng để truy xuất dữ liệu từ server mà không làm thay đổi trạng thái server (idempotent), dữ liệu được truyền qua URL. POST được sử dụng để gửi dữ liệu đến server nhằm tạo hoặc cập nhật tài nguyên, dữ liệu được truyền trong body của request.
  - id: KP1_2
    content: Tính bảo mật và giới hạn
    keypoint_weight: 0.4
    description: GET bị giới hạn về độ dài URL và không dùng cho dữ liệu nhạy cảm. POST không bị giới hạn độ dài và an toàn hơn cho dữ liệu nhạy cảm vì dữ liệu không hiển thị trực tiếp trên thanh địa chỉ URL.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích khái niệm DOM (Document Object Model) trong phát triển Front-end.
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa DOM là cây cấu trúc của trang web
    keypoint_weight: 0.5
    description: DOM là giao diện lập trình cho các tài liệu HTML/XML, biểu diễn tài liệu dưới dạng một cấu trúc cây các đối tượng (nodes) mà trình duyệt tạo ra sau khi tải trang.
  - id: KP2_2
    content: Vai trò của DOM đối với JavaScript
    keypoint_weight: 0.5
    description: DOM cho phép JavaScript truy cập, thay đổi nội dung, cấu trúc, kiểu dáng và phản hồi các sự kiện người dùng trên trang web một cách động.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Sự khác biệt giữa `let`, `const` và `var` trong JavaScript hiện đại (ES6+) là gì?
* **expected_key_points:**
  - id: KP3_1
    content: Phạm vi hoạt động (Scope)
    keypoint_weight: 0.5
    description: `var` có phạm vi function-scope, trong khi `let` và `const` có phạm vi block-scope (giới hạn trong cặp dấu `{}`).
  - id: KP3_2
    content: Khả năng gán lại giá trị
    keypoint_weight: 0.5
    description: `var` và `let` cho phép gán lại giá trị, còn `const` khai báo hằng số không thể gán lại sau khi đã khởi tạo lần đầu.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Cơ chế hoạt động của Asynchronous JavaScript (Async/Await) là gì so với Callback truyền thống?
* **expected_key_points:**
  - id: KP4_1
    content: Giải quyết Callback Hell
    keypoint_weight: 0.4
    description: Async/Await làm cho code bất đồng bộ trông giống như code đồng bộ, giúp mã nguồn sạch sẽ, dễ đọc và dễ bảo trì hơn thay vì phải lồng ghép các hàm callback (Callback Hell).
  - id: KP4_2
    content: Bản chất dựa trên Promise
    keypoint_weight: 0.3
    description: Async/Await thực chất là cú pháp rút gọn của Promise, giúp xử lý các tác vụ bất đồng bộ một cách tuần tự và rõ ràng.
  - id: KP4_3
    content: Xử lý lỗi (Error Handling)
    keypoint_weight: 0.3
    description: Sử dụng `try/catch` để xử lý lỗi tập trung trong Async/Await thay vì phải kiểm tra lỗi trong từng hàm callback riêng lẻ.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong thiết kế cơ sở dữ liệu, sự khác biệt chính giữa SQL và NoSQL là gì?
* **expected_key_points:**
  - id: KP5_1
    content: Cấu trúc dữ liệu
    keypoint_weight: 0.4
    description: SQL dựa trên bảng (relational) với schema cố định, NoSQL linh hoạt với các cấu trúc dữ liệu như document, key-value, graph và schema động.
  - id: KP5_2
    content: Khả năng mở rộng (Scalability)
    keypoint_weight: 0.3
    description: SQL thường mở rộng theo chiều dọc (vertical - tăng tài nguyên server), NoSQL mở rộng tốt theo chiều ngang (horizontal - thêm node).
  - id: KP5_3
    content: Tính nhất quán (ACID vs BASE)
    keypoint_weight: 0.3
    description: SQL ưu tiên ACID (tính nhất quán cao), NoSQL thường ưu tiên tính sẵn sàng (Availability) và hiệu suất (BASE).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Middleware trong Express.js (hoặc các backend framework tương tự) có vai trò gì trong một request/response cycle?
* **expected_key_points:**
  - id: KP6_1
    content: Xử lý trung gian (Request Processing)
    keypoint_weight: 0.5
    description: Middleware là các hàm đứng giữa request và response, có khả năng thực thi code, sửa đổi request/response hoặc dừng chu trình xử lý trước khi đến đích cuối cùng.
  - id: KP6_2
    content: Ứng dụng thực tế
    keypoint_weight: 0.5
    description: Thường dùng để xác thực người dùng (Authentication), ghi log (Logging), xử lý dữ liệu đầu vào (Parser) hoặc kiểm tra quyền hạn (Authorization).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa Server-side rendering (SSR) và Client-side rendering (CSR) trong ứng dụng web?
* **expected_key_points:**
  - id: KP7_1
    content: SSR xử lý tại server
    keypoint_weight: 0.5
    description: Server tạo HTML hoàn chỉnh và gửi về trình duyệt, giúp cải thiện SEO và tốc độ hiển thị nội dung ban đầu.
  - id: KP7_2
    content: CSR xử lý tại client
    keypoint_weight: 0.5
    description: Trình duyệt tải file JS, thực thi để render giao diện, giúp trải nghiệm người dùng sau khi đã tải trang mượt mà hơn nhưng ban đầu SEO kém hơn.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích các nguyên tắc cốt lõi để một API được coi là RESTful API?
* **expected_key_points:**
  - id: KP8_1
    content: Statelessness (Không lưu trạng thái)
    keypoint_weight: 0.4
    description: Server không lưu trạng thái client giữa các request; mỗi request phải chứa đủ thông tin để server hiểu và xử lý.
  - id: KP8_2
    content: Resource-based (Dựa trên tài nguyên)
    keypoint_weight: 0.3
    description: Tài nguyên được đại diện thông qua các URI duy nhất (đường dẫn tài nguyên).
  - id: KP8_3
    content: Uniform Interface
    keypoint_weight: 0.3
    description: Sử dụng chuẩn các HTTP methods (GET, POST, PUT, DELETE) và các mã phản hồi HTTP tiêu chuẩn để tương tác với tài nguyên.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Làm thế nào để tối ưu hóa hiệu năng cho một ứng dụng Web Full Stack?
* **expected_key_points:**
  - id: KP9_1
    content: Tối ưu tài nguyên (Frontend)
    keypoint_weight: 0.4
    description: Nén ảnh, minify JS/CSS, sử dụng lazy loading, phân phối nội dung qua CDN.
  - id: KP9_2
    content: Tối ưu hiệu suất Backend và DB
    keypoint_weight: 0.3
    description: Sử dụng Caching (Redis), đánh Index trong Database, tối ưu câu lệnh truy vấn SQL.
  - id: KP9_3
    content: Kiến trúc ứng dụng
    keypoint_weight: 0.3
    description: Code splitting, tree shaking, sử dụng các cơ chế caching phía trình duyệt và HTTP cache.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Cross-Origin Resource Sharing (CORS) là gì và cách xử lý lỗi CORS trong ứng dụng thực tế?
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế bảo mật trình duyệt
    keypoint_weight: 0.4
    description: CORS là cơ chế bảo mật trình duyệt ngăn chặn request tới domain khác nếu server đích không cho phép.
  - id: KP10_2
    content: Cấu hình phía Server
    keypoint_weight: 0.3
    description: Server cần thiết lập header `Access-Control-Allow-Origin` để liệt kê các domain được phép truy cập.
  - id: KP10_3
    content: Preflight Request
    keypoint_weight: 0.3
    description: Trình duyệt gửi request OPTIONS trước để hỏi quyền server trước khi thực hiện các request thay đổi dữ liệu nguy hiểm.