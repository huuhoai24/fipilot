# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 4) - Tập Đề Vector Search và GraphRAG (13)

* **Role:** AI Engineer
* **Level:** Level 4
* **Experience:** 6 - 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh cơ chế tìm kiếm BM25 (Sparse Retrieval) và Dense Vector Search (Dense Retrieval) trong bài toán tìm kiếm ngữ nghĩa.
* **expected_key_points:**
  - id: KP1_1
    content: Nguyên lý BM25 vs Dense Vector
    keypoint_weight: 0.5
    description: BM25 dựa trên tần suất xuất hiện từ khóa chính xác trong tài liệu (TF-IDF cải tiến). Dense Vector Search chuyển câu thành vector liên tục và so sánh khoảng cách ngữ nghĩa.
  - id: KP1_2
    content: Trường hợp áp dụng tối ưu
    keypoint_weight: 0.5
    description: BM25 tối ưu khi tìm tên riêng, mã sản phẩm, thuật ngữ kỹ thuật chính xác. Dense Vector Search tối ưu khi câu hỏi diễn đạt khác từ khóa nhưng cùng ý nghĩa.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày các chiến lược chia nhỏ tài liệu (Chunking) trong RAG: Phân biệt Character-based, Token-based, và Semantic Chunking.
* **expected_key_points:**
  - id: KP2_1
    content: Character-based vs Token-based Chunking
    keypoint_weight: 0.5
    description: Character-based chia theo số lượng ký tự cố định. Token-based chia theo số lượng tokens của mô hình embedding, đảm bảo không bị lỗi tràn giới hạn token.
  - id: KP2_2
    content: Đặc trưng Semantic Chunking
    keypoint_weight: 0.5
    description: Phân tích ngữ nghĩa của câu, tính toán khoảng cách vector giữa các câu liên tiếp để chia đoạn tại các vị trí có sự thay đổi nội dung đột ngột, giúp giữ trọn ngữ cảnh.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Ý nghĩa của bước xếp hạng lại (Reranking) trong RAG pipeline là gì? Phân biệt sự khác nhau giữa mô hình Cross-Encoder và Bi-Encoder.
* **expected_key_points:**
  - id: KP3_1
    content: Vai trò của Reranking
    keypoint_weight: 0.4
    description: Sử dụng mô hình chính xác hơn để sắp xếp lại danh sách tài liệu tìm kiếm được từ bước Retrieval, đảm bảo tài liệu liên quan nhất nằm ở đầu ngữ cảnh gửi LLM.
  - id: KP3_2
    content: Cross-Encoder vs Bi-Encoder
    keypoint_weight: 0.6
    description: Bi-Encoder nhúng độc lập câu hỏi và tài liệu thành 2 vector riêng biệt rồi tính dot product (nhanh, dùng cho retrieval). Cross-Encoder nhận đồng thời cả câu hỏi và tài liệu vào mạng nơ-ron cùng lúc để học quan hệ chéo (chậm, chính xác cao, dùng cho reranking).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cấu trúc đồ thị HNSW (Hierarchical Navigable Small World). Các siêu tham số M, ef_construction, và ef_search ảnh hưởng thế nào đến độ chính xác và tốc độ truy vấn?
* **expected_key_points:**
  - id: KP4_1
    content: Cấu trúc đồ thị phân tầng của HNSW
    keypoint_weight: 0.5
    description: Xây dựng đồ thị nhiều tầng dạng skip-list. Tầng trên liên kết thưa để duyệt nhanh khoảng cách lớn, tầng dưới liên kết dày để tìm kiếm chính xác cục bộ.
  - id: KP4_2
    content: Vai trò của các siêu tham số
    keypoint_weight: 0.5
    description: $M$ là số lượng kết nối tối đa của mỗi nút trên đồ thị. $ef\_construction$ kiểm soát độ chính xác khi build đồ thị. $ef\_search$ kiểm soát số lượng nút duyệt qua khi tìm kiếm; tăng $ef\_search$ giúp tăng độ chính xác nhưng tăng latency truy vấn.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích kỹ thuật nén Product Quantization (PQ) giúp tiết kiệm bộ nhớ RAM trong Vector Database. Giải thích cơ chế Asymmetric Distance Computation (ADC).
* **expected_key_points:**
  - id: KP5_1
    content: Nguyên lý nén Product Quantization (PQ)
    keypoint_weight: 0.5
    description: Chia không gian vector gốc thành $m$ không gian con độc lập. Thực hiện phân cụm K-Means trên từng không gian con để tìm ra tâm cụm. Mỗi vector được lưu dưới dạng chuỗi $m$ chỉ mục của các tâm cụm này, giảm dung lượng RAM đến 90%.
  - id: KP5_2
    content: Cơ chế Asymmetric Distance Computation (ADC)
    keypoint_weight: 0.5
    description: Khi tính khoảng cách giữa query (dạng vector thực đầy đủ) và vector trong DB (đã nén), ADC tính khoảng cách trực tiếp từ query tới các tâm cụm mà không cần giải nén vector trong DB, tăng tốc độ tính toán.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế giải pháp Tìm kiếm kết hợp (Hybrid Search) giữa BM25 và Vector Search dùng thuật toán Reciprocal Rank Fusion (RRF). Viết công thức RRF và giải thích ý nghĩa.
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên lý hoạt động và công thức RRF
    keypoint_weight: 0.6
    description: Công thức: $RRF\_Score(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$ với $r_m(d)$ là thứ hạng của tài liệu $d$ trong danh sách kết quả của phương pháp tìm kiếm $m$, $k$ là hằng số smoothing (thường bằng 60).
  - id: KP6_2
    content: Lợi thế của RRF
    keypoint_weight: 0.4
    description: RRF không phụ thuộc vào dải điểm số (scores) khác nhau của BM25 và Vector Search; gộp kết quả dựa trên thứ hạng giúp hệ thống ổn định và bắt tốt cả từ khóa lẫn ngữ nghĩa.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cách tối ưu hóa prompt gửi lên LLM trong hệ thống RAG sử dụng kỹ thuật nén prompt (Prompt Compression). Kỹ thuật này giải quyết vấn đề gì?
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
* **Câu hỏi:** Thiết kế kiến trúc hệ thống GraphRAG kết hợp đồ thị tri thức (Knowledge Graph) và Vector DB để giải quyết các truy vấn mang tính tổng quan toàn cục (Global Queries - ví dụ: 'Nêu các chủ đề chính của cuốn sách').
* **expected_key_points:**
  - id: KP8_1
    content: Xây dựng Đồ thị Tri thức (Knowledge Graph Construction)
    keypoint_weight: 0.5
    description: Sử dụng LLM trích xuất các Thực thể (Entities) và Mối quan hệ (Relationships) từ các chunks tài liệu để xây dựng đồ thị; sử dụng thuật toán phân cụm đồ thị (như Leiden algorithm) để nhóm các thực thể liên quan chặt chẽ thành các cộng đồng (communities).
  - id: KP8_2
    content: Quy trình truy vấn toàn cục (Global Query Pipeline)
    keypoint_weight: 0.5
    description: Sử dụng LLM để sinh báo cáo tóm tắt (community summaries) cho mỗi cộng đồng thực thể -> Khi nhận câu hỏi toàn cục, LLM đọc song song tất cả các báo cáo cộng đồng để trích xuất câu trả lời cục bộ -> Gộp các câu trả lời lại một lần nữa để trả về kết quả tổng hợp đầy đủ ngữ cảnh.

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
* **Câu hỏi:** Thiết kế hệ thống RAG tra cứu báo cáo tài chính nội bộ cho doanh nghiệp lớn. Hệ thống phải đảm bảo trích xuất chính xác 100% dữ liệu số và bảng biểu phức tạp trong tài liệu.
* **expected_key_points:**
  - id: KP10_1
    content: Pipeline trích xuất và cấu trúc hóa bảng biểu (Table Parsing)
    keypoint_weight: 0.5
    description: Sử dụng mô hình chuyên biệt để phát hiện bảng biểu (như Table Transformer) -> trích xuất nội dung bảng thành định dạng HTML/Markdown để giữ nguyên cấu trúc dòng cột -> lưu trữ bảng dưới dạng các node riêng biệt liên kết với ngữ cảnh xung quanh.
  - id: KP10_2
    content: Cơ chế tìm kiếm bảng biểu nâng cao (Table Retrieval)
    keypoint_weight: 0.5
    description: Sử dụng kỹ thuật Summary-based Retrieval: sinh tóm tắt chi tiết cho mỗi bảng, nhúng vector phần tóm tắt để tìm kiếm. Khi truy vấn trúng, gửi toàn bộ bảng HTML/Markdown làm ngữ cảnh cho LLM; kết hợp công cụ lập trình Python (Code Interpreter) để LLM tự viết code tính toán lại các số liệu trên bảng tránh tính nhẩm sai.

