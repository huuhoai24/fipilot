# Bộ Câu Hỏi Phỏng Vấn Data Engineer (Level 1)

* **Role:** Data Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế cơ sở dữ liệu và hệ thống lưu trữ, hãy phân biệt điểm khác biệt cốt lõi về mục đích xử lý và cấu trúc mô hình giữa Normalization (Chuẩn hóa dữ liệu) và Denormalization (Phi chuẩn hóa dữ liệu).
* **expected_key_points:**
  - id: KP1_1
    content: Bản chất và ngữ cảnh áp dụng của Normalization
    keypoint_weight: 0.5
    description: Chuẩn hóa dữ liệu (thường đến mức 3NF) nhằm mục đích triệt tiêu sự dư thừa dữ liệu và lỗi bất thường khi cập nhật. Mô hình này chia nhỏ dữ liệu thành nhiều bảng có mối quan hệ chặt chẽ, tối ưu hóa cho các tác vụ ghi (Write-heavy) của hệ thống nghiệp vụ OLTP.
  - id: KP1_2
    content: Bản chất và ngữ cảnh áp dụng của Denormalization
    keypoint_weight: 0.5
    description: Phi chuẩn hóa chủ động gom cụm dữ liệu dư thừa lại vào ít bảng hơn (như mô hình Star Schema) để giảm thiểu các phép toán JOIN phức tạp. Mô hình này tối ưu hóa tối đa cho tốc độ truy vấn đọc dữ liệu (Read-heavy) của các hệ thống phân tích OLAP/Data Warehouse.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Khi xây dựng Data Lake, hãy phân biệt điểm khác nhau cơ bản về cơ chế lưu trữ cấu trúc dữ liệu và trường hợp áp dụng hiệu quả giữa hai định dạng tệp tin: Apache Avro và Apache Parquet.
* **expected_key_points:**
  - id: KP2_1
    content: Cấu trúc lưu trữ dạng dòng và ứng dụng của Apache Avro
    keypoint_weight: 0.5
    description: Avro là định dạng lưu trữ hướng dòng (Row-oriented), lưu dữ liệu dưới dạng nhị phân kèm schema dạng JSON. Nó tối ưu cho các tác vụ ghi dữ liệu liên tục, nạp dữ liệu nhanh (Write-heavy) và rất phù hợp cho truyền tải thông điệp (Message streaming như Kafka payload).
  - id: KP2_2
    content: Cấu trúc lưu trữ dạng cột và ứng dụng của Apache Parquet
    keypoint_weight: 0.5
    description: Parquet là định dạng lưu trữ hướng cột (Columnar-oriented), nén dữ liệu cực tốt theo từng khối cột. Nó tối ưu cho các câu lệnh truy vấn phân tích đọc dữ liệu lớn (Read-heavy/Analytical queries) nhờ cơ chế chỉ nạp đúng các cột cần tính toán.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong quy trình vận hành hệ thống dữ liệu, công cụ lập lịch và điều phối luồng việc (Data Orchestration Tool - như Apache Airflow) đóng vai trò gì? Khái niệm DAG (Directed Acyclic Graph) trong Airflow nghĩa là gì?
* **expected_key_points:**
  - id: KP3_1
    content: Vai trò tự động hóa, quản lý chuỗi tác vụ của Data Orchestration
    keypoint_weight: 0.5
    description: Công cụ điều phối giúp tự động hóa việc lập lịch chạy, quản lý sự phụ thuộc (Dependencies), giám sát trạng thái và xử lý lỗi/retry cho chuỗi các tác vụ ETL/ELT phức tạp di chuyển giữa nhiều hệ thống khác nhau.
  - id: KP3_2
    content: Logic luồng việc không chu trình của khái niệm DAG
    keypoint_weight: 0.5
    description: DAG (Đồ thị có hướng không chu trình) là một tập hợp các tác vụ (Tasks) được liên kết với nhau theo các mối quan hệ có hướng rõ ràng, quy định thứ tự thực hiện từ trước ra sau, và cam kết cấu trúc luồng chạy không bao giờ bị lặp vòng lặp vô hạn (No loops).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy giải thích hiện tượng "Small Files Problem" (Vấn đề tệp tin nhỏ) trong kiến trúc lưu trữ dữ liệu lớn (như HDFS hoặc Cloud Object Storage). Nguyên nhân phát sinh do đâu và hậu quả tiêu cực của nó là gì?
* **expected_key_points:**
  - id: KP4_1
    content: Nguyên nhân phát sinh hệ thống file nhỏ từ pipeline dữ liệu
    keypoint_weight: 0.4
    description: Phát sinh khi các pipeline dữ liệu (đặc biệt là Near Real-time/Streaming) ghi dữ liệu liên tục xuống hệ thống lưu trữ thành hàng triệu file có kích thước quá nhỏ (vài KB đến vài MB) thay vì gom cụm lại.
  - id: KP4_2
    content: Hậu quả tiêu cực lên bộ nhớ quản lý Metadata (NameNode)
    keypoint_weight: 0.3
    description: Trong các hệ thống như HDFS, NameNode phải lưu giữ thông tin metadata của mọi file trên RAM. Quá nhiều file nhỏ sẽ làm phình to dung lượng metadata và gây tràn bộ nhớ RAM của NameNode điều phối trung tâm.
  - id: KP4_3
    content: Hậu quả tiêu cực làm suy giảm tốc độ truy vấn đọc (I/O Overhead)
    keypoint_weight: 0.3
    description: Khi thực hiện câu lệnh phân tích, các công cụ (như Spark, Hive) phải tốn rất nhiều chi phí mở/đóng và quét metadata của hàng triệu file nhỏ qua mạng, tạo ra chi phí I/O mạng cực lớn và làm giảm mạnh tốc độ đọc dữ liệu.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong Apache Spark, cơ chế tối ưu hóa "Lazy Evaluation" (Đánh giá lười biếng) hoạt động ra sao? Hãy phân biệt sự khác nhau về logic hệ thống giữa các phép toán Transformation và Action.
* **expected_key_points:**
  - id: KP5_1
    content: Nguyên lý xây dựng kế hoạch chạy của Lazy Evaluation
    keypoint_weight: 0.4
    description: Spark không thực thi tính toán vật lý ngay lập tức khi lập trình viên khai báo câu lệnh, mà chỉ ghi nhận các bước xử lý đó vào một sơ đồ kế hoạch logic gọi là DAG. Việc tính toán thực tế chỉ được kích hoạt khi gặp một lệnh Action.
  - id: KP5_2
    content: Logic không sinh dữ liệu vật lý của Transformation
    keypoint_weight: 0.3
    description: Transformation là các phép toán biến đổi dữ liệu (như `map`, `filter`, `join`) dùng để xây dựng nên DAG kế hoạch logic và luôn trả về một DataFrame/RDD mới mà không làm phát sinh chi phí tính toán trên RAM/Đĩa.
  - id: KP5_3
    content: Logic kích hoạt luồng xử lý thực tế của Action
    keypoint_weight: 0.3
    description: Action là các phép toán yêu cầu trả kết quả đầu ra về cho Driver Node hoặc ghi dữ liệu xuống đĩa (như `collect`, `count`, `write`). Khi Action được gọi, Spark Catalyst Optimizer mới tối ưu hóa DAG và đẩy Tasks vật lý xuống các Executor để chạy.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi thiết kế một quy trình nạp dữ liệu tăng trưởng (Incremental Load Data Pipeline), bạn hiểu thế nào là kỹ thuật "Upsert" (Merge) và nó giải quyết khuyết điểm gì của phép toán Append hoặc Overwrite thuần túy?
* **expected_key_points:**
  - id: KP6_1
    content: Logic kết hợp cập nhật và thêm mới dữ liệu của Upsert
    keypoint_weight: 0.5
    description: Upsert (Update + Insert) thực hiện đối chiếu khóa chính: nếu bản ghi từ nguồn đã tồn tại ở đích thì tiến hành cập nhật trạng thái mới (Update); nếu bản ghi chưa tồn tại thì tiến hành chèn dòng mới vào bảng (Insert).
  - id: KP6_2
    content: Khắc phục lỗi trùng lặp và chi phí tính toán của Append/Overwrite
    keypoint_weight: 0.5
    description: Giải quyết lỗi bị trùng lặp dữ liệu (Duplicate) của phép toán `Append` khi chạy lại pipeline, đồng thời loại bỏ chi phí tài nguyên khổng lồ của phép toán `Overwrite` (phải xóa đi ghi lại toàn bộ bảng cũ không đổi), giúp pipeline đạt tính lũy đẳng (Idempotency).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong thiết kế kho dữ liệu (Data Warehouse) theo mô hình Dimensional Modeling, tại sao lập trình viên Data Engineer nên sử dụng "Surrogate Key" (Khóa thay thế) làm Khóa chính cho bảng Dimension thay vì dùng trực tiếp "Natural Key" (Khóa tự nhiên)?
* **expected_key_points:**
  - id: KP7_1
    content: Định nghĩa bản chất kỹ thuật của Surrogate Key
    keypoint_weight: 0.3
    description: Surrogate Key là một trường số nguyên (Integer) tự tăng được sinh ra và quản lý nội bộ bên trong Data Warehouse, hoàn toàn độc lập và không mang ý nghĩa nghiệp vụ kinh doanh.
  - id: KP7_2
    content: Bảo vệ cấu trúc kho dữ liệu khỏi sự thay đổi logic của hệ thống nguồn
    keypoint_weight: 0.4
    description: Natural Key (như số CCCD, mã SKU, ID nhân viên) có thể bị hệ thống nguồn thay đổi logic, thay đổi định dạng chuỗi văn bản hoặc tái sử dụng lại. Surrogate Key giúp Data Warehouse cách ly, bảo toàn tính nhất quán và lưu vết được lịch sử dữ liệu (như SCD Type 2).
  - id: KP7_3
    content: Tối ưu hóa hiệu năng thực thi phép toán liên kết bảng (JOIN Performance)
    keypoint_weight: 0.3
    description: Thực hiện phép toán JOIN giữa các bảng lớn bằng kiểu dữ liệu số nguyên (Surrogate Key) giúp Database Engine tối ưu bộ nhớ và tính toán nhanh hơn rất nhiều so với JOIN bằng các chuỗi văn bản dài (String/Varchar) của Natural Key.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong công nghệ tính toán dữ liệu phân tán (như Apache Spark), tiến trình "Shuffle" là gì? Tại sao tiến trình này là tác nhân gây thắt nút cổ chai hiệu năng hệ thống nặng nề nhất và nêu hai giải pháp cấu trúc mã nguồn để giảm thiểu nó?
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất tái phân phối dữ liệu qua mạng vật lý của tiến trình Shuffle
    keypoint_weight: 0.4
    description: Shuffle là quá trình phân phối, sắp xếp và xáo trộn lại dữ liệu giữa các phân vùng (Partitions) trên toàn bộ các Node trong cụm cluster, xảy ra khi hệ thống cần gom nhóm dữ liệu có chung thuộc tính khóa (như `groupByKey`, `join`, `reduceByKey`).
  - id: KP8_2
    content: Chi phí tài nguyên cực lớn đè nặng lên I/O Đĩa cứng và Mạng (Disk & Network Bottleneck)
    keypoint_weight: 0.3
    description: Shuffle ép buộc các Node phải ghi dữ liệu trung gian xuống đĩa cứng cục bộ (Disk I/O), sau đó truyền tải lượng lớn dữ liệu thô này qua hạ tầng mạng vật lý (Network I/O) tới các Node khác, rất dễ gây nghẽn mạch mạng, chậm hệ thống hoặc lỗi tràn bộ nhớ (OOM).
  - id: KP8_3
    content: Giải pháp kỹ thuật giảm thiểu Shuffle ở mức lập trình
    keypoint_weight: 0.3
    description: Sử dụng cơ chế Broadcast Hash Join đối với phép JOIN giữa bảng lớn và bảng nhỏ để sao chép trực tiếp bảng nhỏ sang RAM của các Node, loại bỏ hoàn toàn Shuffle qua mạng; hoặc thay thế hàm `groupByKey` bằng hàm `reduceByKey`/`aggregateByKey` để gộp bớt dữ liệu cục bộ trước khi truyền đi (Map-side aggregation).

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích sâu cơ chế hoạt động kiến trúc ngầm của định dạng bảng Delta Lake giúp hệ thống này đảm bảo được tính chất giao dịch ACID Transactions và cung cấp tính năng "Time Travel" trên nền tảng tệp tin tĩnh (như Parquet lưu trên Cloud).
* **expected_key_points:**
  - id: KP9_1
    content: Vai trò định danh trạng thái của tệp nhật ký giao dịch tuần tự (Delta Transaction Log / Commit Log)
    keypoint_weight: 0.4
    description: Delta Lake duy trì một thư mục nhật ký chạy ngầm chứa các file JSON ghi nhận theo thứ tự thời gian tuyến tính mọi hành động thay đổi cấu trúc bảng (file nào được thêm, file nào bị hủy hiệu lực). File log này là nguồn chân lý duy nhất định nghĩa trạng thái phiên bản của bảng dữ liệu.
  - id: KP9_2
    content: Tính chất bất biến của tệp dữ liệu vật lý (Immutability) dưới đĩa cứng
    keypoint_weight: 0.4
    description: Toàn bộ các file lưu trữ Parquet vật lý đều mang tính chất bất biến (Immutable). Khi có lệnh sửa đổi hoặc xóa dữ liệu (UPDATE, DELETE), hệ thống sẽ ghi các file Parquet mới chứa dữ liệu thay đổi chứ không sửa trên file cũ, đồng thời cập nhật vào Transaction Log rằng file cũ đã hết hiệu lực từ Version hiện tại.
  - id: KP9_3
    content: Cơ chế khôi phục trạng thái lịch sử (State Reconstruction) của tính năng Time Travel
    keypoint_weight: 0.2
    description: Khi người dùng gọi truy vấn Time Travel về một phiên bản/mốc thời gian cụ thể, hệ thống sẽ đọc chuỗi file JSON trong Transaction Log từ đầu lùi tới mốc yêu cầu để dựng lại chính xác danh sách các file Parquet vật lý nào có giá trị tại thời điểm đó và chỉ nạp đúng các file này lên RAM.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong kiến trúc xử lý dữ liệu thời gian thực luồng (Stream Processing), hãy giải thích sự khác biệt logic giữa ba khái niệm mốc thời gian: Event Time, Ingestion Time, và Processing Time. Cơ chế "Watermark" kết hợp với hệ thống Windowing xử lý bài toán dữ liệu đến muộn (Late Data) dựa trên nguyên lý kỹ thuật nào?
* **expected_key_points:**
  - id: KP10_1
    content: Phân biệt bản chất ý nghĩa của ba khái niệm mốc thời gian
    keypoint_weight: 0.4
    description: - **Event Time:** Thời điểm sự kiện thực sự xảy ra ở thiết bị nguồn (gắn liền trong payload dữ liệu).
                 - **Ingestion Time:** Thời điểm sự kiện được nạp thành công vào hệ thống tiếp nhận trung gian (như Kafka topic).
                 - **Processing Time:** Thời điểm sự kiện được luồng tính toán (như Spark Streaming, Flink) thực thi xử lý trực tiếp trên bộ nhớ RAM.
  - id: KP10_2
    content: Bản chất thước đo thời gian logic tịnh tiến của cơ chế Watermark
    keypoint_weight: 0.3
    description: Watermark là một mốc thời gian logic di chuyển tịnh tiến đại diện cho tiến trình của Event Time. Nó là một cam kết kỹ thuật của hệ thống: "giả định từ thời điểm này trở đi, sẽ không còn dữ liệu nào có Event Time cũ hơn mốc $T$ xuất hiện nữa", dùng để quản lý vòng đời của cửa sổ thời gian.
  - id: KP10_3
    content: Cơ chế quản lý độ trễ chấp nhận dữ liệu muộn và đóng cửa sổ tính toán
    keypoint_weight: 0.3
    description: Watermark cấu hình một khoảng thời gian trễ cho phép (thùng chứa mở rộng) để gom các dữ liệu bị đến muộn do nghẽn mạng vật lý. Khi mốc toán học của Watermark vượt qua biên đóng của cửa sổ (Window End), hệ thống sẽ lập tức khóa chặt cửa sổ, tính toán kết quả tổng hợp cuối cùng và giải phóng RAM, bỏ qua mọi dữ liệu đến trễ hơn mốc Watermark này.