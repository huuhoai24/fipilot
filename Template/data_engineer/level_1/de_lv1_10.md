# Bộ Câu Hỏi Phỏng Vấn Data Engineer (Level 1)

* **Role:** Data Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong quản trị hệ thống cơ sở dữ liệu, hãy phân biệt điểm khác biệt cơ bản về mục đích sử dụng và cơ chế hoạt động giữa hai kỹ thuật sao lưu dữ liệu: Full Backup (Sao lưu toàn bộ) và Incremental Backup (Sao lưu tăng trưởng).
* **expected_key_points:**
  - id: KP1_1
    content: Bản chất và tần suất hoạt động của Full Backup
    keypoint_weight: 0.5
    description: Full Backup sao chép toàn bộ dữ liệu hiện có trong hệ thống tại một thời điểm. Kỹ thuật này an toàn, dễ khôi phục nhất nhưng tiêu tốn rất nhiều không gian lưu trữ và thời gian thực thi, nên thường được chạy định kỳ với tần suất thấp (ví dụ: hàng tuần).
  - id: KP1_2
    content: Bản chất và tần suất hoạt động của Incremental Backup
    keypoint_weight: 0.5
    description: Incremental Backup chỉ sao lưu phần dữ liệu mới được thêm vào hoặc thay đổi kể từ lần sao lưu gần nhất (bất kể là Full hay Incremental). Kỹ thuật này chạy rất nhanh và tiết kiệm dung lượng đĩa cứng, nên thường chạy hằng ngày, nhưng quy trình khôi phục phức tạp hơn vì cần ghép chuỗi các bản sao lưu lại.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Khi thu thập và xử lý luồng dữ liệu (Data Pipelines), thành phần hàng đợi tin nhắn (Message Queue / Message Broker - như Apache Kafka, RabbitMQ) đóng vai trò logic gì và giải quyết bài toán thắt nút cổ chai nào giữa hệ thống nguồn và hệ thống đích?
* **expected_key_points:**
  - id: KP2_1
    content: Vai trò làm bộ đệm trung gian phi đồng bộ (Decoupling)
    keypoint_weight: 0.5
    description: Message Queue đóng vai trò làm vùng đệm lưu trữ tạm thời tách biệt hoàn toàn hệ thống tạo dữ liệu (Producer) và hệ thống tiêu thụ dữ liệu (Consumer). Giúp hai hệ thống hoạt động độc lập không đồng bộ, không phụ thuộc trực tiếp vào nhau.
  - id: KP2_2
    content: Cơ chế giảm tải hệ thống (Backpressure / Rate Limiting)
    keypoint_weight: 0.5
    description: Giải quyết bài toán thắt nút cổ chai hiệu năng khi tốc độ sinh dữ liệu từ nguồn quá nhanh vượt quá khả năng xử lý của hệ thống đích. Message Queue giữ lại dữ liệu an toàn, cho phép hệ thống đích kéo dữ liệu về xử lý tuần tự theo năng lực thực tế mà không bị sập nguồn.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt điểm khác nhau cốt lõi về cách thức tổ chức lưu trữ dữ liệu và ngữ cảnh áp dụng hiệu quả giữa Cơ sở dữ liệu hướng tài liệu (Document-oriented NoSQL - như MongoDB) và Cơ sở dữ liệu hướng đồ thị (Graph NoSQL - như Neo4j).
* **expected_key_points:**
  - id: KP3_1
    content: Cấu trúc và ứng dụng của Document-oriented Database
    keypoint_weight: 0.5
    description: Lưu trữ dữ liệu dưới dạng các cặp khóa-giá trị nằm trong các tài liệu bán cấu trúc (JSON/BSON). Mỗi tài liệu độc lập và tự chứa thông tin của chính nó, cấu trúc schema linh hoạt, tối ưu cho việc đọc/ghi các bản ghi thực thể phức tạp đơn lẻ (như thông tin user profile, catalog sản phẩm).
  - id: KP3_2
    content: Cấu trúc và ứng dụng của Graph Database
    keypoint_weight: 0.5
    description: Lưu trữ dữ liệu dựa trên kiến trúc lý thuyết đồ thị gồm các Đỉnh (Nodes/Vertices) đại diện cho thực thể và các Cạnh (Edges/Relationships) đại diện cho mối liên kết trực tiếp giữa các thực thể đó. Tối ưu cho việc truy vấn phân tích các mối quan hệ chằng chịt, phức tạp với hiệu năng cực cao (như mạng xã hội, hệ thống gợi ý, phát hiện gian lận thẻ tín dụng).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi lưu trữ và nạp dữ liệu lớn vào hồ dữ liệu (Data Lake), hãy phân biệt sự khác biệt về mặt kỹ thuật, ưu và nhược điểm giữa hai thuật toán nén dữ liệu phổ biến: GZIP và SNAPPY.
* **expected_key_points:**
  - id: KP4_1
    content: Đặc tính nén cao và chi phí CPU của thuật toán GZIP
    keypoint_weight: 0.5
    description: GZIP cung cấp tỷ lệ nén dữ liệu cực kỳ cao, giúp tiết kiệm tối đa không gian lưu trữ đĩa cứng. Đổi lại, nó tiêu tốn nhiều tài nguyên CPU và thời gian để nén/giải nén, đồng thời file GZIP không có tính chất chia tách được (Non-splittable), gây hạn chế khi chạy phân tán. Phù hợp lưu trữ dữ liệu lạnh (Cold data).
  - id: KP4_2
    content: Đặc tính tốc độ và khả năng phân tán của thuật toán SNAPPY
    keypoint_weight: 0.5
    description: SNAPPY ưu tiên tối đa hóa tốc độ nén và giải nén cực nhanh với chi phí CPU rất thấp, chấp nhận tỷ lệ nén dữ liệu thô kém hơn GZIP. Khối dữ liệu nén bằng Snappy khi tích hợp vào các định dạng như Parquet có khả năng chia tách (Splittable), giúp các công cụ tính toán phân tán (Spark/MapReduce) xử lý song song hiệu quả. Phù hợp lưu trữ dữ liệu nóng (Hot data).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong thiết kế cơ sở dữ liệu phân tích (OLAP), kỹ thuật thiết kế bảng "Partitioning" (Phân vùng) và "Clustering" (Gom cụm - như trong BigQuery) khác nhau như thế nào về cơ chế tổ chức dữ liệu vật lý và cách tối ưu câu lệnh truy vấn?
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế phân chia vật lý dựa trên giá trị cột của Partitioning
    keypoint_weight: 0.5
    description: Partitioning chia nhỏ một bảng dữ liệu lớn thành các phân vùng vật lý độc lập dựa trên giá trị cụ thể của một cột (thường là trường Date hoặc String danh mục). Khi truy vấn, hệ thống quét thẳng vào phân vùng tương ứng (Partition Pruning), bỏ qua các vùng khác để tăng tốc độ và giảm dung lượng I/O đĩa cứng.
  - id: KP5_2
    content: Cơ chế sắp xếp thứ tự dữ liệu cục bộ trong phân vùng của Clustering
    keypoint_weight: 0.5
    description: Clustering thực hiện sắp xếp thứ tự dữ liệu một cách tối ưu bên trong cấu trúc lưu trữ của bảng hoặc bên trong từng phân vùng dựa trên nội dung của một hoặc nhiều cột được chọn. Kỹ thuật này không chia nhỏ file vật lý cố định mà giúp tăng tốc các câu lệnh lọc điều kiện tinh chỉnh (Filter/Aggregate) trên các trường có độ đa dạng cao (High cardinality).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi thiết kế một pipeline thu thập dữ liệu tự động, cơ chế "Schema Validation" (Kiểm tra cấu trúc dữ liệu) đóng vai trò gì? Điều gì sẽ xảy ra với tính toàn vẹn dữ liệu nếu hệ thống nguồn bất ngờ thay đổi cấu trúc cột mà thiếu cơ chế này?
* **expected_key_points:**
  - id: KP6_1
    content: Bản chất rào chắn chất lượng của Schema Validation
    keypoint_weight: 0.5
    description: Schema Validation là bước kiểm tra tự động ở đầu vào của pipeline, đối chiếu dữ liệu thô nhận được với một khuôn mẫu cấu trúc định sẵn (Schema Registry/Blueprint) để đảm bảo dữ liệu đúng định dạng, đúng kiểu dữ liệu và đủ số lượng cột bắt buộc.
  - id: KP6_2
    content: Hậu quả lỗi phá vỡ dữ liệu ở đích (Schema Drift) và giải pháp
    keypoint_weight: 0.5
    description: Nếu thiếu bước này, khi hệ thống nguồn thay đổi (ví dụ: đổi kiểu dữ liệu từ Int sang String, xóa cột hoặc đổi tên cột), dữ liệu lỗi sẽ tràn vào làm hỏng các câu lệnh xử lý trung gian, gây lỗi crash hệ thống tính toán hoặc làm ghi nạp dữ liệu sai cấu trúc vào kho lưu trữ đích (Data Warehouse/Lake), phá vỡ tính toàn vẹn dữ liệu.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong việc lập lịch và quản lý luồng công việc dữ liệu (Data Orchestration), tại sao việc thiết kế cơ chế xử lý lỗi "Retry Policy" và thông báo "Alerting" lại đóng vai trò sinh tử để duy trì tính ổn định của hệ thống?
* **expected_key_points:**
  - id: KP7_1
    content: Vai trò xử lý lỗi tự động của Retry Policy giải quyết lỗi tạm thời (Transient faults)
    keypoint_weight: 0.5
    description: Các Data Pipelines thường bị lỗi do các tác nhân ngoại vi tạm thời (như đứt kết nối mạng API trong vài giây, Database nguồn bị quá tải phản hồi chậm). Cấu hình Retry Policy (số lần thử lại, khoảng thời gian chờ tăng dần - Exponential Backoff) giúp pipeline tự phục vụ vượt qua lỗi mà không cần con người can thiệp.
  - id: KP7_2
    content: Vai trò thông báo và giám sát của cơ chế Alerting khi lỗi nghiêm trọng
    keypoint_weight: 0.5
    description: Khi số lần Retry vượt ngưỡng cấu hình chứng tỏ hệ thống gặp lỗi nghiêm trọng (như sai thông tin tài khoản, sập server đích), cơ chế Alerting lập tức kích hoạt đẩy thông báo (qua Slack, Email, PagerDuty) kèm log chi tiết giúp đội ngũ kỹ sư phát hiện và ứng cứu kịp thời, đảm bảo SLA dữ liệu cho doanh nghiệp.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong thiết kế kiến trúc hệ thống lưu trữ phân tán lớn (Distributed Systems), hãy phân biệt sự khác biệt bản chất giữa mô hình "Strong Consistency" (Nhất quán mạnh) và "Eventual Consistency" (Nhất quán muộn). Mô hình Eventual Consistency giải quyết bài toán hiệu năng mở rộng hệ thống (Scalability) như thế nào?
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất khóa luồng đồng bộ của mô hình Strong Consistency
    keypoint_weight: 0.4
    description: Strong Consistency đảm bảo dữ liệu sau khi ghi/cập nhật thành công ở một Node sẽ lập tức hiển thị chính xác đồng bộ trên tất cả các Node còn lại của hệ thống phân tán. Mọi request đọc tại cùng một thời điểm ở bất kỳ Node nào đều ra kết quả giống nhau, đổi lại hệ thống phải khóa tài nguyên (Locking) làm chậm tốc độ ghi.
  - id: KP8_2
    content: Bản chất phi đồng bộ của mô hình Eventual Consistency
    keypoint_weight: 0.3
    description: Chấp nhận trạng thái tại một thời điểm, các Node khác nhau có thể trả về dữ liệu cũ/mới lệch nhau. Hệ thống cam kết nếu không có bản ghi mới nào nạp vào, qua một khoảng thời gian trễ nhất định, dữ liệu giữa các Node sẽ tự động đồng bộ nhất quán hoàn toàn với nhau.
  - id: KP8_3
    content: Tối ưu hóa khả năng chịu tải và tính sẵn sàng (Availability) nhờ Eventual Consistency
    keypoint_weight: 0.3
    description: Giải phóng hệ thống khỏi tiến trình khóa đồng bộ diện rộng, cho phép các Node nhận request đọc/ghi phi đồng bộ song song độc lập. Giúp tối ưu hóa tối đa thông lượng xử lý hệ thống (High Throughput), tăng tính sẵn sàng chịu lỗi (Availability) theo định lý CAP khi mở rộng quy mô cụm cluster.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong xử lý dữ liệu lớn bằng Apache Spark, hãy giải thích hiện tượng "OOM (Out Of Memory) Exception" ở tầng Executor Node. Hãy phân tích hai nguyên nhân bản chất về mặt quản lý bộ nhớ dữ liệu gây ra lỗi này và cách cấu hình/lập trình để khắc phục.
* **expected_key_points:**
  - id: KP9_1
    content: Nguyên nhân do mất cân bằng phân bổ dữ liệu vật lý (Data Skew / Straggler Task)
    keypoint_weight: 0.4
    description: Xảy ra khi một Partition chứa dung lượng dữ liệu quá lớn vượt trội so với các partition khác do chọn khóa băm (Join/Group key) sai. Khi thực thi phép toán (như Shuffle), Executor nhận partition lệch này phải nạp khối lượng lớn dữ liệu vượt quá giới hạn RAM được cấp phát cho một Task, gây sập nguồn Executor. Khắc phục bằng kỹ thuật Salting khóa hoặc tăng số lượng phân vùng `spark.sql.shuffle.partitions`.
  - id: KP9_2
    content: Nguyên nhân do cấu hình sai tỷ lệ phân chia bộ nhớ hoặc lạm dụng phép toán gộp (Collect Operation)
    keypoint_weight: 0.4
    description: Xảy ra khi lập trình viên sử dụng lệnh `.collect()` trên một tập dữ liệu lớn, ép buộc nạp toàn bộ dữ liệu phân tán dưới các Worker về RAM của duy nhất một Node; hoặc cấu hình phân chia tỷ lệ bộ nhớ RAM giữa vùng tính toán (Execution Memory) và vùng lưu trữ (Storage Memory) không phù hợp với bản chất tác vụ I/O nặng. Khắc phục bằng cách ghi trực tiếp dữ liệu xuống đĩa cứng (`.write`) và tối ưu tham số `spark.executor.memory`.
  - id: KP9_3
    content: Hiện tượng rò rỉ bộ nhớ ở tầng JVM chạy ngầm (Garbage Collection Overhead)
    keypoint_weight: 0.2
    description: Do Spark sinh ra quá nhiều đối tượng Java ngắn hạn trong vòng lặp tính toán liên tục khiến bộ dọn dẹp Garbage Collection của JVM bị quá tải, không giải phóng RAM kịp thời. Khắc phục bằng cách chuyển đổi sang cấu trúc dữ liệu tối ưu bộ nhớ của Spark SQL/Dataset.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Khi xây dựng kiến trúc Lambda Architecture để xử lý dữ liệu quy mô lớn, hãy giải thích nguyên lý hoạt động phối hợp giữa hai phân lớp: "Batch Layer" và "Speed Layer". Kiến trúc này giải quyết bài toán gì và điểm yếu lớn nhất của nó trong việc bảo trì hệ thống là gì?
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế hoạt động song song của Batch Layer và Speed Layer
    keypoint_weight: 0.4
    description: Dữ liệu thô đầu vào được đẩy đồng thời vào hai luồng. **Batch Layer** lưu trữ toàn bộ dữ liệu gốc và định kỳ tính toán (ví dụ mỗi ngày một lần) để cho ra kết quả chính xác tuyệt đối nhưng có độ trễ cao. **Speed Layer** xử lý luồng dữ liệu thời gian thực (Streaming) liên tục để tính toán ra kết quả nhanh nhất (Near real-time) nhằm bù đắp khoảng trống độ trễ của Batch Layer, chấp nhận xác suất sai lệch nhỏ.
  - id: KP10_2
    content: Giải quyết bài toán cân bằng giữa tính chính xác toàn cục và tốc độ thời gian thực
    keypoint_weight: 0.3
    description: Giải quyết bài toán tối ưu hóa hệ thống giúp tầng hiển thị (Serving Layer) có thể trả về kết quả phân tích tổng hợp ngay lập tức bằng cách cộng gộp kết quả chính xác trong quá khứ của Batch với kết quả tức thời hiện tại của Speed Layer.
  - id: KP10_3
    content: Khuyết điểm chí tử về chi phí bảo trì mã nguồn trùng lặp (Dual-codebase maintenance)
    keypoint_weight: 0.3
    description: Điểm yếu lớn nhất của Lambda là lập trình viên phải viết, duy trì và đồng bộ logic nghiệp vụ (Business logic) trên hai nền tảng công nghệ mã nguồn hoàn toàn khác nhau cùng lúc (ví dụ: code MapReduce/Spark SQL cho Batch và code Storm/Flink cho Speed), cực kỳ phức tạp khi cần chỉnh sửa hay debug lỗi hệ thống.