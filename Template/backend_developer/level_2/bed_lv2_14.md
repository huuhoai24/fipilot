# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2) - Tập Đề API Integration và Error Handling (14)

* **Role:** Backend Developer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày cách triển khai cơ chế bắt lỗi tập trung (Global Exception Handling) trong ứng dụng Backend để tránh lộ thông tin nhạy cảm của hệ thống.
* **expected_key_points:**
  - id: KP1_1
    content: Ý nghĩa bắt lỗi tập trung
    keypoint_weight: 0.5
    description: Sử dụng một bộ lọc chung (như `@ControllerAdvice` trong Spring Boot hoặc Middleware bắt lỗi trong Express/NestJS) để bắt toàn bộ các lỗi phát sinh không mong muốn.
  - id: KP1_2
    content: Tránh lộ stack trace bảo mật
    keypoint_weight: 0.5
    description: Không trả về stack trace hệ thống hay mã lỗi raw DB cho client; ghi log chi tiết ở server và trả về client JSON lỗi thân thiện kèm mã code lỗi chung.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Làm thế nào để tích hợp và gọi một API của bên thứ ba (Third-party API) từ Backend ứng dụng? Nêu tên các thư viện/công cụ bạn thường dùng.
* **expected_key_points:**
  - id: KP2_1
    content: Cách tích hợp gọi API bên ngoài
    keypoint_weight: 0.6
    description: Sử dụng một HTTP Client để gửi request (GET, POST...) kèm theo các headers xác thực (Bearer Token, API Key) tới endpoint của bên thứ ba và parse JSON trả về.
  - id: KP2_2
    content: Các thư viện/công cụ phổ biến
    keypoint_weight: 0.4
    description: Axios (Node.js), RestTemplate/WebClient (Spring Boot), HTTP Client (Python Requests) hoặc Go HTTP package.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích khái niệm Validation dữ liệu đầu vào (Input Validation). Backend Developer nên kiểm tra những gì trước khi xử lý dữ liệu nghiệp vụ?
* **expected_key_points:**
  - id: KP3_1
    content: Mục đích Validation dữ liệu
    keypoint_weight: 0.5
    description: Đảm bảo dữ liệu nhận được từ client hợp lệ về định dạng, độ dài và kiểu dữ liệu trước khi thực hiện bất kỳ xử lý nghiệp vụ nào, giúp tránh lỗi hệ thống và tấn công SQLi/XSS.
  - id: KP3_2
    content: Các tiêu chí kiểm tra cơ bản
    keypoint_weight: 0.5
    description: Kiểm tra null/empty, độ dài chuỗi tối đa/tối thiểu, định dạng email/số điện thoại bằng biểu thức chính quy (Regex), kiểm tra dải giá trị của số.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao việc gọi API bên ngoài (Third-party API) song song trực tiếp trong luồng request chính của người dùng là rủi ro? Giải pháp khắc phục là gì?
* **expected_key_points:**
  - id: KP4_1
    content: Rủi ro nghẽn luồng và timeout
    keypoint_weight: 0.5
    description: Nếu API bên thứ ba bị chậm hoặc sập, luồng xử lý request chính của backend sẽ bị block chờ đợi, dẫn đến cạn kiệt thread pool và làm chậm toàn bộ hệ thống.
  - id: KP4_2
    content: Giải pháp xử lý bất đồng bộ và timeout
    keypoint_weight: 0.5
    description: Thiết lập cấu hình Connection Timeout và Read Timeout cực kỳ nghiêm ngặt; đối với tác vụ không cần kết quả ngay (như gửi email), đẩy vào hàng đợi bất đồng bộ xử lý nền.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế cơ chế tự động thử lại (Retry Mechanism) kết hợp Exponential Backoff khi gọi các API bên ngoài không ổn định.
* **expected_key_points:**
  - id: KP5_1
    content: Nguyên lý Exponential Backoff
    keypoint_weight: 0.5
    description: Khi gọi API lỗi, không retry ngay lập tức mà tăng dần thời gian chờ giữa các lần thử lại theo lũy thừa (ví dụ: lần 1 chờ 1s, lần 2 chờ 2s, lần 3 chờ 4s) để tránh làm nghẽn hệ thống đích.
  - id: KP5_2
    content: Giới hạn số lần thử lại và Fallback
    keypoint_weight: 0.5
    description: Thiết lập số lần thử lại tối đa (ví dụ 3 lần); nếu vẫn lỗi sau lần cuối, ghi log lỗi nghiêm trọng và chạy luồng fallback trả về lỗi mặc định thân thiện.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích vai trò của mẫu thiết kế Circuit Breaker khi tích hợp với các hệ thống Web Services bên thứ ba (như cổng thanh toán).
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế bảo vệ bằng Circuit Breaker
    keypoint_weight: 0.6
    description: Theo dõi tỷ lệ lỗi kết nối đến cổng thanh toán; nếu cổng thanh toán bị sập (tỷ lệ lỗi > 50%), Circuit Breaker tự động chuyển sang trạng thái Open để chặn đứng các request gửi lên cổng đó.
  - id: KP6_2
    content: Giảm thiểu lãng phí tài nguyên
    keypoint_weight: 0.4
    description: Giúp trả lỗi ngay lập tức cho client mà không mất thời gian gửi request vô ích qua mạng, giải phóng tài nguyên cho hệ thống backend xử lý việc khác.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Làm thế nào để ghi nhật ký lỗi (Error Logging) hiệu quả ở môi trường Production? Những thông tin nào bắt buộc phải có trong một dòng log lỗi?
* **expected_key_points:**
  - id: KP7_1
    content: Sử dụng Structured Logging và log levels
    keypoint_weight: 0.5
    description: Ghi log cấu trúc dạng JSON; phân biệt rõ các cấp độ log (ERROR cho lỗi hệ thống cần can thiệp, WARN cho cảnh báo, INFO cho thông tin luồng chạy).
  - id: KP7_2
    content: Thông tin bắt buộc trong log lỗi
    keypoint_weight: 0.5
    description: Mốc thời gian (timestamp), ID yêu cầu (Correlation ID), mô tả lỗi, ID người dùng liên quan, và Stack Trace chi tiết (chỉ ghi ở log file, không trả về client).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp giao dịch phân tán (Distributed Transaction) để xử lý hoàn tiền cho khách hàng qua Stripe API, đảm bảo nếu hệ thống của ta bị sập giữa chừng thì giao dịch hoàn tiền không bị mất mát hay thực hiện lặp.
* **expected_key_points:**
  - id: KP8_1
    content: Ghi nhận trạng thái PENDING và Outbox
    keypoint_weight: 0.5
    description: Khi nhận yêu cầu: tạo bản ghi hoàn tiền trong DB với trạng thái `PENDING`; ghi sự kiện yêu cầu hoàn tiền vào bảng outbox trong cùng 1 transaction DB.
  - id: KP8_2
    content: Worker xử lý lũy đẳng kết hợp Stripe Idempotency Key
    keypoint_weight: 0.5
    description: Worker đọc bảng outbox -> gọi Stripe API truyền kèm khóa `Stripe-Idempotency-Key` (bằng ID hoàn tiền của ta). Nếu gọi thành công -> cập nhật trạng thái DB thành `SUCCESS`. Nếu sập, chạy lại vẫn truyền key cũ giúp Stripe nhận diện tránh hoàn tiền 2 lần.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống Rate Limiting (Giới hạn tần suất gọi API) ở lớp API Gateway sử dụng thuật toán Token Bucket kết hợp bộ lưu trữ Redis phân tán.
* **expected_key_points:**
  - id: KP9_1
    content: Nguyên lý thuật toán Token Bucket
    keypoint_weight: 0.5
    description: Mỗi người dùng được cấp một chiếc xô chứa tối đa $B$ tokens; định kỳ tự động nạp $R$ tokens vào xô. Mỗi request tiêu thụ 1 token; nếu xô rỗng, từ chối request (HTTP 429).
  - id: KP9_2
    content: Triển khai an toàn với Redis Lua Script
    keypoint_weight: 0.5
    description: Lưu trữ số lượng token và mốc thời gian cập nhật gần nhất của từng user trong Redis. Viết câu lệnh Lua script chạy nguyên tử (atomic) trên Redis để kiểm tra và trừ token, tránh tranh chấp tài nguyên.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc Logging tập trung (Centralized Logging) cho hệ thống gồm 10 microservices, đảm bảo có thể truy vết dòng chảy của một request đi qua toàn bộ hệ thống bằng Correlation ID.
* **expected_key_points:**
  - id: KP10_1
    content: Tạo và truyền nhận Correlation ID
    keypoint_weight: 0.5
    description: API Gateway tự động sinh ra một mã UUID duy nhất (Correlation ID) cho mỗi request đầu vào; đính kèm mã này vào HTTP Header chuyển tiếp qua các microservices.
  - id: KP10_2
    content: Thu thập log và truy vấn tập trung
    keypoint_weight: 0.5
    description: Tất cả các microservices chèn Correlation ID vào từng dòng log. Log shipper (Filebeat) đẩy logs về Elasticsearch/Kibana; kỹ sư có thể tìm kiếm bằng Correlation ID để xem toàn bộ luồng đi của request.

