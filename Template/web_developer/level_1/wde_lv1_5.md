# Bộ Câu Hỏi Phỏng Vấn Web Developer (Level 1) - Tập Đề Mới (16)

* **Role:** Web Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS Flexbox, sự khác biệt giữa `justify-content` và `align-items` là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Trục chính (Main Axis)
    keypoint_weight: 0.5
    description: `justify-content` điều khiển sự phân bổ các phần tử dọc theo trục chính (mặc định là hàng ngang).
  - id: KP1_2
    content: Trục chéo (Cross Axis)
    keypoint_weight: 0.5
    description: `align-items` điều khiển sự căn chỉnh các phần tử dọc theo trục chéo (mặc định là cột dọc).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong JavaScript, sự khác biệt cơ bản giữa `for...of` và `for...in` là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Cơ chế hoạt động của for...in
    keypoint_weight: 0.5
    description: `for...in` lặp qua các thuộc tính (keys/index) của một đối tượng hoặc mảng (bao gồm cả các thuộc tính kế thừa).
  - id: KP2_2
    content: Cơ chế hoạt động của for...of
    keypoint_weight: 0.5
    description: `for...of` lặp trực tiếp qua các giá trị (values) của các đối tượng có tính iterable (như Array, String, Set, Map).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao nên sử dụng `<button>` thay vì thẻ `<a>` hoặc `<div>` cho các hành động click (như gửi form, mở modal)?
* **expected_key_points:**
  - id: KP3_1
    content: Khả năng tiếp cận (Accessibility)
    keypoint_weight: 0.5
    description: `<button>` hỗ trợ bàn phím mặc định (phím Enter/Space) và trình đọc màn hình hiểu rõ đây là phần tử tương tác.
  - id: KP3_2
    content: Ngữ nghĩa (Semantic)
    keypoint_weight: 0.5
    description: Sử dụng đúng thẻ giúp trình duyệt quản lý sự kiện tốt hơn và tách biệt rõ ràng giữa điều hướng (link) và hành động (button).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích hiện tượng "Prop Drilling" trong React và cách khắc phục?
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa Prop Drilling
    keypoint_weight: 0.5
    description: Là hiện tượng truyền dữ liệu qua nhiều cấp component trung gian chỉ để đến được component con cần dùng, dù các component ở giữa không sử dụng dữ liệu đó.
  - id: KP4_2
    content: Giải pháp
    keypoint_weight: 0.5
    description: Sử dụng `Context API` để chia sẻ dữ liệu toàn cục, hoặc các thư viện quản lý state (như Redux, Zustand) để truy cập dữ liệu trực tiếp.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong SQL, khái niệm "Transaction" là gì và tại sao nó cần thiết?
* **expected_key_points:**
  - id: KP5_1
    content: Định nghĩa Transaction
    keypoint_weight: 0.5
    description: Là một chuỗi các thao tác trên DB được coi như một đơn vị làm việc duy nhất, đảm bảo tính toàn vẹn (tất cả thành công hoặc tất cả thất bại).
  - id: KP5_2
    content: Ví dụ thực tế
    keypoint_weight: 0.5
    description: Ví dụ chuyển tiền: trừ tài khoản A và cộng tài khoản B phải cùng xảy ra, nếu một bước lỗi thì phải rollback cả giao dịch.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao `Cookie` có thuộc tính `HttpOnly` lại quan trọng đối với bảo mật web?
* **expected_key_points:**
  - id: KP6_1
    content: Ngăn chặn XSS
    keypoint_weight: 0.5
    description: Khi `HttpOnly` được bật, JavaScript ở phía client không thể truy cập Cookie này qua `document.cookie`, ngăn kẻ tấn công đánh cắp session ID nếu trang web dính lỗi XSS.
  - id: KP6_2
    content: Bản chất truyền tải
    keypoint_weight: 0.5
    description: Cookie vẫn được trình duyệt tự động gửi lên server qua các HTTP request, vẫn hoạt động bình thường cho các tác vụ xác thực.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `REST` và `GraphQL` trong việc lấy dữ liệu (fetching)?
* **expected_key_points:**
  - id: KP7_1
    content: REST (Cố định endpoint)
    keypoint_weight: 0.5
    description: Mỗi endpoint trả về cấu trúc dữ liệu cố định, thường gây dư thừa (over-fetching) hoặc thiếu (under-fetching).
  - id: KP7_2
    content: GraphQL (Linh hoạt)
    keypoint_weight: 0.5
    description: Client tự định nghĩa cấu trúc dữ liệu muốn nhận, server chỉ trả về chính xác những trường đó, tối ưu băng thông.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Reflow" và cách tránh nó khi thao tác DOM số lượng lớn.
* **expected_key_points:**
  - id: KP8_1
    content: Định nghĩa Reflow
    keypoint_weight: 0.5
    description: Quá trình trình duyệt tính toán lại vị trí và hình học của các phần tử trong cây render, cực kỳ tiêu tốn hiệu năng.
  - id: KP8_2
    content: Cách giảm thiểu
    keypoint_weight: 0.5
    description: Dùng `DocumentFragment` để thao tác off-DOM, thay đổi style bằng cách thêm class thay vì sửa từng thuộc tính, hoặc dùng `requestAnimationFrame`.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Khái niệm "Hydration" và lý do tại sao nó là điểm yếu về hiệu năng (Performance) trong các SSR Framework?
* **expected_key_points:**
  - id: KP9_1
    content: Bản chất Hydration
    keypoint_weight: 0.5
    description: Sau khi server gửi HTML tĩnh, trình duyệt phải tải toàn bộ Bundle JS và chạy lại để "gắn" lại các event handler và state.
  - id: KP9_2
    content: Vấn đề hiệu năng
    keypoint_weight: 0.5
    description: Quá trình này khóa Main Thread của trình duyệt. Nếu Bundle JS lớn, người dùng không thể tương tác với trang dù trang đã hiển thị nội dung.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao Database Transaction Isolation Level: "Repeatable Read" lại có thể ngăn chặn "Non-repeatable Read"?
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa Non-repeatable Read
    keypoint_weight: 0.5
    description: Là khi một giao dịch đọc cùng một bản ghi 2 lần nhưng thấy giá trị thay đổi do giao dịch khác đã update và commit ở giữa.
  - id: KP10_2
    content: Cơ chế Repeatable Read
    keypoint_weight: 0.5
    description: Sử dụng các khóa đọc (Read locks) trên các hàng đã truy vấn, ngăn các giao dịch khác sửa đổi dữ liệu đó cho đến khi giao dịch hiện tại kết thúc.