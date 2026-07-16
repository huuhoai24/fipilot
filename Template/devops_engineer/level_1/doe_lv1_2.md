# Bộ Câu Hỏi Phỏng Vấn DevOps Engineer (Level 1)

* **Role:** DevOps Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong quy trình CI/CD và quản lý mã nguồn, hãy phân biệt sự khác biệt về mặt cơ chế hoạt động và hệ quả lên lịch sử commit (Git History) giữa hai câu lệnh: `git merge` và `git rebase`.
* **expected_key_points:**
  - id: KP1_1
    content: Cơ chế hoạt động và đặc điểm lịch sử của git merge
    keypoint_weight: 0.5
    description: `git merge` thực hiện gộp hai nhánh bằng cách tạo ra một commit gộp độc lập (Merge Commit) nối liền hai nhánh lại với nhau. Cơ chế này giúp bảo toàn nguyên vẹn lịch sử commit và thứ tự thời gian thực tế của cả hai nhánh, nhưng dễ làm lịch sử commit bị rối mắt, chằng chịt khi có nhiều nhánh song hành.
  - id: KP1_2
    content: Cơ chế hoạt động và đặc điểm lịch sử của git rebase
    keypoint_weight: 0.5
    description: `git rebase` thực hiện di chuyển hoặc "bứng" toàn bộ gốc của nhánh hiện tại đặt lên trên đỉnh commit mới nhất của nhánh đích. Nó viết lại lịch sử commit bằng cách tạo ra các commit mới hoàn toàn (thay đổi hash), tạo ra một lịch sử commit dạng một đường thẳng tuyến tính (Linear history) rất sạch sẽ, nhưng làm mất đi mốc thời gian thực tế phát sinh của các commit gốc.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Cơ chế xác thực không mật khẩu thông qua SSH Key (Secure Shell) hoạt động dựa trên nguyên lý mã hóa nào? Hãy giải thích vai trò độc lập và mối quan hệ giữa hai thành phần Private Key và Public Key khi thiết lập kết nối từ máy cá nhân đến Server.
* **expected_key_points:**
  - id: KP2_1
    content: Nguyên lý mã hóa bất đối xứng của cơ chế SSH
    keypoint_weight: 0.4
    description: SSH Key hoạt động dựa trên nền tảng của thuật toán mã hóa bất đối xứng (Asymmetric Cryptography), sử dụng một cặp khóa toán học có mối liên kết chặt chẽ với nhau bao gồm Khóa công khai (Public Key) và Khóa bí mật (Private Key).
  - id: KP2_2
    content: Vai trò lưu trữ và nhiệm vụ của Public Key trên Server
    keypoint_weight: 0.3
    description: Public Key được upload và lưu trữ công khai trên Server đích (trong file authorized_keys). Public Key đóng vai trò như một chiếc ổ khóa, dùng để mã hóa thử thách (Challenge) gửi về cho Client kiểm tra và không cần phải giữ bí mật.
  - id: KP2_3
    content: Vai trò bảo mật và nhiệm vụ ký xác thực của Private Key tại Client
    keypoint_weight: 0.3
    description: Private Key bắt buộc phải được lưu trữ tuyệt đối bảo mật tại máy cá nhân của người dùng (Client) và không được gửi qua mạng. Khi thiết lập kết nối, Client sử dụng Private Key để ký (Sign) giải mã thử thách từ Server gửi sang, chứng minh quyền sở hữu hợp pháp để mở khóa Server.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt sự khác biệt cốt lõi về mặt kiến trúc tài nguyên, cơ chế chia sẻ tài nguyên phần cứng và tốc độ khởi động giữa ảo hóa cấp độ phần cứng Máy ảo (Virtual Machine) và ảo hóa cấp độ hệ điều hành Container (như Docker).
* **expected_key_points:**
  - id: KP3_1
    content: Kiến trúc sở hữu Kernel riêng biệt và lớp Hypervisor của Virtual Machine
    keypoint_weight: 0.4
    description: Máy ảo (VM) chạy trên một lớp điều khiển Hypervisor. Mỗi VM bắt buộc phải cài đặt một Hệ điều hành khách toàn chỉnh (Guest OS), sở hữu một Kernel (Nhân) hệ điều hành độc lập hoàn toàn, tiêu tốn nhiều dung lượng đĩa và tài nguyên phần cứng cố định cho OS.
  - id: KP3_2
    content: Kiến trúc chia sẻ chung Guest OS Kernel của Container
    keypoint_weight: 0.4
    description: Container loại bỏ lớp Hypervisor và Guest OS, chạy trực tiếp trên Container Engine (như Docker Daemon). Tất cả các Container dùng chung (share) Kernel của Hệ điều hành máy chủ (Host OS) và cô lập ứng dụng bằng các tính năng của Linux Kernel (Namespaces và Cgroups), giúp kích thước siêu nhẹ.
  - id: KP3_3
    content: Khác biệt về tốc độ khởi động và chi phí tài nguyên runtime
    keypoint_weight: 0.2
    description: VM mất từ vài phút để khởi động vì phải boot toàn bộ hệ điều hành từ đầu và ngốn nhiều RAM/CPU tĩnh. Container khởi động gần như ngay lập tức (vài giây) vì thực chất chỉ là một tiến trình (Process) độc lập được cô lập trên Host OS, tối ưu thông lượng tài nguyên.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Chiến lược triển khai ứng dụng Blue-Green Deployment là gì? Hãy giải thích cơ chế chuyển đổi môi trường và nêu ưu điểm lớn nhất của chiến lược này khi hệ thống phát sinh lỗi nghiêm trọng ngay sau khi chuyển đổi traffic.
* **expected_key_points:**
  - id: KP4_1
    content: Nguyên lý duy trì song song hai môi trường hạ tầng độc lập
    keypoint_weight: 0.4
    description: Blue-Green Deployment yêu cầu duy trì song song hai môi trường hạ tầng giống hệt nhau: Môi trường Blue (hiện tại đang chạy production nhận traffic của người dùng) và Môi trường Green (môi trường mới nơi deployment phiên bản code mới để chạy thử nghiệm nội bộ).
  - id: KP4_2
    content: Cơ chế cấu hình định tuyến chuyển đổi traffic ở tầng Router/Load Balancer
    keypoint_weight: 0.3
    description: Khi phiên bản mới trên môi trường Green đã kiểm thử thành công, DevOps Engineer sẽ thực hiện thay đổi cấu hình định tuyến (Routing/DNS) tại tầng Load Balancer hoặc Router để trỏ toàn bộ 100% traffic của người dùng từ Blue sang Green một cách tức thì.
  - id: KP4_3
    content: Cơ chế Rollback tức thời không gây gián đoạn hệ thống khi phát sinh lỗi
    keypoint_weight: 0.3
    description: Ưu điểm lớn nhất là nếu phiên bản mới phát sinh lỗi nghiêm trọng trên Production, hệ thống có thể Rollback lập tức bằng cách cấu hình Load Balancer trỏ traffic ngược lại về môi trường Blue cũ (vẫn đang chạy ngầm ổn định), giúp triệt tiêu thời gian sập hệ thống (Zero downtime rollback).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong công cụ quản lý hạ tầng dạng mã (IaC) Terraform, tệp tin `terraform.tfstate` (Statefile) đóng vai trò gì? Tại sao trong môi trường dự án doanh nghiệp lớn có nhiều kỹ sư cùng làm việc, chúng ta bắt buộc phải cấu hình Remote State kết hợp State Locking?
* **expected_key_points:**
  - id: KP5_1
    content: Vai trò lưu trữ bản đồ ánh xạ hạ tầng của Statefile
    keypoint_weight: 0.4
    description: Statefile đóng vai trò là nguồn chân lý duy nhất (Source of truth) lưu trữ trạng thái thực tế của hạ tầng, giúp Terraform ánh xạ giữa các file cấu hình mã nguồn (.tf) và các tài nguyên vật lý thực tế được tạo ra trên Cloud Provider.
  - id: KP5_2
    content: Rủi ro bất đồng nhất dữ liệu hạ tầng khi lưu Statefile cục bộ (Local State)
    keypoint_weight: 0.3
    description: Nếu lưu cục bộ trên máy cá nhân, các kỹ sư khác nhau sẽ có các phiên bản statefile khác nhau, dẫn đến hiện tượng ghi đè, xung đột hạ tầng hoặc xóa nhầm tài nguyên của nhau khi chạy lệnh `terraform apply`. Remote State (lưu tập trung trên AWS S3, GCS) giải quyết bài toán này bằng một file state store tập trung chung.
  - id: KP5_3
    content: Cơ chế khóa file của State Locking chống rủi ro ghi đè đồng thời (Race Condition)
    keypoint_weight: 0.3
    description: State Locking (sử dụng DynamoDB hoặc Redis) đảm bảo rằng tại một thời điểm chỉ có duy nhất một câu lệnh thực thi apply hạ tầng được phép ghi vào file State. Nếu kỹ sư A đang chạy apply, file State sẽ bị khóa; kỹ sư B cố tình apply cùng lúc sẽ bị từ chối, ngăn chặn thảm họa Race Condition phá vỡ cấu trúc file state.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy trình bày kiến trúc phân tách thành phần cơ bản của một cụm Kubernetes Cluster (K8s). Phân biệt nhiệm vụ logic giữa Control Plane (Master Node) và Worker Node.
* **expected_key_points:**
  - id: KP6_1
    content: Nhiệm vụ điều phối toàn cục và quản lý trạng thái của Control Plane (Master Node)
    keypoint_weight: 0.4
    description: Control Plane chịu trách nhiệm đưa ra các quyết định điều phối toàn cụm, phát hiện và phản hồi các sự kiện. Các thành phần bắt buộc phải có bao gồm: `kube-apiserver` (giao tiếp trung tâm), `etcd` (lưu trữ database trạng thái cụm), `kube-scheduler` (lập lịch phân phối Pods), và `kube-controller-manager` (duy trì trạng thái mong muốn).
  - id: KP6_2
    content: Nhiệm vụ thực thi chạy tải ứng dụng vật lý của Worker Node
    keypoint_weight: 0.4
    description: Worker Node là nơi trực tiếp tiếp nhận và duy trì hoạt động vật lý của các Pods ứng dụng. Các thành phần cốt lõi chạy trên mỗi Worker Node gồm: `kubelet` (tác vụ ngầm giao tiếp với Master Node để quản lý vòng đời container), `kube-proxy` (quản lý mạng và định tuyến traffic nội bộ), và Container Runtime (như Docker/containerd để chạy container).
  - id: KP6_3
    content: Logic đóng gói đơn vị tính toán nhỏ nhất thông qua Pods
    keypoint_weight: 0.2
    description: Pod là đơn vị tính toán nhỏ nhất có thể lập lịch trong Kubernetes, đại diện cho một tiến trình đang chạy trong cụm, có thể chứa một hoặc một nhóm các container chia sẻ chung không gian lưu trữ mạng (Network/Storage namespaces).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi xây dựng một Continuous Integration (CI) Pipeline tự động, tại sao việc nhúng trực tiếp mật khẩu, API tokens (Hardcoded Secrets) vào mã nguồn Git lại là một lỗ hổng bảo mật nghiêm trọng? Hãy nêu cơ chế quản lý Secrets an toàn sử dụng các công cụ quản lý chuyên biệt (như HashiCorp Vault hoặc Cloud Secret Manager).
* **expected_key_points:**
  - id: KP7_1
    content: Nguy cơ lộ lọt thông tin diện rộng và mất vết kiểm toán của Hardcoded Secrets
    keypoint_weight: 0.4
    description: Git lưu trữ toàn bộ lịch sử commit vĩnh viễn. Việc để lộ secret trên repo (kể cả repo private) tạo ra rủi ro bị hacker scan, lộ lọt thông tin hệ thống diện rộng khi phân quyền cho nhân viên mới, và hoàn toàn mất đi khả năng xoay vòng khóa (Secret rotation) hay kiểm toán bảo mật.
  - id: KP7_2
    content: Cơ chế mã hóa tĩnh (Encryption at rest) và phân quyền truy cập động của công cụ Secret store
    keypoint_weight: 0.4
    description: Các công cụ chuyên biệt như Vault lưu trữ secret dưới dạng mã hóa tĩnh bằng các thuật toán nâng cao, cung cấp cơ chế phân quyền truy cập nghiêm ngặt dựa trên danh tính (AppRole, IAM Roles) thông qua các Token có thời hạn sống ngắn.
  - id: KP7_3
    content: Kỹ thuật Inject Secret động vào runtime của Pipeline (Environment Variables injection)
    keypoint_weight: 0.2
    description: Pipeline CI/CD sẽ sử dụng một tài khoản định danh an toàn để gọi vào API của Secret Manager tại runtime nhằm kéo secret về bộ nhớ đệm RAM, nhúng trực tiếp dưới dạng biến môi trường (Environment Variables) cho ứng dụng và tự động xóa sạch khi kết thúc task, không để lại dấu vết trên đĩa cứng hay Git.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong các hệ thống hạ tầng phân tán quy mô lớn, thành phần lưu trữ trạng thái của Kubernetes (etcd) hoặc công cụ quản lý cấu hình Consul hoạt động dựa trên thuật toán đồng thuận Raft (Raft Consensus Algorithm). Hãy giải thích nguyên lý toán học của khái niệm Quorum và tại sao cụm máy chủ chạy Raft bắt buộc phải thiết lập số lượng Nodes là số lẻ (3, 5, 7)?
* **expected_key_points:**
  - id: KP8_1
    content: Định nghĩa nguyên lý đạt đa số phiếu của khái niệm Quorum
    keypoint_weight: 0.4
    description: Thuật toán Raft yêu cầu hệ thống phải đạt được trạng thái đồng thuận của đa số để có thể bầu chọn Leader mới hoặc commit một log ghi dữ liệu hạ tầng thành công. Ngưỡng đa số này gọi là Quorum, được tính toán nghiêm ngặt bằng công thức: $Q = \lfloor N/2 \rfloor + 1$ (với $N$ là tổng số node trong cụm cluster).
  - id: KP8_2
    content: Bài toán phân tách mạng (Network Partition / Split-Brain) và cơ chế tự vệ của Raft
    keypoint_weight: 0.4
    description: Khi xảy ra sự cố đứt kết nối mạng chia đôi cụm cluster làm hai phần độc lập (Network Partition), nếu không có số lẻ, cả hai phần đều có nguy cơ tự bầu lên một Leader riêng (hiện tượng Split-Brain) gây phá hủy cấu trúc dữ liệu vĩnh viễn. Raft giải quyết bài toán này bằng cách chỉ cho phép phần phân vùng nào bốc thăm đạt đủ ngưỡng Quorum (đa số phiếu) được quyền hoạt động và ghi dữ liệu, phần còn lại không đủ số phiếu sẽ tự động chuyển sang chế độ Read-only hoặc tạm dừng.
  - id: KP8_3
    content: Phân tích hiệu quả toán học về khả năng chịu lỗi tối ưu của cấu hình số lẻ
    keypoint_weight: 0.2
    description: Thiết lập số lẻ tối ưu hóa chi phí phần cứng và khả năng chịu lỗi. Ví dụ: cụm 3 node có Quorum là 2, chịu lỗi được 1 node sập ($3 - 2 = 1$). Nếu tăng lên 4 node, Quorum tăng lên thành 3, khả năng chịu lỗi vẫn chỉ là 1 node sập ($4 - 3 = 1$). Do đó, cụm 4 node không tăng cường năng lực chịu lỗi so với cụm 3 node nhưng lại tốn thêm chi phí tài nguyên vật lý và băng thông đồng bộ qua mạng.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Khi triển khai vi dịch vụ (Microservices) trên Kubernetes, kỹ thuật Canary Deployment kết hợp với Service Mesh (như Istio) giúp kiểm soát lưu lượng mạng chuyên sâu ra sao? Hãy giải thích cơ chế hoạt động của Envoy Proxy (Sidecar Container) trong việc điều phối định tuyến Traffic Splitting dựa trên các thuộc tính của HTTP Request (Headers/Cookies).
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế cấu hình tỷ lệ phần trăm phân phối traffic linh hoạt ở tầng Service Mesh
    keypoint_weight: 0.4
    description: Khác với cơ chế phân phối thô sơ của Kubernetes Service (phụ thuộc vào số lượng Pods), Istio Service Mesh cho phép can thiệp sâu vào tầng mạng để định tuyến chính xác một tỷ lệ phần trăm nhỏ traffic (ví dụ 1% hoặc 5%) sang phiên bản ứng dụng mới (Canary) để kiểm thử mức độ ổn định mà không cần thay đổi quy mô số lượng Pods vật lý.
  - id: KP9_2
    content: Nguyên lý đánh chặn mạng chạy ngầm của Envoy Proxy Sidecar
    keypoint_weight: 0.4
    description: Istio nhúng một container phụ chạy ngầm là Envoy Proxy (Sidecar) nằm chung Pod với Container ứng dụng chính. Mọi lưu lượng mạng đi vào hoặc đi ra khỏi Pod đều bị Envoy Proxy đánh chặn (intercept) thông qua cấu hình iptables của Linux Kernel, giúp thực thi cấu hình định tuyến logic độc lập với mã nguồn của lập trình viên.
  - id: KP9_3
    content: Kỹ thuật định tuyến thông minh dựa trên Layer 7 Metadata (Headers/Cookies)
    keypoint_weight: 0.2
    description: Envoy Proxy phân tích sâu metadata của gói tin ở tầng ứng dụng (Layer 7). Nó cho phép thiết lập ranh giới định tuyến Canary tinh vi, ví dụ: chỉ định tuyến các request chứa HTTP Header `version: canary`, hoặc các request có Cookie chứa ID thuộc nhóm người dùng thử nghiệm (Beta testers) sang Pod Canary, phần còn lại vẫn chạy trên môi trường ổn định cũ.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Để đạt được quy trình Zero-Downtime khi cập nhật ứng dụng bằng chiến lược Rolling Update trong Kubernetes, tại sao chỉ dựa vào cấu hình mặc định là chưa đủ? Hãy phân tích cơ chế phối hợp toán học của hai tham số `maxSurge`, `maxUnavailable` kết hợp với cấu trúc logic kiểm tra sức khỏe hệ thống thông qua `livenessProbe` và `readinessProbe`.
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế toán học điều khiển số lượng Pod biến động của maxSurge và maxUnavailable
    keypoint_weight: 0.4
    description: `maxSurge` quy định số lượng hoặc tỷ lệ phần trăm tối đa các Pod có thể được tạo vượt ngưỡng mong muốn tại runtime trong quá trình cập nhật. `maxUnavailable` quy định số lượng Pod tối đa có thể rơi vào trạng thái không sẵn sàng (down) cùng một lúc. DevOps Engineer cần cấu hình tinh vi (ví dụ: `maxSurge: 25%`, `maxUnavailable: 0`) để cam kết hệ thống luôn có đủ số lượng Pod tối thiểu chịu tải, loại bỏ hoàn toàn rủi ro thiếu hụt tài nguyên gây sập luồng xử lý.
  - id: KP10_2
    content: Bản chất tách biệt logic của livenessProbe và tầm quan trọng của readinessProbe đối với tầng mạng Load Balancer
    keypoint_weight: 0.4
    description: `livenessProbe` kiểm tra xem container còn sống hay đã chết để K8s quyết định khởi động lại (restart) container. `readinessProbe` kiểm tra xem container đã sẵn sàng nhận traffic phục vụ người dùng chưa (ví dụ đã khởi chạy xong kết nối DB, nạp xong bộ đệm cache). Nếu không cấu hình `readinessProbe`, K8s sẽ lập tức đẩy traffic từ Load Balancer vào Pod mới ngay khi container vừa start, gây ra lỗi HTTP 502/503 cho khách hàng do ứng dụng chưa nạp xong logic bên trong.
  - id: KP10_3
    content: Quy trình phối hợp đồng bộ điều khiển vòng đời cập nhật (Rolling Update Workflow)
    keypoint_weight: 0.2
    description: Trong quá trình dịch chuyển cuốn chiếu, K8s tạo Pod mới (dựa trên maxSurge). Kubelet sẽ chạy liên tục kiểm tra `readinessProbe`. Chỉ khi Pod mới vượt qua bài test này thành công, K8s mới cập nhật Endpoint mạng để trỏ traffic vào nó, và sau đó mới kích hoạt lệnh xóa (terminate) một Pod cũ tương ứng, đảm bảo luồng traffic truyền tải liên tục không đứt quãng một mili giây nào.