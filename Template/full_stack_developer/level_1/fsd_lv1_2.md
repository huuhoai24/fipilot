# Bộ Câu Hỏi Phỏng Vấn Full Stack Developer (Level 1) - Bộ Mới

* **Role:** Full Stack Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, hãy phân biệt cơ chế hiển thị của `display: block`, `display: inline` và `display: inline-block`.
* **expected_key_points:**
  - id: KP1_1
    content: Đặc điểm của block và inline
    keypoint_weight: 0.6
    description: `block` chiếm toàn bộ chiều ngang có sẵn và bắt đầu trên dòng mới. `inline` chỉ chiếm chiều ngang bằng nội dung của nó và không bắt đầu trên dòng mới.
  - id: KP1_2
    content: Đặc điểm của inline-block
    keypoint_weight: 0.4
    description: `inline-block` cho phép element nằm trên cùng một dòng như inline nhưng vẫn có thể thiết lập được chiều rộng (width) và chiều cao (height) như block.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao chúng ta nên sử dụng `rel="noopener noreferrer"` khi dùng thẻ `<a>` với thuộc tính `target="_blank"`?
* **expected_key_points:**
  - id: KP2_1
    content: Vấn đề bảo mật (Tabnabbing)
    keypoint_weight: 0.5
    description: Trang web mới mở ra có thể truy cập đối tượng `window.opener` của trang cũ, cho phép trang đích thực hiện các hành vi độc hại. `noreferrer` ngăn chặn việc gửi thông tin referrer.
  - id: KP2_2
    content: Hiệu năng (Performance)
    keypoint_weight: 0.5
    description: `noopener` ngăn không cho trang mới chạy trên cùng một process với trang cũ, giúp tránh việc trang đích làm chậm (block) main thread của trang gốc.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong JavaScript, sự khác biệt giữa `==` (loose equality) và `===` (strict equality) là gì?
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế so sánh giá trị
    keypoint_weight: 0.5
    description: `==` thực hiện ép kiểu (type coercion) trước khi so sánh, dẫn đến các kết quả đôi khi không trực quan (ví dụ: `0 == '0'` là true).
  - id: KP3_2
    content: Cơ chế so sánh giá trị và kiểu dữ liệu
    keypoint_weight: 0.5
    description: `===` kiểm tra cả giá trị và kiểu dữ liệu, nếu kiểu khác nhau nó sẽ trả về false ngay lập tức mà không ép kiểu.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích nguyên lý hoạt động của `Event Loop` trong Node.js.
* **expected_key_points:**
  - id: KP4_1
    content: Tính chất đơn luồng (Single-threaded)
    keypoint_weight: 0.4
    description: Node.js chạy trên một luồng đơn nhưng vẫn xử lý được nhiều tác vụ nhờ offloading các tác vụ I/O (file, network) ra ngoài luồng chính.
  - id: KP4_2
    content: Call Stack và Callback Queue
    keypoint_weight: 0.3
    description: Call Stack xử lý code đồng bộ. Khi tác vụ bất đồng bộ hoàn thành, callback của nó được đưa vào Queue.
  - id: KP4_3
    content: Vòng lặp Event Loop
    keypoint_weight: 0.3
    description: Event Loop liên tục kiểm tra nếu Call Stack rỗng, nó sẽ lấy các callback từ Queue và đưa vào Stack để thực thi.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, `useEffect` hook dùng để làm gì? Nêu sự khác biệt giữa việc để mảng phụ thuộc (dependency array) là `[]`, không có mảng, và có phần tử `[data]`.
* **expected_key_points:**
  - id: KP5_1
    content: Mục đích của useEffect
    keypoint_weight: 0.4
    description: Dùng để xử lý side-effects (gọi API, subscriptions, DOM manipulation) sau khi component render.
  - id: KP5_2
    content: Các trạng thái dependency array
    keypoint_weight: 0.6
    description: `[]`: chỉ chạy 1 lần khi mount. Không có: chạy sau mỗi lần render. `[data]`: chỉ chạy khi `data` thay đổi.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao nên sử dụng Index trong Database và nhược điểm của việc lạm dụng Index là gì?
* **expected_key_points:**
  - id: KP6_1
    content: Tăng tốc độ truy vấn (Read)
    keypoint_weight: 0.5
    description: Index giúp database tìm kiếm bản ghi mà không cần quét toàn bộ bảng (Full Table Scan), giống như mục lục của cuốn sách.
  - id: KP6_2
    content: Nhược điểm về hiệu năng ghi (Write) và lưu trữ
    keypoint_weight: 0.5
    description: Mỗi khi thêm/sửa/xóa dữ liệu, index phải được cập nhật lại, gây tốn tài nguyên và thời gian ghi. Index cũng tốn thêm dung lượng lưu trữ trên disk.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** JWT (JSON Web Token) là gì và tại sao nó lại được ưu tiên dùng trong các ứng dụng stateless thay vì Session dựa trên Cookie?
* **expected_key_points:**
  - id: KP7_1
    content: Cấu trúc của JWT
    keypoint_weight: 0.4
    description: Gồm 3 phần: Header, Payload và Signature, tất cả được mã hóa Base64URL.
  - id: KP7_2
    content: Tính Stateless
    keypoint_weight: 0.3
    description: Server không cần lưu trạng thái session trong database, vì mọi thông tin cần thiết đều nằm trong token của client.
  - id: KP7_3
    content: Phù hợp hệ thống phân tán
    keypoint_weight: 0.3
    description: JWT cho phép các service khác nhau xác thực cùng một token mà không cần hỏi lại server lưu trữ session.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Hoisting" trong JavaScript. Tại sao `let` và `const` được gọi là có "Temporal Dead Zone"?
* **expected_key_points:**
  - id: KP8_1
    content: Hoisting là đưa khai báo lên trên cùng
    keypoint_weight: 0.5
    description: JavaScript đưa khai báo biến lên đầu scope trước khi thực thi code. `var` được khởi tạo là `undefined`, còn `let/const` không được khởi tạo.
  - id: KP8_2
    content: Temporal Dead Zone (TDZ)
    keypoint_weight: 0.5
    description: Là khoảng thời gian từ lúc vào scope đến khi khai báo `let/const` được thực thi. Trong vùng này, biến tồn tại nhưng chưa thể truy cập, gây lỗi ReferenceError nếu cố sử dụng.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Nêu cơ chế "Virtual DOM" trong React hoạt động như thế nào để tối ưu hóa hiệu năng render?
* **expected_key_points:**
  - id: KP9_1
    content: Bản sao nhẹ của DOM
    keypoint_weight: 0.5
    description: React giữ một bản sao của DOM trong bộ nhớ (Virtual DOM). Khi state thay đổi, React tạo bản sao mới của Virtual DOM.
  - id: KP9_2
    content: Thuật toán Diffing (Reconciliation)
    keypoint_weight: 0.5
    description: React so sánh (diff) Virtual DOM cũ và mới để xác định chính xác những phần nào đã thay đổi, sau đó chỉ cập nhật những phần đó vào Real DOM, giảm thiểu thao tác nặng trên DOM thật.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong backend API, tại sao cơ chế "Rate Limiting" lại quan trọng và các chiến lược thực hiện nó?
* **expected_key_points:**
  - id: KP10_1
    content: Bảo vệ hệ thống
    keypoint_weight: 0.5
    description: Rate Limiting ngăn chặn việc lạm dụng API (DDoS, Brute force, scraping), đảm bảo tài nguyên server không bị quá tải.
  - id: KP10_2
    content: Các chiến lược Rate Limiting
    keypoint_weight: 0.5
    description: Token Bucket (cho phép burst), Leaky Bucket (lưu lượng ổn định), Fixed Window hoặc Sliding Window (giới hạn theo thời gian).