# Bộ Câu Hỏi Phỏng Vấn Web Developer (Level 1)

* **Role:** Web Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong HTML, thuộc tính `alt` của thẻ `<img>` có vai trò gì và tại sao nó lại quan trọng?
* **Đáp án mẫu:** Thuộc tính `alt` cung cấp đoạn văn bản thay thế hiển thị khi hình ảnh bị lỗi không tải được, giúp các trình đọc màn hình (Screen Reader) hỗ trợ người khiếm thị hiểu được nội dung ảnh, đồng thời tối ưu hóa SEO cho website.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Sự khác biệt cốt lõi giữa hai phương thức HTTP: GET và POST là gì?
* **Đáp án mẫu:** GET dùng để gửi yêu cầu lấy dữ liệu từ máy chủ, tham số được đính kèm trực tiếp trên URL nên bị giới hạn độ dài và không bảo mật. POST dùng để gửi dữ liệu lên máy chủ để xử lý/tạo mới, dữ liệu nằm trong phần thân (Body) của request nên an toàn hơn và không giới hạn dung lượng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS Box Model, hãy phân biệt ý nghĩa của hai thuộc tính `margin` và `padding`.
* **Đáp án mẫu:** `padding` là khoảng không gian đệm nằm giữa nội dung (content) và phần viền (border) của chính phần tử đó. `margin` là khoảng cách không gian trống bên ngoài phần viền, dùng để tạo khoảng cách giữa phần tử này với các phần tử khác xung quanh.

---

## CÂU HỎI TRUNG BÌNH (4 câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong JavaScript, sự khác biệt giữa các từ khóa khai báo biến `var`, `let` và `const` là gì?
* **Đáp án mẫu:** `var` có phạm vi hàm (function scope) và hỗ trợ hoisting đầy đủ. `let` và `const` có phạm vi khối (block scope), không thể khai báo lại trong cùng một phạm vi; trong đó biến khai báo bằng `const` bắt buộc phải gán giá trị ngay và không thể gán lại giá trị mới (read-only).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Nguyên lý hoạt động của kỹ thuật Responsive Web Design (RWD) là gì và thuộc tính CSS nào đóng vai trò cốt lõi để hiện thực hóa nó?
* **Đáp án mẫu:** Nguyên lý là tự động thay đổi bố cục, kích thước giao diện trang web sao cho hiển thị tối ưu trên mọi kích thước màn hình (Desktop, Tablet, Mobile). Thuộc tính CSS cốt lõi để hiện thực hóa là `@media` rule (Media Queries) kết hợp với các hệ thống lưới linh hoạt (Flexbox/Grid).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Khái niệm "DOM" (Document Object Model) trong lập trình web là gì và JavaScript tương tác với DOM như thế nào?
* **Đáp án mẫu:** DOM là một giao diện lập trình ứng dụng (API), biểu diễn toàn bộ cấu trúc của một tài liệu HTML dưới dạng một cây phân cấp các đối tượng (Object Tree). JavaScript sử dụng các phương thức của DOM API (như `querySelector`, `addEventListener`) để truy cập, thay đổi nội dung, cấu trúc, định dạng CSS hoặc lắng nghe các sự kiện từ người dùng.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trạng thái bất đồng bộ (Asynchronous) trong JavaScript là gì? Hãy nêu 2 cách phổ biến để xử lý lập trình bất đồng bộ hiện nay.
* **Đáp án mẫu:** Là cơ chế cho phép các tác vụ tốn thời gian (như gọi API, đọc file) chạy ngầm mà không làm chặn (block) việc thực thi các dòng code tiếp theo của chương trình. Hai cách xử lý phổ biến là dùng `Promise` (.then/.catch) và cú pháp `async/await`.

---

## CÂU HỎI KHÓ (3 câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Chính sách Same-Origin Policy (SOP) trên trình duyệt là gì và cơ chế CORS (Cross-Origin Resource Sharing) giải quyết vấn đề này như thế nào?
* **Đáp án mẫu:** SOP là cơ chế bảo mật của trình duyệt, ngăn chặn một trang web gửi request đến một domain khác (khác giao thức, host, hoặc port) với domain gốc. CORS là một cơ chế dựa trên các HTTP Header bổ sung, cho phép máy chủ chỉ định rõ ràng những domain ngoại bang nào được phép truy cập vào tài nguyên của mình một cách an toàn.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Kỹ thuật Lazy Loading hình ảnh giúp tối ưu hóa hiệu năng tải trang (Web Performance) như thế nào? Cơ chế hoạt động của nó dựa trên thuộc tính nào trong HTML hiện đại?
* **Đáp án mẫu:** Lazy Loading trì hoãn việc tải các hình ảnh nằm ngoài vùng nhìn thấy (Viewport) của người dùng cho đến khi họ cuộn trang đến gần vị trí của ảnh đó, giúp giảm băng thông và tăng tốc độ tải trang ban đầu. Trong HTML hiện đại, cơ chế này được kích hoạt trực tiếp bằng thuộc tính `loading="lazy"` trên thẻ `<img>`.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Để bảo vệ một website khỏi lỗ hổng bảo mật XSS (Cross-Site Scripting), lập trình viên cần xử lý dữ liệu đầu vào từ người dùng (User Input) và dữ liệu đầu ra như thế nào?
* **Đáp án mẫu:** - Đầu vào: Phải tiến hành kiểm tra (Validation) và làm sạch dữ liệu (Sanitization) để loại bỏ các ký tự hoặc thẻ nguy hiểm.
  - Đầu ra: Phải thực hiện mã hóa ký tự (Output Encoding/Escaping) các ký tự đặc biệt (như `<`, `>`, `&`, `"`) thành mã HTML Entities tương ứng trước khi hiển thị lên trình duyệt để ngăn chặn việc thực thi mã script độc hại.