# Bộ Câu Hỏi Phỏng Vấn Web Developer (Level 1) - Tập Đề Mới (22)

* **Role:** Web Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, sự khác biệt giữa `inline`, `block` và `inline-block` là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Đặc tính chiếm chỗ (Box Model)
    keypoint_weight: 0.6
    description: `block` chiếm toàn bộ chiều rộng. `inline` chỉ chiếm không gian bằng nội dung. `inline-block` nằm trên cùng một dòng nhưng cho phép tùy chỉnh width/height/margin/padding.
  - id: KP1_2
    content: Luồng tài liệu (Flow)
    keypoint_weight: 0.4
    description: `block` luôn bắt đầu dòng mới, trong khi `inline` và `inline-block` cho phép các phần tử khác nằm cùng dòng.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Sự khác biệt giữa `==` (loose equality) và `===` (strict equality) trong JavaScript?
* **expected_key_points:**
  - id: KP2_1
    content: Cơ chế so sánh
    keypoint_weight: 0.5
    description: `==` thực hiện ép kiểu (type coercion) nếu hai vế khác kiểu dữ liệu. `===` kiểm tra cả giá trị và kiểu dữ liệu (không ép kiểu).
  - id: KP2_2
    content: Tính an toàn
    keypoint_weight: 0.5
    description: Dùng `===` được khuyến khích để tránh các lỗi logic khó đoán do cơ chế ép kiểu tự động của JavaScript gây ra.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Thẻ `alt` trong thẻ `<img>` có ý nghĩa gì đối với SEO và Accessibility?
* **expected_key_points:**
  - id: KP3_1
    content: Hỗ trợ người dùng khiếm thị
    keypoint_weight: 0.5
    description: Cung cấp mô tả thay thế cho các công cụ đọc màn hình (screen readers) để người khiếm thị hiểu nội dung ảnh.
  - id: KP3_2
    content: Dự phòng và SEO
    keypoint_weight: 0.5
    description: Hiển thị khi ảnh không tải được và giúp các máy tìm kiếm (Google) hiểu nội dung ảnh thông qua văn bản thay vì chỉ là tệp tin.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, sự khác biệt giữa `State` và `Props` là gì?
* **expected_key_points:**
  - id: KP4_1
    content: Quyền sở hữu và chỉnh sửa
    keypoint_weight: 0.5
    description: `Props` là dữ liệu nhận từ cha (read-only). `State` là dữ liệu nội tại, có thể thay đổi bởi chính component đó.
  - id: KP4_2
    content: Tính chất
    keypoint_weight: 0.5
    description: Props dùng để cấu hình/truyền thông tin. State dùng để quản lý các giá trị biến động theo tương tác người dùng.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm `Closures` trong JavaScript.
* **expected_key_points:**
  - id: KP5_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Là hiện tượng hàm con có khả năng ghi nhớ và truy cập vào các biến ở phạm vi (scope) của hàm cha ngay cả khi hàm cha đã kết thúc.
  - id: KP5_2
    content: Ứng dụng
    keypoint_weight: 0.5
    description: Thường dùng để tạo private variables (biến riêng tư) hoặc các hàm tạo (factory functions).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** `Left Join` và `Inner Join` trong SQL khác nhau như thế nào?
* **expected_key_points:**
  - id: KP6_1
    content: Inner Join
    keypoint_weight: 0.5
    description: Chỉ trả về các bản ghi có dữ liệu khớp (match) ở cả hai bảng được join.
  - id: KP6_2
    content: Left Join
    keypoint_weight: 0.5
    description: Trả về tất cả bản ghi từ bảng bên trái, và các bản ghi khớp từ bảng phải. Nếu không khớp ở bảng phải thì trả về giá trị NULL.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao nên dùng `Environment Variables` (biến môi trường) trong dự án web?
* **expected_key_points:**
  - id: KP7_1
    content: Bảo mật
    keypoint_weight: 0.5
    description: Tránh hardcode các khóa bảo mật (API keys, DB credentials) vào mã nguồn khi đẩy lên git.
  - id: KP7_2
    content: Tính linh hoạt
    keypoint_weight: 0.5
    description: Dễ dàng cấu hình ứng dụng cho các môi trường khác nhau (dev, staging, production) mà không cần thay đổi code.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao `React.memo` đôi khi không ngăn được component re-render?
* **expected_key_points:**
  - id: KP8_1
    content: So sánh nông (Shallow Compare)
    keypoint_weight: 0.5
    description: `React.memo` chỉ so sánh nông props. Nếu props chứa hàm hoặc đối tượng được tạo mới sau mỗi lần render của cha, tham chiếu sẽ khác.
  - id: KP8_2
    content: Cách khắc phục
    keypoint_weight: 0.5
    description: Sử dụng `useCallback` hoặc `useMemo` ở component cha để ổn định tham chiếu (reference) cho các props truyền xuống.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Cơ chế "Event Loop" trong trình duyệt xử lý microtask và macrotask khác nhau ra sao?
* **expected_key_points:**
  - id: KP9_1
    content: Microtask ưu tiên
    keypoint_weight: 0.5
    description: Microtasks (như Promise) được thực thi ngay lập tức sau khi tác vụ đồng bộ kết thúc, trước khi trình duyệt thực hiện việc vẽ lại (render).
  - id: KP9_2
    content: Macrotask
    keypoint_weight: 0.5
    description: Macrotasks (như `setTimeout`) được đẩy vào queue và đợi lượt thực thi sau khi các microtask queue trống.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích "Database Normalization" và lý do tại sao đôi khi chúng ta cần "Denormalization"?
* **expected_key_points:**
  - id: KP10_1
    content: Normalization (Chuẩn hóa)
    keypoint_weight: 0.5
    description: Chia nhỏ bảng để giảm dư thừa, đảm bảo toàn vẹn dữ liệu.
  - id: KP10_2
    content: Denormalization
    keypoint_weight: 0.5
    description: Gom dữ liệu lại để tăng tốc độ truy vấn (đọc) cho các hệ thống yêu cầu hiệu năng cao, chấp nhận dư thừa dữ liệu có kiểm soát.