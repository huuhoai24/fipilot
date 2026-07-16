# Bộ Câu Hỏi Phỏng Vấn Data Scientist (Level 1)

* **Role:** Data Scientist
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong mô hình hồi quy Logistic (Logistic Regression) áp dụng cho bài toán phân lớp nhị phân, khái niệm Log-Odds (Logit) đại diện cho điều gì về mặt toán học? Hãy giải thích tại sao chúng ta cần sử dụng hàm hàm mũ hoặc hàm Sigmoid để chuyển đổi Log-Odds thành giá trị xác suất dự báo cuối cùng.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa bản chất toán học của tỷ lệ Log-Odds
    keypoint_weight: 0.5
    description: Log-Odds là logarit tự nhiên của tỷ số Odds, trong đó Odds bằng tỷ lệ xác suất xảy ra sự kiện chia cho xác suất không xảy ra sự kiện (p / (1 - p)). Log-Odds chuyển đổi miền giá trị xác suất từ khoảng giới hạn (0, 1) sang dải số thực vô hạn (-inf, +inf), giúp mô hình tuyến tính học các hệ số một cách dễ dàng.
  - id: KP1_2
    content: Nhiệm vụ ánh xạ dải số thực về miền xác suất của hàm Sigmoid
    keypoint_weight: 0.5
    description: Do đầu ra của phương trình tuyến tính là dải số thực vô hạn, hệ thống bắt buộc phải áp dụng hàm kích hoạt phi tuyến tính Sigmoid (hoặc hàm Logistic) để nén dải giá trị này quay ngược trở lại khoảng giới hạn nghiêm ngặt từ 0 đến 1, tạo thành một phân phối xác suất hợp lệ đại diện cho độ tự tin của dự báo.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong giai đoạn làm sạch dữ liệu (Data Cleaning), hãy nêu hai tác động tiêu cực của các giá trị ngoại lai (Outliers) đối với các mô hình hồi quy tuyến tính thông thường. Trình bày phương pháp nhận diện ngoại lai dựa trên chỉ số IQR (Interquartile Range).
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
* **Câu hỏi:** Trong các bài toán học máy phân lớp, hãy phân biệt sự khác biệt về mặt triết lý thiết kế hệ thống giữa hai trường phái: Generative Models (Mô hình tạo sinh - như Naive Bayes) và Discriminative Models (Mô hình phân biệt - như Logistic Regression).
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
* **Câu hỏi:** Khi đo lường hiệu năng của bài toán hồi quy (Regression), hãy phân biệt sự khác biệt về mặt công thức toán học và mức độ nhạy cảm đối với lỗi lớn giữa hai chỉ số: MAE (Mean Absolute Error) và RMSE (Root Mean Squared Error).
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
    description: Do đặc tính hình học của hàm logarithm âm (-ln(p)), khi xác suất dự báo đúng nhãn p tiến dần về sát mốc 0, giá trị của hàm loss sẽ tăng vọt lên rất nhanh theo đồ thị hàm mũ tiệm cận về mức dương vô cùng (+inf). Do đó, nếu mô hình dự báo một mẫu là nhãn 1 với độ tự tin cực cao (p=0.999) nhưng thực tế nhãn lại là 0, giá trị Log Loss tổng thể sẽ bị kéo phình to khủng khiếp, ép buộc mô hình phải sửa chữa độ tự tin vô căn cứ này.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Kỹ thuật Giảm chiều dữ liệu PCA (Principal Component Analysis) hoạt động dựa trên nguyên lý toán học nào để tìm ra các thành phần chính? Hãy giải thích mối liên quan giữa ma trận hiệp phương sai (Covariance Matrix), trị riêng (Eigenvalues) và vectơ riêng (Eigenvectors) trong tiến trình này.
* **expected_key_points:**
  - id: KP8_1
    content: Mục tiêu toán học tối đa hóa phương sai dữ liệu chiếu của PCA
    keypoint_weight: 0.4
    description: PCA thực hiện phép biến đổi tuyến tính để chiếu tập dữ liệu gốc từ không gian đa chiều về một không gian mới có số chiều nhỏ hơn, sao cho lượng thông tin được bảo toàn là lớn nhất. Tiêu chuẩn toán học để bảo toàn thông tin ở đây là tối đa hóa phương sai (Variance) của dữ liệu trên các trục tọa độ mới (Principal Components).
  - id: KP8_2
    content: Vai trò phân tích cấu trúc tương quan của Ma trận hiệp phương sai
    keypoint_weight: 0.3
    description: PCA tính toán ma trận hiệp phương sai (Covariance Matrix) từ tập dữ liệu đặc trưng đã được chuẩn hóa để đo lường và làm rõ cấu trúc mối tương quan tuyến tính chằng chịt giữa tất cả các cặp biến đặc trưng đầu vào hằng ngày.
  - id: KP8_3
    content: Ý nghĩa hình học của Vectơ riêng và Trị riêng trong việc xác định Trục thành phần chính
    keypoint_weight: 0.3
    description: Hệ thống thực hiện phân rã giá trị đặc trưng (Eigenvalue Decomposition) hoặc phân rã giá trị suy biến (SVD) trên ma trận hiệp phương sai. Các Vectơ riêng (Eigenvectors) xác định hướng hình học của các trục tọa độ mới (Trục thành phần chính). Các Trị riêng (Eigenvalues) tương ứng đo lường độ lớn của phương sai (lượng thông tin) mà trục đặc trưng đó nắm giữ, làm căn cứ để sắp xếp thứ tự ưu tiên và lựa chọn số lượng thành phần giữ lại.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong huấn luyện các mạng thần kinh nhân tạo sâu (Deep Neural Networks), hiện tượng Gradient Vanishing (Triệt tiêu đạo hàm) là gì? Hãy phân tích nguyên nhân bản chất xuất phát từ việc lựa chọn hàm kích hoạt (Activation Function) kết hợp toán tử lan truyền ngược (Backpropagation), và nêu hai giải pháp khắc phục ở mức kiến trúc.
* **expected_key_points:**
  - id: KP9_1
    content: Bản chất toán học và hệ quả của hiện tượng Gradient Vanishing
    keypoint_weight: 0.4
    description: Hiện tượng xảy ra khi các giá trị đạo hàm của hàm mất mát (Gradients) bị thu nhỏ tiệm cận về mức số 0 cực kỳ nhanh trong quá trình lan truyền ngược về các tầng đầu tiên (Early layers) của mạng. Hệ quả là trọng số của các tầng đầu gần như không được cập nhật, khiến mạng sâu không thể học được các đặc trưng vĩ mô cốt lõi.
  - id: KP9_2
    content: Nguyên nhân do phép nhân chuỗi đạo hàm của hàm Sigmoid/Tanh ở Backpropagation
    keypoint_weight: 0.3
    description: Do sử dụng các hàm kích hoạt phi tuyến tính có vùng bão hòa biên đạo hàm cực nhỏ như Sigmoid (đạo hàm lớn nhất là 0.25) hoặc Tanh (đạo hàm lớn nhất là 1.0). Khi thực hiện thuật toán lan truyền ngược (Backpropagation), quy tắc chuỗi (Chain Rule) bắt buộc thực hiện phép nhân liên tiếp các giá trị đạo hàm nhỏ này qua nhiều tầng, làm giá trị tích số bị triệt tiêu lũy thừa tiến về 0.
  - id: KP9_3
    content: Các giải pháp kỹ thuật khắc phục ở mức kiến trúc mạng
    keypoint_weight: 0.3
    description: Khắc phục bằng cách thay thế các hàm kích hoạt cũ bằng hàm ReLU (Rectified Linear Unit) hoặc các biến thể của nó (Leaky ReLU) vì đạo hàm của ReLU ở vùng dương luôn bằng 1, không làm thu nhỏ gradient; kết hợp áp dụng kỹ thuật chuẩn hóa theo lô Batch Normalization hoặc thiết kế các kết nối tắt vượt tầng (Skip Connections / Residual Connections như trong ResNet).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong các bài toán tối ưu hóa của học máy tiên tiến, thuật toán Stochastic Gradient Descent (SGD) thường bị mất ổn định hoặc kẹt ở các điểm Yên ngựa (Saddle Points) trên bề mặt lỗi. Hãy giải thích nguyên lý toán học của cơ chế "Momentum" (Động lượng) giúp thuật toán này vượt qua các điểm bẫy hình học nói trên để tăng tốc hội tụ.
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế tích lũy lịch sử bước đi dựa trên vận tốc toán học
    keypoint_weight: 0.4
    description: Cơ chế Momentum mô phỏng lại hiện tượng vật lý của một quả cầu lăn từ trên đỉnh dốc xuống. Nó đưa thêm một biến vận tốc v_t để tích lũy giá trị trung bình trượt có trọng số mũ (Exponential moving average) của tất cả các vectơ gradient từ các bước thời gian quá khứ: v_t = \beta v_{t-1} + \alpha \nabla L(w).
  - id: KP10_2
    content: Bản chất triệt tiêu dao động nhiễu và tăng tốc hướng đích
    keypoint_weight: 0.4
    description: Khi di chuyển qua các thung lũng dốc có bề mặt gồ ghề, các thành phần gradient theo hướng nhiễu ngang sẽ mang dấu trái ngược nhau qua các bước và tự động triệt tiêu lẫn nhau khi cộng dồn. Trong khi đó, các thành phần gradient trỏ thẳng về hướng điểm cực tiểu luôn cùng dấu và được tích lũy cộng dồn, làm gia tăng động lượng di chuyển cực mạnh theo trục chính, giúp tăng tốc hội tụ vượt trội.
  - id: KP10_3
    content: Nguyên lý cơ năng vượt bẫy hình học tại điểm Yên ngựa (Saddle Points)
    keypoint_weight: 0.2
    description: Tại các điểm Yên ngựa (Saddle Points) hoặc vùng cao nguyên phẳng (Plateaus), giá trị đạo hàm gradient bằng 0 tuyệt đối (\nabla L(w) = 0). Thuật toán SGD thuần túy sẽ bị đứng im vĩnh viễn tại đây. Nhờ có Momentum, biến vận tốc quá khứ v_{t-1} vẫn còn giữ giá trị cơ năng tích lũy trước đó, đẩy mô hình tiếp tục trượt thẳng qua vùng bẫy có đạo hàm bằng 0 này cho đến khi bắt được vùng dốc mới.