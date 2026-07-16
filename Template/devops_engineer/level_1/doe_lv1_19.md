# Bộ Câu Hỏi Phỏng Vấn DevOps Engineer (Level 1)

* **Role:** DevOps Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong quy trình CI/CD, hãy phân biệt sự khác biệt cơ bản giữa Continuous Integration (CI) và Continuous Delivery (CD).
* **expected_key_points:**
  - id: KP1_1
    content: CI tập trung vào việc tự động hóa kiểm thử mã nguồn
    keypoint_weight: 0.5
    description: CI là quá trình tự động hóa việc build và chạy kiểm thử mỗi khi có thay đổi mã nguồn, giúp phát hiện lỗi sớm.
  - id: KP1_2
    content: CD là đảm bảo mã nguồn luôn sẵn sàng triển khai
    keypoint_weight: 0.5
    description: CD mở rộng CI bằng cách đảm bảo các thay đổi code luôn được đóng gói và sẵn sàng để triển khai lên môi trường đích bất cứ lúc nào.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Container là gì? Giải thích lý do tại sao Container lại tối ưu hơn Virtual Machine (VM) về tài nguyên.
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm Container là đơn vị đóng gói ứng dụng và thư viện
    keypoint_weight: 0.5
    description: Container đóng gói code và tất cả các dependency của ứng dụng vào một khối duy nhất, đảm bảo tính nhất quán trên mọi môi trường.
  - id: KP2_2
    content: Chia sẻ Kernel giúp tối ưu hiệu năng
    keypoint_weight: 0.5
    description: Container chia sẻ Kernel của máy chủ, nhẹ hơn nhiều so với VM (mỗi VM phải chạy một hệ điều hành riêng biệt), giúp khởi động nhanh và tốn ít tài nguyên hơn.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Lệnh `git pull` thực hiện những thao tác gì? Khi nào thì xảy ra xung đột (Conflict)?
* **expected_key_points:**
  - id: KP3_1
    content: Sự kết hợp của fetch và merge
    keypoint_weight: 0.5
    description: `git pull` là sự kết hợp của `git fetch` (tải dữ liệu từ remote về) và `git merge` (gộp dữ liệu đó vào nhánh hiện tại).
  - id: KP3_2
    content: Xung đột xảy ra khi cùng chỉnh sửa một đoạn code
    keypoint_weight: 0.5
    description: Xung đột xảy ra khi mã nguồn trên remote và local cùng sửa đổi tại một vị trí, yêu cầu người dùng phải xử lý thủ công trước khi commit tiếp.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Dockerfile là gì? Nêu 3 nguyên tắc (Best Practices) để tối ưu hóa Docker Image.
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa Dockerfile là tập lệnh cấu hình Image
    keypoint_weight: 0.3
    description: Dockerfile là tệp cấu hình chứa các lệnh để Docker tự động xây dựng Image theo từng layer.
  - id: KP4_2
    content: Tối ưu layer và kích thước image
    keypoint_weight: 0.4
    description: Sử dụng base image nhẹ (như Alpine), gộp lệnh `RUN` để giảm số lượng layer, và xóa các file tạm thời ngay trong tầng đó để tiết kiệm dung lượng.
  - id: KP4_3
    content: Bảo mật qua User context
    keypoint_weight: 0.3
    description: Sử dụng `USER` thay vì quyền root để hạn chế rủi ro bảo mật nếu container bị xâm nhập.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong Kubernetes, Pod là gì? Tại sao Deployment lại là lựa chọn tốt hơn so với việc tạo Pod đơn lẻ?
* **expected_key_points:**
  - id: KP5_1
    content: Pod là đơn vị nhỏ nhất, chứa 1 hoặc nhiều container
    keypoint_weight: 0.4
    description: Pod bao bọc một hoặc nhiều container chia sẻ chung không gian mạng và storage.
  - id: KP5_2
    content: Deployment quản lý tự phục hồi và scale
    keypoint_weight: 0.3
    description: Deployment cung cấp khả năng tự phục hồi (tự khởi tạo lại Pod nếu Pod cũ chết), quản lý phiên bản (Rollout/Rollback) và mở rộng số lượng (Scaling) một cách tự động.
  - id: KP5_3
    content: Pod đơn lẻ thiếu tính sẵn sàng cao
    keypoint_weight: 0.3
    description: Tạo Pod đơn lẻ khi Pod chết sẽ mất hoàn toàn, không có cơ chế tự khởi tạo lại, do đó không đáp ứng được yêu cầu về độ sẵn sàng (Availability) cho ứng dụng production.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Hệ thống giám sát (Monitoring) như Prometheus hoạt động theo mô hình Pull-based. Hãy giải thích tại sao cơ chế Pull lại hiệu quả hơn Push trong một hệ thống lớn với hàng nghìn microservices?
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế Pull chủ động kiểm soát tài nguyên
    keypoint_weight: 0.5
    description: Prometheus chủ động cào (scrape) dữ liệu từ các target. Server nắm quyền kiểm soát tần suất, giúp tránh tình trạng hệ thống giám sát bị quá tải nếu các ứng dụng đồng loạt gửi dữ liệu về.
  - id: KP6_2
    content: Khả năng phát hiện service chết (Down detection)
    keypoint_weight: 0.5
    description: Với mô hình Pull, nếu không kết nối được đến target, hệ thống có thể ngay lập tức đánh dấu target đó là "DOWN" và gửi cảnh báo, trong khi mô hình Push khó phân biệt giữa việc ứng dụng chết hay mạng bị nghẽn.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Infrastructure as Code (IaC) là gì? Giải thích khái niệm Idempotency trong IaC.
* **expected_key_points:**
  - id: KP7_1
    content: IaC dùng mã để quản lý hạ tầng
    keypoint_weight: 0.4
    description: IaC là việc sử dụng các file mã nguồn (như HCL của Terraform) để khai báo, cấp phát và quản lý hạ tầng thay vì thao tác tay trên giao diện web.
  - id: KP7_2
    content: Idempotency là trạng thái cuối luôn đồng nhất
    keypoint_weight: 0.4
    description: Chạy code cấu hình bao nhiêu lần thì kết quả cuối cùng vẫn như nhau.
  - id: KP7_3
    content: Cơ chế bỏ qua nếu hạ tầng đã đúng
    keypoint_weight: 0.2
    description: Nếu tài nguyên đã tồn tại và đúng cấu hình, công cụ sẽ thực hiện các bước kiểm tra và bỏ qua, không gây lỗi hoặc trùng lặp tài nguyên.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Service Account trong Kubernetes là gì? Phân biệt nó với User Account.
* **expected_key_points:**
  - id: KP8_1
    content: Service Account quản lý danh tính cho Pod
    keypoint_weight: 0.5
    description: Service Account là thực thể được Kubernetes cấp cho các Pod để thực hiện các thao tác với API của cluster (ví dụ: một Pod đọc thông tin các Pod khác).
  - id: KP8_2
    content: Phân biệt đối tượng quản lý
    keypoint_weight: 0.5
    description: User Account là dành cho con người (admin, developer) để truy cập cụm, thường quản lý bởi hệ thống bên ngoài. Service Account là dành cho máy (ứng dụng/pod) để tương tác với cụm.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hãy giải thích chiến lược Rolling Update trong Kubernetes. Làm thế nào để đảm bảo hệ thống không bị gián đoạn (Zero Downtime) trong quá trình cập nhật phiên bản mới?
* **expected_key_points:**
  - id: KP9_1
    content: Quá trình xoay vòng Pod mới và xóa Pod cũ
    keypoint_weight: 0.5
    description: Rolling Update tạo Pod mới dần dần, đợi Pod mới sẵn sàng (Ready) rồi mới xóa Pod cũ, đảm bảo tổng số lượng Pod luôn ở mức yêu cầu.
  - id: KP9_2
    content: Vai trò sống còn của Readiness Probe
    keypoint_weight: 0.5
    description: Phải có `readinessProbe` để Kubernetes biết khi nào ứng dụng trong Pod đã khởi động xong hoàn toàn, tránh việc trỏ traffic vào Pod chưa sẵn sàng gây ra lỗi.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong môi trường sản phẩm thực tế, việc quản lý "Secret" (mật khẩu, khóa API) là cực kỳ quan trọng. Tại sao không nên lưu trữ Secret trực tiếp trong Docker Image hoặc Git, và cách tiếp cận an toàn hơn là gì?
* **expected_key_points:**
  - id: KP10_1
    content: Rủi ro lộ lọt qua lịch sử Git hoặc Image layers
    keypoint_weight: 0.5
    description: Secret lưu trong Git sẽ tồn tại vĩnh viễn trong lịch sử commit. Secret trong Docker Image sẽ bị lộ khi Image được đẩy lên Registry công cộng hoặc người khác có quyền pull image.
  - id: KP10_2
    content: Giải pháp quản lý Secret tập trung
    keypoint_weight: 0.5
    description: Sử dụng các dịch vụ quản lý bí mật (HashiCorp Vault, AWS Secret Manager) để mã hóa dữ liệu. Tại runtime, Secret được inject vào Pod dưới dạng volume hoặc biến môi trường mà không lưu cứng trên disk của Image.