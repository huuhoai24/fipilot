# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2) - Tập Đề Authentication và Authorization (3)

* **Role:** Backend Developer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh sự khác nhau cơ bản giữa cơ chế xác thực dựa trên Session (Session-based) và dựa trên Token (Token-based như JWT).
* **expected_key_points:**
  - id: KP1_1
    content: Xác thực Session-based (Stateful)
    keypoint_weight: 0.5
    description: Session ID được lưu trong cookie của client; server phải lưu thông tin session trong bộ nhớ (RAM/Redis/DB) để kiểm tra ở mỗi request.
  - id: KP1_2
    content: Xác thực Token-based (Stateless)
    keypoint_weight: 0.5
    description: Server ký số và gửi JWT cho client lưu. JWT chứa sẵn thông tin user (claims) nên server chỉ cần xác thực chữ ký mà không cần truy vấn session store.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** JWT (JSON Web Token) cấu thành từ những phần nào? Giải thích vai trò của từng phần.
* **expected_key_points:**
  - id: KP2_1
    content: Ba phần cấu thành của JWT
    keypoint_weight: 0.6
    description: Gồm 3 phần phân tách bằng dấu chấm: Header (chứa thuật toán mã hóa), Payload (chứa dữ liệu người dùng/claims), và Signature (chữ ký số bảo mật).
  - id: KP2_2
    content: Cơ chế bảo mật chữ ký (Signature)
    keypoint_weight: 0.4
    description: Chữ ký được tạo bằng cách băm Header + Payload kết hợp với một khóa bí mật (Secret Key) ở server, ngăn chặn việc sửa đổi dữ liệu payload ở phía client.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa hai khái niệm: Authentication (Xác thực) và Authorization (Phân quyền). Cho ví dụ thực tế.
* **expected_key_points:**
  - id: KP3_1
    content: Định nghĩa Authentication vs Authorization
    keypoint_weight: 0.6
    description: Authentication xác nhận danh tính người dùng là ai (qua login, password, OTP). Authorization xác định người dùng đó có quyền thực hiện hành động gì.
  - id: KP3_2
    content: Ví dụ thực tế dễ hiểu
    keypoint_weight: 0.4
    description: Đăng nhập thành công vào app là Authentication; kiểm tra chỉ tài khoản Admin mới được xóa bài viết là Authorization.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế giải pháp phân quyền người dùng theo vai trò (Role-Based Access Control - RBAC) trong cơ sở dữ liệu quan hệ cho một ứng dụng có nhiều chức năng phức tạp.
* **expected_key_points:**
  - id: KP4_1
    content: Mô hình quan hệ RBAC trong CSDL
    keypoint_weight: 0.5
    description: Thiết kế 3 bảng chính: Users, Roles, Permissions và 2 bảng trung gian biểu diễn quan hệ nhiều-nhiều: User_Roles và Role_Permissions.
  - id: KP4_2
    content: Luồng kiểm tra quyền truy cập
    keypoint_weight: 0.5
    description: Khi user gọi API, query lấy danh sách Permissions của các Roles thuộc về User đó, đối chiếu với quyền yêu cầu của endpoint để cho phép/từ chối.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao không nên lưu trữ mật khẩu dưới dạng văn bản rõ (plain text)? Trình bày cơ chế hoạt động và vai trò của kỹ thuật Salt trong việc băm mật khẩu.
* **expected_key_points:**
  - id: KP5_1
    content: Nguy cơ lộ mật khẩu và băm mật khẩu
    keypoint_weight: 0.5
    description: Tránh lộ mật khẩu khi DB bị hack. Dùng các thuật toán băm (bcrypt, argon2) để mã hóa mật khẩu một chiều không thể dịch ngược.
  - id: KP5_2
    content: Cơ chế và vai trò của Salt
    keypoint_weight: 0.5
    description: Salt là một chuỗi ký tự ngẫu nhiên được sinh ra và cộng thêm vào mật khẩu trước khi băm, giúp chống lại các cuộc tấn công tra cứu bảng băm chuẩn bị sẵn (Rainbow Tables).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích luồng Authorization Code Flow trong giao thức OAuth2. Luồng này thường được sử dụng trong kịch bản nào?
* **expected_key_points:**
  - id: KP6_1
    content: Các bước của Authorization Code Flow
    keypoint_weight: 0.6
    description: Client hướng user đến Authorization Server -> User đồng ý cấp quyền -> Server trả về Authorization Code -> Client gửi Code kèm Client Secret lên Server để đổi lấy Access Token.
  - id: KP6_2
    content: Kịch bản sử dụng thực tế
    keypoint_weight: 0.4
    description: Sử dụng cho các ứng dụng web truyền thống có máy chủ backend bảo mật để giữ Client Secret an toàn khi tích hợp login mạng xã hội (Google, Facebook).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích vai trò của Access Token và Refresh Token. Tại sao phải thiết lập thời gian hết hạn (TTL) của Access Token ngắn và Refresh Token dài?
* **expected_key_points:**
  - id: KP7_1
    content: Vai trò của cặp Access và Refresh Token
    keypoint_weight: 0.6
    description: Access Token dùng để xác thực các request tài nguyên thông thường. Refresh Token dùng để lấy Access Token mới khi nó hết hạn mà không bắt user login lại.
  - id: KP7_2
    content: Tối ưu hóa thời gian hết hạn bảo mật
    keypoint_weight: 0.4
    description: Access Token ngắn (ví dụ 15 phút) giảm thiểu thiệt hại nếu token bị đánh cắp. Refresh Token dài (ví dụ 30 ngày) được lưu trữ an toàn hơn ở client.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế cơ chế xoay vòng Refresh Token (Refresh Token Rotation) nhằm phát hiện và ngăn chặn kẻ tấn công sử dụng Refresh Token bị rò rỉ để giả mạo người dùng.
* **expected_key_points:**
  - id: KP8_1
    content: Cơ chế xoay vòng Refresh Token
    keypoint_weight: 0.5
    description: Mỗi lần client dùng Refresh Token cũ để lấy Access Token mới, server lập tức hủy bỏ Refresh Token cũ và trả về một cặp Access/Refresh Token mới hoàn toàn.
  - id: KP8_2
    content: Phát hiện tấn công dùng lại Token cũ (Replay detection)
    keypoint_weight: 0.5
    description: Nếu nhận được Refresh Token đã từng bị thu hồi -> lập tức coi là vụ rò rỉ bảo mật -> hủy bỏ toàn bộ phiên làm việc của user đó trên mọi thiết bị và yêu cầu login lại.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp vô hiệu hóa JWT (Token Revocation) trước khi hết hạn (ví dụ khi người dùng đăng xuất hoặc đổi mật khẩu) trong một hệ thống phân tán.
* **expected_key_points:**
  - id: KP9_1
    content: Vấn đề vô hiệu hóa JWT stateless
    keypoint_weight: 0.4
    description: JWT mặc định không thể thu hồi từ xa vì server không giữ trạng thái. Cần thiết kế giải pháp thu hồi hiệu quả.
  - id: KP9_2
    content: Giải pháp sử dụng Redis Blacklist
    keypoint_weight: 0.6
    description: Lưu các token bị vô hiệu hóa (hoặc ID của token `jti`) vào Redis kèm thời gian hết hạn của chính token đó; khi kiểm tra request, đối chiếu nhanh với Redis Blacklist để từ chối.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống đăng nhập một lần (Single Sign-On - SSO) sử dụng chuẩn SAML hoặc OpenID Connect (OIDC) cho hệ sinh thái gồm nhiều website chạy độc lập của doanh nghiệp.
* **expected_key_points:**
  - id: KP10_1
    content: Vai trò của Identity Provider (IdP) tập trung
    keypoint_weight: 0.5
    description: Thiết lập một Identity Server trung tâm quản lý tài khoản người dùng, phát hành ID Tokens và Access Tokens cho các dịch vụ thành viên.
  - id: KP10_2
    content: Liên kết và đồng bộ trạng thái đăng nhập
    keypoint_weight: 0.5
    description: Các website thành viên tích hợp thư viện OIDC client để chuyển hướng xác thực và sử dụng cookies dùng chung ở cổng con hoặc chia sẻ session qua domain mẹ.

