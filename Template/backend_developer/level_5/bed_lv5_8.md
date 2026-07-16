# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 5) - Tập Đề Elasticsearch Indexing và ILM (8)

* **Role:** Backend Developer
* **Level:** Level 5
* **Experience:** Trên 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Elasticsearch là gì? Hãy so sánh sự khác nhau về nguyên lý cấu trúc dữ liệu và khả năng tìm kiếm văn bản giữa Inverted Index của Elasticsearch và B-Tree Index của cơ sở dữ liệu quan hệ.
* **expected_key_points:**
  - id: KP1_1
    content: Bản chất Inverted Index vs B-Tree
    keypoint_weight: 0.5
    description: B-Tree sắp xếp khóa tìm kiếm theo thứ tự cây cân bằng, duyệt tuần tự để tìm kiếm. Inverted Index phân tách văn bản thành các từ tố (tokens) độc lập và lập bản đồ ánh xạ từ mỗi từ tố tới danh sách các tài liệu chứa từ đó.
  - id: KP1_2
    content: Khả năng tìm kiếm văn bản
    keypoint_weight: 0.5
    description: B-Tree tìm kiếm văn bản rất chậm (phép `LIKE '%text%'` phải quét toàn bộ bảng). Inverted Index cho phép tìm kiếm văn bản toàn văn (full-text search) cực nhanh chỉ trong vài mili-giây, bất kể dung lượng tài liệu.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích khái niệm Shards và Replicas trong Elasticsearch. Tại sao việc thiết lập số lượng shards quá lớn hoặc quá nhỏ đều ảnh hưởng nghiêm trọng đến hiệu năng hệ thống?
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm Shards và Replicas
    keypoint_weight: 0.5
    description: Shards là các phân mảnh dữ liệu vật lý chứa một phần chỉ mục Lucene. Replicas là các bản sao của Shards dùng để dự phòng lỗi và tăng tốc độ đọc.
  - id: KP2_2
    content: Tác động đến hiệu năng
    keypoint_weight: 0.5
    description: Quá nhiều shards gây lãng phí overhead quản lý bộ nhớ của JVM. Quá ít shards làm kích thước một shard quá lớn (>50GB), gây chậm chạp khi di chuyển dữ liệu giữa các node và khó tận dụng sức mạnh tính toán song song.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau về cơ chế so khớp văn bản và tính điểm liên quan giữa Term Query và Match Query trong Elasticsearch.
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế Term Query
    keypoint_weight: 0.5
    description: Term Query thực hiện so khớp chính xác giá trị nhập vào với giá trị lưu trong chỉ mục (không qua phân tích từ tố), phù hợp cho các dữ liệu khóa như ID, Email, Category.
  - id: KP3_2
    content: Cơ chế Match Query
    keypoint_weight: 0.5
    description: Match Query đưa chuỗi nhập vào qua bộ phân tích (Analyzer) để chia nhỏ từ tố -> thực hiện so khớp ngữ nghĩa trên từng từ tố và tính điểm liên quan (TF-IDF/BM25) để trả kết quả.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế pipeline thu thập và lưu trữ log tập trung quy mô lớn sử dụng kiến trúc ELK/EFK Stack kết hợp hàng đợi Apache Kafka làm bộ đệm chống tràn.
* **expected_key_points:**
  - id: KP4_1
    content: Vai trò của Log Agent và Kafka buffer
    keypoint_weight: 0.5
    description: Log Agents (Filebeat) đọc file log từ các server -> đẩy nhanh vào Kafka để giải phóng đĩa cứng. Kafka đóng vai trò bộ đệm (buffer) hấp thụ tải đột biến, tránh làm sập Elasticsearch.
  - id: KP4_2
    content: Logstash parsing và Ghi vào Elasticsearch
    keypoint_weight: 0.5
    description: Logstash tiêu thụ dữ liệu từ Kafka -> thực hiện phân tích cú pháp (Grok parser) cấu trúc hóa log -> ghi song song vào cụm Elasticsearch phân mảnh hợp lý.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế giải pháp xếp hạng kết quả tìm kiếm (Relevance Scoring) tùy chỉnh trong Elasticsearch bằng cách sử dụng các hàm Function Score và Boosting.
* **expected_key_points:**
  - id: KP5_1
    content: Sử dụng Function Score
    keypoint_weight: 0.5
    description: Sử dụng `function_score` để nhân/cộng điểm cơ bản BM25 với các tiêu chí kinh doanh khác như: độ mới của bài viết (decay function), số lượng xem (field value factor).
  - id: KP5_2
    content: Kỹ thuật Boosting
    keypoint_weight: 0.5
    description: Áp dụng Boosting để ưu tiên nâng điểm cho các tài liệu khớp tiêu đề chính xác cao hơn là khớp nội dung; phạt điểm các tài liệu chứa spam hoặc hết hàng.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích hiện tượng Split-brain trong cụm Elasticsearch. Nguyên nhân xảy ra là gì và làm thế nào để cấu hình ngăn chặn nó ở các phiên bản mới?
* **expected_key_points:**
  - id: KP6_1
    content: Bản chất Split-brain trong Elasticsearch
    keypoint_weight: 0.5
    description: Xảy ra khi đứt mạng giữa các node làm cụm bị chia làm 2 phần. Mỗi bên tự bầu ra một Master node riêng, làm cụm bị phân rã trạng thái dữ liệu (mất nhất quán).
  - id: KP6_2
    content: Ngăn chặn bằng cấu hình Quorum Master
    keypoint_weight: 0.5
    description: Cấu hình `cluster.initial_master_nodes` thiết lập danh sách master-eligible nodes cố định; thuật toán bầu cử mới trong ES 7.x+ tự động yêu cầu sự đồng ý của đa số nodes (Quorum) để duy trì master, ngăn chặn triệt để split-brain.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế phân tích từ tố (Analysis Pipeline) trong Elasticsearch khi xử lý văn bản đa ngôn ngữ, bao gồm Character Filters, Tokenizer, và Token Filters.
* **expected_key_points:**
  - id: KP7_1
    content: Ba thành phần của Analyzer
    keypoint_weight: 0.6
    description: Character Filters: làm sạch văn bản thô (loại bỏ thẻ HTML). Tokenizer: chia văn bản thành các từ tố (ví dụ chia theo khoảng trắng). Token Filters: biến đổi từ tố (chuyển chữ thường, loại bỏ stop words, đưa từ về nguyên gốc - stemming).
  - id: KP7_2
    content: Xử lý đa ngôn ngữ
    keypoint_weight: 0.4
    description: Sử dụng các analyzer chuyên biệt cho từng ngôn ngữ (như ICU Analyzer cho ngôn ngữ phức tạp, Vi_analyzer cho tiếng Việt để ghép từ ghép).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống tìm kiếm sản phẩm thương mại điện tử quy mô 100 triệu sản phẩm hỗ trợ tìm kiếm mờ (fuzzy search), gợi ý tự động (auto-suggest), tìm kiếm theo danh mục (faceted search) dưới 30ms.
* **expected_key_points:**
  - id: KP8_1
    content: Thiết kế Mapping Index tối ưu và Auto-suggest
    keypoint_weight: 0.5
    description: Sử dụng kiểu dữ liệu `completion suggester` cho auto-suggest thời gian thực; áp dụng kỹ thuật N-gram và Edge N-gram để phân tích từ tố hỗ trợ tìm kiếm nhanh từ một phần chữ đang gõ.
  - id: KP8_2
    content: Faceted Search và Caching
    keypoint_weight: 0.5
    description: Sử dụng Elasticsearch Aggregations để phân tích động các thuộc tính sản phẩm (giá, thương hiệu); cấu hình Elasticsearch Shard Request Cache và Node Query Cache để đạt tốc độ phản hồi < 30ms chịu tải hàng vạn rps.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế pipeline cập nhật Elasticsearch index thời gian thực (Real-time Indexing Pipeline) từ cơ sở dữ liệu chính PostgreSQL chịu tải ghi cực lớn mà không gây ảnh hưởng đến hiệu năng đọc của người dùng.
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế CDC qua Debezium và Kafka
    keypoint_weight: 0.5
    description: Lắng nghe sự thay đổi của PostgreSQL qua WAL sử dụng Debezium -> đẩy các events thay đổi vào Kafka. Thiết lập cơ chế gộp lô ghi (Bulk Indexing) của Elasticsearch consumer.
  - id: KP9_2
    content: Kiến trúc Alias và Zero-downtime Reindexing
    keypoint_weight: 0.5
    description: Sử dụng Elasticsearch Index Alias để trỏ ứng dụng đọc sang chỉ mục hiện tại; khi cần cập nhật lớn, tạo index mới chạy nền để reindex rồi tráo đổi alias nhanh, tránh làm ảnh hưởng đến luồng đọc.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống phân tích nhật ký (Log Analytics) khổng lồ xử lý hàng chục Terabytes logs mỗi ngày sử dụng Elasticsearch Rollover Index, Index Lifecycle Management (ILM) và phân tầng lưu trữ (Hot-Warm-Cold).
* **expected_key_points:**
  - id: KP10_1
    content: Phân tầng lưu trữ Hot-Warm-Cold
    keypoint_weight: 0.5
    description: Hot tier dùng các GPU/SSD tốc độ cao chuyên cho ghi log và tìm kiếm log mới. Warm tier dùng các đĩa chậm hơn chứa log trung hạn ít ghi. Cold tier lưu trữ dạng nén chỉ đọc phục vụ audit.
  - id: KP10_2
    content: Chính sách Rollover và ILM
    keypoint_weight: 0.5
    description: Thiết lập chính sách tự động Rollover index khi kích thước vượt quá 50GB hoặc thọ quá 1 ngày; dùng ILM tự động chuyển index từ Hot -> Warm -> Cold -> Delete theo thời gian quy định.

