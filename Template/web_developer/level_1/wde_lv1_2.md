# Bộ Câu Hỏi Phỏng Vấn Web Developer (Level 1) - Tập Đề Mới (34)

* **Role:** Web Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, thuộc tính `z-index` có tác dụng gì và khi nào nó không hiệu quả?
* **expected_key_points:**
  - id: KP1_1
    content: Cơ chế xếp chồng
    keypoint_weight: 0.6
    description: `z-index` quyết định thứ tự chồng (chồng lên hoặc nằm dưới) của các phần tử theo trục Z. Giá trị cao hơn nằm đè lên giá trị thấp hơn.
  - id: KP1_2
    content: Điều kiện hoạt động
    keypoint_weight: 0.4
    description: Chỉ hoạt động khi phần tử có `position` khác `static` (ví dụ: `relative`, `absolute`, `fixed`). Nếu là `static`, `z-index` không có tác dụng.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Sự khác biệt giữa `Map` và `Object` trong JavaScript về mặt khóa (key)?
* **expected_key_points:**
  - id: KP2_1
    content: Kiểu dữ liệu của khóa
    keypoint_weight: 0.5
    description: `Object` khóa bị giới hạn là string hoặc Symbol. `Map` cho phép khóa là bất kỳ kiểu dữ liệu nào (kể cả object, hàm, số).
  - id: KP2_2
    content: Thuộc tính tích hợp
    keypoint_weight: 0.5
    description: `Map` có thuộc tính `size` để lấy số lượng phần tử nhanh chóng. Với `Object`, bạn phải tự tính toán qua `Object.keys().length`.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Thẻ `<a>` với thuộc tính `target="_blank"` có những rủi ro bảo mật nào?
* **expected_key_points:**
  - id: KP3_1
    content: Chiếm quyền điều khiển (Tabnabbing)
    keypoint_weight: 0.6
    description: Trang web mới mở ra có thể truy cập vào `window.opener` của trang gốc để chuyển hướng trang gốc sang trang độc hại.
  - id: KP3_2
    content: Giải pháp
    keypoint_weight: 0.4
    description: Luôn đi kèm `rel="noopener noreferrer"` để vô hiệu hóa liên kết `window.opener`, đảm bảo an toàn cho trang gốc.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm "Closure" trong JavaScript.
* **expected_key_points:**
  - id: KP4_1
    content: Bản chất closure
    keypoint_weight: 0.5
    description: Là khả năng một hàm con ghi nhớ và truy cập vào các biến thuộc phạm vi (scope) của hàm cha ngay cả sau khi hàm cha đã kết thúc.
  - id: KP4_2
    content: Trường hợp sử dụng
    keypoint_weight: 0.5
    description: Dùng để tạo các biến riêng tư (private variables) không thể truy cập trực tiếp từ bên ngoài.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, sự khác biệt giữa `useState` và `useRef`?
* **expected_key_points:**
  - id: KP5_1
    content: Render logic
    keypoint_weight: 0.5
    description: Thay đổi `useState` kích hoạt re-render. Thay đổi `useRef.current` KHÔNG kích hoạt re-render.
  - id: KP5_2
    content: Case sử dụng
    keypoint_weight: 0.5
    description: `useState` dùng cho UI cần hiển thị. `useRef` dùng cho lưu trữ giá trị cần giữ qua nhiều render mà không ảnh hưởng UI, hoặc thao tác DOM trực tiếp.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `INNER JOIN` và `LEFT JOIN` trong SQL?
* **expected_key_points:**
  - id: KP6_1
    content: INNER JOIN
    keypoint_weight: 0.5
    description: Chỉ lấy những bản ghi có giá trị khớp ở cả 2 bảng.
  - id: KP6_2
    content: LEFT JOIN
    keypoint_weight: 0.5
    description: Lấy toàn bộ bảng trái, và dữ liệu khớp từ bảng phải (nếu không khớp thì trả về NULL).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao nên dùng `Environment Variables` trong dự án web?
* **expected_key_points:**
  - id: KP7_1
    content: Bảo mật thông tin
    keypoint_weight: 0.5
    description: Tránh việc hardcode các API Key, DB Credentials trực tiếp vào source code đẩy lên Git.
  - id: KP7_2
    content: Cấu hình linh hoạt
    keypoint_weight: 0.5
    description: Giúp dễ dàng chuyển đổi cấu hình giữa các môi trường (Dev, Staging, Production) mà không cần can thiệp code.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" khi không gỡ bỏ Global Event Listeners.
* **expected_key_points:**
  - id: KP8_1
    content: Giữ tham chiếu
    keypoint_weight: 0.5
    description: Listener gắn vào `window`/`document` liên kết hàm callback với component. Nếu không remove, component sẽ mãi bị tham chiếu dù đã bị hủy.
  - id: KP8_2
    content: Hậu quả GC
    keypoint_weight: 0.5
    description: Trình dọn rác (GC) không thể giải phóng bộ nhớ, gây ra lỗi rò rỉ bộ nhớ nghiêm trọng trong các ứng dụng SPA phức tạp.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** "Hydration" trong các Framework SSR ảnh hưởng đến TTI (Time to Interactive) ra sao?
* **expected_key_points:**
  - id: KP9_1
    content: Bản chất Hydration
    keypoint_weight: 0.5
    description: Trình duyệt phải tải và thực thi lại JS bundle để gắn các event handler vào nội dung HTML tĩnh từ Server.
  - id: KP9_2
    content: Hiệu năng thực tế
    keypoint_weight: 0.5
    description: Quá trình này chiếm dụng Main Thread. Nếu bundle JS quá nặng, người dùng sẽ không thể tương tác (click, scroll) dù trang đã hiển thị.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao "Optimistic UI Updates" lại cần xử lý Rollback?
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa Optimistic
    keypoint_weight: 0.5
    description: Cập nhật UI ngay lập tức trước khi nhận phản hồi từ server để tăng độ mượt mà.
  - id: KP10_2
    content: Rollback
    keypoint_weight: 0.5
    description: Khi request thực tế lỗi, giao diện phải hoàn tác về trạng thái cũ để đảm bảo tính nhất quán của dữ liệu.