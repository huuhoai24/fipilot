# Bộ Câu Hỏi Phỏng Vấn Full-Stack Developer (Level 1)

* **Role:** Full-Stack Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Khái niệm "Client-Side" và "Server-Side" trong lập trình Web đại diện cho những thành phần nào và chúng giao tiếp with nhau qua giao thức nào?
* **Đáp án mẫu:** - Client-Side (Frontend) chạy trên trình duyệt của người dùng (HTML, CSS, JS). 
  - Server-Side (Backend) chạy trên máy chủ để xử lý logic và cơ sở dữ liệu. 
  - Hai bên giao tiếp với nhau chủ yếu qua giao thức HTTP/HTTPS.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, sự khác biệt cốt lõi giữa hai thuộc tính hiển thị `display: none` và `visibility: hidden` là gì?
* **Đáp án mẫu:** - `display: none` ẩn hoàn toàn phần tử và xóa bỏ hoàn toàn không gian chiếm dụng của nó trên giao diện (layout).
  - `visibility: hidden` ẩn phần tử nhưng vẫn giữ lại khoảng không gian chiếm dụng của phần tử đó trên giao diện (để lại khoảng trống).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Lệnh `git merge` và `git rebase` đều dùng để tích hợp code từ nhánh này sang nhánh khác. Sự khác biệt cơ bản về lịch sử commit (Commit History) giữa chúng là gì?
* **Đáp án mẫu:** - `git merge` giữ nguyên lịch sử và tạo ra một commit gộp (merge commit) mới, liên kết cả hai nhánh lại với nhau.
  - `git rebase` viết lại lịch sử bằng cách chuyển toàn bộ các commit của nhánh hiện tại lên trên đỉnh của nhánh đích, tạo ra một đường thẳng tuyến tính.

---

## CÂU HỎI TRUNG BÌNH (4 câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Mô hình kiến trúc MVC (Model-View-Controller) phân tách một ứng dụng web thành 3 thành phần cốt lõi nào? Nêu nhiệm vụ ngắn gọn của từng thành phần.
* **Đáp án mẫu:** - Model: Quản lý dữ liệu, logic nghiệp vụ và tương tác với Database.
  - View: Hiển thị giao diện và dữ liệu cho người dùng cuối.
  - Controller: Tiếp nhận request từ người dùng, điều phối dữ liệu qua Model và chọn View phù hợp để trả về kết quả.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Cơ chế State Management (Quản lý trạng thái) trong các Frontend Framework (như React, Vue) giải quyết bài toán khó khăn nào của JavaScript thuần?
* **Đáp án mẫu:** Nó giải quyết bài toán đồng bộ và truyền dữ liệu giữa nhiều component phức tạp. Thay vì phải truyền dữ liệu thủ công qua nhiều tầng (prop drilling) hoặc cập nhật DOM thủ công bằng JS thuần, State Management tạo ra một luồng dữ liệu tập trung giúp giao diện tự động cập nhật chính xác khi trạng thái thay đổi.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt cốt lõi giữa cơ chế kết nối qua HTTP Request truyền thống và WebSockets là gì? Khi nào một Full-Stack Developer nên dùng WebSockets?
* **Đáp án mẫu:** - HTTP Request: Client phải chủ động gửi yêu cầu thì Server mới phản hồi (giao tiếp một chiều, ngắt kết nối sau khi phản hồi).
  - WebSockets: Thiết lập một kết nối liên tục, hai chiều (full-duplex) giữa Client và Server.
  - Nên dùng WebSockets khi xây dựng ứng dụng thời gian thực (Real-time) như: Chat app, biểu đồ chứng khoán, thông báo trực ca.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Để phòng chống lỗ hổng bảo mật SQL Injection khi tương tác với cơ sở dữ liệu, lập trình viên Back-End nên viết câu lệnh truy vấn theo cách nào?
* **Đáp án mẫu:** Tuyệt đối không dùng kỹ thuật cộng chuỗi (string concatenation) để ghép dữ liệu nhập từ người dùng vào câu lệnh SQL. Thay vào đó, phải sử dụng Parameterized Queries (truy vấn có tham số) hoặc Prepared Statements, hoặc sử dụng các thư viện ORM phổ biến.

---

## CÂU HỎI KHÓ (3 câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân biệt hai chiến lược kết xuất trang web: SSR (Server-Side Rendering) và SPA (Single Page Application - Client-Side Rendering) về mặt tốc độ tải trang ban đầu và tối ưu hóa SEO.
* **Đáp án mẫu:** - SSR: Server render sẵn mã HTML đầy đủ nội dung rồi gửi về trình duyệt. Ưu điểm: SEO cực tốt, trang ban đầu hiển thị nhanh. Nhược điểm: Chuyển trang chậm vì phải load lại từ server.
  - SPA: Trình duyệt tải một file HTML rỗng và file JS về rồi tự sinh giao diện trên máy Client. Ưu điểm: Trải nghiệm mượt, chuyển trang nhanh. Nhược điểm: Tải trang đầu chậm, SEO kém nếu không có cấu hình bổ trợ.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Khi thiết kế một hệ thống lưu trữ phiên đăng nhập, việc lưu JWT ở `LocalStorage` của trình duyệt có nguy cơ bảo mật gì và giải pháp thay thế an toàn hơn là gì?
* **Đáp án mẫu:** - Nguy cơ: `LocalStorage` có thể bị truy cập bởi bất kỳ đoạn mã JavaScript nào trên trang, dẫn đến nguy cơ bị đánh cắp Token qua lỗ hổng tấn công XSS (Cross-Site Scripting).
  - Giải pháp: Lưu JWT vào bên trong `HttpOnly Cookie` kèm theo cờ `Secure` và `SameSite`, ngăn không cho JavaScript truy cập trực tiếp vào cookie này, giảm thiểu nguy cơ bị tấn công đánh cắp.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong mô hình Database Transaction (Giao dịch cơ sở dữ liệu), tính chất ACID gồm những đặc tính nào? Giải thích ngắn gọn ý nghĩa của tính Atomicity (Tính nguyên tử).
* **Đáp án mẫu:** - ACID gồm: Atomicity (Nguyên tử), Consistency (Nhất quán), Isolation (Cô lập), Durability (Bền vững).
  - Atomicity (Tính nguyên tử): Đảm bảo một chuỗi các thao tác trong một transaction phải được thực hiện trọn vẹn cùng nhau (All or Nothing). Nếu có bất kỳ một thao tác nào bị lỗi, toàn bộ transaction sẽ bị hủy bỏ (rollback) và dữ liệu quay về trạng thái ban đầu như chưa có chuyện gì xảy ra.