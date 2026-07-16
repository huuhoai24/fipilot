# Bộ Câu Hỏi Phỏng Vấn DevOps Engineer (Level 1)

* **Role:** DevOps Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong quy trình CI/CD, hãy giải thích sự khác biệt cơ bản giữa Continuous Integration (CI) và Continuous Delivery (CD). Tại sao việc tự động hóa kiểm thử (Automated Testing) lại là thành phần không thể thiếu của CI?
* **expected_key_points:**
  - id: KP1_1
    content: Mục tiêu của CI là tích hợp và phát hiện lỗi sớm
    keypoint_weight: 0.5
    description: CI tập trung vào việc tự động build và chạy các bài kiểm thử (unit test, integration test) mỗi khi có code mới được đẩy lên hệ thống, nhằm phát hiện sớm xung đột hoặc lỗi logic.
  - id: KP1_2
    content: CD là đảm bảo mã nguồn luôn sẵn sàng để triển khai
    keypoint_weight: 0.5
    description: CD mở rộng CI bằng cách tự động hóa khâu đóng gói (artifact creation) và triển khai lên môi trường đích, đảm bảo mã nguồn luôn ở trạng thái sẵn sàng để phát hành.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Container là gì? Tại sao Container lại được coi là giải pháp thay thế hiệu quả cho Virtual Machine (VM) trong việc triển khai ứng dụng hiện đại?
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm Container là đơn vị đóng gói ứng dụng và thư viện
    keypoint_weight: 0.5
    description: Container đóng gói code và tất cả các dependency của ứng dụng vào một khối duy nhất, đảm bảo tính nhất quán trên mọi môi trường.
  - id: KP2_2
    content: Sự khác biệt về kiến trúc (Chia sẻ Kernel) giúp tối ưu hiệu năng
    keypoint_weight: 0.5
    description: Khác với VM yêu cầu mỗi máy ảo chạy một hệ điều hành riêng biệt, Container chia sẻ chung Kernel của máy chủ, giúp khởi động nhanh hơn, chiếm ít bộ nhớ và tài nguyên hơn đáng kể.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong Git, lệnh `git pull` thực hiện những thao tác nào? Tại sao chúng ta cần lưu ý đến xung đột (Conflict) khi sử dụng lệnh này?
* **expected_key_points:**
  - id: KP3_1
    content: Sự kết hợp của fetch và merge
    keypoint_weight: 0.5
    description: `git pull` là sự kết hợp của `git fetch` (tải dữ liệu từ remote về) và `git merge` (gộp dữ liệu đó vào nhánh hiện tại).
  - id: KP3_2
    content: Xung đột xảy ra khi cùng chỉnh sửa một đoạn code
    keypoint_weight: 0.5
    description: Xung đột xảy ra khi mã nguồn trên remote và local cùng sửa đổi tại một vị trí (dòng code). Cần phải xử lý thủ công bằng cách chọn nội dung muốn giữ lại trước khi commit tiếp.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Dockerfile là gì? Hãy liệt kê các nguyên tắc (Best Practices) để tối ưu hóa Docker Image.
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa Dockerfile là tập lệnh cấu hình Image
    keypoint_weight: 0.3
    description: Dockerfile là một file văn bản chứa danh sách các chỉ dẫn mà Docker sử dụng để xây dựng một image tự động theo từng layer.
  - id: KP4_2
    content: Tối ưu dung lượng bằng cách gộp câu lệnh và dùng image nhẹ
    keypoint_weight: 0.4
    description: Sử dụng các image cơ sở nhỏ gọn (như Alpine), gộp các câu lệnh `RUN` để giảm số lượng layer, và dọn dẹp bộ đệm tạm thời ngay trong tầng đó.
  - id: KP4_3
    content: Bảo mật qua nguyên tắc Least Privilege
    keypoint_weight: 0.3
    description: Không chạy container dưới quyền `root`, hãy tạo và sử dụng `USER` chuyên dụng để tăng tính bảo mật.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong Kubernetes, Pod là gì? Tại sao trong thực tế chúng ta ít khi tạo Pod trực tiếp mà lại thông qua các controller như Deployment?
* **expected_key_points:**
  - id: KP5_1
    content: Pod là đơn vị nhỏ nhất, chứa 1 hoặc nhiều container
    keypoint_weight: 0.4
    description: Pod là thực thể nhỏ nhất trong Kubernetes, đóng vai trò là môi trường bao bọc các container chia sẻ chung không gian mạng và storage.
  - id: KP5_2
    content: Vai trò của Deployment trong quản lý vòng đời
    keypoint_weight: 0.3
    description: Deployment cung cấp khả năng tự phục hồi, quản lý phiên bản (Rollout/Rollback) và mở rộng số lượng (Scaling) một cách tự động.
  - id: KP5_3
    content: Pod đơn lẻ không có tính sẵn sàng cao
    keypoint_weight: 0.3
    description: Tạo Pod đơn lẻ khi Pod chết sẽ mất hoàn toàn, không có cơ chế tự khởi tạo lại, do đó không đáp ứng được yêu cầu về độ sẵn sàng (Availability) cho ứng dụng production.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Hệ thống giám sát (Monitoring) như Prometheus hoạt động theo mô hình Pull-based. Tại sao cơ chế Pull lại hiệu quả hơn Push trong một hệ thống lớn với hàng nghìn microservices?
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế Pull chủ động kiểm soát tài nguyên
    keypoint_weight: 0.5
    description: Prometheus chủ động cào dữ liệu định kỳ từ các target. Server nắm quyền kiểm soát tần suất, giúp tránh tình trạng hệ thống giám sát bị quá tải nếu các ứng dụng đồng loạt gửi dữ liệu về.
  - id: KP6_2
    content: Khả năng phát hiện service chết
    keypoint_weight: 0.5
    description: Với mô hình Pull, nếu không kết nối được đến target, hệ thống có thể ngay lập tức đánh dấu target đó là "DOWN" và cảnh báo, thay vì phải đoán xem dữ liệu có bị nghẽn mạng hay không như mô hình Push.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Infrastructure as Code (IaC) là gì? Giải thích khái niệm Idempotency trong IaC.
* **expected_key_points:**
  - id: KP7_1
    content: IaC định nghĩa hạ tầng bằng mã thay vì thủ công
    keypoint_weight: 0.4
    description: IaC là việc sử dụng các file mã nguồn để khai báo, cấp phát và quản lý hạ tầng thay vì thao tác tay trên giao diện web.
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
    description: Service Account là thực thể được Kubernetes cấp cho các Pod để thực hiện các tác vụ với API của cluster.
  - id: KP8_2
    content: Phân biệt đối tượng quản lý
    keypoint_weight: 0.5
    description: User Account dành cho người dùng (admin, developer) để truy cập cụm, trong khi Service Account dành cho máy (ứng dụng) để tương tác với cụm.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hãy giải thích chiến lược Rolling Update trong Kubernetes. Làm thế nào để đảm bảo hệ thống không bị gián đoạn (Zero Downtime) trong quá trình cập nhật?
* **expected_key_points:**
  - id: KP9_1
    content: Quá trình xoay vòng Pod mới và xóa Pod cũ
    keypoint_weight: 0.5
    description: Rolling Update tạo Pod mới dần dần, đợi Pod mới sẵn sàng rồi mới xóa Pod cũ, đảm bảo tổng số lượng Pod luôn ở mức yêu cầu.
  - id: KP9_2
    content: Vai trò sống còn của Readiness Probe
    keypoint_weight: 0.5
    description: Phải có `readinessProbe` để Kubernetes biết khi nào ứng dụng trong Pod đã khởi động xong hoàn toàn, tránh việc trỏ traffic vào Pod chưa sẵn sàng gây lỗi cho người dùng.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao không nên lưu Secret trong Git? Cách quản lý Secret an toàn trong Pipeline?
* **expected_key_points:**
  - id: KP10_1
    content: Rủi ro lộ lọt từ lịch sử Git
    keypoint_weight: 0.5
    description: Git lưu lịch sử vĩnh viễn, secret trong git sẽ bị lộ khi có người truy cập repo hoặc repo bị leak.
  - id: KP10_2
    content: Sử dụng Secret Manager tập trung
    keypoint_weight: 0.5
    description: Dùng các công cụ chuyên biệt (Vault, AWS Secrets Manager), inject secret vào Pod ở runtime/env, không lưu cứng trên disk.