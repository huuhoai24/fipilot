# Bộ Câu Hỏi Phỏng Vấn DevOps Engineer (Level 1)

* **Role:** DevOps Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong Git, sự khác biệt giữa hai lệnh `git fetch` và `git pull` là gì?
* **Đáp án mẫu:** `git fetch` chỉ tải các thay đổi và commits mới từ repository từ xa (remote) về máy cục bộ nhưng không tự động hòa trộn (merge) vào code hiện tại. `git pull` kết hợp cả hai bước: tải dữ liệu mới về (`fetch`) và tự động hòa trộn (`merge`) chúng vào nhánh hiện tại.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Tiến trình CI/CD là viết tắt của cụm từ nào? Nêu mục đích cốt lõi của CI và CD trong chu trình phát triển phần mềm.
* **Đáp án mẫu:** CI/CD là Continuous Integration (Tích hợp liên tục) và Continuous Delivery/Deployment (Chuyển giao/Triển khai liên tục). Mục đích của CI là tự động hóa việc kiểm tra, build và test code ngay khi lập trình viên commit. Mục đích của CD là tự động hóa quy trình đưa code đã qua kiểm thử lên các môi trường (Staging/Production) một cách an toàn và nhanh chóng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Containerization (Đóng gói ứng dụng) bằng Docker mang lại lợi ích gì so với việc chạy ứng dụng trực tiếp trên máy ảo (Virtual Machine) truyền thống?
* **Đáp án mẫu:** Docker container chia sẻ chung nhân hệ điều hành (OS kernel) của máy host nên khởi động nhanh hơn (vài giây), tiêu tốn ít tài nguyên phần cứng (CPU/RAM) và có kích thước nhẹ hơn rất nhiều so với máy ảo (VM) vốn cần một hệ điều hành khách (Guest OS) riêng biệt cho mỗi thực thể.

---

## CÂU HỎI TRUNG BÌNH (4 câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Phương pháp "Infrastructure as Code" (IaC) là gì? Hãy nêu tên 2 công cụ phổ biến thường được dùng để triển khai IaC.
* **Đáp án mẫu:** IaC là phương pháp quản lý, thiết lập và cấp phát hạ tầng CNTT (mạng, máy ảo, cấu hình) bằng các tệp tin cấu hình máy tính đọc được (code), thay vì cấu hình thủ công bằng tay trên giao diện. Hai công cụ phổ biến: Terraform và Ansible.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong Docker, điểm khác biệt về mục đích sử dụng giữa lệnh `EXPOSE` và việc ánh xạ cổng (Port Forwarding/Publishing) bằng cờ `-p` khi chạy container là gì?
* **Đáp án mẫu:** Lệnh `EXPOSE` trong Dockerfile chỉ mang tính chất tài liệu hóa và thông báo cổng mạng mà ứng dụng bên trong container sẽ lắng nghe, không thực sự mở cổng ra bên ngoài máy host. Trong khi đó, cờ `-p` (ví dụ: `-p 8080:80`) thực sự tạo ra một quy tắc mạng để ánh xạ cổng từ máy host vào cổng của container, cho phép bên ngoài truy cập.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Mô hình phân phối bản phát hành theo chiến lược "Blue-Green Deployment" hoạt động như thế nào để giảm thiểu thời gian gián đoạn (Downtime)?
* **Đáp án mẫu:** Chiến lược này duy trì hai môi trường phần cứng giống hệt nhau: Blue (đang chạy phiên bản hiện tại) và Green (môi trường staging chứa phiên bản mới). Khi phiên bản mới trên Green đã test thành công, bộ định tuyến (Router/Load Balancer) sẽ lập tức chuyển hướng toàn bộ traffic từ Blue sang Green, giúp downtime gần như bằng không và dễ dàng rollback nếu có lỗi.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Hệ thống giám sát (Monitoring) trong DevOps thường được chia làm hai loại chỉ số: "White-box monitoring" và "Black-box monitoring". Hãy phân biệt hai khái niệm này.
* **Đáp án mẫu:** - White-box monitoring: Giám sát dựa trên các số liệu nội bộ bên trong hệ thống (như dung lượng bộ nhớ RAM, CPU, logs của ứng dụng).
  - Black-box monitoring: Giám sát hệ thống từ bên ngoài như một người dùng cuối, kiểm tra xem hành vi hiển thị bên ngoài có đúng không (như kiểm tra giao thức HTTP response code, trạng thái ping endpoint).

---

## CÂU HỎI KHÓ (3 câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong cấu trúc phân cấp mạng của Kubernetes, một Service loại `ClusterIP`, `NodePort` và `LoadBalancer` khác nhau như thế nào về phạm vi truy cập?
* **Đáp án mẫu:** - `ClusterIP`: Chỉ cho phép các dịch vụ bên trong nội bộ cụm (cluster) Kubernetes giao tiếp with nhau, không thể truy cập từ internet.
  - `NodePort`: Mở một cổng cố định trên tất cả các Node (máy chủ), cho phép bên ngoài truy cập vào Pod thông qua địa chỉ IP của Node kết hợp với cổng đó (`NodeIP:NodePort`).
  - `LoadBalancer`: Tự động khởi tạo một bộ cân bằng tải thực tế của nhà cung cấp Cloud (như AWS, GCP), cấp một IP tĩnh duy nhất hướng trực tiếp traffic bên ngoài vào Service.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Khi cấu hình pipeline CI/CD, làm thế nào để quản lý các thông tin nhạy cảm (như API Keys, SSH Keys, Mật khẩu cơ sở dữ liệu) một cách an toàn mà không bị lộ trong mã nguồn Git?
* **Đáp án mẫu:** Tuyệt đối không hardcode vào tệp tin lưu trên Git. Thay vào đó, sử dụng tính năng quản lý biến môi trường bảo mật của chính công cụ CI/CD (như GitHub Actions Secrets, GitLab CI/CD Variables) hoặc tích hợp các dịch vụ quản lý bí mật chuyên dụng (như HashiCorp Vault, AWS Secrets Manager, Google Secret Manager) để inject vào container/pipeline khi thực thi.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong Terraform, tệp tin `terraform.tfstate` có vai trò gì và tại sao việc quản lý tệp này ở chế độ "Remote State" lại tối ưu hơn lưu ở cục bộ (Local)?
* **Đáp án mẫu:** Tệp `terraform.tfstate` lưu trữ sơ đồ trạng thái thực tế của hạ tầng đã được tạo để đối chiếu với mã nguồn code hiện tại. Việc lưu trữ ở Remote State (như trên AWS S3, Google Cloud Storage) giúp nhiều kỹ sư trong đội ngũ có thể cùng làm việc chung mà không bị xung đột, hỗ trợ tính năng khóa trạng thái (State Locking) tránh ghi đè dữ liệu lẫn nhau và bảo mật thông tin hạ tầng tốt hơn.