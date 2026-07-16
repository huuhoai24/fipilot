# Bộ Câu Hỏi Phỏng Vấn Data Scientist (Level 1)

* **Role:** Data Scientist
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt điểm khác biệt cốt lõi về bản chất của dữ liệu đầu vào (Input data) và mục tiêu xử lý giữa hai trường phái học máy: Supervised Learning (Học máy có giám sát) và Unsupervised Learning (Học máy không giám sát).
* **expected_key_points:**
  - id: KP1_1
    content: Bản chất dữ liệu nhãn và mục tiêu của Supervised Learning
    keypoint_weight: 0.5
    description: Học máy có giám sát yêu cầu tập dữ liệu huấn luyện bắt buộc phải được gán nhãn mục tiêu trước (Labeled data), nghĩa là với mỗi vector đặc trưng đầu vào X đều có một giá trị đích Y tương ứng. Mục tiêu là học một hàm ánh xạ từ X sang Y để dự báo cho dữ liệu mới.
  - id: KP1_2
    content: Bản chất dữ liệu thô và mục tiêu của Unsupervised Learning
    keypoint_weight: 0.5
    description: Học máy không giám sát tiếp nhận tập dữ liệu hoàn toàn không có nhãn mục tiêu (Unlabeled data). Mục tiêu của thuật toán là tự động phân tích, khám phá các cấu trúc hình học ẩn sâu, các mối quan hệ tương đồng hoặc phân cụm tự nhiên nội tại bên trong dữ liệu thô.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong phân tích thống kê dữ liệu, kiểm định Chi-square Test of Independence (Kiểm định chi-bình phương về tính độc lập) được sử dụng nhằm mục đích gì? Phát biểu cấu trúc giả thuyết không H0 và giả thuyết đối lập H1 của kiểm định này.
* **expected_key_points:**
  - id: KP2_1
    content: Mục tiêu đo lường mối quan hệ giữa hai biến danh mục của Chi-square
    keypoint_weight: 0.5
    description: Kiểm định Chi-square về tính độc lập được sử dụng để xác định xem có mối quan hệ phụ thuộc mang ý nghĩa thống kê giữa hai biến định tính/biến danh mục (Categorical variables) hay không, dựa trên bảng tần suất chéo (Contingency table).
  - id: KP2_2
    content: Cấu trúc phát biểu giả thuyết H0 và H1
    keypoint_weight: 0.5
    description: Giả thuyết không H0 phát biểu rằng hai biến danh mục hoàn toàn độc lập với nhau (Không có mối quan hệ trong tổng thể). Giả thuyết đối lập H1 phát biểu rằng hai biến danh mục có mối quan hệ phụ thuộc lẫn nhau một cách có ý nghĩa thống kê.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Kỹ thuật Frequency Encoding (hoặc Count Encoding) thường được dùng để tiền xử lý biến danh mục (Categorical Features). Hãy giải thích cơ chế hoạt động và nêu một khuyết điểm toán học của phương pháp này khi hai nhóm danh mục khác nhau có tần suất xuất hiện trùng nhau.
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế mã hóa bằng tỷ lệ tần suất xuất hiện của nhóm danh mục
    keypoint_weight: 0.5
    description: Frequency Encoding chuyển đổi các giá trị chuỗi danh mục bằng cách tính toán tần suất xuất hiện hoặc tỷ lệ phần trăm của chính nhóm danh mục đó trên tổng số mẫu của tập dữ liệu huấn luyện hằng ngày.
  - id: KP3_2
    content: Hiện tượng trùng lặp mã hóa làm mất thông tin ngữ nghĩa (Collision rủi ro)
    keypoint_weight: 0.5
    description: Hạn chế lớn nhất là nếu hai giá trị danh mục hoàn toàn khác biệt về mặt logic nghiệp vụ kinh doanh nhưng lại có số lần xuất hiện bằng nhau trong tập Train, thuật toán sẽ mã hóa chúng thành cùng một con số duy nhất, vô tình xóa sạch sự khác biệt logic giữa hai thực thể và làm giảm năng lực phân tách của mô hình.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thuật toán DBSCAN là một phương pháp phân cụm dựa trên mật độ. Hãy giải thích ý nghĩa của hai siêu tham số Eps (Epsilon) và MinPts (Minimum Points) cùng cơ chế nhận diện điểm nhiễu (Noise Points) của thuật toán này.
* **expected_key_points:**
  - id: KP4_1
    content: Vai trò định nghĩa không gian hình học của siêu tham số Eps và MinPts
    keypoint_weight: 0.4
    description: Eps xác định bán kính vùng lân cận hình học xung quanh một điểm dữ liệu. MinPts quy định số lượng điểm tối thiểu bắt buộc phải nằm trong vùng bán kính Eps đó để một điểm có thể được xác lập tư cách là một điểm lõi (Core Point).
  - id: KP4_2
    content: Cơ chế phân loại các loại điểm (Core, Border) dựa trên mật độ
    keypoint_weight: 0.3
    description: Điểm lõi (Core Point) có số điểm lân cận >= MinPts. Điểm biên (Border Point) có số điểm lân cận < MinPts nhưng bản thân nó lại nằm trong vùng bán kính Eps của một điểm lõi khác. Thuật toán loan tỏa cụm từ các điểm lõi này.
  - id: KP4_3
    content: Cơ chế cô lập và nhận diện điểm nhiễu tự động (Noise Points)
    keypoint_weight: 0.3
    description: Một điểm được xác định là Điểm nhiễu (Noise Point) nếu nó không phải là điểm lõi và đồng thời không nằm trong vùng lân cận của bất kỳ điểm lõi nào. DBSCAN tự động cô lập các điểm này ra khỏi tất cả các cụm, giúp mô hình có khả năng chống nhiễu cực tốt mà không cần định trước số lượng cụm K.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong bài toán phân loại đa lớp (Multi-class Classification), hãy phân biệt sự khác biệt về mặt logic toán học và ngữ cảnh áp dụng giữa hai phương pháp tính toán điểm trung bình hiệu năng: F1-Macro Score và F1-Micro Score.
* **expected_key_points:**
  - id: KP5_1
    content: Logic tính trung bình cộng đồng đều của chỉ số F1-Macro
    keypoint_weight: 0.4
    description: F1-Macro thực hiện tính toán chỉ số F1-score độc lập cho từng lớp nhãn trước, sau đó lấy trung bình cộng giản đơn của toàn bộ các điểm số đó một cách đồng đều, không phụ thuộc vào kích thước mẫu của lớp. Kỹ thuật này coi mọi lớp có độ quan trọng ngang nhau, tối ưu cho việc đánh giá các lớp thiểu số trong dữ liệu mất cân bằng.
  - id: KP5_2
    content: Logic cộng dồn tổng thể tính toán theo mẫu của chỉ số F1-Micro
    keypoint_weight: 0.4
    description: F1-Micro thực hiện cộng dồn tổng số lượng các giá trị True Positive, False Positive, False Negative của toàn bộ các lớp nhãn trên toàn hệ thống trước, sau đó mới áp dụng công thức tính F1-score tổng cục một lần. Chỉ số này chịu sự chi phối mạnh mẽ bởi hiệu năng của các lớp đa số.
  - id: KP5_3
    content: Ngữ cảnh lựa chọn áp dụng chỉ số phù hợp với bài toán dữ liệu
    keypoint_weight: 0.2
    description: Chọn F1-Macro khi doanh nghiệp yêu cầu mô hình phải hoạt động tốt trên các lớp hiếm (vị trí thiểu số). Chọn F1-Micro khi ta muốn tối ưu hóa độ chính xác tổng thể trên từng thực thể mẫu dữ liệu di chuyển hằng ngày mà không quan tâm đến tính chất hiếm của lớp.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong các bài toán hồi quy (Regression), hàm mất mát Huber Loss thường được sử dụng như một giải pháp thay thế thông minh cho MSE và MAE. Hãy giải thích công thức logic hoạt động và ưu điểm hình học của Huber Loss đối với dữ liệu chứa nhiều nhiễu ngoại lai (Outliers).
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế phân tách điều kiện dựa trên ngưỡng Delta của Huber Loss
    keypoint_weight: 0.5
    description: Huber Loss phân tách hàm toán học thành hai phân vùng dựa trên một siêu tham số ngưỡng Delta. Khi sai số dự báo nhỏ hơn hoặc bằng Delta, Huber Loss áp dụng công thức của hàm bình phương MSE. Khi sai số dự báo vượt quá ngưỡng Delta, hàm tự động chuyển sang cấu trúc tuyến tính tuyệt đối của hàm MAE.
  - id: KP6_2
    content: Ưu điểm hình học cân bằng giữa tính ổn định và tính khả vi (Differentiability)
    keypoint_weight: 0.5
    description: Nhờ cơ chế lai ghép, Huber Loss tận dụng ưu điểm của MAE ở vùng biên ngoài để chống chịu hiệu quả với nhiễu ngoại lai (không phóng đại sai số lớn theo hàm mũ như MSE), đồng thời tận dụng ưu điểm của MSE ở vùng trung tâm giúp đồ thị mượt mà và khả vi liên tục (Differentiable) tại điểm sai số bằng 0, giúp thuật toán Gradient Descent hội tụ ổn định, không bị dao động nhiễu.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong các bài toán tối ưu hóa bằng thuật toán Gradient Descent, siêu tham số Learning Rate (Tốc độ học) thường được cải tiến qua cơ chế Momentum (Động lượng). Hãy giải thích nguyên lý hoạt động toán học và mục đích hình học của cơ chế này.
* **expected_key_points:**
  - id: KP7_1
    content: Cơ chế tích lũy lịch sử bước đi dựa trên vận tốc toán học (Velocity vector)
    keypoint_weight: 0.5
    description: Cơ chế Momentum đưa thêm một biến vận tốc vào công thức cập nhật để tích lũy giá trị trung bình trượt có trọng số mũ (Exponential moving average) của tất cả các vectơ gradient từ các bước thời gian quá khứ, mô phỏng lại gia tốc động lượng của vật lý.
  - id: KP7_2
    content: Bản chất triệt tiêu dao động nhiễu và tăng tốc hướng đích
    keypoint_weight: 0.5
    description: Khi di chuyển qua các thung lũng dốc có bề mặt gồ ghề, các thành phần gradient theo hướng nhiễu ngang mang dấu trái ngược sẽ tự động triệt tiêu lẫn nhau khi cộng dồn. Trong khi các thành phần gradient trỏ về hướng điểm cực tiểu luôn cùng dấu và được tích lũy cộng dồn, làm gia tăng động lượng giúp mô hình hội tụ nhanh và ổn định hơn.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong mô hình Support Vector Machine (SVM) dành cho bài toán phân lớp, siêu phẳng biên cực đại (Maximum Margin Hyperplane) là gì? Hãy giải thích cơ chế toán học giúp Kernel Trick tối ưu hóa chi phí tính toán khi chuyển đổi không gian đặc trưng đa chiều.
* **expected_key_points:**
  - id: KP8_1
    content: Mục tiêu tìm kiếm siêu phẳng phân tách có khoảng cách lề lớn nhất
    keypoint_weight: 0.4
    description: SVM tìm kiếm một siêu phẳng phân tách tuyến tính tối ưu nằm ở chính giữa hai lớp dữ liệu sao cho khoảng cách lề (Margin) từ siêu phẳng đó đến các điểm dữ liệu gần nhất của cả hai lớp (Support Vectors) đạt giá trị lớn nhất, nhằm tăng cường khả năng tổng quát hóa trên dữ liệu mới.
  - id: KP8_2
    content: Cơ chế toán học tính toán trực tiếp tích vô hướng ở không gian thấp (Dot Product Optimization)
    keypoint_weight: 0.4
    description: Khi dữ liệu phi tuyến phức tạp ở không gian gốc, thay vì phải thực hiện tường minh phép toán chuyển đổi tất cả các điểm dữ liệu lên không gian cao (vốn cực kỳ tốn tài nguyên), hàm Kernel cho phép tính toán trực tiếp giá trị tích vô hướng (Dot product) của hai điểm trong không gian cao thông qua một biểu thức toán học thực thi ngay tại không gian gốc thấp ban đầu.
  - id: KP8_3
    content: Triệt tiêu rủi ro của Lời nguyền đa chiều lên hiệu năng tính toán
    keypoint_weight: 0.2
    description: Giúp thuật toán SVM tối ưu hóa hàm mục tiêu kép (Dual optimization problem) đạt hiệu năng cực cao, triệt tiêu hoàn toàn chi phí tính toán tường minh ở không gian vô hạn chiều, bảo vệ hệ thống khỏi các thảm họa sụp đổ tài nguyên xử lý dữ liệu lớn.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Kỹ thuật giảm chiều dữ liệu t-SNE (t-Distributed Stochastic Neighbor Embedding) thường được sử dụng để trực quan hóa dữ liệu có số chiều lớn. Hãy giải thích nguyên lý toán học giúp t-SNE bảo toàn được cấu trúc cục bộ (Local Structure) và cách nó sử dụng phân phối t-Student để giải quyết bài toán sụp đổ không gian (Crowding Problem).
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế chuyển đổi khoảng cách hình học thành phân phối xác suất tương đồng
    keypoint_weight: 0.4
    description: t-SNE chuyển đổi khoảng cách giữa các cặp điểm trong không gian cao thành các giá trị xác suất biểu thị độ tương đồng (Similarity). Điểm gần nhau có xác suất cao. Mục tiêu là tối ưu hóa để phân phối xác suất ở không gian thấp gần nhất với không gian cao thông qua giảm thiểu độ chênh lệch Kullback-Leibler (KL Divergence).
  - id: KP9_2
    content: Bản chất toán học của bài toán Crowding Problem khi giảm chiều dữ liệu
    keypoint_weight: 0.3
    description: Khi ép dữ liệu từ không gian nhiều chiều về không gian ít chiều (2 chiều), thể tích không gian bị co rút theo hàm mũ. Các điểm ở khoảng cách trung bình trong không gian cao sẽ không có đủ không gian hình học để phân bổ ở không gian thấp, dẫn đến việc chúng bị dồn ứ, đè lên nhau và xóa sạch cấu trúc phân cụm cục bộ.
  - id: KP9_3
    content: Cơ chế sử dụng đuôi dài của phân phối t-Student để đẩy giãn cách dữ liệu ở không gian thấp
    keypoint_weight: 0.3
    description: t-SNE giải quyết bài toán này bằng cách áp dụng phân phối t-Student với 1 độ tự do ở không gian thấp thay vì dùng phân phối chuẩn Gauss. Phân phối t-Student có phần đuôi dài hơn và dày hơn rất nhiều (Heavy-tailed); để đạt cùng một mức xác suất tương đồng như không gian cao, các điểm ở khoảng cách trung bình buộc phải được đẩy ra xa nhau hơn rất nhiều trong không gian 2D, giúp giải phóng không gian và làm hiển thị rõ ràng cấu trúc phân cụm cục bộ.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích sự tiến hóa về mặt toán học tối ưu hóa từ thuật toán RMSProp lên thuật toán Adam (Adaptive Moment Estimation). Làm thế nào Adam kết hợp được ưu điểm của cả hai cơ chế: Động lượng mũ và Điều chỉnh tốc độ học thích ứng theo từng tham số?
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế RMSProp trong việc kìm hãm dao động bằng mô-men đại lượng cấp hai
    keypoint_weight: 0.4
    description: RMSProp tính toán giá trị trung bình trượt có trọng số mũ của bình phương các vectơ đạo hàm gradient quá khứ (vt), đại diện cho Mô-men đại lượng cấp hai. Khi cập nhật trọng số, nó chia Learning rate cho căn bậc hai của vt. Cơ chế này giúp tự động điều chỉnh giảm tốc độ học thích ứng cho các tham số có biến động gradient quá lớn, làm mịn bề mặt tối ưu hóa.
  - id: KP10_2
    content: Sự tích hợp thêm đại lượng cấp một mô phỏng Động lượng mũ (Momentum) của Adam
    keypoint_weight: 0.4
    description: Adam nâng cấp RMSProp bằng cách đưa thêm thành phần tính toán giá trị trung bình trượt có trọng số mũ của chính các vectơ đạo hàm gradient thô quá khứ (mt), đại diện cho Mô-men đại lượng cấp một. Cơ chế này đóng vai trò như lực quán tính động lượng, giúp mô hình triệt tiêu các thành phần dao động nhiễu ngang chéo và tích lũy động năng đẩy tham số lao thẳng nhanh hơn về hướng đáy thung lũng cực tiểu.
  - id: KP10_3
    content: Cơ chế hiệu chỉnh toán học lỗi khởi tạo vùng biên (Bias Correction)
    keypoint_weight: 0.2
    description: Do các giá trị mô-men mt và vt thường được khởi tạo bằng các vectơ số 0 ở thời điểm bắt đầu, chúng bị kéo lệch về sát gốc 0 trong các bước lặp đầu tiên của tiến trình huấn luyện. Adam giải quyết triệt để bài toán này bằng cách áp dụng các công thức hiệu chỉnh toán học Bias Correction để chuẩn hóa lại giá trị chuyển dịch ở những vòng lặp đầu, giúp thuật toán hoạt động chính xác và ổn định ngay từ khi bắt đầu.