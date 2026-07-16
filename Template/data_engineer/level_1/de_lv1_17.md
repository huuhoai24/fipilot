# Bộ Câu Hỏi Phỏng Vấn Data Engineer (Level 1)

* **Role:** Data Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong các hệ thống lưu trữ dữ liệu lớn (như Apache Cassandra hoặc RocksDB), cấu trúc dữ liệu Bloom Filter là gì và nó giúp tối ưu hóa hiệu năng đọc dữ liệu từ đĩa vật lý dựa trên cơ chế nào?
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa bản chất của Bloom Filter
    keypoint_weight: 0.5
    description: Bloom Filter là một cấu trúc dữ liệu xác suất (Probabilistic data structure) cực kỳ tiết kiệm bộ nhớ, dùng để kiểm tra nhanh xem một phần tử có tồn tại trong một tập hợp hay không. Nó có thể trả về kết quả khẳng định chắc chắn "Không tồn tại" hoặc kết quả mang tính xác suất "Có thể tồn tại" (chấp nhận tỷ lệ False Positive nhỏ).
  - id: KP1_2
    content: Cơ chế tối ưu hóa tốc độ đọc đĩa (Disk I/O reduction)
    keypoint_weight: 0.5
    description: Thay vì phải truy cập trực tiếp vào đĩa cứng để quét các file dữ liệu (SSTables) vốn tốn rất nhiều tài nguyên, hệ thống kiểm tra nhanh Bloom Filter trên RAM trước. Nếu Bloom Filter báo "Không tồn tại", hệ thống lập tức bỏ qua file đó mà không cần đọc đĩa, giúp tiết kiệm tối đa tài nguyên I/O đĩa cứng.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Khi thiết kế các tác vụ xử lý dữ liệu (Data Processing Jobs), hãy phân biệt sự khác biệt cơ bản về mặt lưu trữ bộ nhớ và logic xử lý giữa Stateless Processing (Xử lý phi trạng thái) và Stateful Processing (Xử lý có trạng thái).
* **expected_key_points:**
  - id: KP2_1
    content: Bản chất và cơ chế hoạt động của Stateless Processing
    keypoint_weight: 0.5
    description: Xử lý phi trạng thái nghĩa là việc tính toán trên một bản ghi dữ liệu hiện tại hoàn toàn độc lập và không phụ thuộc vào bất kỳ bản ghi nào khác đã được xử lý trước đó. Hệ thống không cần duy trì bộ đệm bộ nhớ cho trạng thái lịch sử. Ví dụ: Chuyển đổi định dạng ngày tháng, lọc bỏ các dòng có giá trị NULL.
  - id: KP2_2
    content: Bản chất và cơ chế hoạt động của Stateful Processing
    keypoint_weight: 0.5
    description: Xử lý có trạng thái yêu cầu hệ thống phải lưu giữ và cập nhật thông tin trung gian (State) từ các bản ghi trước đó trong bộ nhớ RAM để tính toán ra kết quả cho bản ghi hiện tại. Ví dụ: Tính toán tổng giá trị đơn hàng tích lũy của khách hàng trong ngày, hoặc tính trung bình động trong một cửa sổ thời gian (Windowing).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong kiến trúc luồng dữ liệu thời gian thực, hãy phân biệt sự khác biệt cơ bản về cơ chế phân phối thông điệp và cách quản lý trạng thái đọc giữa hàng đợi truyền thống (như RabbitMQ) và hàng đợi dựa trên tệp nhật ký (Log-based Message Broker - như Apache Kafka).
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế của RabbitMQ (AMQP / Message-queue model)
    keypoint_weight: 0.5
    description: RabbitMQ đẩy thông điệp trực tiếp đến Consumer và sẽ xóa thông điệp khỏi hàng đợi ngay khi nhận được phản hồi xác nhận (Acknowledge) từ phía Consumer. Trạng thái đọc (tin nhắn nào đã đọc hay chưa) do chính RabbitMQ quản lý, và thông điệp không thể được đọc lại một khi đã bị xóa.
  - id: KP3_2
    content: Cơ chế của Apache Kafka (Log-based / Commit-log model)
    keypoint_weight: 0.5
    description: Kafka lưu trữ thông điệp dưới dạng một tệp nhật ký ghi thêm (Append-only commit log) bất biến trên đĩa cứng và duy trì chúng trong một khoảng thời gian cấu hình sẵn (Retention policy). Trạng thái đọc do chính Consumer tự quản lý thông qua vị trí con trỏ (Offset), cho phép nhiều Consumer khác nhau cùng đọc một tệp log độc lập hoặc cho phép đọc lại dữ liệu cũ khi cần thiết.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi xây dựng mô hình dữ liệu Dimensional Modeling cho kho dữ liệu (Data Warehouse), kỹ thuật thiết kế bảng "Outrigger Dimension" (Bảng chiều mở rộng) là gì? Nó khác biệt thế nào với mô hình Snowflake Schema thông thường?
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa bản chất của Outrigger Dimension
    keypoint_weight: 0.4
    description: Outrigger Dimension là một bảng chiều phụ được liên kết trực tiếp với một bảng chiều chính khác (thay vì liên kết trực tiếp với bảng Fact), dùng để phân tách bớt các thuộc tính có tính chất phân cấp phức tạp hoặc thay đổi với tần suất khác biệt.
  - id: KP4_2
    content: Sự khác biệt về mặt cấu trúc so với Snowflake Schema
    keypoint_weight: 0.3
    description: Trong Snowflake Schema, toàn bộ các bảng chiều của hệ thống đều bị chuẩn hóa phân cấp diện rộng (gây ra sự phức tạp khi viết truy vấn SQL do phải JOIN bắc cầu nhiều tầng). Trong khi đó, Outrigger chỉ chuẩn hóa cục bộ tại một hoặc hai bảng chiều cụ thể khi cực kỳ cần thiết, phần còn lại của kho dữ liệu vẫn duy trì cấu trúc Star Schema phi chuẩn hóa để tối ưu hiệu năng.
  - id: KP4_3
    content: Mục đích tối ưu hóa dung lượng đĩa và tái sử dụng thông tin
    keypoint_weight: 0.3
    description: Giúp cô lập các nhóm thuộc tính dùng chung lớn (như thông tin địa lý, thông tin tổ chức hành chính) để có thể tái sử dụng dễ dàng ở nhiều bảng chiều khác nhau mà không cần nhân bản thuộc tính, từ đó tiết kiệm dung lượng đĩa cứng và nâng cao tính nhất quán dữ liệu.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong các hệ thống tích hợp dữ liệu thời gian thực, cơ chế truyền thông điệp "At-least-once" (Ít nhất một lần) giải quyết rủi ro gì của hạ tầng mạng vật lý? Sự đánh đổi về tài nguyên hệ thống ở phía đích nhận dữ liệu là gì?
* **expected_key_points:**
  - id: KP5_1
    content: Nguyên lý đảm bảo không mất mát dữ liệu của At-least-once
    keypoint_weight: 0.5
    description: Cơ chế này đảm bảo mọi thông điệp từ nguồn gửi đi chắc chắn sẽ đến được hệ thống đích ít nhất một lần. Nếu hệ thống nguồn không nhận được tín hiệu xác nhận (Acknowledge) từ đích trong một khoảng thời gian chờ (Timeout) do đứt kết nối mạng tạm thời, nó sẽ tự động gửi lại thông điệp đó cho đến khi thành công, loại bỏ hoàn toàn rủi ro mất mát dữ liệu (Data loss).
  - id: KP5_2
    content: Đánh đổi chi phí xử lý trùng lặp ở hệ thống đích (Deduplication cost)
    keypoint_weight: 0.5
    description: Điểm đánh đổi lớn nhất là hệ thống đích sẽ bị nhận trùng lặp dữ liệu (Duplicate messages) khi xảy ra sự cố mạng chập chờn. Để đảm bảo tính toàn vẹn, Data Engineer bắt buộc phải xây dựng thêm một lớp xử lý lọc trùng dữ liệu (Deduplication) dựa trên khóa chính hoặc thiết kế các tác vụ có tính lũy đẳng (Idempotent), gây tốn thêm tài nguyên tính toán CPU/RAM ở đích.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi xây dựng kiến trúc Data Pipeline theo mô hình Event-driven trong hệ thống Microservices, tại sao một "Schema Registry" tập trung (như Confluent Schema Registry) lại là thành phần cốt lõi để đảm bảo hệ thống vận hành an toàn?
* **expected_key_points:**
  - id: KP6_1
    content: Vai trò định nghĩa và đồng bộ cấu trúc dữ liệu tập trung
    keypoint_weight: 0.5
    description: Schema Registry đóng vai trò là một dịch vụ tập trung dùng để lưu trữ và quản lý phiên bản của tất cả các khuôn mẫu cấu trúc dữ liệu (Schemas - ví dụ bằng định dạng Avro, Protobuf). Nó giúp cả hai phía sinh dữ liệu (Producer) và tiêu thụ dữ liệu (Consumer) có một điểm tra cứu duy nhất để giải mã dữ liệu nhị phân truyền qua mạng.
  - id: KP6_2
    content: Kiểm soát và ngăn chặn lỗi phá vỡ dữ liệu (Compatibility validation)
    keypoint_weight: 0.5
    description: Schema Registry tự động kiểm tra tính tương thích của schema khi có sự thay đổi (như thêm cột, xóa cột). Nếu Producer cố tình đẩy dữ liệu có cấu trúc không tương thích (ví dụ: thay đổi kiểu dữ liệu của cột khóa từ Int sang String), hệ thống sẽ từ chối trực tiếp từ đầu, ngăn chặn việc làm crash các ứng dụng xử lý dữ liệu ở hạ nguồn.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong thiết kế cơ sở dữ liệu hướng cột, hãy giải thích nguyên lý hoạt động của kỹ thuật nén dữ liệu từ điển Dictionary Encoding kết hợp với kỹ thuật đóng gói bit (Bit-Packing). Tại sao sự kết hợp này lại đem lại tỷ lệ nén vượt trội cho các trường dữ liệu kiểu chuỗi ký tự?
* **expected_key_points:**
  - id: KP7_1
    content: Nguyên lý ánh xạ chuỗi thành số nguyên của Dictionary Encoding
    keypoint_weight: 0.5
    description: Dictionary Encoding thay thế các chuỗi ký tự dài, lặp lại nhiều lần bằng các mã số nguyên nhỏ (ví dụ: ánh xạ "Hà Nội" thành số 0, "Hồ Chí Minh" thành số 1). Bản thân các số nguyên này chiếm dụng rất ít bộ nhớ so với chuỗi ký tự gốc.
  - id: KP7_2
    content: Tối ưu hóa dung lượng lưu trữ vật lý bằng kỹ thuật Bit-Packing
    keypoint_weight: 0.5
    description: Bit-Packing rà soát dải giá trị của các mã số nguyên trong từ điển. Nếu bảng chỉ chứa 4 tỉnh thành khác nhau (mã từ 0 đến 3), hệ thống nhận diện chỉ cần đúng 2 bits nhị phân để biểu diễn một giá trị, thay vì tốn toàn bộ 32-bits (4 bytes) cho một kiểu Int thông thường, giúp triệt tiêu hoàn toàn các bit 0 dư thừa và nén chặt dung lượng file vật lý trên đĩa cứng.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong các hệ quản trị cơ sở dữ liệu phân tán (Distributed Databases), tại sao các thuật toán đồng thuận phân tán (Distributed Consensus Algorithms - như Raft hoặc Paxos) lại mang ý nghĩa sống còn để duy trì trạng thái dữ liệu đồng nhất? Hãy giải thích cơ chế bầu chọn nút dẫn đầu (Leader Election) trong Raft.
* **expected_key_points:**
  - id: KP8_1
    content: Vai trò duy trì một trạng thái thống nhất duy nhất trên hệ thống phân tán
    keypoint_weight: 0.4
    description: Thuật toán đồng thuận đảm bảo rằng một nhóm các máy chủ độc lập (Nodes) trong cụm cluster có thể cùng đồng ý về một giá trị dữ liệu hoặc một chuỗi các lệnh giao dịch ghi, ngay cả khi có một vài máy chủ bị sập nguồn hoặc mất kết nối mạng, ngăn chặn hiện tượng dữ liệu bị bất đồng nhất giữa các Node.
  - id: KP8_2
    content: Cơ chế bầu chọn thủ lĩnh (Leader Election) trong Raft dựa trên bộ đếm thời gian ngẫu nhiên
    keypoint_weight: 0.4
    description: Khi Node dẫn đầu (Leader) hiện tại bị sập, các Node còn lại không nhận được tín hiệu duy trì sự sống (Heartbeat). Sau một khoảng thời gian chờ ngẫu nhiên (Election Timeout) của riêng mình, Node nào hết thời gian trước sẽ tự chuyển trạng thái sang Ứng cử viên (Candidate), tự tăng chỉ số phiên bầu cử (Term ID) và gửi yêu cầu bầu chọn (RequestVote) đến các Node khác.
  - id: KP8_3
    content: Nguyên lý đạt đa số phiếu để xác lập quyền thủ lĩnh chính thức (Quorum)
    keypoint_weight: 0.2
    description: Mỗi Node chỉ bầu tối đa 1 phiếu cho ứng cử viên đầu tiên liên hệ thỏa mãn điều kiện có lịch sử log cập nhật tương đương hoặc mới hơn mình. Nếu Candidate nhận được đa số phiếu ủng hộ từ cụm (đạt ngưỡng Quorum: $> N/2$), nó sẽ chính thức trở thành Leader mới và bắt đầu điều hành việc ghi chép dữ liệu.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích cấu trúc vật lý của một tệp tin nhị phân Apache Parquet dưới đĩa cứng. Giải thích cơ chế tổ chức của các thành phần: Page Header, Column Chunk, và vai trò của Footer Metadata trong việc tối ưu hóa tốc độ truy vấn đọc.
* **expected_key_points:**
  - id: KP9_1
    content: Cấu trúc phân tầng vật lý của tệp tin Parquet
    keypoint_weight: 0.4
    description: File Parquet gồm nhiều Nhóm dòng (Row Groups). Trong mỗi Row Group, dữ liệu được chia tách theo các khối cột (Column Chunks). Mỗi Column Chunk lại được cấu thành từ nhiều Trang dữ liệu (Pages) nhỏ hơn (thường là 1MB). Mỗi Page chứa một vùng Page Header lưu trữ metadata cục bộ về kiểu dữ liệu và thuật toán nén.
  - id: KP9_2
    content: Vai trò định tuyến và tra cứu sơ đồ của Footer Metadata
    keypoint_weight: 0.4
    description: Footer Metadata nằm ở cuối tệp tin Parquet, chứa thông tin Schema của toàn bộ bảng, vị trí vật lý (Offsets) bắt đầu của tất cả các Column Chunks và Row Groups trong file. Khi thực hiện câu lệnh đọc, hệ thống luôn đọc ngược từ cuối file lên để lấy sơ đồ định vị này trước, giúp nạp chính xác vùng đĩa chứa cột cần đọc mà không phải quét từ đầu file.
  - id: KP9_3
    content: Cơ chế bỏ qua khối dữ liệu không thỏa mãn điều kiện (Data skipping)
    keypoint_weight: 0.2
    description: Footer Metadata lưu trữ các thông tin thống kê tóm tắt của từng khối cột như giá trị Min, Max, số lượng phần tử NULL. Giúp các công cụ truy vấn (như Spark, Athena) đối chiếu điều kiện lọc của câu lệnh SQL để chủ động bỏ qua (Skip) toàn bộ các Row Groups không thỏa mãn điều kiện mà không cần tốn tài nguyên tải và giải nén chúng.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong Apache Spark, phép toán gộp dữ liệu `groupBy` trên các bảng có kích thước cực lớn thường gây ra tiến trình Shuffle cực kỳ đắt đỏ. Hãy giải thích cơ chế tối ưu hóa của giải thuật "Map-side Aggregation" (được triển khai qua `reduceByKey` ở RDD hoặc Catalyst Optimizer ở DataFrame) giúp giảm thiểu tối đa lượng dữ liệu truyền qua hạ tầng mạng vật lý.
* **expected_key_points:**
  - id: KP10_1
    content: Nguyên lý gộp dữ liệu cục bộ trước khi Shuffle (Local aggregation)
    keypoint_weight: 0.5
    description: Thay vì gửi trực tiếp toàn bộ các bản ghi thô có cùng một khóa (Key) qua mạng vật lý tới Node đích để tính toán (như cơ chế hoạt động của `groupByKey`), giải thuật Map-side Aggregation thực hiện phép toán gộp (như tính Sum, Count) ngay tại bộ nhớ đệm RAM cục bộ của từng Executor trước khi tiến trình Shuffle bắt đầu.
  - id: KP10_2
    content: Tiết kiệm tối đa băng thông truyền tải mạng và I/O đĩa cứng
    keypoint_weight: 0.3
    description: Kết quả của bước gộp cục bộ là mỗi Executor chỉ cần gửi đi duy nhất một bản ghi tổng hợp ứng với mỗi khóa khóa (ví dụ: gửi một cặp [Key, Total_Sum] duy nhất thay vì gửi hàng triệu bản ghi thô [Key, 1] qua mạng), làm giảm hàng triệu lần lượng dữ liệu truyền tải vật lý (Network I/O) và giảm dung lượng ghi file trung gian xuống đĩa cứng (Disk I/O).
  - id: KP10_3
    content: Loại bỏ hoàn toàn rủi ro tràn bộ nhớ ở tầng Reduce (OOM protection)
    keypoint_weight: 0.2
    description: Nhờ lượng dữ liệu sau Shuffle đã được tinh gọn ở mức tối đa, các Executor ở tầng nhận dữ liệu (Reduce stage) sẽ không bị quá tải bộ nhớ đệm RAM khi xử lý, triệt tiêu hoàn toàn rủi ro gây sập nguồn hệ thống do lỗi tràn bộ nhớ (Out Of Memory Exception).