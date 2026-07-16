# Bộ Câu Hỏi Phỏng Vấn Data Scientist (Level 1)

* **Role:** Data Scientist
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong chuẩn bị đặc trưng dữ liệu danh mục (Categorical Features), kỹ thuật Frequency Encoding (hoặc Count Encoding) hoạt động ra sao? Nêu một điểm hạn chế lớn về mặt toán học khi hai giá trị danh mục khác nhau lại có tần suất xuất hiện bằng nhau trong tập dữ liệu.
* **expected_key_points:**
  - id: KP1_1
    content: Cơ chế mã hóa dựa trên tỷ lệ tần suất xuất hiện của nhóm danh mục
    keypoint_weight: 0.5
    description: Frequency Encoding chuyển đổi các giá trị chuỗi danh mục bằng cách tính toán tần suất xuất hiện (hoặc tỷ lệ phần trăm) của chính nhóm danh mục đó trên tổng số mẫu của tập dữ liệu huấn luyện.
  - id: KP1_2
    content: Hiện tượng trùng lặp thông tin đặc trưng khi trùng tần suất (Collision rủi ro)
    keypoint_weight: 0.5
    description: Hạn chế lớn nhất là nếu hai giá trị danh mục hoàn toàn khác nhau về mặt ngữ nghĩa nghiệp vụ nhưng lại có số lần xuất hiện bằng nhau, thuật toán sẽ mã hóa chúng thành cùng một con số duy nhất. Điều này vô tình xóa sạch sự khác biệt logic giữa hai thực thể, khiến mô hình học máy không thể phân tách ngữ cảnh độc lập của chúng.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Thuật toán phân loại Naive Bayes có nhiều biến thể khác nhau để xử lý các dạng dữ liệu đầu vào riêng biệt. Hãy phân biệt sự khác biệt cơ bản về giả định phân phối dữ liệu đặc trưng giữa Gaussian Naive Bayes và Multinomial Naive Bayes.
* **expected_key_points:**
  - id: KP2_1
    content: Giả định phân phối liên tục hình chuông của Gaussian Naive Bayes
    keypoint_weight: 0.5
    description: Gaussian Naive Bayes được áp dụng khi các biến đặc trưng đầu vào là các biến số liên tục (Continuous variables). Thuật toán giả định rằng dữ liệu của mỗi đặc trưng ứng với mỗi lớp nhãn mục tiêu tuân theo phân phối chuẩn Gauss (hình chuông), xác suất được tính dựa trên hàm mật độ xác suất chuẩn qua giá trị trung bình và phương sai.
  - id: KP2_2
    content: Giả định phân phối rời rạc dựa trên tần suất đếm của Multinomial Naive Bayes
    keypoint_weight: 0.5
    description: Multinomial Naive Bayes được áp dụng khi các đặc trưng đầu vào biểu diễn dữ liệu rời rạc dạng tần suất đếm (Count data). Thuật toán giả định dữ liệu tuân theo phân phối đa thức, cực kỳ phổ biến trong xử lý văn bản (NLP) nơi các đặc trưng là số lần xuất hiện của từ khóa trong văn bản.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Khi đánh giá hiệu năng của mô hình hồi quy tuyến tính (Linear Regression), tại sao chỉ số R-squared ($R^2$) thuần túy có xu hướng tăng lên một cách giả tạo khi ta thêm biến mới vào mô hình? Chỉ số Adjusted R-squared (R-squared hiệu chỉnh) giải quyết khuyết điểm này dựa trên cơ chế nào?
* **expected_key_points:**
  - id: KP3_1
    content: Điểm hạn chế phình to cơ học của chỉ số R-squared thuần túy
    keypoint_weight: 0.5
    description: Chỉ số R-squared thuần túy được tính toán dựa trên tỷ lệ tổng bình phương sai số phần dư. Về mặt toán học, khi thêm bất kỳ biến độc lập mới nào vào mô hình (kể cả biến nhiễu vô nghĩa), tổng bình phương sai số phần dư luôn giữ nguyên hoặc giảm xuống, khiến R-squared luôn tăng lên, dễ đánh lừa nhà khoa học dữ liệu về độ chính xác thực tế.
  - id: KP3_2
    content: Cơ chế trừng phạt số lượng biến dựa trên độ tự do của Adjusted R-squared
    keypoint_weight: 0.5
    description: Adjusted R-squared giải quyết vấn đề này bằng cách đưa thêm thành phần phạt dựa trên số lượng biến đặc trưng ($p$) và kích thước mẫu ($n$) vào công thức tính toán độ tự do. Chỉ số này sẽ chỉ tăng lên nếu biến mới thêm vào giúp mô hình cải thiện hiệu năng thực tế vượt qua mức phạt cơ học, ngược lại nếu thêm biến nhiễu, Adjusted R-squared sẽ tự động sụt giảm.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong giai đoạn tiền xử lý dữ liệu, kỹ thuật Box-Cox Transformation được sử dụng nhằm mục đích gì? Điều kiện bắt buộc đối với giá trị của biến số đầu vào khi áp dụng phép biến đổi này là gì?
* **expected_key_points:**
  - id: KP4_1
    content: Mục tiêu đưa phân phối lệch về dạng phân phối chuẩn (Normal distribution alignment)
    keypoint_weight: 0.5
    description: Box-Cox Transformation là một kỹ thuật biến đổi toán học phi tuyến dạng lũy thừa, được áp dụng nhằm mục đích chuyển đổi các biến số có phân phối bị lệch nặng hoặc không đồng đều phương sai về dạng phân phối đối xứng gần chuẩn, giúp thỏa mãn giả định phân phối chuẩn của các mô hình hồi quy hoặc kiểm định tham số.
  - id: KP4_2
    content: Điều kiện toán học bắt buộc giá trị biến số phải dương tuyệt đối
    keypoint_weight: 0.5
    description: Công thức toán học của Box-Cox chứa phép toán logarithm và lũy thừa phân số, do đó điều kiện bắt buộc là toàn bộ các giá trị của biến số đầu vào phải mang giá trị dương tuyệt đối ($x > 0$). Nếu dữ liệu chứa số 0 hoặc số âm, Data Scientist phải dịch chuyển dữ liệu bằng cách cộng thêm một hằng số cố định trước khi biến đổi.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thuật toán Random Forest xây dựng cụm mô hình dựa trên kỹ thuật Bagging. Hãy giải thích khái niệm Out-of-Bag (OOB) Error và tại sao cơ chế này lại cho phép ta đánh giá hiệu năng mô hình một cách khách quan mà không bắt buộc phải sử dụng đến một tập tập dữ liệu Validation độc lập?
* **expected_key_points:**
  - id: KP5_1
    content: Bản chất hình học của phần dữ liệu không được bốc trúng (Out-of-Bag data)
    keypoint_weight: 0.5
    description: Khi Random Forest thực hiện lấy mẫu có hoàn tác (Bootstrap sampling) để huấn luyện cho từng cây quyết định độc lập, về mặt toán học xác suất, sẽ có khoảng 36.8% lượng dữ liệu thô không được bốc trúng vào tập huấn luyện của cây đó. Phần dữ liệu bị bỏ lại này được gọi là dữ liệu Out-of-Bag đối với cây cụ thể đó.
  - id: KP5_2
    content: Cơ chế đánh giá chéo nội bộ mô hình giả lập tập Validation
    keypoint_weight: 0.5
    description: Để tính toán OOB Error, hệ thống duyệt qua từng dòng dữ liệu gốc hằng ngày. Dòng dữ liệu này sẽ được đưa vào làm input dự báo tại tất cả các cây quyết định mà nó không tham gia vào quá trình huấn luyện, sau đó gộp kết quả bỏ phiếu lại. Điểm sai số tổng thể tính toán trên toàn bộ tập dữ liệu qua cơ chế này chính là OOB Error, đóng vai trò như một tập Validation tự động và khách quan.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong bài toán phân loại đa nhãn hoặc đa lớp (Multi-class Classification), hãy phân biệt sự khác biệt về mặt logic toán học và ngữ cảnh áp dụng giữa hai phương pháp tính toán điểm trung bình: F1-Macro Score và F1-Micro Score.
* **expected_key_points:**
  - id: KP6_1
    content: Logic tính trung bình cộng đồng đều của chỉ số F1-Macro
    keypoint_weight: 0.4
    description: F1-Macro thực hiện tính toán chỉ số F1-score độc lập cho từng lớp nhãn trước, sau đó lấy trung bình cộng giản đơn của toàn bộ các điểm số đó một cách đồng đều, không phụ thuộc vào kích thước mẫu của lớp. Kỹ thuật này coi mọi lớp có độ quan trọng ngang nhau, tối ưu cho việc đánh giá các lớp thiểu số trong dữ liệu mất cân bằng.
  - id: KP6_2
    content: Logic cộng dồn tổng thể tính toán theo mẫu của chỉ số F1-Micro
    keypoint_weight: 0.4
    description: F1-Micro thực hiện cộng dồn tổng số lượng các giá trị True Positive, False Positive, False Negative của toàn bộ các lớp nhãn trên toàn hệ thống trước, sau đó mới áp dụng công thức tính F1-score tổng cục một lần. Chỉ số này chịu sự chi phối mạnh mẽ bởi hiệu năng của các lớp đa số.
  - id: KP6_3
    content: Ngữ cảnh lựa chọn áp dụng chỉ số phù hợp với bài toán doanh nghiệp
    keypoint_weight: 0.2
    description: Chọn F1-Macro khi doanh nghiệp yêu cầu mô hình phải hoạt động tốt trên các lớp hiếm (ví dụ: phát hiện các loại bệnh hiếm). Chọn F1-Micro khi ta muốn tối ưu hóa độ chính xác tổng thể trên từng thực thể mẫu dữ liệu di chuyển hằng ngày mà không quan tâm đến tính chất hiếm của lớp.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy phân biệt điểm khác biệt cốt lõi về triết lý thiết kế hình học và xử lý sai số giữa Hard-margin SVM và Soft-margin SVM. Siêu tham số phạt $C$ đóng vai trò gì trong việc điều khiển ranh giới quyết định của Soft-margin SVM?
* **expected_key_points:**
  - id: KP7_1
    content: Ràng buộc tuyệt đối của Hard-margin vs Cơ chế nới lỏng bằng biến bù lỗi của Soft-margin
    keypoint_weight: 0.5
    description: Hard-margin SVM đặt ràng buộc cứng nhắc, yêu cầu dữ liệu phải phân tách tuyến tính hoàn hảo và không chấp nhận bất kỳ sai số nào lấn vào lề an toàn. Soft-margin SVM đưa thêm các biến bù lỗi (Slack Variables) vào hàm mục tiêu tối ưu, cho phép một số điểm dữ liệu nằm sai vị trí hoặc lấn vào lề để đổi lấy một siêu phẳng có độ rộng lề lớn hơn, ổn định hơn trước nhiễu.
  - id: KP7_2
    content: Vai trò điều khiển mức độ trừng phạt sai số của siêu tham số C
    keypoint_weight: 0.5
    description: Siêu tham số $C$ quy định trọng số trừng phạt các sai số vi phạm của biến bù lỗi trong hàm mục tiêu. Khi cấu hình $C$ quá lớn, mô hình phạt nặng sai số, ép ranh giới quyết định uốn lượn để phân tách đúng điểm, dễ gây Overfitting. Khi $C$ quá nhỏ, mô hình chấp nhận bỏ qua nhiều sai số để giữ ranh giới phẳng mịn toàn cục, dễ dẫn đến Underfitting.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Phân rã giá trị suy biến SVD (Singular Value Decomposition) là một nền tảng toán học đại số tuyến tính tối quan trọng. Hãy giải thích cấu trúc phân rã của một ma trận dữ liệu $A$ thành tích của ba ma trận đặc biệt trong thuật toán SVD và ứng dụng của nó đối với kỹ thuật giảm chiều dữ liệu PCA.
* **expected_key_points:**
  - id: KP8_1
    content: Cấu trúc toán học của ba ma trận thành phần trong phân rã SVD
    keypoint_weight: 0.4
    description: SVD phân rã một ma trận $A$ kích thước $m \times n$ thành tích số của ba ma trận tuần tự: $A = U \Sigma V^T$. Trong đó $U$ là ma trận trực giao chứa các vectơ trực chuẩn trái (Left singular vectors), $V$ là ma trận trực giao chứa các vectơ trực chuẩn phải (Right singular vectors), và $\Sigma$ là ma trận đường chéo chứa các giá trị suy biến (Singular values) giảm dần đại diện cho độ lớn năng lượng đặc trưng.
  - id: KP8_2
    content: Mối liên quan toán học giữa giá trị suy biến và trị riêng (Eigenvalues)
    keypoint_weight: 0.4
    description: Các giá trị suy biến trong ma trận $\Sigma$ chính là căn bậc hai của các trị riêng (Eigenvalues) thu được từ ma trận hiệp phương sai của tập dữ liệu. Các vectơ trong ma trận $V$ tương ứng chính là các vectơ riêng (Eigenvectors) định nghĩa hướng của các trục thành phần chính trong PCA.
  - id: KP8_3
    content: Cơ chế giảm chiều tối ưu thông qua cắt bỏ giá trị suy biến nhỏ (Truncated SVD)
    keypoint_weight: 0.2
    description: PCA ứng dụng SVD bằng cách giữ lại $k$ giá trị suy biến lớn nhất trong ma trận $\Sigma$ và cắt bỏ phần còn lại. Tiến trình này giúp chiếu ma trận dữ liệu gốc về không gian $k$ chiều tối ưu nhất mà vẫn bảo toàn tối đa phương sai thông tin nội tại, giảm thiểu chi phí tính toán tường minh ma trận hiệp phương sai trực tiếp.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong huấn luyện các mạng nơ-ron nhân tạo sâu (Deep Neural Networks), tầng Batch Normalization được áp dụng rộng rãi. Hãy giải thích nguyên lý toán học hoạt động của Batch Normalization trong quá trình lan truyền tiến và cách nó giải quyết hiện tượng dịch chuyển phân phối nội bộ (Internal Covariate Shift).
* **expected_key_points:**
  - id: KP9_1
    content: Công thức toán học chuẩn hóa dữ liệu dựa trên giá trị trung bình và phương sai của mini-batch
    keypoint_weight: 0.4
    description: Batch Normalization thực hiện chuẩn hóa các giá trị kích hoạt đầu ra (Activations) của một tầng cho từng mini-batch dữ liệu bằng cách trừ đi giá trị trung bình và chia cho độ lệch chuẩn của chính mini-batch đó, đưa dữ liệu về dạng có trung bình bằng 0 và phương sai bằng 1.
  - id: KP9_2
    content: Cơ chế khôi phục năng lực biểu diễn phi tuyến bằng hai tham số học được (Scale and Shift)
    keypoint_weight: 0.3
    description: Để tránh việc chuẩn hóa làm mất đi tính chất phi tuyến đặc thù của hàm kích hoạt (ví dụ ép dữ liệu rơi vào vùng tuyến tính trung tâm của Sigmoid), Batch Normalization đưa thêm hai tham số có khả năng học được (Trainable parameters) là $\gamma$ (Scale) và $\beta$ (Shift). Công thức cuối cùng: $Y = \gamma \hat{X} + \beta$, cho phép mạng nơ-ron tự động điều chỉnh tối ưu hóa cấu trúc bề mặt dữ liệu.
  - id: KP9_3
    content: Nguyên lý giải quyết lỗi ổn định Internal Covariate Shift tăng tốc độ hội tụ
    keypoint_weight: 0.3
    description: Internal Covariate Shift là hiện tượng phân phối dữ liệu đầu vào của các tầng phía sau liên tục bị thay đổi chao đảo khi trọng số của các tầng phía trước cập nhật qua từng bước lặp. Batch Normalization triệt tiêu hiện tượng này bằng cách cố định phân phối đầu vào của mỗi tầng luôn ổn định quanh mốc $\gamma$ và $\beta$, giúp kiểm soát tốt lỗi triệt tiêu đạo hàm, cho phép cấu hình Learning rate lớn hơn để mạng hội tụ cực nhanh.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích sự tiến hóa về mặt toán học tối ưu hóa từ thuật toán RMSProp lên thuật toán Adam (Adaptive Moment Estimation). Làm thế nào Adam kết hợp được ưu điểm của cả hai cơ chế: Động lượng mũ và Điều chỉnh tốc độ học thích ứng theo từng tham số?
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế RMSProp trong việc kìm hãm dao động bằng mô-men đại lượng cấp hai
    keypoint_weight: 0.4
    description: RMSProp tính toán giá trị trung bình trượt có trọng số mũ của bình phương các vectơ đạo hàm gradient quá khứ ($v_t$), đại diện cho Mô-men đại lượng cấp hai. Khi cập nhật trọng số, nó chia Learning rate cho căn bậc hai của $v_t$. Cơ chế này giúp tự động điều chỉnh giảm tốc độ học thích ứng cho các tham số có biến động gradient quá lớn, làm mịn bề mặt tối ưu hóa.
  - id: KP10_2
    content: Sự tích hợp thêm đại lượng cấp một mô phỏng Động lượng mũ (Momentum) của Adam
    keypoint_weight: 0.4
    description: Adam nâng cấp RMSProp bằng cách đưa thêm thành phần tính toán giá trị trung bình trượt có trọng số mũ của chính các vectơ đạo hàm gradient thô quá khứ ($m_t$), đại diện cho Mô-men đại lượng cấp một. Cơ chế này đóng vai trò như lực quán tính động lượng, giúp mô hình triệt tiêu các thành phần dao động nhiễu ngang chéo và tích lũy động năng đẩy tham số lao thẳng nhanh hơn về hướng đáy thung lũng cực tiểu.
  - id: KP10_3
    content: Cơ chế hiệu chỉnh toán học lỗi khởi tạo vùng biên (Bias Correction)
    keypoint_weight: 0.2
    description: Do các giá trị mô-men $m_t$ và $v_t$ thường được khởi tạo bằng các vectơ số 0 ở thời điểm bắt đầu, chúng bị kéo lệch về sát gốc 0 trong các bước lặp đầu tiên của tiến trình huấn luyện. Adam giải quyết triệt để bài toán này bằng cách áp dụng các công thức hiệu chỉnh toán học Bias Correction ($\hat{m}_t = m_t / (1 - \beta_1^t)$ và $\hat{v}_t = v_t / (1 - \beta_2^t)$) để chuẩn hóa lại giá trị chuyển dịch ở những vòng lặp đầu, giúp thuật toán hoạt động chính xác và ổn định ngay từ khi bắt đầu.