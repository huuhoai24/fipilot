# Bộ Câu Hỏi Phỏng Vấn Data Scientist (Level 1)

* **Role:** Data Scientist
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong xử lý ngôn ngữ tự nhiên (NLP), kỹ thuật TF-IDF (Term Frequency - Inverse Document Frequency) dùng để làm gì? Hãy giải thích ý nghĩa độc lập của hai thành phần cấu thành nên chỉ số này.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa cấu trúc toán học và ý nghĩa của TF (Term Frequency)
    keypoint_weight: 0.4
    description: TF đo lường tần suất xuất hiện của một từ khóa trong một văn bản cụ thể. Số lần xuất hiện càng nhiều chứng tỏ từ đó càng quan trọng đối với nội dung của chính văn bản đó.
  - id: KP1_2
    content: Định nghĩa cấu trúc toán học và ý nghĩa của IDF (Inverse Document Frequency)
    keypoint_weight: 0.4
    description: IDF đo lường mức độ phổ biến của từ khóa trên toàn bộ tập văn bản (Corpus) bằng cách tính hàm logarit nghịch đảo của tỷ lệ văn bản chứa từ đó. Từ nào xuất hiện ở quá nhiều văn bản khác nhau (như từ 'và', 'thì', 'là') sẽ có giá trị IDF thấp vì nó không có tính chất phân tách ngữ cảnh độc đáo.
  - id: KP1_3
    content: Mục tiêu tổng hợp của chỉ số TF-IDF đối với trích chọn đặc trưng
    keypoint_weight: 0.2
    description: TF-IDF kết hợp tích số của hai chỉ số trên để gán trọng số cho từ khóa, giúp chuyển đổi văn bản thô thành vectơ số, làm nổi bật các từ mang nhiều giá trị đặc trưng nhất của từng văn bản để đưa vào mô hình học máy.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Thuật toán phân loại Naive Bayes dựa trên định lý Bayes trong xác suất. Hãy giải thích tại sao thuật toán này lại có tên gọi là "Naive" (Ngây thơ) và hiện tượng "Zero-Frequency Problem" (Vấn đề tần suất bằng 0) là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Giả định ngây thơ về tính độc lập có điều kiện giữa các đặc trưng
    keypoint_weight: 0.5
    description: Thuật toán gọi là "Ngây thơ" vì nó dựa trên một giả định toán học cực kỳ đơn giản hóa và ít khi đúng trong thực tế: coi tất cả các đặc trưng đầu vào (Features) hoàn toàn độc lập và không có mối tương quan nào với nhau khi biết nhãn mục tiêu. Giả định này giúp đơn giản hóa phép nhân xác suất đồng thời, giảm thiểu tối đa chi phí tính toán.
  - id: KP2_2
    content: Bản chất triệt tiêu xác suất của hiện tượng Zero-Frequency
    keypoint_weight: 0.5
    description: Hiện tượng xảy ra khi một giá trị đặc trưng nào đó ở tập dữ liệu mới chưa từng xuất hiện cùng với nhãn mục tiêu trong quá trình huấn luyện, dẫn đến xác suất có điều kiện cục bộ bằng 0. Khi nhân chuỗi xác suất để tính toán, giá trị 0 này sẽ triệt tiêu hoàn toàn kết quả của toàn bộ biểu thức, khiến mô hình đưa ra dự báo sai lệch tuyệt đối. Khắc phục bằng kỹ thuật làm mịn Laplace (Laplace Smoothing).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong phân tích thống kê để khám phá dữ liệu (EDA), kiểm định ANOVA (Analysis of Variance) được sử dụng nhằm mục đích gì? Hãy phát biểu rõ ràng cấu trúc của giả thuyết không H0 và giả thuyết đối lập H1 của kiểm định này.
* **expected_key_points:**
  - id: KP3_1
    content: Mục tiêu toán học so sánh giá trị trung bình đa nhóm của ANOVA
    keypoint_weight: 0.5
    description: ANOVA là kỹ thuật kiểm định thống kê tham số được sử dụng để so sánh giá trị trung bình (Means) của một biến liên tục trên ba hoặc nhiều nhóm độc lập khác nhau, nhằm xác định xem sự khác biệt giữa các nhóm có ý nghĩa thống kê hay không.
  - id: KP3_2
    content: Phát biểu cấu trúc của giả thuyết không H0 và giả thuyết đối lập H1
    keypoint_weight: 0.5
    description: Giả thuyết không H0 phát biểu rằng giá trị trung bình của tất cả các nhóm hoàn toàn bằng nhau (Không có sự khác biệt). Giả thuyết đối lập H1 phát biểu rằng có ít nhất một cặp nhóm có giá trị trung bình khác nhau rõ rệt trong tổng thể.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Kỹ thuật Regularization rất quan trọng để kiểm soát Overfitting. Hãy giải thích nguyên lý hoạt động của ElasticNet Regularization và chỉ ra điểm vượt trội của nó so với việc áp dụng độc lập Lasso (L1) hoặc Ridge (L2) trong bài toán dữ liệu chứa nhiều biến đa cộng tuyến.
* **expected_key_points:**
  - id: KP4_1
    content: Công thức toán học tổ hợp tuyến tính của ElasticNet
    keypoint_weight: 0.4
    description: ElasticNet là sự kết hợp đồng thời cả hai thành phần phạt của L1 (Lasso) và L2 (Ridge) vào hàm mất mát của mô hình hồi quy thông qua hai siêu tham số điều khiển. Công thức phạt tổng quát: L = Loss + l1_ratio * ||w||_1 + (1 - l1_ratio) * ||w||_2^2.
  - id: KP4_2
    content: Điểm hạn chế của Lasso độc lập khi xử lý nhóm biến cộng tuyến mạnh
    keypoint_weight: 0.3
    description: Khi đối mặt với một nhóm các biến độc lập có mối tương quan cực kỳ mạnh mẽ với nhau, thuật toán Lasso (L1) thuần túy có xu hướng chọn ngẫu nhiên duy nhất một biến trong nhóm và ép các hệ số còn lại về bằng 0 tuyệt đối, làm mất thông tin ngữ cảnh tổng thể của nhóm biến đó.
  - id: KP4_3
    content: Giải pháp hiệu ứng nhóm (Group Effect) của ElasticNet
    keypoint_weight: 0.3
    description: Nhờ tích hợp thêm thành phần L2 của Ridge, ElasticNet khắc phục được khuyết điểm trên bằng cách tạo ra hiệu ứng nhóm (Group Effect). Hệ thống sẽ giữ lại hoặc thu nhỏ đồng đều các trọng số của cả nhóm biến có mối tương quan mạnh mẽ, giúp mô hình ổn định hơn và bảo toàn thông tin phân tích cấu trúc tốt hơn.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong xây dựng mô hình học máy, kỹ thuật lựa chọn đặc trưng RFE (Recursive Feature Elimination) hoạt động ra sao? Hãy nêu rõ tiêu chí toán học mà RFE dựa vào để loại bỏ các đặc trưng qua từng vòng lặp.
* **expected_key_points:**
  - id: KP5_1
    content: Quy trình lặp duyệt loại bỏ dần theo chuỗi của thuật toán RFE
    keypoint_weight: 0.5
    description: RFE là phương pháp lựa chọn đặc trưng theo trường phái Wrapper. Thuật toán bắt đầu bằng việc huấn luyện mô hình trên toàn bộ tập đặc trưng ban đầu. Sau đó, nó thực hiện một chuỗi lặp: đo lường độ quan trọng, loại bỏ một hoặc một nhóm các đặc trưng kém quan trọng nhất, rồi lại huấn luyện lại mô hình trên tập đặc trưng còn lại. Quá trình này lặp đi lặp lại cho đến khi đạt được số lượng đặc trưng tối ưu mong muốn.
  - id: KP5_2
    content: Tiêu chí toán học đo lường độ quan trọng đặc trưng (Feature Importance / Coefficients)
    keypoint_weight: 0.5
    description: RFE phụ thuộc vào một mô hình cốt lõi bên dưới (như Linear Regression hoặc SVM). Tiêu chí toán học để RFE đánh giá và loại bỏ đặc trưng dựa trực tiếp vào độ lớn tuyệt đối của các hệ số trọng số hồi quy (Coefficients) hoặc chỉ số độ quan trọng của các vết cắt trong cây quyết định (Feature Importances). Biến có trọng số nhỏ nhất sẽ bị loại bỏ trước.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Thuật toán Hierarchical Clustering (Phân cụm phân cấp) hoạt động dựa trên cơ chế gộp dần từ dưới lên (Agglomerative). Hãy phân biệt sự khác biệt về mặt logic toán học của ba kỹ thuật liên kết khoảng cách (Linkage Criteria): Single Linkage, Complete Linkage và Average Linkage.
* **expected_key_points:**
  - id: KP6_1
    content: Logic khoảng cách tối thiểu của Single Linkage
    keypoint_weight: 0.4
    description: Single Linkage định nghĩa khoảng cách giữa hai cụm là khoảng cách ngắn nhất (tối thiểu) giữa một điểm bất kỳ thuộc cụm thứ nhất và một điểm bất kỳ thuộc cụm thứ hai. Kỹ thuật này dễ tạo ra hiện tượng kéo chuỗi dài (Chaining effect), làm các cụm bị phình to bề ngang bất hợp lý.
  - id: KP6_2
    content: Logic khoảng cách tối đa của Complete Linkage
    keypoint_weight: 0.3
    description: Complete Linkage định nghĩa khoảng cách giữa hai cụm là khoảng cách dài nhất (tối đa) giữa một điểm thuộc cụm thứ nhất và một điểm thuộc cụm thứ hai. Kỹ thuật này có xu hướng tạo ra các cụm có cấu trúc hình học tròn, gọn góc và kích thước đồng đều hơn.
  - id: KP6_3
    content: Logic khoảng cách trung bình tổng thể của Average Linkage
    keypoint_weight: 0.3
    description: Average Linkage tính toán giá trị trung bình cộng của tất cả các cặp khoảng cách giữa mọi điểm thuộc cụm thứ nhất và mọi điểm thuộc cụm thứ hai. Kỹ thuật này trung hòa hai phương pháp trên và có độ ổn định cao trước dữ liệu chứa nhiều nhiễu.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong các bài toán hồi quy (Regression), hàm mất mát Huber Loss thường được sử dụng như một giải pháp thay thế thông minh cho MSE và MAE. Hãy giải thích công thức logic hoạt động và ưu điểm hình học của Huber Loss đối với dữ liệu chứa nhiều nhiễu ngoại lai.
* **expected_key_points:**
  - id: KP7_1
    content: Cơ chế phân tách điều kiện dựa trên ngưỡng Delta của Huber Loss
    keypoint_weight: 0.5
    description: Huber Loss phân tách hàm toán học thành hai phân vùng dựa trên một siêu tham số ngưỡng Delta ($\delta$). Khi sai số dự báo nhỏ hơn hoặc bằng Delta, Huber Loss áp dụng công thức của hàm bình phương MSE. Khi sai số dự báo vượt quá ngưỡng Delta, hàm tự động chuyển sang cấu trúc tuyến tính tuyệt đối của hàm MAE.
  - id: KP7_2
    content: Ưu điểm hình học cân bằng giữa tính ổn định và tính khả vi (Differentiability)
    keypoint_weight: 0.5
    description: Nhờ cơ chế lai ghép, Huber Loss tận dụng ưu điểm của MAE ở vùng biên ngoài để chống chịu hiệu quả với nhiễu ngoại lai (không phóng đại sai số lớn theo hàm mũ như MSE), đồng thời tận dụng ưu điểm của MSE ở vùng trung tâm giúp đồ thị mượt mà và khả vi liên tục (Differentiable) tại điểm sai số bằng 0, giúp thuật toán Gradient Descent hội tụ ổn định, không bị dao động như khi dùng MAE thuần túy.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Mô hình Support Vector Regression (SVR) áp dụng triết lý hình học của SVM cho bài toán hồi quy. Hãy giải thích ý nghĩa toán học của khái niệm "Epsilon-insensitive tube" (Ống không nhạy cảm epsilon) và siêu tham số phạt $C$ ảnh hưởng thế nào đến việc tối ưu hóa hàm mục tiêu của SVR.
* **expected_key_points:**
  - id: KP8_1
    content: Ý nghĩa hình học vùng không phạt của Epsilon-insensitive tube
    keypoint_weight: 0.4
    description: Ống không nhạy cảm Epsilon ($\epsilon$) xác định một vùng không gian ranh giới song hành bao quanh đường dự báo hồi quy với khoảng cách độ rộng bằng $\epsilon$. Mọi điểm dữ liệu huấn luyện nằm hoàn toàn bên trong chiếc ống này sẽ có sai số dự báo bằng 0 đối với hàm mục tiêu, nghĩa là hệ thống hoàn toàn không trừng phạt các sai số nhỏ nằm trong ngưỡng Epsilon.
  - id: KP8_2
    content: Cơ chế trừng phạt sai số ngoài ống thông qua biến bù lỗi (Slack Variables)
    keypoint_weight: 0.3
    description: Các điểm dữ liệu nằm văng ra ngoài phạm vi của ống Epsilon sẽ bị tính toán sai số vật lý thực tế. Mức độ sai lệch này được đo lường thông qua các biến bù lỗi (Slack Variables $\xi_i, \xi_i^*$), biểu thị khoảng cách từ điểm đó đến biên gần nhất của chiếc ống.
  - id: KP8_3
    content: Bản chất đánh đổi của siêu tham số phạt $C$ trong hàm mục tiêu tối ưu
    keypoint_weight: 0.3
    description: Siêu tham số $C$ quy định tỷ lệ đánh đổi giữa độ lớn của lề phẳng (độ mượt của đường hồi quy) và tổng hình phạt sai số của các điểm nằm ngoài ống Epsilon. Khi cấu hình $C$ quá lớn, mô hình tập trung trừng phạt nặng sai số ngoài ống, khiến đường hồi quy phải uốn lượn liên tục để gom điểm, dẫn đến hiện tượng Overfitting. Khi $C$ nhỏ, mô hình ưu tiên độ phẳng mịn toàn cục, chấp nhận nhiều điểm rơi ngoài ống, dễ dẫn đến Underfitting.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong kiến trúc mạng nơ-ron tích chập (Convolutional Neural Networks - CNN), phép toán Tích chập (Convolution) hoạt động dựa trên nguyên lý toán học nào? Hãy phân tích ý nghĩa của cấu trúc chia sẻ trọng số (Weight Sharing) và tính bất biến tịnh tiến (Translation Invariance) đối với việc xử lý dữ liệu hình ảnh đa chiều.
* **expected_key_points:**
  - id: KP9_1
    content: Bản chất phép toán trượt nhân ma trận của tầng Convolutional
    keypoint_weight: 0.4
    description: Phép toán tích chập thực hiện việc trượt một ma trận bộ lọc nhỏ (Kernel/Filter) tuần tự trên không gian của ma trận ảnh gốc đầu vào. Tại mỗi vị trí dừng, hệ thống tính tổng các tích số của từng phần tử tương ứng (Element-wise multiplication and summation) để trích xuất ra một ma trận đặc trưng mới (Feature Map).
  - id: KP9_2
    content: Nguyên lý giảm thiểu tham số nhờ cấu trúc chia sẻ trọng số (Weight Sharing)
    keypoint_weight: 0.3
    description: Chia sẻ trọng số quy định rằng các hệ số trong ma trận của một bộ lọc (Kernel) sẽ được sử dụng lặp đi lặp lại ở tất cả các vị trí không gian khi quét qua bức ảnh. Cơ chế này giúp triệt tiêu hoàn toàn sự bùng nổ số lượng tham số huấn luyện so với mạng liên kết toàn bộ (Fully Connected), bảo vệ hệ thống khỏi hiện tượng Overfitting nặng nề khi xử lý ảnh độ phân giải lớn.
  - id: KP9_3
    content: Khả năng nhận diện đặc trưng bất kể vị trí của tính bất biến tịnh tiến (Translation Invariance)
    keypoint_weight: 0.3
    description: Nhờ phép toán tích chập quét đều khắp không gian kết hợp với tầng gộp Pooling, mạng CNN đạt được tính chất bất biến tịnh tiến. Nghĩa là nếu một đặc trưng cấu trúc (như góc cạnh, hình dáng đồ vật) di chuyển tịnh tiến sang bất kỳ vị trí nào khác trên bức ảnh, bộ lọc vẫn có khả năng kích hoạt và nhận diện chính xác đặc trưng đó, nâng cao năng lực tổng quát hóa.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thuật toán tối ưu hóa Adam (Adaptive Moment Estimation) là một trong những giải thuật phổ biến nhất trong Deep Learning. Hãy giải thích bản chất toán học của Adam khi nó kết hợp cả hai cơ chế: Động lượng (Momentum) và Tốc độ học thích ứng theo từng tham số (RMSProp).
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế tính toán mô-men đại lượng cấp một mô phỏng Momentum
    keypoint_weight: 0.4
    description: Adam duy trì và tính toán giá trị trung bình trượt có trọng số mũ của các vectơ đạo hàm gradient quá khứ ($m_t$), đại diện cho Mô-men đại lượng cấp một (First Moment). Cơ chế này mô phỏng lại gia tốc động lượng của vật lý, giúp mô hình triệt tiêu các dao động nhiễu ngang và tăng tốc lao thẳng về hướng điểm cực tiểu của hàm lỗi.
  - id: KP10_2
    content: Cơ chế điều chỉnh tốc độ học thích ứng dựa trên mô-men đại lượng cấp hai của RMSProp
    keypoint_weight: 0.4
    description: Đồng thời, Adam tính toán giá trị trung bình trượt có trọng số mũ của bình phương các vectơ đạo hàm gradient quá khứ ($v_t$), đại diện cho Mô-men đại lượng cấp hai (Second Moment). Khi cập nhật trọng số, Adam chia nhỏ Learning rate cho căn bậc hai của $v_t$. Điều này giúp tự động điều chỉnh tốc độ học thích ứng cho từng tham số độc lập: tham số nào có gradient biến động lớn sẽ bị kìm hãm bước nhảy ngắn lại, tham số nào có gradient nhỏ và thưa thớt sẽ được kéo bước nhảy dài ra để nhanh hội tụ.
  - id: KP10_3
    content: Cơ chế hiệu chỉnh sai lệch ở các bước lặp đầu tiên (Bias Correction)
    keypoint_weight: 0.2
    description: Do các giá trị mô-men $m_t$ và $v_t$ thường được khởi tạo bằng vectơ số 0 ở thời điểm ban đầu, chúng bị sai lệch dịch chuyển tiến về sát gốc 0 trong các bước lặp đầu tiên. Adam giải quyết bài toán này bằng cách đưa thêm các công thức hiệu chỉnh sai lệch toán học (Bias Correction terms: $\hat{m}_t = m_t / (1 - \beta_1^t)$ và $\hat{v}_t = v_t / (1 - \beta_2^t)$) để chuẩn hóa lại giá trị chuyển dịch ở những vòng lặp đầu.