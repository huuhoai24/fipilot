# Bộ Câu Hỏi Phỏng Vấn Data Engineer (Level 1)

* **Role:** Data Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế cơ sở dữ liệu, hãy phân biệt sự khác biệt cốt lõi về mặt mục đích sử dụng, cấu trúc lưu trữ và cách tối ưu hóa giữa hai hệ thống: OLTP (Online Transaction Processing) và OLAP (Online Analytical Processing).
* **expected_key_points:**
  - id: KP1_1
    content: Phân biệt về mục đích sử dụng và cơ chế xử lý giao dịch
    keypoint_weight: 0.5
    description: OLTP tối ưu cho các tác vụ ghi/đọc nhanh, xử lý các giao dịch hằng ngày (INSERT, UPDATE, DELETE) với lượng dữ liệu nhỏ trên mỗi transaction (như hệ thống ngân hàng, bán hàng). OLAP tối ưu cho việc phân tích dữ liệu lịch sử khổng lồ, thực hiện các truy vấn đọc phức tạp (SELECT, Aggregations) để hỗ trợ ra quyết định (BI/Reporting).
  - id: KP1_2
    content: Phân biệt về cấu trúc dữ liệu và tối ưu hóa thiết kế
    keypoint_weight: 0.5
    description: OLTP sử dụng mô hình cơ sở dữ liệu quan hệ chuẩn hóa cao (Normalized - 3NF) để tránh dư thừa dữ liệu và đảm bảo tính nhất quán. OLAP thường sử dụng mô hình phi chuẩn hóa (Denormalized) như Star Schema, Snowflake Schema hoặc định dạng lưu trữ theo cột (Columnar Storage) để tối ưu hóa tốc độ truy vấn.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong quy trình xây dựng Data Pipeline, ba bước E-T-L (Extract, Transform, Load) đại diện cho những hoạt động kỹ thuật cụ thể nào?
* **expected_key_points:**
  - id: KP2_1
    content: Ý nghĩa và hoạt động của giai đoạn Extract và Load
    keypoint_weight: 0.5
    description: Extract là quá trình thu thập và trích xuất dữ liệu thô từ nhiều nguồn khác nhau (APIs, Databases, Logs, Files). Load là quá trình nạp dữ liệu sau khi đã xử lý xong vào hệ thống lưu trữ đích (như Data Warehouse hoặc Data Lake).
  - id: KP2_2
    content: Ý nghĩa và hoạt động của giai đoạn Transform
    keypoint_weight: 0.5
    description: Transform là quá trình làm sạch, biến đổi cấu trúc, lọc dữ liệu rác, chuẩn hóa định dạng, gộp nhóm hoặc thực hiện các phép toán logic nghiệp vụ để dữ liệu sẵn sàng cho việc phân tích.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt điểm khác nhau về mặt cơ chế lưu trữ và hiệu năng truy vấn giữa cấu trúc lưu trữ dạng dòng (Row-oriented) và lưu trữ dạng cột (Columnar) trong các hệ thống dữ liệu.
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế lưu trữ và thế mạnh của Row-oriented Storage
    keypoint_weight: 0.5
    description: Dữ liệu của một hàng được xếp liên tục cạnh nhau trên ổ đĩa. Phù hợp cho việc đọc/ghi trọn vẹn thông tin của một bản ghi cụ thể (như OLTP Databases), nhưng rất chậm khi cần tính toán gộp (Aggregation) trên một cột vì đĩa cứng phải đọc toàn bộ bảng dữ liệu.
  - id: KP3_2
    content: Cơ chế lưu trữ và thế mạnh của Columnar Storage
    keypoint_weight: 0.5
    description: Dữ liệu của cùng một cột được xếp liên tục cạnh nhau trên ổ đĩa (như Parquet, ORC). Phù hợp cho các truy vấn phân tích (OLAP) chỉ cần đọc một vài cột cụ thể, giúp giảm thiểu tối đa dung lượng I/O phải đọc và hỗ trợ nén dữ liệu cực tốt.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong thiết kế Data Warehouse theo mô hình Dimensional Modeling (như Star Schema), hãy phân biệt sự khác biệt về vai trò logic giữa Fact Table (Bảng sự kiện) và Dimension Table (Bảng chiều thông tin).
* **expected_key_points:**
  - id: KP4_1
    content: Vai trò và nội dung của Fact Table
    keypoint_weight: 0.5
    description: Fact Table lưu trữ các phép đo định lượng, số liệu thực tế (Metrics/Measures) phát sinh từ các sự kiện nghiệp vụ (ví dụ: số tiền giao dịch, số lượng hàng bán), kết hợp với các trường khóa ngoại (Foreign Keys) trỏ tới các bảng chiều liên quan. Bảng này thường có số lượng hàng cực kỳ lớn và phình to rất nhanh.
  - id: KP4_2
    content: Vai trò và nội dung của Dimension Table
    keypoint_weight: 0.5
    description: Dimension Table chứa các thông tin mô tả ngữ cảnh xung quanh sự kiện (như ai, cái gì, ở đâu, khi nào). Bảng này lưu thông tin chi tiết (ví dụ: tên khách hàng, địa chỉ, danh mục sản phẩm) dùng để lọc (Filter) hoặc nhóm (Group by) dữ liệu khi phân tích.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi thiết kế một hệ thống xử lý dữ liệu lớn bằng Apache Spark, hãy giải thích sự khác biệt giữa hai loại biến đổi dữ liệu: Narrow Transformation và Wide Transformation. Loại nào tốn chi phí tài nguyên mạng hơn và tại sao?
* **expected_key_points:**
  - id: KP5_1
    content: Khái niệm và cơ chế hoạt động của Narrow Transformation
    keypoint_weight: 0.4
    description: Là các phép biến đổi mà dữ liệu đầu vào của một phân vùng (Partition) chỉ cần thiết để tính toán ra một phân vùng đầu ra tương ứng trên cùng một Node (ví dụ: `map`, `filter`). Không yêu cầu di chuyển dữ liệu qua mạng giữa các Executor.
  - id: KP5_2
    content: Khái niệm và cơ chế hoạt động của Wide Transformation
    keypoint_weight: 0.4
    description: Là các phép biến đổi yêu cầu dữ liệu từ nhiều phân vùng khác nhau phải được gom nhóm và phân phối lại trên toàn bộ cụm cluster (ví dụ: `groupByKey`, `join`, `reduceByKey`). Phép toán này kích hoạt tiến trình Shuffle dữ liệu.
  - id: KP5_3
    content: Xác định loại tiêu tốn tài nguyên mạng và lý do
    keypoint_weight: 0.2
    description: Wide Transformation tiêu tốn tài nguyên mạng và đĩa cứng lớn nhất vì nó bắt buộc phải thực hiện phân vùng lại dữ liệu và truyền tải một lượng lớn dữ liệu qua lại giữa các Node trong cụm (Shuffle operation).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi xây dựng các pipeline tích hợp dữ liệu tự động, cơ chế CDC (Change Data Capture) giải quyết bài toán gì tốt hơn so với phương pháp truy vấn quét bảng định kỳ (Batch Query)?
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế bắt sự kiện thay đổi thời gian thực của CDC
    keypoint_weight: 0.5
    description: CDC theo dõi và ghi nhận trực tiếp các sự kiện thay đổi dữ liệu (INSERT, UPDATE, DELETE) ngay khi chúng xảy ra ở tầng Database log (như Transaction Log/Binlog) mà không cần can thiệp trực tiếp vào dữ liệu bảng chính.
  - id: KP6_2
    content: Giải quyết bài toán tải hệ thống và độ trễ dữ liệu
    keypoint_weight: 0.5
    description: CDC loại bỏ việc phải chạy các câu lệnh SELECT quét toàn bộ bảng (Full Table Scan) định kỳ, giúp giảm thiểu tối đa tải của cơ sở dữ liệu nguồn (Source DB), đồng thời giảm độ trễ dữ liệu truyền về đích (đạt mức Near Real-Time).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi lưu trữ dữ liệu lớn (Big Data) trên các hệ thống Cloud Object Storage (như AWS S3, Google Cloud Storage), kỹ thuật Phân vùng dữ liệu (Data Partitioning) bằng cách thiết kế thư mục (Prefix) đóng vai trò gì trong việc tối ưu hóa chi phí và tốc độ truy vấn?
* **expected_key_points:**
  - id: KP7_1
    content: Tối ưu hóa hiệu năng đọc dữ liệu nhờ cơ chế bỏ qua (Partition Pruning)
    keypoint_weight: 0.5
    description: Việc chia nhỏ dữ liệu thành cấu trúc thư mục dạng khóa-giá trị (như `year=2026/month=07/`) giúp các công cụ truy vấn (như Athena, Presto, Spark) nhận diện và chỉ đọc đúng các thư mục chứa dữ liệu cần thiết, bỏ qua hoàn toàn phần dữ liệu không liên quan.
  - id: KP7_2
    content: Tối ưu hóa chi phí tài nguyên và chi phí quét dữ liệu
    keypoint_weight: 0.5
    description: Hạn chế quét dư thừa giúp giảm lượng dữ liệu phải đọc (Data Scanned), từ đó tiết kiệm tối đa chi phí tính toán, chi phí I/O mạng của Cloud Storage và tăng tốc độ trả về kết quả cho phân tích.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Khi thực hiện phép toán liên kết hai bảng dữ liệu cực lớn trong Apache Spark, hãy giải thích nguyên lý hoạt động của cơ chế "Broadcast Hash Join" (Map-side Join) và điều kiện kỹ thuật để áp dụng cơ chế này hiệu quả.
* **expected_key_points:**
  - id: KP8_1
    content: Cơ chế phân phối bảng nhỏ đến toàn bộ các Executor
    keypoint_weight: 0.4
    description: Thay vì thực hiện Shuffle dữ liệu của cả hai bảng lớn (tốn tài nguyên), Spark sẽ sao chép (Broadcast) toàn bộ dữ liệu của bảng nhỏ hơn đến bộ nhớ RAM của tất cả các Executor chạy ngầm trên các Worker Nodes.
  - id: KP8_2
    content: Thực hiện liên kết cục bộ triệt tiêu tiến trình Shuffle (Map-side Join)
    keypoint_weight: 0.3
    description: Mỗi Executor tiến hành phép toán Join trực tiếp giữa phân vùng của bảng lớn sẵn có trên Node đó với bản sao bảng nhỏ nằm trong bộ nhớ cục bộ, giúp triệt tiêu hoàn toàn bước xáo trộn dữ liệu qua mạng (No network Shuffle).
  - id: KP8_3
    content: Điều kiện kích thước bộ nhớ vật lý để áp dụng thành công
    keypoint_weight: 0.3
    description: Áp dụng khi một trong hai bảng có kích thước đủ nhỏ (thông thường dưới ngưỡng cấu hình `spark.sql.autoBroadcastJoinThreshold`, mặc định là 10MB) để có thể nằm vừa vặn hoàn toàn trong bộ nhớ RAM của các Executor mà không gây ra lỗi tràn bộ nhớ (Out Of Memory - OOM).

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong thiết kế kiến trúc hồ dữ liệu hiện đại, định dạng lưu trữ "Lakehouse" (như Delta Lake, Apache Iceberg) giải quyết các khuyết điểm chí tử nào của Data Lake truyền thống (như HDFS hoặc Object Storage thuần túy)?
* **expected_key_points:**
  - id: KP9_1
    content: Hỗ trợ các thuộc tính giao dịch ACID (ACID Transactions) trên Data Lake
    keypoint_weight: 0.4
    description: Lakehouse ghi nhận một bảng kê chi tiết các thay đổi (Metadata Transaction Log) chạy ngầm, đảm bảo các tác vụ ghi/đọc chạy song song không làm hỏng dữ liệu, hỗ trợ hoàn tác giao dịch (Rollback) và ngăn chặn tình trạng dữ liệu rác/đọc dở dang (Dirty reads).
  - id: KP9_2
    content: Cơ chế quản lý cấu trúc dữ liệu và tiến hóa Schema (Schema Enforcement & Evolution)
    keypoint_weight: 0.3
    description: Ngăn chặn việc ghi nạp dữ liệu sai cấu trúc (Schema Enforcement) làm hỏng bảng, đồng thời cho phép tự động cập nhật, biến đổi cấu trúc cột dữ liệu theo thời gian (Schema Evolution) mà không cần phải ghi đè lại toàn bộ dữ liệu lịch sử.
  - id: KP9_3
    content: Hỗ trợ cơ chế truy vấn lịch sử dữ liệu (Time Travel) và tối ưu hóa file
    keypoint_weight: 0.3
    description: Cho phép người dùng truy vấn trực tiếp dữ liệu tại một thời điểm chính xác trong quá khứ thông qua Transaction Log, đồng thời tự động gộp các file nhỏ chạy ngầm (Compaction) để tối ưu hóa hiệu năng đọc đĩa.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong kiến trúc xử lý dữ liệu thời gian thực (Stream Processing), hãy giải thích sự khác biệt logic giữa ba cơ chế đảm bảo truyền tải thông điệp (Delivery Semantics): At-most-once, At-least-once, và Exactly-once. Cơ chế Exactly-once thường đòi hỏi giải pháp kỹ thuật đồng bộ nào để đạt được hiệu quả?
* **expected_key_points:**
  - id: KP10_1
    content: Phân biệt cơ chế At-most-once và At-least-once
    keypoint_weight: 0.4
    description: At-most-once đảm bảo thông điệp được gửi đi tối đa 1 lần, chấp nhận rủi ro mất mát dữ liệu nếu gặp sự cố nhưng không bị trùng lặp. At-least-once đảm bảo thông điệp đến đích ít nhất 1 lần bằng cách gửi lại nếu chưa nhận được xác nhận (Ack), đảm bảo không mất dữ liệu nhưng có thể gây trùng lặp.
  - id: KP10_2
    content: Định nghĩa cơ chế lý tưởng Exactly-once
    keypoint_weight: 0.3
    description: Đảm bảo dữ liệu được xử lý chính xác đúng 1 lần duy nhất trên hệ thống đích, không bị mất mát và hoàn toàn không bị lặp lại dù có lỗi hay tiến trình gửi lại xảy ra ở tầng vật lý.
  - id: KP10_3
    content: Các giải pháp kỹ thuật đồng bộ để đạt được Exactly-once
    keypoint_weight: 0.3
    description: Đòi hỏi sự kết hợp đồng bộ chặt chẽ giữa: Nguồn phát hỗ trợ replay dữ liệu (như Apache Kafka offsets), công cụ xử lý hỗ trợ cơ chế checkpoint trạng thái (như Spark/Flink State checkpointing), và hệ thống đích có tính chất Idempotent (ghi đè trùng lặp không đổi dữ liệu) hoặc hỗ trợ giao dịch hai pha (Two-Phase Commit - 2PC).