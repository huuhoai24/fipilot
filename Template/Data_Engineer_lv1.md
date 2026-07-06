# Bộ Câu Hỏi Phỏng Vấn Data Engineer (Level 1)

* **Role:** Data Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong quy trình ETL truyền thống, ba chữ cái E, T, L là viết tắt của các từ nào và nhiệm vụ cốt lõi của từng bước là gì?
* **Đáp án mẫu:** - E (Extract): Trích xuất dữ liệu từ các nguồn khác nhau (Database, API, File thô).
  - T (Transform): Biến đổi dữ liệu (làm sạch, chuẩn hóa, tính toán, định dạng lại) cho phù hợp với yêu cầu nghiệp vụ.
  - L (Load): Ghi/Nạp dữ liệu đã biến đổi vào hệ thống lưu trữ đích (như Data Warehouse).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau cơ bản về mục đích sử dụng giữa Data Warehouse (Kho dữ liệu) và Data Lake (Hồ dữ liệu).
* **Đáp án mẫu:** - Data Warehouse: Lưu trữ dữ liệu đã qua xử lý, có cấu trúc rõ ràng (Structured), phục vụ chủ yếu cho việc làm báo cáo BI và phân tích định kỳ.
  - Data Lake: Lưu trữ dữ liệu thô ở mọi định dạng (Structured, Semi-structured, Unstructured) với khối lượng lớn, phục vụ cho khai phá dữ liệu và Data Science.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong SQL, sự khác biệt về kết quả trả về giữa hai phép toán `INNER JOIN` và `LEFT JOIN` là gì?
* **Đáp án mẫu:** - `INNER JOIN`: Chỉ trả về các bản ghi có giá trị trùng khớp xuất hiện ở cả hai bảng.
  - `LEFT JOIN`: Trá về toàn bộ các bản ghi từ bảng bên trái và các bản ghi trùng khớp từ bảng bên phải; các vị trí không có dữ liệu trùng khớp ở bảng bên phải sẽ được điền giá trị `NULL`.

---

## CÂU HỎI TRUNG BÌNH (4 câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong các hệ thống Big Data, cơ chế phân tán dữ liệu "Sharding" và "Replication" khác nhau như thế nào về mục đích?
* **Đáp án mẫu:** - Sharding: Chia nhỏ một tập dữ liệu lớn thành các phần nhỏ hơn (shards) và lưu trữ rải rác trên nhiều máy chủ để tăng hiệu năng xử lý ghi/đọc (mở rộng theo chiều ngang).
  - Replication: Sao chép cùng một tập dữ liệu ra nhiều bản để lưu trữ trên nhiều máy chủ khác nhau nhằm đảm bảo tính sẵn sàng cao (High Availability) và khả năng chịu lỗi (Fault Tolerance) khi có máy chủ bị hỏng.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Định dạng lưu trữ tệp tin dạng dòng (Row-oriented như CSV, JSON) và dạng cột (Columnar như Parquet, ORC) có ưu thế khác nhau thế nào khi thực hiện truy vấn dữ liệu?
* **Đáp án mẫu:** - Dạng dòng (Row-oriented): Tối ưu cho các tác vụ ghi dữ liệu liên tục hoặc truy vấn lấy ra toàn bộ thông tin của một vài bản ghi cụ thể.
  - Dạng cột (Columnar): Tối ưu cho các truy vấn phân tích tổng hợp (như `SUM`, `AVG`, `COUNT` trên một vài cột cụ thể) vì hệ thống chỉ cần đọc đúng các cột đó mà không phải quét qua toàn bộ các cột khác, giúp giảm IO và tăng tốc độ xử lý.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy phân biệt sự khác nhau giữa Batch Processing (Xử lý theo lô) và Stream Processing (Xử lý luồng/thời gian thực). Cho ví dụ về công cụ phổ biến cho mỗi loại.
* **Đáp án mẫu:** - Batch Processing: Xử lý một lượng lớn dữ liệu tích tụ lại sau một khoảng thời gian cố định (độ trễ cao). Ví dụ công cụ: Apache Spark, AWS EMR.
  - Stream Processing: Xử lý dữ liệu liên tục, ngay lập tức khi dữ liệu vừa mới phát sinh (độ trễ cực thấp). Ví dụ công cụ: Apache Kafka, Apache Flink, Apache Spark Streaming.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Công cụ quản lý luồng công việc (Workflow Orchestration) như Apache Airflow đảm nhận vai trò gì trong một kiến trúc dữ liệu hiện đại?
* **Đáp án mẫu:** Apache Airflow đảm nhận vai trò lập lịch (Scheduling), điều phối và giám sát các pipeline dữ liệu dưới dạng đồ thị có hướng không chu trình (DAG). Nó giúp tự động hóa thứ tự chạy của các tác vụ, quản lý các kết nối, xử lý lỗi (retry) và gửi cảnh báo khi pipeline gặp sự cố.

---

## CÂU HỎI KHÓ (3 câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Khi thiết kế Data Warehouse theo mô hình Dimensional Modeling, bảng Sự kiện (Fact Table) và bảng Chiều (Dimension Table) khác nhau như thế nào? Nêu mối quan hệ kết nối giữa chúng trong sơ đồ Star Schema.
* **Đáp án mẫu:** - Fact Table: Chứa các chỉ số định lượng có thể đo lường được (metrics/measures như doanh số, số lượng) và các khóa ngoại liên kết tới các bảng chiều.
  - Dimension Table: Chứa các thuộc tính văn bản mô tả bối cảnh của sự kiện (như thông tin khách hàng, sản phẩm, thời gian).
  - Trong Star Schema: Fact Table nằm ở trung tâm và kết nối trực tiếp với các Dimension Table xung quanh thông qua mối quan hệ khóa chính - khóa ngoại (mô hình 1-nhiều).

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong tính toán phân tán với Apache Spark, sự khác biệt giữa hai loại thao tác "Transformation" và "Action" là gì? Cơ chế "Lazy Evaluation" hoạt động như thế nào dựa trên hai thao tác này?
* **Đáp án mẫu:** - Transformation: Tạo ra một RDD/DataFrame mới từ một RDD/DataFrame cũ (như `map`, `filter`, `groupBy`).
  - Action: Thực thi tính toán để trả về kết quả cho Driver program hoặc ghi dữ liệu ra bộ lưu trữ ngoại vi (như `count