# Bộ Câu Hỏi Phỏng Vấn Data Engineer (Level 1)

* **Role:** Data Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong kiến trúc hệ thống dữ liệu phân tán, hãy định nghĩa khái niệm Data Serialization (Tuần tự hóa dữ liệu) và Deserialization (Giải tuần tự hóa dữ liệu). Tại sao kỹ thuật này lại đóng vai trò quan trọng khi các máy chủ trao đổi dữ liệu với nhau?
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa bản chất của Serialization và Deserialization
    keypoint_weight: 0.5
    description: Serialization là quá trình chuyển đổi cấu trúc dữ liệu hoặc trạng thái của một đối tượng trong bộ nhớ RAM thành một định dạng byte (chuỗi nhị phân hoặc văn bản) để có thể lưu trữ hoặc truyền tải. Deserialization là quá trình ngược lại, tái dựng định dạng byte đó thành đối tượng có cấu trúc nguyên bản trong bộ nhớ.
  - id: KP1_2
    content: Tầm quan trọng của kỹ thuật trong truyền tải mạng và lưu trữ phân tán
    keypoint_weight: 0.5
    description: Giúp tối ưu hóa băng thông đường truyền mạng (Network bandwidth) và không gian đĩa cứng khi truyền tải dữ liệu giữa các Worker Nodes trong hệ thống phân tán, đồng thời đảm bảo tính độc lập về ngôn ngữ lập trình giữa các hệ thống giao tiếp.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt điểm khác biệt cốt lõi về khả năng mở rộng (Scalability) và tính nhất quán dữ liệu (Data Consistency) giữa Cơ sở dữ liệu quan hệ (SQL) và Cơ sở dữ liệu phi quan hệ (NoSQL).
* **expected_key_points:**
  - id: KP2_1
    content: So sánh về cơ chế mở rộng hệ thống (Vertical vs Horizontal Scalability)
    keypoint_weight: 0.5
    description: CSDL SQL truyền thống tối ưu cho việc mở rộng theo chiều dọc (Vertical Scaling - tăng RAM/CPU của một máy chủ). CSDL NoSQL được thiết kế từ đầu để dễ dàng mở rộng theo chiều ngang (Horizontal Scaling - bổ sung thêm nhiều máy chủ giá rẻ vào cụm cluster) nhờ cấu trúc phi tập trung.
  - id: KP2_2
    content: So sánh về tính nhất quán dữ liệu (ACID vs BASE)
    keypoint_weight: 0.5
    description: CSDL SQL tuân thủ nghiêm ngặt tính chất ACID, đảm bảo dữ liệu nhất quán ngay lập tức sau mỗi giao dịch. CSDL NoSQL thường tuân theo mô hình BASE, chấp nhận tính nhất quán muộn (Eventual Consistency) để đổi lấy hiệu năng ghi và tính sẵn sàng cao.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong một Data Pipeline chuyên nghiệp, hoạt động Kiểm định chất lượng dữ liệu (Data Quality Testing) là gì? Tại sao chúng ta không nên bỏ qua bước này trước khi nạp dữ liệu vào Data Warehouse?
* **expected_key_points:**
  - id: KP3_1
    content: Định nghĩa hoạt động Data Quality Testing
    keypoint_weight: 0.5
    description: Là quá trình thiết lập các quy tắc kiểm tra tự động (Data validation rules) để rà soát tính chính xác, tính đầy đủ, tính nhất quán và tính hợp lệ của dữ liệu đầu vào (ví dụ kiểm tra giá trị NULL, kiểm tra định dạng email, kiểm tra miền giá trị hợp lệ).
  - id: KP3_2
    content: Vai trò ngăn ngừa ô nhiễm dữ liệu hệ thống đích (Garbage In Garbage Out)
    keypoint_weight: 0.5
    description: Ngăn chặn dữ liệu lỗi, dữ liệu rác từ nguồn xâm nhập vào Data Warehouse, tránh làm hỏng các báo cáo BI, dashboard hoặc làm sai lệch các mô hình học máy (Machine Learning) ở tầng hạ nguồn.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi thiết kế kho dữ liệu (Data Warehouse) theo mô hình Dimensional Modeling, hãy phân biệt điểm khác biệt về cấu trúc tổ chức dữ liệu và hiệu năng truy vấn giữa Star Schema (Sơ đồ hình sao) và Snowflake Schema (Sơ đồ bông tuyết).
* **expected_key_points:**
  - id: KP4_1
    content: Khác biệt về cấu trúc chuẩn hóa của bảng chiều (Dimension Tables)
    keypoint_weight: 0.4
    description: Trong Star Schema, các bảng Dimension được giữ ở trạng thái phi chuẩn hóa (Denormalized), dữ liệu lưu trữ dư thừa trong một bảng duy nhất. Trong Snowflake Schema, các bảng Dimension được chuẩn hóa (Normalized) thành nhiều bảng nhỏ hơn có mối quan hệ cha-con nhằm giảm dư thừa dữ liệu.
  - id: KP4_2
    content: Khác biệt về hiệu năng truy vấn đọc dữ liệu (JOIN Operations)
    keypoint_weight: 0.3
    description: Star Schema cho hiệu năng truy vấn nhanh hơn vì Database Engine thực hiện ít phép toán JOIN hơn (chỉ cần JOIN trực tiếp giữa Fact và các Dimension). Snowflake Schema yêu cầu thực hiện nhiều phép toán JOIN bắc cầu giữa các bảng chiều chuẩn hóa, làm giảm tốc độ truy vấn.
  - id: KP4_3
    content: Khác biệt về khả năng bảo trì và không gian lưu trữ
    keypoint_weight: 0.3
    description: Snowflake Schema tiết kiệm không gian đĩa cứng hơn và dễ bảo trì tính toàn vẹn dữ liệu hơn nhờ cấu trúc chuẩn hóa, phù hợp với các hệ thống có bảng chiều kích thước cực kỳ lớn.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong Apache Spark, hãy giải thích sự khác biệt về mặt quản lý bộ nhớ và cơ chế hoạt động giữa hai phương thức tối ưu hóa: `.cache()` và `.persist()`. Khi nào chúng ta nên sử dụng chúng?
* **expected_key_points:**
  - id: KP5_1
    content: Bản chất mặc định của phương thức cache()
    keypoint_weight: 0.5
    description: Phương thức `.cache()` là một trường hợp đặc biệt của `.persist()`, nó tự động lưu trữ dữ liệu DataFrame/RDD vào bộ nhớ RAM với mức độ lưu trữ mặc định là MEMORY_AND_DISK (hoặc MEMORY_ONLY đối với RDD).
  - id: KP5_2
    content: Khả năng tùy biến mức độ lưu trữ của phương thức persist()
    keypoint_weight: 0.5
    description: Phương thức `.persist()` cho phép lập trình viên chủ động lựa chọn và cấu hình nhiều mức độ lưu trữ khác nhau (Storage Levels) tùy thuộc vào tài nguyên hệ thống, bao gồm lưu trữ thuần trên RAM, lưu trữ thuần trên Đĩa, lưu trữ kết hợp cả hai, hoặc nhân bản dữ liệu sang nhiều node để chịu lỗi (ví dụ: MEMORY_ONLY_SER, DISK_ONLY_2).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong kiến trúc hệ thống cơ sở dữ liệu quy mô lớn, hãy phân biệt sự khác biệt về mặt vật lý và phạm vi áp dụng giữa hai kỹ thuật: Partitioning (Phân vùng) và Sharding (Phân mảnh).
* **expected_key_points:**
  - id: KP6_1
    content: Bản chất phân chia dữ liệu nội bộ của Partitioning
    keypoint_weight: 0.5
    description: Partitioning là việc chia nhỏ một bảng dữ liệu lớn thành các phần vật lý độc lập (Partitions) nhưng toàn bộ các phần này vẫn nằm chung trên một máy chủ (Single database instance). Hệ thống quản lý chung một schema và phân vùng dựa trên một cột khóa (ví dụ: chia theo tháng).
  - id: KP6_2
    content: Bản chất phân mảnh dữ liệu đa máy chủ của Sharding
    keypoint_weight: 0.5
    description: Sharding là kỹ thuật chia nhỏ dữ liệu của một bảng và phân phối chúng ra nhiều máy chủ vật lý độc lập khác nhau (mỗi máy chủ gọi là một Shard). Mỗi Shard là một cơ sở dữ liệu hoàn chỉnh riêng biệt, giúp giải quyết triệt để giới hạn phần cứng của một máy đơn lẻ.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi xây dựng kiến trúc Data Ingestion (Thu thập dữ liệu), hãy phân biệt điểm khác nhau về cơ chế kích hoạt và truyền tải thông tin giữa mô hình Pull-based (Kéo dữ liệu) và Push-based (Đẩy dữ liệu). Nêu ví dụ thực tế cho mỗi loại.
* **expected_key_points:**
  - id: KP7_1
    content: Cơ chế hoạt động và ví dụ của Pull-based Ingestion
    keypoint_weight: 0.5
    description: Hệ thống thu thập dữ liệu (Consumer/Collector) chủ động gửi yêu cầu định kỳ đến hệ thống nguồn để quét và kéo dữ liệu mới về. Giúp hệ thống đích tự kiểm soát được tải xử lý của mình. Ví dụ: Viết script gọi API REST của Salesforce hằng giờ, hoặc Logstash quét file log định kỳ.
  - id: KP7_2
    content: Cơ chế hoạt động và ví dụ của Push-based Ingestion
    keypoint_weight: 0.5
    description: Hệ thống nguồn (Producer) chủ động đẩy dữ liệu sang hệ thống đích ngay khi có sự kiện mới phát sinh. Giúp truyền tải thông tin cực nhanh nhưng hệ thống đích phải có cơ chế chịu tải tốt khi lượng dữ liệu tăng đột biến. Ví dụ: Webhook thông báo sự kiện thanh toán, hoặc thiết bị IoT gửi dữ liệu cảm biến trực tiếp lên API Gateway.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Hãy trình bày nội dung của định lý CAP trong hệ thống phân tán. Tại sao một Data Engineer bắt buộc phải đánh đổi giữa tính nhất quán (Consistency) và tính sẵn sàng (Availability) khi xảy ra sự cố phân tách mạng (Network Partition)?
* **expected_key_points:**
  - id: KP8_1
    content: Định nghĩa ba yếu tố cốt lõi của định lý CAP
    keypoint_weight: 0.4
    description: Định lý CAP phát biểu rằng một hệ thống dữ liệu phân tán chỉ có thể đáp ứng tối đa hai trong ba yếu tố: Consistency (Tính nhất quán - mọi node đều đọc ra dữ liệu giống nhau cùng lúc), Availability (Tính sẵn sàng - mọi request không lỗi đều nhận được phản hồi), và Partition Tolerance (Khả năng chịu sự phân tách mạng).
  - id: KP8_2
    content: Sự bắt buộc của yếu tố Partition Tolerance (P) trong thực tế mạng vật lý
    keypoint_weight: 0.3
    description: Trong mạng vật lý thực tế, sự cố mất kết nối giữa các node (Network Partition) chắc chắn sẽ xảy ra vào một thời điểm nào đó. Do đó, hệ thống bắt buộc phải hỗ trợ Partition Tolerance (chọn P), nghĩa là bài toán thực tế là phải chọn lựa giữa CP hoặc AP.
  - id: KP8_3
    content: Bản chất đánh đổi giữa tính nhất quán (CP) và tính sẵn sàng (AP)
    keypoint_weight: 0.3
    description: Nếu chọn CP (Consistency): Khi mất kết nối, hệ thống từ chối phản hồi ghi/đọc ở các node bị cô lập để tránh sai lệch dữ liệu, làm giảm tính sẵn sàng. Nếu chọn AP (Availability): Hệ thống vẫn chấp nhận cho các node hoạt động độc lập phản hồi khách hàng, dẫn đến việc dữ liệu giữa các node không đồng nhất tại thời điểm đó.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong thiết kế kho dữ liệu, Slowly Changing Dimension (SCD) Type 1 và Type 2 rất phổ biến. Tuy nhiên, hãy giải thích cơ chế hoạt động và mục đích sử dụng nâng cao của kỹ thuật SCD Type 3 và SCD Type 4.
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế lưu trữ lịch sử giới hạn bằng thêm cột của SCD Type 3
    keypoint_weight: 0.4
    description: SCD Type 3 lưu trữ lịch sử thay đổi bằng cách thêm các cột mới vào chính dòng hiện tại (ví dụ thêm cột `Previous_Address` bên cạnh cột `Current_Address`). Kỹ thuật này chỉ lưu vết được một số lượng phiên bản giới hạn (thường là phiên bản gần nhất) nhưng giúp truy vấn so sánh trực tiếp hai trạng thái rất nhanh.
  - id: KP9_2
    content: Cơ chế tách biệt bảng lịch sử độc lập của SCD Type 4
    keypoint_weight: 0.4
    description: SCD Type 4 giữ bảng Dimension chính hoàn toàn sạch sẽ (chỉ ghi đè giá trị hiện tại như Type 1) và chuyển toàn bộ lịch sử biến động dữ liệu sang một bảng phụ chuyên biệt gọi là History Table (bảng lịch sử).
  - id: KP9_3
    content: Mục đích tối ưu hóa hiệu năng truy vấn của SCD Type 4 đối với dữ liệu lớn
    keypoint_weight: 0.2
    description: Giúp bảng Dimension chính duy trì kích thước nhỏ gọn để tối ưu hóa hiệu năng cho các câu lệnh JOIN phân tích hằng ngày, trong khi vẫn bảo toàn lịch sử biến động chi tiết phục vụ cho các báo cáo kiểm toán chuyên sâu khi cần thiết.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích sự khác biệt về mặt triết lý thiết kế hệ thống, cơ chế xử lý lỗi cấu trúc và tính linh hoạt giữa hai mô hình kiểm soát cấu trúc dữ liệu: Schema-on-Write (Áp cấu trúc khi ghi) và Schema-on-Read (Áp cấu trúc khi đọc).
* **expected_key_points:**
  - id: KP10_1
    content: Bản chất kiểm soát chặt chẽ của Schema-on-Write
    keypoint_weight: 0.4
    description: Schema-on-Write yêu cầu cấu trúc bảng (Schema) phải được định nghĩa trước khi nạp dữ liệu (như cơ sở dữ liệu quan hệ RDBMS). Khi ghi, hệ thống tự động kiểm tra, nếu dữ liệu không khớp schema sẽ bị từ chối trực tiếp, đảm bảo chất lượng dữ liệu sạch tuyệt đối ở đích nhưng làm giảm tốc độ nạp dữ liệu thô.
  - id: KP10_2
    content: Bản chất nạp nhanh linh hoạt của Schema-on-Read
    keypoint_weight: 0.4
    description: Schema-on-Read cho phép nạp trực tiếp mọi dữ liệu thô, bán cấu trúc vào hệ thống lưu trữ (như Hadoop HDFS, Cloud Object Storage) mà không cần kiểm tra cấu trúc lúc ghi. Cấu trúc dữ liệu chỉ được áp đặt và phân tích khi người dùng thực hiện câu lệnh đọc dữ liệu (ví dụ truy vấn bằng Hive/Spark SQL), tối ưu cho tốc độ nạp và tính linh hoạt cao.
  - id: KP10_3
    content: Khả năng xử lý sự tiến hóa của cấu trúc dữ liệu (Schema Evolution)
    keypoint_weight: 0.2
    description: Schema-on-Read hỗ trợ cực tốt cho sự thay đổi cấu trúc dữ liệu theo thời gian (Schema Evolution) vì hệ thống không bị ràng buộc bởi các DDL cứng nhắc, cho phép lưu trữ nhiều phiên bản dữ liệu khác nhau mà không cần cấu trúc lại bảng vật lý.