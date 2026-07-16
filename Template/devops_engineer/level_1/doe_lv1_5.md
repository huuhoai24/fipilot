# Bộ Câu Hỏi Phỏng Vấn DevOps Engineer (Level 1)

* **Role:** DevOps Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong quy trình CI/CD và quản lý mã nguồn, khi cần tích hợp các thay đổi từ một nhánh tính năng (Feature Branch) vào nhánh chính (Main Branch), hãy phân biệt sự khác biệt cơ bản về mặt cơ chế hoạt động và cấu trúc lịch sử commit (Git History) giữa hai câu lệnh: `git merge` và `git rebase`.
* **expected_key_points:**
  - id: KP1_1
    content: Cơ chế tạo Merge Commit để liên kết nhánh của git merge
    keypoint_weight: 0.5
    description: `git merge` gộp nhánh bằng cách tạo ra một commit gộp độc lập (Merge Commit) kết nối lịch sử của hai nhánh. Cơ chế này bảo toàn nguyên vẹn dòng lịch sử phi tuyến tính và thứ tự thời gian thực tế của các commit, nhưng có thể làm Git history bị rối, chằng chịt khi có nhiều nhánh song hành.
  - id: KP1_2
    content: Cơ chế viết lại lịch sử tuyến tính của git rebase
    keypoint_weight: 0.5
    description: `git rebase` di chuyển toàn bộ gốc của nhánh hiện tại đặt lên trên đỉnh commit mới nhất của nhánh đích. Thao tác này viết lại lịch sử commit (thay đổi hash), tạo ra một dòng lịch sử thẳng tuyến tính (Linear history) rất sạch sẽ, nhưng làm mất đi mốc thời gian thực tế phát sinh của các commit gốc.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Cơ chế xác thực không mật khẩu (Passwordless Authentication) thông qua SSH Key hoạt động dựa trên nguyên lý mã hóa nào? Hãy phân biệt vai trò độc lập của hai thành phần Private Key và Public Key khi thiết lập kết nối an toàn đến Server.
* **expected_key_points:**
  - id: KP2_1
    content: Nguyên lý mã hóa bất đối xứng (Asymmetric Cryptography) của SSH
    keypoint_weight: 0.4
    description: Xác thực SSH Key hoạt động dựa trên thuật toán mã hóa bất đối xứng, sử dụng một cặp khóa toán học có liên kết chặt chẽ với nhau bao gồm Khóa công khai (Public Key) và Khóa bí mật (Private Key).
  - id: KP2_2
    content: Vai trò lưu trữ và thử thách (Challenge) của Public Key trên Server
    keypoint_weight: 0.3
    description: Public Key được cấu hình và lưu trữ công khai trên Server đích (trong file authorized_keys). Nó đóng vai trò như một chiếc ổ khóa, dùng để mã hóa thông điệp thử thách gửi về cho Client và không cần giữ bí mật.
  - id: KP2_3
    content: Vai trò giải mã và ký xác thực của Private Key tại Client
    keypoint_weight: 0.3
    description: Private Key phải được lưu trữ tuyệt đối bí mật tại máy của người dùng (Client) và không bao giờ truyền qua mạng. Client sử dụng Private Key để giải mã thử thách hoặc ký số xác thực, chứng minh quyền sở hữu hợp pháp để thiết lập phiên kết nối.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt sự khác biệt cốt lõi về mặt kiến trúc tài nguyên và cơ chế chia sẻ nhân hệ điều hành (Kernel) giữa Máy ảo (Virtual Machine) và Container (như Docker Container).
* **expected_key_points:**
  - id: KP3_1
    content: Kiến trúc sở hữu Guest OS và lớp Hypervisor của Virtual Machine
    keypoint_weight: 0.4
    description: Máy ảo (VM) chạy trên một lớp Hypervisor. Mỗi VM bắt buộc phải cài đặt một Hệ điều hành khách đầy đủ (Guest OS), sở hữu một Kernel biệt lập, tiêu tốn nhiều tài nguyên tĩnh và dung lượng lưu trữ cho OS.
  - id: KP3_2
    content: Kiến trúc chia sẻ chung Host OS Kernel của Container
    keypoint_weight: 0.4
    description: Container loại bỏ lớp Hypervisor và Guest OS, chạy trực tiếp trên Container Runtime. Tất cả các Container dùng chung Kernel của Hệ điều hành máy chủ (Host OS) và cô lập ứng dụng bằng các tính năng của Linux (Namespaces và Cgroups), giúp kích thước siêu nhẹ.
  - id: KP3_3
    content: Khác biệt về chi phí tài nguyên và tốc độ khởi động tại runtime
    keypoint_weight: 0.2
    description: VM mất vài phút để khởi động vì phải boot toàn bộ hệ điều hành và ngốn tài nguyên RAM/CPU cố định. Container khởi động gần như ngay lập tức (vài giây) vì chỉ là các tiến trình được cô lập trên Host OS, tối ưu hiệu suất tài nguyên.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy trình bày nguyên lý hoạt động của chiến lược triển khai ứng dụng Blue-Green Deployment. Cơ chế này giúp hệ thống Rollback như thế nào nếu phiên bản ứng dụng mới phát sinh lỗi nghiêm trọng?
* **expected_key_points:**
  - id: KP4_1
    content: Nguyên lý duy trì song song hai môi trường hạ tầng đồng nhất
    keypoint_weight: 0.4
    description: Blue-Green Deployment yêu cầu duy trì hai môi trường hạ tầng độc lập nhưng giống hệt nhau: Môi trường Blue (phiên bản hiện tại đang chạy production nhận traffic) và Môi trường Green (phiên bản mới được deploy để thực hiện smoke test).
  - id: KP4_2
    content: Cơ chế cấu hình Router/Load Balancer để chuyển đổi lưu lượng mạng
    keypoint_weight: 0.3
    description: Khi phiên bản mới trên môi trường Green đạt chuẩn kiểm thử, DevOps Engineer thực hiện thay đổi cấu hình định tuyến (DNS hoặc Routing rules) tại tầng Load Balancer để chuyển hướng 100% traffic của người dùng từ Blue sang Green một cách tức thì.
  - id: KP4_3
    content: Cơ chế Rollback lập tức (Zero-Downtime Rollback) khi có sự cố
    keypoint_weight: 0.3
    description: Nếu phiên bản mới phát sinh lỗi nghiêm trọng trên production, hệ thống có thể rollback ngay lập tức bằng cách cấu hình Load Balancer trỏ traffic quay ngược lại về môi trường Blue cũ (vẫn đang chạy ổn định), giúp triệt tiêu thời gian sập hệ thống.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong công cụ quản lý hạ tầng dạng mã (IaC) Terraform, tệp tin `terraform.tfstate` (Statefile) đóng vai trò gì? Tại sao khi làm việc nhóm lớn, chúng ta bắt buộc phải cấu hình Remote State kết hợp với State Locking?
* **expected_key_points:**
  - id: KP5_1
    content: Vai trò lưu trữ nguồn chân lý hạ tầng (Source of Truth) của Statefile
    keypoint_weight: 0.4
    description: Statefile lưu trữ trạng thái thực tế của các tài nguyên hạ tầng đã được tạo ra, giúp Terraform ánh xạ chính xác giữa mã nguồn (.tf) và các tài nguyên vật lý thực tế trên Cloud Provider.
  - id: KP5_2
    content: Rủi ro xung đột dữ liệu hạ tầng khi lưu Statefile cục bộ (Local State)
    keypoint_weight: 0.3
    description: Nếu lưu cục bộ trên máy cá nhân, các kỹ sư khác nhau sẽ không có trạng thái đồng bộ, dẫn đến hiện tượng ghi đè, tạo lặp tài nguyên hoặc xóa nhầm hạ tầng của nhau. Cấu hình Remote State (như AWS S3, GCS) giúp lưu trữ tệp tin tập trung tại một nơi duy nhất.
  - id: KP5_3
    content: Cơ chế khóa file của State Locking chống rủi ro ghi đè đồng thời
    keypoint_weight: 0.3
    description: State Locking (như sử dụng DynamoDB hoặc Redis) đảm bảo rằng tại một thời điểm chỉ có duy nhất một tiến trình thực thi `terraform apply` được quyền can thiệp vào file State. Nếu có người khác cố tình áp dụng hạ tầng cùng lúc, hệ thống sẽ từ chối để ngăn thảm họa hỏng cấu trúc file state.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy trình bày kiến trúc phân tách thành phần cơ bản của một cụm Kubernetes Cluster (K8s). Phân biệt chức năng logic giữa Control Plane (Master Node) và Worker Node.
* **expected_key_points:**
  - id: KP6_1
    content: Chức năng điều phối và quản lý trạng thái cụm của Control Plane (Master Node)
    keypoint_weight: 0.4
    description: Control Plane chịu trách nhiệm đưa ra các quyết định điều phối toàn cụm và duy trì trạng thái mong muốn. Các thành phần cốt lõi gồm: `kube-apiserver` (giao tiếp trung tâm), `etcd` (lưu trữ database trạng thái cụm), `kube-scheduler` (lập lịch phân phối Pods), và `kube-controller-manager` (quản lý các bộ điều khiển trạng thái).
  - id: KP6_2
    content: Chức năng thực thi chạy tải ứng dụng vật lý của Worker Node
    keypoint_weight: 0.4
    description: Worker Node là nơi trực tiếp duy trì hoạt động vật lý của các Pod ứng dụng. Các thành phần bắt buộc phải chạy trên mỗi Worker Node gồm: `kubelet` (tác vụ ngầm giao tiếp với Control Plane để quản lý vòng đời container), `kube-proxy` (quản lý định tuyến traffic mạng nội bộ), và Container Runtime (như containerd).
  - id: KP6_3
    content: Khái niệm đơn vị tính toán nhỏ nhất thông qua Pod
    keypoint_weight: 0.2
    description: Thí sinh cần nêu được Pod là đơn vị nhỏ nhất có thể lập lịch và quản lý trong Kubernetes, đại diện cho một tiến trình đang chạy, chứa một hoặc một nhóm container chia sẻ chung tài nguyên lưu trữ và mạng.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao việc nhúng trực tiếp thông tin bảo mật (Hardcoded Secrets/API Tokens) vào mã nguồn Git lại là một lỗ hổng bảo mật nghiêm trọng? Hãy nêu giải pháp quản lý Secrets an toàn trong một CI/CD Pipeline.
* **expected_key_points:**
  - id: KP7_1
    content: Nguy cơ lộ lọt thông tin diện rộng do đặc tính lưu lịch sử vĩnh viễn của Git
    keypoint_weight: 0.4
    description: Git lưu trữ lịch sử commit vĩnh viễn, việc nhúng cứng secret tạo rủi ro bị lộ lọt thông tin khi repo bị scan, rò rỉ ra ngoài hoặc khi phân quyền cho nhân sự mới, đồng thời làm mất đi khả năng xoay vòng khóa (Secret rotation).
  - id: KP7_2
    content: Sử dụng các công cụ quản lý chuyên biệt (Mã hóa tĩnh - Encryption at rest)
    keypoint_weight: 0.4
    description: Sử dụng các công cụ chuyên dụng như HashiCorp Vault, AWS Secrets Manager hoặc Secret của chính nền tảng CI/CD. Các công cụ này lưu trữ secret dưới dạng mã hóa tĩnh và phân quyền truy cập nghiêm ngặt dựa trên danh tính (IAM/Token).
  - id: KP7_3
    content: Kỹ thuật Inject Secret động vào runtime biến môi trường (Environment Variables)
    keypoint_weight: 0.2
    description: Pipeline CI/CD sẽ gọi API của công cụ quản lý secret tại runtime để kéo dữ liệu về bộ nhớ đệm RAM, nhúng trực tiếp dưới dạng biến môi trường cho ứng dụng và tự động xóa sạch khi kết thúc task, không để lại dấu vết trên đĩa cứng hay mã nguồn.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thành phần lưu trữ trạng thái của Kubernetes (`etcd`) hoạt động dựa trên thuật toán đồng thuận Raft (Raft Consensus Algorithm). Hãy giải thích nguyên lý của khái niệm Quorum và lý do tại sao cụm máy chủ chạy Raft bắt buộc phải thiết lập tổng số Nodes là một số lẻ (3, 5, 7)?
* **expected_key_points:**
  - id: KP8_1
    content: Nguyên lý đạt đa số phiếu của khái niệm Quorum trong Raft
    keypoint_weight: 0.4
    description: Thuật toán Raft yêu cầu hệ thống phải đạt được trạng thái đồng thuận của đa số node để bầu chọn Leader mới hoặc commit dữ liệu thành công. Ngưỡng đa số này gọi là Quorum, được tính bằng công thức toán học: $Q = \lfloor N/2 \rfloor + 1$ (với $N$ là tổng số node trong cụm).
  - id: KP8_2
    content: Cơ chế chống lỗi phân tách mạng (Network Partition / Hiện tượng Split-Brain)
    keypoint_weight: 0.4
    description: Khi xảy ra sự cố đứt kết nối mạng chia đôi cụm cluster làm hai phần độc lập (Network Partition), nếu sử dụng số lượng node chẵn (ví dụ 4 node bị chia đôi thành 2-2), cả hai bên đều không đạt đủ ngưỡng Quorum để hoạt động, hệ thống bị tê liệt. Nếu là số lẻ (ví dụ 5 node bị chia thành 3-2), phân vùng chứa 3 node (đạt Quorum) sẽ tiếp tục hoạt động và ghi dữ liệu, phân vùng còn lại sẽ tự động dừng, ngăn chặn thảm họa bất đồng nhất dữ liệu (Split-Brain).
  - id: KP8_3
    content: Phản tích khả năng chịu lỗi tối ưu của cấu hình số lẻ so với số chẵn liền kề
    keypoint_weight: 0.2
    description: Cấu hình số lẻ tối ưu hóa chi phí tài nguyên và năng lực chịu lỗi. Ví dụ cụm 3 node (Quorum là 2) chịu được 1 node sập ($3-2=1$). Nếu tăng lên 4 node (Quorum tăng lên thành 3), khả năng chịu lỗi vẫn chỉ là 1 node sập ($4-3=1$). Do đó, cụm 4 node không tăng khả năng chịu lỗi so với cụm 3 node nhưng lại tốn thêm chi phí phần cứng và băng thông đồng bộ.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Khi triển khai vi dịch vụ (Microservices), kỹ thuật Canary Deployment kết hợp với Service Mesh (như Istio) giúp kiểm soát lưu lượng mạng chuyên sâu như thế nào? Hãy giải thích cơ chế hoạt động của Envoy Proxy trong việc thực hiện Traffic Splitting dựa trên các thuộc tính của Layer 7 Metadata.
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế điều phối traffic linh hoạt theo tỷ lệ phần trăm độc lập với số lượng Pod
    keypoint_weight: 0.4
    description: Khác với cơ chế phân phối thô sơ của Kubernetes Service gốc, Service Mesh cho phép can thiệp sâu để định tuyến chính xác một tỷ lệ phần trăm nhỏ lưu lượng mạng (ví dụ 1% hoặc 5%) sang phiên bản ứng dụng mới (Canary) để kiểm thử mức độ ổn định mà không cần thay đổi quy mô số lượng Pod vật lý.
  - id: KP9_2
    content: Nguyên lý đánh chặn lưu lượng (Traffic Interception) của Sidecar Envoy Proxy
    keypoint_weight: 0.4
    description: Istio nhúng một container phụ chạy ngầm là Envoy Proxy (Sidecar) nằm chung Pod với Container ứng dụng chính. Mọi lưu lượng mạng đi vào hoặc đi ra khỏi Pod đều bị Envoy Proxy đánh chặn thông qua cấu hình mạng `iptables` của Linux Kernel, giúp thực thi cấu hình định tuyến độc lập với mã nguồn ứng dụng.
  - id: KP9_3
    content: Kỹ thuật định tuyến thông minh dựa trên Layer 7 Metadata (Headers/Cookies)
    keypoint_weight: 0.2
    description: Envoy Proxy phân tích sâu thông tin của gói tin ở tầng ứng dụng (Layer 7). Nó cho phép thiết lập ranh giới định tuyến Canary tinh vi, ví dụ chỉ định tuyến các request chứa HTTP Header cụ thể (`version: canary`) hoặc các request có Cookie thuộc nhóm người dùng thử nghiệm sang Pod Canary, phần còn lại vẫn chạy trên môi trường ổn định cũ.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Để đạt được quy trình cập nhật ứng dụng không gây gián đoạn hệ thống (Zero-Downtime) bằng chiến lược Rolling Update trong Kubernetes, tại sao chỉ dựa vào cấu hình mặc định là chưa đủ? Hãy phân tích sự phối hợp của hai tham số `maxSurge`, `maxUnavailable` và vai trò của `readinessProbe`.
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế toán học điều khiển số lượng Pod biến động của maxSurge và maxUnavailable
    keypoint_weight: 0.4
    description: `maxSurge` quy định số lượng hoặc tỷ lệ phần trăm tối đa các Pod có thể được tạo vượt ngưỡng mong muốn tại runtime trong quá trình cập nhật. `maxUnavailable` quy định số lượng Pod tối đa có thể rơi vào trạng thái không sẵn sàng cùng một lúc. Để cam kết Zero-Downtime, cần cấu hình tinh vi (ví dụ: `maxSurge: 25%`, `maxUnavailable: 0`) để đảm bảo hệ thống luôn có đủ số lượng Pod tối thiểu chịu tải, loại bỏ hoàn toàn rủi ro thiếu hụt tài nguyên gây sập luồng xử lý.
  - id: KP10_2
    content: Bản chất của readinessProbe đối với việc kiểm soát luồng traffic từ Load Balancer
    keypoint_weight: 0.4
    description: `readinessProbe` kiểm tra xem ứng dụng bên trong container thực sự đã sẵn sàng nhận traffic phục vụ người dùng chưa (ví dụ: đã khởi chạy xong kết nối DB, nạp xong bộ đệm cache). Nếu không cấu hình `readinessProbe`, Kubernetes sẽ lập tức đẩy traffic từ Load Balancer vào Pod mới ngay khi container vừa khởi động (Start), gây ra lỗi HTTP 502/503 cho khách hàng do ứng dụng chưa kịp nạp xong các logic bên trong.
  - id: KP10_3
    content: Quy trình phối hợp đồng bộ điều khiển vòng đời cập nhật (Rolling Update Workflow)
    keypoint_weight: 0.2
    description: Trong quá trình dịch chuyển cuốn chiếu, Kubernetes tạo Pod mới (dựa trên maxSurge). Kubelet sẽ chạy liên tục kiểm tra `readinessProbe`. Chỉ khi Pod mới vượt qua bài test này thành công, Kubernetes mới cập nhật Endpoint mạng để trỏ traffic vào nó, và sau đó mới kích hoạt lệnh xóa (terminate) một Pod cũ tương ứng, đảm bảo luồng traffic truyền tải liên tục không đứt quãng.