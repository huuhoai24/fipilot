# Bộ Câu Hỏi Phỏng Vấn Data Scientist (Level 1)

* **Role:** Data Scientist
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thống kê ứng dụng và học máy, hãy phát biểu nội dung và ý nghĩa thực tế của Định lý giới hạn trung tâm (Central Limit Theorem - CLT). Định lý này giúp ích gì khi chúng ta cần thực hiện các kiểm định thống kê trên tập dữ liệu lớn?
* **expected_key_points:**
  - id: KP1_1
    content: Nội dung toán học về sự hội tụ phân phối của CLT
    keypoint_weight: 0.5
    description: Định lý giới hạn trung tâm phát biểu rằng khi kích thước mẫu (n) đủ lớn (thường là n >= 30), phân phối chọn mẫu của số trung bình mẫu (Sampling Distribution of the Sample Mean) sẽ hội tụ về phân phối chuẩn (Normal Distribution), bất kể tổng thể ban đầu tuân theo hình dạng phân phối nào.
  - id: KP1_2
    content: Ý nghĩa thực tế đối với các kiểm định tham số (Parametric Tests)
    keypoint_weight: 0.5
    description: CLT cho phép các nhà khoa học dữ liệu áp dụng một cách an toàn các kỹ thuật kiểm định tham số phổ biến (như t-test, ANOVA) hoặc xây dựng khoảng tin cậy trên tập dữ liệu thực tế hằng ngày mà không cần phải lo lắng hay chứng minh tổng thể gốc có phân phối chuẩn hay không.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong giai đoạn làm sạch dữ liệu (Data Cleaning), hãy nêu hai tác động tiêu cực của các giá trị ngoại lai (Outliers) đối với các mô hình hồi quy tuyến tính. Trình bày phương pháp nhận diện ngoại lai dựa trên chỉ số IQR (Interquartile Range).
* **expected_key_points:**
  - id: KP2_1
    content: Hệ quả tiêu cực của Outliers lên đường hồi quy tuyến tính
    keypoint_weight: 0.4
    description: Outliers làm dịch chuyển đường hồi quy tuyến tính ra khỏi xu hướng chung của đại đa số dữ liệu vì hàm mất mát MSE cố gắng giảm thiểu bình phương sai số của các điểm cực biên này. Điều này làm sai lệch nghiêm trọng các hệ số trọng số và làm giảm mạnh khả năng tổng quát hóa của mô hình.
  - id: KP2_2
    content: Định nghĩa dải IQR dựa trên các phân vị (Tứ phân vị)
    keypoint_weight: 0.3
    description: IQR là khoảng biến thiên tứ phân vị, được tính bằng hiệu số giữa tứ phân vị thứ ba (Q3 - phân vị 75%) và tứ phân vị thứ nhất (Q1 - phân vị 25%): IQR = Q3 - Q1. Nó đại diện cho dải không gian chứa 50% lượng dữ liệu ở trung tâm.
  - id: KP2_3
    content: Tiêu chuẩn toán học để xác định ranh giới cắt Outliers
    keypoint_weight: 0.3
    description: Một điểm dữ liệu được xác định là ngoại lai (Outlier) nếu nó nằm ngoài khoảng ranh giới an toàn: Lower Bound = Q1 - 1.5 * IQR hoặc Upper Bound = Q3 + 1.5 * IQR.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong các thuật toán học máy phân lớp, hãy phân biệt sự khác biệt về mặt triết lý thiết kế hệ thống giữa hai trường phái: Generative Models (Mô hình tạo sinh - như Naive Bayes) và Discriminative Models (Mô hình phân biệt - như Logistic Regression).
* **expected_key_points:**
  - id: KP3_1
    content: Triết lý học phân phối xác suất đồng thời của Generative Models
    keypoint_weight: 0.5
    description: Mô hình tạo sinh tìm cách học và mô hình hóa phân phối xác suất đồng thời P(X, Y) của cả đặc trưng đầu vào X và nhãn mục tiêu Y. Từ đó, mô hình hiểu được cách dữ liệu được sinh ra như thế nào để tính toán xác suất hậu nghiệm P(Y|X) thông qua định lý Bayes.
  - id: KP3_2
    content: Triết lý học ranh giới phân tách trực tiếp của Discriminative Models
    keypoint_weight: 0.5
    description: Mô hình phân biệt bỏ qua việc tìm hiểu cách dữ liệu được sinh ra, tập trung trực tiếp vào việc học phân phối xác suất điều kiện P(Y|X) hoặc xây dựng ranh giới quyết định (Decision Boundary) để phân tách các lớp dữ liệu trong không gian đặc trưng.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi đo lường hiệu năng của bài toán hồi quy (Regression), hãy phân biệt sự khác biệt về mặt công thức toán học và mức độ nhạy cảm đối với lỗi lớn giữa hai chỉ số: MAE (Mean Absolute Error) và RMSE (Mean Squared Error).
* **expected_key_points:**
  - id: KP4_1
    content: Bản chất toán học sai số tuyến tính của chỉ số MAE
    keypoint_weight: 0.4
    description: MAE tính toán giá trị trung bình của tổng các khoảng cách tuyệt đối giữa giá trị dự báo và giá trị thực tế. Do không sử dụng phép nâng lũy thừa, MAE đối xử với mọi mức độ lỗi một cách tuyến tính và đồng đều, phản ánh chính xác mức độ sai số trung bình thực tế.
  - id: KP4_2
    content: Cơ chế trừng phạt nặng sai số lớn bằng phép bình phương của RMSE
    keypoint_weight: 0.4
    description: RMSE tính căn bậc hai của trung bình tổng bình phương các sai số. Do có phép bình phương trước khi lấy căn, các lỗi có khoảng cách lớn sẽ bị phóng đại và trừng phạt nặng nề hơn rất nhiều so với các lỗi nhỏ, khiến RMSE trở nên cực kỳ nhạy cảm với các điểm dữ liệu dự báo sai lệch nghiêm trọng.
  - id: KP4_3
    content: Ngữ cảnh lựa chọn áp dụng chỉ số phù hợp trong thực tế
    keypoint_weight: 0.2
    description: Nên chọn RMSE khi hệ thống doanh nghiệp coi các lỗi lớn là thảm họa cần tránh tuyệt đối (ví dụ: dự báo dòng tiền hệ thống). Nên chọn MAE khi dữ liệu thô chứa nhiều nhiễu bất khả kháng và ta muốn mô hình hoạt động ổn định, không bị chi phối quá mức bởi outliers.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong huấn luyện các mô hình học máy bằng thuật toán Gradient Descent, siêu tham số Learning Rate (Tốc độ học) thường được điều chỉnh động qua cơ chế Learning Rate Decay (Suy giảm tốc độ học). Hãy giải thích nguyên lý và mục đích của cơ chế này.
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế tự động co rút bước nhảy theo tiến trình huấn luyện
    keypoint_weight: 0.5
    description: Learning Rate Decay là kỹ thuật tự động giảm dần giá trị của Learning Rate theo thời gian hoặc theo số lượng vòng lặp (Epochs) huấn luyện dựa trên một hàm quy luật xác định (như suy giảm theo hàm mũ, hàm tuyến tính hoặc theo chu kỳ step).
  - id: KP5_2
    content: Động lực tối ưu hóa tốc độ ở giai đoạn đầu và tính hội tụ ổn định ở giai đoạn cuối
    keypoint_weight: 0.5
    description: Ở giai đoạn đầu, Learning Rate lớn giúp mô hình di chuyển nhanh, tiết kiệm thời gian và dễ dàng nhảy qua các điểm cực tiểu cục bộ nông. Ở giai đoạn cuối, khi đã tiến sát đáy hàm lỗi, Learning Rate nhỏ dần giúp các bước nhảy ngắn lại, tránh hiện tượng dao động vượt quá điểm tối ưu (Overshooting) và đảm bảo mô hình hội tụ ổn định vào điểm cực tiểu toàn cục.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Thuật toán DBSCAN (Density-Based Spatial Clustering of Applications with Noise) là một phương pháp phân cụm dựa trên mật độ. Hãy giải thích ý nghĩa của hai siêu tham số Eps (Epsilon) và MinPts (Minimum Points) cùng cơ chế nhận diện điểm nhiễu (Noise Points) của thuật toán này.
* **expected_key_points:**
  - id: KP6_1
    content: Vai trò định nghĩa không gian hình học của siêu tham số Eps và MinPts
    keypoint_weight: 0.4
    description: Eps xác định bán kính vùng lân cận hình học xung quanh một điểm dữ liệu. MinPts quy định số lượng điểm tối thiểu bắt buộc phải nằm trong vùng bán kính Eps đó để một điểm có thể được xác lập tư cách là một điểm lõi (Core Point).
  - id: KP6_2
    content: Cơ chế phân loại các loại điểm (Core, Border) dựa trên mật độ
    keypoint_weight: 0.3
    description: Điểm lõi (Core Point) có số điểm lân cận >= MinPts. Điểm biên (Border Point) có số điểm lân cận < MinPts nhưng bản thân nó lại nằm trong vùng bán kính Eps của một điểm lõi khác. Thuật toán loan tỏa cụm từ các điểm lõi này.
  - id: KP6_3
    content: Cơ chế cô lập và nhận diện điểm nhiễu tự động (Noise Points)
    keypoint_weight: 0.3
    description: Một điểm được xác định là Điểm nhiễu (Noise Point) nếu nó không phải là điểm lõi và đồng thời không nằm trong vùng lân cận của bất kỳ điểm lõi nào. DBSCAN tự động cô lập các điểm này ra khỏi tất cả các cụm, giúp mô hình có khả năng chống nhiễu cực tốt mà không cần định trước số lượng cụm K.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi đánh giá hiệu năng của mô hình hồi quy Logistic cho bài toán phân lớp nhị phân, hãy giải thích ý nghĩa toán học của hàm Log Loss (Cross-Entropy Loss). Tại sao hàm này lại trừng phạt cực kỳ nghiêm khắc những dự báo sai mà mô hình lại quá tự tin?
* **expected_key_points:**
  - id: KP7_1
    content: Công thức và bản chất tính toán xác suất của hàm Log Loss
    keypoint_weight: 0.5
    description: Log Loss đo lường hiệu năng bằng cách tính toán khoảng cách thông tin dựa trên hàm logarithm âm của xác suất dự báo đúng nhãn thực tế: Loss = -[y*ln(p) + (1-y)*ln(1-p)]. Giá trị Loss bằng 0 khi xác suất dự báo trùng khớp hoàn hảo với nhãn thực tế.
  - id: KP7_2
    content: Cơ chế tiệm cận vô hạn của hàm logarit trừng phạt lỗi tự tin sai (High confidence errors)
    keypoint_weight: 0.5
    description: Do đặc tính hình học của hàm logarithm âm ($-ln(p)$), khi xác suất dự báo đúng nhãn $p$ tiến dần về sát mốc 0, giá trị của hàm loss sẽ tăng vọt lên rất nhanh theo đồ thị hàm mũ tiệm cận về mức dương vô cùng ($+\infty$). Do đó, nếu mô hình dự báo một mẫu là nhãn 1 với độ tự tin cực cao ($p=0.999$) nhưng thực tế nhãn lại là 0, giá trị Log Loss tổng thể sẽ bị kéo phình to khủng khiếp, ép buộc mô hình phải sửa chữa độ tự tin vô căn cứ này.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong mô hình Support Vector Machine (SVM), hàm nhân RBF (Radial Basis Function / Gaussian Kernel) là một công cụ phi tuyến tính cực mạnh. Hãy giải thích nguyên lý toán học của siêu tham số Gamma ($\gamma$) trong hàm nhân RBF và tác động của việc cấu hình Gamma quá nhỏ hoặc quá lớn đến ranh giới quyết định (Decision Boundary).
* **expected_key_points:**
  - id: KP8_1
    content: Công thức toán học và ý nghĩa hình học khoảng cách của Kernel RBF
    keypoint_weight: 0.4
    description: Kernel RBF tính toán giá trị tương đồng dựa trên khoảng cách hình học Gauss: $K(x, x') = \exp(-\gamma ||x - x'||^2)$. Siêu tham số Gamma ($\gamma$) quy định tỷ lệ nghịch với bán kính ảnh hưởng của các vectơ hỗ trợ (Support Vectors) lên ranh giới quyết định.
  - id: KP8_2
    content: Hệ quả cấu hình Gamma quá lớn gây co cụm biên (Overfitting)
    keypoint_weight: 0.3
    description: Khi Gamma quá lớn, vùng không gian ảnh hưởng của từng vectơ hỗ trợ riêng lẻ bị thu hẹp lại rất nhỏ. Ranh giới quyết định sẽ phải uốn lượn liên tục, tạo ra các "hòn đảo" cục bộ bao quanh chặt chẽ từng điểm dữ liệu huấn luyện đơn lẻ, dẫn đến hiện tượng mô hình học thuộc lòng và bị Overfitting nặng nề.
  - id: KP8_3
    content: Hệ quả cấu hình Gamma quá nhỏ gây phẳng hóa ranh giới biên (Underfitting)
    keypoint_weight: 0.3
    description: Khi Gamma quá nhỏ, bán kính không gian ảnh hưởng của các vectơ hỗ trợ phình to diện rộng trên toàn cục. Hệ thống coi các điểm ở xa vẫn có mối liên quan mạnh mẽ, làm ranh giới quyết định bị phẳng hóa quá mức, không thể bắt được các cấu trúc phi tuyến tính phức tạp của dữ liệu, dẫn đến hiện tượng Underfitting.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Kỹ thuật giảm chiều dữ liệu t-SNE (t-Distributed Stochastic Neighbor Embedding) thường được sử dụng để trực quan hóa dữ liệu có số chiều lớn. Hãy giải thích nguyên lý toán học giúp t-SNE bảo toàn được cấu trúc cấu trúc cục bộ (Local Structure) và cách nó sử dụng phân phối t-Student để giải quyết bài toán sụp đổ không gian (Crowding Problem) mà PCA gặp phải.
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế chuyển đổi khoảng cách hình học thành phân phối xác suất điều kiện
    keypoint_weight: 0.4
    description: t-SNE chuyển đổi khoảng cách Euclidean giữa các cặp điểm trong không gian cao thành các giá trị xác suất điều kiện biểu thị độ tương đồng (Similarity). Điểm gần nhau có xác suất cao, điểm xa có xác suất tiệm cận 0. Mục tiêu là tối ưu hóa để phân phối xác suất ở không gian thấp gần nhất với phân phối ở không gian cao thông qua giảm thiểu độ chênh lệch Kullback-Leibler (KL Divergence).
  - id: KP9_2
    content: Bản chất toán học của bài toán Crowding Problem khi giảm chiều dữ liệu
    keypoint_weight: 0.3
    description: Khi ép dữ liệu từ không gian nhiều chiều (ví dụ 100 chiều) về không gian ít chiều (2 chiều), thể tích không gian bị co rút theo hàm mũ. Các điểm ở khoảng cách trung bình trong không gian cao sẽ không có đủ không gian hình học để phân bổ ở không gian thấp, dẫn đến việc chúng bị dồn ứ, đè lên nhau và xóa sạch cấu trúc phân cụm cục bộ (Crowding Problem).
  - id: KP9_3
    content: Cơ chế sử dụng đuôi dài của phân phối t-Student để đẩy giãn cách dữ liệu ở không gian thấp
    keypoint_weight: 0.3
    description: t-SNE giải quyết triệt để vấn đề này bằng cách áp dụng phân phối t-Student với 1 độ tự do (đồ thị Cauchy) ở không gian thấp thay vì dùng phân phối chuẩn Gauss. Phân phối t-Student có phần đuôi dài hơn và dày hơn rất nhiều (Heavy-tailed); để đạt cùng một mức xác suất tương đồng như không gian cao, các điểm ở khoảng cách trung bình buộc phải được đẩy ra xa nhau hơn rất nhiều trong không gian 2D, giúp giải phóng không gian và làm hiển thị rõ ràng cấu trúc phân cụm cục bộ.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong các bài toán tối ưu hóa của học máy tiên tiến, thuật toán Stochastic Gradient Descent (SGD) thường bị mất ổn định hoặc kẹt ở các điểm Yên ngựa (Saddle Points) trên bề mặt lỗi. Hãy giải thích nguyên lý toán học của cơ chế "Momentum" (Động lượng) giúp thuật toán này vượt qua các điểm bẫy hình học nói trên để tăng tốc hội tụ.
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế tích lũy lịch sử bước đi dựa trên vận tốc toán học
    keypoint_weight: 0.4
    description: Cơ chế Momentum mô phỏng lại hiện tượng vật lý của một quả cầu lăn từ trên đỉnh dốc xuống. Nó đưa thêm một biến vận tốc $v_t$ để tích lũy giá trị trung bình trượt có trọng số mũ (Exponential moving average) của tất cả các vectơ gradient từ các bước thời gian quá khứ: $v_t = \beta v_{t-1} + \alpha \nabla L(w)$.
  - id: KP10_2
    content: Bản chất triệt tiêu dao động nhiễu và tăng tốc hướng đích
    keypoint_weight: 0.4
    description: Khi di chuyển qua các thung lũng dốc có bề mặt gồ ghề, các thành phần gradient theo hướng nhiễu ngang sẽ mang dấu trái ngược nhau qua các bước và tự động triệt tiêu lẫn nhau khi cộng dồn. Trong khi đó, các thành phần gradient trỏ thẳng về hướng điểm cực tiểu luôn cùng dấu và được tích lũy cộng dồn, làm gia tăng động lượng di chuyển cực mạnh theo trục chính, giúp tăng tốc hội tụ vượt trội.
  - id: KP10_3
    content: Nguyên lý cơ năng vượt bẫy hình học tại điểm Yên ngựa (Saddle Points)
    keypoint_weight: 0.2
    description: Tại các điểm Yên ngựa (Saddle Points) hoặc vùng cao nguyên phẳng (Plateaus), giá trị đạo hàm gradient bằng 0 tuyệt đối ($\nabla L(w) = 0$). Thuật toán SGD thuần túy sẽ bị đứng im vĩnh viễn tại đây. Nhờ có Momentum, biến vận tốc quá khứ $v_{t-1}$ vẫn còn giữ giá trị cơ năng tích lũy trước đó, đẩy mô hình tiếp tục trượt thẳng qua vùng bẫy có đạo hàm bằng 0 này cho đến khi bắt được vùng dốc mới.