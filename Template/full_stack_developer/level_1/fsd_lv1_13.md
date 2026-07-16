# Bộ Câu Hỏi Phỏng Vấn Full Stack Developer (Level 1) - Tập Đề Mới (5)

* **Role:** Full Stack Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, `Flexbox` là gì? Khi nào bạn nên sử dụng `flex-direction: column` thay vì mặc định `row`?
* **expected_key_points:**
  - id: KP1_1
    content: Khái niệm Flexbox
    keypoint_weight: 0.5
    description: Flexbox là mô hình layout một chiều (one-dimensional) giúp căn chỉnh, phân bổ không gian và sắp xếp các phần tử bên trong container một cách linh hoạt.
  - id: KP1_2
    content: Khi nào dùng column
    keypoint_weight: 0.5
    description: Sử dụng `column` khi muốn các phần tử xếp chồng lên nhau theo chiều dọc (ví dụ: menu dọc, stack các khối nội dung trong màn hình mobile).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Sự khác biệt giữa `localStorage` và `sessionStorage` trong trình duyệt là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Thời hạn tồn tại của dữ liệu
    keypoint_weight: 0.5
    description: `localStorage` lưu trữ dữ liệu vĩnh viễn cho đến khi bị xóa. `sessionStorage` chỉ lưu dữ liệu trong phiên làm việc hiện tại, dữ liệu mất khi đóng tab hoặc trình duyệt.
  - id: KP2_2
    content: Phạm vi chia sẻ
    keypoint_weight: 0.5
    description: `localStorage` chia sẻ dữ liệu giữa tất cả các tab/cửa sổ cùng domain. `sessionStorage` chỉ tồn tại trong tab đó, các tab khác không truy cập được.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** `Array.map()` khác với `Array.forEach()` như thế nào?
* **expected_key_points:**
  - id: KP3_1
    content: Giá trị trả về
    keypoint_weight: 0.5
    description: `map()` trả về một mảng mới chứa kết quả của hàm callback. `forEach()` không trả về giá trị nào (trả về undefined).
  - id: KP3_2
    content: Mục đích sử dụng
    keypoint_weight: 0.5
    description: `map()` dùng để biến đổi dữ liệu (transformation). `forEach()` dùng để thực hiện các tác vụ phụ (side effects) trên từng phần tử.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm "Hoisting" trong JavaScript.
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa Hoisting
    keypoint_weight: 0.5
    description: Là cơ chế JavaScript tự động đưa khai báo biến (`var`) và hàm lên đầu scope trước khi thực thi code.
  - id: KP4_2
    content: Sự khác biệt với let/const
    keypoint_weight: 0.5
    description: `var` được hoisted và khởi tạo là `undefined`. `let`/`const` bị hoisted nhưng không được khởi tạo, dẫn đến lỗi "Temporal Dead Zone" nếu truy cập trước khi khai báo.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, `useEffect` hoạt động như thế nào và tại sao cần `cleanup function`?
* **expected_key_points:**
  - id: KP5_1
    content: Cách hoạt động của useEffect
    keypoint_weight: 0.5
    description: `useEffect` chạy sau khi render. Nó cho phép xử lý các side effect như gọi API hoặc thao tác DOM.
  - id: KP5_2
    content: Vai trò của cleanup function
    keypoint_weight: 0.5
    description: Dùng để dọn dẹp các tác vụ (như hủy subscription, clear timer) khi component bị unmount hoặc trước khi chạy lại effect mới, giúp tránh memory leak.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao Database Index lại tăng tốc độ truy vấn nhưng gây chậm thao tác ghi?
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế của Index (Read)
    keypoint_weight: 0.5
    description: Index tạo ra một cấu trúc dữ liệu bổ trợ (như B-tree) giúp database tìm kiếm mà không cần quét toàn bộ bảng.
  - id: KP6_2
    content: Chi phí cho thao tác ghi (Write)
    keypoint_weight: 0.5
    description: Khi thêm, sửa hoặc xóa dữ liệu, database phải cập nhật thêm cấu trúc index đó, làm tăng chi phí thao tác ghi (CPU và Disk I/O).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** RESTful API là gì? Giải thích các phương thức HTTP chính.
* **expected_key_points:**
  - id: KP7_1
    content: Định nghĩa REST
    keypoint_weight: 0.5
    description: REST (Representational State Transfer) là phong cách thiết kế API sử dụng các quy tắc HTTP chuẩn để tương tác với tài nguyên.
  - id: KP7_2
    content: Các phương thức HTTP
    keypoint_weight: 0.5
    description: GET (lấy dữ liệu), POST (tạo tài nguyên), PUT/PATCH (cập nhật), DELETE (xóa tài nguyên).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Event Bubbling" và làm thế nào để ngăn chặn nó?
* **expected_key_points:**
  - id: KP8_1
    content: Cơ chế Bubbling
    keypoint_weight: 0.5
    description: Sự kiện sau khi bắt nguồn từ target element sẽ lan truyền dần lên các phần tử cha (ancestors).
  - id: KP8_2
    content: Cách ngăn chặn
    keypoint_weight: 0.5
    description: Sử dụng phương thức `event.stopPropagation()` bên trong hàm xử lý sự kiện để dừng việc lan truyền lên trên.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích sự khác biệt giữa `Concurrency` (Đồng thời) và `Parallelism` (Song song) trong lập trình.
* **expected_key_points:**
  - id: KP9_1
    content: Concurrency
    keypoint_weight: 0.5
    description: Khả năng xử lý nhiều công việc bằng cách chia nhỏ và chuyển đổi qua lại giữa chúng (context switching) trên một luồng CPU.
  - id: KP9_2
    content: Parallelism
    keypoint_weight: 0.5
    description: Thực hiện nhiều công việc cùng lúc thực sự trên nhiều lõi CPU (Multi-core), yêu cầu phần cứng hỗ trợ.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao một ứng dụng React có thể bị render thừa (re-render) và cách ngăn chặn?
* **expected_key_points:**
  - id: KP10_1
    content: Nguyên nhân re-render
    keypoint_weight: 0.5
    description: Khi state của cha thay đổi hoặc props truyền vào không ổn định (tạo đối tượng mới sau mỗi lần render), component sẽ re-render.
  - id: KP10_2
    content: Cách ngăn chặn
    keypoint_weight: 0.5
    description: Sử dụng `React.memo` (cho component), `useMemo` (cho giá trị), `useCallback` (cho hàm) để ghi nhớ dữ liệu và chỉ render khi cần thiết.