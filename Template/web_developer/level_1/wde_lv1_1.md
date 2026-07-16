# Bộ Câu Hỏi Phỏng Vấn Web Developer (Level 1) - Tập Đề Mới (35)

* **Role:** Web Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, thuộc tính `display: none` khác với `visibility: hidden` như thế nào?
* **expected_key_points:**
  - id: KP1_1
    content: Chiếm chỗ trong luồng layout
    keypoint_weight: 0.6
    description: `display: none` loại bỏ hoàn toàn phần tử khỏi luồng layout, khiến các phần tử xung quanh lấp đầy chỗ đó. `visibility: hidden` giữ nguyên không gian chiếm dụng của phần tử (chỉ làm nó vô hình).
  - id: KP1_2
    content: Tương tác DOM
    keypoint_weight: 0.4
    description: Cả hai đều không cho phép tương tác chuột. Tuy nhiên, `display: none` khiến phần tử biến mất khỏi cây render, còn `visibility: hidden` thì không.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Sự khác biệt giữa `==` và `===` trong JavaScript?
* **expected_key_points:**
  - id: KP2_1
    content: Ép kiểu dữ liệu (Type coercion)
    keypoint_weight: 0.5
    description: `==` thực hiện ép kiểu trước khi so sánh nếu hai vế khác kiểu dữ liệu. `===` so sánh nghiêm ngặt cả giá trị lẫn kiểu dữ liệu (không ép kiểu).
  - id: KP2_2
    content: Độ an toàn
    keypoint_weight: 0.5
    description: `===` luôn được khuyến khích vì tránh các lỗi logic tiềm ẩn do cơ chế ép kiểu tự động của JavaScript gây ra.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao nên sử dụng `<meta name="viewport">` cho web mobile?
* **expected_key_points:**
  - id: KP3_1
    content: Kiểm soát độ rộng viewport
    keypoint_weight: 0.5
    description: Thiết lập `width=device-width` để website tự động co giãn theo chiều rộng màn hình thiết bị, tránh render theo độ rộng desktop mặc định.
  - id: KP3_2
    content: Trải nghiệm người dùng
    keypoint_weight: 0.5
    description: Giúp nội dung hiển thị ở kích thước hợp lý, không bị quá nhỏ và không cần người dùng phải zoom bằng tay.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm "Event Bubbling" trong DOM.
* **expected_key_points:**
  - id: KP4_1
    content: Lan truyền sự kiện
    keypoint_weight: 0.5
    description: Sự kiện kích hoạt ở phần tử con sẽ lan tỏa lên trên các phần tử cha lần lượt cho đến hết cấu trúc cây DOM.
  - id: KP4_2
    content: Event Delegation
    keypoint_weight: 0.5
    description: Kỹ thuật gán listener vào phần tử cha để quản lý sự kiện cho hàng loạt phần tử con, tối ưu bộ nhớ và xử lý linh hoạt cho các phần tử được thêm sau này.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, sự khác biệt giữa `useState` và `useRef`?
* **expected_key_points:**
  - id: KP5_1
    content: Render logic
    keypoint_weight: 0.5
    description: Cập nhật `useState` gây re-render component. Thay đổi giá trị `.current` của `useRef` không gây re-render.
  - id: KP5_2
    content: Trường hợp sử dụng
    keypoint_weight: 0.5
    description: `useState` quản lý dữ liệu cần hiển thị lên UI. `useRef` lưu giữ giá trị bền vững không cần hiển thị hoặc thao tác trực tiếp với node DOM.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** `PUT` và `PATCH` khác nhau như thế nào trong thiết kế API?
* **expected_key_points:**
  - id: KP6_1
    content: PUT (Thay thế toàn phần)
    keypoint_weight: 0.5
    description: Client gửi toàn bộ object để ghi đè (replace) lên tài nguyên cũ trên server.
  - id: KP6_2
    content: PATCH (Cập nhật một phần)
    keypoint_weight: 0.5
    description: Chỉ gửi các trường thông tin cần sửa đổi, phần còn lại của tài nguyên được giữ nguyên.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao nên dùng `Environment Variables` trong dự án web?
* **expected_key_points:**
  - id: KP7_1
    content: Bảo mật
    keypoint_weight: 0.5
    description: Tránh việc để lộ các thông tin nhạy cảm như API Keys, DB Credentials trực tiếp trong mã nguồn đẩy lên git.
  - id: KP7_2
    content: Quản lý cấu hình
    keypoint_weight: 0.5
    description: Cho phép thay đổi cấu hình linh hoạt cho từng môi trường (Development, Staging, Production) mà không cần can thiệp code.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" khi không gỡ bỏ Global Event Listeners.
* **expected_key_points:**
  - id: KP8_1
    content: Giữ tham chiếu
    keypoint_weight: 0.5
    description: Gán listener vào `window`/`document` giữ tham chiếu đến component, ngăn cản trình thu dọn rác (GC) giải phóng vùng nhớ.
  - id: KP8_2
    content: Hệ quả
    keypoint_weight: 0.5
    description: Bộ nhớ bị chiếm dụng liên tục, dẫn đến tình trạng rò rỉ bộ nhớ, gây chậm hoặc treo ứng dụng theo thời gian.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** "Hydration" trong các framework SSR gây nút thắt hiệu năng (TTI) ra sao?
* **expected_key_points:**
  - id: KP9_1
    content: Quy trình Hydration
    keypoint_weight: 0.5
    description: Sau khi render HTML từ server, trình duyệt phải tải và thực thi lại toàn bộ JS bundle để đính kèm sự kiện vào DOM tĩnh.
  - id: KP9_2
    content: Nút thắt (Bottleneck)
    keypoint_weight: 0.5
    description: Quá trình này tiêu tốn nhiều CPU và khóa Main Thread, khiến ứng dụng không phản hồi tương tác (click, scroll) dù nội dung đã hiển thị.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao "Optimistic UI Updates" cần cơ chế Rollback?
* **expected_key_points:**
  - id: KP10_1
    content: Khái niệm Optimistic
    keypoint_weight: 0.5
    description: Cập nhật UI ngay lập tức dựa trên giả định request tới server thành công để tăng trải nghiệm người dùng (mượt mà).
  - id: KP10_2
    content: Xử lý Rollback
    keypoint_weight: 0.5
    description: Nếu request thực tế từ server trả về lỗi, giao diện cần phải tự động hoàn tác về trạng thái cũ để đảm bảo tính nhất quán của dữ liệu.