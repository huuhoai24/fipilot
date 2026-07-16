# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 4) - Tập Đề Two-Tower Models và CTR Prediction (7)

* **Role:** AI Engineer
* **Level:** Level 4
* **Experience:** 6 - 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt sự khác nhau giữa hai phương pháp xây dựng hệ thống khuyến nghị: Collaborative Filtering (Lọc cộng tác) và Content-based Filtering (Lọc dựa trên nội dung).
* **expected_key_points:**
  - id: KP1_1
    content: Đặc trưng Collaborative Filtering
    keypoint_weight: 0.5
    description: Dự đoán sở thích của người dùng dựa trên hành vi tương tác lịch sử của các người dùng khác có sở thích tương tự (không cần phân tích chi tiết thuộc tính sản phẩm).
  - id: KP1_2
    content: Đặc trưng Content-based Filtering
    keypoint_weight: 0.5
    description: Gợi ý các sản phẩm có thuộc tính, đặc trưng giống với các sản phẩm mà người dùng hiện tại từng thích trong quá khứ (phân tích thông tin tag, thể loại, văn bản sản phẩm).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày sự khác nhau giữa hai cách tiếp cận lọc cộng tác: User-based Collaborative Filtering và Item-based Collaborative Filtering.
* **expected_key_points:**
  - id: KP2_1
    content: Cơ chế User-based CF
    keypoint_weight: 0.5
    description: Tìm kiếm các người dùng có hành vi tương tự với User A -> gợi ý những sản phẩm mà nhóm người dùng này thích nhưng User A chưa từng xem.
  - id: KP2_2
    content: Cơ chế Item-based CF
    keypoint_weight: 0.5
    description: Tính toán độ tương đồng giữa các sản phẩm dựa trên việc chúng cùng được thích bởi những nhóm user nào -> gợi ý sản phẩm tương tự sản phẩm User A vừa mua. Thường ổn định hơn User-based vì số lượng sản phẩm ít thay đổi hơn số lượng người dùng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Ma trận tương tác thưa (Sparse Interaction Matrix) là gì? Tại sao nó lại là thách thức lớn đối với việc huấn luyện hệ thống khuyến nghị?
* **expected_key_points:**
  - id: KP3_1
    content: Khái niệm ma trận thưa
    keypoint_weight: 0.5
    description: Là ma trận biểu diễn tương tác giữa User và Item, trong đó đại đa số các ô đều trống (giá trị 0/NULL) do một người dùng chỉ tương tác với tỷ lệ cực nhỏ trên tổng số hàng triệu sản phẩm.
  - id: KP3_2
    content: Thách thức đối với mô hình
    keypoint_weight: 0.5
    description: Gây thiếu thông tin huấn luyện, mô hình dễ bị overfitting trên các tương tác phổ biến, khó tìm được các mối quan hệ ẩn giữa người dùng và sản phẩm ít tương tác (long-tail items).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích phương pháp Phân tích ma trận trị riêng (Matrix Factorization - ví dụ SVD hoặc ALS) trong hệ thống gợi ý. Làm thế nào phương pháp này tìm ra các đặc trưng ẩn (latent features)?
* **expected_key_points:**
  - id: KP4_1
    content: Phân rã ma trận tương tác
    keypoint_weight: 0.6
    description: Phân rã ma trận tương tác thưa kích thước $M \times N$ thành tích của hai ma trận có chiều kích thước nhỏ hơn: Ma trận User $U \in \mathbb{R}^{M \times K}$ và Ma trận Item $V \in \mathbb{R}^{K \times N}$ với $K$ là số chiều đặc trưng ẩn ($K \ll M, N$).
  - id: KP4_2
    content: Học đặc trưng ẩn (Latent Features)
    keypoint_weight: 0.4
    description: Huấn luyện bằng cách tối thiểu hóa sai số tái lập ma trận trên các ô có tương tác thực tế (sử dụng SGD hoặc Alternating Least Squares - ALS) để tự động học ra các đặc trưng ẩn (ví dụ: thể loại phim ẩn, thói quen người dùng) mà không cần dán nhãn thủ công.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày kiến trúc mô hình Hai tháp (Two-Tower Model - ví dụ DSSM) thường được sử dụng trong giai đoạn truy xuất (Retrieval) của các hệ thống gợi ý quy mô lớn.
* **expected_key_points:**
  - id: KP5_1
    content: Cấu trúc User Tower và Item Tower
    keypoint_weight: 0.5
    description: User Tower nhận đặc trưng user (id, demographic, lịch sử) sinh ra vector embedding đại diện $u$. Item Tower nhận đặc trưng item (id, categories, text) sinh ra vector $v$. Hai tháp chạy song song độc lập.
  - id: KP5_2
    content: Tính toán khớp và tối ưu hóa suy luận
    keypoint_weight: 0.5
    description: Độ tương đồng được tính bằng tích vô hướng (dot product) hoặc cosine similarity $u \cdot v^T$. Khi suy luận, các vector Item có thể tính trước (offline) và lưu vào Vector DB. Khi user truy cập, chỉ cần chạy tháp User lấy vector $u$ rồi tìm kiếm lân cận gần nhất (ANN) trên DB để trả kết quả dưới 10ms.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách tính và so sánh vai trò của các chỉ số đánh giá hệ thống gợi ý: Recall@K, Precision@K, và NDCG@K.
* **expected_key_points:**
  - id: KP6_1
    content: Cách tính và vai trò Precision@K và Recall@K
    keypoint_weight: 0.6
    description: Precision@K đo tỷ lệ sản phẩm thực sự liên quan trong số K sản phẩm được gợi ý đầu tiên. Recall@K đo tỷ lệ sản phẩm liên quan được gợi ý thành công trong số tất cả sản phẩm thực tế user quan tâm. Dùng để đánh giá độ bao phủ ở giai đoạn đầu.
  - id: KP6_2
    content: Vai trò của NDCG@K
    keypoint_weight: 0.4
    description: NDCG@K đánh giá thứ tự xếp hạng của K sản phẩm được gợi ý, áp dụng hàm phạt nếu sản phẩm liên quan tốt bị xếp ở các vị trí phía sau. Thích hợp nhất để đánh giá giai đoạn Ranking cuối cùng.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Làm thế nào để giải quyết vấn đề lọc bỏ các sản phẩm người dùng đã xem gần đây (Frequency Capping) và tăng độ đa dạng (Diversity), độ mới lạ (Serendipity) của danh sách gợi ý?
* **expected_key_points:**
  - id: KP7_1
    content: Cơ chế Frequency Capping
    keypoint_weight: 0.5
    description: Thiết lập bộ lọc (filter) loại bỏ các sản phẩm nằm trong danh sách lịch sử tương tác gần đây của user (lưu trong Redis/cache) trước khi đưa vào bước xếp hạng cuối cùng.
  - id: KP7_2
    content: Tăng tính đa dạng (Diversity) và mới lạ
    keypoint_weight: 0.5
    description: Sử dụng thuật toán MMR (Maximal Marginal Relevance) để cân bằng giữa độ liên quan và độ đa dạng (tránh gợi ý toàn bộ sản phẩm cùng loại); áp dụng cơ chế khám phá (exploration) chèn ngẫu nhiên một tỷ lệ nhỏ sản phẩm mới lạ thuộc lĩnh vực khác sở thích thường ngày của user.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống gợi ý video ngắn (như TikTok) có khả năng phản hồi thời gian thực với độ trễ < 50ms cho 100 triệu người dùng hoạt động hàng ngày.
* **expected_key_points:**
  - id: KP8_1
    content: Thiết kế kiến trúc 4 giai đoạn (Retrieval, Filtering, Ranking, Re-ranking)
    keypoint_weight: 0.5
    description: Phase 1: Retrieval dùng Two-Tower model truy xuất nhanh 1000 video từ kho hàng triệu video. Phase 2: Filtering lọc video đã xem, bị báo cáo. Phase 3: Ranking dùng mô hình Deep Learning nặng (như DLRM/DeepFM) dự đoán CTR và thời gian xem (watch time). Phase 4: Re-ranking tối ưu hóa độ đa dạng và chèn quảng cáo.
  - id: KP8_2
    content: Streaming Feature Update và Caching
    keypoint_weight: 0.5
    description: Sử dụng Kafka/Flink để ghi nhận hành vi lướt/xem video (time spent, like, skip) trong thời gian thực, cập nhật lập tức user profile vào Redis; sử dụng cụm Vector DB phân tán lập chỉ mục HNSW để đảm bảo thời gian truy xuất cực thấp.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp Session-based Recommendation (gợi ý dựa trên phiên làm việc hiện tại) dành cho khách vãng lai mua sắm trên trang thương mại điện tử mà không cần thông tin đăng nhập hay lịch sử lâu dài.
* **expected_key_points:**
  - id: KP9_1
    content: Mô hình hóa hành vi phiên làm việc (Session Modeling)
    keypoint_weight: 0.6
    description: Biểu diễn các hành động của user (xem sản phẩm, thêm vào giỏ) trong phiên hiện tại thành một chuỗi tuần tự thời gian. Sử dụng kiến trúc mạng GRU4Rec (dùng GRU học tính tuần tự của clicks) hoặc Graph Neural Networks (SR-GNN biểu diễn phiên thành đồ thị để học quan hệ giữa các sản phẩm).
  - id: KP9_2
    content: Tận dụng Session Embedding sinh gợi ý
    keypoint_weight: 0.4
    description: Sinh vector embedding đại diện cho trạng thái hiện tại của phiên làm việc của user -> Thực hiện tính độ tương đồng cosine với các vector sản phẩm để gợi ý sản phẩm tiếp theo liên quan nhất ngay trong phiên.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống dự đoán tỷ lệ click quảng cáo (Click-Through Rate - CTR Prediction) kết hợp các đặc trưng tương tác bậc cao và bậc thấp sử dụng kiến trúc Deep & Wide hoặc DeepFM.
* **expected_key_points:**
  - id: KP10_1
    content: Kiến trúc Deep & Wide
    keypoint_weight: 0.5
    description: Wide component là mô hình tuyến tính học các tương tác ghi nhớ (memorization) từ các đặc trưng kết hợp chéo thiết lập thủ công. Deep component dùng mạng nơ-ron sâu tự động học các biểu diễn đặc trưng ẩn bậc cao (generalization) thông qua embeddings.
  - id: KP10_2
    content: Cải tiến của DeepFM
    keypoint_weight: 0.5
    description: DeepFM thay thế phần Wide bằng mạng Factorization Machine (FM) chia sẻ chung vector embedding đầu vào với mạng Deep. Giúp tự động học các tương tác đặc trưng bậc 1 và bậc 2 mà không cần thiết kế đặc trưng chéo thủ công, tăng độ chính xác dự đoán CTR.

