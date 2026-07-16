# Bộ Câu Hỏi Phỏng Vấn Full Stack Developer (Level 1) - Tập Đề Mới (7)

* **Role:** Full Stack Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, `z-index` chỉ hoạt động với các phần tử có thuộc tính `position` như thế nào?
* **expected_key_points:**
  - id: KP1_1
    content: Yêu cầu về position
    keypoint_weight: 0.6
    description: `z-index` chỉ có tác dụng trên các phần tử có thuộc tính `position` là `relative`, `absolute`, `fixed`, hoặc `sticky`. Nó không hoạt động với `static` (mặc định).
  - id: KP1_2
    content: Cơ chế xếp chồng (Stacking context)
    keypoint_weight: 0.4
    description: Phần tử có `z-index` cao hơn sẽ nằm đè lên phần tử có `z-index` thấp hơn. Nếu không khai báo, phần tử xuất hiện sau trong DOM sẽ nằm đè lên phần tử trước.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Sự khác biệt giữa `==` và `===` trong JavaScript là gì?
* **expected_key_points:**
  - id: KP2_1
    content: So sánh giá trị và ép kiểu
    keypoint_weight: 0.5
    description: `==` so sánh giá trị sau khi đã thực hiện ép kiểu (type coercion). `===` so sánh cả giá trị và kiểu dữ liệu mà không ép kiểu.
  - id: KP2_2
    content: Tại sao nên dùng ===
    keypoint_weight: 0.5
    description: Dùng `===` giúp tránh lỗi logic khó hiểu do việc tự động ép kiểu gây ra trong JavaScript.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Định nghĩa và lợi ích của `Semantic HTML` là gì?
* **expected_key_points:**
  - id: KP3_1
    content: Định nghĩa thẻ ngữ nghĩa
    keypoint_weight: 0.5
    description: Là sử dụng các thẻ HTML phản ánh đúng ý nghĩa của nội dung bên trong, ví dụ: `<header>`, `<nav>`, `<section>`, `<article>`, `<footer>`.
  - id: KP3_2
    content: Lợi ích chính
    keypoint_weight: 0.5
    description: Cải thiện khả năng đọc của công cụ tìm kiếm (SEO) và hỗ trợ tốt cho người dùng sử dụng thiết bị hỗ trợ (screen readers).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, `props` được truyền đi như thế nào và tại sao nó lại là "read-only"?
* **expected_key_points:**
  - id: KP4_1
    content: Luồng dữ liệu một chiều (One-way data flow)
    keypoint_weight: 0.5
    description: Props truyền từ component cha xuống con. Tính read-only giúp đảm bảo dữ liệu không bị thay đổi bất ngờ, giúp ứng dụng dễ dự đoán.
  - id: KP4_2
    content: Cách thay đổi dữ liệu
    keypoint_weight: 0.5
    description: Nếu con muốn thay đổi dữ liệu của cha, cha phải truyền xuống một hàm callback để con gọi, giúp cha cập nhật state của chính mình.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm `JSON` và lý do nó trở thành chuẩn giao tiếp dữ liệu chính trong Web API.
* **expected_key_points:**
  - id: KP5_1
    content: Định nghĩa JSON
    keypoint_weight: 0.5
    description: JSON (JavaScript Object Notation) là định dạng văn bản nhẹ, dễ đọc cho cả người và máy, dùng để trao đổi dữ liệu.
  - id: KP5_2
    content: Tại sao phổ biến
    keypoint_weight: 0.5
    description: JSON tương thích hoàn hảo với JavaScript (nơi phát triển web chính), dễ parse, cấu trúc gọn nhẹ hơn so với XML.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong SQL, sự khác biệt giữa `WHERE` và `HAVING` là gì?
* **expected_key_points:**
  - id: KP6_1
    content: Thời điểm áp dụng
    keypoint_weight: 0.5
    description: `WHERE` lọc các hàng trước khi thực hiện nhóm dữ liệu (GROUP BY). `HAVING` lọc các nhóm dữ liệu sau khi đã thực hiện GROUP BY.
  - id: KP6_2
    content: Ứng dụng
    keypoint_weight: 0.5
    description: Dùng `WHERE` cho điều kiện hàng dữ liệu thông thường; dùng `HAVING` cho điều kiện trên các hàm tổng hợp như `COUNT`, `SUM`, `AVG`.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Middleware trong Node.js (Express) là gì?
* **expected_key_points:**
  - id: KP7_1
    content: Chu trình xử lý request
    keypoint_weight: 0.5
    description: Middleware là hàm có quyền truy cập vào đối tượng request (req), đối tượng response (res) và hàm `next` trong chu trình xử lý.
  - id: KP7_2
    content: Chức năng
    keypoint_weight: 0.5
    description: Dùng để thực thi logic bổ sung, sửa đổi dữ liệu request, hoặc chặn request nếu không thỏa mãn điều kiện (ví dụ: auth middleware).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" trong các ứng dụng JavaScript Single Page Application (SPA).
* **expected_key_points:**
  - id: KP8_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Memory leak xảy ra khi các đối tượng không còn được sử dụng nhưng vẫn bị tham chiếu bởi ứng dụng, khiến trình duyệt không thể dọn dẹp bằng Garbage Collection.
  - id: KP8_2
    content: Ví dụ phổ biến
    keypoint_weight: 0.5
    description: Quên remove event listeners khi component unmount, lưu trữ quá nhiều dữ liệu vào các biến global, hoặc đóng closure giữ lại các object lớn.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao Database Transaction cần tính Isolation? Nêu một vấn đề xảy ra nếu mức cô lập (Isolation Level) quá thấp.
* **expected_key_points:**
  - id: KP9_1
    content: Mục đích
    keypoint_weight: 0.5
    description: Isolation đảm bảo các giao dịch chạy đồng thời không ảnh hưởng đến nhau, giữ cho trạng thái DB luôn nhất quán.
  - id: KP9_2
    content: Vấn đề Dirty Read
    keypoint_weight: 0.5
    description: Nếu mức cô lập thấp, giao dịch có thể đọc phải dữ liệu mà giao dịch khác đã thay đổi nhưng chưa hoàn tất commit (dirty data), dẫn đến lỗi dữ liệu sai.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Khái niệm "Hydration" trong các framework như Next.js hoặc React SSR là gì?
* **expected_key_points:**
  - id: KP10_1
    content: Quá trình Hydration
    keypoint_weight: 0.5
    description: Là quá trình gắn các trình xử lý sự kiện (event listeners) và làm cho HTML tĩnh (do Server render) trở nên "sống động" bằng JavaScript phía client.
  - id: KP10_2
    content: Tầm quan trọng
    keypoint_weight: 0.5
    description: Cho phép người dùng nhìn thấy nội dung trang ngay lập tức (nhanh) trong khi vẫn có đầy đủ tính tương tác của một ứng dụng web hiện đại.