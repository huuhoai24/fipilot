# Bộ Câu Hỏi Phỏng Vấn Web Developer (Level 1) - Tập Đề Mới (20)

* **Role:** Web Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, `z-index` hoạt động như thế nào và tại sao đôi khi nó không có tác dụng?
* **expected_key_points:**
  - id: KP1_1
    content: Điều kiện cần của position
    keypoint_weight: 0.5
    description: `z-index` chỉ hoạt động trên các phần tử có thuộc tính `position` là `relative`, `absolute`, `fixed`, hoặc `sticky` (không phải `static`).
  - id: KP1_2
    content: Stacking Context
    keypoint_weight: 0.5
    description: `z-index` bị giới hạn trong Stacking Context của phần tử cha. Nếu phần tử cha có stacking context thấp hơn, thì `z-index` của phần tử con không thể vượt ra ngoài.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong JavaScript, sự khác biệt giữa `let` và `var` khi khai báo biến trong vòng lặp là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Scope (Phạm vi)
    keypoint_weight: 0.5
    description: `var` có phạm vi function-scope (dùng chung 1 biến trong toàn bộ hàm). `let` có phạm vi block-scope (tạo ra một biến mới cho mỗi vòng lặp).
  - id: KP2_2
    content: Hiện tượng Closure trong loop
    keypoint_weight: 0.5
    description: Với `var`, các callback trong loop thường tham chiếu cùng một giá trị cuối cùng. Với `let`, mỗi iteration lưu giữ giá trị riêng của nó.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Thẻ `<picture>` trong HTML dùng để làm gì?
* **expected_key_points:**
  - id: KP3_1
    content: Responsive Images
    keypoint_weight: 0.5
    description: Cho phép chỉ định nhiều nguồn ảnh khác nhau cho các kích thước màn hình hoặc định dạng trình duyệt khác nhau.
  - id: KP3_2
    content: Hiệu năng tải trang
    keypoint_weight: 0.5
    description: Giúp trình duyệt chỉ tải đúng file ảnh phù hợp, giảm băng thông không cần thiết cho các thiết bị di động.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm "Higher-Order Function" trong JavaScript và cho ví dụ.
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa HOF
    keypoint_weight: 0.5
    description: Là hàm có khả năng nhận hàm khác làm tham số hoặc trả về một hàm như là kết quả.
  - id: KP4_2
    content: Ví dụ phổ biến
    keypoint_weight: 0.5
    description: Các hàm mảng như `map`, `filter`, `reduce` là những ví dụ điển hình của HOF giúp xử lý logic mạnh mẽ và linh hoạt.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, sự khác biệt giữa `useCallback` và `useMemo` là gì?
* **expected_key_points:**
  - id: KP5_1
    content: Mục đích ghi nhớ
    keypoint_weight: 0.5
    description: `useMemo` dùng để lưu trữ giá trị tính toán. `useCallback` dùng để lưu trữ tham chiếu của chính function đó.
  - id: KP5_2
    content: Trường hợp sử dụng
    keypoint_weight: 0.5
    description: Dùng `useMemo` cho các hàm tính toán nặng. Dùng `useCallback` khi truyền hàm xuống component con đã được `React.memo` để tránh re-render thừa.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong SQL, sự khác biệt giữa `TRUNCATE` và `DELETE` trong việc quản lý dữ liệu?
* **expected_key_points:**
  - id: KP6_1
    content: Bản chất thao tác
    keypoint_weight: 0.5
    description: `DELETE` là DML, xóa từng hàng và ghi log (có thể rollback). `TRUNCATE` là DDL, giải phóng bảng (reset cấu trúc) và không ghi log từng dòng.
  - id: KP6_2
    content: Hiệu năng và Trigger
    keypoint_weight: 0.5
    description: `TRUNCATE` nhanh hơn nhiều nhưng không kích hoạt các `DELETE` trigger.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Ý nghĩa của `Same-Origin Policy` đối với các API Request từ Client?
* **expected_key_points:**
  - id: KP7_1
    content: Cơ chế bảo mật
    keypoint_weight: 0.5
    description: Ngăn chặn script từ domain A truy cập dữ liệu (cookie, localstorage) hoặc thực hiện API request đến domain B nếu server B không cho phép.
  - id: KP7_2
    content: Giải pháp CORS
    keypoint_weight: 0.5
    description: CORS (Cross-Origin Resource Sharing) là cơ chế mà server sử dụng header để cấp quyền cho phép các domain khác truy cập tài nguyên của mình.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Reflow" và cách tránh nó khi thao tác DOM số lượng lớn.
* **expected_key_points:**
  - id: KP8_1
    content: Định nghĩa Reflow
    keypoint_weight: 0.5
    description: Quá trình trình duyệt tính toán lại vị trí và hình học của các phần tử trong cây render, tiêu tốn CPU đáng kể.
  - id: KP8_2
    content: Cách giảm thiểu
    keypoint_weight: 0.5
    description: Dùng `DocumentFragment` để thao tác off-DOM, thay đổi style bằng cách thêm class thay vì sửa từng thuộc tính, hoặc dùng `requestAnimationFrame`.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Cơ chế "Hydration" trong SSR gây ảnh hưởng đến TTI (Time to Interactive) như thế nào?
* **expected_key_points:**
  - id: KP9_1
    content: Quá trình Hydration
    keypoint_weight: 0.5
    description: Là việc trình duyệt chạy lại bundle JS để gắn kết các event listeners vào HTML tĩnh đã nhận được từ Server.
  - id: KP9_2
    content: Nút thắt hiệu năng
    keypoint_weight: 0.5
    description: Quá trình này khóa Main Thread. Nếu bundle JS quá lớn, người dùng sẽ thấy trang web đã hiện nhưng không thể tương tác (bấm chuột không phản hồi).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** "Optimistic UI Updates" là gì và tại sao cần xử lý Rollback?
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Cập nhật giao diện ngay lập tức dựa trên giả định rằng request tới server sẽ thành công.
  - id: KP10_2
    content: Xử lý Rollback
    keypoint_weight: 0.5
    description: Nếu server trả về lỗi, giao diện phải hoàn tác về trạng thái cũ để đảm bảo tính nhất quán của dữ liệu.