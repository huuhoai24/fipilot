# Bộ Câu Hỏi Phỏng Vấn Web Developer (Level 1) - Tập Đề Mới (39)

* **Role:** Web Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, sự khác biệt giữa `position: absolute` và `position: fixed` là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Hệ quy chiếu định vị
    keypoint_weight: 0.6
    description: `absolute` định vị dựa trên phần tử tổ tiên gần nhất có `position` khác `static`. `fixed` định vị trực tiếp dựa trên khung nhìn (viewport) của trình duyệt.
  - id: KP1_2
    content: Hành vi khi cuộn trang
    keypoint_weight: 0.4
    description: Phần tử `absolute` sẽ cuộn theo nội dung trang web. Phần tử `fixed` sẽ đứng yên tại vị trí cố định trên màn hình bất chấp người dùng cuộn trang.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** JavaScript `Array.prototype.slice()` khác gì với `Array.prototype.splice()`?
* **expected_key_points:**
  - id: KP2_1
    content: Tính biến đổi (Mutability)
    keypoint_weight: 0.5
    description: `slice()` không làm thay đổi mảng gốc và trả về một bản sao. `splice()` thay đổi trực tiếp mảng gốc.
  - id: KP2_2
    content: Mục đích
    keypoint_weight: 0.5
    description: `slice()` dùng để trích xuất một phần mảng. `splice()` dùng để chèn, xóa hoặc thay thế các phần tử bên trong mảng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao nên dùng các thẻ ngữ nghĩa (Semantic tags) trong HTML5?
* **expected_key_points:**
  - id: KP3_1
    content: Accessibility (Trợ năng)
    keypoint_weight: 0.6
    description: Các thẻ như `<header>`, `<footer>`, `<nav>` giúp công cụ đọc màn hình nhận diện cấu trúc trang web chính xác cho người dùng khiếm thị.
  - id: KP3_2
    content: SEO
    keypoint_weight: 0.4
    description: Hỗ trợ các bộ máy tìm kiếm (Google) hiểu rõ nội dung chính và phân cấp thông tin, giúp cải thiện xếp hạng tìm kiếm.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích "Event Bubbling" trong DOM và Event Delegation.
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế lan truyền
    keypoint_weight: 0.5
    description: Khi một sự kiện kích hoạt trên phần tử con, nó sẽ "nổi" lên qua các phần tử cha theo thứ tự DOM.
  - id: KP4_2
    content: Event Delegation
    keypoint_weight: 0.5
    description: Gán listener tại cha để xử lý sự kiện cho hàng loạt con, giúp tối ưu hiệu năng và xử lý tốt cho các phần tử được thêm mới sau này.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, khi nào nên sử dụng `useMemo` và khi nào nên tránh?
* **expected_key_points:**
  - id: KP5_1
    content: Mục đích
    keypoint_weight: 0.5
    description: Dùng để ghi nhớ (memoize) kết quả tính toán tốn kém tài nguyên (CPU intensive) giữa các lần render.
  - id: KP5_2
    content: Khi nào tránh
    keypoint_weight: 0.5
    description: Tránh lạm dụng cho các phép tính đơn giản vì việc lưu trữ cache cũng tốn bộ nhớ và chi phí xử lý dependency check không cần thiết.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `PUT` và `PATCH` khi thiết kế REST API?
* **expected_key_points:**
  - id: KP6_1
    content: PUT (Replace)
    keypoint_weight: 0.5
    description: Gửi toàn bộ dữ liệu mới để thay thế hoàn toàn tài nguyên cũ.
  - id: KP6_2
    content: PATCH (Update partial)
    keypoint_weight: 0.5
    description: Chỉ gửi một phần dữ liệu cần thay đổi, giữ lại các phần cũ không đề cập.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Ý nghĩa của `Content-Security-Policy` (CSP) header?
* **expected_key_points:**
  - id: KP7_1
    content: Chống XSS
    keypoint_weight: 0.5
    description: CSP giúp kiểm soát các nguồn (domain) được phép load script, style, ảnh, ngăn chặn việc chạy mã độc từ nguồn lạ.
  - id: KP7_2
    content: Cơ chế thực thi
    keypoint_weight: 0.5
    description: Trình duyệt dựa vào chính sách khai báo trong header để từ chối các hành động tải tài nguyên không được cấp phép.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" do Global Event Listeners không được dọn dẹp.
* **expected_key_points:**
  - id: KP8_1
    content: Tham chiếu component
    keypoint_weight: 0.5
    description: Listener gán vào `window`/`document` giữ tham chiếu đến component và các biến bên trong nó, ngăn cản Garbage Collector dọn dẹp.
  - id: KP8_2
    content: Hệ quả
    keypoint_weight: 0.5
    description: Tích lũy bộ nhớ bị chiếm dụng (memory leak) gây treo ứng dụng theo thời gian dài trong các ứng dụng SPA (Single Page Application).

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** "Hydration" trong SSR Framework và tác động đến hiệu năng TTI.
* **expected_key_points:**
  - id: KP9_1
    content: Quy trình Hydration
    keypoint_weight: 0.5
    description: Trình duyệt phải thực thi toàn bộ JS bundle để đính kèm event listeners vào nội dung tĩnh từ server.
  - id: KP9_2
    content: Nút thắt (Bottleneck)
    keypoint_weight: 0.5
    description: Việc chạy JS khóa Main Thread, khiến người dùng không thể tương tác (click, scroll) dù nội dung đã hiển thị rõ ràng trên màn hình.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao "Optimistic UI Updates" đòi hỏi cơ chế Rollback?
* **expected_key_points:**
  - id: KP10_1
    content: Bản chất Optimistic
    keypoint_weight: 0.5
    description: UI cập nhật ngay dựa trên giả định request thành công để tăng độ mượt mà (UX).
  - id: KP10_2
    content: Sự cần thiết của Rollback
    keypoint_weight: 0.5
    description: Khi request thực tế phía server thất bại, hệ thống phải hoàn tác (rollback) trạng thái UI về đúng với dữ liệu từ server để tránh sai lệch thông tin.