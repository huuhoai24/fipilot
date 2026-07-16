# Bộ Câu Hỏi Phỏng Vấn DevOps Engineer (Level 1)

* **Role:** DevOps Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt sự khác biệt cốt lõi về mặt định nghĩa quy trình và mức độ tự động hóa giữa ba khái niệm: Continuous Integration (CI), Continuous Delivery (CD), và Continuous Deployment.
* **expected_key_points:**
  - id: KP1_1
    content: Bản chất tích hợp và kiểm thử liên tục của CI (Continuous Integration)
    keypoint_weight: 0.3
    description: CI tập trung vào việc tự động hóa quá trình build và chạy kiểm thử (Unit test, Integration test) ngay khi lập trình viên commit mã nguồn mới lên kho lưu trữ chung, nhằm phát hiện lỗi sớm ở mức độ code.
  - id: KP1_2
    content: Cơ chế đóng gói tự động nhưng duyệt triển khai thủ công của Continuous Delivery (CD)
    keypoint_weight: 0.4
    description: Continuous Delivery đảm bảo mã nguồn sau khi vượt qua CI sẽ tự động được đóng gói thành artifact (Docker Image, file nén) và sẵn sàng deploy lên các môi trường (Staging/Production). Điểm mấu chốt là bước phát hành lên Production cuối cùng vẫn yêu cầu sự phê duyệt thủ công (Manual approval) từ con người.
  - id: KP1_3
    content: Tự động hóa hoàn toàn luồng phát hành của Continuous Deployment
    keypoint_weight: 0.3
    description: Continuous Deployment là bước nâng cấp cao nhất, tự động hóa hoàn toàn 100% quy trình. Mọi commit vượt qua các vòng kiểm thử tự động của pipeline sẽ ngay lập tức được deploy trực tiếp lên môi trường Production mà không cần bất kỳ sự can thiệp thủ công nào.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế hạ tầng dạng mã (IaC), hãy phân biệt sự khác biệt về mặt triết lý tiếp cận giữa Declarative (Khai báo - như Terraform) và Imperative (Mệnh lệnh - như Ansible/Bash script) khi thực hiện việc cập nhật số lượng máy chủ.
* **expected_key_points:**
  - id: KP2_1
    content: Triết lý định nghĩa trạng thái mong muốn của Declarative approach
    keypoint_weight: 0.5
    description: Phương pháp Declarative yêu cầu kỹ sư chỉ cần định nghĩa trạng thái cuối cùng mong muốn của hạ tầng (ví dụ: tôi muốn có chính xác 5 máy chủ). Công cụ IaC (như Terraform) sẽ tự tính toán khoảng chênh lệch với thực tế và thực hiện các bước cần thiết để đạt được trạng thái đó.
  - id: KP2_2
    content: Triết lý thực thi từng bước tuần tự của Imperative approach
    keypoint_weight: 0.5
    description: Phương pháp Imperative yêu cầu kỹ sư phải viết rõ từng câu lệnh chỉ dẫn hệ thống thực hiện tuần tự theo các bước (ví dụ: khởi chạy 1 máy chủ, sau đó cấu hình mạng, sau đó thêm vào cụm). Nếu muốn tăng lên 5, kỹ sư phải tự viết script lặp lại hoặc thêm lệnh tạo thêm 4 máy chủ nữa, rất khó kiểm soát trạng thái nếu chạy lại nhiều lần.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Khi quản lý tài nguyên hệ thống trên máy chủ Linux, lệnh `ulimit` cho phép thiết lập cấu hình giới hạn tài nguyên. Hãy phân biệt sự khác biệt cơ bản về quyền hạn thay đổi và mục đích sử dụng giữa hai mức giới hạn: Soft Limit và Hard Limit.
* **expected_key_points:**
  - id: KP3_1
    content: Định nghĩa tính linh hoạt và quyền thay đổi của Soft Limit
    keypoint_weight: 0.5
    description: Soft Limit là giới hạn tài nguyên thực tế đang được áp dụng trực tiếp cho một tiến trình (Process) tại runtime. Người dùng thông thường (Non-root user) có thể chủ động tự tăng hoặc giảm giá trị Soft Limit này tùy ý, miễn là không vượt quá ngưỡng Hard Limit.
  - id: KP3_2
    content: Định nghĩa ranh giới trần cứng nhắc và quyền bảo vệ hệ thống của Hard Limit
    keypoint_weight: 0.5
    description: Hard Limit đóng vai trò như một mức trần tuyệt đối (Ceiling value) của tài nguyên, được quản trị viên hệ thống (Root user) thiết lập để ngăn chặn các tiến trình tiêu tốn quá đà làm sập OS. Người dùng thông thường chỉ có thể giảm chứ không thể tăng Hard Limit nếu không có đặc quyền root.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong cụm Kubernetes Cluster, các Pods nằm trên các Node khác nhau giao tiếp vật lý với nhau như thế nào? Hãy giải thích nguyên lý hoạt động của cơ chế mạng Overlay Network thông qua CNI (Container Network Interface - như Calico, Flannel).
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế gán dải IP duy nhất không chồng lấn cho từng Node
    keypoint_weight: 0.3
    description: CNI quản lý và phân phối cho mỗi Node trong cụm một dải IP con (Subnet CIDR) riêng biệt và không chồng lấn. Mỗi Pod khi được tạo ra trên Node đó sẽ nhận một IP duy nhất trong dải Subnet này, đảm bảo tính định danh toàn cụm.
  - id: KP4_2
    content: Cơ chế đóng gói gói tin gốc của Overlay Network (Encapsulation)
    keypoint_weight: 0.4
    description: Khi Pod A trên Node 1 gửi gói tin đến Pod B trên Node 2, gói tin gốc (chứa IP nội bộ của Pod) sẽ bị CNI đánh chặn và đóng gói (Encapsulation) bằng cách bọc thêm một lớp header mạng vật lý bên ngoài (ví dụ sử dụng giao thức VXLAN hoặc Geneve) chứa địa chỉ IP vật lý của Node 1 và Node 2.
  - id: KP4_3
    content: Cơ chế mở gói tin và định tuyến tại Node đích (Decapsulation)
    keypoint_weight: 0.3
    description: Gói tin bọc ngoài di chuyển qua hạ tầng mạng vật lý thông thường để đến Node 2. Tại đây, CNI Agent trên Node 2 nhận gói tin, thực hiện gỡ bỏ lớp bọc ngoài (Decapsulation) để lấy lại gói tin gốc của Pod và chuyển tiếp trực tiếp vào Pod B thông qua veth pair.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi sử dụng công cụ quản lý cấu hình Ansible cho hạ tầng tự động co giãn (Auto Scaling), tại sao phương pháp khai báo Static Inventory truyền thống lại thất bại? Giải pháp Dynamic Inventory giải quyết vấn đề này dựa trên cơ chế nào?
* **expected_key_points:**
  - id: KP5_1
    content: Điểm hạn chế không thể cập nhật IP của Static Inventory khi hạ tầng co giãn
    keypoint_weight: 0.4
    description: Static Inventory lưu trữ danh sách IP máy chủ cứng nhắc trong file văn bản tĩnh. Khi hệ thống Auto Scaling tự động thêm mới hoặc hủy bỏ các máy chủ (máy chủ mới nhận IP ngẫu nhiên), file tĩnh này sẽ bị lỗi thời ngay lập tức, khiến Ansible không thể cấu hình đúng các máy chủ mới sinh ra.
  - id: KP5_2
    content: Cơ chế gọi API thời gian thực để truy vấn hạ tầng của Dynamic Inventory
    keypoint_weight: 0.4
    description: Dynamic Inventory thay thế file tĩnh bằng một script tự động (hoặc plugin của Ansible). Mỗi khi chạy playbook, script này sẽ trực tiếp gọi API của các Cloud Provider (như AWS, GCP) để truy vấn danh sách các máy chủ đang hoạt động tại thời điểm đó theo thời gian thực.
  - id: KP5_3
    content: Khả năng phân nhóm máy chủ tự động dựa trên Tags/Metadata
    keypoint_weight: 0.2
    description: Dữ liệu trả về từ API được phân tích và phân nhóm tự động dựa trên các thuộc tính nhãn (Tags/Metadata, ví dụ: env=production, role=web), giúp Ansible luôn áp dụng đúng playbook cấu hình lên đúng đối tượng máy chủ mà không cần can thiệp thủ công.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong thiết lập Continuous Integration (CI) Pipeline, hãy phân biệt mục đích sử dụng, phạm vi chia sẻ và thời gian tồn tại giữa hai cơ chế: Caching (Bộ nhớ đệm) và Artifacts (Sản phẩm đầu ra).
* **expected_key_points:**
  - id: KP6_1
    content: Mục đích tối ưu thời gian build và phạm vi cục bộ của Caching
    keypoint_weight: 0.5
    description: Cache được sử dụng để lưu lại các tài nguyên trung gian tốn thời gian tải hoặc biên dịch (như thư mục node_modules, thư viện maven/pip) giữa các lần chạy pipeline khác nhau. Mục đích là để đẩy nhanh tốc độ build, phạm vi lưu trữ thường là cục bộ trên runner và không dùng để chuyển giao sản phẩm chạy.
  - id: KP6_2
    content: Mục đích chuyển giao và tính chất lưu trữ lâu dài của Artifacts
    keypoint_weight: 0.5
    description: Artifact đại diện cho sản phẩm đóng gói cuối cùng của một stage thành công (ví dụ: file .war, .jar, Docker image) cần được chuyển sang các stage sau (như deploy) hoặc lưu trữ lại để phục vụ việc tải về phát hành. Artifact có tính chất định danh phiên bản, được upload lên kho lưu trữ tập trung và có thời hạn tồn tại cấu hình rõ ràng.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi xây dựng hệ thống giám sát hệ thống (Monitoring), hãy phân biệt cơ chế thu thập dữ liệu dạng Pull (Kéo - như Prometheus) và dạng Push (Đẩy - như InfluxDB Telegraf). Nêu ưu điểm lớn nhất của cơ chế Pull đối với việc kiểm soát sức khỏe của các Target cần giám sát.
* **expected_key_points:**
  - id: KP7_1
    content: Bản chất giao tiếp của cơ chế Pull vs Push
    keypoint_weight: 0.4
    description: Cơ chế Pull: Server giám sát chủ động gửi HTTP request theo chu kỳ để cào (scrape) chỉ số từ các Target. Cơ chế Push: Các Target tự cài đặt Agent để chủ động đẩy metrics của mình về phía Server giám sát tập trung.
  - id: KP7_2
    content: Ưu điểm tự động phát hiện sập nguồn (Dead target detection) của cơ chế Pull
    keypoint_weight: 0.4
    description: Với cơ chế Pull, nếu Server không thể kết nối tới Target sau một số lần thử, nó lập tức xác định ngay Target đó đã bị sập (State: DOWN) và kích hoạt cảnh báo. Với cơ chế Push, khi Target sập, nó đơn giản là dừng đẩy metrics; Server rất khó phân biệt giữa việc Target bị chết hay mạng bị nghẽn tạm thời nếu không cấu hình timeout phức tạp.
  - id: KP7_3
    content: Khả năng bảo vệ máy chủ giám sát khỏi quá tải (Overload protection)
    keypoint_weight: 0.2
    description: Cơ chế Pull giúp Server giám sát tự làm chủ tần suất cào dữ liệu, ngăn ngừa rủi ro Server bị tràn ngập dữ liệu (DDOS vô ý) khi số lượng các container ứng dụng đột ngột tăng lên hàng ngàn thực thể cùng lúc.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Hãy giải thích kiến trúc thiết kế và nguyên lý hoạt động của Kubernetes Operator Pattern. Làm thế nào một Operator có thể tự động hóa các tác vụ quản lý ứng dụng phức tạp (như cài đặt, backup, scale một cụm Database) dựa trên Custom Resource Definitions (CRDs) và Reconcile Loop?
* **expected_key_points:**
  - id: KP8_1
    content: Khái niệm mở rộng Kubernetes API thông qua CRD (Custom Resource Definition)
    keypoint_weight: 0.3
    description: Operator định nghĩa ra một thực thể tài nguyên mới dành riêng cho ứng dụng đó thông qua CRD (ví dụ: `kind: PostgresDatabase`). CRD này mở rộng Kubernetes API cho phép người dùng khai báo cấu trúc ứng dụng phức tạp như một tài nguyên K8s gốc.
  - id: KP8_2
    content: Cơ chế vận hành của Custom Controller lưu trữ logic nghiệp vụ
    keypoint_weight: 0.4
    description: Operator chứa một Custom Controller chạy ngầm để lắng nghe các sự kiện liên quan đến CRD đó. Controller này chứa mã nguồn đóng gói toàn bộ tri thức của một người quản trị hệ thống (như cách khởi tạo slave, cách đồng bộ master-slave, cách chạy câu lệnh backup vật lý).
  - id: KP8_3
    content: Vòng lặp hòa giải tự động (Reconciliation Loop) duy trì tính toàn vẹn ứng dụng phức tạp
    keypoint_weight: 0.3
    description: Controller liên tục chạy vòng lặp Reconcile so sánh giữa Live State của DB thực tế và Desired State khai báo trong CRD. Nếu phát hiện Slave bị hỏng, nó tự động kích hoạt logic nghiệp vụ để tạo lại Slave mới, tự động thực hiện cấu hình liên kết, gán IP và đồng bộ dữ liệu mà không cần con người can thiệp.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong thiết kế hạ tầng cơ sở dữ liệu có tính sẵn sàng cao (High Availability Database) sử dụng công cụ DCS (Distributed Consensus Store - như etcd, Consul), hiện tượng Split-Brain là gì? Hãy giải thích giải pháp kỹ thuật sử dụng DCS kết hợp cơ chế Fencing (như STONITH) để giải quyết triệt để rủi ro này.
* **expected_key_points:**
  - id: KP9_1
    content: Bản chất hủy hoại dữ liệu của hiện tượng Split-Brain khi đứt liên kết mạng
    keypoint_weight: 0.4
    description: Split-Brain xảy ra khi kết nối mạng giữa hai phân vùng DB bị đứt. Cả hai phía (ví dụ Active và Standby cũ) đều tự nhận mình là Master duy nhất và tiếp tục ghi dữ liệu độc lập. Khi mạng kết nối lại, dữ liệu bị xung đột nghiêm trọng và không thể tự phục hồi phục.
  - id: KP9_2
    content: Cơ chế khóa phân tán (Distributed Lock / Lease) của DCS bảo vệ quyền Master độc nhất
    keypoint_weight: 0.4
    description: Hệ thống sử dụng một cụm DCS tập trung (như etcd) để quản lý một khóa phân tán (Leader Lock) đi kèm cơ chế gia hạn tự động (Lease). Chỉ có node nào giữ được khóa trong etcd mới được quyền làm Master ghi dữ liệu. Khi mạng đứt, node bị cô lập không thể liên lạc với cụm etcd sẽ tự động bị mất khóa Lease và phải tự hạ cấp xuống Read-only.
  - id: KP9_3
    content: Kỹ thuật trừng phạt vật lý Fencing (STONITH) để triệt tiêu hoàn toàn rủi ro ghi đè trùng lặp
    keypoint_weight: 0.2
    description: Để đề phòng trường hợp node Master cũ bị đơ (hung state) chưa kịp nhả khóa nhưng vẫn cố ghi xuống đĩa, hệ thống áp dụng cơ chế Fencing mạnh bạo - STONITH (Shoot The Other Node In The Head). Node Master mới được bầu chọn sẽ gọi API phần cứng (IPMI/PDU) để lập tức ngắt nguồn điện vật lý hoặc restart cứng node Master cũ, đảm bảo an toàn dữ liệu tuyệt đối.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Khi áp dụng DevSecOps vào luồng CI/CD tự động hóa, hãy phân biệt phạm vi quét lỗi bảo mật và thời điểm thực thi của hai kỹ thuật: SAST (Static Application Security Testing) và DAST (Dynamic Application Security Testing). Trình bày phương pháp tự động xử lý hiện tượng cảnh báo giả (False Positives) trong pipeline để tránh làm nghẽn luồng build.
* **expected_key_points:**
  - id: KP10_1
    content: Bản chất phân tích mã nguồn thô của SAST ở giai đoạn đầu pipeline
    keypoint_weight: 0.3
    description: SAST thực hiện quét trực tiếp trên mã nguồn tĩnh (Source code thô) trước khi build để phát hiện các lỗ hổng cú pháp, cấu hình cứng, hoặc hàm nguy hiểm (SQL Injection, XSS) dựa trên các bộ quy tắc định sẵn. Chạy rất sớm ngay sau bước code checkout.
  - id: KP10_2
    content: Bản chất tấn công giả lập hộp đen của DAST ở giai đoạn sau deploy
    keypoint_weight: 0.3
    description: DAST là kiểm thử hộp đen (Black-box testing), quét ứng dụng khi nó đang chạy thực tế trên một môi trường (như Staging). DAST giả lập các cuộc tấn công từ bên ngoài mạng để tìm kiếm các lỗi về cấu hình server, quyền hạn, phiên làm việc (session hijacking). Chạy ở giai đoạn muộn sau khi deploy thành công.
  - id: KP10_3
    content: Kỹ thuật tự động hóa lọc lỗi bằng cơ chế Baseline và Severity Thresholds
    keypoint_weight: 0.4
    description: Để tránh False Positives làm nghẽn pipeline, DevOps tích hợp file cấu hình bỏ qua danh sách lỗi đã xác nhận an toàn (Vulnerability Baseline / Ignore list). Đồng thời, thiết lập bộ lọc ngưỡng nghiêm trọng (Severity thresholds - ví dụ chỉ block pipeline khi phát hiện lỗi mức HIGH/CRITICAL), các lỗi mức LOW/MEDIUM sẽ được ghi nhận vào dashboard bảo mật để rà soát sau thay vì dừng luồng build.