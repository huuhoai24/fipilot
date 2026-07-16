# Bộ Câu Hỏi Phỏng Vấn Full Stack Developer (Level 1) - Tập Đề Mới (41)

* **Role:** Full Stack Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong HTTP, sự khác biệt giữa phương thức `GET` và `POST` là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Mục đích sử dụng
    keypoint_weight: 0.6
    description: `GET` dùng để truy xuất dữ liệu từ server, không làm thay đổi trạng thái. `POST` dùng để gửi dữ liệu lên server để tạo mới hoặc xử lý, gây thay đổi trạng thái.
  - id: KP1_2
    content: Cách truyền dữ liệu
    keypoint_weight: 0.4
    description: `GET` truyền dữ liệu qua URL (query params), giới hạn độ dài. `POST` truyền dữ liệu qua Body, không giới hạn độ dài và bảo mật hơn cho dữ liệu nhạy cảm.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong database SQL, `Primary Key` và `Unique Key` khác nhau thế nào?
* **expected_key_points:**
  - id: KP2_1
    content: Tính chất NULL
    keypoint_weight: 0.5
    description: `Primary Key` không được phép chứa giá trị NULL. `Unique Key` cho phép một hoặc nhiều giá trị NULL (tùy theo hệ quản trị DB).
  - id: KP2_2
    content: Số lượng
    keypoint_weight: 0.5
    description: Mỗi bảng chỉ có duy nhất một `Primary Key`. Một bảng có thể có nhiều `Unique Key`.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Sự khác biệt giữa `sessionStorage` và `localStorage` trong trình duyệt?
* **expected_key_points:**
  - id: KP3_1
    content: Vòng đời dữ liệu
    keypoint_weight: 0.6
    description: `localStorage` tồn tại vĩnh viễn cho đến khi xóa thủ công. `sessionStorage` chỉ tồn tại trong phiên làm việc của tab đó, đóng tab là mất.
  - id: KP3_2
    content: Phạm vi chia sẻ
    keypoint_weight: 0.4
    description: `localStorage` chia sẻ được giữa các tab cùng origin. `sessionStorage` không chia sẻ giữa các tab ngay cả khi cùng origin.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích mô hình bất đồng bộ (Asynchronous) trong Node.js (Event Loop).
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế không chặn (Non-blocking I/O)
    keypoint_weight: 0.5
    description: Node.js xử lý I/O bất đồng bộ, cho phép luồng chính tiếp tục công việc khác mà không đợi I/O hoàn thành.
  - id: KP4_2
    content: Event Loop
    keypoint_weight: 0.5
    description: Khi tác vụ async hoàn tất, callback được đưa vào Callback Queue. Event Loop kiểm tra Stack rỗng để đẩy callback vào Stack thực thi.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, sự khác biệt giữa `useEffect` và `useLayoutEffect`?
* **expected_key_points:**
  - id: KP5_1
    content: Thời điểm thực thi
    keypoint_weight: 0.5
    description: `useEffect` chạy sau khi trình duyệt đã render màn hình. `useLayoutEffect` chạy đồng bộ ngay sau khi cập nhật DOM nhưng trước khi trình duyệt paint.
  - id: KP5_2
    content: Ứng dụng
    keypoint_weight: 0.5
    description: `useLayoutEffect` dùng cho các thao tác đo đạc hoặc chỉnh sửa DOM ngay lập tức để tránh hiện tượng nháy màn hình (flickering).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm "Dependency Injection" trong phát triển backend (ví dụ NestJS hoặc Spring).
* **expected_key_points:**
  - id: KP6_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Thay vì một class tự khởi tạo các thành phần phụ thuộc (dependencies), chúng được "tiêm" vào qua constructor hoặc setter từ bên ngoài.
  - id: KP6_2
    content: Lợi ích
    keypoint_weight: 0.5
    description: Giúp code dễ unit test, giảm sự phụ thuộc giữa các class (loose coupling), giúp mã nguồn sạch và dễ bảo trì hơn.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là Database Index và tại sao nó giúp tăng tốc truy vấn?
* **expected_key_points:**
  - id: KP7_1
    content: Cấu trúc Index
    keypoint_weight: 0.5
    description: Là cấu trúc dữ liệu bổ sung (như B-Tree) lưu trữ giá trị cột kèm con trỏ tới hàng dữ liệu gốc.
  - id: KP7_2
    content: Lợi ích
    keypoint_weight: 0.5
    description: Giúp tìm kiếm dữ liệu mà không cần quét toàn bộ bảng (Full Table Scan), từ đó giảm đáng kể thời gian truy vấn.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" do không dọn dẹp các Global Event Listeners trong SPA.
* **expected_key_points:**
  - id: KP8_1
    content: Giữ tham chiếu
    keypoint_weight: 0.5
    description: Listener gán vào `window` giữ tham chiếu đến scope của component, ngăn cản Garbage Collector thu hồi vùng nhớ sau khi component hủy.
  - id: KP8_2
    content: Giải pháp
    keypoint_weight: 0.5
    description: Cần sử dụng `removeEventListener` trong `useEffect` cleanup function hoặc lifecycle unmount để giải phóng hoàn toàn tham chiếu.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Sự khác biệt giữa `Microtask Queue` và `Macrotask Queue` trong Event Loop.
* **expected_key_points:**
  - id: KP9_1
    content: Độ ưu tiên
    keypoint_weight: 0.5
    description: Microtasks (như Promise) luôn được thực thi ngay sau khi tác vụ đồng bộ kết thúc, trước khi trình duyệt thực hiện các tác vụ vẽ lại (render).
  - id: KP9_2
    content: Đặc điểm Macrotask
    keypoint_weight: 0.5
    description: Macrotasks (như `setTimeout`, `setInterval`) đợi sau khi toàn bộ Microtask Queue trống mới được thực hiện trong lượt tiếp theo của Event Loop.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao "Optimistic UI" đòi hỏi logic Rollback ở phía Frontend?
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa Optimistic UI
    keypoint_weight: 0.5
    description: Cập nhật giao diện ngay lập tức dựa trên giả định request thành công để tăng trải nghiệm mượt mà.
  - id: KP10_2
    content: Sự cần thiết của Rollback
    keypoint_weight: 0.5
    description: Nếu request tới server thực tế thất bại, frontend phải hoàn tác giao diện về trạng thái gốc để đảm bảo tính nhất quán dữ liệu cho người dùng.