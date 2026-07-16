# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2) - Tập Đề Basic Cloud và Deployment (15)

* **Role:** Backend Developer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Docker là gì? Giải thích vai trò của Docker Container trong việc đồng nhất môi trường phát triển và môi trường chạy Production.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa Docker và Container
    keypoint_weight: 0.5
    description: Docker là nền tảng ảo hóa ở cấp độ hệ điều hành; cho phép đóng gói ứng dụng cùng toàn bộ thư viện, cấu hình phụ thuộc vào một Container độc lập gọn nhẹ.
  - id: KP1_2
    content: Đảm bảo tính đồng nhất môi trường
    keypoint_weight: 0.5
    description: Giúp loại bỏ hoàn toàn lỗi kinh điển 'chạy trên máy tôi nhưng không chạy trên server' vì container chứa sẵn hệ điều hành thu nhỏ và các dependencies giống hệt nhau.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau về bản chất và mục đích sử dụng giữa hai file cấu hình: `Dockerfile` và `docker-compose.yml`.
* **expected_key_points:**
  - id: KP2_1
    content: Mục đích của Dockerfile
    keypoint_weight: 0.5
    description: Chứa các chỉ thị tuần tự (FROM, RUN, COPY, CMD) để xây dựng (build) nên một Docker Image đơn lẻ cho một ứng dụng cụ thể.
  - id: KP2_2
    content: Mục đích của docker-compose.yml
    keypoint_weight: 0.5
    description: Là file cấu hình định dạng YAML dùng để định nghĩa và quản lý chạy đồng thời nhiều containers liên quan (ví dụ: chạy song song web app, DB, Redis).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao không nên hardcode thông tin kết nối Database hoặc API Keys trong mã nguồn? Trình bày cách quản lý bằng biến môi trường (Environment Variables).
* **expected_key_points:**
  - id: KP3_1
    content: Rủi ro khi hardcode secrets
    keypoint_weight: 0.5
    description: Dễ bị lộ mật khẩu, tài khoản DB khi đẩy mã nguồn lên các kho chứa công cộng (GitHub); khó thay đổi cấu hình khi deploy sang các môi trường khác nhau.
  - id: KP3_2
    content: Quản lý bằng biến môi trường
    keypoint_weight: 0.5
    description: Đọc cấu hình từ biến môi trường của hệ điều hành (ví dụ: sử dụng `process.env` hoặc `System.getenv`); sử dụng file `.env` cục bộ cho môi trường dev.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích các chỉ thị cơ bản trong một Dockerfile: FROM, RUN, COPY, EXPOSE, và CMD. Chỉ ra sự khác nhau giữa CMD và ENTRYPOINT.
* **expected_key_points:**
  - id: KP4_1
    content: Giải thích các chỉ thị Dockerfile
    keypoint_weight: 0.6
    description: FROM (định nghĩa base image), RUN (chạy lệnh lúc build image), COPY (sao chép file từ máy chủ vào image), EXPOSE (khai báo cổng mạng), CMD (lệnh mặc định chạy khi container khởi động).
  - id: KP4_2
    content: Phân biệt CMD và ENTRYPOINT
    keypoint_weight: 0.4
    description: CMD dễ bị ghi đè khi chạy container bằng cách truyền tham số bổ sung ở terminal. ENTRYPOINT cố định lệnh khởi chạy, các tham số truyền thêm sẽ được coi là đối số của lệnh.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày sự khác nhau về cơ chế hoạt động và dung lượng bộ nhớ giữa Ảo hóa cấp độ phần cứng (Virtual Machines - VM) và Ảo hóa cấp độ OS (Containers).
* **expected_key_points:**
  - id: KP5_1
    content: Nguyên lý Virtual Machines (VM)
    keypoint_weight: 0.5
    description: Chạy trên Hypervisor; mỗi VM bắt buộc phải cài đặt một hệ điều hành khách (Guest OS) riêng biệt, tiêu tốn rất nhiều dung lượng đĩa và RAM, thời gian khởi động lâu (vài phút).
  - id: KP5_2
    content: Nguyên lý Containers
    keypoint_weight: 0.5
    description: Chia sẻ chung nhân hệ điều hành (Host OS Kernel); chỉ đóng gói ứng dụng và thư viện phụ thuộc nên dung lượng cực nhẹ (vài chục MB), khởi động tức thời trong vài giây.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế một quy trình CI/CD cơ bản sử dụng GitHub Actions để tự động hóa việc build, test và deploy một ứng dụng Backend Node.js/Java lên máy chủ cloud.
* **expected_key_points:**
  - id: KP6_1
    content: Các bước trong CI pipeline
    keypoint_weight: 0.5
    description: Khi push code -> trigger workflow -> chạy máy ảo -> checkout code -> cài đặt runtime -> chạy lint và unit tests -> build project thành file chạy.
  - id: KP6_2
    content: Các bước trong CD pipeline
    keypoint_weight: 0.5
    description: Đóng gói ứng dụng thành Docker Image -> đẩy lên Docker Registry -> kết nối SSH tới máy chủ cloud -> pull image mới -> restart container chạy ứng dụng.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách sử dụng Docker Volumes để lưu trữ dữ liệu bền vững (Data Persistence) cho container cơ sở dữ liệu (như PostgreSQL/MySQL). Điều gì xảy ra với dữ liệu nếu container bị xóa mà không gắn volume?
* **expected_key_points:**
  - id: KP7_1
    content: Cơ chế Docker Volumes
    keypoint_weight: 0.6
    description: Volume ánh xạ một thư mục cụ thể từ máy chủ vật lý (Host machine) trực tiếp vào bên trong thư mục chứa dữ liệu của DB container, giúp dữ liệu tồn tại độc lập với vòng đời container.
  - id: KP7_2
    content: Hậu quả khi xóa container không dùng volume
    keypoint_weight: 0.4
    description: Toàn bộ dữ liệu được ghi trong lớp ghi tạm thời của container sẽ bị mất vĩnh viễn không thể phục hồi khi container bị xóa bỏ (destroy).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế file Dockerfile tối ưu hóa dung lượng (Multi-stage Build) cho một ứng dụng Backend Java Spring Boot hoặc Node.js TypeScript, đảm bảo dung lượng image trên production là nhỏ nhất và bảo mật nhất.
* **expected_key_points:**
  - id: KP8_1
    content: Thiết kế cơ chế Multi-stage Build
    keypoint_weight: 0.5
    description: Stage 1 (Build): sử dụng image đầy đủ JDK/Node SDK để compile và build file chạy. Stage 2 (Run): chỉ sao chép file jar/js đã build sang image chạy tối giản (JRE alpine hoặc Node slim), loại bỏ SDK cồng kềnh.
  - id: KP8_2
    content: Bảo mật không dùng quyền Root (Non-root user)
    keypoint_weight: 0.5
    description: Tạo một user không có quyền quản trị (non-root) trong Dockerfile và thiết lập `USER nonroot` để chạy ứng dụng, tránh rủi ro kẻ tấn công chiếm quyền kiểm soát máy chủ host nếu container bị hack.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc triển khai ứng dụng Backend có tính sẵn sàng cao (High Availability) trên cụm máy chủ sử dụng Kubernetes, đảm bảo không mất kết nối của người dùng khi cập nhật phiên bản mới (Zero-downtime Deployment).
* **expected_key_points:**
  - id: KP9_1
    content: Cấu hình Deployment và Liveness/Readiness Probes
    keypoint_weight: 0.5
    description: Thiết lập `Readiness Probe` để Kubernetes chỉ dẫn traffic vào Pod mới khi ứng dụng đã khởi động hoàn toàn; thiết lập `Liveness Probe` tự động khởi động lại pod nếu ứng dụng bị treo.
  - id: KP9_2
    content: Chiến lược cập nhật Rolling Update
    keypoint_weight: 0.5
    description: Cấu hình `strategy: RollingUpdate` thiết lập `maxSurge` (số pod tạo thêm tối đa) và `maxUnavailable` (số pod tạm dừng tối đa), đảm bảo luôn có tối thiểu 80% số pods cũ chạy phục vụ khách hàng khi đang deploy bản mới.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản xử lý sự cố khi toàn bộ phân vùng ổ đĩa chứa Docker logs bị đầy (100% Disk Usage) trên máy chủ Production, làm gián đoạn mọi dịch vụ Backend.
* **expected_key_points:**
  - id: KP10_1
    content: Khắc phục sự cố khẩn cấp
    keypoint_weight: 0.5
    description: Sử dụng lệnh `docker system prune` để dọn dẹp các container đã dừng, images không dùng; viết script xóa hoặc nén bớt các file log cũ của docker (`/var/lib/docker/containers/.../*-json.log`) để giải phóng dung lượng.
  - id: KP10_2
    content: Giải pháp ngăn ngừa lâu dài (Log Rotation)
    keypoint_weight: 0.5
    description: Cấu hình log rotation mặc định trong file `/etc/docker/daemon.json` giới hạn kích thước tối đa của mỗi file log (ví dụ: `max-size: 10m`) và số lượng file log tối đa được giữ lại (ví dụ: `max-file: 3`).

