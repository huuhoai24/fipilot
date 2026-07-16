# Bộ Câu Hỏi Phỏng Vấn Data Engineer (Level 1)

* **Role:** Data Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong quản trị và vận hành hệ thống dữ liệu lớn, khái niệm Data Lineage (Truy vết nguồn gốc dữ liệu) là gì? Tại sao việc xây dựng sơ đồ Data Lineage lại cực kỳ quan trọng khi xảy ra lỗi dữ liệu ở các báo cáo cuối cùng (Hạ nguồn - Downstream)?
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa bản chất của Data Lineage
    keypoint_weight: 0.5
    description: Data Lineage là bản đồ ghi nhận chi tiết vòng đời của dữ liệu, mô tả rõ ràng nguồn gốc xuất phát của dữ liệu (Data Origin), các bước biến đổi (Transformations) và đường đi di chuyển của dữ liệu qua các hệ thống cho đến điểm đích cuối cùng.
  - id: KP1_2
    content: Vai trò phân tích nguyên nhân gốc rễ (Root Cause Analysis) khi xảy ra lỗi
    keypoint_weight: 0.5
    description: Khi một chỉ số trên báo cáo bị sai lệch, sơ đồ Data Lineage giúp kỹ sư dữ liệu lập tức truy vết ngược dòng (Upstream tracking) để khoanh vùng chính xác lỗi bắt nguồn từ hệ thống nguồn nào hay do công thức biến đổi nào ở bước trung gian, giúp giảm tối đa thời gian sửa lỗi (Debugging time).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế cơ sở dữ liệu phân tán NoSQL, các hệ thống thường tuân theo triết lý thiết kế BASE thay vì ACID. Hãy giải thích ý nghĩa của các chữ cái cấu thành nên thuật ngữ BASE (Basically Available, Soft State, Eventual Consistency).
* **expected_key_points:**
  - id: KP2_1
    content: Ý nghĩa của Basically Available (Sẵn sàng ở mức cơ bản)
    keypoint_weight: 0.3
    description: Đảm bảo hệ thống luôn phản hồi các truy vấn của người dùng kể cả khi có một vài node bị sập, tuy nhiên phản hồi đó có thể không chứa dữ liệu mới nhất hoặc chỉ trả về một phần dữ liệu không bị ảnh hưởng.
  - id: KP2_2
    content: Ý nghĩa của Soft State (Trạng thái mềm/linh hoạt)
    keypoint_weight: 0.3
    description: Trạng thái của dữ liệu có thể tự động thay đổi theo thời gian mà không cần tác vụ ghi của người dùng, do cơ chế tự động đồng bộ phi đồng bộ chạy ngầm giữa các node phân tán.
  - id: KP2_3
    content: Ý nghĩa của Eventual Consistency (Nhất quán muộn) và mối liên kết tổng thể
    keypoint_weight: 0.4
    description: Hệ thống cam kết dữ liệu giữa các node sẽ tự động đồng bộ nhất quán hoàn toàn sau một khoảng thời gian trễ nhất định, miễn là không có thêm cập nhật mới nào được ghi nhận.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt sự khác biệt cơ bản về mặt tổ chức lưu trữ vật lý trên đĩa cứng và hiệu năng truy vấn giữa hai kỹ thuật tối ưu hóa trong cơ sở dữ liệu quan hệ (RDBMS): Table Partitioning (Phân vùng bảng) và Table Indexing (Tạo chỉ mục bảng).
* **expected_key_points:**
  - id: KP3_1
    content: Bản chất vật lý và hiệu năng của Table Partitioning
    keypoint_weight: 0.5
    description: Phân vùng bảng thực hiện chia cắt một bảng dữ liệu lớn thành các tệp tin/thư mục vật lý độc lập hoàn toàn dựa trên giá trị của một cột phân vùng. Khi truy vấn lọc theo cột này, hệ thống chỉ đọc đúng tệp tin của phân vùng đó (Partition Pruning), giúp tối ưu hóa I/O đĩa cứng khi truy vấn lượng dữ liệu cực lớn.
  - id: KP3_2
    content: Bản chất vật lý và hiệu năng của Table Indexing
    keypoint_weight: 0.5
    description: Tạo chỉ mục là việc xây dựng một cấu trúc dữ liệu phụ trợ (như cây B-Tree) chứa các cặp giá trị khóa chỉ mục và con trỏ vật lý trỏ tới vị trí dòng dữ liệu trong bảng chính. Nó không chia tách bảng vật lý mà giúp tăng tốc các truy vấn tìm kiếm ngẫu nhiên hoặc truy xuất một vài bản ghi cụ thể.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong thiết kế kho dữ liệu (Data Warehouse) theo mô hình Dimensional Modeling, Slowly Changing Dimension (SCD) Type 6 (hay còn gọi là Hybrid SCD / Type 1 + 2 + 3) hoạt động ra sao và nó đem lại khả năng phân tích nâng cao nào cho doanh nghiệp?
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế hoạt động kết hợp cấu trúc của SCD Type 6
    keypoint_weight: 0.4
    description: SCD Type 6 kết hợp đồng thời cơ chế của Type 1 (ghi đè), Type 2 (thêm dòng mới lưu lịch sử) và Type 3 (thêm cột mới). Một dòng dữ liệu trong bảng chiều sẽ chứa cả cột giá trị lịch sử (như Historical_Region) và cột giá trị hiện tại (như Current_Region). Khi có thay đổi, hệ thống tạo dòng mới (Type 2) đồng thời cập nhật giá trị hiện tại ở tất cả các dòng cũ của thực thể đó (Type 1).
  - id: KP4_2
    content: Khả năng phân tích báo cáo theo trạng thái lịch sử thực tế
    keypoint_weight: 0.3
    description: Cho phép doanh nghiệp chạy các báo cáo phân tích doanh thu chính xác tại thời điểm giao dịch phát sinh trong quá khứ dựa trên cột giá trị lịch sử (ví dụ: khách hàng thuộc chi nhánh miền Nam lúc mua hàng).
  - id: KP4_3
    content: Khả năng phân tích báo cáo quy đổi theo trạng thái hiện tại
    keypoint_weight: 0.3
    description: Cho phép doanh nghiệp dễ dàng chạy báo cáo quy đổi toàn bộ doanh thu lịch sử của khách hàng về chi nhánh quản lý hiện tại của họ (ví dụ: khách hàng đã chuyển ra miền Bắc, muốn xem tổng doanh thu lịch sử quy về miền Bắc).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong các hệ thống tính toán dữ liệu lớn (như Hive hoặc Apache Spark), hãy phân biệt cơ chế hoạt động giữa Static Partition Insert (Nạp phân vùng tĩnh) và Dynamic Partition Insert (Nạp phân vùng động). Sử dụng Dynamic Partition Insert có rủi ro kỹ thuật gì cho hệ thống lưu trữ đĩa cứng?
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế nạp phân vùng tĩnh (Static Partition)
    keypoint_weight: 0.3
    description: Lập trình viên phải chỉ định cứng tên và giá trị của phân vùng cụ thể trong câu lệnh SQL (ví dụ: PARTITION (year=2026, month=07)). Hệ thống nạp trực tiếp dữ liệu vào thư mục đó mà không cần tính toán phân tích runtime, an toàn nhưng thiếu linh hoạt.
  - id: KP5_2
    content: Cơ chế nạp phân vùng động (Dynamic Partition)
    keypoint_weight: 0.3
    description: Hệ thống tự động phân tích dữ liệu ở runtime, dựa vào giá trị của cột được chọn ở câu lệnh SELECT để tự động tạo và phân phối dữ liệu vào các thư mục phân vùng tương ứng một cách linh hoạt.
  - id: KP5_3
    content: Rủi ro kỹ thuật tạo quá nhiều file nhỏ và sập bộ nhớ metadata
    keypoint_weight: 0.4
    description: Nếu cột phân vùng động có độ đa dạng giá trị quá cao (High cardinality, ví dụ phân vùng theo user_id or timestamp), Spark/Hive sẽ tạo ra hàng triệu thư mục và tệp tin vật lý cực nhỏ ở runtime. Việc này gây ra lỗi "Small Files Problem", làm cạn kiệt bộ nhớ RAM của NameNode (HDFS) hoặc làm sập tác vụ do quá giới hạn file cho phép ghi của hệ thống.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi xây dựng Event-driven Data Ingestion Pipeline (Pipeline thu thập dữ liệu theo sự kiện) trên Cloud, hãy giải thích nguyên lý hoạt động của cơ chế sử dụng Object Storage Event Notifications (như AWS S3 Event Notifications kết hợp với SQS/Lambda).
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế tự động phát sinh sự kiện khi nạp file (Object Creation Event)
    keypoint_weight: 0.4
    description: Ngay khi một tệp dữ liệu mới được tải lên (PUT/POST object) một thư mục chỉ định trên Cloud Object Storage, hệ thống lưu trữ tự động kích hoạt một sự kiện chứa các thông tin metadata của file (tên file, đường dẫn, kích thước).
  - id: KP6_2
    content: Vai trò làm hàng đợi đệm của dịch vụ tin nhắn (như SQS)
    keypoint_weight: 0.3
    description: Sự kiện phát sinh được đẩy trực tiếp vào một hàng đợi tin nhắn (như SQS) để làm bộ đệm trung gian phi đồng bộ, đảm bảo các sự kiện không bị mất mát kể cả khi hệ thống xử lý phía sau gặp sự cố tạm thời.
  - id: KP6_3
    content: Cơ chế kích hoạt hàm xử lý tự động (như Lambda/Spark)
    keypoint_weight: 0.3
    description: Hàm xử lý phi máy chủ (như Lambda) hoặc ứng dụng tiêu thụ chủ động kéo tin nhắn từ hàng đợi, giải mã metadata để lấy đường dẫn file vật lý và thực hiện tính toán ETL nạp vào kho dữ liệu ngay lập tức, đạt độ trễ cực thấp.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong thiết kế Data Pipeline xử lý lỗi dữ liệu, khái niệm Dead Letter Queue (DLQ) là gì? Khi một bản ghi dữ liệu (Data Record) bị lỗi cấu trúc hoặc vi phạm ràng buộc ở bước Transform, cơ chế DLQ xử lý bản ghi đó ra sao để đảm bảo pipeline không bị sập giữa chừng?
* **expected_key_points:**
  - id: KP7_1
    content: Định nghĩa bản chất của Dead Letter Queue (DLQ)
    keypoint_weight: 0.4
    description: DLQ là một hàng đợi hoặc một thư mục lưu trữ chuyên biệt dùng để cách ly các thông điệp hoặc bản ghi dữ liệu bị lỗi, không thể xử lý thành công sau nhiều lần thử lại trong Data Pipeline.
  - id: KP7_2
    content: Cơ chế trích xuất và cách ly bản ghi lỗi (Error Isolation)
    keypoint_weight: 0.4
    description: Khi phát hiện bản ghi bị lỗi (như sai định dạng JSON, lỗi kiểu dữ liệu), thay vì để hệ thống crash sập nguồn hoặc bỏ qua âm thầm, pipeline sẽ bắt lỗi (Try-catch), đóng gói bản ghi lỗi kèm thông tin chi tiết về nguyên nhân gây lỗi (Error stacktrace) và đẩy sang DLQ.
  - id: KP7_3
    content: Bảo toàn tính liên tục của luồng chạy và hỗ trợ khắc phục thủ công
    keypoint_weight: 0.2
    description: Giúp pipeline tiếp tục xử lý các bản ghi hợp lệ tiếp theo mà không bị gián đoạn. Đội ngũ vận hành có thể giám sát DLQ, phân tích lỗi, sửa chữa bản ghi lỗi và nạp lại (Re-drive) vào pipeline sau khi đã khắc phục.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong Apache Spark SQL, công cụ tối ưu hóa Catalyst Optimizer thực hiện nhiệm vụ gì? Hãy giải thích bốn giai đoạn logic mà Catalyst Optimizer trải qua để chuyển đổi một câu lệnh SQL của người dùng thành mã byte thực thi vật lý tối ưu (Physical Plan).
* **expected_key_points:**
  - id: KP8_1
    content: Giai đoạn Phân tích cú pháp và liên kết lược đồ (Analysis & Catalog)
    keypoint_weight: 0.3
    description: Catalyst nhận câu lệnh SQL/DataFrame và xây dựng cây cú pháp trừu tượng chưa được giải quyết (Unresolved Logical Plan). Sau đó, nó đối chiếu các tên bảng, tên cột với thư viện Catalog (Metadata store) để xác thực tính hợp lệ và chuyển đổi thành Resolved Logical Plan.
  - id: KP8_2
    content: Giai đoạn Tối ưu hóa logic dựa trên tập quy tắc (Logical Optimization)
    keypoint_weight: 0.3
    description: Áp dụng các quy tắc tối ưu hóa toán học chuẩn (Rule-based optimization) để tinh gọn cây kế hoạch logic, bao gồm việc đẩy bộ lọc xuống gần nguồn dữ liệu nhất (Predicate Pushdown), chỉ đọc các cột cần thiết (Projection Pruning) và rút gọn các phép toán hằng số.
  - id: KP8_3
    content: Giai đoạn Lập kế hoạch vật lý dựa trên chi phí (Physical Planning & Cost Model)
    keypoint_weight: 0.2
    description: Catalyst sinh ra nhiều kế hoạch thực thi vật lý khác nhau dựa trên các thuật toán thực tế (như chọn Broadcast Join hay SortMergeJoin). Sau đó, nó sử dụng mô hình chi phí (Cost-based Model) ước tính tài nguyên để chọn ra một Physical Plan tối ưu nhất.
  - id: KP8_4
    content: Giai đoạn Tự động sinh mã byte tối ưu hóa (Code Generation - Janino)
    keypoint_weight: 0.2
    description: Spark sử dụng trình biên dịch Janino chạy ngầm để biên dịch Physical Plan đã chọn trực tiếp thành mã byte Java (Java bytecode) tối ưu, loại bỏ các vòng lặp ảo và tối đa hóa tốc độ thực thi của CPU.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong thiết kế cơ sở dữ liệu phân tán quy mô lớn (Distributed NoSQL), thuật toán Consistent Hashing (Băm nhất quán) giải quyết bài toán gì? Khi hệ thống thực hiện thêm một Node vật lý mới hoặc bớt một Node cũ, thuật toán này giúp tối ưu hóa tiến trình di chuyển dữ liệu (Data Re-sharding) như thế nào?
* **expected_key_points:**
  - id: KP9_1
    content: Nguyên lý ánh xạ khóa lên vòng tròn băm logic (Hash Ring)
    keypoint_weight: 0.4
    description: Consistent Hashing ánh xạ cả các Node vật lý và các khóa dữ liệu (Keys) lên cùng một không gian dải giá trị băm tròn khép kín (vòng tròn logic từ 0 đến 2^32-1). Khóa dữ liệu sẽ được lưu trữ tại Node đầu tiên xuất hiện khi di chuyển theo chiều kim đồng hồ từ vị trí của khóa đó trên vòng tròn.
  - id: KP9_2
    content: Tối ưu hóa dung lượng dữ liệu cần di chuyển khi thay đổi quy mô (Scale out/in)
    keypoint_weight: 0.4
    description: Khi thêm hoặc bớt một Node, hệ thống không cần phải phân vùng lại toàn bộ dữ liệu (re-hash toàn cục làm nghẽn mạng). Consistent Hashing đảm bảo chỉ có một tỷ lệ nhỏ dữ liệu nằm ở các phân vùng liền kề trực tiếp với Node bị thay đổi là cần phải di chuyển qua mạng sang Node mới, phần lớn dữ liệu trên các Node còn lại giữ nguyên vị trí vật lý.
  - id: KP9_3
    content: Giải quyết bài toán mất cân bằng tải trọng qua cơ chế Node ảo (Virtual Nodes)
    keypoint_weight: 0.2
    description: Áp dụng cơ chế Node ảo (Vnodes) bằng cách ánh xạ một Node vật lý thành nhiều điểm đại diện ngẫu nhiên trên vòng tròn băm, giúp phân bổ đều dữ liệu và chia sẻ tải trọng ghi đều khắp cụm cluster, tránh hiện tượng lệch tải (Hotspots).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Khi xây dựng hệ thống xử lý dữ liệu lớn, hãy so sánh sự khác biệt cốt lõi về mặt triết lý thiết kế và lưu trữ dữ liệu giữa Kappa Architecture và Lambda Architecture. Trong Kappa Architecture, làm thế nào hệ thống thực hiện xử lý lại toàn bộ dữ liệu lịch sử (Data Replay) khi logic nghiệp vụ thay đổi?
* **expected_key_points:**
  - id: KP10_1
    content: Triết lý tối giản hóa một luồng xử lý duy nhất của Kappa Architecture
    keypoint_weight: 0.4
    description: Kappa Architecture loại bỏ hoàn toàn tầng Batch Layer của Lambda, chỉ duy trì một luồng xử lý thời gian thực duy nhất (Stream-only layer). Mọi dữ liệu (bao gồm cả dữ liệu lịch sử và dữ liệu mới) đều được coi là một dòng chảy liên tục và được xử lý chung bởi một công cụ xử lý luồng (như Spark Streaming, Flink).
  - id: KP10_2
    content: Cơ chế lưu trữ nhật ký sự kiện bất biến dài hạn (Event Log Store)
    keypoint_weight: 0.3
    description: Đòi hỏi hệ thống hàng đợi ở đầu vào phải lưu trữ và bảo toàn toàn bộ lịch sử dữ liệu thô bất biến một cách dài hạn (như Kafka commit log với retention policy dài hạn) để làm nguồn chân lý duy nhất phục vụ cho việc đọc lại khi cần thiết.
  - id: KP10_3
    content: Quy trình xử lý lại dữ liệu lịch sử qua cơ chế Data Replay phi ảnh hưởng
    keypoint_weight: 0.3
    description: Khi logic tính toán thay đổi, Data Engineer sẽ dựng một instance của ứng dụng streaming mới chạy song song, cấu hình con trỏ đọc (Offset) quay trở lại thời điểm 0 của Kafka để kéo và tính toán lại toàn bộ dữ liệu lịch sử. Sau khi ứng dụng mới đã đuổi kịp thời gian thực (Caught up), hệ thống sẽ chuyển hướng tầng hiển thị (Serving layer) sang ứng dụng mới và tắt ứng dụng cũ đi.