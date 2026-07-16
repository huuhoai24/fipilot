# Bộ Câu Hỏi Phỏng Vấn Web Developer (Level 1) - Tập Đề Mới (19)

* **Role:** Web Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, sự khác biệt giữa `visibility: hidden` và `display: none` là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Ảnh hưởng đến không gian layout
    keypoint_weight: 0.6
    description: `display: none` loại bỏ hoàn toàn phần tử khỏi luồng layout (như thể nó không tồn tại). `visibility: hidden` vẫn giữ nguyên không gian chiếm dụng của phần tử đó.
  - id: KP1_2
    content: Sự kiện người dùng
    keypoint_weight: 0.4
    description: Cả hai đều khiến phần tử không thể nhận sự kiện (click, hover), nhưng `display: none` còn làm phần tử không thể truy cập qua DOM API.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** JavaScript `Array.prototype.push()` và `Array.prototype.concat()` khác nhau như thế nào?
* **expected_key_points:**
  - id: KP2_1
    content: Tính biến đổi (Mutability)
    keypoint_weight: 0.5
    description: `push()` thay đổi trực tiếp (mutate) mảng gốc. `concat()` tạo ra và trả về một mảng hoàn toàn mới.
  - id: KP2_2
    content: Giá trị trả về
    keypoint_weight: 0.5
    description: `push()` trả về độ dài mới của mảng sau khi thêm. `concat()` trả về mảng kết hợp cuối cùng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao nên ưu tiên đặt thẻ `<script>` ở cuối thẻ `<body>` thay vì trong thẻ `<head>`?
* **expected_key_points:**
  - id: KP3_1
    content: Hiệu năng tải trang
    keypoint_weight: 0.5
    description: Trình duyệt phân tích HTML từ trên xuống dưới. Script đặt ở head sẽ chặn quá trình vẽ giao diện (blocking rendering).
  - id: KP3_2
    content: Trải nghiệm người dùng
    keypoint_weight: 0.5
    description: Đặt cuối body đảm bảo nội dung HTML được hiển thị trước khi JavaScript được nạp và chạy, giúp người dùng thấy nội dung trang web nhanh hơn.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm "Strict Mode" trong JavaScript và tại sao nó được khuyến khích sử dụng?
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Là chế độ nghiêm ngặt, buộc code phải tuân thủ các quy tắc chặt chẽ hơn (ví dụ: không dùng biến chưa khai báo).
  - id: KP4_2
    content: Lợi ích bảo mật và hiệu năng
    keypoint_weight: 0.5
    description: Loại bỏ các hành vi cú pháp lỏng lẻo, chuyển các lỗi tiềm ẩn thành lỗi exception cụ thể, và giúp engine JS tối ưu mã tốt hơn.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, sự khác biệt giữa `useState` và `useRef` là gì? Khi nào nên sử dụng mỗi loại?
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế render
    keypoint_weight: 0.5
    description: Thay đổi `useState` trigger một lần render lại component. Thay đổi giá trị của `useRef` KHÔNG gây re-render.
  - id: KP5_2
    content: Mục đích sử dụng
    keypoint_weight: 0.5
    description: `useState` dùng cho dữ liệu ảnh hưởng đến giao diện. `useRef` dùng cho lưu trữ giá trị không cần hiển thị hoặc thao tác trực tiếp DOM.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong SQL, khái niệm "Index" (Chỉ mục) giúp ích gì và tại sao không nên tạo quá nhiều Index trên một bảng?
* **expected_key_points:**
  - id: KP6_1
    content: Tăng tốc độ truy vấn
    keypoint_weight: 0.5
    description: Index tạo ra cấu trúc cây tra cứu giúp tìm kiếm dữ liệu cực nhanh mà không cần quét toàn bộ bảng.
  - id: KP6_2
    content: Chi phí cho thao tác ghi
    keypoint_weight: 0.5
    description: Quá nhiều index làm chậm thao tác thêm/sửa/xóa vì mỗi thay đổi dữ liệu đều buộc phải cập nhật lại cấu trúc index liên quan.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `PUT` và `PATCH` khi cập nhật dữ liệu trong REST API là gì?
* **expected_key_points:**
  - id: KP7_1
    content: PUT (Thay thế)
    keypoint_weight: 0.5
    description: Thay thế toàn bộ tài nguyên bằng dữ liệu mới. Nếu thiếu trường nào, trường đó thường bị xóa hoặc đặt giá trị default.
  - id: KP7_2
    content: PATCH (Cập nhật một phần)
    keypoint_weight: 0.5
    description: Chỉ gửi những phần dữ liệu cần thay đổi, giữ nguyên các thuộc tính cũ của tài nguyên.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" do lạm dụng Closure trong các hàm tạo (factory function).
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất closure
    keypoint_weight: 0.5
    description: Closure lưu giữ phạm vi scope của hàm cha. Nếu hàm cha có các biến lớn, chúng không bao giờ được Garbage Collector giải phóng chừng nào closure còn sống.
  - id: KP8_2
    content: Hệ quả
    keypoint_weight: 0.5
    description: Bộ nhớ bị chiếm dụng liên tục, dẫn đến ứng dụng bị chậm hoặc crash khi chạy trong thời gian dài.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Cơ chế "Hydration" của React SSR gây ảnh hưởng thế nào đến chỉ số TTI (Time to Interactive)?
* **expected_key_points:**
  - id: KP9_1
    content: Bản chất của Hydration
    keypoint_weight: 0.5
    description: Trình duyệt phải tải và thực thi lại toàn bộ bundle JS để đính kèm event listeners vào HTML tĩnh từ server.
  - id: KP9_2
    content: Tác động hiệu năng
    keypoint_weight: 0.5
    description: Việc thực thi JS này khóa main thread, khiến người dùng không thể bấm click hay tương tác với web ngay sau khi nhìn thấy trang.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao Database Transaction Isolation Level: "Repeatable Read" lại có thể ngăn chặn "Non-repeatable Read"?
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa Non-repeatable Read
    keypoint_weight: 0.5
    description: Xảy ra khi một giao dịch đọc lại dữ liệu lần 2 và thấy giá trị đã thay đổi do một giao dịch khác commit ở giữa.
  - id: KP10_2
    content: Cơ chế của Repeatable Read
    keypoint_weight: 0.5
    description: Cơ sở dữ liệu giữ khóa (read lock) trên các dòng đã truy vấn, ngăn các giao dịch khác sửa đổi dữ liệu đó tới khi giao dịch hiện tại kết thúc.