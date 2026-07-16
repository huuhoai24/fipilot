# Bộ Câu Hỏi Phỏng Vấn Data Engineer (Level 1)

* **Role:** Data Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế cơ sở dữ liệu quan hệ (RDBMS), việc thiết lập Index (Chỉ mục) dựa trên cơ chế cấu trúc dữ liệu nào? Tại sao một bảng có quá nhiều Index lại làm giảm hiệu năng của các tác vụ ghi (INSERT, UPDATE, DELETE)?
* **expected_key_points:**
  - id: KP1_1
    content: Cơ chế cấu trúc dữ liệu cây tìm kiếm (B-Tree/B+Tree)
    keypoint_weight: 0.5
    description: Index hoạt động dựa trên việc tạo ra các cấu trúc cây tìm kiếm (phổ biến nhất là B-Tree hoặc B+Tree) lưu trữ các cặp khóa và con trỏ trỏ tới hàng dữ liệu thực tế, giúp giảm độ phức tạp tìm kiếm từ O(N) xuống O(log N).
  - id: KP1_2
    content: Chi phí tính toán cập nhật chỉ mục khi ghi dữ liệu (Write Overhead)
    keypoint_weight: 0.5
    description: Mỗi khi thực hiện ghi mới hoặc cập nhật dữ liệu, hệ thống không chỉ thay đổi dữ liệu trong bảng vật lý mà còn bắt buộc phải cập nhật và tái cấu trúc lại toàn bộ các cây chỉ mục liên quan, gây tốn tài nguyên I/O đĩa cứng và làm chậm tốc độ ghi.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Khi xây dựng Data Lake, hãy phân biệt điểm khác biệt cốt lộ về cấu trúc lưu trữ và tối ưu hóa hiệu năng đọc/ghi giữa hai định dạng tệp tin: CSV (văn bản thô) và Apache Parquet (nhị phân).
* **expected_key_points:**
  - id: KP2_1
    content: Bản chất lưu trữ dạng dòng (Row-oriented) của CSV
    keypoint_weight: 0.5
    description: CSV lưu trữ dữ liệu theo từng dòng văn bản thô (Plain text), không có thông tin Schema tích hợp sẵn. Phù hợp cho việc trao đổi dữ liệu dung lượng nhỏ nhưng cực kỳ tốn không gian đĩa cứng và rất chậm khi cần truy vấn tính toán gộp (Aggregation).
  - id: KP2_2
    content: Bản chất lưu trữ dạng cột (Columnar-oriented) và nén của Parquet
    keypoint_weight: 0.5
    description: Parquet lưu trữ dữ liệu phân tách theo dạng cột dưới dạng nhị phân, tích hợp sẵn Metadata về Schema của bảng. Định dạng này hỗ trợ nén dữ liệu rất cao và tối ưu hóa hiệu năng đọc bằng cách chỉ nạp đúng các cột cần thiết cho việc phân tích (Projection).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt điểm khác nhau về cơ chế xử lý dữ liệu và tần suất kích hoạt hệ thống giữa hai mô hình: Batch Processing (Xử lý theo lô) và Stream Processing (Xử lý luồng).
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế hoạt động của Batch Processing (Xử lý theo lô định kỳ)
    keypoint_weight: 0.5
    description: Thu thập dữ liệu thô và tích lũy lại thành một lô lớn trong một khoảng thời gian xác định (theo giờ, ngày, tuần) rồi mới khởi động hệ thống tính toán một lần, chấp nhận độ trễ thông tin cao để tối ưu hiệu năng tính toán khối lượng lớn dữ liệu lịch sử.
  - id: KP3_2
    content: Cơ chế hoạt động của Stream Processing (Xử lý luồng thời gian thực)
    keypoint_weight: 0.5
    description: Tiếp nhận và xử lý tính toán liên tục trên từng bản ghi dữ liệu đơn lẻ (Event-by-event) ngay tại thời điểm chúng phát sinh, đáp ứng yêu cầu độ trễ cực thấp (gần như tức thời) cho các bài toán phân tích thời gian thực.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong thiết kế kho dữ liệu (Data Warehouse) theo mô hình Dimensional Modeling, kỹ thuật "Slowly Changing Dimension" (SCD) dùng để xử lý bài toán gì? Hãy mô tả sự khác biệt giữa SCD Type 1 và SCD Type 2.
* **expected_key_points:**
  - id: KP4_1
    content: Mục tiêu quản lý sự biến động của dữ liệu thuộc tính theo thời gian
    keypoint_weight: 0.4
    description: SCD được áp dụng trong các bảng Dimension nhằm quản lý và lưu giữ thông tin khi các thuộc tính mô tả (như địa chỉ khách hàng, tên phòng ban nhân viên) bị thay đổi chậm theo thời gian.
  - id: KP4_2
    content: Cơ chế ghi đè trực tiếp của SCD Type 1
    keypoint_weight: 0.3
    description: SCD Type 1 thực hiện ghi đè trực tiếp giá trị mới lên trường dữ liệu cũ, không giữ lại lịch sử thay đổi, phù hợp cho việc sửa sai thông tin hoặc khi lịch sử không có giá trị phân tích.
  - id: KP4_3
    content: Cơ chế thêm dòng mới lưu vết lịch sử của SCD Type 2
    keypoint_weight: 0.3
    description: SCD Type 2 tạo một dòng mới trong bảng chứa giá trị mới, kết hợp thêm các cột trạng thái (như Effective_Date, End_Date, Is_Current) để phân tách các phiên bản dữ liệu và lưu giữ lịch sử biến động đầy đủ.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong kiến trúc công nghệ xử lý dữ liệu lớn phân tán Apache Spark, hai thành phần "Driver" và "Executor" thực hiện các vai trò logic gì khi một ứng dụng (Application) được thực thi?
* **expected_key_points:**
  - id: KP5_1
    content: Vai trò điều phối trung tâm của Driver Node
    keypoint_weight: 0.5
    description: Driver là tiến trình chứa hàm main(), có nhiệm vụ phân tích mã nguồn của người dùng để xây dựng kế hoạch thực thi logic (DAG), chia nhỏ công việc thành các Stages/Tasks vật lý và điều phối lịch trình gửi Tasks xuống các Worker Nodes.
  - id: KP5_2
    content: Vai trò tính toán trực tiếp của Executor Node
    keypoint_weight: 0.5
    description: Executor là các tiến trình chạy ngầm trên Worker Nodes chịu trách nhiệm nhận Tasks từ Driver, cấp phát bộ nhớ RAM để thực thi tính toán trực tiếp trên dữ liệu và báo cáo kết quả cùng trạng thái hoạt động về cho Driver.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao việc thiết kế "Idempotency" (Tính lũy đẳng) lại là tiêu chuẩn bắt buộc khi xây dựng các Data Pipelines thu thập dữ liệu tự động? Nêu một ví dụ thực tế về lỗi dữ liệu nếu thiếu tính chất này.
* **expected_key_points:**
  - id: KP6_1
    content: Đảm bảo kết quả nhất quán không đổi khi chạy lại nhiều lần (Retry Safety)
    keypoint_weight: 0.5
    description: Idempotency đảm bảo rằng nếu một pipeline hay tác vụ ghi dữ liệu bị chạy lại một hoặc nhiều lần với cùng một tập dữ liệu đầu vào (do lỗi mạng hoặc hệ thống khởi động lại), trạng thái dữ liệu ở đích vẫn hoàn toàn nhất quán, không bị nhân bản hay sai lệch.
  - id: KP6_2
    content: Rủi ro trùng lặp dữ liệu kèm ví dụ thực tế
    keypoint_weight: 0.5
    description: Thiếu tính lũy đẳng sẽ dẫn đến việc ghi đè hoặc chèn trùng lặp dữ liệu. Ví dụ: Một pipeline nạp dữ liệu giao dịch tài chính bị mất kết nối giữa chừng và chạy lại; nếu không có cơ chế chặn trùng (như UPSERT/Merge), một đơn hàng sẽ bị chèn 2 lần vào DB đích, làm sai lệch báo cáo doanh thu.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy phân tích tại sao mô hình kiến trúc ELT (Extract, Load, Transform) đang dần thay thế mô hình ETL (Extract, Transform, Load) truyền thống khi doanh nghiệp dịch chuyển hệ thống dữ liệu lên Cloud?
* **expected_key_points:**
  - id: KP7_1
    content: Lưu trữ thô trước để tối ưu hóa thời gian nạp dữ liệu (Load first)
    keypoint_weight: 0.5
    description: ELT trích xuất và đẩy thẳng dữ liệu thô vào Data Lake/Warehouse trước khi biến đổi, giúp rút ngắn thời gian xử lý trung gian và lưu trữ nguyên bản dữ liệu lịch sử để tái sử dụng sau này, tận dụng giá thành lưu trữ Cloud cực rẻ.
  - id: KP7_2
    content: Tận dụng trực tiếp sức mạnh tính toán phân tán (MPP) của Warehouse đích
    keypoint_weight: 0.5
    description: Thay vì tốn tài nguyên dựng máy chủ biến đổi dữ liệu riêng bên ngoài (như ETL), ELT tận dụng trực tiếp năng lực tính toán phân tán song song cực mạnh của các Modern Cloud Data Warehouses (như Snowflake, BigQuery) thông qua các câu lệnh SQL để biến đổi dữ liệu ngay tại đích.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong tính toán dữ liệu phân tán (như Apache Spark), hiện tượng "Data Skew" (Lệch dữ liệu) là gì? Hiện tượng này gây ra hậu quả hiệu năng tiêu cực nào và phương pháp xử lý cơ bản ở mức mã nguồn là gì?
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất phân bổ dữ liệu không đồng đều giữa các Partitions
    keypoint_weight: 0.4
    description: Data Skew xảy ra khi một số ít phân vùng (Partitions) chứa lượng dữ liệu khổng lồ vượt trội so với phần còn lại, thường do khóa phân vùng (Partition Key) bị trùng lặp quá nhiều giá trị (như khóa NULL hoặc mã ID mặc định).
  - id: KP8_2
    content: Gây thắt nút cổ chai hiệu năng hệ thống (Straggler Tasks)
    keypoint_weight: 0.3
    description: Trong tính toán phân tán, một Stage chỉ kết thúc khi Task cuối cùng chạy xong. Node nhận phân vùng bị lệch sẽ phải xử lý dữ liệu lâu hơn rất nhiều, làm treo tài nguyên của cả cụm (Straggler) hoặc gây lỗi tràn bộ nhớ (Out Of Memory - OOM).
  - id: KP8_3
    content: Giải pháp khắc phục bằng kỹ thuật Salting (Nhiễu muối) hoặc tách lọc
    keypoint_weight: 0.3
    description: Áp dụng kỹ thuật Salting bằng cách thêm một hậu tố số ngẫu nhiên vào khóa bị lệch để phân tán dữ liệu đều ra các phân vùng khác nhau trước khi thực hiện các phép toán Group by/Join, hoặc thực hiện lọc tách riêng nhóm dữ liệu bị lệch để xử lý bằng Broadcast Join rồi Union lại sau.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hãy giải thích nguyên lý kỹ thuật giúp các hệ thống Lakehouse (như Delta Lake) có thể hỗ trợ tính năng "Time Travel" (Truy cập dữ liệu lịch sử tại một thời điểm) mà không cần sao chép nhân bản các tệp tin vật lý thành nhiều phiên bản.
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế quản lý trạng thái qua tệp nhật ký giao dịch tuần tự (Commit Log / Transaction Log)
    keypoint_weight: 0.4
    description: Delta Lake lưu giữ một thư mục nhật ký giao dịch chạy ngầm ghi nhận chi tiết mọi thay đổi cấu trúc bảng dưới dạng các tệp JSON tuần tự, chỉ ra chính xác danh sách các tệp Parquet vật lý nào đang có hiệu lực ứng với từng Version của bảng.
  - id: KP9_2
    content: Cơ chế bất biến của tệp dữ liệu vật lý dưới đĩa cứng (Immutability)
    keypoint_weight: 0.4
    description: Các tệp Parquet vật lý là bất biến. Khi thực hiện UPDATE hoặc DELETE, hệ thống ghi các file Parquet mới chứa dữ liệu thay đổi chứ không ghi đè lên file cũ, đồng thời đánh dấu trong Transaction Log rằng file cũ đã hết hiệu lực từ phiên bản mới.
  - id: KP9_3
    content: Cơ chế tái dựng trạng thái bảng tại thời điểm yêu cầu (State Reconstruction)
    keypoint_weight: 0.2
    description: Khi người dùng thực hiện truy vấn lịch sử (ví dụ truy cập Version 3), hệ thống sẽ đọc Transaction Log từ đầu đến phiên bản số 3 để xác định đúng danh sách các tệp Parquet vật lý có hiệu lực tại thời điểm đó và chỉ nạp đúng các tệp này để trả về kết quả.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong xử lý dữ liệu luồng (Streaming), hãy phân biệt sự khác biệt logic giữa ba khái niệm thời gian: Event Time, Ingestion Time, và Processing Time. Cơ chế "Watermark" được sử dụng để giải quyết bài toán gì khi dữ liệu bị đến trễ (Late Data)?
* **expected_key_points:**
  - id: KP10_1
    content: Phân biệt rõ bản chất của ba mốc thời gian trong vòng đời dữ liệu luồng
    keypoint_weight: 0.4
    description: Event Time là thời điểm sự kiện thực sự xảy ra tại thiết bị nguồn. Ingestion Time là thời điểm sự kiện được nạp vào hệ thống tiếp nhận (như Kafka). Processing Time là thời điểm sự kiện được máy chủ xử lý thực thi tính toán trực tiếp trên RAM.
  - id: KP10_2
    content: Bản chất và mục đích của cơ chế Watermark
    keypoint_weight: 0.3
    description: Watermark là một mốc thời gian logic di chuyển tịnh tiến đại diện cho tiến trình của Event Time. Nó đóng vai trò là một lời khẳng định ngầm rằng "hệ thống giả định không còn dữ liệu nào có Event Time cũ hơn mốc $T$ xuất hiện nữa", làm căn cứ để quản lý cửa sổ thời gian (Windowing).
  - id: KP10_3
    content: Cơ chế xử lý và cho phép độ trễ của dữ liệu đến muộn
    keypoint_weight: 0.3
    description: Watermark cho phép hệ thống duy trì cửa sổ tính toán mở thêm một khoảng thời gian chờ cố định để gom các dữ liệu bị trễ do nghẽn mạng mạng vật lý. Khi Watermark vượt qua biên của cửa sổ, hệ thống sẽ thực hiện đóng cửa sổ, tính toán kết quả cuối cùng và bỏ qua các dữ liệu đến trễ hơn mốc này.