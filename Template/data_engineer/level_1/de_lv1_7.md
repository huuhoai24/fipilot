# Bộ Câu Hỏi Phỏng Vấn Data Engineer (Level 1)

* **Role:** Data Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế cơ sở dữ liệu quan hệ, việc tạo chỉ mục (Index) giúp tăng tốc độ truy vấn đọc dữ liệu dựa trên nguyên lý cấu trúc gì và điểm đánh đổi tiêu cực của nó đối với các tác vụ ghi (Write Operations) là gì?
* **expected_key_points:**
  - id: KP1_1
    content: Nguyên lý cấu trúc cây tìm kiếm để giảm thiểu phạm vi quét đĩa (B-Tree/Hash)
    keypoint_weight: 0.5
    description: Index tạo ra một cấu trúc dữ liệu phụ trợ (thường là B-Tree) sắp xếp dữ liệu theo thứ tự logic, giúp Database Engine tìm kiếm bản ghi với độ phức tạp O(log N) thay vì phải quét toàn bộ bảng (Full Table Scan) với độ phức tạp O(N).
  - id: KP1_2
    content: Đánh đổi chi phí tính toán và không gian lưu trữ cho tác vụ ghi (Write Overhead)
    keypoint_weight: 0.5
    description: Mỗi khi có thao tác ghi dữ liệu (INSERT, UPDATE, DELETE), Database không chỉ ghi vào bảng vật lý mà còn bắt buộc phải cập nhật và tái cấu trúc lại cây chỉ mục, làm chậm tốc độ ghi và tiêu tốn thêm dung lượng đĩa cứng để lưu trữ cấu trúc Index.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Khi lưu trữ dữ liệu lớn trong các hệ thống hồ dữ liệu (Data Lake), hãy phân biệt điểm khác biệt cơ bản về mặt cấu trúc và mục đích sử dụng giữa hai định dạng tệp tin: CSV và Apache Parquet.
* **expected_key_points:**
  - id: KP2_1
    content: Bản chất lưu trữ dạng dòng, văn bản thô của định dạng CSV
    keypoint_weight: 0.5
    description: CSV là định dạng lưu trữ dạng dòng (Row-oriented), lưu dữ liệu dưới dạng văn bản thô (Plain text), không lưu trữ siêu dữ liệu (Metadata) về kiểu dữ liệu. CSV dễ đọc bởi con người nhưng tốn dung lượng lưu trữ và có hiệu năng truy vấn phân tích rất kém.
  - id: KP2_2
    content: Bản chất lưu trữ dạng cột, tối ưu nén của định dạng Parquet
    keypoint_weight: 0.5
    description: Parquet là định dạng lưu trữ dạng cột (Columnar), lưu trữ dữ liệu dưới dạng nhị phân (Binary) tích hợp sẵn Metadata về Schema của bảng. Parquet hỗ trợ nén dữ liệu cực tốt, tối ưu cho việc đọc một vài cột cụ thể trong các câu lệnh phân tích quy mô lớn mà không cần quét toàn bộ tệp tin.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế luồng xử lý dữ liệu (Data Pipelines), hãy phân biệt sự khác biệt cơ bản về cơ chế hoạt động và tần suất xử lý giữa hai mô hình: Batch Processing (Xử lý theo lô) và Stream Processing (Xử lý luồng).
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế tích lũy dữ liệu định kỳ của Batch Processing
    keypoint_weight: 0.5
    description: Batch Processing thu thập dữ liệu thô và tích lũy lại thành một lô lớn trong một khoảng thời gian định sẵn (theo giờ, ngày, tuần) rồi mới kích hoạt hệ thống tính toán xử lý cùng một lúc. Mô hình này chấp nhận độ trễ dữ liệu cao (High Latency) nhưng tối ưu chi phí tính toán lượng lớn dữ liệu lịch sử.
  - id: KP3_2
    content: Cơ chế xử lý liên tục thời gian thực của Stream Processing
    keypoint_weight: 0.5
    description: Stream Processing tiếp nhận và tính toán xử lý dữ liệu ngay lập tức trên từng bản ghi (Event-by-event) tại thời điểm nó phát sinh. Mô hình này yêu cầu độ trễ cực thấp (Low Latency), phù hợp cho các bài toán nhạy cảm về thời gian thực như phát hiện gian lận tài chính, giám sát hệ thống.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi thiết kế kho dữ liệu (Data Warehouse) theo mô hình Dimensional Modeling, kỹ thuật "Slowly Changing Dimension" (SCD) được áp dụng để giải quyết bài toán gì? Hãy phân biệt cơ chế lưu trữ lịch sử giữa SCD Type 1 và SCD Type 2.
* **expected_key_points:**
  - id: KP4_1
    content: Bài toán quản lý sự thay đổi thông tin thuộc tính theo thời gian
    keypoint_weight: 0.4
    description: SCD giải quyết bài toán làm thế nào để lưu trữ và quản lý các dữ liệu thuộc tính trong bảng Dimension bị thay đổi chậm theo thời gian (ví dụ: khách hàng thay đổi địa chỉ cư trú, nhân viên chuyển phòng ban).
  - id: KP4_2
    content: Cơ chế ghi đè trực tiếp không lưu lịch sử của SCD Type 1
    keypoint_weight: 0.3
    description: SCD Type 1 thực hiện ghi đè (Overwrite) trực tiếp giá trị mới lên trường dữ liệu cũ. Phương pháp này đơn giản, tiết kiệm dung lượng nhưng làm mất hoàn toàn dấu vết lịch sử biến động của dữ liệu.
  - id: KP4_3
    content: Cơ chế tạo dòng mới lưu vết lịch sử của SCD Type 2
    keypoint_weight: 0.3
    description: SCD Type 2 thực hiện tạo một dòng mới (New Row) trong bảng chứa giá trị mới, kết hợp thêm các cột trạng thái (như `Effective_Date`, `End_Date`, `Is_Current`) để đánh dấu phiên bản dữ liệu. Cách này giúp lưu trữ lịch sử biến động hoàn chỉnh của thực thể nhưng làm bảng phình to nhanh hơn.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong công nghệ xử lý dữ liệu phân tán Apache Spark, hai khái niệm "Driver" và "Executor" đóng vai trò logic gì trong kiến trúc vận hành của một ứng dụng (Application)?
* **expected_key_points:**
  - id: KP5_1
    content: Vai trò điều phối, lập kế hoạch của Driver Node
    keypoint_weight: 0.5
    description: Driver là tiến trình trung tâm điều hành ứng dụng. Nó chịu trách nhiệm biên dịch code của lập trình viên thành các tác vụ tính toán logic (DAG - Directed Acyclic Graph), phân chia công việc thành các Stages/Tasks và lên lịch trình (Scheduler) phân phối chúng xuống các Worker Nodes.
  - id: KP5_2
    content: Vai trò thực thi tính toán trực tiếp của Executor Node
    keypoint_weight: 0.5
    description: Executor là các tiến trình chạy ngầm trên các Worker Nodes chịu trách nhiệm trực tiếp thực thi các Tasks tính toán do Driver gửi xuống, lưu trữ kết quả tính toán tạm thời vào bộ nhớ RAM hoặc đĩa cứng (Cache/BlockManager) và báo cáo trạng thái hoàn thành về cho Driver.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi xây dựng pipeline ETL thu thập dữ liệu từ các ứng dụng nguồn (SaaS APIs, DBs) về Data Lake, tại sao việc thiết kế cơ chế "Idempotency" (Tính lũy đẳng) lại là tiêu chuẩn bắt buộc? Hãy nêu một ví dụ thực tế về lỗi hệ thống nếu thiếu tính chất này.
* **expected_key_points:**
  - id: KP6_1
    content: Bản chất đảm bảo kết quả không đổi khi thực thi lại nhiều lần
    keypoint_weight: 0.5
    description: Idempotency đảm bảo rằng dù một pipeline hoặc một câu lệnh ghi dữ liệu được thực thi lại một hay nhiều lần với cùng một tập dữ liệu đầu vào, kết quả trạng thái dữ liệu cuối cùng tại hệ thống đích vẫn hoàn toàn nhất quán và không thay đổi.
  - id: KP6_2
    content: Ngăn chặn lỗi trùng lặp dữ liệu kèm ví dụ thực tế
    keypoint_weight: 0.5
    description: Nếu gặp sự cố mạng làm đứt kết nối giữa chừng khiến hệ thống tự động chạy lại (Retry), việc thiếu Idempotency sẽ gây ra lỗi duplicate (trùng lặp) dữ liệu ở đích. Ví dụ: pipeline nạp đơn hàng bị chạy lại khiến một đơn hàng của khách bị insert 2 lần vào bảng Doanh thu, gây sai lệch báo cáo tài chính.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong kỹ nghệ dữ liệu, mô hình kiến trúc ELT (Extract, Load, Transform) đang dần thay thế mô hình ETL (Extract, Transform, Load) truyền thống nhờ tận dụng lợi thế công nghệ gì từ các Modern Cloud Data Warehouses (như Snowflake, BigQuery)?
* **expected_key_points:**
  - id: KP7_1
    content: Tách biệt tài nguyên tính toán và lưu trữ để lưu thô trước (Load first)
    keypoint_weight: 0.5
    description: ELT đẩy dữ liệu thô trực tiếp vào Data Lake/Warehouse trước khi biến đổi, giúp giảm thiểu tối đa thời gian xử lý trung gian và rủi ro mất mát dữ liệu. Việc này khả thi nhờ chi phí lưu trữ trên Cloud hiện nay cực kỳ rẻ.
  - id: KP7_2
    content: Tận dụng sức mạnh xử lý song song cực lớn (MPP) của Warehouse đích
    keypoint_weight: 0.5
    description: Thay vì sử dụng một công cụ trung gian (như Spark, Talend) để Transform dữ liệu bên ngoài, ELT sử dụng chính tài nguyên tính toán phân tán (MPP Engine) cực mạnh của BigQuery/Snowflake để thực thi các câu lệnh SQL biến đổi dữ liệu trực tiếp tại đích, giúp tối ưu tốc độ xử lý trên quy mô dữ liệu lớn.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Khi cấu hình cụm máy chủ xử lý dữ liệu lớn (Big Data Cluster), hiện tượng "Data Skew" (Lệch dữ liệu) là gì? Hiện tượng này làm ảnh hưởng tiêu cực như thế nào đến thời gian chạy của Job phân tán và cách khắc phục ở mức lập trình dữ liệu?
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất phân bổ dữ liệu mất cân bằng giữa các phân vùng (Partitions)
    keypoint_weight: 0.4
    description: Data Skew xảy ra khi một hoặc một vài phân vùng (Partitions) chứa lượng dữ liệu khổng lồ vượt trội hoàn toàn so với các phân vùng còn lại (thường do chọn Key để băm/chia nhóm dữ liệu bị trùng lặp quá nhiều, ví dụ giá trị NULL hoặc mã ID phổ biến).
  - id: KP8_2
    content: Gây thắt nút cổ chai hiệu năng do quy luật Node chạy chậm nhất (Straggler task)
    keypoint_weight: 0.3
    description: Trong tính toán phân tán, một Stage chỉ hoàn thành khi Task cuối cùng chạy xong. Node nhận phân vùng bị lệch (Skewed partition) sẽ phải xử lý lâu hơn, tiêu tốn nhiều RAM/CPU dẫn đến lỗi tràn bộ nhớ (OOM) trong khi các node khác đã rảnh rỗi, kéo dài thời gian chạy của toàn bộ Job.
  - id: KP8_3
    content: Giải pháp khắc phục bằng kỹ thuật nhiễu muối (Salting) hoặc lọc lọc phân tách
    keypoint_weight: 0.3
    description: Áp dụng kỹ thuật Salting (thêm một chuỗi số ngẫu nhiên vào Key bị lệch trước khi thực hiện phép Join/Group by để ép dữ liệu phân bổ đều ra các phân vùng khác nhau), hoặc thực hiện lọc tách riêng nhóm dữ liệu bị lệch ra để xử lý bằng Broadcast Join rồi gộp (Union) lại sau.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Khi thiết kế một hệ thống Data Lakehouse sử dụng cấu trúc bảng Delta Table, hãy giải thích nguyên lý kỹ thuật giúp hệ thống này thực hiện được tính năng "Time Travel" (Truy cập dữ liệu lịch sử tại một thời điểm) mà không cần sao chép nhân bản các tệp tin vật lý thành nhiều phiên bản.
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế quản lý trạng thái bằng tệp nhật ký giao dịch (Delta Transaction Log / Commit Log)
    keypoint_weight: 0.4
    description: Delta Lake duy trì một thư mục nhật ký giao dịch chạy ngầm ghi nhận chi tiết mọi hoạt động thay đổi cấu trúc bảng (nhập thêm file, xóa file, sửa đổi schema) dưới dạng các file JSON tuần tự. Đây là "nguồn chân lý duy nhất" (Single source of truth) định nghĩa trạng thái của bảng.
  - id: KP9_2
    content: Cơ chế bất biến của tệp dữ liệu vật lý (Immutability) và lưu trữ Delta
    keypoint_weight: 0.4
    description: Các tệp tin dữ liệu Parquet vật lý dưới đĩa cứng là bất biến (Immutable). Khi có thao tác sửa đổi hoặc xóa dữ liệu (UPDATE, DELETE), hệ thống không can thiệp vào file cũ mà chỉ viết các file Parquet mới chứa dữ liệu thay đổi, đồng thời ghi nhận vào Transaction Log rằng file cũ đã hết hiệu lực từ phiên bản này.
  - id: KP9_3
    content: Cơ chế dựng lại trạng thái bảng (State Reconstruction) tại phiên bản mong muốn
    keypoint_weight: 0.2
    description: Khi người dùng gọi truy vấn Time Travel (ví dụ trỏ về Version 5), Spark Engine sẽ đọc Transaction Log từ đầu đến Version 5 để dựng lại danh sách các file Parquet vật lý thực sự có hiệu lực tại thời điểm đó và chỉ đọc đúng các file này để trả về kết quả.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong xử lý dữ liệu luồng (Streaming), hãy phân biệt sự khác biệt logic giữa ba khái niệm thời gian: Event Time (Thời gian xảy ra sự kiện), Ingestion Time (Thời gian nạp dữ liệu), và Processing Time (Thời gian hệ thống xử lý). Cơ chế "Watermark" được sử dụng để giải quyết bài toán gì khi dữ liệu bị đến trễ (Late Data)?
* **expected_key_points:**
  - id: KP10_1
    content: Phân biệt rõ bản chất của ba mốc thời gian trong vòng đời dữ liệu
    keypoint_weight: 0.4
    description: - Event Time: Thời điểm sự kiện thực sự xảy ra ở thiết bị nguồn (được ghi nhận trong payload dữ liệu). - Ingestion Time: Thời điểm sự kiện được nạp vào hệ thống tiếp nhận (như Kafka topic). - Processing Time: Thời điểm sự kiện được luồng tính toán (như Spark/Flink) thực thi xử lý trực tiếp trên RAM.
  - id: KP10_2
    content: Bản chất và mục đích của cơ chế Watermark
    keypoint_weight: 0.3
    description: Watermark là một thước đo thời gian logic di chuyển tịnh tiến đại diện cho tiến trình của Event Time. Nó cho hệ thống biết rằng "chúng ta giả định sẽ không còn dữ liệu nào có Event Time cũ hơn mốc T này xuất hiện nữa", dùng để quản lý cửa sổ thời gian (Windowing).
  - id: KP10_3
    content: Cơ chế xử lý dữ liệu đến trễ và đóng cửa sổ tính toán
    keypoint_weight: 0.3
    description: Watermark cho phép hệ thống duy trì cửa sổ tính toán mở thêm một khoảng thời gian chờ cố định để gom các dữ liệu bị trễ do nghẽn mạng. Khi Watermark vượt qua biên của cửa sổ, hệ thống sẽ thực hiện đóng cửa sổ, tính toán kết quả cuối cùng và bỏ qua (hoặc chuyển hướng sang Dead Letter Queue) các dữ liệu đến trễ hơn mốc Watermark này.