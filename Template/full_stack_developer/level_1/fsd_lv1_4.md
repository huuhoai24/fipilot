# Bộ Câu Hỏi Phỏng Vấn Full Stack Developer (Level 1)

* **Role:** Full Stack Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong kiến trúc web, hãy giải thích sự khác biệt cơ bản giữa phương thức HTTP GET và POST. Khi nào bạn ưu tiên sử dụng phương thức nào?
* **expected_key_points:**
  - id: KP1_1
    content: Mục đích và tính chất (Idempotency)
    keypoint_weight: 0.5
    description: GET dùng để truy xuất dữ liệu, không làm thay đổi trạng thái server (idempotent), tham số truyền qua URL. POST dùng để tạo/cập nhật tài nguyên, dữ liệu truyền trong body.
  - id: KP1_2
    content: Tính bảo mật và giới hạn dữ liệu
    keypoint_weight: 0.5
    description: GET có giới hạn độ dài URL và kém an toàn do thông tin hiển thị trên URL. POST hỗ trợ dung lượng dữ liệu lớn và bảo mật hơn vì dữ liệu nằm trong body request.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** DOM (Document Object Model) là gì và tại sao nó lại quan trọng đối với JavaScript trên trình duyệt?
* **expected_key_points:**
  - id: KP2_1
    content: DOM là đại diện cấu trúc của trang web
    keypoint_weight: 0.6
    description: DOM là mô hình cấu trúc cây (tree structure) của một tài liệu HTML/XML, được trình duyệt tạo ra sau khi tải trang.
  - id: KP2_2
    content: Khả năng tương tác của JavaScript
    keypoint_weight: 0.4
    description: JavaScript sử dụng DOM để truy cập, thay đổi nội dung, thuộc tính và style của trang web một cách động, cho phép tạo ra các giao diện người dùng tương tác.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong JavaScript, giải thích sự khác biệt giữa `let`, `const` và `var`.
* **expected_key_points:**
  - id: KP3_1
    content: Phạm vi hoạt động (Scope)
    keypoint_weight: 0.5
    description: `var` là function-scoped (hoặc toàn cục), trong khi `let` và `const` là block-scoped (giới hạn trong cặp dấu `{}`).
  - id: KP3_2
    content: Khả năng thay đổi giá trị (Reassignment)
    keypoint_weight: 0.5
    description: `var` và `let` có thể gán lại giá trị mới. `const` dùng để khai báo hằng số, không được phép gán lại sau khi đã khởi tạo.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Cơ chế Asynchronous JavaScript (Async/Await) giải quyết vấn đề gì so với Callback truyền thống?
* **expected_key_points:**
  - id: KP4_1
    content: Khử bỏ Callback Hell
    keypoint_weight: 0.5
    description: Async/Await làm cho code bất đồng bộ trông giống như code đồng bộ, loại bỏ tình trạng code bị lồng ghép (Callback Hell), tăng khả năng đọc hiểu.
  - id: KP4_2
    content: Xử lý lỗi tập trung với try/catch
    keypoint_weight: 0.5
    description: Thay vì kiểm tra lỗi ở từng hàm callback, Async/Await cho phép sử dụng `try/catch` để xử lý lỗi một cách đồng nhất và chuyên nghiệp.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt cốt lõi giữa kiến trúc cơ sở dữ liệu SQL và NoSQL là gì?
* **expected_key_points:**
  - id: KP5_1
    content: Cấu trúc dữ liệu và Schema
    keypoint_weight: 0.4
    description: SQL dựa trên bảng quan hệ (relational) với schema cố định, NoSQL hỗ trợ đa dạng cấu trúc (document, key-value) với schema linh hoạt.
  - id: KP5_2
    content: Khả năng mở rộng
    keypoint_weight: 0.3
    description: SQL thường mở rộng theo chiều dọc (scale-up), NoSQL mở rộng hiệu quả theo chiều ngang (scale-out).
  - id: KP5_3
    content: Tính nhất quán (ACID vs BASE)
    keypoint_weight: 0.3
    description: SQL ưu tiên ACID (tính nhất quán cao), NoSQL ưu tiên BASE (tính sẵn sàng và hiệu suất).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Vai trò của Middleware trong các Framework backend (như Express.js) là gì?
* **expected_key_points:**
  - id: KP6_1
    content: Xử lý request/response tập trung
    keypoint_weight: 0.5
    description: Middleware là hàm đứng giữa request và response, cho phép thực thi logic trước khi đến handler chính hoặc trước khi trả về client.
  - id: KP6_2
    content: Ứng dụng phổ biến
    keypoint_weight: 0.5
    description: Dùng để xác thực (Authentication), kiểm tra quyền (Authorization), ghi log, hoặc parse dữ liệu đầu vào.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh Server-side Rendering (SSR) và Client-side Rendering (CSR).
* **expected_key_points:**
  - id: KP7_1
    content: SSR xử lý render tại server
    keypoint_weight: 0.5
    description: Server tạo HTML hoàn chỉnh rồi gửi về trình duyệt, hỗ trợ SEO tốt và nội dung hiển thị nhanh ngay từ đầu.
  - id: KP7_2
    content: CSR xử lý render tại client
    keypoint_weight: 0.5
    description: Trình duyệt tải JS và thực thi render giao diện, mang lại trải nghiệm mượt mà nhưng mất thời gian chờ render ban đầu và SEO khó hơn.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Các nguyên tắc để thiết kế một RESTful API đạt chuẩn là gì?
* **expected_key_points:**
  - id: KP8_1
    content: Tính Stateless và Resource-oriented
    keypoint_weight: 0.5
    description: Server không lưu trạng thái client; mỗi request phải độc lập và dựa trên tài nguyên được định danh qua URI.
  - id: KP8_2
    content: Sử dụng đúng HTTP Methods và Status Codes
    keypoint_weight: 0.5
    description: Dùng đúng chuẩn các phương thức (GET, POST, PUT, DELETE) và mã trạng thái (200, 201, 400, 404, 500) để giao tiếp rõ ràng.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Làm thế nào để tối ưu hóa hiệu năng tải trang cho Frontend (Web Performance Optimization)?
* **expected_key_points:**
  - id: KP9_1
    content: Tối ưu tài nguyên và code
    keypoint_weight: 0.5
    description: Nén ảnh, minify JS/CSS, sử dụng lazy loading, code splitting, tree shaking để giảm khối lượng tải.
  - id: KP9_2
    content: Chiến lược Caching và CDN
    keypoint_weight: 0.5
    description: Sử dụng HTTP Cache, Service Worker, và CDN để phân phối nội dung gần người dùng, giảm độ trễ truy cập.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích lỗi CORS (Cross-Origin Resource Sharing) và cách khắc phục trong thực tế.
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế bảo mật trình duyệt
    keypoint_weight: 0.5
    description: CORS là chính sách bảo mật chặn các request chéo domain để tránh tấn công.
  - id: KP10_2
    content: Cấu hình Header phía Server
    keypoint_weight: 0.5
    description: Cần cấu hình Header `Access-Control-Allow-Origin` phía server để cấp quyền cho phép các domain cụ thể thực hiện request.