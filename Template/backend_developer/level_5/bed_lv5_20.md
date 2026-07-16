# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 5) - Tập Đề Kubernetes Patroni và GitOps CI/CD (20)

* **Role:** Backend Developer
* **Level:** Level 5
* **Experience:** Trên 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Kubernetes là gì? Giải thích vai trò của các thành phần chính trong Kubernetes Control Plane: API Server, etcd, Scheduler, và Controller Manager.
* **expected_key_points:**
  - id: KP1_1
    content: Khái niệm Kubernetes và API Server/etcd
    keypoint_weight: 0.5
    description: Kubernetes là hệ thống điều phối container phân tán. API Server là cổng giao tiếp trung tâm nhận mọi request. etcd là kho lưu trữ key-value phân tán lưu toàn bộ trạng thái cấu hình của cụm.
  - id: KP1_2
    content: Vai trò của Scheduler và Controller Manager
    keypoint_weight: 0.5
    description: Scheduler theo dõi các Pods mới tạo và chọn node phù hợp nhất để chạy Pod đó. Controller Manager chạy các tiến trình giám sát (controllers) để duy trì trạng thái thực tế của cụm trùng khớp với trạng thái mong muốn.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau về bản chất và kịch bản sử dụng giữa hai tài nguyên Kubernetes: Deployment và StatefulSet. Khi nào bắt buộc phải dùng StatefulSet?
* **expected_key_points:**
  - id: KP2_1
    content: Đặc trưng Deployment vs StatefulSet
    keypoint_weight: 0.5
    description: Deployment quản lý các stateless pods không có định danh duy nhất (có thể thay thế tự do). StatefulSet quản lý các stateful pods có định danh số thứ tự tăng dần cố định (`pod-0`, `pod-1`) và gắn kèm Persistent Volume riêng biệt không đổi khi Pod khởi động lại.
  - id: KP2_2
    content: Trường hợp bắt buộc dùng StatefulSet
    keypoint_weight: 0.5
    description: Khi triển khai các ứng dụng cơ sở dữ liệu (PostgreSQL master-slave, MongoDB replica set, Kafka brokers) yêu cầu định danh mạng cố định và bộ nhớ độc lập cho từng node.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích khái niệm Hạ tầng dưới dạng Code (Infrastructure as Code - IaC). So sánh sự khác nhau về nguyên lý giữa phong cách Declarative (như Terraform) và Imperative (như Ansible).
* **expected_key_points:**
  - id: KP3_1
    content: Phong cách Declarative (Terraform)
    keypoint_weight: 0.5
    description: Khai báo trạng thái mong muốn cuối cùng của hạ tầng (ví dụ: tôi muốn có 3 VMs). Công cụ tự động tính toán sai lệch với thực tế và thực hiện các bước thay đổi để đạt trạng thái đó.
  - id: KP3_2
    content: Phong cách Imperative (Ansible)
    keypoint_weight: 0.5
    description: Khai báo tuần tự các bước cấu hình cụ thể cần chạy (ví dụ: tạo VM -> cài java -> copy file). Phù hợp cho cấu hình phần mềm trên máy chủ có sẵn; Declarative phù hợp hơn cho quản lý vòng đời tài nguyên.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế giải pháp Phát hiện dịch vụ (Service Discovery) và Cân bằng tải (Load Balancing) trong cụm Kubernetes sử dụng Kube-Proxy và CoreDNS.
* **expected_key_points:**
  - id: KP4_1
    content: Vai trò của CoreDNS
    keypoint_weight: 0.5
    description: CoreDNS tự động cập nhật bản ghi DNS khi có Service mới tạo, giúp các Pods tìm thấy nhau qua tên miền nội bộ (ví dụ: `http://my-service.my-namespace`).
  - id: KP4_2
    content: Cơ chế hoạt động của Kube-Proxy
    keypoint_weight: 0.5
    description: Kube-Proxy chạy trên mỗi node, liên tục cập nhật các quy tắc iptables hoặc IPVS để tự động điều hướng và cân bằng tải các request từ IP ảo của Service tới các Pod thực tế phía sau.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế file cấu hình Terraform quản lý hạ tầng cụm máy chủ Backend đa vùng, trình bày cách quản lý an toàn trạng thái (State File Locking) sử dụng S3 và DynamoDB.
* **expected_key_points:**
  - id: KP5_1
    content: Cấu trúc cấu hình Terraform đa vùng
    keypoint_weight: 0.5
    description: Sử dụng Terraform Modules để tái sử dụng mã nguồn hạ tầng; cấu hình các provider tương ứng cho từng vùng (ví dụ: `aws.us-east-1` và `aws.eu-west-1`).
  - id: KP5_2
    content: Quản lý khóa trạng thái (State Locking)
    keypoint_weight: 0.5
    description: Cấu hình Terraform Backend lưu file trạng thái (.tfstate) lên S3 bucket có bật tính năng versioning để phục hồi; sử dụng DynamoDB table làm khóa chặn (lock) để ngăn chặn 2 người cùng apply Terraform đồng thời gây xung đột.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích cơ chế hoạt động của Kubernetes HPA (Horizontal Pod Autoscaler) và cách cấu hình scale dựa trên Custom Metrics (Prometheus queries) thay vì CPU/RAM.
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên lý hoạt động của HPA
    keypoint_weight: 0.5
    description: HPA định kỳ truy vấn chỉ số tài nguyên thông qua Metrics Server và tự động tăng/giảm số lượng replica của Deployment để duy trì chỉ số trung bình đạt mức mong muốn.
  - id: KP6_2
    content: Cấu hình scale bằng Custom Metrics (Prometheus)
    keypoint_weight: 0.5
    description: Triển khai Prometheus Adapter để chuyển đổi metrics từ Prometheus thành API Kubernetes custom metrics; cấu hình HPA scale dựa trên số lượng request rps trên mỗi Pod hoặc độ dài hàng đợi tin nhắn.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh ưu nhược điểm và kiến trúc hoạt động của các giải pháp Ingress Controller phổ biến trong Kubernetes: Nginx Ingress, Traefik, và HAProxy.
* **expected_key_points:**
  - id: KP7_1
    content: Kiến trúc Nginx Ingress vs Traefik vs HAProxy
    keypoint_weight: 0.6
    description: Nginx Ingress chạy trên cấu hình tĩnh, nạp lại cấu hình (reload) khi đổi pods. Traefik thiết kế cloud-native tự động nạp cấu hình động tức thời. HAProxy tối ưu cho throughput lớn và cân bằng tải lớp 4/7 tốt.
  - id: KP7_2
    content: Lựa chọn áp dụng phù hợp
    keypoint_weight: 0.4
    description: Chọn Traefik cho môi trường microservices có pod thay đổi liên tục. Chọn Nginx Ingress cho sự ổn định, quen thuộc và tính năng đa dạng. Chọn HAProxy cho tải cực cao.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc triển khai hệ thống cơ sở dữ liệu quan hệ (như PostgreSQL) có tính sẵn sàng cao chạy trên Kubernetes sử dụng CloudNativePG hoặc Patroni Operator, đảm bảo tự động failover và không mất dữ liệu.
* **expected_key_points:**
  - id: KP8_1
    content: Cơ chế bầu chọn Leader và Đồng bộ replication
    keypoint_weight: 0.5
    description: Sử dụng Patroni kết hợp etcd để quản lý trạng thái động của cụm; Patroni liên tục kiểm tra sức khỏe của Master. Thiết lập replication dạng Streaming Replication để đồng bộ dữ liệu.
  - id: KP8_2
    content: Tự động Failover an sau sự cố (Split-brain prevention)
    keypoint_weight: 0.5
    description: Khi Master sập -> etcd thu hồi khóa -> Patroni bầu một Replica có tiến trình WAL mới nhất lên làm Master mới và tự động cập nhật Service IP của Kubernetes để định tuyến ghi không bị lỗi.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế quy trình CI/CD GitOps tự động hóa hoàn toàn sử dụng ArgoCD và Helm để triển khai mã nguồn an toàn lên cụm Kubernetes production đa vùng địa lý.
* **expected_key_points:**
  - id: KP9_1
    content: Nguyên lý GitOps và ArgoCD Application
    keypoint_weight: 0.5
    description: Mọi cấu hình Kubernetes (Helm charts) được lưu trữ trong Git. ArgoCD liên tục so sánh trạng thái thực tế của cụm K8s với file định nghĩa trên Git (Git source of truth); tự động chạy đồng bộ (Sync) khi có thay đổi trên Git branch.
  - id: KP9_2
    content: Triển khai đa vùng địa lý (Multi-destination Sync)
    keypoint_weight: 0.5
    description: Cấu hình ArgoCD quản lý nhiều đích (Clusters) khác vùng; sử dụng Helm values tương ứng cho từng vùng để tự động cập nhật số lượng replica, địa chỉ kết nối nội bộ riêng biệt.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp phân bổ mạng an toàn (Network Policies) cho hệ thống Kubernetes chạy microservices phức tạp, áp dụng quy tắc Zero-Trust ngăn chặn hoàn toàn giao tiếp không được phép giữa các namespaces.
* **expected_key_points:**
  - id: KP10_1
    content: Quy tắc mặc định từ chối toàn bộ (Default Deny All)
    keypoint_weight: 0.5
    description: Thiết lập NetworkPolicy mặc định chặn toàn bộ kết nối đầu vào (Ingress) và đầu ra (Egress) của tất cả các Pods trong namespace, cô lập hoàn toàn mạng lưới.
  - id: KP10_2
    content: Cấp phép mịn theo nhãn (Label-based Allow Rules)
    keypoint_weight: 0.5
    description: Viết các NetworkPolicies cụ thể cho phép Pod A được kết nối tới Pod B dựa trên nhãn `app=pod-b` và cổng port xác định; chỉ cho phép Ingress Controller giao tiếp với API Gateway, tuân thủ mô hình bảo mật Zero-Trust.

