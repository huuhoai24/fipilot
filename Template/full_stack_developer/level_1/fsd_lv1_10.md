# Bộ Câu Hỏi Phỏng Vấn Full Stack Developer (Level 1) - Tập Đề Mới (2)

* **Role:** Full Stack Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong HTML5, thẻ `<section>`, `<article>` và `<div>` khác nhau như thế nào về mặt ngữ nghĩa (semantic)?
* **expected_key_points:**
  - id: KP1_1
    content: Sự khác biệt về ngữ nghĩa
    keypoint_weight: 0.6
    description: `<div>` là thẻ không có ý nghĩa ngữ nghĩa, dùng làm container thuần túy. `<section>` dùng để gom nhóm nội dung theo chủ đề. `<article>` dùng cho nội dung độc lập, có thể tái sử dụng (như bài blog, tin tức).
  - id: KP1_2
    content: Tầm quan trọng đối với SEO và Accessibility
    keypoint_weight: 0.4
    description: Sử dụng đúng thẻ ngữ nghĩa giúp bộ máy tìm kiếm (Google) hiểu cấu trúc trang tốt hơn và hỗ trợ các công cụ đọc màn hình cho người khiếm thị.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong JavaScript, sự khác biệt giữa `Map` và `Object` là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Loại key được hỗ trợ
    keypoint_weight: 0.5
    description: `Object` chỉ hỗ trợ key là String hoặc Symbol. `Map` cho phép key là bất kỳ kiểu dữ liệu nào (kể cả object hoặc function).
  - id: KP2_2
    content: Thứ tự và kích thước
    keypoint_weight: 0.5
    description: `Map` lưu trữ dữ liệu theo thứ tự chèn và dễ dàng lấy kích thước (size) thông qua thuộc tính `.size`, trong khi `Object` không đảm bảo thứ tự và phải tự tính toán độ dài.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Thuộc tính `position: relative` và `position: absolute` trong CSS hoạt động như thế nào?
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế của relative
    keypoint_weight: 0.5
    description: Phần tử vẫn nằm trong luồng tài liệu bình thường, các thuộc tính top/left sẽ dịch chuyển nó so với vị trí gốc.
  - id: KP3_2
    content: Cơ chế của absolute
    keypoint_weight: 0.5
    description: Phần tử bị tách ra khỏi luồng tài liệu và được định vị so với phần tử cha gần nhất có `position` khác `static`.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm "Hoisting" trong JavaScript và cách nó ảnh hưởng đến khai báo biến.
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa Hoisting
    keypoint_weight: 0.5
    description: Là cơ chế JavaScript tự động đưa các khai báo biến/hàm lên trên đầu scope hiện tại trước khi code được thực thi.
  - id: KP4_2
    content: Sự khác biệt giữa var và let/const
    keypoint_weight: 0.5
    description: `var` được hoisted và khởi tạo là `undefined`. `let`/`const` cũng được hoisted nhưng không được khởi tạo, dẫn đến "Temporal Dead Zone" (lỗi nếu dùng trước khi khai báo).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong thiết kế REST API, tại sao chúng ta nên sử dụng mã trạng thái HTTP (HTTP Status Codes) một cách chính xác?
* **expected_key_points:**
  - id: KP5_1
    content: Giao tiếp rõ ràng giữa Client và Server
    keypoint_weight: 0.5
    description: Mã trạng thái giúp phía client hiểu ngay lập tức kết quả của request mà không cần phân tích nội dung body (ví dụ 401 là lỗi xác thực, 404 là không tìm thấy).
  - id: KP5_2
    content: Phân loại trạng thái tiêu chuẩn
    keypoint_weight: 0.5
    description: Biết cách phân biệt các nhóm chính: 2xx (Success), 4xx (Client Error), 5xx (Server Error).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao chúng ta cần sử dụng "Memoization" trong các hàm tính toán phức tạp?
* **expected_key_points:**
  - id: KP6_1
    content: Định nghĩa Memoization
    keypoint_weight: 0.5
    description: Kỹ thuật lưu trữ kết quả của các lần gọi hàm trước đó dựa trên đầu vào (caching) để tái sử dụng thay vì tính toán lại.
  - id: KP6_2
    content: Tối ưu hiệu năng
    keypoint_weight: 0.5
    description: Đặc biệt hiệu quả với các hàm đệ quy hoặc hàm tốn CPU, giúp giảm thời gian phản hồi cho các yêu cầu có đầu vào trùng lặp.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong Express.js, làm thế nào để xử lý lỗi (Error Handling) toàn cục cho ứng dụng?
* **expected_key_points:**
  - id: KP7_1
    content: Định nghĩa Error Middleware
    keypoint_weight: 0.5
    description: Sử dụng hàm middleware có 4 tham số `(err, req, res, next)` để bắt tất cả các lỗi được ném ra từ các route.
  - id: KP7_2
    content: Vị trí khai báo
    keypoint_weight: 0.5
    description: Middleware xử lý lỗi phải luôn được khai báo cuối cùng sau tất cả các `app.use()` và routes để đảm bảo nó bắt được lỗi từ mọi nơi.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" trong JavaScript và các nguyên nhân phổ biến gây ra nó.
* **expected_key_points:**
  - id: KP8_1
    content: Cơ chế của Garbage Collection
    keypoint_weight: 0.5
    description: Trình duyệt tự dọn dẹp các đối tượng không còn được tham chiếu. Memory leak xảy ra khi các đối tượng vẫn bị tham chiếu không cần thiết.
  - id: KP8_2
    content: Các nguyên nhân thường gặp
    keypoint_weight: 0.5
    description: Biến toàn cục (Global variables), quên remove Event Listeners, lạm dụng closure giữ lại scope, hoặc setInterval không được clear.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Cơ chế "Reconciliation" của React giúp cập nhật giao diện như thế nào sau khi Virtual DOM thay đổi?
* **expected_key_points:**
  - id: KP9_1
    content: So sánh (Diffing Algorithm)
    keypoint_weight: 0.5
    description: React so sánh cây Virtual DOM cũ và mới. Khi phát hiện thay đổi ở một node, nó đánh dấu cập nhật mà không cần rebuild toàn bộ DOM.
  - id: KP9_2
    content: Tối ưu hoá bằng Key
    keypoint_weight: 0.5
    description: Sử dụng `key` giúp React định danh chính xác các item trong list, tránh việc render lại toàn bộ danh sách khi có item thêm/xóa/sắp xếp lại.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích khái niệm "Strict Mode" trong JavaScript và tại sao nó được khuyến khích sử dụng?
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế và ý nghĩa
    keypoint_weight: 0.5
    description: `use strict` chuyển đổi những sai sót cú pháp thành lỗi thực thụ (throw error) thay vì bỏ qua âm thầm, giúp code an toàn hơn.
  - id: KP10_2
    content: Các hạn chế an toàn
    keypoint_weight: 0.5
    description: Cấm sử dụng biến chưa khai báo, cấm `this` trỏ về window (để nó là undefined trong hàm), loại bỏ cú pháp `with`.