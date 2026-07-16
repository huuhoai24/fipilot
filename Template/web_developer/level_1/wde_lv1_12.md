# Bộ Câu Hỏi Phỏng Vấn Web Developer (Level 1) - Tập Đề Mới (24)

* **Role:** Web Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, thuộc tính `position: absolute` định vị phần tử dựa trên cơ sở nào?
* **expected_key_points:**
  - id: KP1_1
    content: Hệ quy chiếu của phần tử
    keypoint_weight: 0.6
    description: Phần tử có `position: absolute` được định vị so với tổ tiên (ancestor) gần nhất có thuộc tính `position` khác `static` (như `relative`, `absolute`, `fixed`).
  - id: KP1_2
    content: Nếu không có tổ tiên nào thỏa mãn
    keypoint_weight: 0.4
    description: Nếu không tìm thấy tổ tiên nào có position khác `static`, phần tử sẽ được định vị dựa trên thẻ `<body>` hoặc `<html>` (viewport).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Sự khác biệt giữa `Map` và `Object` trong JavaScript về mặt khóa (key)?
* **expected_key_points:**
  - id: KP2_1
    content: Kiểu dữ liệu của khóa
    keypoint_weight: 0.5
    description: `Object` chỉ hỗ trợ khóa là chuỗi (string) hoặc `Symbol`. `Map` hỗ trợ khóa là bất kỳ kiểu dữ liệu nào (kể cả object, function, number).
  - id: KP2_2
    content: Quản lý kích thước
    keypoint_weight: 0.5
    description: `Map` cung cấp thuộc tính `size` để lấy số lượng phần tử một cách trực tiếp, trong khi với `Object` cần dùng `Object.keys().length`.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Thẻ `<a>` (anchor) thường có thuộc tính `target="_blank"`. Tại sao chúng ta nên đi kèm với `rel="noopener"` hoặc `rel="noreferrer"`?
* **expected_key_points:**
  - id: KP3_1
    content: Bảo mật (Security)
    keypoint_weight: 0.6
    description: Ngăn chặn trang web được mở ra (trang đích) có quyền truy cập vào đối tượng `window.opener` của trang hiện tại, tránh tấn công giả mạo hoặc chiếm quyền điều khiển.
  - id: KP3_2
    content: Hiệu năng
    keypoint_weight: 0.4
    description: Cho phép trang đích chạy trên một tiến trình riêng biệt, giảm tải cho luồng chính của trang hiện tại.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, sự khác biệt giữa `useState` và `useReducer` là gì? Khi nào nên chọn `useReducer`?
* **expected_key_points:**
  - id: KP4_1
    content: Khả năng mở rộng của logic
    keypoint_weight: 0.5
    description: `useState` phù hợp cho state đơn giản. `useReducer` dùng cho state phức tạp có nhiều sub-values hoặc khi state tiếp theo phụ thuộc vào state trước đó.
  - id: KP4_2
    content: Trình tự xử lý
    keypoint_weight: 0.5
    description: `useReducer` tách biệt logic cập nhật state (reducer function) khỏi component, giúp code dễ đọc và dễ test hơn với các kịch bản state phức tạp.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích hiện tượng "Hoisting" trong JavaScript đối với các khai báo biến `var` và `let/const`.
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế của var
    keypoint_weight: 0.5
    description: Các khai báo `var` được đưa lên đầu scope và khởi tạo mặc định là `undefined`, nên có thể truy cập trước dòng khai báo mà không lỗi.
  - id: KP5_2
    content: Temporal Dead Zone (TDZ)
    keypoint_weight: 0.5
    description: `let` và `const` được hoist nhưng KHÔNG khởi tạo. Truy cập chúng trước dòng khai báo sẽ dẫn đến lỗi `ReferenceError` (đây là vùng TDZ).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong REST API, tại sao HTTP Status Code lại quan trọng trong việc thiết kế?
* **expected_key_points:**
  - id: KP6_1
    content: Chuẩn giao tiếp
    keypoint_weight: 0.5
    description: Status code giúp client hiểu kết quả request (thành công, lỗi client, lỗi server) mà không cần phân tích nội dung phản hồi.
  - id: KP6_2
    content: Phân loại cơ bản
    keypoint_weight: 0.5
    description: 2xx (thành công), 4xx (lỗi người dùng - cần sửa), 5xx (lỗi hệ thống - cần fix server).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `INNER JOIN` và `OUTER JOIN` trong SQL?
* **expected_key_points:**
  - id: KP7_1
    content: Inner Join
    keypoint_weight: 0.5
    description: Chỉ lấy ra những bản ghi mà cả hai bảng tham gia đều có giá trị khớp nhau tại cột điều kiện.
  - id: KP7_2
    content: Outer Join (Left/Right)
    keypoint_weight: 0.5
    description: Lấy toàn bộ dữ liệu của một bảng (bảng trái/phải) và các dữ liệu khớp từ bảng còn lại (nếu không khớp trả về NULL).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** "Event Delegation" trong DOM giúp tối ưu hóa hiệu năng như thế nào trong các danh sách (list) lớn?
* **expected_key_points:**
  - id: KP8_1
    content: Cơ chế quản lý bộ nhớ
    keypoint_weight: 0.5
    description: Thay vì gán hàng nghìn event listeners cho từng item, ta chỉ gán 1 listener cho thẻ cha (ul). Điều này giảm tiêu thụ bộ nhớ đáng kể.
  - id: KP8_2
    content: Xử lý phần tử động
    keypoint_weight: 0.5
    description: Với các phần tử được thêm mới vào DOM sau khi trang đã load, delegation giúp xử lý sự kiện ngay mà không cần gán lại listener cho phần tử mới đó.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hiện tượng "Memory Leak" do việc không dọn dẹp các closure tham chiếu đến DOM element?
* **expected_key_points:**
  - id: KP9_1
    content: Giữ tham chiếu DOM
    keypoint_weight: 0.5
    description: Nếu một closure (hoặc hàm callback) giữ tham chiếu đến một phần tử DOM, ngay cả khi phần tử đó bị xóa khỏi trang, bộ nhớ vẫn không được thu hồi.
  - id: KP9_2
    content: Giải pháp
    keypoint_weight: 0.5
    description: Cần đặt các biến tham chiếu DOM bằng `null` hoặc xóa bỏ các listener/timer khi component unmount để tránh bị "giữ chân" trong bộ nhớ.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích sự khác biệt giữa `Concurrency` (Đồng thời) và `Parallelism` (Song song) trong bối cảnh thực thi của Node.js?
* **expected_key_points:**
  - id: KP10_1
    content: Concurrency (Node.js)
    keypoint_weight: 0.5
    description: Node.js là đơn luồng nhưng có tính đồng thời cao nhờ Event Loop, cho phép chuyển đổi giữa các tác vụ I/O mà không chờ đợi.
  - id: KP10_2
    content: Parallelism
    keypoint_weight: 0.5
    description: Việc thực thi đồng thời thực sự trên nhiều lõi CPU. Node.js đạt được điều này qua `Worker Threads` hoặc `Cluster`, chứ không phải luồng chính.