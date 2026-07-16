# Bộ Câu Hỏi Phỏng Vấn Data Scientist (Level 1)

* **Role:** Data Scientist
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong giai đoạn tiền xử lý dữ liệu (Data Preprocessing), kỹ thuật rời rạc hóa dữ liệu (Data Binning/Discretization) là gì? Hãy nêu mục đích thực tế của việc chuyển đổi một biến số liên tục thành các khoảng rời rạc.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa bản chất của kỹ thuật Data Binning
    keypoint_weight: 0.5
    description: Data Binning là quá trình chia nhỏ dải giá trị của một biến số liên tục (Numerical variable) thành một số lượng cố định các khoảng giá trị nhỏ hơn (gọi là các bins hoặc buckets) để biến đổi đặc trưng đó thành dạng rời rạc hoặc định danh.
  - id: KP1_2
    content: Mục đích giảm nhiễu và tăng tính giải thích (Noise reduction)
    keypoint_weight: 0.5
    description: Giúp mô hình học máy giảm thiểu sự ảnh hưởng của các nhiễu nhỏ hoặc các giá trị ngoại lai biên (Outliers), ngăn chặn hiện tượng Overfitting, đồng thời tăng tính giải thích của dữ liệu đối với các bài toán phân tích nghiệp vụ kinh doanh (ví dụ: chuyển đổi tuổi cụ thể thành các nhóm tuổi như Thanh niên, Trung niên).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong các bài toán phân cụm phi giám sát (Unsupervised Clustering), hãy phân biệt sự khác biệt cơ bản về triết lý tổ chức cấu trúc dữ liệu giữa hai trường phái: Partitioning Clustering (như K-Means) và Hierarchical Clustering (như Agglomerative Clustering).
* **expected_key_points:**
  - id: KP2_1
    content: Triết lý phân hoạch phẳng và cố định số cụm của Partitioning Clustering
    keypoint_weight: 0.5
    description: Trường phái phân hoạch thực hiện chia trực tiếp tập dữ liệu thành các nhóm phẳng, độc lập và không chồng chéo lên nhau. Người dùng bắt buộc phải xác định trước số lượng cụm K, và thuật toán sẽ tối ưu hóa vị trí các tâm cụm dựa trên khoảng cách hình học.
  - id: KP2_2
    content: Triết lý xây dựng cấu trúc lồng ghép dạng cây của Hierarchical Clustering
    keypoint_weight: 0.5
    description: Trường phái phân cấp không yêu cầu chỉ định trước số cụm, mà tập trung xây dựng một chuỗi các cấu trúc phân tầng lồng ghép nhau hiển thị trực quan qua đồ thị cây (Dendrogram), cho phép nhà khoa học dữ liệu chọn số lượng cụm linh hoạt bằng cách cắt cây tại các độ cao khác nhau sau khi thuật toán chạy xong.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Một mạng nơ-ron truyền thẳng cơ bản (Feedforward Neural Network / Multi-Layer Perceptron) được cấu thành từ ba tầng (Layers) logic nào? Hãy giải thích ngắn gọn nhiệm vụ của tầng trung gian (Hidden Layer).
* **expected_key_points:**
  - id: KP3_1
    content: Liệt kê chính xác ba tầng cấu trúc của mạng nơ-ron
    keypoint_weight: 0.5
    description: Mạng nơ-ron truyền thẳng cơ bản được cấu thành tuần tự từ: Input Layer (Tầng đầu vào tiếp nhận đặc trưng), Hidden Layer (Tầng ẩn xử lý tính toán), và Output Layer (Tầng đầu ra trả về kết quả dự báo).
  - id: KP3_2
    content: Nhiệm vụ trích xuất đặc trưng phi tuyến của tầng ẩn (Hidden Layer)
    keypoint_weight: 0.5
    description: Tầng ẩn thực hiện các phép biến đổi tuyến tính kết hợp với hàm kích hoạt phi tuyến tính (Activation function) để tự động trích xuất, tổng hợp các tổ hợp đặc trưng bậc cao từ dữ liệu thô đầu vào, giúp mạng có khả năng biểu diễn và học các quy luật phi tuyến phức tạp.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong kỹ thuật trích chọn đặc trưng (Feature Selection), chỉ số Thông tin tương hỗ (Mutual Information) được tính toán dựa trên nguyên lý gì? Tại sao chỉ số này lại ưu việt hơn hệ số tương quan Pearson khi đánh giá mối quan hệ giữa biến độc lập và biến mục tiêu phi tuyến?
* **expected_key_points:**
  - id: KP4_1
    content: Nguyên lý đo lường lượng thông tin chia sẻ dựa trên Entropy của Mutual Information
    keypoint_weight: 0.4
    description: Mutual Information đo lường lượng thông tin mà ta có thể thu được về một biến số thông qua việc quan sát biến số còn lại, dựa trên lý thuyết Entropy: $I(X;Y) = H(X) + H(Y) - H(X,Y)$. Chỉ số này luôn mang giá trị không âm, bằng 0 khi hai biến độc lập hoàn toàn.
  - id: KP4_2
    content: Điểm hạn chế chỉ đo tuyến tính của hệ số tương quan Pearson
    keypoint_weight: 0.3
    description: Hệ số tương quan Pearson chỉ có khả năng đo lường và phát hiện mối quan hệ tuyến tính thẳng giữa hai biến số. Nếu hai biến có mối quan hệ phi tuyến phức tạp (ví dụ quan hệ hình parabol $y = x^2$), hệ số Pearson sẽ bằng 0, dễ khiến Data Scientist loại bỏ nhầm đặc trưng quan trọng này.
  - id: KP4_3
    content: Khả năng bắt trọn mọi mối quan hệ phi tuyến của Mutual Information
    keypoint_weight: 0.3
    description: Do tính toán dựa trên phân phối xác suất đồng thời toàn cục, Mutual Information có năng lực phát hiện bất kỳ dạng mối quan hệ phụ thuộc nào, kể cả các cấu trúc phi tuyến tính chằng chịt, giúp trích chọn đặc trưng chính xác hơn cho các mô hình học máy phức tạp.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thuật tối ưu hóa Mini-batch Gradient Descent hoạt động ra sao? Hãy phân tích sự đánh đổi về mặt hiệu năng tính toán và độ ổn định của hàm mất mát khi ta tăng kích thước lô (Batch Size) từ nhỏ lên lớn.
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế chia nhỏ tập dữ liệu để cập nhật trọng số của Mini-batch Gradient Descent
    keypoint_weight: 0.4
    description: Thay vì dùng một mẫu độc lẻ hay toàn bộ tập dữ liệu, Mini-batch Gradient Descent chia tập dữ liệu huấn luyện thành các gói nhỏ (Lô/Batches) có kích thước cố định để tính toán gradient và cập nhật trọng số mô hình tuần tự sau khi quét xong mỗi lô.
  - id: KP5_2
    content: Tác động của việc tăng Batch Size lên tốc độ tính toán song song (Hardware utilization)
    keypoint_weight: 0.3
    description: Khi tăng kích thước lô, hệ thống tận dụng tốt hơn năng lực tính toán song song vector hóa của phần cứng (GPU/TPU), giúp giảm số lượng bước cập nhật trong một Epoch và tăng tốc độ xử lý cơ học của tài nguyên dữ liệu lớn.
  - id: KP5_3
    content: Tác động của việc tăng Batch Size lên quỹ đạo hội tụ và rủi ro kẹt cực trị cục bộ
    keypoint_weight: 0.3
    description: Kích thước lô quá lớn làm mịn đường đi của gradient, quỹ đạo hội tụ ít biến động hơn nhưng lại làm mất đi tính ngẫu nhiên ngẫu biến. Việc thiếu nhiễu đồ thị khiến mô hình dễ bị mắc kẹt vĩnh viễn ở các bẫy điểm cực tiểu cục bộ nông (Local Minima) hoặc vùng yên ngựa, làm giảm khả năng tổng quát hóa so với kích thước lô vừa phải.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong phân tích thử nghiệm giả thuyết thống kê phục vụ cho bài toán doanh nghiệp, hãy trình bày các điều kiện giả định toán học bắt buộc phải thỏa mãn trước khi áp dụng kiểm định ANOVA một yếu tố (One-Way ANOVA).
* **expected_key_points:**
  - id: KP6_1
    content: Giả định về tính độc lập của các quan sát (Independence)
    keypoint_weight: 0.3
    description: Các mẫu dữ liệu trong các nhóm phải được thu thập một cách ngẫu nhiên và độc lập hoàn toàn với nhau, hành vi hay giá trị của một mẫu không được chi phối hoặc ảnh hưởng đến mẫu khác.
  - id: KP6_2
    content: Giả định về phân phối chuẩn của biến phụ thuộc (Normality)
    keypoint_weight: 0.4
    description: Biến phụ thuộc liên tục phải tuân theo phân phối chuẩn (Normal Distribution) bên trong mỗi nhóm xã hội được so sánh. Điều này có thể kiểm tra qua biểu đồ Q-Q plot hoặc kiểm định Shapiro-Wilk.
  - id: KP6_3
    content: Giả định về tính đồng nhất phương sai giữa các nhóm (Homogeneity of Variances)
    keypoint_weight: 0.3
    description: Phương sai dữ liệu của các nhóm độc lập bắt buộc phải tương đồng hoặc bằng nhau trong tổng thể (kiểm tra qua Levene's Test), đảm bảo biến động nội bộ không làm lệch phép toán so sánh F-statistic.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Chỉ số Cohen's Kappa được sử dụng nhằm mục đích gì trong đánh giá mô hình phân loại đa lớp? Chỉ số này ưu việt hơn chỉ số Accuracy (Độ chính xác tổng thể) thông thường ở điểm cốt lõi nào?
* **expected_key_points:**
  - id: KP7_1
    content: Mục tiêu đo lường độ đồng thuận loại trừ yếu tố ngẫu nhiên của Cohen's Kappa
    keypoint_weight: 0.5
    description: Cohen's Kappa đo lường mức độ đồng thuận giữa nhãn dự báo của mô hình và nhãn thực tế thực tế, bằng cách chủ động khấu trừ đi tỷ lệ đồng thuận ngẫu nhiên có thể xảy ra (Agreement by chance): $\kappa = (p_o - p_e) / (1 - p_e)$.
  - id: KP7_2
    content: Khả năng chống chịu sự đánh giá sai lệch trên dữ liệu mất cân bằng nhãn nặng
    keypoint_weight: 0.5
    description: Chỉ số Accuracy thông thường sẽ cho điểm rất cao một cách giả tạo trên dữ liệu mất cân bằng (ví dụ mô hình luôn đoán nhãn đa số). Cohen's Kappa giải quyết triệt để vấn đề này vì nó tự động trừng phạt mạnh năng lực dự báo ngẫu nhiên, giúp phản ánh chính xác độ tin cậy thực tế của Data Scientist trên các tập dữ liệu lệch.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong các mạng nơ-ron học sâu tích hợp so khớp đặc trưng Metric Learning, hàm mất mát Contrastive Loss trong kiến trúc mạng Siamese Network hoạt động ra sao? Hãy giải thích công thức toán học xử lý cho hai trường hợp mẫu tương đồng (Positive pair) và mẫu khác biệt (Negative pair).
* **expected_key_points:**
  - id: KP8_1
    content: Cấu trúc chia sẻ trọng số đầu vào cặp song hành của Siamese Network
    keypoint_weight: 0.3
    description: Kiến trúc Siamese Network sử dụng hai nhánh mạng nơ-ron hoàn toàn giống nhau và chia sẻ chung bộ trọng số (Weights) để biến đổi một cặp mẫu đầu vào thành hai vectơ đặc trưng (Embeddings) trong không gian vector thấp.
  - id: KP8_2
    content: Cơ chế toán học ép kéo sát khoảng cách cho mẫu tương đồng (Positive pair)
    keypoint_weight: 0.4
    description: Khi cặp mẫu đầu vào thuộc cùng một thực thể (Nhãn $Y=0$), công thức Contrastive Loss chỉ giữ lại thành phần bình phương khoảng cách Euclidean: $L = \frac{1}{2} (D_w)^2$. Quá trình tối ưu hóa sẽ ép mô hình phải cập nhật trọng số để kéo sát hai vectơ này lại gần nhau tối đa trong không gian embedding.
  - id: KP8_3
    content: Cơ chế toán học đẩy giãn cách vượt ngưỡng lề cho mẫu khác biệt (Negative pair)
    keypoint_weight: 0.3
    description: Khi cặp mẫu thuộc hai thực thể khác biệt (Nhãn $Y=1$), công thức chuyển sang dạng phạt dựa trên lề an toàn Margin ($m$): $L = \frac{1}{2} \max(0, m - D_w)^2$. Nếu khoảng cách hiện tại $D_w$ đã lớn hơn $m$, loss bằng 0; nếu nhỏ hơn, hệ thống sẽ trừng phạt nặng và đẩy tách xa hai vectơ này ra ngoài phạm vi lề $m$.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích nguyên lý hoạt động của giải thuật Di truyền (Genetic Algorithm - GA) khi áp dụng vào bài toán tối ưu hóa lựa chọn siêu tham số tự động. Giải thích ý nghĩa của các bước toán tử sinh học: Crossover (Lai ghép) và Mutation (Đột biến).
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế mã hóa nhiễm sắc thể và đánh giá hàm thích nghi (Fitness Function)
    keypoint_weight: 0.4
    description: Giải thuật Di truyền mã hóa các tổ hợp siêu tham số thành một chuỗi nhị phân hoặc chuỗi số đại diện cho một Nhiễm sắc thể (Chromosome/Individual). GA khởi tạo một quần thể (Population) gồm nhiều cá thể ngẫu nhiên, sau đó huấn luyện mô hình học máy để tính toán chỉ số hiệu năng (như F1-score) làm Hàm thích nghi (Fitness Function) chấm điểm sinh tồn cho từng cá thể.
  - id: KP9_2
    content: Nguyên lý toán tử Lai ghép (Crossover) bảo tồn đặc trưng tốt của thế hệ trước
    keypoint_weight: 0.3
    description: Toán tử Crossover chọn lọc các cá thể có điểm Fitness cao làm bố mẹ, thực hiện trao đổi chéo các đoạn mã cấu trúc siêu tham số tại một hoặc nhiều điểm cắt ngẫu nhiên để sinh ra các cá thể con đời sau, giúp thế hệ sau kế thừa và tích tụ các vùng không gian siêu tham số tốt từ thế hệ trước để tăng tốc hướng đích.
  - id: KP9_3
    content: Nguyên lý toán tử Đột biến (Mutation) tạo đột phá không gian thoát bẫy cực trị cục bộ
    keypoint_weight: 0.3
    description: Toán tử Mutation chủ động lật ngẫu nhiên một vài bit hoặc thay đổi nhỏ giá trị siêu tham số trong chuỗi mã hóa của cá thể con với một xác suất rất nhỏ. Cơ chế này đưa các đặc trưng hoàn toàn mới vào quần thể, tạo động lực giúp thuật toán thực hiện chiến lược khám phá (Exploration) vào các vùng không gian xa lạ, giúp hệ thống thoát khỏi các bẫy điểm cực trị cục bộ.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thuật toán giảm chiều t-SNE bảo toàn cấu trúc cục bộ bằng cách ánh xạ khoảng cách thành xác suất tương đồng. Hãy phân tích bản chất toán học của tiến trình tối ưu hóa hàm mục tiêu Kullback-Leibler (KL) Divergence bằng thuật toán Gradient Descent trong t-SNE. Tại sao tiến trình này lại tốn chi phí tài nguyên tính toán cực kỳ lớn hằng ngày?
* **expected_key_points:**
  - id: KP10_1
    content: Công thức toán học đo lường độ chênh lệch thông tin của hàm mục tiêu KL Divergence
    keypoint_weight: 0.4
    description: Hàm mục tiêu của t-SNE tối ưu hóa việc giảm thiểu độ chênh lệch thông tin giữa phân phối xác suất tương đồng không gian cao ($P$) và không gian thấp ($Q$): $KL(P||Q) = \sum_{i} \sum_{j} p_{ij} \log \frac{p_{ij}}{q_{ij}}$. Đạo hàm của hàm lỗi này đối với tọa độ điểm ở không gian thấp tạo ra một hệ thống lực kéo vật lý (Lực hút giữa các điểm tương đồng và lực đẩy giữa các điểm khác biệt).
  - id: KP10_2
    content: Bản chất toán học của phép toán cặp đôi trong ma trận xác suất (N-to-N interaction)
    keypoint_weight: 0.4
    description: Để tính toán phân phối $Q$ và gradient tại mỗi bước lặp, công thức bắt buộc phải tính tổng chuẩn hóa ở mẫu số chứa khoảng cách của tất cả các cặp điểm có thể có trong không gian thấp: $q_{ij} = \frac{(1 + ||y_i - y_j||^2)^{-1}}{\sum_{k} \sum_{l \neq k} (1 + ||y_k - y_l||^2)^{-1}}$. Phép toán này yêu cầu sự tương tác cặp đôi toàn cục, đẩy độ phức tạp thuật toán lên mức bình phương kích thước mẫu $O(N^2)$.
  - id: KP10_3
    content: Chi phí tài nguyên bùng nổ khi tăng kích thước mẫu dữ liệu đầu vào
    keypoint_weight: 0.2
    description: Do độ phức tạp là $O(N^2)$, khi kích thước mẫu $N$ tăng lên quy mô lớn, số lượng phép toán ma trận cần tính ở runtime sẽ bùng nổ theo hàm mũ, làm cạn kiệt băng thông RAM và CPU, khiến t-SNE thuần túy không thể mở rộng cho các tập dữ liệu Big Data nếu không áp dụng các giải thuật tối ưu xấp xỉ như Barnes-Hut ($O(N \log N)$).