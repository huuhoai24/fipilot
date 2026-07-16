# Bộ Câu Hỏi Phỏng Vấn Web Developer (Level 1) - Tập Đề Mới (17)

* **Role:** Web Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, thuộc tính `box-sizing: border-box` giúp ích gì cho việc tính toán kích thước phần tử?
* **expected_key_points:**
  - id: KP1_1
    content: Cơ chế tính toán (Box Model)
    keypoint_weight: 0.6
    description: `border-box` gộp cả `padding` và `border` vào trong tổng chiều rộng/cao được khai báo, thay vì cộng thêm vào kích thước gốc như `content-box`.
  - id: KP1_2
    content: Lợi ích thực tế
    keypoint_weight: 0.4
    description: Giúp lập trình viên dễ dàng thiết lập kích thước cố định cho các phần tử mà không lo bị tràn layout khi thay đổi padding hoặc border.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong JavaScript, sự khác biệt giữa `getAttribute()` và truy cập thuộc tính trực tiếp (ví dụ: `element.id`) là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Bản chất dữ liệu (HTML attribute vs DOM property)
    keypoint_weight: 0.5
    description: `getAttribute()` lấy giá trị từ mã HTML gốc. Truy cập trực tiếp qua DOM property lấy giá trị trạng thái hiện tại của phần tử trong DOM tree.
  - id: KP2_2
    content: Trường hợp sử dụng
    keypoint_weight: 0.5
    description: Dùng `getAttribute()` cho các thuộc tính tùy chỉnh (custom attributes). Dùng property trực tiếp cho các thuộc tính tiêu chuẩn (id, className, value).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Thẻ `<meta name="viewport">` tại sao bắt buộc phải có trong các ứng dụng web hiện đại?
* **expected_key_points:**
  - id: KP3_1
    content: Kiểm soát hiển thị trên di động
    keypoint_weight: 0.5
    description: Thiết lập `width=device-width` để trang web co giãn theo độ rộng màn hình thay vì giữ kích thước mặc định của desktop.
  - id: KP3_2
    content: Trải nghiệm người dùng (UX)
    keypoint_weight: 0.5
    description: Đảm bảo văn bản và giao diện không bị quá nhỏ, không cần người dùng phải zoom bằng tay để đọc.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích hiện tượng "Event Bubbling" trong DOM và lợi ích của Event Delegation.
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế Bubbling
    keypoint_weight: 0.5
    description: Sự kiện kích hoạt ở phần tử con sẽ lan tỏa ngược lên các phần tử cha theo thứ tự DOM từ dưới lên.
  - id: KP4_2
    content: Lợi ích của Delegation
    keypoint_weight: 0.5
    description: Gán 1 listener duy nhất tại cha giúp tối ưu bộ nhớ và xử lý được cả các phần tử con được thêm vào DOM sau này mà không cần gán lại.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `sessionStorage` và `localStorage` trong việc chia sẻ dữ liệu giữa các tab.
* **expected_key_points:**
  - id: KP5_1
    content: Phạm vi chia sẻ
    keypoint_weight: 0.5
    description: `localStorage` chia sẻ dữ liệu giữa tất cả các tab/cửa sổ có cùng origin. `sessionStorage` tách biệt hoàn toàn theo từng tab trình duyệt.
  - id: KP5_2
    content: Vòng đời dữ liệu
    keypoint_weight: 0.5
    description: `localStorage` tồn tại vĩnh viễn tới khi xóa. `sessionStorage` tự xóa khi tab/cửa sổ tương ứng bị đóng.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao Database Transaction Isolation Level: "Repeatable Read" lại có thể ngăn chặn "Non-repeatable Read"?
* **expected_key_points:**
  - id: KP6_1
    content: Định nghĩa Non-repeatable Read
    keypoint_weight: 0.5
    description: Xảy ra khi một giao dịch đọc một dòng dữ liệu 2 lần và nhận kết quả khác nhau do giao dịch khác đã update/commit giữa 2 lần đọc đó.
  - id: KP6_2
    content: Cơ chế Repeatable Read
    keypoint_weight: 0.5
    description: Cơ sở dữ liệu sẽ khóa (lock) dữ liệu đã đọc, ngăn các giao dịch khác sửa đổi nó cho tới khi giao dịch hiện tại kết thúc.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** "Memoization" trong JavaScript là gì và áp dụng khi nào?
* **expected_key_points:**
  - id: KP7_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Lưu kết quả trả về của một hàm dựa trên tham số đầu vào (caching). Nếu gọi lại với cùng tham số, trả về kết quả đã lưu.
  - id: KP7_2
    content: Áp dụng
    keypoint_weight: 0.5
    description: Dùng cho các hàm tính toán phức tạp, đệ quy tốn CPU, giúp tránh việc tính toán trùng lặp, tăng hiệu suất.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" do lạm dụng Closure trong hàm tạo (factory function).
* **expected_key_points:**
  - id: KP8_1
    content: Cơ chế closure gây leak
    keypoint_weight: 0.5
    description: Closure giữ lại scope của hàm cha. Nếu hàm cha có biến lớn, biến đó không bao giờ được GC dọn dẹp chừng nào closure còn tồn tại.
  - id: KP8_2
    content: Cách phòng ngừa
    keypoint_weight: 0.5
    description: Hủy các tham chiếu không cần thiết (gán `null`) sau khi thực hiện logic hoặc tránh tạo quá nhiều closure bao bọc các biến lớn.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Cơ chế "Hydration" của các Framework SSR (như Next.js) làm chậm thời gian tương tác (TTI) như thế nào?
* **expected_key_points:**
  - id: KP9_1
    content: Bản chất công việc của Hydration
    keypoint_weight: 0.5
    description: Sau khi tải HTML, trình duyệt phải tải và chạy lại toàn bộ bundle JS để "nối" lại các event handler vào DOM đã render.
  - id: KP9_2
    content: Tác động hiệu năng
    keypoint_weight: 0.5
    description: Quá trình này tiêu tốn nhiều CPU và chặn main thread, khiến người dùng thấy trang đã xong nhưng bấm nút không có tác dụng trong một khoảng thời gian.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Sự khác biệt cốt lõi giữa "Race Condition" trong JS (bất đồng bộ) và trong DB (Transaction).
* **expected_key_points:**
  - id: KP10_1
    content: Race Condition trong JS
    keypoint_weight: 0.5
    description: Do các request API bất đồng bộ hoàn thành không đúng thứ tự, dẫn đến state UI bị sai lệch.
  - id: KP10_2
    content: Race Condition trong DB
    keypoint_weight: 0.5
    description: Do 2 giao dịch cùng sửa đổi một row dữ liệu tại một thời điểm, dẫn đến mất dữ liệu hoặc xung đột logic nghiệp vụ (ví dụ: số dư tài khoản).