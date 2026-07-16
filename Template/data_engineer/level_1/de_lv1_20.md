# Bộ Câu Hỏi Phỏng Vấn Data Engineer (Level 1)

* **Role:** Data Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong các hệ thống lưu trữ phân tán lớn, kỹ thuật băm dữ liệu (Data Hashing) thường được dùng để phân vùng dữ liệu. Hãy phân biệt điểm khác biệt cơ bản về mặt logic phân bổ dữ liệu giữa cơ chế Modulo Hashing (Băm chia dư) và Consistent Hashing (Băm nhất quán).
* **expected_key_points:**
  - id: KP1_1
    content: Nguyên lý và điểm yếu của Modulo Hashing
    keypoint_weight: 0.5
    description: Sử dụng hàm băm của khóa chia lấy dư cho tổng số lượng node vật lý hiện tại để xác định node lưu trữ. Cơ chế này đơn giản nhưng có điểm yếu chí tử là khi tăng hoặc giảm số lượng node (Scale out/in), hầu như toàn bộ dữ liệu trên hệ thống bị thay đổi giá trị hash chia dư, ép buộc hệ thống phải phân phối, dịch chuyển lại gần như toàn bộ dữ liệu qua mạng (Full Re-sharding), gây nghẽn mạch hệ thống.
  - id: KP1_2
    content: Nguyên lý và ưu điểm của Consistent Hashing
    keypoint_weight: 0.5
    description: Áp dụng việc ánh xạ cả node và khóa dữ liệu lên một vòng tròn băm logic (Hash Ring). Khi số lượng node thay đổi, Consistent Hashing đảm bảo chỉ có một tỷ lệ nhỏ dữ liệu liên quan trực tiếp đến node bị thay đổi là cần phải di chuyển qua mạng sang node khác, phần lớn dữ liệu trên các node còn lại giữ nguyên vị trí, tối ưu hóa băng thông mạng.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Khi lưu trữ dữ liệu lớn trong hồ dữ liệu (Data Lake), hãy phân biệt sự khác biệt cơ bản về mặt cấu trúc tệp tin và trường hợp sử dụng hiệu quả giữa hai định dạng: Apache Avro và Apache Parquet.
* **expected_key_points:**
  - id: KP2_1
    content: Bản chất cấu trúc hướng dòng và ứng dụng của Apache Avro
    keypoint_weight: 0.5
    description: Avro là định dạng lưu trữ dữ liệu hướng dòng (Row-oriented), lưu dưới dạng nhị phân kèm schema dạng JSON đính kèm ở đầu file. Nó tối ưu cho các tác vụ ghi nạp dữ liệu nhanh, liên tục trên toàn bộ các trường của bản ghi (Write-heavy), rất phù hợp cho tầng Message Streaming (như Kafka payload).
  - id: KP2_2
    content: Bản chất cấu trúc hướng cột và ứng dụng của Apache Parquet
    keypoint_weight: 0.5
    description: Parquet là định dạng lưu trữ hướng cột (Columnar-oriented), nén dữ liệu rất chặt theo từng khối cột. Nó tối ưu cho các tác vụ truy vấn đọc phân tích lượng lớn dữ liệu (Read-heavy/Analytical queries) nhờ cơ chế chỉ nạp đúng các cột cần thiết cho việc tính toán, giảm tối đa băng thông I/O đĩa.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế Data Pipeline, công cụ lập lịch và quản lý luồng công việc (Data Orchestration Tool - như Apache Airflow) đóng vai trò gì? Khái niệm DAG (Directed Acyclic Graph) trong Airflow nghĩa là gì?
* **expected_key_points:**
  - id: KP3_1
    content: Vai trò tự động hóa quản lý chuỗi tác vụ của Data Orchestration
    keypoint_weight: 0.5
    description: Công cụ điều phối giúp tự động hóa việc lập lịch chạy, quản lý sự phụ thuộc (Dependencies), giám sát trạng thái hoạt động và xử lý tự động lỗi/retry cho chuỗi các tác vụ ETL/ELT phức tạp di chuyển giữa nhiều hệ thống khác nhau.
  - id: KP3_2
    content: Logic luồng việc không có chu trình của khái niệm DAG
    keypoint_weight: 0.5
    description: DAG (Đồ thị có hướng không chu trình) là một tập hợp các tác vụ (Tasks) được liên kết với nhau theo các mối quan hệ có hướng rõ ràng, quy định thứ tự thực hiện từ trước ra sau, và cam kết cấu trúc luồng chạy không bao giờ bị lặp vòng lặp vô hạn (No loops).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi xây dựng mô hình dữ liệu Dimensional Modeling cho kho dữ liệu (Data Warehouse), kỹ thuật thiết kế bảng "Junk Dimension" là gì và nó giúp giải quyết khuyết điểm gì trong cấu trúc thiết kế bảng Fact?
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
* **Câu hỏi:** Trong Apache Spark, cơ chế tối ưu hóa "Lazy Evaluation" (Đánh giá lười biếng) hoạt động ra sao? Hãy phân biệt sự khác biệt về mặt logic hệ thống giữa các phép toán Transformation và Action.
* **expected_key_points:**
  - id: KP5_1
    content: Nguyên lý xây dựng kế hoạch chạy của Lazy Evaluation
    keypoint_weight: 0.4
    description: Spark không thực thi tính toán vật lý ngay lập tức khi lập trình viên khai báo câu lệnh, mà chỉ ghi nhận các bước xử lý đó vào một sơ đồ kế hoạch logic gọi là DAG. Việc tính toán thực tế chỉ được kích hoạt khi gặp một lệnh Action.
  - id: KP5_2
    content: Logic không sinh dữ liệu vật lý của Transformation
    keypoint_weight: 0.3
    description: Transformation là các phép toán biến đổi dữ liệu (như map, filter, join) dùng để xây dựng nên DAG kế hoạch logic và luôn trả về một DataFrame/RDD mới mà không làm phát sinh chi phí tính toán trên RAM/Đĩa.
  - id: KP5_3
    content: Logic kích hoạt luồng xử lý thực tế của Action
    keypoint_weight: 0.3
    description: Action là các phép toán yêu cầu trả kết quả đầu ra về cho Driver Node hoặc ghi dữ liệu xuống đĩa (như collect, count, write). Khi Action được gọi, Spark Catalyst Optimizer mới tối ưu hóa DAG và đẩy Tasks vật lý xuống các Executor để chạy.

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
    description: Giải quyết lỗi bị trùng lặp dữ liệu (Duplicate) của phép toán Append khi chạy lại pipeline, đồng thời loại bỏ chi phí tài nguyên khổng lồ của phép toán Overwrite (phải xóa đi ghi lại toàn bộ bảng cũ không đổi), giúp pipeline đạt tính lũy đẳng (Idempotency).

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
* **Câu hỏi:** Trong tính toán dữ liệu phân tán (như Apache Spark), hiện tượng "Data Skew" (Lệch dữ liệu) là gì? Hiện tượng này gây ra hậu quả hiệu năng tiêu cực nào và phương pháp xử lý cơ bản bằng kỹ thuật nhiễu muối (Salting) ở mức mã nguồn là gì?
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất phân bổ dữ liệu không đồng đều giữa các Partitions
    keypoint_weight: 0.4
    description: Data Skew xảy ra khi một số ít phân vùng (Partitions) chứa lượng dữ liệu khổng lồ vượt trội so với phần còn lại, thường do khóa phân vùng (Partition Key) bị trùng lặp quá nhiều giá trị (như khóa NULL hoặc mã ID mặc định chiếm đa số).
  - id: KP8_2
    content: Gây thắt nút cổ chai hiệu năng hệ thống (Straggler Tasks)
    keypoint_weight: 0.3
    description: Trong tính toán phân tán, một Stage chỉ kết thúc khi Task cuối cùng chạy xong. Node nhận phân vùng bị lệch sẽ phải xử lý dữ liệu lâu hơn rất nhiều, làm treo tài nguyên của cả cụm (Straggler) hoặc gây lỗi tràn bộ nhớ (Out Of Memory - OOM) trong khi các node khác đã rảnh rỗi.
  - id: KP8_3
    content: Nguyên lý giải quyết bằng kỹ thuật Salting khóa
    keypoint_weight: 0.3
    description: Áp dụng kỹ thuật Salting bằng cách thêm một hậu tố số ngẫu nhiên (ví dụ từ 1 đến N) vào sau khóa bị lệch để băm nhỏ và phân tán dữ liệu của khóa đó đều ra các phân vùng khác nhau, cho phép các Worker node tính toán song song, loại bỏ hiện tượng nghẽn.

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