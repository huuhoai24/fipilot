# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 5) - Tập Đề GraphSAGE và Knowledge Graph QA (18)

* **Role:** AI Engineer
* **Level:** Level 5
* **Experience:** Trên 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh sự khác nhau giữa mạng nơ-ron đồ thị GNN (Graph Neural Networks) và mạng nơ-ron tích chập CNN về cấu trúc dữ liệu đầu vào và phép toán cốt lõi.
* **expected_key_points:**
  - id: KP1_1
    content: Cấu trúc dữ liệu Grid vs Non-grid
    keypoint_weight: 0.5
    description: CNN nhận đầu vào là dữ liệu có cấu trúc lưới cố định (grid-like như hình ảnh). GNN nhận đầu vào là đồ thị phi cấu trúc lưới (non-grid) gồm các đỉnh và cạnh có mối quan hệ tự do.
  - id: KP1_2
    content: Phép toán tích chập vs Truyền tin nhắn
    keypoint_weight: 0.5
    description: CNN sử dụng bộ lọc kernel trượt cố định trên ảnh. GNN sử dụng phép toán truyền tin nhắn (Message Passing): mỗi nút cập nhật trạng thái bằng cách gộp (aggregate) đặc trưng của các nút lân cận.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Khái niệm Thực thể (Entity) và Mối quan hệ (Relation) trong Đồ thị Tri thức (Knowledge Graph) là gì? Cho ví dụ về 1 bộ ba (triple) tri thức.
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa Thực thể và Mối quan hệ
    keypoint_weight: 0.5
    description: Thực thể biểu diễn các đối tượng/khái niệm thực tế (nút đồ thị). Mối quan hệ biểu diễn liên kết ngữ nghĩa giữa các đối tượng đó (cạnh đồ thị).
  - id: KP2_2
    content: Ví dụ Bộ ba (Triple)
    keypoint_weight: 0.5
    description: Nêu đúng ví dụ bộ ba dạng (Subject, Relation, Object). Ví dụ: (Hà Nội, là thủ đô của, Việt Nam).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh hai định dạng lưu trữ cơ sở dữ liệu đồ thị phổ biến hiện nay: RDF (Resource Description Framework) và Property Graph.
* **expected_key_points:**
  - id: KP3_1
    content: Đặc trưng định dạng RDF
    keypoint_weight: 0.5
    description: RDF lưu trữ dữ liệu dưới dạng các bộ ba (triples) chuẩn hóa, sử dụng URI để định danh duy nhất, tối ưu cho việc trao đổi dữ liệu toàn cầu và ngữ nghĩa web.
  - id: KP3_2
    content: Đặc trưng định dạng Property Graph
    keypoint_weight: 0.5
    description: Property Graph cho phép các nút và cạnh chứa các thuộc tính key-value tùy chỉnh bên trong, dễ truy vấn và tối ưu hiệu năng cho các ứng dụng thực tế.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích chi tiết cơ chế hoạt động của thuật toán GraphSAGE trong việc sinh vector embedding cho các nút trên đồ thị tri thức lớn. Kỹ thuật này giải quyết vấn đề gì của thuật toán GCN thông thường?
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế Message Passing và Aggregators của GraphSAGE
    keypoint_weight: 0.5
    description: GraphSAGE thay vì tính toán trên toàn bộ đồ thị, nó lấy mẫu ngẫu nhiên một nhóm nhỏ lân cận (neighborhood sampling), sử dụng các hàm gộp (Mean, LSTM, Pooling) để tổng hợp đặc trưng của lân cận rồi cập nhật trạng thái nút.
  - id: KP4_2
    content: Giải quyết bài toán quy mô lớn (Inductive Learning)
    keypoint_weight: 0.5
    description: GCN thông thường yêu cầu toàn bộ ma trận kề đồ thị lưu trên RAM (transductive learning, không scale được). GraphSAGE hỗ trợ inductive learning, có thể sinh embedding cho các nút mới thêm vào đồ thị mà không cần train lại toàn bộ.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Xây dựng pipeline tự động trích xuất Tri thức (Knowledge Extraction) từ văn bản tiếng Việt phi cấu trúc dùng LLM.
* **expected_key_points:**
  - id: KP5_1
    content: Quy trình trích xuất thực thể và quan hệ
    keypoint_weight: 0.5
    description: Tiền xử lý văn bản -> Viết prompt cung cấp schema mẫu cho LLM để trích xuất danh sách thực thể, nhãn của thực thể, và liên kết quan hệ (dạng JSON list).
  - id: KP5_2
    content: Giải quyết lỗi trùng lặp thực thể (Entity Resolution/Linking)
    keypoint_weight: 0.5
    description: Sử dụng vector similarity để gộp các từ đồng nghĩa biểu diễn cùng một thực thể (ví dụ: 'HN', 'Hà Nội', 'TP. Hà Nội') vào một nút duy nhất trên đồ thị tri thức.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh hiệu năng truy vấn đồ thị giữa cơ sở dữ liệu đồ thị Neo4j và cơ sở dữ liệu đồ thị phân tán (như TigerGraph) khi thực hiện các truy vấn quét đồ thị sâu đa bước (deep multi-hop queries).
* **expected_key_points:**
  - id: KP6_1
    content: Hạn chế của Neo4j ở các bước quét sâu
    keypoint_weight: 0.5
    description: Neo4j lưu trữ cấu trúc liên kết trỏ trực tiếp. Rất nhanh ở các bước quét gần (1-2 hops) nhưng khi truy vấn sâu (>3 hops) thời gian chạy tăng theo cấp số nhân do nghẽn băng thông bộ nhớ.
  - id: KP6_2
    content: Ưu thế của TigerGraph (Massively Parallel Processing)
    keypoint_weight: 0.5
    description: TigerGraph sử dụng kiến trúc biên dịch mã truy vấn và xử lý song song phân tán (MPP), cho phép chạy các thuật toán đồ thị phức tạp qua hàng chục hops thời gian thực hiệu quả hơn.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách tích hợp thông tin cấu trúc đồ thị tri thức vào mô hình BERT để cải thiện độ chính xác phân loại văn bản (ví dụ kiến trúc ERNIE).
* **expected_key_points:**
  - id: KP7_1
    content: Cơ chế căn chỉnh Thực thể (Entity Alignment Layer)
    keypoint_weight: 0.6
    description: Sử dụng thuật toán TransE/TransR để pre-train lấy vector đại diện thực thể trên Đồ thị Tri thức. Trong mô hình BERT, chèn thêm một lớp căn chỉnh (alignment layer) để kết hợp vector chữ của BERT và vector thực thể tương ứng từ đồ thị.
  - id: KP7_2
    content: Lợi ích ngữ nghĩa
    keypoint_weight: 0.4
    description: Giúp mô hình có thêm kiến thức nền thực tế (factual knowledge), cải thiện khả năng phân loại văn bản và trích xuất thông tin chuyên ngành tốt hơn.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống hỏi đáp trên đồ thị tri thức y khoa (Knowledge Graph QA / KBQA) tiếng Việt phục vụ bác sĩ tra cứu tương tác thuốc và chuẩn đoán bệnh lý tự động.
* **expected_key_points:**
  - id: KP8_1
    content: Kiến trúc chuyển đổi câu hỏi sang truy vấn đồ thị (Text-to-Cypher/SPARQL)
    keypoint_weight: 0.5
    description: Sử dụng LLM fine-tune để dịch ngôn ngữ tự nhiên tiếng Việt của bác sĩ thành câu lệnh truy vấn đồ thị chuẩn (như Cypher hoặc SPARQL) dựa trên schema đồ thị y tế được cung cấp trong prompt.
  - id: KP8_2
    content: Xử lý kết quả truy vấn và sinh câu trả lời
    keypoint_weight: 0.5
    description: Thực thi câu lệnh Cypher trên DB đồ thị (như Neo4j) để lấy dữ liệu tương tác thuốc chuẩn xác -> Nạp dữ liệu này làm ngữ cảnh cho LLM sinh câu trả lời y khoa an toàn và chính xác 100%.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp tìm kiếm ngữ nghĩa kết hợp Vector Search và Knowledge Graph (GraphRAG) giải quyết các câu hỏi phân tích logic phức tạp (ví dụ: 'Liệt kê các đối tác của công ty A có liên quan đến bê bối tài chính gần đây').
* **expected_key_points:**
  - id: KP9_1
    content: Xây dựng đồ thị con ngữ cảnh (Sub-graph Retrieval)
    keypoint_weight: 0.5
    description: Dùng Vector Search tìm các thực thể xuất hiện trong câu hỏi -> truy xuất các nút và cạnh lân cận trong phạm vi 2-hops từ Đồ thị Tri thức để tạo thành một đồ thị con ngữ cảnh (sub-graph).
  - id: KP9_2
    content: Cấu trúc hóa ngữ cảnh gửi LLM
    keypoint_weight: 0.5
    description: Chuyển đổi đồ thị con ngữ cảnh thành mô tả văn bản có cấu trúc (ví dụ danh sách các mối quan hệ A -> B -> C) để nạp vào prompt của LLM, giúp LLM lập luận logic chuẩn xác không bị ảo tưởng.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống tự động phát hiện mâu thuẫn tri thức (Knowledge Conflict Detection) khi tích hợp dữ liệu từ nhiều nguồn khác nhau (như Wikipedia, báo chí, báo cáo nội bộ) vào đồ thị tri thức doanh nghiệp.
* **expected_key_points:**
  - id: KP10_1
    content: Phát hiện mâu thuẫn logic và thuộc tính
    keypoint_weight: 0.5
    description: Xây dựng các luật logic (ontological constraints) để tự động phát hiện mâu thuẫn (ví dụ: một người không thể sinh vào hai năm khác nhau, hoặc công ty A chỉ có một CEO duy nhất).
  - id: KP10_2
    content: Cơ chế giải quyết mâu thuẫn (Conflict Resolution)
    keypoint_weight: 0.5
    description: Sử dụng mô hình chấm điểm độ tin cậy nguồn tin (Source Credibility Scoring) kết hợp với LLM để phân tích ngữ cảnh, lựa chọn thông tin đúng nhất để cập nhật đồ thị và ghi vết nguồn gốc dữ liệu (data provenance).

