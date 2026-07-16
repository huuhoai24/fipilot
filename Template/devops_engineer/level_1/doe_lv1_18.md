# Bộ Câu Hỏi Phỏng Vấn DevOps Engineer (Level 1)

* **Role:** DevOps Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong quy trình CI/CD, hãy phân biệt sự khác biệt cơ bản giữa Continuous Integration (CI) và Continuous Delivery (CD). Tại sao tự động hóa kiểm thử lại là thành phần không thể thiếu của CI?
* **expected_key_points:**
  - id: KP1_1
    content: CI tập trung vào tích hợp và phát hiện lỗi sớm
    keypoint_weight: 0.5
    description: CI là quy trình tự động hóa việc build và chạy các bài kiểm thử (unit test, integration test) mỗi khi có thay đổi mã nguồn, giúp phát hiện sớm xung đột hoặc lỗi logic.
  - id: KP1_2
    content: CD là đảm bảo mã nguồn sẵn sàng triển khai
    keypoint_weight: 0.5
    description: CD mở rộng CI bằng cách tự động hóa khâu đóng gói (artifact) và đảm bảo mã nguồn luôn ở trạng thái sẵn sàng để phát hành lên môi trường đích bất cứ lúc nào.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Container là gì? Giải thích tại sao Container lại tối ưu hơn Virtual Machine (VM) về tài nguyên.
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm Container là đơn vị đóng gói ứng dụng
    keypoint_weight: 0.5
    description: Container đóng gói mã nguồn, thư viện và dependency vào một khối duy nhất, đảm bảo tính nhất quán trên mọi môi trường.
  - id: KP2_2
    content: Chia sẻ Kernel giúp tối ưu hiệu năng
    keypoint_weight: 0.5
    description: Container dùng chung Kernel của máy chủ, nhẹ hơn nhiều so với VM (mỗi VM chạy hệ điều hành riêng), giúp khởi động nhanh và tốn ít RAM/CPU hơn.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Lệnh `git pull` thực hiện những thao tác gì? Tại sao cần xử lý xung đột (Conflict) khi dùng lệnh này?
* **expected_key_points:**
  - id: KP3_1
    content: Sự kết hợp của fetch và merge
    keypoint_weight: 0.5
    description: `git pull` là sự kết hợp của `git fetch` (tải dữ liệu từ remote) và `git merge` (gộp dữ liệu vào nhánh hiện tại).
  - id: KP3_2
    content: Xung đột xảy ra khi cùng chỉnh sửa một đoạn code
    keypoint_weight: 0.5
    description: Xung đột xảy ra khi remote và local cùng sửa đổi tại một vị trí, yêu cầu người dùng phải xử lý thủ công trước khi commit tiếp.

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
    description: Sử dụng base image nhẹ (Alpine), gộp lệnh `RUN` để giảm số layer, xóa file tạm thời ngay trong tầng đó để tiết kiệm dung lượng.
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
    description: Pod bao bọc các container chia sẻ chung không gian mạng và storage.
  - id: KP5_2
    content: Deployment quản lý tự phục hồi và scale
    keypoint_weight: 0.3
    description: Deployment cung cấp khả năng tự phục hồi, quản lý phiên bản (Rollout/Rollback) và mở rộng số lượng (Scaling) tự động.
  - id: KP5_3
    content: Pod đơn lẻ thiếu tính sẵn sàng (Availability)
    keypoint_weight: 0.3
    description: Pod đơn lẻ không có cơ chế tự khởi tạo lại khi chết, không đáp ứng được yêu cầu uptime cho hệ thống production.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao hệ thống giám sát Pull-based (như Prometheus) thường hiệu quả hơn Push-based trong hệ thống microservices lớn?
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế Pull chủ động kiểm soát tài nguyên
    keypoint_weight: 0.5
    description: Server Pull nắm quyền quyết định tần suất cào dữ liệu, tránh nghẽn server nếu hàng nghìn ứng dụng cùng đẩy dữ liệu về một lúc (Push).
  - id: KP6_2
    content: Khả năng phát hiện service chết
    keypoint_weight: 0.5
    description: Pull giúp Server phát hiện ngay lập tức target bị sập (không cào được), thay vì phải đoán xem dữ liệu có bị nghẽn mạng như Push.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Infrastructure as Code (IaC) là gì? Giải thích khái niệm Idempotency trong IaC.
* **expected_key_points:**
  - id: KP7_1
    content: IaC dùng mã để quản lý hạ tầng
    keypoint_weight: 0.4
    description: IaC định nghĩa hạ tầng bằng mã nguồn (như Terraform) thay vì thao tác tay trên giao diện web.
  - id: KP7_2
    content: Idempotency là trạng thái cuối luôn đồng nhất
    keypoint_weight: 0.4
    description: Chạy code cấu hình bao nhiêu lần thì kết quả cuối cùng vẫn như nhau.
  - id: KP7_3
    content: Cơ chế bỏ qua nếu hạ tầng đã đúng
    keypoint_weight: 0.2
    description: Nếu tài nguyên đã tồn tại và đúng cấu hình, công cụ sẽ thực hiện kiểm tra và bỏ qua, không gây lỗi hay trùng lặp.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Service Account trong Kubernetes là gì? Phân biệt với User Account.
* **expected_key_points:**
  - id: KP8_1
    content: Service Account quản lý danh tính cho Pod
    keypoint_weight: 0.5
    description: Service Account cấp danh tính cho Pod để tương tác với Kubernetes API.
  - id: KP8_2
    content: User Account là danh tính cho con người
    keypoint_weight: 0.5
    description: User Account dành cho người dùng (admin, dev) quản lý bởi hệ thống ngoài, không lưu trữ trong Kubernetes.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích chiến lược Rolling Update trong Kubernetes. Làm thế nào để đạt được Zero Downtime?
* **expected_key_points:**
  - id: KP9_1
    content: Xoay vòng Pod dần dần
    keypoint_weight: 0.5
    description: Tạo Pod mới, đợi sẵn sàng rồi xóa Pod cũ, đảm bảo tổng Pod luôn đáp ứng yêu cầu.
  - id: KP9_2
    content: Readiness Probe giúp tránh lỗi traffic
    keypoint_weight: 0.5
    description: Sử dụng `readinessProbe` để biết khi nào ứng dụng sẵn sàng, tránh gửi traffic vào Pod chưa khởi động xong (tránh lỗi 502).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao không nên lưu Secret trong Git? Cách tiếp cận an toàn hơn là gì?
* **expected_key_points:**
  - id: KP10_1
    content: Rủi ro lộ lọt từ lịch sử Git
    keypoint_weight: 0.5
    description: Git lưu lịch sử vĩnh viễn, secret trong git sẽ bị lộ khi có người truy cập repo hoặc repo bị leak.
  - id: KP10_2
    content: Sử dụng Secret Manager tập trung
    keypoint_weight: 0.5
    description: Dùng dịch vụ chuyên biệt (Vault, AWS Secrets Manager), inject secret qua volume hoặc env tại runtime, không lưu cứng trên disk.