# Bộ Câu Hỏi Phỏng Vấn Data Scientist (Level 1)

* **Role:** Data Scientist
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong các bài toán phân lớp đa lớp (Multi-class Classification) bằng mạng nơ-ron hoặc mô hình Logistic Regression mở rộng, hàm kích hoạt Softmax thường được sử dụng ở tầng đầu ra (Output layer). Hãy giải thích nguyên lý toán học và ý nghĩa của hàm Softmax đối với các giá trị dự báo đầu ra.
* **expected_key_points:**
  - id: KP1_1
    content: Công thức toán học chuyển đổi giá trị thô dựa trên hàm mũ (Exponential transformation)
    keypoint_weight: 0.5
    description: Hàm Softmax tiếp nhận một vectơ chứa các giá trị dự báo thô (Logits) từ tầng trước đó, áp dụng phép toán hàm mũ cơ số e lên từng phần tử để biến đổi toàn bộ các số thực (kể cả số âm) thành các giá trị số thực dương.
  - id: KP1_2
    content: Cơ chế chuẩn hóa tổng bằng 1 tạo thành phân phối xác suất (Probability distribution)
    keypoint_weight: 0.5
    description: Softmax chia giá trị hàm mũ của từng lớp cho tổng tất cả các giá trị hàm mũ của toàn bộ các lớp trong vectơ. Kết quả thu được là các giá trị đầu ra nằm trong khoảng từ 0 đến 1 và tổng của chúng bắt buộc phải bằng 1, biến đổi vectơ logits thành một phân phối xác suất giúp mô hình biểu diễn độ tự tin đối với từng lớp nhãn mục tiêu.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Khi phân tích dữ liệu kinh doanh hằng ngày (ví dụ: dữ liệu chi tiêu của khách hàng, số lượng lượt xem video), nhà khoa học dữ liệu thường gặp hiện tượng dữ liệu có Phân phối đuôi dài (Long-tailed / Heavy-tailed Distribution). Hiện tượng này ảnh hưởng thế nào đến các chỉ số thống kê trung tâm (Mean, Median) và cách xử lý cơ bản là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Hệ quả làm lệch giá trị thống kê trung tâm (Mean vs Median)
    keypoint_weight: 0.5
    description: Phân phối đuôi dài (hoặc phân phối lệch phải) chứa một số ít các điểm dữ liệu có giá trị cực kỳ lớn nằm kéo dài về phía bên phải đồ thị. Sự xuất hiện của các điểm cực biên này kéo phình to giá trị trung bình cộng (Mean) lên rất cao, khiến Mean không còn đại diện chính xác cho xu hướng trung tâm của số đông, trong khi giá trị trung vị (Median) hoạt động ổn định và phản ánh đúng thực tế hơn.
  - id: KP2_2
    content: Giải pháp biến đổi toán học phi tuyến (Log Transformation) để chuẩn hóa dữ liệu
    keypoint_weight: 0.5
    description: Sử dụng phép biến đổi Logarithm (Log Transformation, ví dụ: $log(x)$ hoặc $log(x+1)$) lên biến số đó. Bản chất đồ thị hàm log giúp nén chặt khoảng cách của các giá trị cực lớn ở phần đuôi dài và kéo giãn khoảng cách của các giá trị nhỏ ở vùng trung tâm, đưa phân phối dữ liệu về dạng gần đối xứng hoặc phân phối chuẩn (Normal-like), giúp các mô hình tuyến tính học hiệu quả hơn.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong kỹ thuật giảm chiều dữ liệu theo trường phái Filter Method, chỉ số ANOVA F-value thường được áp dụng để lựa chọn đặc trưng (Feature Selection). Hãy giải thích nguyên lý sử dụng chỉ số này để lọc ra các biến số đầu vào hữu ích cho bài toán phân loại nhị phân.
* **expected_key_points:**
  - id: KP3_1
    content: Nguyên lý đo lường tỷ lệ phương sai giữa các nhóm và nội bộ nhóm (F-statistic logic)
    keypoint_weight: 0.5
    description: Chỉ số F-value trong kiểm định ANOVA tính toán tỷ lệ giữa phương sai của dữ liệu giữa các nhóm nhãn mục tiêu (Between-group variance) và phương sai nội bộ bên trong từng nhóm nhãn (Within-group variance). Giá trị F-value càng lớn chứng tỏ sự khác biệt giữa các nhóm càng rõ rệt.
  - id: KP3_2
    content: Tiêu chí toán học xếp hạng và lựa chọn đặc trưng
    keypoint_weight: 0.5
    description: Đối với một biến số đặc trưng liên tục, nếu giá trị F-value tính toán được đối với hai nhóm nhãn mục tiêu càng lớn (tương ứng p-value càng nhỏ), chứng tỏ biến số đó có năng lực phân tách mạnh mẽ giữa hai lớp nhãn. RFE hoặc thuật toán lọc sẽ sắp xếp thứ tự và giữ lại các đặc trưng có F-value cao nhất để đưa vào huấn luyện mô hình.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong xử lý đặc trưng dữ liệu danh mục (Categorical Features), kỹ thuật Target Encoding (hoặc Mean Encoding) hoạt động ra sao? Hãy chỉ ra rủi ro kỹ thuật lớn nhất của phương pháp này và một giải pháp để kiểm soát rủi ro đó.
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế mã hóa danh mục bằng giá trị trung bình của biến mục tiêu
    keypoint_weight: 0.4
    description: Target Encoding chuyển đổi các giá trị chuỗi danh mục bằng cách tính toán giá trị trung bình (Mean) của biến mục tiêu ứng với chính nhóm danh mục đó trong tập dữ liệu huấn luyện.
  - id: KP4_2
    content: Rủi ro rò rỉ thông tin dữ liệu mục tiêu (Target Leakage / Overfitting)
    keypoint_weight: 0.3
    description: Kỹ thuật này trực tiếp sử dụng thông tin của biến mục tiêu để sinh ra đặc trưng đầu vào. Nếu một nhóm danh mục có số lượng mẫu quá nhỏ, giá trị trung bình sẽ bị chi phối tuyệt đối bởi các mẫu đó, dẫn đến việc rò rỉ thông tin từ tương lai vào mô hình, gây Overfitting nặng nề (mô hình đạt điểm tuyệt đối trên tập Train nhưng sụp đổ trên tập Test).
  - id: KP4_3
    content: Giải pháp kỹ thuật làm mịn dữ liệu hoặc kiểm giá chéo (Smoothing / Out-of-fold encoding)
    keypoint_weight: 0.3
    description: Khắc phục bằng kỹ thuật làm mịn (Smoothing) bằng cách kết hợp trọng số giữa giá trị trung bình cục bộ của nhóm và giá trị trung bình toàn cục của toàn bộ bảng dữ liệu thô; hoặc áp dụng kỹ thuật mã hóa Out-of-fold (K-fold target encoding) để đảm bảo giá trị mã hóa của một dòng không chứa thông tin mục tiêu của chính dòng đó.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thuật toán HDBSCAN (Hierarchical Density-Based Spatial Clustering of Applications with Noise) được xem là một sự cải tiến vượt trội của DBSCAN. Hãy giải thích điểm khác biệt cốt lõi về mặt triết lý xử lý siêu tham số mật độ giữa hai thuật toán này.
* **expected_key_points:**
  - id: KP5_1
    content: Điểm hạn chế biên mật độ cố định của thuật toán DBSCAN truyền thống
    keypoint_weight: 0.4
    description: DBSCAN yêu cầu cấu hình một siêu tham số bán kính Eps cố định trên toàn cục. Điều này khiến DBSCAN hoàn toàn thất bại khi đối mặt với các tập dữ liệu thực tế có mật độ phân bổ không đồng đều (Variable density), nơi các cụm dữ liệu có độ nén chặt hoặc thưa thớt khác nhau.
  - id: KP5_2
    content: Nguyên lý xây dựng cây phân cấp mật độ biến đổi của HDBSCAN
    keypoint_weight: 0.4
    description: HDBSCAN loại bỏ việc chọn siêu tham số Eps cố định. Thuật toán quét qua toàn bộ dải giá trị của Eps để xây dựng một đồ thị cây phân cấp phân cụm (Dendrogram) dựa trên sự liên kết mật độ của các điểm, cho phép nhận diện và trích xuất các cụm dữ liệu có mật độ biến đổi linh hoạt ở các tầng không gian khác nhau.
  - id: KP5_3
    content: Tiêu chí tối ưu độ bền vững để trích xuất cụm (Cluster Stability)
    keypoint_weight: 0.2
    description: HDBSCAN duyệt qua cây phân cấp và sử dụng một tiêu chí toán học đo lường độ bền vững (Stability - dựa trên thời gian sinh tồn của cụm khi thay đổi ngưỡng mật độ) để tự động quyết định cắt cây và chọn ra các cụm có cấu trúc vật lý ổn định nhất.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong các hệ thống gợi ý (Information Retrieval / Recommendation Systems), tại sao chỉ số Mean Average Precision (MAP) lại được sử dụng phổ biến để đánh giá danh sách kết quả trả về? Hãy giải thích cách tính chỉ số này dựa trên thuộc tính thứ tự (Ranking).
* **expected_key_points:**
  - id: KP6_1
    content: Ý nghĩa kiểm soát thuộc tính thứ tự của chỉ số MAP đối với trải nghiệm người dùng
    keypoint_weight: 0.4
    description: Khác với Precision thông thường (chỉ đếm số lượng), MAP là chỉ số đánh giá bài toán xếp hạng (Ranking metric). Nó trừng phạt mô hình nếu các mục gợi ý chính xác, phù hợp bị xếp ở vị trí cuối danh sách, và thưởng điểm cao nếu các mục phù hợp được đẩy lên các vị trí đầu tiên đầu ngày.
  - id: KP6_2
    content: Quy trình tính chỉ số Average Precision (AP) cho một người dùng độc lập
    keypoint_weight: 0.4
    description: Đối với một người dùng, ta duyệt tuần tự từ đầu đến cuối danh sách gợi ý. Tại mỗi vị trí có mục gợi ý thực sự phù hợp (Relevant item), ta tính toán chỉ số Precision tại thời điểm đó (Precision@k). Giá trị AP là trung bình cộng của tất cả các Precision@k tại các điểm phù hợp này.
  - id: KP6_3
    content: Quy trình lấy trung bình toàn cục để tính MAP
    keypoint_weight: 0.2
    description: Chỉ số MAP (Mean Average Precision) được tính toán bằng cách lấy giá trị trung bình cộng của toàn bộ các chỉ số AP thu được từ tất cả các người dùng hoặc tất cả các lượt truy vấn trong tập dữ liệu kiểm thử.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy trình bày cơ chế hoạt động của thuật toán AdaBoost (Adaptive Boosting) cho bài toán phân loại. Thuật toán này điều chỉnh trọng số của các mẫu dữ liệu (Sample Weights) bị dự báo sai như thế nào qua từng vòng lặp?
* **expected_key_points:**
  - id: KP7_1
    content: Quy trình huấn luyện tuần tự các mô hình yếu (Weak learners)
    keypoint_weight: 0.4
    description: AdaBoost khởi tạo một trọng số đồng đều cho tất cả các mẫu dữ liệu thô. Qua từng vòng lặp, thuật toán huấn luyện một mô hình phân loại yếu (thường là một cây quyết định nông có 1 vết cắt - Decision Stump) bám sát vào tập trọng số hiện tại.
  - id: KP7_2
    content: Cơ chế tăng trọng số cho mẫu dự báo sai và giảm trọng số cho mẫu đúng
    keypoint_weight: 0.4
    description: Sau mỗi vòng lặp, AdaBoost tính toán tỷ lệ lỗi của mô hình. Đối với các mẫu dữ liệu bị mô hình hiện tại dự báo sai nhãn mục tiêu, thuật toán sẽ tăng mạnh trọng số của chúng lên (Tăng mức độ trừng phạt). Đối với các mẫu dự báo đúng, trọng số bị giảm đi. Điều này ép buộc mô hình yếu ở vòng lặp tiếp theo phải tập trung tối đa vào việc giải quyết các mẫu khó mà mô hình trước đã làm sai.
  - id: KP7_3
    content: Cơ chế cộng gộp kết quả có trọng số mô hình (Classifier weights)
    keypoint_weight: 0.2
    description: Mỗi mô hình yếu được gán một trọng số năng lực (Amount of say - chỉ số Alpha) tỷ lệ nghịch với tỷ lệ lỗi của nó. Kết quả dự báo cuối cùng là sự bỏ phiếu có trọng số hệ số Alpha của toàn bộ các mô hình yếu trong chuỗi.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong huấn luyện mạng nơ-ron sâu (Deep Learning), tầng Dropout Layer được sử dụng rộng rãi như một kỹ thuật Regularization. Hãy giải thích nguyên lý hoạt động vật lý của Dropout trong quá trình lan truyền tiến (Forward Propagation) và tại sao nó lại giúp chống Overfitting dựa trên triết lý Ensemble Learning ngầm?
* **expected_key_points:**
  - id: KP8_1
    content: Cơ chế loại bỏ ngẫu nhiên các nơ-ron theo xác suất ở bước Forward propagation
    keypoint_weight: 0.4
    description: Trong mỗi bước lặp huấn luyện (Iteration) của quá trình lan truyền tiến, tầng Dropout chủ động tắt hoặc loại bỏ ngẫu nhiên một tỷ lệ phần trăm các nút nơ-ron (Neurons) trong tầng hiện tại theo một xác suất cấu hình sẵn $p$ (ví dụ $p=0.5$), bằng cách ép giá trị đầu ra của các nút đó bằng 0.
  - id: KP8_2
    content: Phá vỡ sự phụ thuộc chéo đồng thích nghi giữa các trọng số (Co-adaptation)
    keypoint_weight: 0.3
    description: Việc tắt ngẫu nhiên ép buộc mạng nơ-ron không được phép phụ thuộc hoàn toàn vào một mối liên kết hay một vài nút nơ-ron cụ thể nào để dự báo. Các trọng số bắt buộc phải tự phân bổ đều năng lực học và tìm kiếm các quy luật độc lập, giúp phá vỡ sự phụ thuộc chéo đồng thích nghi (Co-adaptation) giữa các nơ-ron.
  - id: KP8_3
    content: Triết lý Ensemble Learning tích hợp ngầm của Dropout
    keypoint_weight: 0.3
    description: Do mỗi iteration cấu trúc đồ thị mạng nơ-ron bị thay đổi ngẫu nhiên, quá trình huấn luyện với Dropout thực chất tương đương với việc ta đang huấn luyện đồng thời hàng triệu mô hình mạng nơ-ron con con cấu trúc khác nhau chia sẻ chung trọng số. Ở giai đoạn Inference (Đọc báo cáo dự báo), toàn bộ các nơ-ron đều mở lại và được nhân với hệ số điều chỉnh ($1-p$), tạo ra hiệu ứng gộp trung bình kết quả phân tích của một mạng Ensemble khổng lồ, giúp tối ưu phương sai và chống Overfitting mạnh mẽ.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Đối với các mô hình học máy phức tạp có thời gian huấn luyện lâu (như Deep Learning hoặc XGBoost dữ liệu lớn), kỹ thuật Bayesian Optimization được ưu tiên sử dụng để tìm kiếm siêu tham số tối ưu. Hãy giải thích nguyên lý hoạt động của giải thuật này thông qua hai thành phần: Surrogate Model (Mô hình thay thế - Gaussian Process) và Acquisition Function (Hàm thu thập).
* **expected_key_points:**
  - id: KP9_1
    content: Vai trò ước lượng và đo lường độ bất định của Surrogate Model (Gaussian Process)
    keypoint_weight: 0.4
    description: Do việc thử nghiệm trực tiếp siêu tham số tốn chi phí rất lớn, Bayesian Optimization dựng một mô hình thay thế (Surrogate Model, phổ biến nhất là Quá trình Gauss - Gaussian Process) để mô phỏng lại bề mặt hàm lỗi của siêu tham số. Tại mỗi điểm không gian, Gaussian Process không chỉ dự báo giá trị hiệu năng trung bình mà còn tính toán được cả khoảng phương sai đo lường độ bất định (Uncertainty) của vùng không gian đó.
  - id: KP9_2
    content: Vai trò định hướng điểm thử nghiệm tiếp theo của Acquisition Function
    keypoint_weight: 0.4
    description: Hàm thu thập (Acquisition Function - ví dụ: Expected Improvement, Upper Confidence Bound) sử dụng kết quả dự báo và độ bất định của Surrogate Model để tính toán và chấm điểm cho toàn bộ không gian siêu tham số, nhằm tìm ra tọa độ điểm siêu tham số tối ưu nhất cần mang đi chạy thử nghiệm vật lý ở bước tiếp theo.
  - id: KP9_3
    content: Bản chất toán học của chiến lược cân bằng giữa Khai thác và Khám phá (Exploration vs Exploitation)
    keypoint_weight: 0.2
    description: Acquisition Function điều khiển sự cân bằng toán học giữa hai chiến lược: **Exploitation (Khai thác):** Ưu tiên quét vào các vùng không gian đã biết là đang cho điểm hiệu năng cao; và **Exploration (Khám phá):** Ưu tiên nhảy vào các vùng không gian xa lạ có độ bất định cao (phương sai lớn) nhằm tìm kiếm cơ hội đột phá chỉ số, giúp thuật toán tìm ra điểm tối ưu toàn cục nhanh nhất với số lần thử nghiệm vật lý ít nhất.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong kiến trúc mạng học sâu so khớp đặc trưng Metric Learning (như Face Recognition), hàm mất mát Triplet Loss được thiết kế như thế nào? Hãy giải thích cấu trúc toán học của hàm lỗi này dựa trên ba thành phần đầu vào: Anchor, Positive, và Negative.
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa bản chất hình học của ba thành phần vector embedding đầu vào
    keypoint_weight: 0.4
    description: Triplet Loss tiếp nhận đầu vào đồng thời là một bộ ba bức ảnh (Triplet) đã được chuyển đổi thành các vectơ đặc trưng (Embeddings) bao gồm: **Anchor (A - mẫu neo):** mẫu thực thể được chọn làm gốc; **Positive (P - mẫu tích cực):** một mẫu khác thuộc cùng một thực thể với Anchor; **Negative (N - mẫu tiêu cực):** một mẫu thuộc về một thực thể hoàn toàn khác biệt.
  - id: KP10_2
    content: Công thức toán học tính toán khoảng cách lề (Margin) của Triplet Loss
    keypoint_weight: 0.4
    description: Hàm lỗi tính toán khoảng cách Euclidean giữa các cặp vectơ và ép buộc ràng buộc tối ưu hóa: $L = \max(0, d(A, P) - d(A, N) + \alpha)$. Trong đó $\alpha$ là một siêu tham số cấu hình khoảng cách lề an toàn (Margin). Mục tiêu toán học là giảm thiểu tối đa khoảng cách $d(A,P)$ và phóng đại khoảng cách $d(A,N)$ vượt qua ngưỡng lề $\alpha$.
  - id: KP10_3
    content: Cơ chế phân loại mẫu trích chọn để huấn luyện (Semi-hard triplets / Hard negative mining)
    keypoint_weight: 0.2
    description: Nếu chọn các mẫu Negative quá dễ (khoảng cách $d(A,N)$ đã quá xa), hàm loss sẽ bằng 0 tuyệt đối và mô hình không thể cập nhật trọng số để học được các chi tiết tinh vi. Data Engineer bắt buộc phải áp dụng giải thuật lọc tìm kiếm mẫu nâng cao (Hard Negative Mining) để trích chọn các mẫu Semi-hard hoặc Hard triplets (các khuôn mặt người khác nhau nhưng có cấu trúc hình học rất giống nhau) để ép mô hình học phân tách vùng biên quyết định tối đa.