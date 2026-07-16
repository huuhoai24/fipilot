# Bộ Câu Hỏi Phỏng Vấn Full Stack Developer (Level 1) - Tập Đề Mới (8)

* **Role:** Full Stack Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong JavaScript, sự khác biệt giữa `Map` và `Object` là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Khả năng lưu trữ Key
    keypoint_weight: 0.5
    description: `Object` chỉ hỗ trợ key là chuỗi (string) hoặc symbol. `Map` cho phép sử dụng bất kỳ kiểu dữ liệu nào làm key, bao gồm cả số, đối tượng hoặc hàm.
  - id: KP1_2
    content: Thuộc tính kích thước và thứ tự
    keypoint_weight: 0.5
    description: `Map` có thuộc tính `.size` để lấy số lượng phần tử nhanh chóng và duy trì thứ tự chèn. `Object` không có tính năng này mặc định.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Sự khác biệt giữa `HTTP` và `HTTPS` là gì? Tại sao HTTPS lại quan trọng?
* **expected_key_points:**
  - id: KP2_1
    content: Mã hóa dữ liệu
    keypoint_weight: 0.5
    description: HTTP truyền dữ liệu dạng plain-text, dễ bị đánh cắp. HTTPS sử dụng TLS/SSL để mã hóa dữ liệu, đảm bảo tính bảo mật.
  - id: KP2_2
    content: Chứng thực và tin cậy
    keypoint_weight: 0.5
    description: HTTPS xác thực danh tính server thông qua chứng chỉ số (SSL Certificate), tạo niềm tin cho người dùng khi giao dịch.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, `transition` và `animation` khác nhau như thế nào?
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế kích hoạt
    keypoint_weight: 0.5
    description: `transition` cần một sự thay đổi trạng thái (như `:hover`) để kích hoạt. `animation` có thể tự động chạy mà không cần tương tác người dùng.
  - id: KP3_2
    content: Độ phức tạp
    keypoint_weight: 0.5
    description: `transition` chỉ định nghĩa thay đổi từ điểm A sang điểm B. `animation` hỗ trợ các keyframes phức tạp, cho phép thực hiện nhiều trạng thái chuyển đổi liên tiếp.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế "Event Bubbling" và cách sử dụng `event.stopPropagation()`.
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế lan truyền sự kiện
    keypoint_weight: 0.5
    description: Khi một phần tử con kích hoạt sự kiện, sự kiện đó sẽ lan truyền lên các thành phần cha (parent elements) theo thứ tự từ trong ra ngoài (bubbling).
  - id: KP4_2
    content: Ngăn chặn lan truyền
    keypoint_weight: 0.5
    description: `event.stopPropagation()` được dùng để dừng sự lan truyền này, ngăn chặn các hàm xử lý sự kiện ở các phần tử cha được thực thi.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, `useMemo` và `useCallback` có điểm gì chung và khác biệt ra sao?
* **expected_key_points:**
  - id: KP5_1
    content: Điểm chung (Memoization)
    keypoint_weight: 0.5
    description: Cả hai đều dùng để tối ưu hiệu năng bằng cách ghi nhớ giá trị (useMemo) hoặc hàm (useCallback) để tránh tính toán lại không cần thiết.
  - id: KP5_2
    content: Sự khác biệt
    keypoint_weight: 0.5
    description: `useMemo` trả về giá trị (kết quả của một phép tính). `useCallback` trả về chính hàm đó (phiên bản đã được memoize).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao chúng ta nên ưu tiên sử dụng `Prepared Statements` khi truy vấn database SQL?
* **expected_key_points:**
  - id: KP6_1
    content: Ngăn chặn SQL Injection
    keypoint_weight: 0.5
    description: Prepared Statements tách biệt code SQL và dữ liệu đầu vào, giúp ngăn chặn kẻ tấn công chèn các câu lệnh SQL độc hại.
  - id: KP6_2
    content: Tối ưu thực thi
    keypoint_weight: 0.5
    description: Database biên dịch (compile) câu truy vấn một lần và tái sử dụng, giúp tăng tốc độ cho các truy vấn lặp đi lặp lại nhiều lần.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm "Promises" trong JavaScript và cách nó khắc phục Callback Hell.
* **expected_key_points:**
  - id: KP7_1
    content: Định nghĩa Promise
    keypoint_weight: 0.5
    description: Promise đại diện cho kết quả của một tác vụ bất đồng bộ (Pending, Fulfilled, hoặc Rejected).
  - id: KP7_2
    content: Chaining (Chuỗi)
    keypoint_weight: 0.5
    description: Thay vì lồng callback, Promise cho phép dùng `.then()` để nối các tác vụ bất đồng bộ theo chiều ngang, giúp mã nguồn rõ ràng và dễ xử lý lỗi hơn.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Khái niệm "Strict Mode" (`'use strict'`) trong JavaScript và lợi ích của nó?
* **expected_key_points:**
  - id: KP8_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Là chế độ nghiêm ngặt của JS, chuyển các lỗi tiềm ẩn (silent errors) thành lỗi thực sự (exceptions), giúp lập trình viên tránh các lỗi khó phát hiện.
  - id: KP8_2
    content: Các hạn chế chính
    keypoint_weight: 0.5
    description: Cấm khai báo biến không từ khóa, ngăn chặn việc sử dụng `this` trỏ về Global object trong hàm, cấm dùng cú pháp `with`.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Sự khác biệt giữa "Shallow Copy" và "Deep Copy" của đối tượng (Object) trong JS là gì?
* **expected_key_points:**
  - id: KP9_1
    content: Shallow Copy
    keypoint_weight: 0.5
    description: Chỉ copy lớp đối tượng đầu tiên. Các object lồng bên trong vẫn giữ nguyên tham chiếu (thay đổi object con sẽ ảnh hưởng tới cả 2).
  - id: KP9_2
    content: Deep Copy
    keypoint_weight: 0.5
    description: Tạo bản sao toàn bộ cấu trúc dữ liệu, kể cả các object lồng bên trong, không còn tham chiếu tới object gốc.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Cơ chế "Database Transaction Isolation Levels" - Tại sao lại cần mức Read Committed và Serializable?
* **expected_key_points:**
  - id: KP10_1
    content: Read Committed
    keypoint_weight: 0.5
    description: Đảm bảo chỉ đọc dữ liệu đã được commit, tránh tình trạng "Dirty Read" (đọc dữ liệu bẩn).
  - id: KP10_2
    content: Serializable
    keypoint_weight: 0.5
    description: Mức cô lập cao nhất, đảm bảo các giao dịch chạy đồng thời mang lại kết quả giống như chạy tuần tự, đảm bảo tính nhất quán tuyệt đối nhưng giảm hiệu năng.