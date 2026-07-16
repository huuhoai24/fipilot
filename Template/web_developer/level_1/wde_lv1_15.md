# Bộ Câu Hỏi Phỏng Vấn Web Developer (Level 1) - Tập Đề Mới (29)

* **Role:** Web Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, tại sao việc sử dụng `rem` lại tốt hơn `px` cho kích thước font chữ?
* **expected_key_points:**
  - id: KP1_1
    content: Tính khả năng truy cập (Accessibility)
    keypoint_weight: 0.6
    description: `rem` dựa trên kích thước font gốc của trình duyệt. Người dùng có thể tùy chỉnh kích thước font trong cài đặt trình duyệt để dễ đọc hơn, còn `px` thì cố định.
  - id: KP1_2
    content: Tính nhất quán của layout
    keypoint_weight: 0.4
    description: `rem` giúp toàn bộ giao diện co giãn theo tỷ lệ khi font gốc thay đổi, tạo ra trải nghiệm nhất quán trên nhiều thiết bị.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong JavaScript, sự khác biệt giữa `Map` và `Object` khi dùng để lưu trữ dữ liệu cặp khóa-giá trị?
* **expected_key_points:**
  - id: KP2_1
    content: Loại dữ liệu của khóa (Key)
    keypoint_weight: 0.5
    description: `Object` chỉ hỗ trợ khóa là string hoặc Symbol. `Map` cho phép bất kỳ kiểu dữ liệu nào (kể cả object, hàm) làm khóa.
  - id: KP2_2
    content: Hiệu năng và tính năng
    keypoint_weight: 0.5
    description: `Map` có thuộc tính `size` tích hợp sẵn và đảm bảo thứ tự chèn, trong khi `Object` cần tính toán thủ công và không đảm bảo thứ tự.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Thẻ `<meta charset="UTF-8">` trong HTML có vai trò gì?
* **expected_key_points:**
  - id: KP3_1
    content: Bảng mã ký tự
    keypoint_weight: 0.5
    description: Chỉ định cho trình duyệt rằng tài liệu sử dụng bảng mã UTF-8 để hiển thị văn bản.
  - id: KP3_2
    content: Tránh lỗi hiển thị (mojibake)
    keypoint_weight: 0.5
    description: Đảm bảo các ký tự đặc biệt, tiếng Việt, biểu tượng emoji được hiển thị đúng, không bị lỗi font.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích hiện tượng "Event Bubbling" trong DOM.
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế lan truyền
    keypoint_weight: 0.5
    description: Khi sự kiện xảy ra trên một phần tử con, nó sẽ kích hoạt listener tại đó trước, sau đó lan tỏa ngược lên các phần tử cha theo thứ tự DOM (từ dưới lên).
  - id: KP4_2
    content: Lợi ích của Event Delegation
    keypoint_weight: 0.5
    description: Cho phép gán listener vào phần tử cha để quản lý sự kiện cho hàng loạt phần tử con, tối ưu hiệu năng và bộ nhớ.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, sự khác biệt giữa `useEffect` với dependency là `[]` và không có dependency là gì?
* **expected_key_points:**
  - id: KP5_1
    content: Dependency []
    keypoint_weight: 0.5
    description: Chỉ chạy đúng một lần duy nhất sau lần render đầu tiên (tương đương `componentDidMount`).
  - id: KP5_2
    content: Không có dependency
    keypoint_weight: 0.5
    description: Chạy sau MỖI lần render của component. Dễ gây ra lỗi vòng lặp render vô tận nếu có cập nhật state bên trong.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** `PUT` và `PATCH` khác nhau như thế nào trong REST API?
* **expected_key_points:**
  - id: KP6_1
    content: PUT (Thay thế toàn phần)
    keypoint_weight: 0.5
    description: Yêu cầu gửi lại toàn bộ tài nguyên để thay thế cho bản gốc.
  - id: KP6_2
    content: PATCH (Cập nhật một phần)
    keypoint_weight: 0.5
    description: Chỉ cần gửi những trường thông tin cần sửa đổi, giữ lại các thuộc tính cũ của tài nguyên.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao `CORS` gây ra lỗi và cách xử lý phổ biến?
* **expected_key_points:**
  - id: KP7_1
    content: Nguyên nhân
    keypoint_weight: 0.5
    description: Trình duyệt chặn request vì khác origin. Đây là lớp bảo mật mặc định để tránh trang web xấu gửi request trái phép tới API.
  - id: KP7_2
    content: Cách xử lý
    keypoint_weight: 0.5
    description: Server đích cần cấu hình header `Access-Control-Allow-Origin` để cấp phép cho domain client thực hiện truy vấn.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích Memory Leak do Closure trong Factory Function.
* **expected_key_points:**
  - id: KP8_1
    content: Tham chiếu scope
    keypoint_weight: 0.5
    description: Closure giữ lại scope của hàm cha. Các biến lớn trong hàm cha không được dọn dẹp (GC) chừng nào closure còn tồn tại.
  - id: KP8_2
    content: Cách phòng ngừa
    keypoint_weight: 0.5
    description: Gán các biến tham chiếu lớn thành `null` sau khi không sử dụng hoặc tránh lạm dụng tạo hàm con bao bọc các biến lớn không cần thiết.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao "Hydration" trong SSR (Server Side Rendering) lại tốn nhiều thời gian trên Main Thread?
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế của Hydration
    keypoint_weight: 0.5
    description: Trình duyệt phải thực thi lại toàn bộ code JS bundle để tạo lại cây component ảo (virtual DOM) và gắn kết các sự kiện vào DOM tĩnh.
  - id: KP9_2
    content: Nút thắt (Bottleneck)
    keypoint_weight: 0.5
    description: Quá trình này chặn Main Thread. Nếu trang có nhiều nội dung tương tác (JS lớn), trang web sẽ bị "đóng băng" không phản hồi dù nội dung đã hiển thị xong.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Sự khác biệt giữa "Race Condition" trong JS (Async) và "Race Condition" trong Database (Transaction)?
* **expected_key_points:**
  - id: KP10_1
    content: Race Condition JS
    keypoint_weight: 0.5
    description: Do các request API bất đồng bộ hoàn thành không đúng thứ tự, dẫn đến cập nhật sai state giao diện.
  - id: KP10_2
    content: Race Condition DB
    keypoint_weight: 0.5
    description: Do 2 giao dịch tranh chấp ghi cùng một dòng dữ liệu, gây mâu thuẫn dữ liệu hoặc mất cập nhật nếu không có cơ chế Locking hợp lý.