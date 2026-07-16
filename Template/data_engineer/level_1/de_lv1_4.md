# Bộ Câu Hỏi Phỏng Vấn Data Engineer (Level 1)

* **Role:** Data Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế cơ sở dữ liệu quan hệ (RDBMS), tại sao việc thiết kế chuẩn hóa dữ liệu (Database Normalization - đến mức 3NF) là bắt buộc cho hệ thống OLTP?
* **expected_key_points:**
  - id: KP1_1
    content: Triệt tiêu sự dư thừa dữ liệu và lỗi bất thường khi cập nhật (Data Redundancy & Anomalies)
    keypoint_weight: 0.5
    description: Chuẩn hóa chia nhỏ các bảng dữ liệu để loại bỏ việc lưu trữ lặp đi lặp lại một thông tin, ngăn chặn các lỗi bất thường khi thêm, sửa hoặc xóa dữ liệu (Insertion, Update, Deletion Anomalies).
  - id: KP1_2
    content: Đảm bảo tính toàn vẹn dữ liệu và tối ưu cho tác vụ ghi nhanh (ACID & Write Performance)
    keypoint_weight: 0.5
    description: Giúp hệ thống OLTP duy trì các ràng buộc toàn vẹn một cách dễ dàng, đồng thời tối ưu hóa tốc độ ghi (Write) vì Database Engine chỉ cần thực hiện ghi thông tin vào một nơi duy nhất.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong hệ sinh thái dữ liệu, sự khác biệt cơ bản về mặt kiến trúc, cấu trúc dữ liệu lưu trữ và mục đích sử dụng giữa Data Lake (Hồ dữ liệu) và Data Warehouse (Kho dữ liệu) là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Phân biệt cấu trúc dữ liệu lưu trữ (Structured vs Raw data)
    keypoint_weight: 0.5
    description: Data Warehouse chỉ lưu trữ dữ liệu đã được cấu trúc hóa chặt chẽ (Schema-on-write), sạch và đã được chuyển đổi. Data Lake lưu trữ mọi dạng dữ liệu thô (Schema-on-read) từ có cấu trúc, bán cấu trúc cho đến phi cấu trúc (như logs, images, PDFs).
  - id: KP2_2
    content: Phân biệt về đối tượng sử dụng và mục tiêu phân tích (BI vs Advanced Analytics)
    keypoint_weight: 0.5
    description: Data Warehouse phục vụ chính cho việc làm báo cáo tĩnh, phân tích BI của doanh nghiệp. Data Lake là nền tảng cho khoa học dữ liệu (Data Science), học máy (Machine Learning) và các phân tích khám phá chuyên sâu.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt điểm khác nhau về cơ chế hoạt động mạng và logic xử lý dữ liệu giữa hai kiến trúc Data Pipeline: ETL (Extract, Transform, Load) và ELT (Extract, Load, Transform).
* **expected_key_points:**
  - id: KP3_1
    content: Thứ tự thực thi biến đổi và vị trí xử lý dữ liệu
    keypoint_weight: 0.5
    description: ETL thực hiện biến đổi dữ liệu (Transform) trên một máy chủ trung gian trước khi nạp vào kho lưu trữ đích. ELT nạp trực tiếp dữ liệu thô vào hệ thống đích trước, sau đó mới thực hiện biến đổi ngay tại đích.
  - id: KP3_2
    content: Sự phụ thuộc vào sức mạnh tính toán của hệ thống đích
    keypoint_weight: 0.5
    description: ETL chịu tải tính toán trên công cụ xử lý riêng (SaaS, Spark). ELT tận dụng trực tiếp năng lực tính toán phân tán (MPP Engine) cực mạnh của các Modern Cloud Data Warehouses (như BigQuery, Snowflake) để biến đổi dữ liệu bằng SQL.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi xây dựng mô hình dữ liệu Dimensional Modeling cho Data Warehouse, kỹ thuật "Surrogate Key" (Khóa thay thế) là gì và tại sao chúng ta nên sử dụng nó thay thế cho "Natural Key" (Khóa tự nhiên)?
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa bản chất của Surrogate Key
    keypoint_weight: 0.4
    description: Khóa thay thế là một trường số nguyên tự tăng (Integer), độc lập hoàn toàn, không mang ý nghĩa nghiệp vụ, được tạo ra và quản lý nội bộ bên trong Data Warehouse để làm Khóa chính cho bảng Dimension.
  - id: KP4_2
    content: Bảo vệ hệ thống khỏi sự thay đổi logic nghiệp vụ của Natural Key
    keypoint_weight: 0.3
    description: Khóa tự nhiên (như ID nhân viên, số CCCD) có thể bị thay đổi cấu trúc hoặc định dạng do chính sách của hệ thống nguồn (Source system). Sử dụng Surrogate Key giúp Data Warehouse cô lập và bảo vệ cấu trúc liên kết nội bộ không bị phá vỡ.
  - id: KP4_3
    content: Tối ưu hóa hiệu năng truy vấn liên kết bảng (JOIN Performance)
    keypoint_weight: 0.3
    description: Thực hiện phép toán JOIN giữa các bảng bằng các trường số nguyên (Surrogate Key) luôn nhanh hơn và tiêu tốn ít tài nguyên CPU/RAM hơn rất nhiều so với JOIN bằng các chuỗi văn bản dài (Text/Varchar Keys).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong Apache Spark, cơ chế tính toán chạy ngầm "Lazy Evaluation" (Đánh giá lười biếng) là gì? Hãy phân biệt sự khác nhau về mặt logic hoạt động giữa "Transformations" và "Actions".
* **expected_key_points:**
  - id: KP5_1
    content: Nguyên lý trì hoãn thực thi của Lazy Evaluation
    keypoint_weight: 0.4
    description: Spark không thực thi trực tiếp các câu lệnh biến đổi ngay khi chúng được khai báo, mà chỉ ghi nhận chúng vào một chuỗi kế hoạch thực thi logic gọi là DAG (Directed Acyclic Graph). Việc tính toán thực sự chỉ bắt đầu khi một Action được kích hoạt.
  - id: KP5_2
    content: Bản chất tạo kế hoạch logic của Transformations
    keypoint_weight: 0.3
    description: Transformations là các phép toán biến đổi một RDD/DataFrame này thành một RDD/DataFrame mới (ví dụ: `map`, `filter`, `groupBy`). Chúng chỉ đóng vai trò dựng DAG và không làm phát sinh tính toán vật lý.
  - id: KP5_3
    content: Bản chất kích hoạt dòng chảy dữ liệu của Actions
    keypoint_weight: 0.3
    description: Actions là các phép toán yêu cầu trả kết quả về cho Driver program hoặc ghi dữ liệu xuống hệ thống lưu trữ ngoại vi (ví dụ: `collect`, `count`, `save`). Khi gọi Action, Spark mới biên dịch DAG thành các Stages/Tasks vật lý và gửi xuống các Executor chạy.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi thiết kế một pipeline thu thập dữ liệu định kỳ (Scheduled Batch Pipeline), bạn hiểu thế nào là cơ chế nạp dữ liệu "Incremental Load" (Nạp tăng trưởng) và nó tối ưu hơn "Full Load" (Nạp toàn bộ) ở điểm nào?
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế nhận diện dữ liệu mới phát sinh (Delta Data)
    keypoint_weight: 0.5
    description: Incremental Load chỉ thực hiện trích xuất và nạp phần dữ liệu mới được thêm vào hoặc có sự thay đổi kể từ lần chạy pipeline thành công gần nhất (thường dựa vào trường `updated_at` hoặc CDC logs).
  - id: KP6_2
    content: Tối ưu hóa băng thông đường truyền và tải hệ thống nguồn
    keypoint_weight: 0.5
    description: Giảm thiểu tối đa dung lượng dữ liệu truyền tải qua mạng và tài nguyên tính toán I/O của hệ thống nguồn (Source), tránh việc quét lại hàng tỷ bản ghi cũ không đổi của Full Load, giúp pipeline hoàn thành nhanh hơn.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy giải thích hiện tượng "Small Files Problem" (Vấn đề file nhỏ) thường gặp trong các Data Lake sử dụng HDFS hoặc S3 Cloud Storage. Nguyên nhân phát sinh và giải pháp khắc phục cơ bản là gì?
* **expected_key_points:**
  - id: KP7_1
    content: Nguyên nhân quá tải bộ nhớ NameNode hoặc tăng chi phí I/O metadata
    keypoint_weight: 0.5
    description: Phát sinh khi pipeline ghi dữ liệu tạo ra hàng triệu tệp tin kích thước quá nhỏ (vài KB đến vài MB), thường do ghi dữ liệu streaming liên tục mà không gom cụm. Trong HDFS, mỗi tệp tin tiêu tốn khoảng 150 bytes RAM của NameNode để lưu metadata, dễ gây tràn bộ nhớ NameNode. Trên Cloud Storage, quá nhiều file nhỏ làm tăng vọt chi phí gọi API truy vấn metadata và làm chậm tốc độ đọc đĩa.
  - id: KP7_2
    content: Giải pháp khắc phục bằng cơ chế gộp tệp tin (Compaction)
    keypoint_weight: 0.5
    description: Sử dụng các tiến trình chạy ngầm hoặc định kỳ để đọc và gộp (Compaction/Merge) nhiều tệp tin nhỏ thành các tệp tin lớn có kích thước tối ưu (thông thường từ 128MB đến 512MB) trước khi nạp vào các bảng phân tích phân tầng.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong tính toán dữ liệu phân tán, tiến trình "Shuffle" là gì? Tại sao lập trình viên Data Engineer cần phải tối thiểu hóa tiến trình Shuffle này trong các Spark Jobs và nêu một kỹ thuật để đạt được điều đó?
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất tái phân phối dữ liệu qua mạng của Shuffle
    keypoint_weight: 0.4
    description: Shuffle là tiến trình phân phối và sắp xếp lại dữ liệu giữa các phân vùng (Partitions) trên toàn bộ các Node trong cụm cluster, xảy ra khi thực hiện các phép toán nhóm hoặc liên kết bảng (như `groupByKey`, `join`).
  - id: KP8_2
    content: Thắt nút cổ chai hiệu năng do chi phí ghi đĩa và truyền tải mạng (Disk & Network I/O)
    keypoint_weight: 0.3
    description: Shuffle bắt buộc các Node phải ghi dữ liệu trung gian xuống đĩa cứng cục bộ, sau đó truyền tải lượng lớn dữ liệu này qua mạng vật lý tới các Node khác, tạo ra chi phí I/O cực lớn và dễ gây lỗi nghẽn mạng hoặc tràn bộ nhớ (OOM).
  - id: KP8_3
    content: Giải pháp giảm thiểu Shuffle bằng kỹ thuật Broadcast Join hoặc Map-side aggregation
    keypoint_weight: 0.3
    description: Sử dụng Broadcast Hash Join đối với các bảng nhỏ để sao chép trực tiếp bảng nhỏ sang tất cả Worker Nodes, loại bỏ hoàn toàn việc Shuffle bảng lớn; hoặc sử dụng các hàm gộp tối ưu như `reduceByKey` thay cho `groupByKey` để giảm dung lượng dữ liệu cần truyền qua mạng.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong thiết kế kiến trúc Data Lakehouse, tại sao định dạng bảng hiện đại Delta Lake lại hỗ trợ được tính chất ACID (Atomicity, Consistency, Isolation, Durability) trên môi trường lưu trữ tệp tin tĩnh (như Parquet trên AWS S3)?
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế quản lý bằng nhật ký giao dịch tuần tự (Delta Transaction Log / Commit Log)
    keypoint_weight: 0.4
    description: Delta Lake duy trì một thư mục nhật ký giao dịch chạy ngầm ghi nhận chi tiết mọi trạng thái thay đổi bảng dưới dạng các file JSON tuần tự. Đây là nguồn chân lý duy nhất (Single source of truth) định nghĩa các file Parquet vật lý nào đang thực sự có hiệu lực.
  - id: KP9_2
    content: Cơ chế ghi nạp bất biến và kiểm soát tương thời bằng lạc quan (Optimistic Concurrency Control)
    keypoint_weight: 0.4
    description: Các tệp tin dữ liệu Parquet dưới đĩa cứng là bất biến (Immutable). Khi có thao tác cập nhật hoặc xóa dữ liệu, hệ thống ghi các file Parquet mới chứa dữ liệu thay đổi, đồng thời ghi nhận vào Transaction Log. Sử dụng cơ chế OCC để kiểm tra chéo, nếu hai giao dịch không xung đột dữ liệu thì cả hai cùng commit, nếu xung đột hệ thống tự động rollback một giao dịch.
  - id: KP9_3
    content: Khả năng tự động khôi phục và đảm bảo tính nhất quán của bảng (Atomicity)
    keypoint_weight: 0.2
    description: Một giao dịch ghi dữ liệu chỉ được coi là thành công khi và chỉ khi file log JSON tương ứng của nó được ghi thành công vào thư mục Transaction Log, đảm bảo không xảy ra trạng thái ghi dở dang nửa chừng làm hỏng dữ liệu.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong xử lý dữ liệu thời gian thực (Stream Processing), hãy giải thích sự khác biệt logic giữa "Sliding Window" (Cửa sổ trượt) và "Tumbling Window" (Cửa sổ nhảy). Nêu tình huống thực tế áp dụng hiệu quả cho mỗi loại cửa sổ.
* **expected_key_points:**
  - id: KP10_1
    content: Bản chất không chồng chéo và ví dụ của Tumbling Window
    keypoint_weight: 0.5
    description: Tumbling Window là cửa sổ thời gian có kích thước cố định, di chuyển nối tiếp liên tục và hoàn toàn không chồng chéo lên nhau (ví dụ: cứ mỗi 5 phút tính toán một lần). Phù hợp cho việc thống kê báo cáo định kỳ không trùng lặp, như đếm số lượng giao dịch mua hàng phát sinh trong mỗi giờ.
  - id: KP10_2
    content: Bản chất chồng chéo linh hoạt và ví dụ của Sliding Window
    keypoint_weight: 0.5
    description: Sliding Window là cửa sổ có kích thước cố định $W$ nhưng trượt tiến theo một chu kỳ $S$ nhỏ hơn $W$, dẫn đến việc các cửa sổ có phần dữ liệu chồng chéo lên nhau (ví dụ: tính toán dữ liệu trong 10 phút gần nhất, cứ sau mỗi 1 phút lại cập nhật kết quả). Phù hợp cho các bài toán giám sát liên tục theo thời gian thực, như phát hiện cảnh báo lỗi hệ thống nếu số lượng request thất bại vượt ngưỡng trong vòng 10 phút qua.