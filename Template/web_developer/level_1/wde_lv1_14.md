# Bộ Câu Hỏi Phỏng Vấn Web Developer (Level 1) - Tập Đề Mới (27)

* **Role:** Web Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong HTML, sự khác biệt giữa các phần tử `Block` và `Inline` là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Chiếm diện tích (Layout)
    keypoint_weight: 0.6
    description: Phần tử `Block` chiếm toàn bộ chiều rộng có sẵn và bắt đầu một dòng mới. Phần tử `Inline` chỉ chiếm diện tích vừa đủ với nội dung bên trong và nằm cùng dòng với các phần tử khác.
  - id: KP1_2
    content: Khả năng tùy chỉnh
    keypoint_weight: 0.4
    description: `Block` cho phép tùy chỉnh width, height, margin, padding đầy đủ. `Inline` bị giới hạn về width/height và top/bottom margin.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong JavaScript, sự khác biệt giữa `null` và `undefined` là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Ngữ nghĩa (Semantics)
    keypoint_weight: 0.5
    description: `undefined` thường là giá trị mặc định của biến chưa được khởi tạo. `null` là giá trị rỗng được gán chủ động để chỉ định "không có gì cả".
  - id: KP2_2
    content: Kiểu dữ liệu (Type)
    keypoint_weight: 0.5
    description: `typeof undefined` là `'undefined'`, trong khi `typeof null` là `'object'` (một lỗi thiết kế đặc thù của JS).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao nên sử dụng `semantic tags` (như `<nav>`, `<article>`, `<section>`) thay vì chỉ dùng thẻ `<div>`?
* **expected_key_points:**
  - id: KP3_1
    content: Accessibility (Trợ năng)
    keypoint_weight: 0.5
    description: Các thẻ ngữ nghĩa giúp thiết bị hỗ trợ (screen readers) hiểu được cấu trúc nội dung, hỗ trợ người khiếm thị truy cập web dễ hơn.
  - id: KP3_2
    content: SEO (Search Engine Optimization)
    keypoint_weight: 0.5
    description: Giúp Google bot hiểu được đâu là nội dung chính, đâu là menu, đâu là footer, từ đó xếp hạng website tốt hơn.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích hiện tượng "Hoisting" trong JavaScript đối với `var` và `let`.
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế Hoisting
    keypoint_weight: 0.5
    description: Tất cả khai báo được đưa lên đầu scope hiện tại. `var` được khởi tạo là `undefined`.
  - id: KP4_2
    content: TDZ (Temporal Dead Zone)
    keypoint_weight: 0.5
    description: `let` được hoist nhưng không khởi tạo, dẫn đến lỗi `ReferenceError` nếu truy cập trước khi khai báo (vùng chết).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, khi nào nên sử dụng `useCallback`?
* **expected_key_points:**
  - id: KP5_1
    content: Ghi nhớ hàm (Memoization)
    keypoint_weight: 0.5
    description: Dùng để lưu trữ tham chiếu của một hàm giữa các lần render, tránh việc tạo mới hàm gây tốn tài nguyên.
  - id: KP5_2
    content: Khi nào cần dùng
    keypoint_weight: 0.5
    description: Thường dùng khi truyền callback xuống các component con đã được `React.memo` bao bọc, tránh component con re-render vô ích vì tham chiếu hàm thay đổi.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `PUT` và `PATCH` trong thiết kế API?
* **expected_key_points:**
  - id: KP6_1
    content: PUT (Thay thế)
    keypoint_weight: 0.5
    description: Dùng để thay thế hoàn toàn một tài nguyên. Client phải gửi đầy đủ cấu trúc của đối tượng.
  - id: KP6_2
    content: PATCH (Cập nhật một phần)
    keypoint_weight: 0.5
    description: Chỉ cần gửi những field cần thay đổi (delta update), tài nguyên cũ được giữ lại các thuộc tính không gửi kèm.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao `Cookie` với cờ `HttpOnly` lại an toàn hơn?
* **expected_key_points:**
  - id: KP7_1
    content: Chống XSS (Cross-Site Scripting)
    keypoint_weight: 0.5
    description: `HttpOnly` ngăn chặn trình duyệt cho phép code JavaScript phía client (cụ thể là `document.cookie`) đọc được giá trị cookie đó.
  - id: KP7_2
    content: Bảo vệ session
    keypoint_weight: 0.5
    description: Kẻ tấn công không thể lấy trộm Session ID thông qua XSS, từ đó hạn chế rủi ro bị chiếm quyền điều khiển phiên làm việc.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Hiện tượng "Memory Leak" xảy ra như thế nào khi sử dụng Closure trong các hàm tạo (factory)?
* **expected_key_points:**
  - id: KP8_1
    content: Scope chain
    keypoint_weight: 0.5
    description: Closure giữ tham chiếu đến scope của hàm cha. Các biến lớn trong hàm cha sẽ không bao giờ bị GC dọn dẹp chừng nào closure còn tồn tại.
  - id: KP8_2
    content: Cách xử lý
    keypoint_weight: 0.5
    description: Giải phóng các tham chiếu lớn (gán `null`) sau khi thực thi hoặc tránh tạo quá nhiều closure bao bọc các biến lớn không cần thiết.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hydration trong SSR framework ảnh hưởng đến Time to Interactive (TTI) như thế nào?
* **expected_key_points:**
  - id: KP9_1
    content: Quá trình Hydration
    keypoint_weight: 0.5
    description: Sau khi render HTML tĩnh, trình duyệt phải tải và chạy JS để đính kèm lại các sự kiện (event listener) vào DOM.
  - id: KP9_2
    content: Nút thắt (Bottleneck)
    keypoint_weight: 0.5
    description: Quá trình này chạy trên Main Thread. Nếu bundle JS lớn, trình duyệt sẽ bị "đóng băng" không thể tương tác trong lúc Hydration diễn ra.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao mức cô lập "Serializable" trong SQL lại làm giảm khả năng xử lý song song?
* **expected_key_points:**
  - id: KP10_1
    content: Tính chất tuần tự hóa
    keypoint_weight: 0.5
    description: Mức này buộc các giao dịch phải chạy như thể chúng đang chạy lần lượt, bất chấp việc chúng gửi tới cùng lúc.
  - id: KP10_2
    content: Đánh đổi hiệu năng
    keypoint_weight: 0.5
    description: Sử dụng các khóa (locks) phạm vi rộng để đảm bảo tính nhất quán, gây tranh chấp dữ liệu và làm giảm nghiêm trọng số lượng giao dịch xử lý đồng thời.