# Bộ Câu Hỏi Phỏng Vấn Web Developer (Level 1) - Tập Đề Mới (31)

* **Role:** Web Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, thuộc tính `display: none` và `visibility: hidden` khác nhau như thế nào về mặt layout?
* **expected_key_points:**
  - id: KP1_1
    content: Chiếm chỗ trong luồng layout
    keypoint_weight: 0.6
    description: `display: none` loại bỏ hoàn toàn phần tử khỏi luồng layout (các phần tử xung quanh sẽ lấp đầy chỗ trống). `visibility: hidden` giữ lại khoảng trống (phần tử chỉ tàng hình).
  - id: KP1_2
    content: Khả năng tương tác
    keypoint_weight: 0.4
    description: Cả hai đều không nhận sự kiện click/hover. Tuy nhiên, `display: none` khiến phần tử mất luôn sự hiện diện trong cây render DOM, còn `visibility: hidden` thì không.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Sự khác biệt giữa `let`, `const` và `var` trong JavaScript?
* **expected_key_points:**
  - id: KP2_1
    content: Phạm vi (Scope)
    keypoint_weight: 0.5
    description: `var` có phạm vi function-scope. `let` và `const` có phạm vi block-scope (giới hạn trong cặp ngoặc nhọn `{}`).
  - id: KP2_2
    content: Khả năng gán lại
    keypoint_weight: 0.5
    description: `var` và `let` có thể thay đổi giá trị. `const` yêu cầu khởi tạo ngay và không cho phép gán lại giá trị mới cho cùng một biến.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao nên dùng thẻ ngữ nghĩa (Semantic tags) như `<main>`, `<article>`, `<footer>` thay vì dùng thẻ `<div>`?
* **expected_key_points:**
  - id: KP3_1
    content: Accessibility (Trợ năng)
    keypoint_weight: 0.6
    description: Giúp công cụ đọc màn hình (screen readers) nhận diện đúng cấu trúc và nội dung quan trọng cho người khiếm thị.
  - id: KP3_2
    content: SEO (Search Engine Optimization)
    keypoint_weight: 0.4
    description: Giúp máy tìm kiếm (như Google) hiểu rõ phân cấp nội dung, từ đó xếp hạng website tốt hơn.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích hiện tượng "Event Bubbling" trong DOM và lợi ích của nó.
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế Bubbling
    keypoint_weight: 0.5
    description: Sự kiện kích hoạt ở phần tử con sẽ lan truyền lên các phần tử cha lần lượt cho đến hết cây DOM.
  - id: KP4_2
    content: Event Delegation
    keypoint_weight: 0.5
    description: Tận dụng Bubbling để gán listener vào phần tử cha, quản lý sự kiện cho hàng loạt phần tử con mà không cần gán cho từng cái, tối ưu hiệu năng.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, sự khác biệt giữa `useState` và `useRef`?
* **expected_key_points:**
  - id: KP5_1
    content: Re-render behavior
    keypoint_weight: 0.5
    description: Thay đổi `useState` khiến component re-render. Thay đổi giá trị `useRef` (biến `.current`) không gây re-render.
  - id: KP5_2
    content: Trường hợp sử dụng
    keypoint_weight: 0.5
    description: `useState` dùng cho dữ liệu giao diện. `useRef` dùng cho lưu trữ giá trị cần giữ bền vững qua nhiều render hoặc thao tác trực tiếp với phần tử DOM.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích "CORS" (Cross-Origin Resource Sharing). Tại sao ứng dụng lại bị lỗi CORS?
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế bảo mật
    keypoint_weight: 0.5
    description: Trình duyệt chặn các request tới một origin khác (khác domain/port/giao thức) để bảo vệ dữ liệu người dùng.
  - id: KP6_2
    content: Cách giải quyết
    keypoint_weight: 0.5
    description: Server đích cần gửi thêm header `Access-Control-Allow-Origin` để cấp quyền cho phép domain của client truy cập tài nguyên.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `PUT` và `PATCH` khi cập nhật tài nguyên?
* **expected_key_points:**
  - id: KP7_1
    content: PUT (Thay thế toàn bộ)
    keypoint_weight: 0.5
    description: Yêu cầu client gửi toàn bộ đối tượng để ghi đè dữ liệu cũ.
  - id: KP7_2
    content: PATCH (Cập nhật một phần)
    keypoint_weight: 0.5
    description: Chỉ gửi các trường thông tin cần sửa đổi, phần còn lại của tài nguyên giữ nguyên trạng thái.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Hiện tượng "Memory Leak" do không dọn dẹp các Global Event Listeners.
* **expected_key_points:**
  - id: KP8_1
    content: Giữ tham chiếu không mong muốn
    keypoint_weight: 0.5
    description: Listener gắn vào `window`/`document` giữ tham chiếu đến component ngay cả khi nó bị hủy.
  - id: KP8_2
    content: Hệ quả GC
    keypoint_weight: 0.5
    description: Trình thu dọn rác (GC) không thể giải phóng bộ nhớ của component đó, dẫn đến rò rỉ bộ nhớ dần theo thời gian.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** "Hydration" trong SSR ảnh hưởng thế nào đến TTI (Time to Interactive)?
* **expected_key_points:**
  - id: KP9_1
    content: Bản chất công việc
    keypoint_weight: 0.5
    description: Quá trình chạy lại JS bundle để gắn các event handler vào HTML tĩnh nhận từ Server.
  - id: KP9_2
    content: Nút thắt (Bottleneck)
    keypoint_weight: 0.5
    description: Chạy JS tốn CPU và khóa Main Thread, người dùng sẽ thấy trang web đứng im (không click được) dù nội dung đã hiển thị xong.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao "Serializable" là mức Transaction Isolation cao nhất nhưng lại gây hại cho hiệu năng?
* **expected_key_points:**
  - id: KP10_1
    content: Tính chất tuần tự
    keypoint_weight: 0.5
    description: Ép các giao dịch phải chạy như thể chúng được thực hiện tuần tự dù có gửi tới cùng lúc.
  - id: KP10_2
    content: Cơ chế Lock
    keypoint_weight: 0.5
    description: Khóa (lock) dữ liệu cực kỳ nghiêm ngặt gây tranh chấp, giảm khả năng xử lý song song (concurrency) của hệ thống.