# Bộ Câu Hỏi Phỏng Vấn DevOps Engineer (Level 1)

* **Role:** DevOps Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong quy trình CI/CD và quản lý mã nguồn, khi cần tích hợp các thay đổi từ nhánh tính năng (Feature Branch) vào nhánh chính (Main Branch), hãy phân biệt sự khác biệt cơ bản về mặt cơ chế hoạt động và cấu trúc lịch sử commit (Git History) giữa hai câu lệnh: `git merge` và `git rebase`.
* **expected_key_points:**
  - id: KP1_1
    content: Cơ chế tạo Merge Commit của git merge
    keypoint_weight: 0.5
    description: `git merge` tạo ra một commit gộp (Merge Commit) để liên kết lịch sử hai nhánh, bảo toàn thứ tự thời gian thực tế nhưng có thể làm lịch sử chằng chịt.
  - id: KP1_2
    content: Cơ chế viết lại lịch sử tuyến tính của git rebase
    keypoint_weight: 0.5
    description: `git rebase` di chuyển nhánh hiện tại sang đỉnh nhánh đích, viết lại lịch sử (thay đổi hash) để tạo ra một đường thẳng tuyến tính (linear history).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Cơ chế xác thực thông qua SSH Key hoạt động dựa trên nguyên lý mã hóa nào? Hãy phân biệt vai trò độc lập của Private Key và Public Key khi kết nối đến Server.
* **expected_key_points:**
  - id: KP2_1
    content: Nguyên lý mã hóa bất đối xứng
    keypoint_weight: 0.4
    description: Sử dụng cặp khóa toán học (Public và Private Key) để xác thực mà không cần gửi mật khẩu qua mạng.
  - id: KP2_2
    content: Vai trò của Public Key trên Server
    keypoint_weight: 0.3
    description: Lưu trong file authorized_keys, dùng như ổ khóa để mã hóa thử thách gửi đến Client.
  - id: KP2_3
    content: Vai trò của Private Key tại Client
    keypoint_weight: 0.3
    description: Lưu bảo mật tại máy cá nhân, dùng để ký/giải mã thử thách từ Server, chứng minh danh tính.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt sự khác biệt cốt lõi về kiến trúc tài nguyên và cơ chế chia sẻ nhân hệ điều hành (Kernel) giữa Máy ảo (VM) và Container (như Docker).
* **expected_key_points:**
  - id: KP3_1
    content: VM sử dụng Hypervisor và Guest OS riêng
    keypoint_weight: 0.4
    description: VM chạy trên Hypervisor, mỗi máy ảo cần một OS riêng biệt với Kernel độc lập, tốn tài nguyên và thời gian khởi động lâu.
  - id: KP3_2
    content: Container chia sẻ Kernel với Host OS
    keypoint_weight: 0.4
    description: Container chạy trên Container Runtime, chia sẻ chung Kernel của máy chủ, khởi động nhanh và cực kỳ nhẹ.
  - id: KP3_3
    content: Tối ưu hiệu năng tài nguyên
    keypoint_weight: 0.2
    description: Container tối ưu thông lượng tài nguyên (RAM/CPU) hơn do loại bỏ lớp Guest OS dư thừa.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Blue-Green Deployment là gì? Cơ chế này hỗ trợ Rollback như thế nào nếu bản cập nhật bị lỗi?
* **expected_key_points:**
  - id: KP4_1
    content: Kiến trúc hai môi trường song song
    keypoint_weight: 0.4
    description: Duy trì hai môi trường Blue (đang chạy) và Green (phiên bản mới) đồng nhất.
  - id: KP4_2
    content: Chuyển đổi traffic qua Load Balancer
    keypoint_weight: 0.3
    description: Cấu hình lại Load Balancer để trỏ traffic từ Blue sang Green sau khi kiểm thử thành công.
  - id: KP4_3
    content: Rollback tức thời
    keypoint_weight: 0.3
    description: Nếu lỗi, chỉ cần trỏ traffic ngược lại về Blue, đạt Zero-downtime rollback.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong Terraform, `terraform.tfstate` đóng vai trò gì? Tại sao cần dùng Remote State và State Locking trong dự án nhóm?
* **expected_key_points:**
  - id: KP5_1
    content: Statefile là nguồn chân lý (Source of Truth)
    keypoint_weight: 0.4
    description: Lưu trữ trạng thái thực tế để ánh xạ mã nguồn với tài nguyên Cloud.
  - id: KP5_2
    content: Remote State tập trung
    keypoint_weight: 0.3
    description: Tránh xung đột và đồng bộ trạng thái khi nhiều người cùng làm việc.
  - id: KP5_3
    content: State Locking tránh ghi đè đồng thời
    keypoint_weight: 0.3
    description: Khóa file state khi một người đang thực thi lệnh, ngăn ngừa thảm họa Race Condition.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày kiến trúc phân tách thành phần cơ bản của một cụm Kubernetes Cluster (Control Plane vs Worker Node).
* **expected_key_points:**
  - id: KP6_1
    content: Control Plane điều phối toàn cụm
    keypoint_weight: 0.4
    description: Chứa API Server, etcd, Scheduler, Controller Manager, chịu trách nhiệm quản lý trạng thái cluster.
  - id: KP6_2
    content: Worker Node thực thi ứng dụng
    keypoint_weight: 0.4
    description: Chứa Kubelet, Kube-proxy, Container Runtime để vận hành các Pod.
  - id: KP6_3
    content: Pod là đơn vị tính toán nhỏ nhất
    keypoint_weight: 0.2
    description: Là bao chứa các container chia sẻ mạng và lưu trữ.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao không nên để Hardcoded Secrets trong mã nguồn? Giải pháp quản lý Secret an toàn trong Pipeline là gì?
* **expected_key_points:**
  - id: KP7_1
    content: Lộ lọt thông tin vĩnh viễn qua Git
    keypoint_weight: 0.4
    description: Git lưu lịch sử commit, việc lộ secret tạo rủi ro bảo mật nghiêm trọng.
  - id: KP7_2
    content: Sử dụng Secret Manager tập trung
    keypoint_weight: 0.4
    description: Dùng HashiCorp Vault, AWS Secrets Manager để lưu mật mã hóa.
  - id: KP7_3
    content: Inject secret vào runtime
    keypoint_weight: 0.2
    description: Nhúng secret qua biến môi trường tại thời điểm chạy pipeline, tránh để lại dấu vết trên disk.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích thuật toán đồng thuận Raft trong `etcd` và lý do vì sao cụm Raft thường yêu cầu số lượng Node lẻ (3, 5, 7)?
* **expected_key_points:**
  - id: KP8_1
    content: Nguyên lý đạt ngưỡng Quorum
    keypoint_weight: 0.4
    description: Cần đa số phiếu bầu (Quorum = N/2 + 1) để quyết định leader hoặc commit dữ liệu.
  - id: KP8_2
    content: Ngăn chặn Split-Brain khi đứt mạng
    keypoint_weight: 0.4
    description: Số lẻ đảm bảo trong trường hợp đứt mạng, phân vùng đạt đa số sẽ hoạt động, phân vùng còn lại dừng, tránh việc hai phe cùng bầu leader.
  - id: KP8_3
    content: Tối ưu khả năng chịu lỗi
    keypoint_weight: 0.2
    description: Số chẵn không tăng khả năng chịu lỗi so với số lẻ nhỏ hơn liền kề nhưng lại gây tốn kém hạ tầng.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Kỹ thuật Canary Deployment kết hợp Istio Service Mesh giúp kiểm soát Traffic Splitting thế nào? Envoy Proxy đóng vai trò gì?
* **expected_key_points:**
  - id: KP9_1
    content: Phân phối traffic linh hoạt
    keypoint_weight: 0.4
    description: Định tuyến chính xác % traffic sang phiên bản mới mà không cần chỉnh số lượng Pod.
  - id: KP9_2
    content: Envoy Proxy đánh chặn traffic (Sidecar)
    keypoint_weight: 0.4
    description: Sidecar proxy trong Pod đánh chặn mạng để điều hướng dựa trên logic định tuyến (không sửa code).
  - id: KP9_3
    content: Định tuyến thông minh theo Layer 7 (Headers/Cookies)
    keypoint_weight: 0.2
    description: Phân tích metadata để định tuyến người dùng thử nghiệm sang Canary, người dùng thường sang bản ổn định.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Tại sao Rolling Update mặc định chưa đủ cho Zero-Downtime? Giải thích sự phối hợp của `maxSurge`, `maxUnavailable` và `readinessProbe`.
* **expected_key_points:**
  - id: KP10_1
    content: Điều khiển số lượng Pod biến động
    keypoint_weight: 0.4
    description: `maxSurge` (Pod tạo mới) và `maxUnavailable` (Pod cũ bị tắt) cần cấu hình chặt chẽ để đảm bảo hệ thống luôn đủ Pod phục vụ.
  - id: KP10_2
    content: readinessProbe đảm bảo ứng dụng đã sẵn sàng
    keypoint_weight: 0.4
    description: Nếu không có nó, traffic bị đẩy vào Pod đang khởi động gây lỗi 502/503.
  - id: KP10_3
    content: Quy trình cuốn chiếu an toàn
    keypoint_weight: 0.2
    description: K8s chỉ trỏ traffic vào Pod mới sau khi vượt qua readinessProbe, sau đó mới xóa Pod cũ, giúp luồng traffic thông suốt.