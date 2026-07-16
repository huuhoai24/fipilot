# Bộ Câu Hỏi Phỏng Vấn Data Engineer (Level 1)

* **Role:** Data Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong các pipeline tích hợp dữ liệu, kỹ thuật CDC (Change Data Capture) giúp theo dõi sự thay đổi dữ liệu. Hãy phân biệt điểm khác biệt cơ bản về cơ chế hoạt động, ưu và nhược điểm giữa Query-based CDC và Log-based CDC.
* **expected_key_points:**
  - id: KP1_1
    content: Cơ chế hoạt động và đánh giá của Query-based CDC
    keypoint_weight: 0.5
    description: Sử dụng các câu lệnh SQL truy vấn định kỳ vào bảng nguồn dựa trên một cột mốc thời gian (như updated_at) hoặc số tăng dần (sequence ID). Cơ chế này dễ triển khai nhưng làm tăng tải CPU/IO cho database nguồn và không ghi nhận được các bản ghi đã bị xóa vật lý (DELETE).
  - id: KP1_2
    content: Cơ chế hoạt động và đánh giá của Log-based CDC
    keypoint_weight: 0.5
    description: Đọc trực tiếp các tệp nhật ký giao dịch chạy ngầm của hệ quản trị cơ sở dữ liệu (như Binlog trong MySQL, WAL trong PostgreSQL). Cơ chế này không gây tải lên bảng chính, ghi nhận được mọi sự thay đổi kể cả lệnh DELETE, đạt hiệu năng gần như thời gian thực nhưng yêu cầu cấu hình phức tạp và quyền truy cập sâu vào hệ thống.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong hệ quản trị cơ sở dữ liệu quan hệ (RDBMS) tuân thủ tính chất ACID, hãy giải thích ý nghĩa và sự khác biệt về mức độ bảo vệ dữ liệu giữa hai mức cô lập giao dịch (Transaction Isolation Levels): Read Committed và Serializable.
* **expected_key_points:**
  - id: KP2_1
    content: Cơ chế hoạt động của mức cô lập Read Committed
    keypoint_weight: 0.5
    description: Đảm bảo một giao dịch chỉ có thể đọc được các dữ liệu đã được commit bởi các giao dịch khác trước đó, giúp tránh được lỗi đọc dữ liệu rác (Dirty Read). Tuy nhiên, mức này vẫn có thể gặp phải hiện tượng đọc không lặp lại (Non-repeatable Read) hoặc đọc bóng ma (Phantom Read) nếu dữ liệu bị thay đổi giữa các bước đọc trong cùng một giao dịch.
  - id: KP2_2
    content: Cơ chế hoạt động của mức cô lập Serializable
    keypoint_weight: 0.5
    description: Là mức cô lập cao nhất, ép buộc các giao dịch chạy song song phải được thực thi tuần tự như thể chỉ có duy nhất một giao dịch được chạy tại một thời điểm. Mức này triệt tiêu hoàn toàn mọi lỗi đồng thời dữ liệu (Dirty Read, Non-repeatable Read, Phantom Read) bằng cách khóa tài nguyên chặt chẽ, đổi lại làm giảm mạnh hiệu năng xử lý song song.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế của các hệ thống lưu trữ dữ liệu và công cụ ghi log (như Apache Kafka, PostgreSQL), cơ chế WAL (Write-Ahead Logging) là gì và tại sao nó lại giúp đảm bảo an toàn dữ liệu trước khi hệ thống thực hiện cập nhật vật lý xuống đĩa cứng?
* **expected_key_points:**
  - id: KP3_1
    content: Nguyên lý ghi nhật ký trước khi ghi dữ liệu của WAL
    keypoint_weight: 0.5
    description: WAL quy định rằng mọi thay đổi về trạng thái dữ liệu bắt buộc phải được ghi và lưu trữ an toàn vào một tệp nhật ký tuần tự (Append-only log file) trên đĩa cứng trước khi các thay đổi vật lý đó thực sự được áp dụng và ghi vào các bảng dữ liệu chính (Data files).
  - id: KP3_2
    content: Khả năng khôi phục dữ liệu khi xảy ra sự cố đột ngột (Crash Recovery)
    keypoint_weight: 0.5
    description: Khi hệ thống bị mất điện hoặc sập nguồn đột ngột, RAM bị xóa sạch. Khi khởi động lại, hệ thống sẽ đọc tệp nhật ký WAL để thực hiện chạy lại (Redo) các giao dịch đã thành công nhưng chưa kịp ghi xuống đĩa, hoặc hoàn tác (Undo) các giao dịch dở dang, đảm bảo dữ liệu không bị hỏng hoặc mất mát.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi truyền tải dữ liệu dung lượng lớn qua mạng hoặc lưu trữ phân tán, kỹ thuật nén dữ liệu nạp theo khối (Block Compression) của định dạng Parquet giúp tối ưu hóa hiệu năng như thế nào? Phân biệt sự khác biệt về vai trò giữa nén metadata và nén dữ liệu cột.
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế nén dữ liệu theo từng khối cột (Column Chunk)
    keypoint_weight: 0.4
    description: Parquet chia nhỏ bảng thành các nhóm hàng (Row Groups), và trong mỗi nhóm hàng, dữ liệu của từng cột được lưu trữ liên tục thành các khối (Column Chunks). Do dữ liệu cùng một cột có kiểu dữ liệu tương đồng, thuật toán nén (như Snappy, Gzip) đạt được tỷ lệ nén cực kỳ cao.
  - id: KP4_2
    content: Tách biệt nén và tối ưu hóa ở mức Page Metadata
    keypoint_weight: 0.3
    description: Mỗi khối cột lại được chia nhỏ thành các Trang dữ liệu (Pages). Các trang này chứa vùng Metadata riêng (lưu Min/Max giá trị, số lượng phần tử). Việc nén Metadata giúp các công cụ đọc bỏ qua các trang không thỏa mãn điều kiện lọc mà không cần giải nén dữ liệu cột (Page skipping).
  - id: KP4_3
    content: Tối ưu băng thông I/O và RAM khi thực thi câu lệnh đọc
    keypoint_weight: 0.3
    description: Nhờ cơ chế lưu trữ và nén theo cột, hệ thống chỉ cần tải từ đĩa cứng và giải nén đúng các cột dữ liệu cần thiết lên RAM, giúp tiết kiệm tối đa tài nguyên I/O đĩa cứng và giảm thiểu băng thông truyền tải mạng.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong các hệ thống cơ sở dữ liệu phân tán quy mô lớn (như Cassandra, DynamoDB), hãy phân biệt sự khác biệt về mặt kiến trúc và cách thức hoạt động giữa Global Index (Chỉ mục toàn cục) và Local Index (Chỉ mục cục bộ).
* **expected_key_points:**
  - id: KP5_1
    content: Bản chất và cơ chế hoạt động của Local Index
    keypoint_weight: 0.5
    description: Chỉ mục cục bộ được xây dựng và lưu trữ độc lập trên từng Node vật lý, chỉ lập chỉ mục cho phần dữ liệu phân vùng (Partition) nằm trên chính Node đó. Khi truy vấn không kèm theo khóa phân vùng (Partition Key), hệ thống buộc phải quét chỉ mục trên tất cả các Node trong cụm, gây tốn tài nguyên mạng (Scatter-gather query).
  - id: KP5_2
    content: Bản chất và cơ chế hoạt động của Global Index
    keypoint_weight: 0.5
    description: Chỉ mục toàn cục lập chỉ mục cho toàn bộ dữ liệu trên tất cả các phân vùng và có thể được lưu trữ trên một hoặc nhiều Node chuyên biệt khác với Node chứa dữ liệu gốc. Giúp định tuyến câu lệnh đọc trực tiếp đến Node đích chứa dữ liệu mà không cần quét diện rộng, nhưng chi phí cập nhật chỉ mục khi ghi dữ liệu (Write Overhead) rất cao vì cần đồng bộ qua mạng.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong xử lý luồng dữ liệu thời gian thực (Stream Processing), hiện tượng sập nguồn hoặc mất mát dữ liệu do chênh lệch tốc độ xử lý được giải quyết bằng cơ chế "Backpressure". Hãy giải thích nguyên lý hoạt động của cơ chế này.
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên lý truyền tín hiệu ngược dòng để điều chỉnh tốc độ
    keypoint_weight: 0.5
    description: Khi hệ thống đích (Consumer) bị quá tải bộ nhớ đệm do tốc độ xử lý chậm hơn tốc độ đẩy dữ liệu từ nguồn, nó sẽ chủ động gửi tín hiệu cảnh báo ngược dòng (Upstream) yêu cầu hệ thống trung gian hoặc hệ thống nguồn (Producer) giảm tốc độ gửi dữ liệu lại.
  - id: KP6_2
    content: Bảo vệ tài nguyên bộ nhớ đệm chống lỗi Out-Of-Memory (OOM)
    keypoint_weight: 0.5
    description: Giúp ngăn chặn việc phình to vô hạn của bộ nhớ đệm (In-memory buffers) trên các máy chủ xử lý trung gian, loại bỏ rủi ro crash hệ thống do tràn bộ nhớ và đảm bảo không bị thất thoát dữ liệu trong quá trình truyền tải.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi thiết kế một hệ thống Data Lake trên Cloud, tại sao việc xây dựng một "Metadata Store" (như AWS Glue Data Catalog, Hive Metastore) lại mang ý nghĩa sống còn để quản lý tài nguyên dữ liệu?
* **expected_key_points:**
  - id: KP7_1
    content: Quản lý và lưu trữ thông tin cấu trúc dữ liệu tĩnh (Schema Registry)
    keypoint_weight: 0.5
    description: Metadata Store lưu trữ thông tin về Schema (tên cột, kiểu dữ liệu), vị trí vật lý của các file dữ liệu trên Cloud Object Storage, và các thông tin phân vùng (Partition metadata), giúp phân tách lớp lưu trữ vật lý và lớp tính toán logic.
  - id: KP7_2
    content: Điểm kết nối trung gian duy nhất cho các công cụ truy vấn phân tích (Unified Catalog)
    keypoint_weight: 0.5
    description: Cung cấp một thư mục định danh duy nhất để các công cụ tính toán khác nhau (như Spark, Athena, Presto) có thể tìm kiếm, đọc hiểu cấu trúc file thô tĩnh và thực thi các câu lệnh SQL trực tiếp trên Data Lake mà không cần phải tự quét và phân tích định dạng file từ đầu.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong các hệ thống lưu trữ phân tán không sử dụng cơ chế Master-Slave (như Cassandra), hiện tượng xung đột dữ liệu khi có nhiều Node cùng ghi đồng thời được giải quyết thế nào? Phân biệt cơ chế Last-Write-Wins (LWW) và Vector Clocks.
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất và rủi ro mất dữ liệu của cơ chế Last-Write-Wins (LWW)
    keypoint_weight: 0.4
    description: LWW giải quyết xung đột dựa vào mốc thời gian vật lý (Timestamp) của hệ thống. Bản ghi nào có mốc thời gian mới nhất sẽ ghi đè lên bản ghi cũ. Cơ chế này đơn giản nhưng có rủi ro mất mát dữ liệu hợp lệ của người dùng nếu đồng hồ vật lý giữa các máy chủ bị lệch nhau (Clock skew).
  - id: KP8_2
    content: Cơ chế theo dõi mối quan hệ nhân quả của Vector Clocks
    keypoint_weight: 0.4
    description: Vector Clocks sử dụng một mảng các bộ đếm số phiên bản logic của từng Node để theo dõi lịch sử và mối quan hệ nhân quả (Causality) giữa các lần ghi dữ liệu. Nó giúp phát hiện chính xác khi nào hai lần ghi xảy ra đồng thời và độc lập với nhau mà không phụ thuộc vào đồng hồ vật lý.
  - id: KP8_3
    content: Khả năng giữ lại dữ liệu xung đột để ứng dụng tự giải quyết (Conflict resolution)
    keypoint_weight: 0.2
    description: Khi phát hiện xung đột đồng thời thông qua Vector Clocks, hệ thống phân tán sẽ không tự ý xóa dữ liệu mà lưu trữ cả hai phiên bản và đẩy trách nhiệm quyết định lựa chọn/gộp dữ liệu về cho tầng ứng dụng (Application level) xử lý lúc đọc.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong các định dạng bảng hiện đại (như Delta Lake, Apache Iceberg), kỹ thuật sắp xếp dữ liệu đa chiều "Z-Ordering" (Z-Address) hoạt động dựa trên nguyên lý toán học nào và tại sao nó lại vượt trội hơn kỹ thuật phân vùng Partitioning thông thường khi truy vấn trên nhiều cột lọc?
* **expected_key_points:**
  - id: KP9_1
    content: Nguyên lý toán học bản đồ không gian đa chiều về một chiều (Space-filling curve)
    keypoint_weight: 0.4
    description: Z-Ordering sử dụng thuật toán ánh xạ tọa độ của nhiều cột dữ liệu khác nhau thành một chuỗi giá trị một chiều duy nhất (Z-value) bằng cách xen kẽ các bit nhị phân của các giá trị cột đó, giúp bảo toàn tính chất gần nhau của dữ liệu trong không gian đa chiều khi lưu xuống đĩa.
  - id: KP9_2
    content: Tối ưu hóa hiệu năng lọc đồng thời trên nhiều cột độc lập
    keypoint_weight: 0.4
    description: Khác với phân vùng phân cấp thông thường (chỉ tối ưu khi lọc theo đúng thứ tự cột phân vùng), Z-Ordering phân bổ đều độ chọn lọc trên tất cả các cột được chọn. Giúp các câu lệnh truy vấn lọc theo bất kỳ tổ hợp cột nào cũng có hiệu năng quét cực nhanh nhờ cơ chế lọc bỏ file hiệu quả (Data skipping).
  - id: KP9_3
    content: Giải quyết bài toán giới hạn số lượng phân vùng (Over-partitioning problem)
    keypoint_weight: 0.2
    description: Ngăn chặn hiện tượng tạo ra quá nhiều thư mục nhỏ làm quá tải metadata của Data Lake khi phân vùng theo các cột có độ đa dạng giá trị cao (High-cardinality), duy trì kích thước file vật lý ở mức tối ưu.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong Apache Spark 3.x, tính năng tối ưu hóa truy vấn động AQE (Adaptive Query Execution) giải quyết bài toán hiệu năng Shuffle bằng cách tự động tinh chỉnh kế hoạch thực thi vật lý (Physical Plan) ở runtime dựa trên nguyên lý nào?
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế tự động gộp các phân vùng nhỏ sau khi Shuffle (Coalescing post-shuffle partitions)
    keypoint_weight: 0.4
    description: AQE rà soát kích thước dữ liệu thực tế tại các phân vùng trung gian sau giai đoạn Map. Nếu phát sinh quá nhiều phân vùng nhỏ, Spark sẽ tự động gộp chúng lại thành các phân vùng có kích thước lớn hơn để tránh lãng phí tài