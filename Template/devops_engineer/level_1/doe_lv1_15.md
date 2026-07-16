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
    description: CI là quá trình tự động hóa việc build và chạy kiểm thử (unit test, integration test) mỗi khi có thay đổi mã nguồn, giúp phát hiện lỗi sớm.
  - id: KP1_2
    content: CD là đảm bảo mã nguồn luôn sẵn sàng triển khai
    keypoint_weight: 0.5
    description: CD mở rộng CI bằng cách đảm bảo các thay đổi code luôn được đóng gói và sẵn sàng để triển khai lên môi trường sản phẩm bất cứ lúc nào.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Container là gì? Giải thích lý do tại sao Container lại tối ưu hơn Virtual Machine (VM) về tài nguyên.
* **expected_key_points:**
  - id: KP2_1
    content: Container là đơn vị đóng gói ứng dụng
    keypoint_weight: 0.5
    description: Container đóng gói mã nguồn, thư viện và dependency vào một khối duy nhất, đảm bảo ứng dụng chạy đồng nhất trên mọi môi trường.
  - id: KP2_2
    content: Chia sẻ Kernel giúp tối ưu hóa tài nguyên
    keypoint_weight: 0.5
    description: Container dùng chung Kernel của máy chủ, nhẹ hơn nhiều so với VM (mỗi VM phải chạy một hệ điều hành riêng biệt), giúp khởi động nhanh và tốn ít RAM/CPU hơn.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Lệnh `git pull` trong Git thực hiện những thao tác gì? Tại sao cần xử lý xung đột (Conflict) khi dùng lệnh này?
* **expected_key_points:**
  - id: KP3_1
    content: `git pull` là sự kết hợp của `git fetch` và `git merge`
    keypoint_weight: 0.5
    description: `git pull` tải dữ liệu từ remote repository về (fetch) và ngay lập tức gộp vào nhánh local hiện tại (merge).
  - id: KP3_2
    content: Xung đột xảy ra do thay đổi cùng một vị trí
    keypoint_weight: 0.5
    description: Xung đột xảy ra khi dòng code ở local và remote cùng thay đổi tại một vị trí, yêu cầu người dùng phải can thiệp thủ công để đồng bộ nội dung.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Dockerfile là gì? Nêu 3 nguyên tắc tối ưu hóa Docker Image.
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa Dockerfile
    keypoint_weight: 0.3
    description: Dockerfile là tệp cấu hình chứa các lệnh để Docker tự động xây dựng Image theo từng tầng (layer).
  - id: KP4_2
    content: Tối ưu layer và kích thước image
    keypoint_weight: 0.4
    description: Sử dụng base image nhẹ (như Alpine), gộp lệnh `RUN` để giảm layer, xóa file rác sau khi cài đặt để tiết kiệm dung lượng.
  - id: KP4_3
    content: Bảo mật qua User context
    keypoint_weight: 0.3
    description: Sử dụng `USER` thay vì quyền root để hạn chế rủi ro bảo mật nếu container bị xâm nhập.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong Kubernetes, Pod là gì? Tại sao Deployment lại là lựa chọn tốt hơn so với việc tạo Pod đơn lẻ?
* **expected_key_points:**
  - id: KP5_1
    content: Pod là đơn vị triển khai nhỏ nhất
    keypoint_weight: 0.4
    description: Pod bao bọc các container dùng chung tài nguyên mạng và storage.
  - id: KP5_2
    content: Deployment cung cấp cơ chế tự phục hồi và scale
    keypoint_weight: 0.3
    description: Deployment giúp tự động khởi tạo lại Pod khi gặp sự cố và cho phép điều chỉnh số lượng bản sao.
  - id: KP5_3
    content: Pod đơn lẻ thiếu tính sẵn sàng (Availability)
    keypoint_weight: 0.3
    description: Nếu tạo Pod đơn lẻ, khi Node hoặc Pod chết, ứng dụng sẽ ngừng hoạt động vĩnh viễn, không đảm bảo uptime.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao trong hệ thống microservices quy mô lớn, mô hình giám sát Pull-based (như Prometheus) thường được ưu tiên hơn Push-based?
* **expected_key_points:**
  - id: KP6_1
    content: Kiểm soát tần suất chủ động (Pull)
    keypoint_weight: 0.5
    description: Server Pull nắm quyền quyết định khi nào lấy dữ liệu, tránh hiện tượng nghẽn server nếu hàng nghìn ứng dụng đồng loạt đẩy dữ liệu về cùng lúc.
  - id: KP6_2
    content: Phát hiện lỗi kết nối (Dead targets)
    keypoint_weight: 0.5
    description: Pull giúp Server phát hiện ngay lập tức các target bị sập, thay vì phải chờ đợi hoặc đoán xem target có đang gặp lỗi hay không.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Infrastructure as Code (IaC) là gì? Giải thích tính chất Idempotency trong IaC.
* **expected_key_points:**
  - id: KP7_1
    content: IaC dùng code để quản lý hạ tầng
    keypoint_weight: 0.4
    description: IaC định nghĩa hạ tầng thông qua mã nguồn, cho phép tự động hóa việc khởi tạo và quản lý tài nguyên.
  - id: KP7_2
    content: Idempotency đảm bảo tính ổn định
    keypoint_weight: 0.4
    description: Kết quả của cấu hình luôn nhất quán dù chạy bao nhiêu lần đi chăng nữa.
  - id: KP7_3
    content: Tránh thao tác trùng lặp/sai sót
    keypoint_weight: 0.2
    description: Nếu hạ tầng đã đúng cấu hình, công cụ sẽ tự động bỏ qua thay vì tạo mới hoặc gây lỗi.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Service Account trong Kubernetes là gì? Phân biệt với User Account.
* **expected_key_points:**
  - id: KP8_1
    content: Service Account cấp quyền cho ứng dụng (Machine identity)
    keypoint_weight: 0.5
    description: Service Account là danh tính cấp cho Pod để tương tác với Kubernetes API.
  - id: KP8_2
    content: User Account là danh tính cho con người
    keypoint_weight: 0.5
    description: User Account dành cho người dùng (admin, dev) quản lý bởi hệ thống ngoài, Kubernetes không lưu trữ thông tin này.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hãy giải thích chiến lược Rolling Update trong Kubernetes. Làm thế nào để đạt được Zero Downtime?
* **expected_key_points:**
  - id: KP9_1
    content: Quá trình xoay vòng Pod
    keypoint_weight: 0.5
    description: Thay thế dần các Pod cũ bằng Pod mới, đảm bảo số lượng Pod luôn đủ yêu cầu trong suốt quá trình.
  - id: KP9_2
    content: Vai trò của Readiness Probe
    keypoint_weight: 0.5
    description: Kiểm tra Pod đã sẵn sàng phục vụ chưa, giúp tránh việc gửi traffic vào Pod đang khởi động (tránh lỗi 502/503).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao không nên lưu Secret trong Git? Cách tiếp cận an toàn hơn là gì?
* **expected_key_points:**
  - id: KP10_1
    content: Rủi ro lộ lọt từ lịch sử commit
    keypoint_weight: 0.5
    description: Lịch sử Git lưu trữ dữ liệu vĩnh viễn, Secret bị lộ sẽ tồn tại mãi trong lịch sử repo.
  - id: KP10_2
    content: Quản lý Secret tập trung
    keypoint_weight: 0.5
    description: Sử dụng Secret Manager tập trung (như Vault), nhúng secret vào Pod thông qua biến môi trường tại runtime thay vì lưu trong code hoặc image.