# Bộ Câu Hỏi Phỏng Vấn Back-End Developer (Level 1)

* **Role:** Back-End Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác biệt cơ bản giữa Cơ sở dữ liệu quan hệ (Relational Database - RDBMS) và Cơ sở dữ liệu phi quan hệ (NoSQL).
* **Đáp án mẫu:** - RDBMS (như MySQL, PostgreSQL) lưu trữ dữ liệu dưới dạng các bảng (tables) có cấu trúc cố định, sử dụng các mối quan hệ (foreign keys) và truy vấn bằng SQL, tuân thủ tính chất ACID.
  - NoSQL (như MongoDB, Redis) lưu trữ dữ liệu linh hoạt không cần sơ đồ cố định (schema-less) dưới dạng document, key-value, hoặc graph, có khả năng mở rộng theo chiều ngang tốt hơn.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong kiến trúc RESTful API, ý nghĩa của các phương thức HTTP: GET, POST, PUT, DELETE là gì?
* **Đáp án mẫu:** - GET: Đọc/Lấy tài nguyên từ server.
  - POST: Tạo mới một tài nguyên trên server.
  - PUT: Cập nhật hoặc ghi đè toàn bộ một tài nguyên đã tồn tại.
  - DELETE: Xóa một tài nguyên khỏi server.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Khái niệm "Environment Variables" (Biến môi trường) trong phát triển Back-End dùng để làm gì? Cho ví dụ.
* **Đáp án mẫu:** Biến môi trường dùng để lưu trữ các cấu hình nhạy cảm hoặc các thông số thay đổi tùy theo môi trường chạy ứng dụng (Development, Staging, Production) mà không cần hardcode vào mã nguồn. Ví dụ: Chuỗi kết nối DB (Database URL), Secret Key, API Port.

---

## CÂU HỎI TRUNG BÌNH (4 câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Cơ chế xác thực sử dụng JSON Web Token (JWT) hoạt động như thế nào khi Client gửi request đến các API cần bảo mật?
* **Đáp án mẫu:** Sau khi login thành công, Server sinh ra một chuỗi mã hóa JWT và gửi về Client. Ở các request tiếp theo, Client đính kèm JWT này vào HTTP Header (thường là `Authorization: Bearer <token>`). Server chỉ cần giải mã và kiểm tra chữ ký của token đó để xác thực người dùng mà không cần truy vấn lại Database.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Điểm khác biệt cốt lõi giữa "Authentication" (Xác thực) và "Authorization" (Phân quyền) trong hệ thống Back-End là gì?
* **Đáp án mẫu:** - Authentication là quá trình xác minh danh tính của người dùng (Họ là ai? Ví dụ qua chức năng Đăng nhập bằng mật khẩu, OTP).
  - Authorization là quá trình kiểm tra xem người dùng đã được xác thực đó có quyền thực hiện một hành động cụ thể hay truy cập tài nguyên nào (Họ được phép làm gì? Ví dụ: Admin được xóa bài viết, Member chỉ được xem).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong thiết kế cơ sở dữ liệu quan hệ, mục đích của việc tạo Index (Chỉ mục) cho một cột là gì? Nó có nhược điểm gì không?
* **Đáp án mẫu:** - Mục đích: Giúp tăng tốc độ truy vấn, tìm kiếm và sắp xếp dữ liệu trên cột đó bằng cách tạo ra một cấu trúc dữ liệu tra cứu nhanh (như B-Tree).
  - Nhược điểm: Làm chậm các thao tác ghi dữ liệu (INSERT, UPDATE, DELETE) vì hệ thống phải cập nhật lại Index, đồng thời làm tiêu tốn thêm dung lượng bộ nhớ lưu trữ.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Khái niệm Middleware trong các Framework Back-End (như ExpressJS, NestJS, Spring Boot) đảm nhận vai trò gì?
* **Đáp án mẫu:** Middleware là các hàm trung gian nằm giữa request gửi từ Client và router handler cuối cùng trên Server. Nó được dùng để kiểm tra, xử lý trước dữ liệu request (như log thông tin hệ thống, parse dữ liệu, kiểm tra token đăng nhập) hoặc can thiệp vào response trước khi gửi về Client.

---

## CÂU HỎI KHÓ (3 câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Hiện tượng "N+1 Query" trong các thư viện ORM (Object-Relational Mapping) là gì và làm thế nào để khắc phục nó?
* **Đáp án mẫu:** - Khái niệm: Là lỗi hiệu năng xảy ra khi ORM thực hiện 1 câu lệnh SQL để lấy danh sách bản ghi chính, sau đó lại chạy thêm N câu lệnh SQL phụ để lấy dữ liệu liên quan của từng bản ghi đó.
  - Khắc phục: Thay vì tải dữ liệu lười (Lazy Loading), chuyển sang sử dụng kỹ thuật Eager Loading (sử dụng các lệnh `JOIN` hoặc `preload`/`include` tùy framework) để lấy toàn bộ dữ liệu cần thiết chỉ trong 1 hoặc vài câu truy vấn duy nhất.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Sự khác biệt về mặt kiến trúc và cơ chế giao tiếp giữa REST API và gRPC là gì?
* **Đáp án mẫu:** - REST API: Dựa trên kiến trúc HTTP/1.1, dữ liệu truyền nhận ở dạng văn bản (text) thường là JSON, giao tiếp dạng text-based nên tốn băng thông và chậm hơn.
  - gRPC: Dựa trên giao thức HTTP/2, dữ liệu được tuần tự hóa (serialize) sang dạng nhị phân (binary) sử dụng Protocol Buffers, hỗ trợ streaming hai chiều liên tục, hiệu năng cao và tiết kiệm băng thông hơn.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Khi hệ thống gặp hiện tượng thắt nút cổ chai tại Database do lượng truy cập đọc dữ liệu (Read) quá tải, bạn sẽ đề xuất giải pháp kiến trúc cơ bản nào để tối ưu?
* **Đáp án mẫu:** Có 2 giải pháp kiến trúc phổ biến:
  1. Sử dụng Caching Layer (như Redis/Memcached) phía trước DB để lưu trữ các kết quả truy vấn ít thay đổi nhưng được đọc thường xuyên, giảm tải trực tiếp cho DB.
  2. Áp dụng mô hình Database Replication (Master-Slave): Các thao tác ghi (Write) sẽ xử lý trên node Master, dữ liệu được đồng bộ xuống các node Slave và toàn bộ thao tác đọc (Read) sẽ được phân tải cho các node Slave xử lý.