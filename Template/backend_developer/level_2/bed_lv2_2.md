# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2) - Tập Đề API Design và REST Best Practices (2)

* **Role:** Backend Developer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày cách sử dụng các phương thức HTTP (HTTP Methods) phổ biến: GET, POST, PUT, DELETE trong thiết kế chuẩn RESTful API.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa GET và POST
    keypoint_weight: 0.5
    description: GET dùng để truy xuất/đọc tài nguyên từ server, không làm thay đổi trạng thái dữ liệu. POST dùng để tạo mới một tài nguyên trên server.
  - id: KP1_2
    content: Định nghĩa PUT và DELETE
    keypoint_weight: 0.5
    description: PUT dùng để cập nhật đè toàn bộ tài nguyên (hoặc tạo nếu chưa tồn tại). DELETE dùng để xóa bỏ một tài nguyên xác định khỏi hệ thống.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích ý nghĩa và phân biệt các mã trạng thái HTTP (HTTP Status Codes) sau: 200, 201, 400, 401, 403, 404, và 500.
* **expected_key_points:**
  - id: KP2_1
    content: Mã thành công (200, 201) và Lỗi client (400, 404)
    keypoint_weight: 0.5
    description: 200 OK (thành công chung), 201 Created (tạo tài nguyên mới thành công). 400 Bad Request (lỗi cú pháp/dữ liệu gửi lên sai), 404 Not Found (tài nguyên không tồn tại).
  - id: KP2_2
    content: Mã phân quyền (401, 403) và Lỗi server (500)
    keypoint_weight: 0.5
    description: 401 Unauthorized (chưa đăng nhập/thiếu token), 403 Forbidden (đã đăng nhập nhưng không có quyền truy cập). 500 Internal Server Error (lỗi xử lý bên trong server).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Thế nào là tính lũy đẳng (Idempotency) trong thiết kế API? Trong các phương thức HTTP chuẩn, phương thức nào bắt buộc phải lũy đẳng?
* **expected_key_points:**
  - id: KP3_1
    content: Định nghĩa tính lũy đẳng
    keypoint_weight: 0.5
    description: Là tính chất mà khi thực hiện một request nhiều lần song song hay tuần tu thì kết quả trạng thái hệ thống vẫn giống hệt như thực hiện duy nhất một lần.
  - id: KP3_2
    content: Các phương thức bắt buộc lũy đẳng
    keypoint_weight: 0.5
    description: GET, PUT, DELETE, HEAD, OPTIONS bắt buộc phải lũy đẳng. POST không bắt buộc lũy đẳng (mỗi lần gọi tạo ra 1 tài nguyên mới).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy thiết kế cấu trúc URL và các tham số truy vấn (Query Parameters) cho một API quản lý sản phẩm hỗ trợ: lọc theo danh mục, phân trang, và sắp xếp theo giá.
* **expected_key_points:**
  - id: KP4_1
    content: Thiết kế cấu trúc URL RESTful
    keypoint_weight: 0.5
    description: Sử dụng danh từ số nhiều làm tài nguyên chính, ví dụ: `GET /api/v1/products`. Tránh dùng động từ trong đường dẫn.
  - id: KP4_2
    content: Thiết kế Query Parameters lọc, phân trang, sắp xếp
    keypoint_weight: 0.5
    description: Sử dụng query params rõ ràng: `?category=electronics&page=1&limit=20&sort_by=price&order=desc` để lọc, phân trang và sắp xếp linh hoạt.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa thiết kế API dạng RESTful và GraphQL là gì? Khi nào bạn ưu tiên sử dụng GraphQL?
* **expected_key_points:**
  - id: KP5_1
    content: Bản chất RESTful vs GraphQL
    keypoint_weight: 0.5
    description: RESTful sử dụng nhiều endpoints định dạng cứng cho từng tài nguyên. GraphQL chỉ sử dụng một endpoint duy nhất và cho phép client tự định nghĩa cấu trúc dữ liệu trả về.
  - id: KP5_2
    content: Kịch bản ưu tiên GraphQL
    keypoint_weight: 0.5
    description: Khi client cần lấy dữ liệu phức tạp từ nhiều nguồn lồng nhau trong 1 request (tránh over-fetching/under-fetching) hoặc khi xây dựng app mobile cần tối ưu dung lượng mạng.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế CORS (Cross-Origin Resource Sharing). Làm thế nào một lập trình viên Backend có thể cấu hình CORS an toàn?
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế hoạt động của CORS
    keypoint_weight: 0.5
    description: Là cơ chế bảo mật của trình duyệt ngăn chặn client gửi requests tới một domain khác domain hiện tại nếu server đích không cho phép qua các headers HTTP.
  - id: KP6_2
    content: Cấu hình CORS an toàn
    keypoint_weight: 0.5
    description: Không dùng dấu sao wildcard `Access-Control-Allow-Origin: *` cho môi trường production; thay vào đó, định nghĩa danh sách trắng (whitelist) các domains đáng tin cậy.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt sự khác nhau giữa hai phương thức cập nhật dữ liệu: PUT và PATCH. Cho ví dụ minh họa.
* **expected_key_points:**
  - id: KP7_1
    content: Nguyên lý cập nhật PUT vs PATCH
    keypoint_weight: 0.6
    description: PUT cập nhật đè toàn bộ tài nguyên (nếu thiếu trường sẽ gán mặc định hoặc null). PATCH thực hiện cập nhật một phần (partial update) chỉ trên các trường được gửi lên.
  - id: KP7_2
    content: Ví dụ minh họa cụ thể
    keypoint_weight: 0.4
    description: Nếu muốn đổi số điện thoại user: dùng PATCH gửi `{phone: '098...'}` thay vì dùng PUT gửi toàn bộ thông tin profile người dùng.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp đảm bảo tính lũy đẳng (Idempotency) cho API thanh toán (POST /api/v1/payments) trước sự cố trùng lặp request từ mạng không ổn định.
* **expected_key_points:**
  - id: KP8_1
    content: Sử dụng Idempotency Key
    keypoint_weight: 0.5
    description: Yêu cầu client tạo một UUID duy nhất (Idempotency Key) gửi trong header request. Server lưu trữ key này kèm theo kết quả xử lý giao dịch tương ứng vào Redis/DB.
  - id: KP8_2
    content: Xử lý request trùng lặp đồng thời
    keypoint_weight: 0.5
    description: Sử dụng Redis Lock với idempotency key để chặn các request song song; nếu phát hiện key đã có trong cache và giao dịch hoàn thành -> trả về ngay kết quả đã lưu mà không chạy lại thanh toán.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế chiến lược quản lý phiên bản API (API Versioning) cho một hệ thống lớn đang vận hành chịu tải cao mà không làm gián đoạn các đối tác đang kết nối.
* **expected_key_points:**
  - id: KP9_1
    content: Các phương pháp API Versioning
    keypoint_weight: 0.5
    description: Sử dụng URL path versioning (`/v1/users`), Custom Headers (`X-API-Version: 1`), hoặc Accept Header (Content Negotiation). URI versioning là cách rõ ràng và dễ cache nhất.
  - id: KP9_2
    content: Kế hoạch Deprecation và chuyển đổi
    keypoint_weight: 0.5
    description: Thiết lập cảnh báo cảnh báo hết hạn (Deprecation headers); chạy song song các phiên bản cũ và mới; viết log thu thập tỷ lệ sử dụng bản cũ trước khi tắt hẳn.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế cấu trúc mã lỗi chuẩn hóa (Error Response Design) cho toàn bộ hệ thống Microservices, giúp client dễ dàng bắt lỗi và đa ngôn ngữ hóa (I18n).
* **expected_key_points:**
  - id: KP10_1
    content: Cấu trúc body lỗi nhất quán
    keypoint_weight: 0.5
    description: Thiết kế payload trả về có cấu trúc chuẩn gồm: `error_code` (mã lỗi nghiệp vụ dạng chuỗi), `message` (mô tả lỗi tiếng Anh), và `details` (danh sách lỗi chi tiết cho từng trường validation).
  - id: KP10_2
    content: Đa ngôn ngữ hóa lỗi (I18n)
    keypoint_weight: 0.5
    description: Không hardcode message lỗi tiếng Việt ở backend. Server trả về mã code (ví dụ `USER_NOT_FOUND`) để client tự ánh xạ sang ngôn ngữ tương ứng ở giao diện.

