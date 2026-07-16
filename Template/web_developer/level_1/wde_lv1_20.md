# Bộ Câu Hỏi Phỏng Vấn Web Developer (Level 1) - Tập Đề Mới (40)

* **Role:** Web Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, thuộc tính `box-sizing: border-box` có tác động như thế nào đến kích thước thực tế của một phần tử?
* **expected_key_points:**
  - id: KP1_1
    content: Cơ chế tính toán Box Model
    keypoint_weight: 0.7
    description: `border-box` bao gồm `padding` và `border` vào trong giá trị `width` và `height` đã định nghĩa, giúp phần tử không bị phình to ra ngoài kích thước thiết lập.
  - id: KP1_2
    content: Lợi ích trong thiết kế layout
    keypoint_weight: 0.3
    description: Giúp lập trình viên không phải thực hiện các phép cộng/trừ padding/border thủ công khi xác định kích thước cho các khối phần tử UI.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong JavaScript, `let`, `const` và `var` khác nhau như thế nào về mặt phạm vi (scope)?
* **expected_key_points:**
  - id: KP2_1
    content: Phạm vi hoạt động (Scope)
    keypoint_weight: 0.5
    description: `var` hoạt động theo function-scope (giới hạn trong hàm). `let` và `const` hoạt động theo block-scope (giới hạn trong cặp ngoặc nhọn `{}`).
  - id: KP2_2
    content: Khả năng gán lại giá trị
    keypoint_weight: 0.5
    description: `var` và `let` cho phép gán lại giá trị. `const` yêu cầu khởi tạo ngay và không cho phép thay đổi tham chiếu sau khi đã gán.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Thẻ `<a>` với thuộc tính `target="_blank"` có những rủi ro bảo mật nào?
* **expected_key_points:**
  - id: KP3_1
    content: Tấn công Tabnabbing
    keypoint_weight: 0.6
    description: Trang web mở ra ở tab mới có thể truy cập `window.opener` để chuyển hướng trang gốc sang nội dung độc hại.
  - id: KP3_2
    content: Giải pháp phòng ngừa
    keypoint_weight: 0.4
    description: Nên sử dụng thêm `rel="noopener noreferrer"` để ngăn chặn trang đích can thiệp vào ngữ cảnh của trang gốc.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích hiện tượng "Event Bubbling" trong DOM và Event Delegation.
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế lan truyền (Bubbling)
    keypoint_weight: 0.5
    description: Sự kiện kích hoạt ở phần tử con sẽ lan truyền lên các phần tử cha theo thứ tự DOM từ dưới lên.
  - id: KP4_2
    content: Lợi ích của Delegation
    keypoint_weight: 0.5
    description: Gán listener duy nhất tại cha giúp tối ưu bộ nhớ và dễ dàng xử lý sự kiện cho các phần tử con được thêm vào sau này.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, sự khác biệt giữa `useState` và `useRef`?
* **expected_key_points:**
  - id: KP5_1
    content: Tác động đến render
    keypoint_weight: 0.5
    description: Cập nhật `useState` trigger re-render component. Thay đổi giá trị `.current` của `useRef` KHÔNG gây re-render.
  - id: KP5_2
    content: Trường hợp sử dụng
    keypoint_weight: 0.5
    description: `useState` dùng cho dữ liệu cần hiển thị UI. `useRef` dùng cho lưu trữ giá trị cần giữ qua nhiều vòng render mà không cần hiển thị hoặc truy cập DOM trực tiếp.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `PUT` và `PATCH` khi thiết kế REST API?
* **expected_key_points:**
  - id: KP6_1
    content: PUT (Thay thế toàn bộ)
    keypoint_weight: 0.5
    description: Client gửi toàn bộ object mới để thay thế hoàn toàn tài nguyên hiện có trên server.
  - id: KP6_2
    content: PATCH (Cập nhật một phần)
    keypoint_weight: 0.5
    description: Chỉ gửi các trường dữ liệu cần chỉnh sửa, các thuộc tính cũ còn lại của tài nguyên được bảo toàn.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao nên dùng `Environment Variables` trong các dự án web?
* **expected_key_points:**
  - id: KP7_1
    content: Bảo mật
    keypoint_weight: 0.5
    description: Tránh hardcode các dữ liệu nhạy cảm (API Keys, DB Credentials) vào mã nguồn đẩy lên hệ thống quản lý mã nguồn.
  - id: KP7_2
    content: Cấu hình linh hoạt
    keypoint_weight: 0.5
    description: Giúp cấu hình ứng dụng dễ dàng cho từng môi trường (Dev, Staging, Production) mà không cần chỉnh sửa source code.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" do Global Event Listeners không được dọn dẹp.
* **expected_key_points:**
  - id: KP8_1
    content: Giữ tham chiếu component
    keypoint_weight: 0.5
    description: Gán listener vào `window`/`document` giữ tham chiếu đến component ngay cả khi nó bị hủy.
  - id: KP8_2
    content: Hệ quả Garbage Collection
    keypoint_weight: 0.5
    description: Trình thu dọn rác (GC) không thể giải phóng bộ nhớ, gây rò rỉ bộ nhớ nghiêm trọng và làm chậm/treo ứng dụng theo thời gian.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hydration trong SSR framework ảnh hưởng đến TTI (Time to Interactive) ra sao?
* **expected_key_points:**
  - id: KP9_1
    content: Bản chất công việc của Hydration
    keypoint_weight: 0.5
    description: Trình duyệt phải tải và thực thi lại JS bundle để gắn các event listener vào nội dung tĩnh nhận từ Server.
  - id: KP9_2
    content: Nút thắt hiệu năng (Bottleneck)
    keypoint_weight: 0.5
    description: Quá trình này tiêu tốn CPU và khóa Main Thread, khiến ứng dụng không phản hồi tương tác (click, scroll) dù nội dung đã hiển thị.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao "Optimistic UI Updates" cần cơ chế Rollback?
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa Optimistic
    keypoint_weight: 0.5
    description: Cập nhật UI ngay lập tức giả định request thành công để tăng trải nghiệm mượt mà (UX).
  - id: KP10_2
    content: Sự cần thiết của Rollback
    keypoint_weight: 0.5
    description: Khi request thực tế phía server lỗi, hệ thống phải tự động hoàn tác (rollback) trạng thái giao diện để đảm bảo dữ liệu hiển thị đúng với thực tế.