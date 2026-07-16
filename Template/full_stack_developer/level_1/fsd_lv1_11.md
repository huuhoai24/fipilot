# Bộ Câu Hỏi Phỏng Vấn Full Stack Developer (Level 1) - Tập Đề Mới (3)

* **Role:** Full Stack Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong HTML, sự khác biệt giữa các thẻ `inline`, `block` và `inline-block` là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Đặc tính về luồng và kích thước
    keypoint_weight: 0.6
    description: `block` chiếm toàn bộ chiều rộng và bắt đầu dòng mới. `inline` chỉ chiếm diện tích nội dung và nằm trên cùng dòng. `inline-block` kết hợp cả hai: nằm cùng dòng nhưng có thể tùy chỉnh width/height/margin/padding.
  - id: KP1_2
    content: Khả năng tùy chỉnh thuộc tính hộp (box model)
    keypoint_weight: 0.4
    description: `block` và `inline-block` hỗ trợ đầy đủ các thuộc tính width/height/margin/padding, trong khi `inline` bị giới hạn về top/bottom margin/padding.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong JavaScript, `const` có thực sự làm biến trở thành bất biến (immutable) không? Tại sao?
* **expected_key_points:**
  - id: KP2_1
    content: const bảo vệ liên kết (binding)
    keypoint_weight: 0.5
    description: `const` chỉ đảm bảo tên biến không được gán lại một giá trị mới (reassignment), không đảm bảo giá trị bên trong biến không thay đổi.
  - id: KP2_2
    content: Tính khả biến của Object/Array
    keypoint_weight: 0.5
    description: Nếu `const` chứa object hoặc array, bạn vẫn có thể thay đổi các thuộc tính hoặc phần tử bên trong object/array đó.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Thuộc tính `alt` trong thẻ `<img>` có ý nghĩa gì?
* **expected_key_points:**
  - id: KP3_1
    content: Hỗ trợ Accessibility
    keypoint_weight: 0.5
    description: Cung cấp nội dung thay thế cho người dùng khiếm thị hoặc sử dụng trình đọc màn hình để hiểu nội dung ảnh.
  - id: KP3_2
    content: Dự phòng khi lỗi tải ảnh và SEO
    keypoint_weight: 0.5
    description: Hiển thị văn bản khi ảnh không load được và giúp bộ máy tìm kiếm (SEO) hiểu nội dung bức ảnh.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** React `Virtual DOM` so với `Real DOM` khác nhau như thế nào về hiệu năng?
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế của Real DOM
    keypoint_weight: 0.5
    description: Thao tác trực tiếp với Real DOM rất đắt đỏ vì nó gây ra việc tái tính toán layout và vẽ lại (repaint) toàn bộ trang web.
  - id: KP4_2
    content: Sự tối ưu của Virtual DOM
    keypoint_weight: 0.5
    description: React sử dụng bản sao nhẹ trong bộ nhớ (Virtual DOM). Khi state thay đổi, nó dùng thuật toán diffing để chỉ cập nhật những phần nhỏ nhất cần thiết vào Real DOM.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm "Closure" trong JavaScript và cho một ví dụ sử dụng thực tế.
* **expected_key_points:**
  - id: KP5_1
    content: Định nghĩa Closure
    keypoint_weight: 0.5
    description: Là hiện tượng một hàm có thể nhớ và truy cập vào các biến ở phạm vi bên ngoài (scope của hàm cha) ngay cả khi hàm cha đã kết thúc thực thi.
  - id: KP5_2
    content: Ví dụ sử dụng
    keypoint_weight: 0.5
    description: Dùng để tạo ra private variables (biến riêng tư) hoặc trong các hàm factory tạo ra hàm khác (currying).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong database SQL, `Primary Key` và `Unique Key` khác nhau ở điểm nào?
* **expected_key_points:**
  - id: KP6_1
    content: Khả năng chứa giá trị NULL
    keypoint_weight: 0.5
    description: `Primary Key` không bao giờ được phép NULL. `Unique Key` cho phép một giá trị NULL (tùy theo hệ quản trị DB).
  - id: KP6_2
    content: Số lượng trong bảng
    keypoint_weight: 0.5
    description: Mỗi bảng chỉ có duy nhất 1 Primary Key, nhưng có thể có nhiều Unique Key.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao nên sử dụng `Environment Variables` (biến môi trường) để lưu trữ cấu hình như API Key hay Database URL?
* **expected_key_points:**
  - id: KP7_1
    content: Tính bảo mật và tránh lộ code
    keypoint_weight: 0.5
    description: Tránh việc lưu cứng (hardcode) dữ liệu nhạy cảm vào source code, giúp bảo vệ secret khi đẩy code lên git.
  - id: KP7_2
    content: Cấu hình linh hoạt theo môi trường
    keypoint_weight: 0.5
    description: Cho phép thay đổi cấu hình giữa môi trường development, staging, production mà không cần phải thay đổi code.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Cơ chế "Throttling" khác "Debouncing" ở điểm nào trong việc xử lý sự kiện DOM?
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất của Debounce
    keypoint_weight: 0.5
    description: Debounce gom nhiều lần gọi thành 1 lần duy nhất sau khi người dùng ngừng tương tác một khoảng thời gian (ví dụ: gõ phím).
  - id: KP8_2
    content: Bản chất của Throttle
    keypoint_weight: 0.5
    description: Throttle đảm bảo hàm được gọi đều đặn theo chu kỳ thời gian nhất định (ví dụ: scroll 100ms/lần).

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao Database Transaction cần tính ACID? Hãy giải thích chữ "I" (Isolation) trong ACID.
* **expected_key_points:**
  - id: KP9_1
    content: Mục đích của ACID
    keypoint_weight: 0.5
    description: ACID đảm bảo tính toàn vẹn dữ liệu trong các giao dịch phức tạp (như chuyển tiền).
  - id: KP9_2
    content: Giải thích Isolation (Cô lập)
    keypoint_weight: 0.5
    description: Đảm bảo các giao dịch chạy song song không nhìn thấy dữ liệu trung gian của nhau, tránh các hiện tượng như dirty read hoặc phantom read.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Bạn hiểu thế nào về "Server-Sent Events" (SSE) và sự khác biệt với WebSockets?
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế hoạt động của SSE
    keypoint_weight: 0.5
    description: SSE là giao tiếp một chiều từ Server tới Client qua HTTP, tự động reconnect và nhẹ hơn WebSockets.
  - id: KP10_2
    content: So sánh với WebSockets
    keypoint_weight: 0.5
    description: WebSockets là song công (full-duplex), phức tạp hơn, phù hợp cho chat/game. SSE phù hợp cho notification/update dữ liệu thực thời đơn chiều.