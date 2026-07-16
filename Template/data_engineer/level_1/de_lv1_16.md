# Bộ Câu Hỏi Phỏng Vấn Data Engineer (Level 1)

* **Role:** Data Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế hệ thống dữ liệu lớn phân tán, kỹ thuật phân mảnh Sharding giúp chia nhỏ dữ liệu ra nhiều máy chủ vật lý. Hãy phân biệt điểm khác biệt cơ bản về nguyên lý phân bổ dữ liệu giữa hai cơ chế: Range-based Sharding và Hash-based Sharding.
* **expected_key_points:**
  - id: KP1_1
    content: Nguyên lý hoạt động và ưu nhược điểm của Range-based Sharding
    keypoint_weight: 0.5
    description: Range-based Sharding phân chia dữ liệu dựa trên các khoảng giá trị liên tục của khóa phân mảnh (ví dụ: Shard 1 chứa dữ liệu từ A-E, Shard 2 chứa từ F-J). Cơ chế này tối ưu cho các truy vấn tìm kiếm theo khoảng (Range Queries) nhưng dễ gây ra hiện tượng mất cân bằng tải trọng ghi dữ liệu (Hotspotting) trên một Shard cụ thể.
  - id: KP1_2
    content: Nguyên lý hoạt động và ưu nhược điểm của Hash-based Sharding
    keypoint_weight: 0.5
    description: Hash-based Sharding áp dụng một hàm băm (Hash Function) lên khóa phân mảnh, lấy kết quả chia dư cho số lượng Shards để tìm ra máy chủ đích lưu trữ. Cơ chế này giúp phân bổ dữ liệu và tải trọng ghi cực kỳ đồng đều trên toàn bộ các máy chủ vật lý, nhưng hiệu năng của các truy vấn tìm kiếm theo khoảng rất kém vì dữ liệu bị xé nhỏ ngẫu nhiên.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong kiến trúc luồng dữ liệu của một doanh nghiệp, hãy phân biệt điểm khác biệt cơ bản về mặt vai trò logic, thời gian lưu trữ và cấu trúc dữ liệu giữa Staging Area (Vùng lưu thô tạm thời) và Operational Data Store (ODS - Kho lưu trữ dữ liệu vận hành).
* **expected_key_points:**
  - id: KP2_1
    content: Bản chất và vai trò logic của Staging Area
    keypoint_weight: 0.5
    description: Staging Area là vùng đệm lưu trữ tạm thời, dữ liệu ở đây được giữ nguyên trạng từ hệ thống nguồn và thường bị xóa sạch hoặc ghi đè sau khi mỗi mẻ ETL hoàn thành (Thời gian lưu trữ rất ngắn). Cấu trúc của Staging không chuẩn hóa, không có ràng buộc chặt chẽ, chỉ dùng làm bàn đạp trung chuyển.
  - id: KP2_2
    content: Bản chất và vai trò logic của Operational Data Store (ODS)
    keypoint_weight: 0.5
    description: ODS là kho lưu trữ dữ liệu vận hành tích hợp từ nhiều nguồn, dữ liệu được làm sạch, đồng nhất hóa kiểu và cấu trúc dữ liệu. ODS lưu trữ dữ liệu trong thời hạn dài hơn (vài tháng) để phục vụ cho các báo cáo nhanh trong ngày, hỗ trợ các quyết định vận hành tức thì và có cấu trúc chuẩn hóa rõ ràng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong tối ưu hóa lưu trữ hướng cột (Columnar Storage), kỹ thuật nén Dictionary Encoding (Mã hóa từ điển) hoạt động ra sao và loại dữ liệu nào sẽ đạt được tỷ lệ nén tối ưu nhất khi áp dụng kỹ thuật này?
* **expected_key_points:**
  - id: KP3_1
    content: Nguyên lý hoạt động của Dictionary Encoding
    keypoint_weight: 0.5
    description: Kỹ thuật này xây dựng một bảng từ điển phụ (Dictionary) để ánh xạ các giá trị chuỗi văn bản hoặc giá trị dữ liệu dài, lặp đi lặp lại thành các mã số nguyên nhỏ (Integer IDs). Trong bảng dữ liệu chính, hệ thống chỉ lưu trữ các mã số nguyên nhỏ này để tiết kiệm dung lượng đĩa.
  - id: KP3_2
    content: Đặc tính dữ liệu tối ưu cho mã hóa từ điển
    keypoint_weight: 0.5
    description: Đạt tỷ lệ nén và hiệu năng cao nhất đối với các trường dữ liệu kiểu chuỗi (String) hoặc danh mục có độ đa dạng giá trị thấp (Low cardinality) nhưng xuất hiện lặp đi lặp lại với số lượng bản ghi cực lớn (ví dụ: mã quốc gia, tên phòng ban, loại thiết bị).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi xây dựng mô hình dữ liệu Dimensional Modeling cho kho dữ liệu (Data Warehouse), kỹ thuật thiết kế bảng "Junk Dimension" (Chiều chứa các thuộc tính vụn vặt) là gì và nó giúp giải quyết khuyết điểm gì trong cấu trúc thiết kế bảng Fact?
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa bản chất của Junk Dimension
    keypoint_weight: 0.4
    description: Junk Dimension là một bảng chiều duy nhất được tạo ra bằng cách gom nhóm toàn bộ các thuộc tính chỉ báo, mã trạng thái hoặc cờ logic vụn vặt (ví dụ: các cờ boolean Yes/No, trạng thái giao dịch Active/Pending) vốn không thuộc về bất kỳ bảng chiều lớn cụ thể nào khác.
  - id: KP4_2
    content: Giải quyết khuyết điểm phình to số lượng cột khóa ngoại của Fact Table
    keypoint_weight: 0.3
    description: Nếu không dùng Junk Dimension, Data Engineer bắt buộc phải đưa trực tiếp hàng chục cột cờ trạng thái này vào bảng Fact hoặc tạo ra hàng chục bảng chiều nhỏ lẻ tương ứng, làm bảng Fact bị phình to bề ngang và làm phức tạp hóa cấu trúc JOIN.
  - id: KP4_3
    content: Tối ưu hóa hiệu năng truy vấn và cấu trúc lược đồ
    keypoint_weight: 0.3
    description: Việc gom các cờ trạng thái vào một Junk Dimension duy nhất giúp giảm số lượng khóa ngoại nằm trong bảng Fact xuống tối thiểu, làm sạch lược đồ hình sao (Star Schema) và tăng tốc hiệu năng thực thi các phép JOIN.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong vận hành Data Pipeline, hiện tượng "Schema Drift" (Sự biến động cấu trúc dữ liệu từ nguồn) là gì? Hãy nêu hai giải pháp kỹ thuật để thiết kế một pipeline có khả năng chống chịu hoặc tự động xử lý hiện tượng này.
* **expected_key_points:**
  - id: KP5_1
    content: Định nghĩa hiện tượng Schema Drift từ hệ thống nguồn
    keypoint_weight: 0.4
    description: Schema Drift xảy ra khi hệ thống nguồn (Database giao dịch, SaaS API) bất ngờ thay đổi cấu trúc dữ liệu đầu ra (ví dụ: thêm cột mới, xóa cột cũ, thay đổi kiểu dữ liệu) mà không báo trước cho hệ thống nạp dữ liệu (Data Pipeline).
  - id: KP5_2
    content: Giải pháp Schema Evolution (Tiến hóa cấu trúc tự động)
    keypoint_weight: 0.3
    description: Thiết kế pipeline sử dụng các định dạng bảng hiện đại hỗ trợ tính năng tự động cập nhật schema (Schema Evolution như Delta Lake, Apache Iceberg). Khi phát hiện cột mới, hệ thống tự động ghi nhận và cập nhật cấu trúc bảng đích mà không làm treo hay lỗi luồng chạy vật lý.
  - id: KP5_3
    content: Giải pháp vùng đệm dữ liệu phi cấu trúc (Semi-structured fields) hoặc Schema Registry
    keypoint_weight: 0.3
    description: Sử dụng các dịch vụ Schema Registry tập trung để kiểm soát tính tương thích của dữ liệu ở đầu vào của pipeline, hoặc thiết kế lưu trữ cột dự phòng kiểu JSON/Map tại bảng đích để gom các thuộc tính mới phát sinh tự động mà không phá vỡ schema tĩnh hiện tại.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong kỹ thuật đồng bộ hóa dữ liệu (Data Replication), giải pháp đồng bộ dựa trên Transaction Log (Log-based Replication) của cơ sở dữ liệu quan hệ hoạt động dựa trên nguyên lý nào? Tại sao nó tối ưu hơn giải pháp truy vấn quét bảng định kỳ?
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên lý đọc tệp ghi nhật ký giao dịch tuần tự
    keypoint_weight: 0.5
    description: Hệ thống đồng bộ (Replication Engine) đọc trực tiếp tệp nhật ký ghi trước (Write-Ahead Log - WAL / Binlog) nơi lưu trữ tuần tự mọi thay đổi trạng thái của Database trước khi ghi xuống ổ đĩa, sau đó dịch mã các sự kiện này để áp dụng lên cơ sở dữ liệu đích.
  - id: KP6_2
    content: Tối ưu tải tài nguyên và tính toàn vẹn dữ liệu so với quét bảng
    keypoint_weight: 0.5
    description: Loại bỏ hoàn toàn các câu lệnh SELECT quét diện rộng (Full Table Scan) gây quá tải CPU/IO của hệ thống nguồn. Đồng thời, cơ chế này ghi nhận được cả các hành động xóa vật lý (DELETE) và đảm bảo dữ liệu được đồng bộ đồng nhất với độ trễ cực thấp (Near Real-time).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong các hệ thống lưu trữ NoSQL (như Apache Cassandra, RocksDB), tại sao cấu trúc dữ liệu LSM-Tree (Log-Structured Merge-tree) lại được sử dụng thay thế cho cấu trúc B-Tree truyền thống? LSM-Tree tối ưu hóa cho tác vụ nào và cơ chế dọn dẹp chạy ngầm của nó là gì?
* **expected_key_points:**
  - id: KP7_1
    content: Nguyên lý tối ưu ghi tuần tự thông qua MemTable và SSTable
    keypoint_weight: 0.5
    description: LSM-Tree tối ưu hóa cho tác vụ ghi dữ liệu với thông lượng cực cao (Write-heavy). Nó ghi dữ liệu trực tiếp vào bộ đệm bộ nhớ RAM (MemTable) và ghi nhật ký tuần tự xuống đĩa, sau đó định kỳ đẩy (Flush) dữ liệu từ RAM xuống các file tĩnh trên đĩa cứng gọi là SSTable (Sorted String Table) dưới dạng ghi tuần tự, tránh được việc ghi ngẫu nhiên (Random Writes) tốn tài nguyên của B-Tree.
  - id: KP7_2
    content: Cơ chế dọn dẹp và gộp file chạy ngầm Compaction
    keypoint_weight: 0.5
    description: Vì SSTable là bất biến (Immutable) nên việc cập nhật hoặc xóa dữ liệu thực chất là ghi đè phiên bản mới. Hệ thống chạy tiến trình gộp file ngầm (Compaction) để loại bỏ các bản ghi trùng lặp, giải phóng các bản ghi đã bị đánh dấu xóa (Tombstones) và sắp xếp lại dữ liệu để tối ưu hóa hiệu năng đọc.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Khi thực hiện một giao dịch ghi dữ liệu phân tán (Distributed Transaction) yêu cầu tính nhất quán ACID xuyên suốt nhiều máy chủ vật lý độc lập, hãy giải thích nguyên lý hoạt động và nhiệm vụ của hai giai đoạn trong giao thức "Two-Phase Commit" (2PC).
* **expected_key_points:**
  - id: KP8_1
    content: Cơ chế điều phối và hoạt động của Giai đoạn 1 (Prepare Phase)
    keypoint_weight: 0.4
    description: Node điều phối (Coordinator) gửi yêu cầu chuẩn bị ghi đến tất cả các Node tham gia (Participants). Các Node tham gia sẽ thực thi giao dịch cục bộ ở mức tạm thời (ghi vào log/WAL) để kiểm tra các ràng buộc, khóa tài nguyên và phản hồi lại cho Coordinator tín hiệu "Đồng ý" (Vote Commit) hoặc "Từ chối" (Vote Abort).
  - id: KP8_2
    content: Cơ chế và hoạt động của Giai đoạn 2 (Commit Phase)
    keypoint_weight: 0.4
    description: Nếu tất cả các Node tham gia đều Vote Commit, Coordinator sẽ gửi lệnh Commit chính thức, ép buộc các Node áp dụng thay đổi vĩnh viễn và giải phóng khóa. Nếu có ít nhất một Node phản hồi Vote Abort (hoặc hết thời gian chờ - Timeout), Coordinator sẽ gửi lệnh Rollback tới tất cả các Node để hủy bỏ toàn bộ giao dịch, bảo toàn tính nguyên tử (Atomicity).
  - id: KP8_3
    content: Điểm thắt nút cổ chai hiệu năng và rủi ro treo hệ thống của 2PC
    keypoint_weight: 0.2
    description: Giao thức 2PC là cơ chế đồng bộ chặn (Blocking protocol). Nếu Node điều phối bị sập nguồn giữa hai giai đoạn, các Node tham gia sẽ rơi vào trạng thái treo tài nguyên (Blocked) vì không biết nên Commit hay Rollback, làm giảm mạnh tính sẵn sàng (Availability) của hệ thống.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong kiến trúc của các cơ sở dữ liệu phân tán dạng Column-Family Store (như Apache HBase, Google Bigtable), cấu trúc lưu trữ phân tán tổ chức dữ liệu vật lý theo định dạng đa chiều "Sparse, Distributed, Persistent, Multi-dimensional Sorted Map" nghĩa là gì?
* **expected_key_points:**
  - id: KP9_1
    content: Định nghĩa cấu trúc bản đồ khóa đa chiều và tính sắp xếp (Sorted Map)
    keypoint_weight: 0.4
    description: Dữ liệu được định danh và sắp xếp theo thứ tự bảng chữ cái của Khóa hàng (Row Key). Mỗi ô dữ liệu được định vị chính xác bằng một cấu trúc bản đồ đa chiều gồm: Row Key (Khóa hàng) -> Column Family (Nhóm cột) -> Column Qualifier (Tên cột cụ thể) -> Timestamp (Mốc thời gian phiên bản).
  - id: KP9_2
    content: Ý nghĩa vật lý của tính chất thưa thớt (Sparse) đối với dữ liệu lớn
    keypoint_weight: 0.4
    description: Mang tính chất thưa thớt (Sparse) nghĩa là các ô không có dữ liệu (NULL values) sẽ hoàn toàn không chiếm dụng bất kỳ dung lượng lưu trữ vật lý nào trên đĩa cứng. Hệ thống chỉ lưu trữ các ô thực sự có chứa giá trị, giúp tiết kiệm tối đa đĩa cứng khi lưu trữ các bảng phân tích có hàng triệu cột rỗng.
  - id: KP9_3
    content: Tính chất phân tán (Distributed) và lưu trữ vĩnh viễn (Persistent)
    keypoint_weight: 0.2
    description: Dữ liệu của bảng được chia tách theo các khoảng khóa hàng thành các phân đoạn (Regions/Tablets) phân tán trên nhiều máy chủ vật lý khác nhau, và được lưu trữ vĩnh viễn (Persistent) dưới dạng các file tĩnh bất biến trên hệ thống file phân tán (như HDFS/GFS).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong quá trình xử lý song song trong Apache Spark, hãy phân biệt sự khác biệt về mặt cơ chế phân chia dữ liệu và thuật toán băm khóa của đĩa vật lý giữa hai giải pháp phân vùng khi thực thi Shuffle: Hash-partitioning và Range-partitioning.
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế hoạt động và ứng dụng của Hash-partitioning trong Spark Shuffle
    keypoint_weight: 0.4
    description: Hash-partitioning áp dụng hàm băm của Spark lên khóa (Key) của bản ghi, lấy giá trị băm chia dư cho tổng số phân vùng đích để định tuyến dữ liệu. Thường được sử dụng mặc định trong các phép toán nhóm dữ liệu (`groupByKey`, `join`), giúp phân bổ số lượng bản ghi tương đối đồng đều nhưng không bảo toàn thứ tự dữ liệu.
  - id: KP10_2
    content: Cơ chế hoạt động và ứng dụng của Range-partitioning trong Spark Shuffle
    keypoint_weight: 0.4
    description: Range-partitioning phân chia dữ liệu dựa trên các khoảng giá trị của khóa (ví dụ: Phân vùng 1 nhận khóa từ 1-100, Phân vùng 2 nhận từ 101-200). Thường được sử dụng trong các phép toán sắp xếp (`sortByKey`, `orderBy`). Để phân chia dải khóa đồng đều, Spark phải thực hiện một bước quét mẫu dữ liệu chạy ngầm (Sampling) trước khi chia dải, nhằm tránh hiện tượng lệch dữ liệu (Data skew).
  - id: KP10_3
    content: Sự khác biệt về chi phí tính toán và rủi ro lệch phân vùng giữa hai kỹ thuật
    keypoint_weight: 0.2
    description: Hash-partitioning có chi phí tính toán phân vùng cực rẻ nhưng không kiểm soát được sự lệch kích thước vật lý của phân vùng nếu các giá trị khóa trùng nhau quá nhiều. Range-partitioning tốn chi phí quét lấy mẫu dữ liệu hơn nhưng kiểm soát tốt kích thước phân vùng vật lý khi sắp xếp dữ liệu lớn.