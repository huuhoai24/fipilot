# Bộ Câu Hỏi Phỏng Vấn Web Developer (Level 1) - Tập Đề Mới (26)

* **Role:** Web Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, thuộc tính `z-index` có tác dụng gì và khi nào nó không hoạt động?
* **expected_key_points:**
  - id: KP1_1
    content: Cơ chế của z-index
    keypoint_weight: 0.6
    description: `z-index` xác định thứ tự xếp chồng (trước/sau) của các phần tử dọc theo trục Z. Giá trị cao hơn sẽ nằm đè lên giá trị thấp hơn.
  - id: KP1_2
    content: Điều kiện bắt buộc
    keypoint_weight: 0.4
    description: `z-index` chỉ có tác dụng trên các phần tử có thuộc tính `position` là `relative`, `absolute`, `fixed`, hoặc `sticky`. Nó sẽ không hoạt động nếu phần tử có `position: static` (mặc định).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** JavaScript `Array.prototype.map()` và `Array.prototype.forEach()` khác nhau như thế nào?
* **expected_key_points:**
  - id: KP2_1
    content: Giá trị trả về
    keypoint_weight: 0.5
    description: `map()` tạo và trả về một mảng mới chứa kết quả của hàm callback. `forEach()` thực hiện logic trên từng phần tử nhưng không trả về mảng mới (trả về `undefined`).
  - id: KP2_2
    content: Mục đích sử dụng
    keypoint_weight: 0.5
    description: Dùng `map()` để biến đổi dữ liệu (data transformation). Dùng `forEach()` để thực thi các tác vụ phụ (side effects) như logging hoặc thay đổi trạng thái bên ngoài.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao nên dùng thẻ `<button>` thay vì thẻ `<a>` cho các hành động gửi dữ liệu (như submit form)?
* **expected_key_points:**
  - id: KP3_1
    content: Ngữ nghĩa (Semantics)
    keypoint_weight: 0.6
    description: `<button>` biểu thị một hành động (action) cần thực hiện. `<a>` biểu thị một sự điều hướng (navigation) tới một URL mới.
  - id: KP3_2
    content: Hỗ trợ Accessibility
    keypoint_weight: 0.4
    description: Trình đọc màn hình và điều hướng bằng bàn phím xử lý nút bấm đúng theo ngữ nghĩa, đảm bảo trải nghiệm người dùng tốt hơn.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, "Prop Drilling" là gì và làm sao để hạn chế nó?
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa Prop Drilling
    keypoint_weight: 0.5
    description: Là hiện tượng truyền dữ liệu qua nhiều cấp component trung gian mà không thực sự cần dùng, chỉ để chuyển dữ liệu đến component con ở sâu bên dưới.
  - id: KP4_2
    content: Giải pháp hạn chế
    keypoint_weight: 0.5
    description: Sử dụng `Context API` hoặc các thư viện quản lý state (như Redux, Zustand, Recoil) để truy cập dữ liệu trực tiếp tại component cần dùng.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong SQL, sự khác biệt giữa `INNER JOIN` và `LEFT JOIN`?
* **expected_key_points:**
  - id: KP5_1
    content: INNER JOIN
    keypoint_weight: 0.5
    description: Chỉ lấy ra các bản ghi có sự khớp nối (match) dữ liệu ở cả hai bảng.
  - id: KP5_2
    content: LEFT JOIN
    keypoint_weight: 0.5
    description: Lấy tất cả bản ghi ở bảng bên trái và dữ liệu khớp từ bảng phải. Nếu không khớp ở bảng phải, các cột bên phải sẽ có giá trị NULL.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** `JWT` (JSON Web Token) khác gì với `Session` dựa trên Cookies?
* **expected_key_points:**
  - id: KP6_1
    content: Trạng thái (State)
    keypoint_weight: 0.5
    description: Session lưu trạng thái tại server. JWT là stateless, chứa thông tin trong token gửi từ client, giúp giảm tải cho server.
  - id: KP6_2
    content: Khả năng mở rộng
    keypoint_weight: 0.5
    description: JWT giúp hệ thống phân tán dễ dàng mở rộng vì mọi node server đều có thể xác thực token bằng secret key mà không cần tra cứu database.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cách `Event Loop` xử lý các tác vụ bất đồng bộ trong JavaScript.
* **expected_key_points:**
  - id: KP7_1
    content: Call Stack và Callback Queue
    keypoint_weight: 0.5
    description: Các task đồng bộ nằm ở Call Stack. Các task bất đồng bộ (API, timers) khi hoàn thành sẽ được đưa vào Callback Queue.
  - id: KP7_2
    content: Vòng lặp Event Loop
    keypoint_weight: 0.5
    description: Event Loop liên tục kiểm tra nếu Call Stack rỗng, nó sẽ lấy task từ Queue đẩy vào Stack để thực thi.

---

## CÂU ĐỘ KHÓ CAO (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích sự khác biệt giữa "Reflow" và "Repaint" trong trình duyệt.
* **expected_key_points:**
  - id: KP8_1
    content: Reflow (Layout)
    keypoint_weight: 0.5
    description: Quá trình tính toán lại vị trí và kích thước của các phần tử. Đây là thao tác cực kỳ tốn hiệu năng.
  - id: KP8_2
    content: Repaint (Paint)
    keypoint_weight: 0.5
    description: Quá trình vẽ lại các chi tiết trực quan (màu sắc, viền) mà không làm thay đổi layout. Reflow luôn kéo theo Repaint.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao Database Transaction Isolation Level "Serializable" có thể gây ra hiện tượng Deadlock?
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế khóa nghiêm ngặt
    keypoint_weight: 0.5
    description: Mức này giữ các khóa (lock) dữ liệu rất lâu để đảm bảo tuần tự hóa, khiến các giao dịch khác phải đợi.
  - id: KP9_2
    content: Deadlock (Bế tắc)
    keypoint_weight: 0.5
    description: Nếu giao dịch A đang giữ khóa phần 1 và đợi phần 2, trong khi giao dịch B giữ khóa phần 2 và đợi phần 1, hệ thống sẽ rơi vào tình trạng bế tắc vĩnh viễn.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích khái niệm "Hydration" và tác động của nó đến chỉ số TTI (Time to Interactive).
* **expected_key_points:**
  - id: KP10_1
    content: Quy trình Hydration
    keypoint_weight: 0.5
    description: Quá trình React gắn lại event handlers và state vào cây DOM tĩnh đã render từ server (SSR).
  - id: KP10_2
    content: Nút thắt hiệu năng
    keypoint_weight: 0.5
    description: Quá trình này chạy trên Main Thread của trình duyệt. Nếu bundle JS quá lớn, trang web dù đã hiển thị nội dung nhưng vẫn "đóng băng", người dùng không thể thao tác (click, scroll) cho đến khi Hydration hoàn tất.