# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1) - Tập Đề Hệ Thống và Công Nghệ (69)

* **Role:** Tester
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Khi thực hiện kiểm thử API, các mã trạng thái (HTTP Status Codes) thuộc nhóm 2xx, 4xx, và 5xx thể hiện điều gì? Cho ví dụ cụ thể về một mã lỗi phổ biến trong nhóm 4xx và 5xx.
* **expected_key_points:**
  - id: KP1_1
    content: Phân nhóm mã trạng thái HTTP
    keypoint_weight: 0.5
    description: Ý nghĩa của các nhóm mã trạng thái (2xx: Thành công/Success; 4xx: Lỗi phía Client/Client Error; 5xx: Lỗi phía Server/Server Error).
  - id: KP1_2
    content: Ví dụ cụ thể lỗi 4xx và 5xx
    keypoint_weight: 0.5
    description: Chỉ ra được các mã lỗi thực tế như 400 Bad Request, 401 Unauthorized, 403 Forbidden hoặc 404 Not Found (đối với 4xx) và 500 Internal Server Error, 502 Bad Gateway hoặc 503 Service Unavailable (đối với 5xx).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Làm thế nào một Tester có thể sử dụng Chrome DevTools (F12) để hỗ trợ việc kiểm thử và tìm kiếm nguyên nhân lỗi của một ứng dụng web?
* **expected_key_points:**
  - id: KP2_1
    content: Sử dụng Console Tab
    keypoint_weight: 0.5
    description: Dùng để kiểm tra các lỗi JavaScript (Uncaught Errors), log cảnh báo hoặc in thử dữ liệu kiểm tra hành vi client-side.
  - id: KP2_2
    content: Sử dụng Network Tab
    keypoint_weight: 0.5
    description: Dùng để theo dõi các API requests gửi đi, responses nhận về (payload dữ liệu), HTTP status code và kiểm tra xem lỗi xuất phát từ frontend hay backend.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích kỹ thuật phân vùng tương đương (Equivalence Partitioning) và cho ví dụ minh họa cách áp dụng kỹ thuật này cho một ô nhập liệu tuổi từ 18 đến 60.
* **expected_key_points:**
  - id: KP3_1
    content: Định nghĩa phân vùng tương đương
    keypoint_weight: 0.6
    description: Là kỹ thuật kiểm thử hộp đen chia tập hợp dữ liệu đầu vào thành các phân vùng hợp lệ và không hợp lệ, với giả định rằng tất cả các giá trị trong cùng một phân vùng sẽ cho kết quả xử lý như nhau.
  - id: KP3_2
    content: Thiết kế các phân vùng thực tế
    keypoint_weight: 0.4
    description: Thiết lập các phân vùng cụ thể: Phân vùng hợp lệ (từ 18 đến 60, ví dụ: 25); Phân vùng không hợp lệ nhỏ hơn biên dưới (nhỏ hơn 18, ví dụ: 15); Phân vùng không hợp lệ lớn hơn biên trên (lớn hơn 60, ví dụ: 65); Phân vùng không hợp lệ về định dạng (để trống, nhập chữ, ký tự đặc biệt).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao Tester cần thực hiện kiểm thử cơ sở dữ liệu (Database Testing) thay vì chỉ kiểm thử trên giao diện người dùng (UI)? Hãy nêu 3 câu lệnh SQL cơ bản thường dùng nhất.
* **expected_key_points:**
  - id: KP4_1
    content: Lý do kiểm thử Database
    keypoint_weight: 0.6
    description: UI có thể che giấu lỗi hoặc validate thiếu, kiểm thử DB giúp đảm bảo tính toàn vẹn dữ liệu, kiểm tra dữ liệu lưu xuống đúng bảng/cột, tránh mất mát dữ liệu hoặc lỗi đồng bộ giữa các hệ thống.
  - id: KP4_2
    content: Câu lệnh SQL cơ bản
    keypoint_weight: 0.4
    description: Nêu rõ ít nhất 3 câu lệnh như SELECT (truy vấn), INSERT (thêm dữ liệu test), UPDATE (cập nhật trạng thái), DELETE (xóa dữ liệu test) hoặc WHERE (lọc điều kiện kiểm tra).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong kiểm thử tích hợp (Integration Testing), hai khái niệm `Stub` và `Driver` được sử dụng như thế nào? Hãy phân biệt mục đích sử dụng của chúng.
* **expected_key_points:**
  - id: KP5_1
    content: Định nghĩa và vai trò của Stub
    keypoint_weight: 0.5
    description: Stub là một module giả lập được gọi bởi module đang được kiểm thử. Nó thay thế cho các module cấp dưới chưa được phát triển (thường dùng trong phương pháp tiếp cận Top-Down).
  - id: KP5_2
    content: Định nghĩa và vai trò của Driver
    keypoint_weight: 0.5
    description: Driver là một module giả lập dùng để gọi module đang được kiểm thử. Nó thay thế cho các module cấp trên chưa được phát triển (thường dùng trong phương pháp tiếp cận Bottom-Up).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy phân biệt sự khác nhau giữa `Load Testing` (Kiểm thử tải) và `Stress Testing` (Kiểm thử độ chịu tải/áp lực). Mục tiêu chính của mỗi loại là gì?
* **expected_key_points:**
  - id: KP6_1
    content: Bản chất Load Testing
    keypoint_weight: 0.5
    description: Đo lường và đánh giá hiệu năng hệ thống dưới mức tải bình thường và mức tải dự kiến cao nhất để đảm bảo hệ thống đáp ứng được SLA (Service Level Agreement).
  - id: KP6_2
    content: Bản chất Stress Testing
    keypoint_weight: 0.5
    description: Đánh giá khả năng hoạt động của hệ thống ở các mức tải cực hạn vượt quá giới hạn thiết kế nhằm tìm ra điểm gãy (breaking point) và xem hệ thống phục hồi ra sao khi tải giảm.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi phát hiện một lỗi giao diện chỉ xảy ra trên trình duyệt Safari nhưng không xảy ra trên Chrome hay Firefox, bạn sẽ xử lý và báo cáo lỗi này như thế nào?
* **expected_key_points:**
  - id: KP7_1
    content: Cô lập và xác minh lỗi môi trường
    keypoint_weight: 0.5
    description: Kiểm tra cụ thể phiên bản trình duyệt Safari, phiên bản hệ điều hành (macOS/iOS), thiết bị test và chụp ảnh/quay video minh họa rõ ràng lỗi chỉ xảy ra trên môi trường đó.
  - id: KP7_2
    content: Thu thập thông tin kỹ thuật đặc thù
    keypoint_weight: 0.5
    description: Dùng Web Inspector của Safari để kiểm tra xem có lỗi console JavaScript nào riêng biệt hay lỗi không tương thích CSS (ví dụ: các thuộc tính prefixed -webkit-) và đính kèm vào bug report.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Một tính năng cập nhật thông tin cá nhân của người dùng được thông báo cập nhật thành công ở database, nhưng trên giao diện vẫn hiển thị thông tin cũ. Hãy phân tích các nguyên nhân tiềm ẩn liên quan đến hệ thống lưu trữ đệm (Caching) và đề xuất cách kiểm chứng.
* **expected_key_points:**
  - id: KP8_1
    content: Phân tích các tầng Caching
    keypoint_weight: 0.6
    description: Lỗi có thể do Browser Cache (trình duyệt lưu phiên bản tĩnh cũ), API Gateway/Server Cache (server không xóa/không refresh cache sau khi ghi nhận thay đổi), hoặc CDN Cache (nếu thông tin đi qua CDN và chưa hết thời gian cache).
  - id: KP8_2
    content: Đề xuất phương pháp kiểm chứng
    keypoint_weight: 0.4
    description: Thực hiện kiểm chứng bằng cách: Sử dụng chế độ ẩn danh (Incognito) hoặc Hard Reload (Ctrl+F5) để bypass browser cache; Gọi trực tiếp API lấy thông tin qua các công cụ như Postman để kiểm tra xem API trả về data cũ hay mới.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Làm thế nào một Tester có thể thực hiện kiểm thử bảo mật thủ công cơ bản đối với hai lỗ hổng SQL Injection và Cross-Site Scripting (XSS) trên các ô nhập liệu của ứng dụng web?
* **expected_key_points:**
  - id: KP9_1
    content: Cách test SQL Injection thủ công
    keypoint_weight: 0.5
    description: Nhập các chuỗi ký tự đặc biệt SQL (ví dụ: `' OR '1'='1`, `'; DROP TABLE...`) vào các trường nhập liệu (như ô Username, ô Search) để xem hệ thống có báo lỗi cú pháp DB lộ thông tin, hoặc bypass cơ chế đăng nhập mà không cần password hợp lệ hay không.
  - id: KP9_2
    content: Cách test XSS thủ công
    keypoint_weight: 0.5
    description: Nhập các đoạn mã script (ví dụ: `<script>alert('XSS')</script>`, `<img src=x onerror=alert(1)>`) vào các trường lưu trữ thông tin hiển thị lên giao diện để xem trình duyệt có thực thi script đó và bật hộp thoại cảnh báo hay không.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Làm thế nào để bạn xử lý và điều tra một lỗi nghiêm trọng xảy ra ngẫu nhiên (chỉ xuất hiện khoảng 1 trên 10 lần thực hiện) và không có các bước tái hiện ổn định?
* **expected_key_points:**
  - id: KP10_1
    content: Thu thập logs và phân tích ngữ cảnh hệ thống
    keypoint_weight: 0.4
    description: Kiểm tra log hệ thống (Server logs, DB logs, Console logs, Network traffic) tại thời điểm xảy ra lỗi để tìm kiếm thông điệp lỗi (exception/error message).
  - id: KP10_2
    content: Phân tích các yếu tố tác động ngẫu nhiên
    keypoint_weight: 0.4
    description: Xem xét các yếu tố biến đổi như: trạng thái dữ liệu nền, xung đột tiến trình (race condition), độ trễ mạng, hoặc phiên làm việc đồng thời của tài khoản khác.
  - id: KP10_3
    content: Quy trình báo cáo và theo dõi
    keypoint_weight: 0.2
    description: Vẫn tạo bug report, đánh dấu trạng thái "Ngẫu nhiên/Không ổn định (Intermittent/Flaky)", mô tả chi tiết tần suất xuất hiện, đính kèm mọi logs thu thập được và phối hợp cùng Developer để tái hiện lỗi trong môi trường debug.
