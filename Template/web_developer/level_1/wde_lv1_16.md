# Bộ Câu Hỏi Phỏng Vấn Web Developer (Level 1) - Tập Đề Mới (30)

* **Role:** Web Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, sự khác biệt giữa `position: relative` và `position: absolute` là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Luồng tài liệu (Document Flow)
    keypoint_weight: 0.6
    description: `relative` giữ phần tử trong luồng tài liệu bình thường. `absolute` lấy phần tử ra khỏi luồng, cho phép nó đè lên các phần tử khác.
  - id: KP1_2
    content: Hệ quy chiếu định vị
    keypoint_weight: 0.4
    description: `relative` định vị so với vị trí gốc của chính nó. `absolute` định vị so với tổ tiên gần nhất có thuộc tính `position` không phải là `static`.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong JavaScript, `const` có thực sự làm biến trở thành bất biến (immutable)?
* **expected_key_points:**
  - id: KP2_1
    content: Khả năng gán lại (Reassignment)
    keypoint_weight: 0.5
    description: `const` chỉ chặn việc gán lại tham chiếu mới cho biến đó, nhưng không ngăn cản việc thay đổi dữ liệu bên trong object/array.
  - id: KP2_2
    content: Tính khả biến (Mutability)
    keypoint_weight: 0.5
    description: Một object được khai báo bằng `const` vẫn có thể bị thay đổi các thuộc tính bên trong nó một cách bình thường.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Thẻ `<meta name="description">` đóng vai trò gì trong SEO?
* **expected_key_points:**
  - id: KP3_1
    content: Mô tả tóm tắt
    keypoint_weight: 0.5
    description: Cung cấp nội dung tóm tắt ngắn gọn về trang web cho các bộ máy tìm kiếm (Google).
  - id: KP3_2
    content: Tăng tỷ lệ click (CTR)
    keypoint_weight: 0.5
    description: Thường hiển thị dưới tiêu đề trang trong kết quả tìm kiếm, ảnh hưởng trực tiếp đến quyết định click của người dùng.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích hiện tượng "Event Bubbling" và cách ngăn chặn nó.
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế lan truyền
    keypoint_weight: 0.5
    description: Sự kiện kích hoạt từ phần tử con sẽ lan tỏa lên các phần tử cha theo thứ tự DOM.
  - id: KP4_2
    content: Cách ngăn chặn
    keypoint_weight: 0.5
    description: Sử dụng `event.stopPropagation()` bên trong hàm xử lý sự kiện để dừng việc lan truyền lên các cấp cha cao hơn.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, sự khác biệt giữa `useState` và `useReducer` là gì?
* **expected_key_points:**
  - id: KP5_1
    content: Độ phức tạp của State
    keypoint_weight: 0.5
    description: `useState` dùng cho state đơn giản. `useReducer` dùng cho state phức tạp có nhiều logic cập nhật phụ thuộc lẫn nhau.
  - id: KP5_2
    content: Logic quản lý
    keypoint_weight: 0.5
    description: `useReducer` tập trung logic cập nhật vào một hàm reducer duy nhất, giúp code sạch và dễ kiểm soát trạng thái hơn.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `TRUNCATE` và `DELETE` trong SQL?
* **expected_key_points:**
  - id: KP6_1
    content: Bản chất DDL vs DML
    keypoint_weight: 0.5
    description: `DELETE` là DML, xóa từng hàng một và ghi log. `TRUNCATE` là DDL, reset toàn bộ bảng nhanh chóng.
  - id: KP6_2
    content: Khả năng Rollback
    keypoint_weight: 0.5
    description: `DELETE` có thể rollback nếu đang trong transaction. `TRUNCATE` thường không thể rollback (tùy DB).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao `Cookie` với cờ `Secure` và `HttpOnly` lại quan trọng?
* **expected_key_points:**
  - id: KP7_1
    content: Secure
    keypoint_weight: 0.5
    description: Đảm bảo cookie chỉ được truyền qua kết nối HTTPS đã mã hóa, ngăn chặn đánh cắp dữ liệu qua mạng trung gian.
  - id: KP7_2
    content: HttpOnly
    keypoint_weight: 0.5
    description: Ngăn chặn JavaScript phía client truy cập vào cookie, giảm thiểu rủi ro bị tấn công XSS chiếm phiên làm việc.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" do tham chiếu Closure không được giải phóng.
* **expected_key_points:**
  - id: KP8_1
    content: Giữ scope hàm cha
    keypoint_weight: 0.5
    description: Closure giữ lại scope của hàm cha. Các biến lớn trong đó không được dọn dẹp chừng nào closure còn tồn tại trong bộ nhớ.
  - id: KP8_2
    content: Hệ quả
    keypoint_weight: 0.5
    description: Dẫn đến rò rỉ bộ nhớ nghiêm trọng trong các ứng dụng SPA nếu các hàm này bị tạo liên tục mà không bao giờ được hủy.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hydration trong SSR Framework gây nút thắt hiệu năng (Performance) ra sao?
* **expected_key_points:**
  - id: KP9_1
    content: Bản chất Hydration
    keypoint_weight: 0.5
    description: Trình duyệt phải tải và thực thi lại bundle JS để "gắn" sự kiện vào HTML tĩnh.
  - id: KP9_2
    content: Tác động Main Thread
    keypoint_weight: 0.5
    description: Việc chạy bundle JS khóa Main Thread, khiến ứng dụng không phản hồi tương tác (TTI) cho đến khi quá trình gắn kết kết thúc.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao "Optimistic UI Updates" đòi hỏi cơ chế xử lý lỗi (Rollback)?
* **expected_key_points:**
  - id: KP10_1
    content: Bản chất Optimistic
    keypoint_weight: 0.5
    description: Cập nhật giao diện giả định server thành công để tăng tốc độ phản hồi.
  - id: KP10_2
    content: Sự cần thiết của Rollback
    keypoint_weight: 0.5
    description: Khi request thực tế tới server thất bại, ứng dụng cần phải tự động hoàn tác giao diện về trạng thái ban đầu để tránh hiển thị sai dữ liệu.