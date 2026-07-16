# Bộ Câu Hỏi Phỏng Vấn Web Developer (Level 1) - Tập Đề Mới (21)

* **Role:** Web Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong HTML5, sự khác biệt giữa các thẻ `<strong>` và `<b>` (cũng như `<em>` và `<i>`) là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Phân biệt ngữ nghĩa (Semantics)
    keypoint_weight: 0.6
    description: `<strong>` và `<em>` mang ý nghĩa nhấn mạnh (importance/emphasis), được trình đọc màn hình chú trọng. `<b>` và `<i>` chỉ mang tính chất định dạng hình thức (bold/italic) không kèm ngữ nghĩa.
  - id: KP1_2
    content: Accessibility
    keypoint_weight: 0.4
    description: Sử dụng đúng thẻ ngữ nghĩa giúp người dùng khiếm thị nhận biết được các phần văn bản quan trọng.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** JavaScript `null` và `undefined` khác nhau thế nào?
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: `undefined` thường là giá trị mặc định khi biến đã khai báo nhưng chưa được gán. `null` là giá trị rỗng được lập trình viên chủ động gán vào.
  - id: KP2_2
    content: Type
    keypoint_weight: 0.5
    description: `typeof undefined` trả về `'undefined'`. `typeof null` trả về `'object'` (một lỗi lịch sử của JS).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, thuộc tính `box-sizing` có những giá trị nào và giá trị nào được khuyên dùng nhất?
* **expected_key_points:**
  - id: KP3_1
    content: Các giá trị
    keypoint_weight: 0.5
    description: `content-box` (mặc định) và `border-box`.
  - id: KP3_2
    content: Giá trị khuyên dùng
    keypoint_weight: 0.5
    description: `border-box` được khuyên dùng vì nó bao gồm `padding` và `border` trong kích thước đã chỉ định, giúp tính toán layout trực quan hơn.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là Event Delegation trong JavaScript?
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế
    keypoint_weight: 0.5
    description: Gán event listener vào thẻ cha thay vì từng thẻ con, tận dụng sự lan truyền sự kiện (Bubbling) để xử lý hành động.
  - id: KP4_2
    content: Lợi ích
    keypoint_weight: 0.5
    description: Tối ưu bộ nhớ, không cần gán lại event cho các phần tử con được tạo mới sau này.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, khi nào nên sử dụng `useMemo`?
* **expected_key_points:**
  - id: KP5_1
    content: Tối ưu hiệu năng
    keypoint_weight: 0.5
    description: Dùng để ghi nhớ kết quả của một phép tính toán tốn kém tài nguyên (CPU intensive) giữa các lần render.
  - id: KP5_2
    content: Chỉ số dependency
    keypoint_weight: 0.5
    description: Chỉ nên dùng khi các dependency thay đổi thì giá trị mới cần tính lại, nếu không dùng sẽ gây lãng phí bộ nhớ vì tạo thêm bộ đệm (cache).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `localStorage` và `sessionStorage`?
* **expected_key_points:**
  - id: KP6_1
    content: Vòng đời (Persistence)
    keypoint_weight: 0.5
    description: `localStorage` tồn tại đến khi người dùng xóa. `sessionStorage` mất dữ liệu ngay khi đóng tab.
  - id: KP6_2
    content: Phạm vi (Scope)
    keypoint_weight: 0.5
    description: `localStorage` chia sẻ giữa các tab cùng origin. `sessionStorage` chỉ trong tab đang mở.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** `CORS` là gì và tại sao chúng ta gặp lỗi này?
* **expected_key_points:**
  - id: KP7_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Cơ chế bảo mật trình duyệt chặn các request khác origin trừ khi server đích gửi header `Access-Control-Allow-Origin` cho phép.
  - id: KP7_2
    content: Cách giải quyết
    keypoint_weight: 0.5
    description: Cấu hình phía Server cho phép các origin cụ thể được phép gửi yêu cầu tới.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" do không dọn dẹp các Global Event Listeners trong SPA.
* **expected_key_points:**
  - id: KP8_1
    content: Cơ chế tích lũy
    keypoint_weight: 0.5
    description: Các event listener gán vào `window` hoặc `document` không tự mất khi component bị hủy, giữ tham chiếu đến scope của component đó.
  - id: KP8_2
    content: Cách khắc phục
    keypoint_weight: 0.5
    description: Sử dụng phương thức `removeEventListener` trong lifecycle unmount hoặc cleanup function của `useEffect`.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** "Hydration" trong các framework như Next.js ảnh hưởng đến TTI như thế nào?
* **expected_key_points:**
  - id: KP9_1
    content: Quy trình
    keypoint_weight: 0.5
    description: Sau khi render HTML từ server, trình duyệt phải tải JS và chạy lại để "kết nối" sự kiện vào HTML tĩnh.
  - id: KP9_2
    content: Hiệu năng
    keypoint_weight: 0.5
    description: Quá trình này khóa Main Thread, nếu JS quá nặng thì trang web hiển thị xong nhưng không phản hồi khi người dùng thao tác.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao Database Transaction mức "Serializable" có thể làm giảm hiệu năng hệ thống?
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế khóa
    keypoint_weight: 0.5
    description: Mức này buộc các giao dịch phải thực hiện tuần tự bằng cách đặt khóa (lock) nghiêm ngặt trên toàn bộ dải dữ liệu truy vấn.
  - id: KP10_2
    content: Hệ quả
    keypoint_weight: 0.5
    description: Giảm khả năng xử lý song song (concurrency), gây nghẽn chờ đợi (deadlock) nếu nhiều giao dịch cùng tranh chấp dữ liệu.