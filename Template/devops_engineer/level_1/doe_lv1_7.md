# Bộ Câu Hỏi Phỏng Vấn DevOps Engineer (Level 1)

* **Role:** DevOps Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong văn hóa DevOps, phương pháp quản lý Hạ tầng dạng mã (Infrastructure as Code - IaC) là gì? Hãy nêu hai lợi ích cốt lõi của việc áp dụng IaC so với việc cấu hình hạ tầng thủ công (Manual Configuration) thông qua giao diện Web UI.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa bản chất khai báo hạ tầng bằng mã nguồn của IaC
    keypoint_weight: 0.5
    description: Infrastructure as Code (IaC) là phương pháp quản lý, thiết lập và cấp phát tài nguyên hạ tầng máy chủ, mạng, lưu trữ thông qua các tệp tin cấu hình máy tính đọc được (như định dạng YAML, JSON, HCL) thay vì phải thao tác thủ công trên giao diện đồ họa hoặc chạy lệnh script đơn lẻ.
  - id: KP1_2
    content: Lợi ích về tính tự động tái lập và quản lý phiên bản (Version Control)
    keypoint_weight: 0.5
    description: IaC cho phép lưu trữ cấu hình hạ tầng trên Git để quản lý lịch sử phiên bản, giúp rà soát thay đổi (Code Review), giảm thiểu sai sót do con người, và cung cấp năng lực tự động tạo lập lại toàn bộ môi trường giống hệt nhau một cách nhanh chóng, đồng nhất.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế automation script và cấu hình hệ thống bằng các công cụ như Ansible hay Terraform, tính chất "Idempotency" (Tính lũy đẳng) mang ý nghĩa gì? Điều gì xảy ra nếu một câu lệnh cấu hình hạ tầng không thỏa mãn tính chất này?
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa nguyên lý giữ nguyên trạng thái mong muốn của Idempotency
    keypoint_weight: 0.5
    description: Idempotency là đặc tính toán học đảm bảo rằng khi ta thực thi một câu lệnh cấu hình một hoặc nhiều lần liên tiếp trên hệ thống với cùng một tham số đầu vào, kết quả trạng thái cuối cùng thu được của hệ thống luôn giống nhau và không sinh ra tác dụng phụ. Công cụ sẽ tự kiểm tra, nếu hệ thống đã đúng cấu hình thì sẽ bỏ qua và không làm gì cả.
  - id: KP2_2
    content: Hệ quả gây hỏng cấu trúc hệ thống khi câu lệnh không lũy đẳng (Non-idempotent)
    keypoint_weight: 0.5
    description: Nếu một câu lệnh không có tính lũy đẳng (ví dụ: lệnh script thuần `echo "config" >> file.conf`), mỗi lần pipeline chạy lại sẽ liên tục ghi đè hoặc chèn thêm dữ liệu trùng lặp vào file, dẫn đến việc phình to file cấu hình, gây lỗi cú pháp hệ thống và phá vỡ tính nhất quán của hạ tầng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Khi xây dựng một Docker Image từ Dockerfile, cơ chế đóng gói dựa trên cấu trúc phân tầng (Image Layers) hoạt động ra sao? Giải thích cách Docker sử dụng cơ chế lưu bộ đệm (Layer Caching) để tăng tốc độ build Image ở các lần tiếp theo.
* **expected_key_points:**
  - id: KP3_1
    content: Bản chất tích lũy các tầng chỉ đọc (Read-only Layers) của Docker Image
    keypoint_weight: 0.5
    description: Mỗi câu lệnh trong Dockerfile (như RUN, COPY, ADD) khi thực thi sẽ tạo ra một tầng dữ liệu chỉ đọc (Layer) mới lồng lên trên các tầng cũ. Docker Image cuối cùng thực chất là một chuỗi liên kết các tầng dữ liệu được xếp chồng lên nhau một cách có thứ tự.
  - id: KP3_2
    content: Cơ chế kiểm tra thay đổi và tái sử dụng bộ đệm (Layer Caching)
    keypoint_weight: 0.5
    description: Khi build lại Image, Docker sẽ duyệt tuần tự từ trên xuống dưới các câu lệnh trong Dockerfile. Nếu câu lệnh và các file liên quan không có sự thay đổi so với lần build trước, Docker sẽ tái sử dụng lại layer đã có trong bộ đệm (Cache) mà không cần chạy lại câu lệnh đó. Chỉ khi phát hiện một câu lệnh thay đổi, Docker mới build lại layer đó và bắt buộc phải build lại toàn bộ các layer phía sau nó.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy phân biệt sự khác biệt về mặt triết lý vận hành và quy trình sửa lỗi hệ thống giữa mô hình Hạ tầng đột biến (Mutable Infrastructure) và Hạ tầng bất biến (Immutable Infrastructure). Kỹ thuật nào tối ưu hơn cho quy trình tự động hóa CI/CD?
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế chỉnh sửa trực tiếp tại runtime của Mutable Infrastructure và điểm yếu
    keypoint_weight: 0.4
    description: Mutable Infrastructure cho phép các kỹ sư đăng nhập trực tiếp vào server đang chạy (Production) để cài đặt, cập nhật phần mềm hoặc sửa đổi file cấu hình thủ công. Điểm yếu là tạo ra hiện tượng sai lệch cấu hình (Configuration Drift), khiến hạ tầng thực tế không còn giống với thiết kế ban đầu và rất khó đồng bộ trên quy mô lớn.
  - id: KP4_2
    content: Triết lý hủy bỏ và thay mới hoàn toàn của Immutable Infrastructure
    keypoint_weight: 0.4
    description: Immutable Infrastructure quy định tuyệt đối không chỉnh sửa server đang chạy. Khi có phiên bản mới hoặc cần sửa lỗi, hệ thống sẽ tự động build một image mới hoàn chỉnh (như AMI, Docker image), khởi chạy một cụm server mới thay thế và phá hủy vĩnh viễn cụm server cũ, đảm bảo hạ tầng luôn đồng nhất tuyệt đối đúng như mã nguồn.
  - id: KP4_3
    content: Tính tương thích tối ưu đối với luồng tự động hóa CI/CD
    keypoint_weight: 0.2
    description: Thí sinh cần chỉ ra Immutable Infrastructure tối ưu hơn cho CI/CD vì nó triệt tiêu hiện tượng sập hệ thống không rõ nguyên nhân do cấu hình nền, cho phép tự động hóa hoàn toàn quy trình kiểm thử đóng gói từ môi trường Staging sang Production mà không gây sai lệch hành vi ứng dụng.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong cụm Kubernetes (K8s), tài nguyên Network Policy được sử dụng nhằm mục đích gì? Theo cấu hình mặc định ban đầu khi vừa khởi tạo Cluster, luồng giao tiếp mạng giữa các Pods (Pod-to-Pod communication) tuân theo quy tắc bảo mật nào?
* **expected_key_points:**
  - id: KP5_1
    content: Quy tắc mở hoàn toàn (Allow-all) theo cấu hình mạng mặc định của K8s
    keypoint_weight: 0.5
    description: Theo thiết kế mặc định ban đầu của Kubernetes, mọi Pod bên trong cluster đều có thể tự do giao tiếp mạng thẳng với tất cả các Pod khác, bất kể chúng nằm ở các Namespaces khác nhau, không có bất kỳ rào cản tường lửa nào (Non-isolated by default).
  - id: KP5_2
    content: Vai trò can thiệp cô lập và phân quyền Layer 3/4 của Network Policy
    keypoint_weight: 0.5
    description: Network Policy đóng vai trò là một tường lửa mềm (Firewall) được quản lý khai báo bằng mã để kiểm soát luồng traffic mạng đi vào (Ingress) và đi ra (Egress) của các Pods dựa trên các nhãn Labels, Selectors và Cổng mạng Ports, áp dụng nguyên lý bảo mật tối thiểu (Least Privilege) để cô lập các service nhạy cảm.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy phân biệt sự khác biệt cốt lõi về quy trình dịch chuyển container, mức độ ảnh hưởng đến traffic người dùng hằng ngày, và chi phí tài nguyên phần cứng giữa hai chiến lược triển khai ứng dụng của Kubernetes: Recreate Deployment và Rolling Update Deployment.
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế tắt toàn bộ để bật mới của chiến lược Recreate và hệ quả sập luồng traffic
    keypoint_weight: 0.4
    description: Chiến lược Recreate thực hiện tắt và xóa bỏ hoàn toàn tất cả các Pod phiên bản cũ hiện tại trước (Đưa số lượng Pod về 0), sau đó mới tiến hành khởi chạy đồng loạt các Pod phiên bản mới. Quy trình này không tốn thêm tài nguyên phần cứng trung gian nhưng gây ra một khoảng thời gian sập hệ thống hoàn toàn (Downtime), ngắt quãng luồng traffic của người dùng.
  - id: KP6_2
    content: Cơ chế cuốn chiếu thay thế dần dần của chiến lược Rolling Update
    keypoint_weight: 0.4
    description: Rolling Update cập nhật theo cơ chế cuốn chiếu, tạo dần một số lượng nhỏ Pod mới song song với việc xóa bớt một số lượng tương ứng Pod cũ dựa trên cấu hình cấu trúc. Chiến lược này giúp luồng traffic của người dùng luôn được duy trì liên tục không đứt quãng một mili giây nào (Zero Downtime).
  - id: KP6_3
    content: Sự đánh đổi chi phí tài nguyên phần cứng hao phí tại runtime
    keypoint_weight: 0.2
    description: Rolling Update yêu cầu hạ tầng phải có sẵn một lượng tài nguyên RAM/CPU dự phòng (Buffer) để chứa các Pod mới được tạo ra thêm tạm thời trong quá trình cập nhật, ngược lại với Recreate hoàn toàn không yêu cầu phần cứng dư thừa.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi quản lý các ứng dụng lưu trữ trạng thái dữ liệu (Stateful Applications) trên Kubernetes, hãy giải thích vai trò độc lập và mối quan hệ logic gắn kết giữa ba tài nguyên: PersistentVolume (PV), PersistentVolumeClaim (PVC) và StorageClass (SC).
* **expected_key_points:**
  - id: KP7_1
    content: Bản chất cấp phát tài nguyên cứng vật lý của PersistentVolume (PV)
    keypoint_weight: 0.4
    description: PersistentVolume (PV) đại diện cho một phân vùng không gian lưu trữ vật lý thực tế được cấu hình sẵn trong cụm (như AWS EBS, Google Persistent Disk, hoặc NFS), có vòng đời độc lập hoàn toàn với vòng đời của bất kỳ Pod nào sử dụng nó.
  - id: KP7_2
    content: Bản chất câu lệnh yêu cầu, đặc tả dung lượng của PersistentVolumeClaim (PVC)
    keypoint_weight: 0.4
    description: PersistentVolumeClaim (PVC) là một yêu cầu đòi hỏi không gian lưu trữ do người dùng hoặc Pod gửi lên hệ thống. Nó quy định các thông số mong muốn như dung lượng bộ nhớ (Size) và chế độ truy cập (Access Modes như ReadWriteOnce, ReadWriteMany). PVC đóng vai trò như một chiếc vé để K8s tự động tìm kiếm và gắn kết (Bind) vào một PV thích hợp.
  - id: KP7_3
    content: Cơ chế cấp phát động (Dynamic Provisioning) tự động hóa của StorageClass
    keypoint_weight: 0.2
    description: StorageClass (SC) định nghĩa các loại cấu hình lưu trữ và quản lý nhà cung cấp (Provisioner). SC hỗ trợ tính năng Cấp phát động, nghĩa là khi một PVC yêu cầu SC, hệ thống sẽ tự động tạo ra một PV vật lý tương ứng trên Cloud ngay tại runtime mà không cần DevOps Engineer phải tạo PV thủ công từ trước.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong kiến trúc hệ thống mạng nâng cao sử dụng Service Mesh (như Istio), kỹ thuật Traffic Mirroring (hoặc Traffic Shadowing) hoạt động ra sao? Hãy phân tích cách cơ chế này giúp kiểm tra tải thực tế của phiên bản ứng dụng mới trên Production mà hoàn toàn không gây ảnh hưởng đến trải nghiệm của người dùng cuối.
* **expected_key_points:**
  - id: KP8_1
    content: Cơ chế nhân bản lưu lượng mạng bất đồng bộ (Asynchronous traffic duplication) ở tầng Proxy
    keypoint_weight: 0.4
    description: Traffic Mirroring cho phép hệ thống tự động nhân bản (duplicate) toàn bộ hoặc một phần luồng traffic thực tế của người dùng từ Production và gửi bất đồng bộ (Asynchronous) sang phiên bản ứng dụng mới đang thử nghiệm (Canary/Shadow service), chạy song song với luồng xử lý chính.
  - id: KP8_2
    content: Tính năng bỏ qua phản hồi (Response dropping) của luồng Mirrored traffic bảo vệ production
    keypoint_weight: 0.4
    description: Mọi dữ liệu phản hồi (HTTP Responses) sinh ra từ phiên bản thử nghiệm nhận traffic nhân bản sẽ bị tầng Proxy Sidecar (Envoy) chủ động hủy bỏ hoàn toàn và không gửi trả về cho khách hàng. Người dùng cuối chỉ nhận duy nhất kết quả xử lý từ phiên bản Production ổn định cũ, giúp cô lập tuyệt đối rủi ro của code mới.
  - id: KP8_3
    content: Ngữ cảnh đánh giá hiệu năng tải thực tế và phát hiện lỗi logic (Dark launching)
    keypoint_weight: 0.2
    description: Kỹ thuật này giúp doanh nghiệp thực hiện kiểm thử an toàn mức độ chịu tải của phần cứng, đo lường tỷ lệ lỗi với dữ liệu thực tế ngoài đời thực (Real-world payload) mà không gây rủi ro phá vỡ tính toàn vẹn của database hay ảnh hưởng đến trải nghiệm khách hàng hằng ngày.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong các cụm Kubernetes bảo mật cao, cơ chế Token Volume Projection (Service Account Token Volume Projection) được sử dụng để tối ưu hóa an toàn bảo mật. Hãy giải thích thách thức bảo mật của cơ chế gắn token cũ (Legacy Service Account Tokens) và cách cơ chế mới giải quyết vấn đề dựa trên thuộc tính thời gian và phạm vi đối tượng (Audience/Expiration).
* **expected_key_points:**
  - id: KP9_1
    content: Lỗ hổng bảo mật lưu trữ vĩnh viễn không hết hạn của Legacy Service Account Token
    keypoint_weight: 0.4
    description: Trong cơ chế cũ, khi một Pod được tạo ra, Kubernetes tự động sinh ra một Token dạng mã Secret lưu vĩnh viễn trong etcd và gắn trực tiếp vào ổ đĩa của Container. Token này không bao giờ hết hạn (No expiration); nếu tin tặc hack được container và lấy cắp token, chúng có thể chiếm quyền điều khiển cluster vô thời hạn.
  - id: KP9_2
    content: Cơ chế Token Volume Projection tạo khóa động có thời hạn sống ngắn (Short-lived tokens)
    keypoint_weight: 0.4
    description: Cơ chế mới gọi trực tiếp vào API `TokenRequest` để sinh ra các token động nằm trực tiếp trên bộ nhớ đệm RAM (Projected Volume). Các token này bắt buộc phải cấu hình thuộc tính thời hạn sống ngắn (ví dụ: mặc định 1 giờ) và Kubelet chịu trách nhiệm tự động xoay vòng làm mới (rotate) token trước khi hết hạn, giúp giảm thiểu rủi ro lộ lọt khóa.
  - id: KP9_3
    content: Giới hạn ranh giới đối tượng sử dụng qua thuộc tính Audience bound
    keypoint_weight: 0.2
    description: Token mới tích hợp chặt chẽ thuộc tính `Audience`, quy định rõ ràng ranh giới đối tượng hoặc service cụ thể nào được phép tiếp nhận xác thực token này. Nếu token bị mang sang một service khác nằm ngoài phạm vi Audience cấu hình, hệ thống API server sẽ lập tức từ chối xác thực.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong kiến trúc lưu trữ của Docker, các Storage Drivers (như `overlay2`) sử dụng tính năng Copy-on-Write (CoW) để quản lý dữ liệu. Hãy phân tích bản chất quy trình toán học và thao tác vật lý trên đĩa cứng khi một tiến trình bên trong Container thực hiện câu lệnh chỉnh sửa (Write/Modify) một tệp tin lớn vốn đang nằm ở tầng Image lớp dưới.
* **expected_key_points:**
  - id: KP10_1
    content: Bản chất chỉ đọc cố định của các tầng Image layers bên dưới
    keypoint_weight: 0.4
    description: Toàn bộ các layer cấu thành nên Docker Image đều ở trạng thái chỉ đọc tuyệt đối (Read-only). Container khi khởi chạy chỉ được cấp thêm một tầng mỏng ghi đọc nằm ở trên cùng (Container Layer / Writable Layer). Tiến trình không bao giờ được phép sửa đổi trực tiếp dữ liệu trên các tầng Image gốc.
  - id: KP10_2
    content: Quy trình vật lý Copy-on-Write sao chép dữ liệu lên tầng Writable Layer
    keypoint_weight: 0.4
    description: Khi ứng dụng gọi lệnh sửa đổi một file có sẵn từ Image layer, Storage Driver bắt đầu quét tìm vị trí file đó ở các tầng dưới. Tiếp theo, hệ thống thực hiện thao tác Copy-on-Write: sao chép nguyên bản (Copy) toàn bộ tệp tin đó từ tầng chỉ đọc lên trên tầng Container Layer chỉ ghi đọc trên cùng. Thao tác chỉnh sửa thực tế của ứng dụng sẽ chỉ diễn ra trên bản sao mới này.
  - id: KP10_3
    content: Hệ quả trễ thời gian (I/O Latency cổ chai) đối với tác vụ ghi khối lượng lớn
    keypoint_weight: 0.2
    description: Do phải tốn chi phí tìm kiếm và thực hiện phép toán I/O sao chép toàn bộ file qua mạng đĩa cứng ngay tại runtime, bước ghi đầu tiên đối với các file kích thước lớn sẽ bị trễ thời gian xử lý nghiêm trọng (I/O Latency). Đây là lý do các ứng dụng ghi nhiều dữ liệu (như Database) bắt buộc phải sử dụng cơ chế Docker Volumes để ghi trực tiếp xuống đĩa cứng máy chủ, bỏ qua lớp CoW này.