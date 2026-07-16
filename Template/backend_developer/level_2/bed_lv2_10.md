# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2) - Tập Đề Testing và Code Quality (10)

* **Role:** Backend Developer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Unit Test là gì? Giải thích vai trò của Unit Test trong quy trình phát triển và kiểm soát lỗi của sản phẩm phần mềm Backend.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa Unit Test
    keypoint_weight: 0.5
    description: Là việc kiểm thử một đơn vị mã nguồn nhỏ nhất độc lập (thường là một hàm hoặc một phương thức đơn lẻ) để đảm bảo nó trả về kết quả đúng với mọi đầu vào.
  - id: KP1_2
    content: Vai trò trong kiểm soát chất lượng
    keypoint_weight: 0.5
    description: Giúp phát hiện lỗi sớm ngay từ khi viết code; tạo sự tự tin khi refactor mã nguồn mà không sợ làm hỏng các tính năng cũ đang chạy ổn định.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa Unit Test (Kiểm thử đơn vị) và Integration Test (Kiểm thử tích hợp). Cho ví dụ thực tế.
* **expected_key_points:**
  - id: KP2_1
    content: Bản chất Unit Test vs Integration Test
    keypoint_weight: 0.6
    description: Unit Test kiểm thử độc lập hàm nghiệp vụ, giả lập (mock) toàn bộ I/O. Integration Test kiểm thử sự kết hợp thực tế giữa các module, bao gồm cả gọi DB thực tế hoặc kết nối mạng.
  - id: KP2_2
    content: Ví dụ thực tế rõ ràng
    keypoint_weight: 0.4
    description: Test thuật toán tính chiết khấu là Unit Test; Test gọi API đăng ký user ghi thực tế xuống MySQL và gửi email thật là Integration Test.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Mocking trong Unit Test là gì? Tại sao chúng ta cần Mocking khi viết Unit Test cho tầng nghiệp vụ (Business Logic)?
* **expected_key_points:**
  - id: KP3_1
    content: Khái niệm Mocking
    keypoint_weight: 0.5
    description: Là việc tạo ra các đối tượng giả lập (mocks) thay thế cho các đối tượng thật, cho phép ta định nghĩa trước hành vi và giá trị trả về của chúng.
  - id: KP3_2
    content: Lý do cần Mocking ở tầng nghiệp vụ
    keypoint_weight: 0.5
    description: Để cô lập hoàn toàn lớp nghiệp vụ khỏi các yếu tố bên ngoài không ổn định như Database, mạng internet, API bên thứ ba, đảm bảo tốc độ chạy test nhanh nhất.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm Độ bao phủ mã nguồn (Code Coverage). Một dự án Backend có độ bao phủ kiểm thử 100% có đồng nghĩa với việc không còn lỗi hay không?
* **expected_key_points:**
  - id: KP4_1
    content: Ý nghĩa chỉ số Code Coverage
    keypoint_weight: 0.5
    description: Là tỷ lệ phần trăm số dòng code, nhánh logic (branch coverage) được thực thi trong quá trình chạy toàn bộ các bài kiểm thử tự động.
  - id: KP4_2
    content: Giới hạn của Code Coverage 100%
    keypoint_weight: 0.5
    description: Không đồng nghĩa không có lỗi. Code coverage chỉ đo số dòng chạy qua, không đảm bảo logic thuật toán đúng, không bao phủ hết các edge cases hoặc lỗi dữ liệu đầu vào.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày quy trình phát triển hướng kiểm thử Test-Driven Development (TDD) gồm các bước Red - Green - Refactor.
* **expected_key_points:**
  - id: KP5_1
    content: Các bước Red - Green - Refactor
    keypoint_weight: 0.6
    description: Red: viết 1 unit test cho tính năng chưa phát triển (test chạy lỗi). Green: viết mã nguồn tối thiểu vừa đủ để test đó chạy thành công. Refactor: tối ưu hóa mã nguồn đảm bảo test vẫn xanh.
  - id: KP5_2
    content: Lợi ích của quy trình TDD
    keypoint_weight: 0.4
    description: Giúp lập trình viên tập trung vào đặc tả nghiệp vụ trước; thiết kế mã nguồn modular sạch sẽ hơn và luôn có bộ test đi kèm.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Làm thế nào để viết Unit Test cho một hàm xử lý bất đồng bộ (Asynchronous Function) sử dụng Promise/async-await trong Javascript hoặc Spring CompletableFuture?
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế đợi hàm bất đồng bộ trong Test Framework
    keypoint_weight: 0.5
    description: Sử dụng từ khóa `await` trong hàm test hoặc gọi hàm callback `done()` để báo cho test framework biết cần đợi cho đến khi tác vụ bất đồng bộ hoàn thành.
  - id: KP6_2
    content: Xử lý kiểm thử lỗi bất đồng bộ
    keypoint_weight: 0.5
    description: Sử dụng cấu trúc `try-catch` trong test hoặc assert các trường hợp reject/exception trả về từ Promise/Future để kiểm tra tính đúng đắn.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm CI/CD (Continuous Integration / Continuous Delivery). Việc tích hợp Unit Test vào CI/CD mang lại lợi ích gì?
* **expected_key_points:**
  - id: KP7_1
    content: Khái niệm CI/CD cơ bản
    keypoint_weight: 0.5
    description: CI là tự động hóa tích hợp và build code mới. CD là tự động hóa kiểm thử và triển khai mã nguồn lên môi trường staging/production.
  - id: KP7_2
    content: Vai trò của Unit Test trong CI/CD pipeline
    keypoint_weight: 0.5
    description: Khi lập trình viên đẩy code lên Git, pipeline tự động chạy toàn bộ bộ tests; nếu có bất kỳ test nào lỗi -> chặn không cho merge/deploy, đảm bảo tính ổn định tối đa cho nhánh chính.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp Integration Testing (Kiểm thử tích hợp) cho một ứng dụng Backend sử dụng Docker Testcontainers để dựng và xóa tự động cơ sở dữ liệu PostgreSQL thật trong quá trình chạy tests.
* **expected_key_points:**
  - id: KP8_1
    content: Cơ chế hoạt động của Testcontainers
    keypoint_weight: 0.5
    description: Khi khởi chạy bộ test, thư viện tự động tải và khởi động container PostgreSQL từ Docker Hub; cấu hình ứng dụng backend kết nối trực tiếp vào DB container này.
  - id: KP8_2
    content: Đảm bảo tính độc lập dữ liệu giữa các tests
    keypoint_weight: 0.5
    description: Sử dụng các scripts migration (Flyway/Liquibase) để khởi tạo cấu trúc bảng trước mỗi test; dọn sạch dữ liệu (clean database) sau mỗi phương thức test để tránh ảnh hưởng chéo.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản viết Unit Test cho một Service nghiệp vụ phức tạp đòi hỏi phải mock cả Database Repository và dịch vụ API bên thứ ba (ví dụ Stripe Payment API) trong Spring Boot/Node.js.
* **expected_key_points:**
  - id: KP9_1
    content: Mocking Database Repository
    keypoint_weight: 0.5
    description: Sử dụng Mockito hoặc Jest Mock để giả lập database: khi gọi hàm `findById(1)` -> trả về ngay một thực thể DTO được dựng sẵn trong code test.
  - id: KP9_2
    content: Gi giả lập Stripe API Client
    keypoint_weight: 0.5
    description: Sử dụng mock HTTP client (như Nock hoặc MockWebServer) để đánh chặn các request gửi tới Stripe API; trả về mã thành công 200 kèm JSON thanh toán mẫu.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế quy trình tự động phân tích tĩnh mã nguồn (Static Code Analysis) tích hợp trong Git commits và CI Pipeline sử dụng SonarQube hoặc ESLint để kiểm soát chất lượng code của nhóm phát triển.
* **expected_key_points:**
  - id: KP10_1
    content: Cấu hình Linter và Husky Git Hooks
    keypoint_weight: 0.5
    description: Cấu hình ESLint/Checkstyle; sử dụng Husky gán sự kiện pre-commit tự động chạy linter định dạng code; từ chối commit nếu code vi phạm chuẩn định dạng hoặc chứa bug tiềm ẩn.
  - id: KP10_2
    content: Thiết lập Quality Gates trên SonarQube
    keypoint_weight: 0.5
    description: Tích hợp SonarQube quét code trong CI pipeline; thiết lập các chỉ số chặn (Quality Gates): độ bao phủ test > 80%, không chứa lỗi bảo mật nghiêm trọng (critical vulnerabilities), tỷ lệ trùng lặp code < 3%.

