# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 4) - Tập Đề Hybrid Retrieval và GraphRAG (9)

* **Role:** AI Engineer
* **Level:** Level 4
* **Experience:** 6 - 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Cơ sở dữ liệu Vector (Vector Database) là gì? Hãy nêu sự khác biệt lớn nhất giữa Vector DB và cơ sở dữ liệu quan hệ (SQL Database) truyền thống.
* **expected_key_points:**
  - id: KP1_1
    content: Khái niệm Vector Database
    keypoint_weight: 0.5
    description: Là hệ cơ sở dữ liệu được tối ưu hóa riêng để lưu trữ, lập chỉ mục và truy vấn nhanh các vector số thực đa chiều (embeddings) đại diện cho dữ liệu phi cấu trúc.
  - id: KP1_2
    content: Sự khác biệt cốt lõi về cách truy vấn
    keypoint_weight: 0.5
    description: SQL DB truy vấn dựa trên khớp chính xác các giá trị cột hoặc khóa ngoại (exact match/structured query). Vector DB truy vấn dựa trên độ tương đồng khoảng cách toán học giữa các vector (similarity search/ANN) để tìm kết quả gần đúng nhất.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong hệ thống RAG, kỹ thuật chia nhỏ tài liệu (Chunking) là gì? Nêu sự khác nhau giữa hai chiến lược: Fixed-size Chunking và Semantic Chunking.
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa Chunking
    keypoint_weight: 0.4
    description: Là quá trình chia nhỏ các văn bản dài thành các đoạn văn ngắn hơn (chunks) để vừa với cửa sổ ngữ cảnh của mô hình embedding và LLM.
  - id: KP2_2
    content: Fixed-size vs Semantic Chunking
    keypoint_weight: 0.6
    description: Fixed-size chunking chia văn bản theo số lượng ký tự/tokens cố định (có thể có overlap). Semantic chunking phân tích ngữ nghĩa của văn bản để chia đoạn tại các ranh giới tự nhiên (như xuống dòng, chuyển ý, kết thúc đoạn văn) giúp bảo toàn ngữ cảnh tốt hơn.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Mô hình nhúng (Embedding Model) đóng vai trò gì trong hệ thống tìm kiếm ngữ nghĩa? Hãy nêu 2 tiêu chí quan trọng để bạn lựa chọn một mô hình embedding phù hợp.
* **expected_key_points:**
  - id: KP3_1
    content: Vai trò của mô hình Embedding
    keypoint_weight: 0.5
    description: Chuyển đổi dữ liệu văn bản/ảnh thành các vector số thực mật độ cao, ánh xạ các từ/câu có nghĩa giống nhau vào các vị trí gần nhau trong không gian vector.
  - id: KP3_2
    content: Tiêu chí lựa chọn mô hình
    keypoint_weight: 0.5
    description: Nêu được 2 tiêu chí: Số chiều vector đầu ra (dimension), giới hạn độ dài context (context window), hiệu năng trên bảng xếp hạng (MTEB leaderboard), hoặc độ tương thích ngôn ngữ tiếng Việt.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế hoạt động của Tìm kiếm kết hợp (Hybrid Search) giữa BM25 và Dense Vector Search. Tại sao kết hợp này lại mang lại độ chính xác cao hơn?
* **expected_key_points:**
  - id: KP4_1
    content: Nguyên lý BM25 vs Dense Vector Search
    keypoint_weight: 0.5
    description: BM25 là thuật toán tìm kiếm từ khóa dựa trên tần suất xuất hiện từ trong tài liệu (sparse retrieval). Dense Vector Search tìm kiếm dựa trên ngữ nghĩa của câu (dense retrieval).
  - id: KP4_2
    content: Cơ chế gộp kết quả (Reciprocal Rank Fusion - RRF)
    keypoint_weight: 0.5
    description: Hybrid Search gộp danh sách kết quả từ 2 phương pháp bằng thuật toán RRF hoặc chấm điểm có trọng số, giúp bổ sung ưu thế cho nhau: bắt chính xác các từ khóa đặc biệt (mã sản phẩm, tên riêng) nhờ BM25 và hiểu ngữ cảnh sâu nhờ Dense Vector.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày vai trò và cơ chế hoạt động của mô hình xếp hạng lại (Re-ranking Model) trong pipeline RAG. Nó giúp cải thiện chất lượng câu trả lời của LLM như thế nào?
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế hoạt động của Reranker (Cross-Encoder)
    keypoint_weight: 0.6
    description: Giai đoạn 1 (Retrieval) dùng mô hình Bi-Encoder tìm nhanh 100 tài liệu. Giai đoạn 2 (Re-ranking) dùng Cross-Encoder phân tích đồng thời câu hỏi và từng tài liệu để tính điểm liên quan chi tiết hơn, sắp xếp lại thứ tự từ cao xuống thấp.
  - id: KP5_2
    content: Cải thiện chất lượng RAG
    keypoint_weight: 0.4
    description: Đảm bảo các tài liệu liên quan nhất luôn nằm ở đầu danh sách gửi cho LLM, hạn chế việc LLM bị trôi thông tin ở giữa ngữ cảnh (lost in the middle) và giảm nhiễu thông tin không liên quan.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh hai cấu trúc chỉ mục tìm kiếm ANN trên Vector DB: HNSW (Hierarchical Navigable Small World) và IVF-PQ (Inverted File with Product Quantization) về độ chính xác, tốc độ truy vấn, và dung lượng RAM yêu cầu.
* **expected_key_points:**
  - id: KP6_1
    content: Đặc trưng chỉ mục HNSW
    keypoint_weight: 0.5
    description: HNSW xây dựng cấu trúc đồ thị nhiều tầng. Tốc độ tìm kiếm cực nhanh, độ chính xác cao, nhưng tiêu tốn lượng RAM rất lớn để lưu đồ thị chỉ mục.
  - id: KP6_2
    content: Đặc trưng chỉ mục IVF-PQ
    keypoint_weight: 0.5
    description: IVF-PQ phân cụm không gian vector (IVF) và lượng tử hóa nén kích thước vector (PQ). Yêu cầu dung lượng RAM cực nhỏ (tiết kiệm đến 90%), phù hợp cho tập dữ liệu khổng lồ, nhưng tốc độ tìm kiếm chậm hơn và độ chính xác thấp hơn HNSW.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cách bạn tối ưu hóa prompt gửi lên LLM trong hệ thống RAG sử dụng kỹ thuật nén prompt (Prompt Compression). Kỹ thuật này giải quyết vấn đề gì?
* **expected_key_points:**
  - id: KP7_1
    content: Vấn đề của prompt dài trong RAG
    keypoint_weight: 0.4
    description: Tài liệu RAG đính kèm làm prompt dài, tăng chi phí API (token cost), làm tăng thời gian phản hồi (latency), và làm LLM dễ bị nhiễu thông tin.
  - id: KP7_2
    content: Cơ chế của Prompt Compression (ví dụ LLMLingua)
    keypoint_weight: 0.6
    description: Sử dụng một mô hình ngôn ngữ nhỏ (như GPT-2/Llama-3-small) để tính toán độ hỗn loạn (perplexity) của các từ trong prompt. Loại bỏ các từ có độ hỗn loạn thấp (từ dư thừa, mang ít thông tin ngữ nghĩa) để nén prompt ngắn lại tới 20-50% mà vẫn giữ nguyên ý nghĩa câu trả lời sinh ra từ LLM.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống RAG tra cứu báo cáo tài chính nội bộ cho doanh nghiệp lớn. Hệ thống phải đảm bảo trích xuất chính xác 100% dữ liệu số và bảng biểu phức tạp trong tài liệu.
* **expected_key_points:**
  - id: KP8_1
    content: Pipeline trích xuất và cấu trúc hóa bảng biểu (Table Parsing)
    keypoint_weight: 0.5
    description: Sử dụng mô hình chuyên biệt để phát hiện bảng biểu (như Table Transformer) -> trích xuất nội dung bảng thành định dạng HTML/Markdown để giữ nguyên cấu trúc dòng cột -> lưu trữ bảng dưới dạng các node riêng biệt liên kết với ngữ cảnh xung quanh.
  - id: KP8_2
    content: Cơ chế tìm kiếm bảng biểu nâng cao (Table Retrieval)
    keypoint_weight: 0.5
    description: Sử dụng kỹ thuật Summary-based Retrieval: sinh tóm tắt chi tiết cho mỗi bảng, nhúng vector phần tóm tắt để tìm kiếm. Khi truy vấn trúng, gửi toàn bộ bảng HTML/Markdown làm ngữ cảnh cho LLM; kết hợp công cụ lập trình Python (Code Interpreter) để LLM tự viết code tính toán lại các số liệu trên bảng tránh tính nhẩm sai.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế một pipeline cập nhật cơ sở dữ liệu Vector thời gian thực (Real-time Vector DB Update Pipeline) khi các tài liệu nguồn (như cơ sở tri thức Notion/Confluence) thay đổi liên tục.
* **expected_key_points:**
  - id: KP9_1
    content: Kiến trúc sự kiện (Event-driven CDC Pipeline)
    keypoint_weight: 0.6
    description: Thiết lập hệ thống Change Data Capture (CDC - như Debezium) hoặc Webhooks lắng nghe sự thay đổi tài liệu -> gửi event thay đổi (Create/Update/Delete) vào hàng đợi Kafka -> Flink/Spark Streaming xử lý phân mảnh tài liệu (chunking).
  - id: KP9_2
    content: Quản lý Document-Chunk Mapping và cập nhật DB
    keypoint_weight: 0.4
    description: Lưu trữ ánh xạ giữa ID tài liệu gốc và danh sách IDs của các chunks tương ứng trong một DB trung gian (ví dụ PostgreSQL). Khi nhận event UPDATE tài liệu: xóa tất cả chunks cũ trên Vector DB bằng IDs đã lưu, sinh chunks mới, nhúng vector và ghi đè lại vào Vector DB.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống GraphRAG kết hợp Vector Search và đồ thị tri thức (Knowledge Graph) để giải quyết các truy vấn mang tính tổng quan toàn cục (Global Queries - ví dụ: 'Nêu các chủ đề chính của cuốn sách').
* **expected_key_points:**
  - id: KP10_1
    content: Xây dựng Đồ thị Tri thức (Knowledge Graph Construction)
    keypoint_weight: 0.5
    description: Sử dụng LLM trích xuất các Thực thể (Entities) và Mối quan hệ (Relationships) từ các chunks tài liệu để xây dựng đồ thị; sử dụng thuật toán phân cụm đồ thị (như Leiden algorithm) để nhóm các thực thể liên quan chặt chẽ thành các cộng đồng (communities).
  - id: KP10_2
    content: Quy trình truy vấn toàn cục (Global Query Pipeline)
    keypoint_weight: 0.5
    description: Sử dụng LLM để sinh báo cáo tóm tắt (community summaries) cho mỗi cộng đồng thực thể -> Khi nhận câu hỏi toàn cục, LLM đọc song song tất cả các báo cáo cộng đồng để trích xuất câu trả lời cục bộ -> Gộp các câu trả lời lại một lần nữa để trả về kết quả tổng hợp đầy đủ ngữ cảnh.

