# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 2) - Tập Đề Feature Engineering và Data Drift (6)

* **Role:** AI Engineer
* **Level:** Level 2
* **Experience:** 1 - 3  năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa hai hàm loss: L1 Loss (MAE) và L2 Loss (MSE). Trong trường hợp dữ liệu chứa nhiều nhiễu/outliers, bạn chọn loại nào? Tại sao?
* **expected_key_points:**
  - id: KP1_1
    content: Khác biệt công thức toán học và đạo hàm
    keypoint_weight: 0.5
    description: L1 Loss tính tổng trị tuyệt đối sai số, đạo hàm không đổi ngoại trừ điểm 0. L2 Loss tính tổng bình phương sai số, đạo hàm giảm dần khi sai số nhỏ lại.
  - id: KP1_2
    content: Lựa chọn khi có outliers
    keypoint_weight: 0.5
    description: Chọn L1 Loss vì nó ít bị ảnh hưởng bởi outliers (outliers không bị bình phương sai số lên như L2). L2 Loss sẽ cố gắng khớp các điểm outliers này làm lệch mô hình.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** ROC-AUC là gì? Hãy vẽ sơ đồ và giải thích ý nghĩa của chỉ số này trong việc đánh giá mô hình phân loại nhị phân.
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa đường cong ROC
    keypoint_weight: 0.5
    description: ROC (Receiver Operating Characteristic) biểu thị mối quan hệ giữa True Positive Rate (TPR - Recall) và False Positive Rate (FPR) tại các ngưỡng quyết định (thresholds) khác nhau.
  - id: KP2_2
    content: Ý nghĩa AUC (Area Under Curve)
    keypoint_weight: 0.5
    description: AUC đo diện tích dưới đường cong ROC, có giá trị từ 0 đến 1. AUC = 0.5 là phân loại ngẫu nhiên. AUC càng gần 1 chứng tỏ mô hình có khả năng phân biệt lớp tốt.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh hai mô hình phân loại: Decision Tree (Cây quyết định) và Support Vector Machine (SVM) về nguyên lý hoạt động và tính khả giải (explainability).
* **expected_key_points:**
  - id: KP3_1
    content: Nguyên lý hoạt động cơ bản
    keypoint_weight: 0.6
    description: Decision Tree chia nhỏ tập dữ liệu dựa trên các điều kiện của đặc trưng (sử dụng Entropy/Gini Impurity). SVM tìm kiếm một siêu phẳng (hyperplane) tối ưu để phân tách các lớp với lề (margin) lớn nhất trong không gian (sử dụng kernel trick cho phi tuyến).
  - id: KP3_2
    content: So sánh tính khả giải (Explainability)
    keypoint_weight: 0.4
    description: Decision Tree có tính khả giải cao, dễ dàng biểu diễn trực quan dưới dạng sơ đồ logic. SVM hoạt động như hộp đen, rất khó giải thích các hệ số trọng số sau khi sử dụng kernel phi tuyến.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày các phương pháp mã hóa biến phân loại (Categorical Encoding) như One-Hot Encoding và Target Encoding. Nêu ưu nhược điểm từng loại và cách phòng tránh Overfitting khi dùng Target Encoding.
* **expected_key_points:**
  - id: KP4_1
    content: One-Hot vs Target Encoding
    keypoint_weight: 0.5
    description: One-Hot tạo cột nhị phân cho mỗi giá trị duy nhất (gây phình to số chiều nếu cardinality cao). Target Encoding thay thế nhãn phân loại bằng giá trị trung bình của biến mục tiêu (target) tương ứng với nhãn đó.
  - id: KP4_2
    content: Tránh Overfitting trong Target Encoding
    keypoint_weight: 0.5
    description: Target Encoding dễ gây rò rỉ dữ liệu (target leakage). Tránh bằng cách: áp dụng K-fold target encoding (tính trung bình target trên k-1 folds để encode cho fold còn lại), thêm nhiễu (noise addition), hoặc dùng smoothing.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế hoạt động của FlashAttention. Tại sao kỹ thuật này lại tăng tốc độ huấn luyện mô hình Transformer đáng kể?
* **expected_key_points:**
  - id: KP5_1
    content: Vấn đề nghẽn cổ chai của Attention thông thường
    keypoint_weight: 0.5
    description: Attention thông thường yêu cầu ghi ma trận chú ý kích thước $N 	imes N$ ($N$ là độ dài chuỗi) vào bộ nhớ High Bandwidth Memory (HBM) của GPU, gây nghẽn băng thông truyền dữ liệu (I/O bottleneck).
  - id: KP5_2
    content: Cơ chế tối ưu của FlashAttention
    keypoint_weight: 0.5
    description: FlashAttention tính toán softmax theo từng khối (tiling) mà không cần ghi ma trận đầy đủ $N 	imes N$ ra HBM; tận dụng bộ nhớ SRAM tốc độ cực nhanh của GPU để tính toán cục bộ, giảm số lần đọc/ghi bộ nhớ, tăng tốc độ tính toán lên gấp 2-4 lần.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt sự khác nhau giữa Generative Models (Mô hình sinh) và Discriminative Models (Mô hình phân biệt). Nêu ví dụ thuật toán cho mỗi loại.
* **expected_key_points:**
  - id: KP6_1
    content: Bản chất toán học khác biệt
    keypoint_weight: 0.6
    description: Discriminative models học ranh giới phân tách giữa các lớp, ước lượng trực tiếp xác suất có điều kiện $P(Y|X)$. Generative models học phân phối xác suất đồng thời của dữ liệu $P(X, Y)$, từ đó có thể sinh ra dữ liệu mới giống tập train.
  - id: KP6_2
    content: Ví dụ thuật toán cụ thể
    keypoint_weight: 0.4
    description: Discriminative: Logistic Regression, SVM, Random Forest, Neural Networks phân loại. Generative: Naive Bayes, Gaussian Mixture Models (GMM), GANs, VAEs, Diffusion models.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày phương pháp kiểm thử chéo K-Fold Cross-Validation và Stratified K-Fold. Tại sao Stratified K-Fold được khuyên dùng cho dữ liệu mất cân bằng?
* **expected_key_points:**
  - id: KP7_1
    content: Nguyên lý K-Fold vs Stratified K-Fold
    keypoint_weight: 0.6
    description: K-Fold chia ngẫu nhiên dữ liệu thành K phần bằng nhau, luân phiên dùng 1 phần làm test, K-1 phần làm train. Stratified K-Fold đảm bảo tỷ lệ các lớp đối tượng trong mỗi phần chia (fold) luôn bằng đúng tỷ lệ của toàn bộ tập dữ liệu gốc.
  - id: KP7_2
    content: Ứng dụng cho imbalanced data
    keypoint_weight: 0.4
    description: Với dữ liệu mất cân bằng, K-Fold ngẫu nhiên có thể dẫn đến tình trạng một số fold không chứa mẫu nào của lớp thiểu số, gây sai lệch nghiêm trọng khi đánh giá mô hình.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống phát hiện và giám sát hiện tượng suy giảm chất lượng mô hình (Data Drift và Concept Drift) cho một mô hình tín dụng đang chạy production.
* **expected_key_points:**
  - id: KP8_1
    content: Phát hiện Data Drift (Lệch dữ liệu đầu vào)
    keypoint_weight: 0.5
    description: Theo dõi sự thay đổi phân phối của các đặc trưng đầu vào $P(X)$ theo thời gian sử dụng các phép đo khoảng cách/thống kê như Kolmogorov-Smirnov (KS) test, Population Stability Index (PSI), hoặc Kullback-Leibler (KL) divergence.
  - id: KP8_2
    content: Phát hiện Concept Drift (Thay đổi mối quan hệ target)
    keypoint_weight: 0.5
    description: Theo dõi sự thay đổi mối quan hệ giữa đặc trưng và nhãn thực tế $P(Y|X)$ (ví dụ hành vi quỵt nợ thay đổi do khủng hoảng kinh tế) bằng cách giám sát liên tục các metrics hiệu năng thực tế (F1-score, Precision) và kích hoạt pipeline retrain tự động khi metric giảm dưới ngưỡng.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống Multi-Agent System (Hệ thống đa tác nhân LLM) để giải quyết bài toán tự động xử lý khiếu nại và hỗ trợ kỹ thuật cho khách hàng.
* **expected_key_points:**
  - id: KP9_1
    content: Phân vai tác nhân (Agent Roles) và giao tiếp
    keypoint_weight: 0.5
    description: Thiết kế các tác nhân chuyên biệt: Tác nhân Phân loại (Router Agent), Tác nhân Tra cứu dữ liệu (Retrieval Agent), Tác nhân Giải quyết kỹ thuật (Tech Agent), và Tác nhân Kiểm duyệt (Supervisor Agent) giao tiếp với nhau thông qua hàng đợi tin nhắn hoặc API.
  - id: KP9_2
    content: Quản lý trạng thái và Tool Calling
    keypoint_weight: 0.5
    description: Sử dụng framework LangGraph/Autogen để quản lý trạng thái luồng hội thoại (state management), cho phép các agents gọi các công cụ bên ngoài (CRM database, email API) và xử lý lặp (feedback loops) khi câu trả lời chưa đạt yêu cầu.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống tìm kiếm hình ảnh tương đồng (Image Search Engine) quy mô 50 triệu ảnh. Yêu cầu thời gian phản hồi (latency) tìm kiếm < 200ms.
* **expected_key_points:**
  - id: KP10_1
    content: Feature Extraction và Embedding Pipeline
    keypoint_weight: 0.4
    description: Sử dụng mô hình Convolutional nhẹ hoặc Vision Transformer (như ConvNeXt, CLIP ViT) trích xuất đặc trưng ảnh thành vector 512 chiều. Batch processing để đẩy vectors lên DB.
  - id: KP10_2
    content: Vector Indexing và Cluster-based Retrieval
    keypoint_weight: 0.6
    description: Sử dụng Vector DB phân tán lập chỉ mục bằng thuật toán IVF-PQ (Inverted File with Product Quantization) giúp nén kích thước vector lưu trên RAM và tăng tốc độ quét lân cận; triển khai cơ chế caching các kết quả tìm kiếm phổ biến và cân bằng tải (load balancer) cho các nodes truy vấn.

