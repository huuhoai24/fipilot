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
    content: Mục tiêu của CI là phát hiện lỗi sớm qua kiểm thử tự động
    keypoint_weight: 0.5
    description: CI tập trung vào việc tự động build và chạy các bài kiểm thử (unit test, integration test) mỗi khi có code mới được đẩy lên repository, giúp phát hiện xung đột và lỗi logic ngay lập tức.
  - id: KP1_2
    content: Mục tiêu của CD là đảm bảo phần mềm luôn trong trạng thái sẵn sàng phát hành
    keypoint_weight: 0.5
    description: CD mở rộng CI bằng cách tự động hóa khâu đóng gói (artifact creation) và triển khai lên môi trường staging/production, đảm bảo mã nguồn luôn ở trạng thái sẵn sàng để phát hành bất cứ lúc nào.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Container là gì? Tại sao Container lại được coi là giải pháp thay thế hiệu quả cho Virtual Machine (VM) trong việc triển khai ứng dụng hiện đại?
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm Container là đơn vị đóng gói phần mềm kèm môi trường chạy
    keypoint_weight: 0.5
    description: Container là một đơn vị tiêu chuẩn chứa code ứng dụng cùng toàn bộ thư viện, dependency cần thiết để ứng dụng chạy ổn định trên bất kỳ môi trường nào.
  - id: KP2_2
    content: Sự khác biệt về kiến trúc (Chia sẻ Kernel) giúp tối ưu hiệu năng
    keypoint_weight: 0.5
    description: Khác với VM yêu cầu mỗi máy ảo chạy một hệ điều hành riêng, Container chia sẻ chung Kernel của máy chủ, giúp khởi động nhanh hơn, chiếm ít bộ nhớ và tài nguyên hơn đáng kể.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong Git, lệnh `git pull` thực hiện những thao tác nào? Tại sao chúng ta cần lưu ý đến xung đột (Conflict) khi sử dụng lệnh này?
* **expected_key_points:**
  - id: KP3_1
    content: Sự kết hợp của fetch và merge
    keypoint_weight: 0.5
    description: `git pull` là sự kết hợp của `git fetch` (tải dữ liệu từ remote về) và `git merge` (gộp dữ liệu đó vào nhánh hiện tại).
  - id: KP3_2
    content: Xung đột xảy ra khi cùng chỉnh sửa một dòng mã
    keypoint_weight: 0.5
    description: Xung đột xảy ra khi mã nguồn trên remote và local cùng sửa đổi tại một vị trí (dòng code). Cần phải xử lý thủ công bằng cách chọn nội dung muốn giữ lại trước khi commit tiếp.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Dockerfile là gì? Hãy liệt kê 3 Best Practices để tối ưu hóa Docker Image khi viết Dockerfile.
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa Dockerfile là tập lệnh cấu hình Image
    keypoint_weight: 0.3
    description: Dockerfile là một file văn bản chứa danh sách các chỉ dẫn (commands) mà Docker sử dụng để xây dựng một image tự động theo từng layer.
  - id: KP4_2
    content: Best Practices về giảm thiểu Layer và dung lượng
    keypoint_weight: 0.4
    description: Sử dụng các image cơ sở nhỏ gọn (như Alpine), hạn chế số lượng layer bằng cách gộp các câu lệnh `RUN`, và dọn dẹp bộ đệm tạm thời (như `rm -rf /var/lib/apt/lists/*`) ngay trong tầng đó.
  - id: KP4_3
    content: Best Practices về bảo mật (User context)
    keypoint_weight: 0.3
    description: Không chạy container dưới quyền `root`, hãy tạo và sử dụng `USER` chuyên dụng để tăng tính bảo mật cho container.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong Kubernetes, Pod là gì? Tại sao trong thực tế chúng ta ít khi tạo Pod trực tiếp mà lại thông qua các controller như Deployment?
* **expected_key_points:**
  - id: KP5_1
    content: Pod là đơn vị nhỏ nhất, chứa 1 hoặc nhiều container
    keypoint_weight: 0.4
    description: Pod là thực thể nhỏ nhất trong Kubernetes, đóng vai trò là môi trường bao bọc các container chia sẻ chung không gian mạng và storage.
  - id: KP5_2
    content: Vai trò của Deployment trong quản lý vòng đời (Scaling & Self-healing)
    keypoint_weight: 0.3
    description: Deployment cung cấp khả năng tự phục hồi (tự khởi tạo lại Pod nếu Pod cũ chết), quản lý phiên bản (Rollout/Rollback) và mở rộng số lượng (Scaling) một cách tự động.
  - id: KP5_3
    content: Pod đơn lẻ không có tính sẵn sàng cao
    keypoint_weight: 0.3
    description: Tạo Pod đơn lẻ khi Pod chết sẽ mất hoàn toàn, không có cơ chế tự khởi tạo lại, do đó không đáp ứng được yêu cầu về độ sẵn sàng (Availability) cho ứng dụng production.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Hệ thống giám sát (Monitoring) như Prometheus hoạt động theo mô hình Pull-based. Hãy giải thích tại sao cơ chế Pull lại hiệu quả hơn Push trong một hệ thống lớn với hàng nghìn microservices?
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế Pull chủ động kiểm soát tài nguyên
    keypoint_weight: 0.5
    description: Prometheus chủ động cào (scrape) dữ liệu từ các target. Server nắm quyền kiểm soát tần suất cào, giúp tránh tình trạng hệ thống giám sát bị quá tải nếu các ứng dụng đồng loạt gửi dữ liệu về (Push).
  - id: KP6_2
    content: Khả năng phát hiện service chết (Down detection)
    keypoint_weight: 0.5
    description: Với mô hình Pull, nếu không kết nối được đến target, Prometheus có thể ngay lập tức đánh dấu target đó là "DOWN" và gửi cảnh báo, trong khi mô hình Push khó phân biệt giữa việc ứng dụng chết hay mạng bị nghẽn.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Infrastructure as Code (IaC) là gì? Giải thích khái niệm Idempotency trong IaC bằng công cụ như Terraform.
* **expected_key_points:**
  - id: KP7_1
    content: IaC định nghĩa hạ tầng bằng mã thay vì thủ công
    keypoint_weight: 0.4
    description: IaC là việc sử dụng các file mã nguồn (như HCL của Terraform) để khai báo, cấp phát và quản lý hạ tầng phần cứng/mạng thay vì thao tác tay trên giao diện web.
  - id: KP7_2
    content: Idempotency là trạng thái cuối luôn đồng nhất dù chạy bao nhiêu lần
    keypoint_weight: 0.4
    description: Idempotency đảm bảo rằng dù chạy code cấu hình 1 lần hay 100 lần, trạng thái hạ tầng cuối cùng vẫn giống nhau.
  - id: KP7_3
    content: Cơ chế bỏ qua nếu hạ tầng đã đúng
    keypoint_weight: 0.2
    description: Nếu tài nguyên đã tồn tại và đúng cấu hình, công cụ sẽ thực hiện các bước kiểm tra và bỏ qua, không thực hiện lại các thao tác gây lỗi hoặc trùng lặp tài nguyên.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong Kubernetes, Service Account đóng vai trò gì trong bảo mật? Sự khác biệt giữa Service Account và User Account là gì?
* **expected_key_points:**
  - id: KP8_1
    content: Service Account quản lý danh tính cho Pod
    keypoint_weight: 0.5
    description: Service Account là thực thể được Kubernetes cấp cho các Pod để thực hiện các thao tác với API của cluster (ví dụ: một Pod đọc thông tin các Pod khác).
  - id: KP8_2
    content: Phân biệt đối tượng quản lý
    keypoint_weight: 0.5
    description: User Account là dành cho con người (admin, developer) để truy cập cụm, thường quản lý bởi hệ thống bên ngoài (như LDAP, OIDC). Service Account là dành cho máy (ứng dụng/pod) để tương tác với cụm.

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
    description: Phải có `readinessProbe` để Kubernetes biết khi nào ứng dụng trong Pod đã khởi động xong hoàn toàn, tránh việc trỏ traffic vào Pod chưa sẵn sàng gây ra lỗi 502/503.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong môi trường sản phẩm thực tế, việc quản lý "Secret" (mật khẩu, khóa API) là cực kỳ quan trọng. Tại sao không nên lưu trữ Secret trực tiếp trong Docker Image hoặc Git, và cách tiếp cận an toàn hơn là gì?
* **expected_key_points:**
  - id: KP10_1
    content: Rủi ro lộ lọt qua lịch sử Git hoặc Image layers
    keypoint_weight: 0.5
    description: Secret lưu trong Git sẽ tồn tại vĩnh viễn trong lịch sử commit. Secret trong Docker Image sẽ bị lộ khi Image được đẩy lên Registry công cộng hoặc người khác có quyền pull image.
  - id: KP10_2
    content: Giải pháp quản lý Secret tập trung (như Vault hoặc K8s Secrets)
    keypoint_weight: 0.5
    description: Sử dụng các dịch vụ quản lý bí mật (HashiCorp Vault, AWS Secret Manager) để mã hóa dữ liệu. Tại runtime, Secret được inject vào Pod dưới dạng volume hoặc biến môi trường mà không lưu cứng trên disk của Image.