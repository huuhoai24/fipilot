# Bộ Câu Hỏi Phỏng Vấn DevOps Engineer (Level 1)

* **Role:** DevOps Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong các hệ thống tự động hóa CI/CD Pipeline (như Jenkins, GitHub Actions), cơ chế Webhook hoạt động ra sao? Hãy phân biệt sự khác biệt về mặt kiến trúc giao tiếp giữa Webhook và cơ chế Polling truyền thống.
* **expected_key_points:**
  - id: KP1_1
    content: Nguyên lý đẩy dữ liệu theo sự kiện (Event-driven) của Webhook
    keypoint_weight: 0.5
    description: Webhook hoạt động theo cơ chế hướng sự kiện (Push model). Khi có một hành động cụ thể xảy ra trên Source Control (như Git Commit, Pull Request), hệ thống nguồn sẽ tự động gửi một HTTP POST request chứa payload dữ liệu đến một URL cấu hình trước trên CI/CD Server để kích hoạt pipeline tức thì.
  - id: KP1_2
    content: Nguyên lý kéo dữ liệu theo chu kỳ (Pull model) của Polling và điểm yếu
    keypoint_weight: 0.5
    description: Polling hoạt động theo cơ chế kéo (Pull model), trong đó CI/CD Server phải liên tục chủ động gửi request theo chu kỳ thời gian cố định (ví dụ mỗi 5 phút) để hỏi Git Server xem có mã nguồn mới hay không. Cơ chế này gây trễ thời gian kích hoạt pipeline và lãng phí tài nguyên băng thông mạng khi không có thay đổi nào phát sinh.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Khi thiết kế hạ tầng mạng cho ứng dụng, Load Balancer (Bộ cân bằng tải) có thể hoạt động ở Layer 4 hoặc Layer 7 của mô hình OSI. Hãy phân biệt sự khác biệt cốt lõi về loại thông tin mà hai loại Load Balancer này sử dụng để định tuyến lưu lượng (Traffic Routing).
* **expected_key_points:**
  - id: KP2_1
    content: Cơ chế định tuyến tầng giao vận (Transport Layer) của Layer 4 Load Balancing
    keypoint_weight: 0.5
    description: Layer 4 Load Balancer hoạt động ở tầng giao vận (TCP/UDP). Nó đưa ra quyết định điều phối lưu lượng mạng dựa trên các thông tin thuần túy về gói tin như địa chỉ IP nguồn/đích và số cổng Port nguồn/đích, hoàn toàn không mở hay phân tích nội dung bên trong gói tin dữ liệu ứng dụng.
  - id: KP2_2
    content: Cơ chế định tuyến tầng ứng dụng (Application Layer) của Layer 7 Load Balancing
    keypoint_weight: 0.5
    description: Layer 7 Load Balancer hoạt động ở tầng ứng dụng (HTTP/HTTPS). Nó có khả năng mở gói tin và phân tích sâu các thông tin ứng dụng bên trong như HTTP URL path, HTTP Headers, Cookies, hoặc nội dung form dữ liệu để đưa ra các quyết định định tuyến thông minh (ví dụ: chuyển request /api sang cụm server backend).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao trong các hệ thống phân tán chạy microservices, việc cấu hình hệ thống Ghi log tập trung (Centralized Logging - như ELK Stack, EFK Stack) lại là yêu cầu bắt buộc so với việc lưu trữ tệp tin log truyền thống trên từng máy chủ cục bộ?
* **expected_key_points:**
  - id: KP3_1
    content: Khuyết điểm mất dấu vết điều tra khi lưu log cục bộ (Local logs fragmentation)
    keypoint_weight: 0.5
    description: Khi ứng dụng phân tán chạy trên hàng chục máy chủ hoặc container tự động co giãn, log bị chia cắt rải rác ở nhiều nơi. Nếu một container bị sập và xóa bỏ (Terminated), toàn bộ log cục bộ bên trong đĩa cứng của container đó sẽ bị mất vĩnh viễn, khiến kỹ sư không thể tra cứu nguyên nhân gốc rễ (Root cause analysis).
  - id: KP3_2
    content: Cơ chế thu thập tập trung và chuẩn hóa dữ liệu phục vụ điều tra sự cố tức thời
    keypoint_weight: 0.5
    description: Centralized Logging sử dụng các Agent (như Fluentd, Logstash, Vector) chạy ngầm để liên tục đẩy log thời gian thực về một database tập trung (như Elasticsearch). Giúp DevOps dễ dàng tìm kiếm, lọc, tương quan dòng sự kiện xuyên suốt nhiều service và theo dõi biểu đồ lỗi tập trung trên một giao diện duy nhất (Kibana).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong kỹ thuật đóng gói ứng dụng bằng Docker, tại sao kỹ thuật Multi-stage Builds lại được khuyến nghị áp dụng khi viết Dockerfile? Hãy giải thích cơ chế này giúp tối ưu hóa dung lượng Image và tính bảo mật của hệ thống ra sao.
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế phân rã nhiều giai đoạn độc lập trong một Dockerfile
    keypoint_weight: 0.4
    description: Multi-stage Builds cho phép sử dụng nhiều câu lệnh `FROM` trong cùng một file cấu hình Dockerfile. Mỗi stage có thể sử dụng một Base Image khác nhau và kỹ sư có thể chủ động sao chép các tệp tin sản phẩm (Artifacts) từ stage này sang stage khác.
  - id: KP4_2
    content: Cơ chế loại bỏ các công cụ biên dịch để giảm dung lượng Image cuối (Artifact isolation)
    keypoint_weight: 0.3
    description: Giai đoạn đầu (Build stage) dùng image đầy đủ chứa các trình biên dịch (SDK, Maven, npm) để build source code ra file chạy. Giai đoạn cuối (Runtime stage) chỉ dùng một image tối giản (như Alpine, Distroless) và copy duy nhất file chạy đã đóng gói sang, loại bỏ toàn bộ mã nguồn thô và bộ cài nặng, giúp dung lượng image giảm từ hàng GB xuống vài chục MB.
  - id: KP4_3
    content: Tăng cường tính bảo mật nhờ thu hẹp diện tích tấn công (Attack surface reduction)
    keypoint_weight: 0.3
    description: Việc loại bỏ hoàn toàn các trình biên dịch, công cụ hệ thống (như curl, bash, package manager) ra khỏi production image giúp thu hẹp tối đa diện tích tấn công của hệ thống. Nếu tin tặc có xâm nhập được vào container, chúng cũng không có sẵn công cụ để tải mã độc hoặc thực thi các câu lệnh leo thang đặc quyền.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Phương pháp quản lý hạ tầng và triển khai ứng dụng theo trường phái GitOps (sử dụng các công cụ như ArgoCD hoặc FluxCD) hoạt động dựa trên nguyên lý cốt lõi nào? Hãy giải thích cơ chế tự động đồng bộ trạng thái (Automated Reconciliation Loop).
* **expected_key_points:**
  - id: KP5_1
    content: Nguyên lý coi Git repository là nguồn chân lý duy nhất (Source of Truth)
    keypoint_weight: 0.4
    description: Trong cấu trúc GitOps, toàn bộ trạng thái mong muốn của hạ tầng và ứng dụng (K8s Manifests, Helm Charts) bắt buộc phải được khai báo dưới dạng mã (Declarative) và lưu trữ tập trung trên Git repository. Mọi thay đổi trên cluster chỉ được thực hiện thông qua việc chỉnh sửa mã nguồn trên Git.
  - id: KP5_2
    content: Cơ chế vòng lặp hòa giải tự động (Reconciliation Loop) phát hiện độ lệch trạng thái
    keypoint_weight: 0.4
    description: ArgoCD/FluxCD cài đặt một Controller chạy liên tục bên trong K8s cluster để thực hiện vòng lặp hòa giải. Nó liên tục so sánh trạng thái khai báo trên Git (Desired State) và trạng thái thực tế đang chạy trên cluster (Live State) để phát hiện ra sự sai lệch cấu hình.
  - id: KP5_3
    content: Cơ chế tự động sửa lỗi và chống thay đổi thủ công (Configuration Drift prevention)
    keypoint_weight: 0.2
    description: Nếu phát hiện có độ lệch (Configuration Drift - ví dụ một kỹ sư cố tình dùng lệnh kubectl để sửa thủ công cấu hình trên cụm), GitOps Controller sẽ kích hoạt cơ chế đồng bộ, tự động đè cấu hình chuẩn từ Git vào cụm cluster hoặc gửi cảnh báo, đảm bảo hạ tầng luôn nhất quán đúng với mã nguồn.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong quản lý cấu hình hạ tầng (Configuration Management), công cụ Ansible hoạt động theo cơ chế Agentless (Không sử dụng Agent). Hãy giải thích nguyên lý giao tiếp vật lý của Ansible đến các Server đích và nêu ưu điểm của kiến trúc này đối với việc bảo trì hệ thống.
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế giao tiếp đẩy qua giao thức mạng tiêu chuẩn (SSH/WinRM)
    keypoint_weight: 0.5
    description: Ansible không yêu cầu cài đặt bất kỳ phần mềm tác vụ ngầm (Agent) nào lên các máy chủ đích (Managed Nodes). Thao tác quản lý được thực thi từ Control Machine thông qua các giao thức truyền tải mạng tiêu chuẩn có sẵn của hệ điều hành như SSH (cho Linux) hoặc WinRM (cho Windows) để đẩy và thực thi các module python tạm thời.
  - id: KP6_2
    content: Ưu điểm tối ưu chi phí vận hành và tăng tính bảo mật cho hệ thống phần cứng
    keypoint_weight: 0.5
    description: Kiến trúc Agentless giúp triệt tiêu hoàn toàn chi phí tài nguyên CPU/RAM hao phí cho việc duy trì agent trên hàng ngàn máy chủ, loại bỏ gánh nặng bảo trì nâng cấp phiên bản agent hằng ngày, và giảm thiểu rủi ro bảo mật vì hệ thống không phải mở thêm bất kỳ port lạ hay duy trì các daemon có đặc quyền cao ngoài port SSH tiêu chuẩn.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi xây dựng hệ thống Giám sát năng lực hạ tầng (Observability), ba trụ cột cốt lõi bao gồm: Metrics, Logs và Traces. Hãy phân biệt mục đích sử dụng đặc thù của từng thành phần này trong quy trình phát hiện và xử lý sự cố.
* **expected_key_points:**
  - id: KP7_1
    content: Vai trò định lượng hệ thống và cảnh báo sớm của Metrics
    keypoint_weight: 0.4
    description: Metrics là dữ liệu số dạng chuỗi thời gian (Time-series) đo lường các chỉ số hiệu năng hệ thống (như CPU utilization, RAM usage, Request Count, Error Rate). Metrics có kích thước nhẹ, tối ưu để vẽ biểu đồ Dashboard (Prometheus/Grafana) và thiết lập các ngưỡng kích hoạt cảnh báo sớm (Alerting) khi hệ thống quá tải.
  - id: KP7_2
    content: Vai trò ghi vết chi tiết dòng sự kiện của Logs
    keypoint_weight: 0.3
    description: Logs là các bản ghi chuỗi văn bản có mốc thời gian, ghi lại chi tiết các sự kiện rời rạc xảy ra bên trong mã nguồn ứng dụng (như Exception stack trace, Database connection timeout). Logs được dùng để điều tra, phân tích sâu hành vi hệ thống nhằm tìm ra nguyên nhân cụ thể gây lỗi sau khi nhận được cảnh báo từ Metrics.
  - id: KP7_3
    content: Vai trò theo dõi luồng di chuyển xuyên suốt dịch vụ của Traces
    keypoint_weight: 0.3
    description: Traces (Distributed Tracing - như Jaeger, OpenTelemetry) cung cấp cái nhìn toàn cảnh về hành trình di chuyển của một request cụ thể đi xuyên qua hàng loạt microservices khác nhau trong hệ thống phân tán. Traces giúp kỹ sư định vị chính xác vị trí service nào đang bị nghẽn cổ chai (Latency bottleneck) hoặc gây lỗi dây chuyền cho toàn hệ thống.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong kiến trúc mã nguồn vi dịch vụ (Microservices) chạy trên Kubernetes, hệ thống Service Mesh (như Istio) cung cấp tính năng Bảo mật mạng thông qua cơ chế Mutual TLS (mTLS). Hãy giải thích bản chất quy trình toán học thiết lập mã hóa đầu cuối mTLS giữa hai dịch vụ độc lập và cách nó ngăn chặn các cuộc tấn công nghe lén (Man-in-the-Middle).
* **expected_key_points:**
  - id: KP8_1
    content: Cơ chế xác thực chứng chỉ số hai chiều (Bi-directional cryptographic handshake)
    keypoint_weight: 0.4
    description: Khác với TLS thông thường (chỉ Client xác thực Server), mTLS yêu cầu cả hai đầu kết nối phải chủ động trình diễn chứng chỉ số X.509 để xác thực danh tính lẫn nhau. Quá trình bắt tay (Handshake) thiết lập phép toán kiểm tra chữ ký số dựa trên cặp khóa Public/Private Key, chứng minh cả hai service đều hợp pháp trong cụm.
  - id: KP8_2
    content: Quy trình mã hóa đối xứng luồng dữ liệu runtime bằng khóa phiên (Session Key)
    keypoint_weight: 0.4
    description: Sau khi xác thực danh tính thành công qua mật mã bất đối xứng, hai bên sẽ tự động tính toán thỏa thuận ra một Khóa phiên đối xứng chung (Symmetric Session Key) thông qua các giải thuật như Diffie-Hellman. Toàn bộ dữ liệu truyền tải thực tế chạy trên đường truyền mạng (Data plane) từ thời điểm này sẽ được mã hóa bằng khóa phiên này, triệt tiêu hoàn toàn rủi ro bị tấn công nghe lén (Sniffing) hoặc giả mạo gói tin (Man-in-the-Middle).
  - id: KP8_3
    content: Vai trò quản lý và tự động xoay vòng khóa của thành phần Citadel / Istiod CA
    keypoint_weight: 0.2
    description: Tiến trình quản lý, cấp phát chứng chỉ số X.509 cho các Envoy Proxy Sidecar được điều khiển tập trung bởi Certificate Authority nội bộ (như Istiod CA). Hệ thống tự động thiết lập thời hạn sống ngắn cho các chứng chỉ số (Short-lived certificates) và tự động xoay vòng khóa (Automatic certificate rotation) để bảo vệ hạ tầng tĩnh.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Đối với hạ tầng lưu trữ phân tán quy mô lớn (như giải pháp lưu trữ Ceph), việc định vị vị trí lưu trữ dữ liệu thô trên hàng ngàn ổ đĩa cứng không sử dụng cơ chế bảng tra cứu tập trung (Metadata Lookup Table) mà dựa vào giải thuật CRUSH (Controlled Replication Under Scalable Hashing). Hãy giải thích nguyên lý toán học hoạt động và ưu điểm của giải thuật này đối với năng lực mở rộng hạ tầng Big Data.
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế tính toán vị trí trực tiếp dựa trên hàm băm và sơ đồ phân cấp thiết bị (Cluster Map)
    keypoint_weight: 0.4
    description: Giải thuật CRUSH loại bỏ việc tra cứu bảng dữ liệu tĩnh. Khi có một request đọc/ghi dữ liệu (Object), CRUSH tiếp nhận ID của Object kết hợp với sơ đồ cấu trúc vật lý hiện tại của phòng máy (Cluster Map - phân tầng từ Rack, Row, đến từng Node, OSD) chạy qua một hàm băm deterministic để tính toán trực tiếp ra chính xác tọa độ danh sách các ổ đĩa cứng (OSDs) chứa dữ liệu đó.
  - id: KP9_2
    content: Triệt tiêu điểm nghẽn tài nguyên và lỗi chí tử độc điểm (Single Point of Failure)
    keypoint_weight: 0.4
    description: Trong các hệ thống cũ, khi dung lượng dữ liệu tăng lên hàng Petabyte, bảng tra cứu metadata tập trung sẽ phình to khủng khiếp, gây nghẽn băng thông bộ nhớ RAM và CPU của Master Node. CRUSH giải quyết bài toán này vì mọi Client đều tự tính toán được vị trí lưu trữ độc lập bằng CPU của chính nó, loại bỏ hoàn toàn điểm nghẽn trung tâm và triệt tiêu lỗi chí tử Single Point of Failure của kiến trúc lưu trữ.
  - id: KP9_3
    content: Phân bổ lại dữ liệu tối thiểu và cân bằng toán học khi mở rộng/co rút phần cứng
    keypoint_weight: 0.2
    description: Về mặt toán học, khi thêm hoặc bớt một số lượng ổ đĩa cứng vào cụm, giải thuật CRUSH đảm bảo tính chất băm nhất quán (Consistent hashing-like), chỉ dịch chuyển một lượng dữ liệu tối thiểu tương ứng với tỷ lệ phần cứng thay đổi để cân bằng tải lại hệ thống, tránh hiện tượng di chuyển dữ liệu ồ ạt làm sập băng thông mạng nội bộ phòng máy.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Khi thiết kế hạ tầng Khôi phục sau thảm họa (Disaster Recovery - DR) quy mô toàn cầu theo mô hình Multi-Region Active-Active, hãy định nghĩa bản chất của hai chỉ số RTO (Recovery Time Objective) và RPO (Recovery Point Objective). Hãy phân tích thách thức toán học lớn nhất liên quan đến định lý CAP (CAP Theorem) khi đồng bộ dữ liệu Database giữa các vùng địa lý cách xa nhau.
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa bản chất đo lường thời gian của chỉ số RTO và mức độ mất dữ liệu của RPO
    keypoint_weight: 0.4
    description: RTO là mục tiêu thời gian khôi phục, đo lường khoảng thời gian tối đa cho phép hệ thống bị sập cho đến khi khôi phục hoạt động bình thường. RPO là mục tiêu điểm khôi phục, đo lường lượng dữ liệu tối đa (tính theo đơn vị thời gian như vài giây, vài phút) chấp nhận bị mất mát vĩnh viễn do sự cố gây ra. Trong mô hình Active-Active, mục tiêu tối thượng là kéo sát RTO và RPO về bằng 0 tuyệt đối.
  - id: KP10_2
    content: Giới hạn vật lý về độ trễ mạng (Speed of light limitation) và thách thức nhất quán của định lý CAP
    keypoint_weight: 0.4
    description: Do giới hạn vật lý của vận tốc ánh sáng truyền trong cáp quang, việc truyền thông tin giữa hai vùng địa lý (ví dụ Mỹ và Singapore) luôn tốn một khoảng thời gian độ trễ mạng (Network Latency) tối thiểu từ vài chục đến hàng trăm mili giây. Theo định lý CAP, khi xảy ra sự cố đứt kết nối hoặc trễ mạng (Partition Tolerance - P), hệ thống buộc phải lựa chọn đánh đổi giữa: **Consistency (Tính nhất quán tuyệt đối - C)** hoặc **Availability (Tính sẵn sàng cao - A)**.
  - id: KP10_3
    content: Sự đánh đổi kỹ thuật giữa đồng bộ hóa thời gian thực (Synchronous) và bất đồng bộ (Asynchronous)
    keypoint_weight: 0.2
    description: Nếu chọn tính nhất quán (C - Synchronous Replication), mọi transaction ghi dữ liệu ở Region A bắt buộc phải đợi Region B phản hồi xác nhận thành công mới trả kết quả cho khách hàng; điều này làm tăng mạnh độ trễ ứng dụng hằng ngày, kéo tụt hiệu năng hệ thống. Nếu chọn tính sẵn sàng (A - Asynchronous Replication), dữ liệu được ghi tức thì ở Region A và đẩy bất đồng bộ về Region B; điều này giúp ứng dụng chạy cực nhanh nhưng nếu Region A sập đột ngột, lượng dữ liệu chưa kịp đồng bộ sang Region B sẽ bị mất vĩnh viễn, vi phạm chỉ số nghiêm ngặt RPO = 0.