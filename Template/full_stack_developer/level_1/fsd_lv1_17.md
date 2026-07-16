# Bộ Câu Hỏi Phỏng Vấn Full Stack Developer (Level 1) - Tập Đề Mới (10)

* **Role:** Full Stack Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, sự khác biệt giữa `padding` và `margin` là gì? Khi nào bạn chọn sử dụng cái nào?
* **expected_key_points:**
  - id: KP1_1
    content: Vị trí tác động (Box Model)
    keypoint_weight: 0.5
    description: `padding` tạo khoảng cách giữa nội dung của phần tử và đường viền (border) của chính nó. `margin` tạo khoảng cách bên ngoài đường viền, giữa phần tử đó và các phần tử xung quanh.
  - id: KP1_2
    content: Khi nào sử dụng
    keypoint_weight: 0.5
    description: Dùng `padding` khi muốn thay đổi không gian nội bộ hoặc màu nền cần lan rộng ra ngoài nội dung. Dùng `margin` để tách biệt, tạo khoảng hở giữa các khối phần tử với nhau.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** JavaScript có cơ chế "Garbage Collection" (dọn dẹp rác) như thế nào? Tại sao bạn không cần xóa biến thủ công như trong ngôn ngữ C?
* **expected_key_points:**
  - id: KP2_1
    content: Cơ chế Mark-and-Sweep
    keypoint_weight: 0.5
    description: JS tự động xác định các đối tượng không còn được tham chiếu (không thể truy cập được từ root) và tự giải phóng bộ nhớ của chúng.
  - id: KP2_2
    content: Lợi ích tự động
    keypoint_weight: 0.5
    description: Giúp lập trình viên giảm thiểu lỗi bộ nhớ (memory leaks hoặc dangling pointers) so với việc phải quản lý thủ công `malloc`/`free`.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Thẻ `<meta name="viewport" ...>` trong HTML có ý nghĩa gì đối với các trang web di động?
* **expected_key_points:**
  - id: KP3_1
    content: Kiểm soát hiển thị trên di động
    keypoint_weight: 0.5
    description: Thiết lập chiều rộng của viewport bằng với chiều rộng của thiết bị (device-width) và thiết lập tỷ lệ zoom ban đầu (initial-scale=1.0).
  - id: KP3_2
    content: Tầm quan trọng
    keypoint_weight: 0.5
    description: Nếu thiếu thẻ này, trình duyệt mobile sẽ render trang web theo kích thước desktop và thu nhỏ lại, gây khó đọc và không tối ưu cho cảm ứng.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `var`, `let` và `const` về "Hoisting" và "Temporal Dead Zone"?
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế Hoisting
    keypoint_weight: 0.5
    description: Tất cả đều được hoisted (đưa lên đầu scope). `var` khởi tạo là `undefined`, `let`/`const` không khởi tạo.
  - id: KP4_2
    content: Temporal Dead Zone (TDZ)
    keypoint_weight: 0.5
    description: Khoảng thời gian từ khi vào scope đến khi biến được khai báo. Truy cập `let`/`const` trong TDZ gây lỗi `ReferenceError`.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, "Controlled Component" khác gì với "Uncontrolled Component"?
* **expected_key_points:**
  - id: KP5_1
    content: Controlled Component
    keypoint_weight: 0.5
    description: Dữ liệu của form được quản lý thông qua React state và cập nhật qua các hàm xử lý event (onChange).
  - id: KP5_2
    content: Uncontrolled Component
    keypoint_weight: 0.5
    description: Dữ liệu được lấy trực tiếp từ DOM thông qua `ref` khi cần, thay vì đồng bộ hóa liên tục với state.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao Database SQL thường tuân thủ quy tắc "Normalization" (Chuẩn hóa)?
* **expected_key_points:**
  - id: KP6_1
    content: Giảm thiểu dư thừa (Redundancy)
    keypoint_weight: 0.5
    description: Chia nhỏ dữ liệu thành các bảng liên quan để tránh lưu trữ lặp lại thông tin, tiết kiệm bộ nhớ.
  - id: KP6_2
    content: Đảm bảo toàn vẹn dữ liệu
    keypoint_weight: 0.5
    description: Giúp cập nhật dữ liệu ở một nơi là xong, không phải cập nhật nhiều bảng gây lỗi đồng bộ (Data Anomaly).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích ý nghĩa của `Content-Type` header trong HTTP request/response.
* **expected_key_points:**
  - id: KP7_1
    content: Định danh kiểu dữ liệu
    keypoint_weight: 0.5
    description: Header này cho phía nhận biết được body của message đang chứa dữ liệu dạng gì (ví dụ: `application/json`, `text/html`, `multipart/form-data`).
  - id: KP7_2
    content: Tầm quan trọng
    keypoint_weight: 0.5
    description: Nếu không có header này, phía nhận không biết cách parse (giải mã) dữ liệu đúng cách, dẫn đến lỗi xử lý dữ liệu.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Sự khác biệt giữa "Event Loop" trong Browser và Node.js là gì?
* **expected_key_points:**
  - id: KP8_1
    content: Môi trường thực thi
    keypoint_weight: 0.5
    description: Browser có các tác vụ liên quan đến UI/Rendering, trong khi Node.js tập trung vào file system, network và các tác vụ hệ thống (libuv).
  - id: KP8_2
    content: Cấu trúc Queue
    keypoint_weight: 0.5
    description: Node.js có các Phase cụ thể (Timers, Poll, Check) trong Event Loop, trong khi browser tập trung vào việc ưu tiên Macrotasks và Microtasks liên quan đến trình duyệt.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao việc sử dụng "Nested Callbacks" trong lập trình bất đồng bộ bị coi là xấu?
* **expected_key_points:**
  - id: KP9_1
    content: Callback Hell
    keypoint_weight: 0.5
    description: Code bị thụt lề quá sâu (kim tự tháp), làm cho việc đọc hiểu luồng logic cực kỳ khó khăn.
  - id: KP9_2
    content: Khó quản lý lỗi
    keypoint_weight: 0.5
    description: Việc bắt lỗi (Error Handling) phải thực hiện ở từng tầng, dễ quên bắt lỗi và logic xử lý trở nên rời rạc, khó kiểm soát.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Khái niệm "Optimistic UI Updates" là gì và lợi ích của nó trong trải nghiệm người dùng (UX)?
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Là kỹ thuật cập nhật giao diện ngay lập tức trước khi nhận được phản hồi (response) thành công từ server.
  - id: KP10_2
    content: Lợi ích UX
    keypoint_weight: 0.5
    description: Làm cho ứng dụng có cảm giác phản hồi tức thì (cực nhanh), giảm độ trễ cảm nhận cho người dùng, sau đó mới âm thầm đồng bộ hoặc rollback nếu lỗi.