# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2) - Tập Đề Web Security Basics (4)

* **Role:** Backend Developer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Tấn công SQL Injection là gì? Trình bày cách sử dụng Parameterized Queries (Prepared Statements) để ngăn ngừa lỗ hổng này.
* **expected_key_points:**
  - id: KP1_1
    content: Bản chất tấn công SQL Injection
    keypoint_weight: 0.5
    description: Xảy ra khi kẻ tấn công chèn mã SQL độc hại vào các tham số đầu vào của ứng dụng rồi gửi lên server, đánh lừa DB thực thi câu lệnh ngoài ý muốn.
  - id: KP1_2
    content: Cơ chế phòng chống của Prepared Statements
    keypoint_weight: 0.5
    description: Tách biệt hoàn toàn phần câu lệnh SQL tĩnh và phần tham số truyền vào; DB biên dịch trước khung câu lệnh và coi các tham số chỉ là dữ liệu thuần túy.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích lỗ hổng XSS (Cross-Site Scripting). Backend Developer có thể làm gì ở lớp xử lý dữ liệu đầu vào và đầu ra để ngăn chặn nó?
* **expected_key_points:**
  - id: KP2_1
    content: Bản chất lỗ hổng XSS
    keypoint_weight: 0.5
    description: Kẻ tấn công chèn các script độc hại (chủ yếu là Javascript) vào ứng dụng để thực thi trên trình duyệt của người dùng khác.
  - id: KP2_2
    content: Biện pháp phòng chống ở Backend
    keypoint_weight: 0.5
    description: Lọc sạch dữ liệu đầu vào (Input Sanitization); thực hiện mã hóa ký tự đặc biệt ở đầu ra (HTML Entity Encoding) trước khi trả về client.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao việc sử dụng giao thức HTTPS là bắt buộc cho các ứng dụng web hiện nay? Giao thức này bảo vệ dữ liệu khỏi cuộc tấn công nào?
* **expected_key_points:**
  - id: KP3_1
    content: Vai trò của mã hóa TLS/SSL trong HTTPS
    keypoint_weight: 0.6
    description: HTTPS mã hóa toàn bộ dữ liệu truyền nhận giữa client và server sử dụng chứng chỉ số TLS/SSL, đảm bảo tính toàn vẹn và bảo mật dữ liệu trên đường truyền mạng.
  - id: KP3_2
    content: Chống tấn công nghe lén (Man-in-the-Middle)
    keypoint_weight: 0.4
    description: Ngăn chặn kẻ xấu trên mạng công cộng nghe lén (sniffing) hoặc thay đổi nội dung các gói tin (tampering), bảo vệ thông tin thẻ tín dụng, mật khẩu.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế tấn công CSRF (Cross-Site Request Forgery). Làm thế nào để phòng chống sử dụng CSRF Tokens và thuộc tính SameSite của Cookie?
* **expected_key_points:**
  - id: KP4_1
    content: Bản chất tấn công CSRF
    keypoint_weight: 0.5
    description: Kẻ tấn công lừa trình duyệt của nạn nhân tự động gửi một request độc hại đã được xác thực (qua cookie lưu sẵn) tới website mục tiêu mà nạn nhân không hề biết.
  - id: KP4_2
    content: Phòng chống bằng CSRF Token và SameSite Cookie
    keypoint_weight: 0.5
    description: Sử dụng CSRF Token ngẫu nhiên đính kèm trong body/header của mỗi request ghi; cấu hình thuộc tính `SameSite=Strict/Lax` trên cookie để ngăn trình duyệt tự động gửi cookie đi từ site khác.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh sự khác nhau về mức độ bảo mật và kịch bản áp dụng giữa các thuật toán băm (Hashing Algorithms): MD5, SHA-256, và bcrypt.
* **expected_key_points:**
  - id: KP5_1
    content: Đặc trưng MD5 và SHA-256
    keypoint_weight: 0.5
    description: MD5 đã lỗi thời, dễ bị đụng độ băm (collision). SHA-256 nhanh, an toàn cho kiểm tra tính toàn vẹn dữ liệu (checksum) nhưng không nên dùng cho mật khẩu vì quá nhanh, dễ bị brute-force.
  - id: KP5_2
    content: Đặc trưng của bcrypt
    keypoint_weight: 0.5
    description: Bcrypt là thuật toán băm mật khẩu chuyên dụng có cơ chế làm chậm tính toán (work factor) và tự động Salt, chống lại tấn công brute-force hiệu quả.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Làm thế nào để bảo vệ các endpoints API khỏi các cuộc tấn công dò quét mật khẩu (Brute Force) và Spam requests?
* **expected_key_points:**
  - id: KP6_1
    content: Giới hạn tần suất gọi API (Rate Limiting)
    keypoint_weight: 0.5
    description: Cấu hình Rate Limiting giới hạn tối đa số request một IP được gọi trong 1 phút (ví dụ sử dụng Redis Leaky Bucket).
  - id: KP6_2
    content: Cơ chế khóa tài khoản tạm thời (Account Lockout)
    keypoint_weight: 0.5
    description: Theo dõi số lần đăng nhập sai liên tiếp của một tài khoản; khóa tài khoản đó trong 15 phút hoặc yêu cầu CAPTCHA khi đạt ngưỡng tối đa.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cấu hình an toàn cho Cookie (Secure, HttpOnly, SameSite) để bảo vệ Session ID của người dùng khỏi bị đánh cắp qua tấn công XSS.
* **expected_key_points:**
  - id: KP7_1
    content: Vai trò của thuộc tính HttpOnly và Secure
    keypoint_weight: 0.6
    description: HttpOnly ngăn không cho mã Javascript truy cập cookie (chống XSS lấy cắp session). Secure yêu cầu cookie chỉ được gửi qua kết nối HTTPS mã hóa.
  - id: KP7_2
    content: Cấu hình SameSite cookie phù hợp
    keypoint_weight: 0.4
    description: Cấu hình `SameSite=Lax` hoặc `SameSite=Strict` để ngăn trình duyệt tự động gửi cookie trong các truy vấn chéo trang, tăng cường chống tấn công CSRF.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống mã hóa dữ liệu nhạy cảm của người dùng (như số thẻ tín dụng) trong cơ sở dữ liệu (Database Encryption) áp dụng chuẩn mã hóa đối xứng AES-256 kết hợp quản lý khóa an toàn.
* **expected_key_points:**
  - id: KP8_1
    content: Lựa chọn chế độ mã hóa AES (AES-GCM)
    keypoint_weight: 0.5
    description: Sử dụng mã hóa đối xứng AES với chế độ GCM (Galois/Counter Mode) để đảm bảo cả tính bảo mật và tính toàn vẹn (Authenticated Encryption), tạo IV ngẫu nhiên cho mỗi bản ghi.
  - id: KP8_2
    content: Chiến lược quản lý và lưu trữ Khóa bí mật (KMS)
    keypoint_weight: 0.5
    description: Không hardcode khóa mã hóa trong mã nguồn; sử dụng dịch vụ quản lý khóa ngoài chuyên dụng (AWS KMS, HashiCorp Vault) kết hợp phân quyền IAM chặt chẽ.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp phòng chống tấn công chèn ép tài nguyên (DDoS) và khai thác API ở lớp Backend ứng dụng, áp dụng kỹ thuật IP Whitelisting, WAF và API Gateway.
* **expected_key_points:**
  - id: KP9_1
    content: Vai trò của WAF và API Gateway
    keypoint_weight: 0.5
    description: Đặt WAF ở lớp biên để lọc các payload SQLi, XSS và phân tích gói tin độc hại; API Gateway thực hiện xác thực và Rate Limiting sớm trước khi chuyển tiếp request vào microservices.
  - id: KP9_2
    content: Cơ chế chặn IP động và Blacklisting
    keypoint_weight: 0.5
    description: Sử dụng các công cụ phân tích log (Fail2ban) để tự động phát hiện hành vi quét cổng, gửi requests tần suất bất thường để cập nhật tường lửa chặn IP tự động.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích rủi ro bảo mật của lỗ hổng IDOR (Insecure Direct Object Reference). Thiết kế giải pháp ngăn chặn IDOR triệt để tại tầng nghiệp vụ Backend.
* **expected_key_points:**
  - id: KP10_1
    content: Bản chất lỗ hổng IDOR
    keypoint_weight: 0.5
    description: Xảy ra khi ứng dụng cho phép người dùng truy cập trực tiếp tài nguyên của người khác chỉ bằng cách thay đổi ID trong URL hoặc body request mà không kiểm tra quyền sở hữu.
  - id: KP10_2
    content: Giải pháp phòng chống IDOR triệt để
    keypoint_weight: 0.5
    description: Bắt buộc kiểm tra quyền sở hữu (Access Control Checks) trong câu lệnh truy vấn DB: `WHERE resource_id = :id AND user_id = :current_user_id` thay vì chỉ truy vấn bằng resource_id đơn thuần.

