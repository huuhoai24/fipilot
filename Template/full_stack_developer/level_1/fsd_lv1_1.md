# Bộ Câu Hỏi Phỏng Vấn Full Stack Developer (Level 1) - Tập Đề Mới

* **Role:** Full Stack Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, thuộc tính `box-sizing: border-box` có tác dụng gì và tại sao nó lại được coi là lựa chọn mặc định tốt hơn so với `content-box`?
* **expected_key_points:**
  - id: KP1_1
    content: Cơ chế tính toán kích thước phần tử
    keypoint_weight: 0.6
    description: `border-box` bao gồm nội dung (content), padding và border trong tổng chiều rộng (width) và chiều cao (height) được chỉ định. `content-box` chỉ tính kích thước cho phần nội dung, khiến padding và border cộng thêm vào kích thước thực tế.
  - id: KP1_2
    content: Lợi ích trong layout
    keypoint_weight: 0.4
    description: `border-box` giúp việc căn chỉnh layout trở nên dễ dàng và đoán trước được hơn, tránh tình trạng phần tử bị tràn ra ngoài container khi thêm padding hoặc border.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong JavaScript, sự khác biệt giữa `null` và `undefined` là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa cơ bản
    keypoint_weight: 0.5
    description: `undefined` có nghĩa là biến đã được khai báo nhưng chưa được gán giá trị. `null` là một giá trị đặc biệt được gán chủ động để biểu thị trạng thái "không có giá trị" hoặc "đối tượng rỗng".
  - id: KP2_2
    content: Kiểu dữ liệu (Type)
    keypoint_weight: 0.5
    description: `typeof undefined` trả về `'undefined'`, trong khi `typeof null` trả về `'object'` (một lỗi lịch sử của JS).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Bạn hiểu thế nào về khái niệm CORS (Cross-Origin Resource Sharing) trong ứng dụng web?
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế bảo mật trình duyệt
    keypoint_weight: 0.6
    description: CORS là chính sách an ninh của trình duyệt nhằm ngăn chặn các trang web thực hiện request đến domain khác với domain của mình trừ khi domain đích cho phép.
  - id: KP3_2
    content: Cách thức cấp quyền
    keypoint_weight: 0.4
    description: Server cần cấu hình header `Access-Control-Allow-Origin` để chỉ định những domain nào được phép thực hiện request tới nó.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, sự khác biệt giữa `State` và `Props` là gì? Khi nào nên dùng loại nào?
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa và quyền sở hữu
    keypoint_weight: 0.5
    description: `Props` là dữ liệu truyền từ component cha xuống component con, component không được phép thay đổi props. `State` là dữ liệu nội tại của component, có thể được thay đổi bởi chính component đó.
  - id: KP4_2
    content: Trường hợp sử dụng
    keypoint_weight: 0.5
    description: Dùng `props` để cấu hình component hoặc truyền dữ liệu hiển thị. Dùng `state` để quản lý các dữ liệu thay đổi theo thời gian (như input form, toggle).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm "Dependency Injection" trong phát triển backend. Tại sao nó giúp code dễ test hơn?
* **expected_key_points:**
  - id: KP5_1
    content: Định nghĩa DI
    keypoint_weight: 0.5
    description: Là kỹ thuật truyền các dependency (như service, db connection) từ bên ngoài vào đối tượng thay vì để đối tượng tự khởi tạo chúng bên trong.
  - id: KP5_2
    content: Lợi ích trong testing
    keypoint_weight: 0.5
    description: Cho phép dễ dàng thay thế các dependency thật bằng các "mock" hoặc "stub" object khi thực hiện Unit Test.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong SQL, `INNER JOIN` khác gì với `LEFT JOIN`?
* **expected_key_points:**
  - id: KP6_1
    content: INNER JOIN
    keypoint_weight: 0.5
    description: Chỉ trả về các hàng có dữ liệu khớp (match) ở cả hai bảng được join.
  - id: KP6_2
    content: LEFT JOIN
    keypoint_weight: 0.5
    description: Trả về tất cả các hàng từ bảng bên trái, và các hàng khớp từ bảng bên phải; nếu không có dữ liệu khớp bên phải thì sẽ trả về giá trị NULL.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `Session` và `Local Storage` trong trình duyệt là gì?
* **expected_key_points:**
  - id: KP7_1
    content: Thời hạn tồn tại
    keypoint_weight: 0.5
    description: `Local Storage` lưu dữ liệu vĩnh viễn cho đến khi bị xóa thủ công. `Session Storage` chỉ lưu dữ liệu trong một phiên làm việc, dữ liệu mất khi đóng tab trình duyệt.
  - id: KP7_2
    content: Phạm vi truy cập
    keypoint_weight: 0.5
    description: Cả hai đều có giới hạn theo domain (origin), nhưng `Session Storage` còn bị giới hạn theo từng tab/cửa sổ.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích cơ chế "Event Loop" của Node.js xử lý các tác vụ I/O bất đồng bộ như thế nào?
* **expected_key_points:**
  - id: KP8_1
    content: Xử lý đơn luồng và non-blocking I/O
    keypoint_weight: 0.5
    description: Node.js chạy một luồng duy nhất, các tác vụ I/O được đẩy ra thư viện libuv xử lý ở background, giúp luồng chính không bị chờ đợi (blocking).
  - id: KP8_2
    content: Vòng lặp lấy callback từ queue
    keypoint_weight: 0.5
    description: Khi tác vụ I/O xong, callback được đưa vào Event Queue, Event Loop kiểm tra stack rỗng và đưa callback vào để thực thi.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao chúng ta cần sử dụng "Database Index" và khi nào thì Index có thể làm giảm hiệu năng?
* **expected_key_points:**
  - id: KP9_1
    content: Mục đích của Index
    keypoint_weight: 0.5
    description: Tăng tốc độ truy vấn (SELECT) bằng cách tạo cấu trúc dữ liệu phụ (B-tree) để tra cứu thay vì duyệt toàn bảng.
  - id: KP9_2
    content: Tác động tiêu cực tới Write operations
    keypoint_weight: 0.5
    description: Gây chậm khi thêm/sửa/xóa dữ liệu vì mỗi lần ghi, index phải cập nhật lại cấu trúc cây, tốn chi phí CPU và Disk I/O.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Bạn hiểu thế nào về khái niệm "Debounce" và "Throttle" trong JavaScript và khi nào cần áp dụng chúng?
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế Debounce
    keypoint_weight: 0.5
    description: Chỉ thực thi hàm sau khi một khoảng thời gian trôi qua kể từ lần gọi cuối (Ví dụ: search box khi người dùng ngừng gõ).
  - id: KP10_2
    content: Cơ chế Throttle
    keypoint_weight: 0.5
    description: Giới hạn số lần thực thi hàm trong một khoảng thời gian nhất định (Ví dụ: sự kiện scroll hoặc resize cửa sổ).