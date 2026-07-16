# Bộ Câu Hỏi Phỏng Vấn Web Developer (Level 1) - Tập Đề Mới (33)

* **Role:** Web Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, thuộc tính `box-sizing` hoạt động như thế nào và tại sao `border-box` được ưu tiên?
* **expected_key_points:**
  - id: KP1_1
    content: Cơ chế tính toán box model
    keypoint_weight: 0.6
    description: Với `border-box`, giá trị `padding` và `border` được tính nằm trọn trong chiều rộng/chiều cao đã khai báo, giúp phần tử không bị phình to ra ngoài kích thước mong muốn.
  - id: KP1_2
    content: Tính thuận tiện trong layout
    keypoint_weight: 0.4
    description: Giúp lập trình viên kiểm soát kích thước các khối phần tử chính xác hơn mà không cần thực hiện các phép trừ thủ công phức tạp.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong JavaScript, sự khác biệt giữa `==` và `===`?
* **expected_key_points:**
  - id: KP2_1
    content: Cơ chế so sánh
    keypoint_weight: 0.5
    description: `==` (loose equality) sẽ thực hiện ép kiểu dữ liệu (coercion) trước khi so sánh. `===` (strict equality) so sánh cả giá trị lẫn kiểu dữ liệu mà không ép kiểu.
  - id: KP2_2
    content: Độ tin cậy
    keypoint_weight: 0.5
    description: `===` được khuyến khích sử dụng để tránh các kết quả không mong muốn do cơ chế ép kiểu tự động của JavaScript.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Thẻ `<script async>` và `<script defer>` khác nhau như thế nào?
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế của async
    keypoint_weight: 0.5
    description: Nạp script bất đồng bộ, chạy ngay khi tải xong, không đảm bảo thứ tự thực thi với các script khác.
  - id: KP3_2
    content: Cơ chế của defer
    keypoint_weight: 0.5
    description: Nạp script bất đồng bộ, nhưng chỉ thực thi sau khi HTML đã được phân tích xong, đảm bảo đúng thứ tự xuất hiện trên trang.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích hiện tượng "Event Bubbling" trong DOM.
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế lan truyền
    keypoint_weight: 0.5
    description: Khi sự kiện xảy ra ở phần tử con, nó sẽ kích hoạt listener tại đó và lan tỏa ngược lên các phần tử cha theo cấu trúc cây DOM.
  - id: KP4_2
    content: Ứng dụng Event Delegation
    keypoint_weight: 0.5
    description: Tận dụng Bubbling để gán event listener tại thẻ cha, giúp tối ưu hiệu năng và xử lý linh hoạt cho các phần tử con thêm mới mà không cần gán lại.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, sự khác biệt giữa `useState` và `useReducer`?
* **expected_key_points:**
  - id: KP5_1
    content: Độ phức tạp của State
    keypoint_weight: 0.5
    description: `useState` dùng cho state đơn giản. `useReducer` phù hợp cho state phức tạp có logic chuyển đổi liên quan đến nhiều giá trị.
  - id: KP5_2
    content: Quản lý logic
    keypoint_weight: 0.5
    description: `useReducer` tách biệt logic cập nhật ra hàm reducer riêng, giúp code dễ duy trì và kiểm thử hơn.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao `Cookie` với cờ `HttpOnly` lại quan trọng cho bảo mật?
* **expected_key_points:**
  - id: KP6_1
    content: Ngăn chặn XSS
    keypoint_weight: 0.5
    description: `HttpOnly` ngăn chặn các đoạn mã JavaScript phía client truy cập vào cookie (bằng `document.cookie`), hạn chế rủi ro lấy cắp Session ID.
  - id: KP6_2
    content: Duy trì xác thực
    keypoint_weight: 0.5
    description: Dù JS không đọc được, Cookie vẫn được trình duyệt tự động gửi kèm các HTTP request lên server, đảm bảo tính năng xác thực không bị ảnh hưởng.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `PUT` và `PATCH` khi cập nhật dữ liệu API?
* **expected_key_points:**
  - id: KP7_1
    content: PUT (Thay thế)
    keypoint_weight: 0.5
    description: Client gửi toàn bộ object mới để ghi đè (replace) lên dữ liệu cũ hiện có trên server.
  - id: KP7_2
    content: PATCH (Cập nhật một phần)
    keypoint_weight: 0.5
    description: Chỉ gửi các trường thông tin muốn chỉnh sửa, giữ nguyên các thuộc tính không được nhắc tới.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" do không dọn dẹp các Global Event Listeners.
* **expected_key_points:**
  - id: KP8_1
    content: Giữ tham chiếu component
    keypoint_weight: 0.5
    description: Listener gắn vào `window`/`document` giữ tham chiếu đến hàm callback và scope của component, khiến chúng không thể bị hủy.
  - id: KP8_2
    content: Hệ quả Garbage Collection
    keypoint_weight: 0.5
    description: Trình dọn rác (GC) không thể thu hồi bộ nhớ, tích lũy dần theo thời gian làm treo ứng dụng SPA.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hydration trong SSR framework ảnh hưởng đến Time to Interactive (TTI) ra sao?
* **expected_key_points:**
  - id: KP9_1
    content: Quy trình Hydration
    keypoint_weight: 0.5
    description: Sau khi render HTML từ server, trình duyệt phải tải và thực thi lại bundle JS để gắn kết (bind) sự kiện vào DOM tĩnh.
  - id: KP9_2
    content: Nút thắt (Bottleneck)
    keypoint_weight: 0.5
    description: Việc thực thi JS này tiêu tốn CPU và khóa Main Thread, khiến trang web đứng im (not responsive) dù đã hiện nội dung.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** "Optimistic UI Updates" là gì và tại sao cần xử lý rollback?
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa Optimistic
    keypoint_weight: 0.5
    description: Giao diện cập nhật ngay lập tức dựa trên giả định request tới server sẽ thành công để tăng trải nghiệm mượt mà.
  - id: KP10_2
    content: Sự cần thiết của Rollback
    keypoint_weight: 0.5
    description: Khi request thực tế phía server thất bại, hệ thống phải tự động hoàn tác (rollback) trạng thái giao diện để đảm bảo dữ liệu hiển thị không bị sai lệch.