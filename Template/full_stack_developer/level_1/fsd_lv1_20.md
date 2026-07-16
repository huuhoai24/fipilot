# Bộ Câu Hỏi Phỏng Vấn Full Stack Developer (Level 1) - Tập Đề Mới (42)

* **Role:** Full Stack Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong HTTP, sự khác biệt giữa trạng thái 401 Unauthorized và 403 Forbidden là gì?
* **expected_key_points:**
  - id: KP1_1
    content: 401 Unauthorized
    keypoint_weight: 0.5
    description: Xác thực thất bại (chưa đăng nhập hoặc token sai). Client cần cung cấp thông tin xác thực hợp lệ để truy cập.
  - id: KP1_2
    content: 403 Forbidden
    keypoint_weight: 0.5
    description: Đã xác thực nhưng không đủ quyền hạn (permission) để thực hiện hành động đó trên tài nguyên cụ thể.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong database SQL, `LEFT JOIN` và `INNER JOIN` khác nhau thế nào?
* **expected_key_points:**
  - id: KP2_1
    content: INNER JOIN
    keypoint_weight: 0.5
    description: Chỉ trả về các bản ghi có giá trị khớp ở cả hai bảng được join.
  - id: KP2_2
    content: LEFT JOIN
    keypoint_weight: 0.5
    description: Trả về tất cả bản ghi từ bảng bên trái, và các bản ghi khớp từ bảng bên phải. Nếu không khớp ở bảng phải, các cột của bảng đó sẽ là NULL.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** `var`, `let` và `const` trong JavaScript khác nhau về phạm vi (scope)?
* **expected_key_points:**
  - id: KP3_1
    content: Function scope vs Block scope
    keypoint_weight: 0.6
    description: `var` có phạm vi function-scope. `let` và `const` có phạm vi block-scope (giới hạn trong cặp ngoặc `{}`).
  - id: KP3_2
    content: Gán lại giá trị
    keypoint_weight: 0.4
    description: `var`/`let` cho phép gán lại. `const` chỉ được gán duy nhất một lần khi khởi tạo.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là mô hình Middleware trong Express.js (Node.js)?
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế hoạt động
    keypoint_weight: 0.5
    description: Là các hàm có quyền truy cập request, response và hàm `next()` để chuyển tiếp tới middleware tiếp theo trong chuỗi xử lý.
  - id: KP4_2
    content: Vai trò
    keypoint_weight: 0.5
    description: Dùng để thực hiện các tác vụ: authentication, logging, parsing body request, hoặc xử lý lỗi trước khi đến handler chính.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, sự khác biệt giữa `useState` và `useReducer`?
* **expected_key_points:**
  - id: KP5_1
    content: Độ phức tạp
    keypoint_weight: 0.5
    description: `useState` dùng cho state đơn giản. `useReducer` dùng cho state phức tạp, có nhiều logic cập nhật phụ thuộc vào các action khác nhau.
  - id: KP5_2
    content: Tổ chức logic
    keypoint_weight: 0.5
    description: `useReducer` tách logic cập nhật ra hàm reducer riêng, giúp code dễ đọc, dễ quản lý hơn khi state chuyển đổi theo các action cụ thể.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao Database Index có thể giúp tăng tốc truy vấn nhưng lại làm chậm thao tác `INSERT`?
* **expected_key_points:**
  - id: KP6_1
    content: Tăng tốc truy vấn
    keypoint_weight: 0.5
    description: Index tạo ra cấu trúc dữ liệu bổ sung giúp tìm kiếm nhanh mà không cần quét toàn bộ bảng (full table scan).
  - id: KP6_2
    content: Chậm khi chèn
    keypoint_weight: 0.5
    description: Khi chèn mới dữ liệu, DB phải thực hiện cập nhật lại toàn bộ cấu trúc index để đảm bảo tính thứ tự, tốn CPU và Disk I/O.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** `JWT` (JSON Web Token) khác gì với `Session-based authentication`?
* **expected_key_points:**
  - id: KP7_1
    content: Lưu trữ
    keypoint_weight: 0.5
    description: Session lưu trạng thái trên server. JWT là stateless, chứa thông tin xác thực ngay trong chuỗi token gửi lên client.
  - id: KP7_2
    content: Scaling
    keypoint_weight: 0.5
    description: JWT giúp scaling dễ hơn trong hệ thống phân tán vì server không cần lưu session id, chỉ cần xác thực token bằng secret key.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** "Hydration" trong SSR Framework làm chậm chỉ số TTI (Time to Interactive) ra sao?
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất quy trình
    keypoint_weight: 0.5
    description: Sau khi HTML tĩnh hiển thị, trình duyệt phải tải và thực thi lại JS bundle để đính kết các event listener vào cây DOM.
  - id: KP8_2
    content: Tác động Main Thread
    keypoint_weight: 0.5
    description: Việc thực thi JS khóa luồng chính (Main Thread), người dùng sẽ không thể tương tác (click, scroll) dù trang đã hiển thị xong.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" do Global Event Listeners gây ra trong các SPA.
* **expected_key_points:**
  - id: KP9_1
    content: Tham chiếu vòng
    keypoint_weight: 0.5
    description: Listener gắn vào `window`/`document` giữ tham chiếu đến component, ngăn cản trình thu dọn rác (GC) giải phóng bộ nhớ.
  - id: KP9_2
    content: Cách khắc phục
    keypoint_weight: 0.5
    description: Phải dùng `removeEventListener` trong lifecycle unmount hoặc cleanup function của `useEffect` để giải phóng tham chiếu.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao "Optimistic UI Updates" cần phải có cơ chế Rollback?
* **expected_key_points:**
  - id: KP10_1
    content: Khái niệm Optimistic
    keypoint_weight: 0.5
    description: UI cập nhật ngay dựa trên giả định request thành công để tăng trải nghiệm mượt mà.
  - id: KP10_2
    content: Sự cần thiết của Rollback
    keypoint_weight: 0.5
    description: Nếu request thực tế tới server thất bại, UI phải tự động hoàn tác (rollback) về trạng thái cũ để đảm bảo tính nhất quán dữ liệu cho người dùng.