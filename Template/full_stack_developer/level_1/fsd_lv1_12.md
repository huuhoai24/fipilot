# Bộ Câu Hỏi Phỏng Vấn Full Stack Developer (Level 1) - Tập Đề Mới (4)

* **Role:** Full Stack Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong JavaScript, sự khác biệt giữa `==` (loose equality) và `===` (strict equality) là gì? Tại sao nên ưu tiên sử dụng `===`?
* **expected_key_points:**
  - id: KP1_1
    content: Cơ chế so sánh của == và ===
    keypoint_weight: 0.6
    description: `==` thực hiện ép kiểu dữ liệu (type coercion) nếu hai bên khác kiểu, dẫn đến kết quả khó lường. `===` so sánh cả giá trị và kiểu dữ liệu mà không ép kiểu.
  - id: KP1_2
    content: Độ tin cậy của mã nguồn
    keypoint_weight: 0.4
    description: Sử dụng `===` giúp mã nguồn rõ ràng, tránh các lỗi logic ẩn do việc tự động ép kiểu gây ra, tăng tính bảo trì.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong HTML5, sự khác biệt giữa thẻ `<span>` và `<div>` là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Đặc tính hiển thị
    keypoint_weight: 0.5
    description: `<div>` là block-level element (chiếm trọn chiều ngang), `<span>` là inline-level element (chiếm diện tích bằng nội dung).
  - id: KP2_2
    content: Mục đích sử dụng
    keypoint_weight: 0.5
    description: `<div>` dùng để gom nhóm các khối (layout container), `<span>` dùng để styling hoặc xử lý một đoạn text nhỏ trong dòng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao chúng ta cần sử dụng `async` và `defer` khi chèn file JavaScript vào HTML?
* **expected_key_points:**
  - id: KP3_1
    content: Vấn đề render blocking
    keypoint_weight: 0.5
    description: Mặc định script sẽ chặn trình duyệt phân tích HTML khi đang tải, làm trang web bị giật/chậm.
  - id: KP3_2
    content: Tối ưu tải trang
    keypoint_weight: 0.5
    description: `async` tải file bất đồng bộ và chạy ngay khi xong. `defer` tải bất đồng bộ nhưng đợi HTML phân tích xong mới chạy, giúp cải thiện tốc độ tải trang.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, `key` trong danh sách (List) dùng để làm gì? Tại sao không nên dùng `index` làm key?
* **expected_key_points:**
  - id: KP4_1
    content: Định danh của React
    keypoint_weight: 0.5
    description: `key` giúp React định danh từng item, hỗ trợ thuật toán diffing cập nhật DOM chính xác.
  - id: KP4_2
    content: Rủi ro khi dùng index
    keypoint_weight: 0.5
    description: Dùng `index` làm key dẫn đến bug giao diện khi danh sách thay đổi thứ tự, bị chèn thêm hoặc xóa item, vì key không phản ánh đúng dữ liệu item.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong SQL, sự khác biệt giữa `TRUNCATE` và `DELETE` là gì?
* **expected_key_points:**
  - id: KP5_1
    content: Bản chất thao tác
    keypoint_weight: 0.5
    description: `DELETE` là DML (Data Manipulation Language), xóa từng hàng một và ghi log (rollback được). `TRUNCATE` là DDL (Data Definition Language), giải phóng toàn bộ bảng ngay lập tức (không rollback được).
  - id: KP5_2
    content: Hiệu năng và Trigger
    keypoint_weight: 0.5
    description: `TRUNCATE` nhanh hơn nhiều nhưng không kích hoạt `DELETE` triggers của bảng.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** "Event Bubbling" và "Event Capturing" trong DOM là gì?
* **expected_key_points:**
  - id: KP6_1
    content: Event Capturing (Từ trên xuống)
    keypoint_weight: 0.5
    description: Sự kiện đi từ node gốc (document) xuống tới mục tiêu (target) ban đầu.
  - id: KP6_2
    content: Event Bubbling (Từ dưới lên)
    keypoint_weight: 0.5
    description: Sự kiện sau khi đạt mục tiêu sẽ lan tỏa ngược lên các thành phần cha (parent). Đây là cơ chế mặc định thường gặp.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Middleware trong Express.js là gì? Làm sao để dừng một chuỗi middleware?
* **expected_key_points:**
  - id: KP7_1
    content: Định nghĩa middleware
    keypoint_weight: 0.5
    description: Là hàm có quyền truy cập request, response và hàm `next` để chuyển sang bước tiếp theo.
  - id: KP7_2
    content: Dừng chuỗi
    keypoint_weight: 0.5
    description: Không gọi `next()` và gửi phản hồi (res.send/res.json) hoặc gọi `next('route')` để bỏ qua các middleware còn lại của route đó.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Explain the "Prototype Chain" in JavaScript.
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất prototype
    keypoint_weight: 0.5
    description: Mỗi object trong JS có một liên kết nội bộ tới object khác gọi là Prototype. Nếu property không tìm thấy ở object hiện tại, JS sẽ tìm ở prototype của nó.
  - id: KP8_2
    content: Cơ chế kế thừa
    keypoint_weight: 0.5
    description: Đây là cơ chế kế thừa nguyên bản của JS, cho phép chia sẻ thuộc tính/phương thức giữa các object mà không cần tạo class phức tạp.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Khi nào cần dùng `useCallback` hook trong React và tác hại của việc dùng nó quá nhiều?
* **expected_key_points:**
  - id: KP9_1
    content: Mục đích sử dụng
    keypoint_weight: 0.5
    description: Dùng để ghi nhớ (memoize) hàm, ngăn việc tạo mới hàm sau mỗi lần render, tránh việc component con bị re-render không cần thiết.
  - id: KP9_2
    content: Tác hại lạm dụng
    keypoint_weight: 0.5
    description: Dùng sai cách hoặc quá nhiều sẽ gây tốn tài nguyên bộ nhớ để lưu trữ các hàm và tốn CPU để tính toán phụ thuộc của hook, đôi khi còn chậm hơn bình thường.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Sự khác biệt giữa "Concurrency" (Đồng thời) và "Parallelism" (Song song) trong lập trình backend?
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa Concurrency
    keypoint_weight: 0.5
    description: Khả năng xử lý nhiều công việc bằng cách chuyển đổi giữa chúng (context switching), ví dụ Node.js event loop xử lý nhiều request trên 1 luồng.
  - id: KP10_2
    content: Định nghĩa Parallelism
    keypoint_weight: 0.5
    description: Thực hiện nhiều công việc cùng một lúc thực sự (trên nhiều lõi CPU), yêu cầu phần cứng hỗ trợ.