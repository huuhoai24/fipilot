# Bộ Câu Hỏi Phỏng Vấn Data Engineer (Level 1)

* **Role:** Data Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong định dạng lưu trữ hướng cột Apache Parquet, kỹ thuật nén dữ liệu Run-Length Encoding (RLE) hoạt động dựa trên nguyên lý gì và nó mang lại hiệu quả tối ưu cao nhất khi áp dụng cho loại dữ liệu như thế nào?
* **expected_key_points:**
  - id: KP1_1
    content: Nguyên lý hoạt động cơ bản của Run-Length Encoding (RLE)
    keypoint_weight: 0.5
    description: RLE là phương pháp nén dữ liệu không mất mát bằng cách phát hiện các giá trị dữ liệu giống nhau lặp lại liên tiếp, sau đó thay thế chuỗi lặp đó bằng một cặp giá trị duy nhất gồm: [Số lần lặp lại, Giá trị dữ liệu].
  - id: KP1_2
    content: Ngữ cảnh dữ liệu tối ưu nhất cho RLE
    keypoint_weight: 0.5
    description: RLE đạt hiệu năng nén và tiết kiệm dung lượng cao nhất khi áp dụng cho các cột dữ liệu có độ đa dạng giá trị thấp (Low cardinality) và có xu hướng xuất hiện lặp lại liên tục thành từng nhóm (ví dụ: cột trạng thái Active/Inactive, cột giới tính, hoặc dữ liệu đã được sắp xếp tăng/giảm dần trước khi lưu).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Khi lựa chọn giải pháp lưu trữ cho hệ thống Big Data, hãy phân biệt điểm khác biệt cơ bản về mặt kiến trúc và cách thức truy cập dữ liệu giữa HDFS Block Storage (Hadoop Distributed File System) và Cloud Object Storage (như AWS S3, Google Cloud Storage).
* **expected_key_points:**
  - id: KP2_1
    content: Kiến trúc phân mảnh vật lý và tính năng của HDFS
    keypoint_weight: 0.5
    description: HDFS chia nhỏ file dữ liệu thành các khối vật lý cố định (HDFS Blocks, thường là 128MB) và phân tán, nhân bản chúng sang các DataNodes trong cụm máy chủ cục bộ. Nó hỗ trợ ghi đè/append tệp tin và tối ưu hóa tính năng di chuyển code đến dữ liệu (Data Locality) nhưng yêu cầu duy trì NameNode phức tạp.
  - id: KP2_2
    content: Kiến trúc phi cấu trúc hướng đối tượng của Cloud Object Storage
    keypoint_weight: 0.5
    description: Cloud Object Storage lưu trữ dữ liệu dưới dạng các thực thể độc lập (Objects) bao gồm metadata và payload trong một không gian phẳng, truy cập trực tiếp qua HTTP/HTTPS APIs. Hệ thống này không có khái niệm thư mục vật lý thực tế, có khả năng tự động co giãn dung lượng vô hạn với chi phí cực rẻ nhưng không có Data Locality và việc sửa đổi một phần file yêu cầu ghi đè lại toàn bộ.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế Data Pipeline, hãy phân biệt điểm khác nhau về cơ chế kích hoạt luồng xử lý và trường hợp áp dụng thực tế giữa mô hình Time-driven Pipeline (Chạy theo lịch biểu) và Event-driven Pipeline (Chạy theo sự kiện).
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế hoạt động và ứng dụng của Time-driven Pipeline
    keypoint_weight: 0.5
    description: Luồng xử lý được tự động kích hoạt dựa trên mốc thời gian định sẵn (như cấu hình cron job chạy lúc 0h hằng ngày hoặc mỗi 30 phút). Phù hợp cho các tác vụ nạp dữ liệu theo lô (Batch Processing) quy mô lớn, báo cáo tổng hợp lịch sử mà doanh nghiệp không yêu cầu tính tức thời.
  - id: KP3_2
    content: Cơ chế hoạt động và ứng dụng của Event-driven Pipeline
    keypoint_weight: 0.5
    description: Luồng xử lý được kích hoạt ngay lập tức khi phát sinh một sự kiện cụ thể từ hệ thống nguồn (như có file mới nạp vào thư mục, nhận tin nhắn từ Kafka topic hoặc có webhook gọi từ bên thứ ba). Phù hợp cho việc nạp dữ liệu thời gian thực (Near Real-time/Streaming), yêu cầu độ trễ thấp để kịp thời xử lý nghiệp vụ tức thì.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong thiết kế kho dữ liệu (Data Warehouse) theo mô hình Dimensional Modeling, Slowly Changing Dimension (SCD) Type 3 hoạt động ra sao và nó có những hạn chế kỹ thuật lớn nào so với SCD Type 2?
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế lưu trữ lịch sử bằng cách thêm cột mới của SCD Type 3
    keypoint_weight: 0.4
    description: SCD Type 3 theo dõi sự thay đổi thuộc tính bằng cách bổ sung thêm các cột mới vào chính dòng hiện tại của bảng (ví dụ: thêm cột `Previous_City` bên cạnh cột `Current_City`), thay vì tạo thêm dòng mới.
  - id: KP4_2
    content: Hạn chế về số lượng phiên bản lịch sử lưu trữ
    keypoint_weight: 0.3
    description: SCD Type 3 bị giới hạn cứng về số lượng phiên bản lịch sử có thể lưu trữ (thông thường chỉ lưu được trạng thái hiện tại và một trạng thái ngay trước đó). Hệ thống hoàn toàn không có khả năng theo dõi chuỗi lịch sử thay đổi liên tục qua nhiều năm như SCD Type 2.
  - id: KP4_3
    content: Hạn chế về tính linh hoạt và thiết kế cấu trúc bảng (Schema change)
    keypoint_weight: 0.3
    description: Mỗi khi doanh nghiệp phát sinh nhu cầu muốn lưu giữ thêm một phiên bản lịch sử mới, Data Engineer bắt buộc phải can thiệp cấu trúc vật lý của bảng (thực hiện câu lệnh ALTER TABLE để thêm cột), làm tăng chi phí bảo trì hệ thống và có rủi ro ảnh hưởng dây chuyền đến các câu lệnh SQL ở hạ nguồn.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi xây dựng luồng xử lý dữ liệu thời gian thực (Stream Processing), hệ thống rất dễ gặp phải hiện tượng dữ liệu bị đến trễ hoặc bất tuần tự (Out-of-order Data). Hãy giải thích nguyên nhân hệ thống phát sinh hiện tượng này và cơ chế tích hợp bộ đệm trong Spark để xử lý.
* **expected_key_points:**
  - id: KP5_1
    content: Nguyên nhân phát sinh dữ liệu đến trễ và bất tuần tự
    keypoint_weight: 0.5
    description: Dữ liệu bị đến trễ do các sự cố vật lý ngoài tầm kiểm soát của hệ thống dữ liệu như: thiết bị nguồn bị mất kết nối mạng tạm thời nên tích lũy dữ liệu offline rồi đẩy dồn dập sau, nghẽn mạng truyền tải, hoặc do độ trễ xử lý khác nhau giữa các phân vùng mạng phân tán.
  - id: KP5_2
    content: Cơ chế sử dụng bộ đệm trạng thái (Stateful Storage) kết hợp Watermark
    keypoint_weight: 0.5
    description: Spark Streaming duy trì một vùng bộ nhớ đệm chạy ngầm để lưu giữ tạm thời trạng thái tính toán của các cửa sổ thời gian (Windows). Khi nhận được dữ liệu đến trễ, hệ thống đối chiếu với mốc Watermark; nếu Event Time của bản ghi vẫn nằm trong ngưỡng trễ cho phép, Spark sẽ nạp dữ liệu vào bộ đệm để tính toán cập nhật lại kết quả, ngược lại sẽ chủ động loại bỏ dữ liệu để giải phóng RAM.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong thiết kế Data Pipeline truyền tải dữ liệu dung lượng lớn, tại sao kỹ thuật kiểm soát Checksum lại cực kỳ quan trọng để đảm bảo tính nhất quán dữ liệu vật lý khi di chuyển file qua các hệ thống khác nhau?
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên lý tính toán hàm băm kiểm tra tính toàn vẹn file
    keypoint_weight: 0.5
    description: Checksum là việc áp dụng một thuật toán băm mật mã (như MD5, SHA-256) lên toàn bộ nội dung của tệp tin trước khi truyền tải để sinh ra một chuỗi ký tự đại diện duy nhất (Hash value) có kích thước cố định.
  - id: KP6_2
    content: Cơ chế đối chiếu ở hệ thống đích để phát hiện lỗi truyền tin
    keypoint_weight: 0.5
    description: Sau khi tệp tin được truyền sang hệ thống đích, hệ thống đích sẽ tự động tính toán lại Checksum của tệp tin nhận được và đối chiếu với giá trị Checksum gốc từ nguồn gửi sang. Nếu hai giá trị trùng khớp hoàn hảo, file được xác nhận an toàn; nếu sai lệch, chứng tỏ file đã bị lỗi trong quá trình truyền tải (đứt mạng, lỗi ghi đĩa) và cần kích hoạt cơ chế truyền lại.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong kiến trúc hệ thống dữ liệu doanh nghiệp, phân hệ Operational Data Store (ODS - Kho lưu trữ dữ liệu vận hành) đóng vai trò trung gian gì và nó khác biệt thế nào với Data Warehouse (DWH) về mặt tần suất cập nhật dữ liệu và thời gian lưu trữ dữ liệu lịch sử?
* **expected_key_points:**
  - id: KP7_1
    content: Vai trò trung gian tích hợp dữ liệu thô gần thời gian thực của ODS
    keypoint_weight: 0.4
    description: ODS đóng vai trò là tầng lưu trữ trung gian nằm giữa các cơ sở dữ liệu giao dịch nguồn (OLTP) và Data Warehouse. ODS dùng để tích hợp nhanh dữ liệu từ nhiều nguồn khác nhau về một cấu trúc đồng nhất, phục vụ trực tiếp cho các báo cáo vận hành nhanh trong ngày của doanh nghiệp.
  - id: KP7_2
    content: Khác biệt về tần suất nạp dữ liệu và tính thời sự
    keypoint_weight: 0.3
    description: Dữ liệu trong ODS được cập nhật liên tục với tần suất rất cao (thường là thời gian thực hoặc gần thời gian thực qua CDC). Trong khi đó, Data Warehouse thường nạp dữ liệu theo chu kỳ lô định trước (Batch hằng ngày hoặc hằng tuần) để phục vụ phân tích chiến lược dài hạn.
  - id: KP7_3
    content: Khác biệt về khả năng và thời gian lưu trữ dữ liệu lịch sử
    keypoint_weight: 0.3
    description: ODS chỉ lưu trữ dữ liệu ở trạng thái hiện tại hoặc lịch sử rất ngắn (vài tuần đến vài tháng) để tối ưu hóa bộ nhớ và hiệu năng truy vấn nhanh. Data Warehouse lưu trữ toàn bộ lịch sử biến động dữ liệu tích lũy qua nhiều năm để chạy các báo cáo phân tích xu hướng.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong Google BigQuery hoặc các cơ sở dữ liệu phân tích hiện đại, tại sao việc thiết kế dữ liệu phi chuẩn hóa sử dụng cấu trúc "Nested and Repeated Fields" (trường lồng nhau và lặp lại - STRUCT và ARRAY) lại cho hiệu năng truy vấn tối ưu hơn rất nhiều so với việc phân tách thành các bảng Dimension chuẩn hóa thông thường?
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất lưu trữ vật lý đồng địa điểm của cấu trúc lồng ghép (Colocation)
    keypoint_weight: 0.4
    description: Nested and Repeated Fields cho phép lưu trữ trực tiếp các mối quan hệ 1-nhiều (one-to-many, như đơn hàng và danh sách chi tiết mặt hàng mua) vào chung một dòng dữ liệu vật lý duy nhất trên đĩa cứng dưới định dạng cột (như Capacitor/Parquet format).
  - id: KP8_2
    content: Triệt tiêu hoàn toàn chi phí xáo trộn dữ liệu qua mạng của phép toán JOIN (No network Shuffle)
    keypoint_weight: 0.4
    description: Khi thực hiện truy vấn phân tích, hệ thống hoàn toàn không cần thực hiện phép toán JOIN vật lý giữa bảng chính và bảng phụ qua mạng. Dữ liệu liên quan đã nằm sẵn trên cùng một khối dữ liệu vật lý, giúp loại bỏ tiến trình Shuffle đắt đỏ và tăng tốc độ xử lý lên nhiều lần.
  - id: KP8_3
    content: Khả năng bảo toàn cấu trúc phân cấp và tối ưu hóa chi phí quét dữ liệu
    keypoint_weight: 0.2
    description: Giúp lập trình viên dễ dàng làm mịn và truy xuất dữ liệu phân cấp phức tạp bằng các hàm UNNEST mà không làm phình to số lượng dòng quét vật lý của hệ thống, giúp tối ưu tối đa chi phí quét dữ liệu (Data scanned cost) trên đám mây.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích nguyên lý hoạt động của cơ chế kiểm soát truy cập đồng thời đa phiên bản MVCC (Multi-Version Concurrency Control) trong các hệ quản trị cơ sở dữ liệu phân tán. Làm thế nào MVCC đảm bảo các tác vụ đọc không bị chặn bởi các tác vụ ghi (Lock-free reads)?
* **expected_key_points:**
  - id: KP9_1
    content: Nguyên lý tạo phiên bản dữ liệu song song thay vì ghi đè trực tiếp
    keypoint_weight: 0.4
    description: Khi có tác vụ ghi dữ liệu (UPDATE, DELETE), hệ thống không ghi đè trực tiếp lên dữ liệu vật lý cũ mà tạo ra một phiên bản mới của bản ghi dữ liệu đó đi kèm với một số hiệu phiên bản logic (gắn liền mốc transaction ID hoặc timestamp).
  - id: KP9_2
    content: Cơ chế xác định vùng nhìn thấy của giao dịch (Snapshot Isolation)
    keypoint_weight: 0.4
    description: Khi một câu lệnh đọc (SELECT) được kích hoạt, hệ thống tự động cung cấp một ảnh chụp nhanh dữ liệu (Snapshot) tại mốc thời gian bắt đầu giao dịch của câu lệnh đó. Hệ thống chỉ cho phép đọc phiên bản dữ liệu mới nhất đã được commit trước mốc thời gian này, bỏ qua các phiên bản đang được ghi dở dang của các transaction khác.
  - id: KP9_3
    content: Triệt tiêu hiện tượng thắt nút cổ chai do khóa tài nguyên (Lock-free reads)
    keypoint_weight: 0.2
    description: Vì tác vụ đọc dữ liệu luôn truy cập vào một phiên bản lịch sử bất biến ổn định có sẵn, nó hoàn toàn không cần phải chờ đợi hay tranh chấp khóa (Locks) với tác vụ ghi đang diễn ra, giúp tối ưu hóa tối đa thông lượng xử lý song song của hệ thống.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong tối ưu hóa lưu trữ đĩa vật lý của Big Data, hãy giải thích nguyên lý hoạt động của cơ chế mã hóa Delta Encoding. Tại sao cơ chế này lại đem lại tỷ lệ nén file vượt trội khi áp dụng cho các cột dữ liệu kiểu mốc thời gian (Timestamp) tăng dần?
* **expected_key_points:**
  - id: KP10_1
    content: Nguyên lý toán học tính toán khoảng cách giá trị của Delta Encoding
    keypoint_weight: 0.4
    description: Thay vì lưu trữ trực tiếp các giá trị số nguyên vật lý lớn của từng bản ghi, Delta Encoding chỉ thực hiện lưu trữ giá trị gốc đầu tiên, và đối với các bản ghi tiếp theo, hệ thống chỉ lưu trữ giá trị khoảng cách chênh lệch (Delta) so với bản ghi ngay trước nó.
  - id: KP10_2
    content: Cơ chế tối ưu hóa số lượng bit nhị phân cần thiết để biểu diễn dữ liệu
    keypoint_weight: 0.4
    description: Đối với các cột dữ liệu như mốc thời gian tăng dần liên tục, khoảng cách chênh lệch (Delta) giữa các dòng thường là các số nguyên có giá trị cực kỳ nhỏ (ví dụ khoảng cách giữa các click chuột chỉ vài mili giây). Hệ thống chỉ cần sử dụng rất ít bit nhị phân (vài bits) để biểu diễn các số Delta nhỏ này thay vì tốn 64-bit (8 bytes) cho mỗi số nguyên ban đầu.
  - id: KP10_3
    content: Kết hợp đồng bộ với các thuật toán nén bit (như Bit-Packing) để triệt tiêu dung lượng thừa
    keypoint_weight: 0.2
    description: Khi các số Delta nhỏ được chuyển đổi, hệ thống áp dụng kỹ thuật đóng gói bit (Bit-Packing) để nén chặt các luồng dữ liệu thô, loại bỏ hoàn toàn các bit 0 vô nghĩa ở đầu dãy nhị phân, giúp giảm thiểu dung lượng lưu trữ trên đĩa cứng đến mức tối đa.