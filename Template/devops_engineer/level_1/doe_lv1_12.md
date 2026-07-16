# Bộ Câu Hỏi Phỏng Vấn DevOps Engineer (Level 1)

* **Role:** DevOps Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong quy trình CI/CD, hãy giải thích sự khác biệt giữa Continuous Integration (CI) và Continuous Delivery (CD). Tại sao việc tự động hóa kiểm thử (Automated Testing) lại là thành phần không thể thiếu của CI?
* **expected_key_points:**
  - id: KP1_1
    content: Mục tiêu của CI là tích hợp và phát hiện lỗi sớm
    keypoint_weight: 0.5
    description: CI tập trung vào việc tự động build và chạy các bài kiểm thử ngay khi mã nguồn được đẩy lên hệ thống, nhằm phát hiện sớm xung đột hoặc lỗi logic.
  - id: KP1_2
    content: CD là đảm bảo mã nguồn luôn sẵn sàng để triển khai
    keypoint_weight: 0.5
    description: CD đảm bảo các thay đổi code sau khi vượt qua CI được tự động đóng gói và sẵn sàng để triển khai lên môi trường đích (staging/production) bất cứ lúc nào.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Container là gì? Hãy so sánh ngắn gọn hiệu năng giữa Container và Virtual Machine (VM).
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm Container là đơn vị đóng gói ứng dụng và thư viện
    keypoint_weight: 0.5
    description: Container đóng gói code và tất cả các dependency của ứng dụng vào một khối duy nhất, đảm bảo tính nhất quán trên mọi môi trường.
  - id: KP2_2
    content: Chia sẻ Kernel giúp Container tối ưu hơn VM
    keypoint_weight: 0.5
    description: Container chia sẻ Kernel của Host OS, giúp khởi động gần như tức thì và tốn ít tài nguyên hơn so với VM (yêu cầu mỗi VM chạy một hệ điều hành riêng biệt).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Lệnh `git pull` thực hiện những hành động nào trong Git? Khi nào thì xảy ra xung đột (Conflict)?
* **expected_key_points:**
  - id: KP3_1
    content: Sự kết hợp của fetch và merge
    keypoint_weight: 0.5
    description: `git pull` là sự kết hợp của `git fetch` (tải data từ remote) và `git merge` (gộp data vào local branch).
  - id: KP3_2
    content: Xung đột khi sửa cùng một đoạn mã
    keypoint_weight: 0.5
    description: Xung đột xảy ra khi remote và local cùng chỉnh sửa nội dung trên cùng một dòng hoặc khối mã, cần xử lý thủ công để đồng nhất trước khi hoàn tất commit.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Dockerfile là gì? Nêu 3 nguyên tắc (Best Practices) để tối ưu hóa Docker Image.
* **expected_key_points:**
  - id: KP4_1
    content: Dockerfile là script định nghĩa cấu trúc của Image
    keypoint_weight: 0.3
    description: Dockerfile chứa các chỉ dẫn để Docker tự động xây dựng Image theo từng layer.
  - id: KP4_2
    content: Tối ưu dung lượng bằng cách gộp câu lệnh và dùng image nhẹ
    keypoint_weight: 0.4
    description: Sử dụng image cơ sở nhỏ (như Alpine), gộp các lệnh RUN để giảm số lượng layer, và loại bỏ các file rác sau khi cài đặt.
  - id: KP4_3
    content: Bảo mật qua nguyên tắc Least Privilege
    keypoint_weight: 0.3
    description: Không chạy container dưới quyền root, luôn chỉ định `USER` để giảm rủi ro tấn công.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Pod là gì trong Kubernetes? Tại sao nên sử dụng Deployment thay vì tạo Pod thủ công?
* **expected_key_points:**
  - id: KP5_1
    content: Pod là đơn vị nhỏ nhất trong Kubernetes
    keypoint_weight: 0.4
    description: Pod bao bọc một hoặc nhiều container chia sẻ chung không gian mạng và storage.
  - id: KP5_2
    content: Deployment quản lý tự phục hồi và scale
    keypoint_weight: 0.3
    description: Deployment đảm bảo Pod được tự khởi tạo lại khi chết (self-healing) và hỗ trợ tự động mở rộng (scaling).
  - id: KP5_3
    content: Pod thủ công thiếu tính sẵn sàng cao
    keypoint_weight: 0.3
    description: Tạo Pod thủ công sẽ bị mất vĩnh viễn nếu node hoặc pod gặp sự cố, không đáp ứng yêu cầu uptime cho hệ thống production.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh mô hình giám sát Pull-based (Prometheus) và Push-based. Tại sao Pull-based lại được ưa chuộng trong hệ thống microservices?
* **expected_key_points:**
  - id: KP6_1
    content: Pull cào dữ liệu, Push đẩy dữ liệu
    keypoint_weight: 0.5
    description: Pull-based chủ động cào dữ liệu định kỳ từ target. Push-based là target chủ động gửi về server.
  - id: KP6_2
    content: Pull giúp giám sát sức khỏe target tốt hơn
    keypoint_weight: 0.5
    description: Pull giúp server biết ngay target nào đang chết (không cào được), tránh bị quá tải server nhận dữ liệu như mô hình Push.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Infrastructure as Code (IaC) là gì? Giải thích tính chất Idempotency.
* **expected_key_points:**
  - id: KP7_1
    content: IaC dùng mã để quản lý hạ tầng
    keypoint_weight: 0.4
    description: IaC là việc định nghĩa hạ tầng bằng code (như HCL của Terraform) thay vì thao tác tay trên giao diện web.
  - id: KP7_2
    content: Idempotency đảm bảo trạng thái ổn định
    keypoint_weight: 0.4
    description: Chạy code cấu hình bao nhiêu lần thì kết quả cuối vẫn như nhau.
  - id: KP7_3
    content: Tránh trùng lặp tài nguyên
    keypoint_weight: 0.2
    description: Nếu tài nguyên đã tồn tại, công cụ sẽ không tạo mới hoặc gây lỗi, mà sẽ bỏ qua.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Service Account trong Kubernetes là gì? Phân biệt nó với User Account.
* **expected_key_points:**
  - id: KP8_1
    content: Service Account dành cho máy (Pod)
    keypoint_weight: 0.5
    description: Service Account là danh tính cấp cho Pod để tương tác với API Server của K8s.
  - id: KP8_2
    content: User Account dành cho con người
    keypoint_weight: 0.5
    description: User Account dùng cho admin/developer để truy cập cluster, thường quản lý bằng hệ thống ngoài (OIDC, LDAP), K8s không lưu trữ User Account dưới dạng tài nguyên nội bộ.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích chiến lược Rolling Update trong Kubernetes. Làm thế nào để đạt được Zero Downtime?
* **expected_key_points:**
  - id: KP9_1
    content: Xoay vòng Pod dần dần
    keypoint_weight: 0.5
    description: Rolling Update tạo Pod mới, chờ sẵn sàng rồi mới xóa Pod cũ, đảm bảo tổng Pod luôn đáp ứng yêu cầu.
  - id: KP9_2
    content: Readiness Probe là chìa khóa
    keypoint_weight: 0.5
    description: Readiness Probe kiểm tra app đã start hoàn toàn chưa, tránh đẩy traffic vào Pod chưa sẵn sàng gây lỗi 502/503.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao không nên lưu Secret trong Git? Cách quản lý Secret an toàn trong Pipeline?
* **expected_key_points:**
  - id: KP10_1
    content: Rủi ro lộ lọt secret từ lịch sử Git
    keypoint_weight: 0.5
    description: Git lưu lịch sử vĩnh viễn, secret trong git sẽ bị lộ khi có người có quyền truy cập repo hoặc repo bị leak.
  - id: KP10_2
    content: Sử dụng Secret Manager tập trung
    keypoint_weight: 0.5
    description: Dùng HashiCorp Vault hoặc Cloud Secret Manager, inject secret vào Pod qua runtime/env, không lưu cứng trên disk của image.