# Bộ Câu Hỏi Phỏng Vấn Full Stack Developer (Level 1) - Tập Đề Mới (6)

* **Role:** Full Stack Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong HTTP, sự khác biệt giữa các mã phản hồi (Status Codes) 200, 201, 400, 401 và 403 là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Mã thành công (2xx)
    keypoint_weight: 0.5
    description: 200 (OK) là phản hồi thành công chung. 201 (Created) dành riêng khi yêu cầu tạo tài nguyên mới thành công.
  - id: KP1_2
    content: Mã lỗi Client (4xx)
    keypoint_weight: 0.5
    description: 400 (Bad Request) do client gửi dữ liệu sai; 401 (Unauthorized) do thiếu/sai thông tin xác thực; 403 (Forbidden) do đã xác thực nhưng không có quyền truy cập tài nguyên.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Bạn giải thích thế nào về khái niệm "Responsive Web Design"?
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa mục tiêu
    keypoint_weight: 0.5
    description: Là cách thiết kế trang web sao cho giao diện tự động điều chỉnh linh hoạt để hiển thị tốt trên mọi loại kích thước màn hình (mobile, tablet, desktop).
  - id: KP2_2
    content: Các kỹ thuật chính
    keypoint_weight: 0.5
    description: Sử dụng Media Queries trong CSS, layout linh hoạt (Flexbox/Grid), và hình ảnh/media có kích thước tỷ lệ (fluid images).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao chúng ta cần sử dụng `npm` hoặc `yarn` trong các dự án JavaScript?
* **expected_key_points:**
  - id: KP3_1
    content: Quản lý thư viện phụ thuộc (Dependencies)
    keypoint_weight: 0.5
    description: Giúp cài đặt, cập nhật và quản lý các thư viện bên thứ ba mà dự án cần một cách tự động và nhất quán.
  - id: KP3_2
    content: Quản lý phiên bản (Version control)
    keypoint_weight: 0.5
    description: Thông qua file `package.json`, đảm bảo mọi thành viên trong team hoặc môi trường triển khai đều sử dụng đúng phiên bản thư viện cần thiết.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong JavaScript, "Closure" là gì và bạn thường áp dụng nó trong trường hợp nào?
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa Closure
    keypoint_weight: 0.5
    description: Hàm có khả năng ghi nhớ scope bên ngoài (scope của hàm cha) ngay cả khi hàm cha đã thực thi xong.
  - id: KP4_2
    content: Ứng dụng thực tế
    keypoint_weight: 0.5
    description: Dùng để tạo ra các private variables (giữ trạng thái ẩn) hoặc tạo các hàm factory/currying.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao chúng ta nên tránh việc cập nhật `State` trực tiếp trong React (ví dụ: `this.state.value = 1` hoặc `state.push(item)`)?
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế Render của React
    keypoint_weight: 0.5
    description: React dựa vào sự thay đổi tham chiếu (reference) của state để quyết định xem liệu component có cần re-render hay không.
  - id: KP5_2
    content: Sự bất biến (Immutability)
    keypoint_weight: 0.5
    description: Thay đổi trực tiếp không tạo ra reference mới, khiến React không nhận ra state đã thay đổi, dẫn đến giao diện không cập nhật (stale UI).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cách Database Index giúp tăng tốc truy vấn. Tại sao không nên index tất cả các cột trong bảng?
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế tìm kiếm của Index
    keypoint_weight: 0.5
    description: Index tạo ra một cấu trúc dữ liệu cây (B-tree) cho phép tìm kiếm theo giá trị cực nhanh thay vì phải quét toàn bộ bảng (Full Table Scan).
  - id: KP6_2
    content: Chi phí của Index
    keypoint_weight: 0.5
    description: Index chiếm thêm dung lượng lưu trữ trên disk và gây chậm thao tác ghi (INSERT/UPDATE/DELETE) vì cần cập nhật cây index mỗi khi dữ liệu thay đổi.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong kiến trúc Backend, tại sao lại dùng "Layered Architecture" (chia thành Controller, Service, DAO/Repository layers)?
* **expected_key_points:**
  - id: KP7_1
    content: Tách biệt mối quan tâm (Separation of Concerns)
    keypoint_weight: 0.5
    description: Mỗi layer có nhiệm vụ riêng (Controller nhận request, Service chứa logic, DAO thao tác DB), giúp code gọn gàng, dễ hiểu.
  - id: KP7_2
    content: Dễ bảo trì và mở rộng
    keypoint_weight: 0.5
    description: Việc thay đổi cấu trúc DB không ảnh hưởng đến Business Logic trong Service layer, giúp hệ thống dễ nâng cấp hơn.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong trình duyệt, "Event Loop" xử lý các tác vụ như `setTimeout`, `Promises` (Microtask) và `UI Rendering` theo thứ tự nào?
* **expected_key_points:**
  - id: KP8_1
    content: Thứ tự thực thi
    keypoint_weight: 0.5
    description: Các code đồng bộ chạy trước, sau đó tới Microtasks (Promises), cuối cùng mới tới các Macrotasks (`setTimeout`).
  - id: KP8_2
    content: Ưu tiên của Microtasks
    keypoint_weight: 0.5
    description: Microtasks (Promises) luôn được xử lý ngay sau khi một tác vụ đồng bộ kết thúc, trước khi trình duyệt thực hiện việc vẽ lại giao diện (Render).

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao một ứng dụng backend cần "Rate Limiting" và "Throttling"? Sự khác biệt giữa chúng là gì?
* **expected_key_points:**
  - id: KP9_1
    content: Mục đích bảo vệ
    keypoint_weight: 0.5
    description: Chống lại tấn công DDoS, bảo vệ tài nguyên server khỏi bị quá tải bởi các user spam request quá nhiều.
  - id: KP9_2
    content: Phân biệt cơ chế
    keypoint_weight: 0.5
    description: Rate Limiting chặn request sau khi đã vượt quá ngưỡng cho phép. Throttling giới hạn lưu lượng để request được xử lý ổn định trong một khoảng thời gian dài.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Bạn giải thích thế nào về "Race Condition" trong lập trình cơ sở dữ liệu và cách phòng tránh?
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa Race Condition
    keypoint_weight: 0.5
    description: Xảy ra khi hai giao dịch (transactions) cùng đọc và ghi dữ liệu tại một thời điểm, dẫn đến kết quả cuối cùng bị sai lệch (ví dụ: mất dữ liệu).
  - id: KP10_2
    content: Cách phòng tránh
    keypoint_weight: 0.5
    description: Sử dụng các cơ chế khóa (Locking - Optimistic/Pessimistic locking) hoặc thiết kế Database Transaction đúng chuẩn ACID để đảm bảo tính cô lập (Isolation).