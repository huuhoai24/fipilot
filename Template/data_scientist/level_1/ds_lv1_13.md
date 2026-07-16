# Bộ Câu Hỏi Phỏng Vấn Data Scientist (Level 1)

* **Role:** Data Scientist
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong các bài toán học máy giám sát (Supervised Learning), hãy giải thích sự khác biệt cốt lõi về thuộc tính của biến mục tiêu (Target Variable) và mục đích đầu ra giữa hai dạng bài toán: Regression (Hồi quy) và Classification (Phân loại).
* **expected_key_points:**
  - id: KP1_1
    content: Đặc tính biến liên tục và mục tiêu của bài toán Hồi quy (Regression)
    keypoint_weight: 0.5
    description: Bài toán hồi quy nhằm dự đoán một giá trị số liên tục (Continuous/Numerical value) trong một dải vô hạn. Ví dụ: dự đoán giá nhà, dự đoán doanh số bán hàng, hoặc nhiệt độ hằng ngày.
  - id: KP1_2
    content: Đặc tính biến rời rạc và mục tiêu của bài toán Phân loại (Classification)
    keypoint_weight: 0.5
    description: Bài toán phân loại nhằm gán các mẫu dữ liệu vào các nhóm/nhãn rời rạc (Discrete/Categorical classes) đã biết trước. Ví dụ: dự đoán giao dịch là gian lận hay hợp lệ (Nhị phân), hoặc phân loại email vào các hộp thư Spam/Inbox/Promotions (Đa lớp).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Khi đánh giá một mô hình phân lớp nhị phân, Ma trận nhầm lẫn (Confusion Matrix) là gì? Hãy định nghĩa bốn thành phần cơ bản cấu thành nên ma trận này: True Positive (TP), True Negative (TN), False Positive (FP) và False Negative (FN).
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm bảng Confusion Matrix đối chiếu thực tế và dự báo
    keypoint_weight: 0.4
    description: Confusion Matrix là một bảng thống kê chéo (thường là kích thước 2x2 cho phân loại nhị phân) dùng để đối chiếu trực quan giữa nhãn thực tế (Actual Class) và nhãn do mô hình dự báo (Predicted Class).
  - id: KP2_2
    content: Định nghĩa nhóm dự báo chính xác (True Positive và True Negative)
    keypoint_weight: 0.3
    description: True Positive (TP) là số lượng mẫu thực tế là nhóm tích cực (Positive) và mô hình dự báo chính xác là Positive. True Negative (TN) là số lượng mẫu thực tế là nhóm tiêu cực (Negative) và mô hình dự báo chính xác là Negative.
  - id: KP2_3
    content: Định nghĩa nhóm dự báo sai lệch (False Positive và False Negative)
    keypoint_weight: 0.3
    description: False Positive (FP) là số lượng mẫu thực tế là Negative nhưng mô hình dự báo nhầm là Positive (Sai lầm loại một / Báo động giả). False Negative (FN) là số lượng mẫu thực tế là Positive nhưng mô hình dự báo nhầm là Negative (Sai lầm loại hai / Bỏ sót).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong quy trình phân tích và chuẩn bị dữ liệu, tại sao chúng ta cần phân chia tập dữ liệu gốc thành ba tập con riêng biệt: Training set, Validation set và Test set? Nêu vai trò độc lập của từng tập con này trong việc xây dựng mô hình.
* **expected_key_points:**
  - id: KP3_1
    content: Vai trò cập nhật trọng số của tập Training set
    keypoint_weight: 0.4
    description: Tập Training set chiếm tỷ lệ lớn nhất, được mô hình sử dụng trực tiếp để học các đặc trưng, tìm kiếm quy luật và cập nhật các tham số nội tại (như trọng số weights và bias) thông qua quá trình huấn luyện tối ưu hóa.
  - id: KP3_2
    content: Vai trò tinh chỉnh siêu tham số của tập Validation set
    keypoint_weight: 0.3
    description: Tập Validation set được dùng để đánh giá độc lập hiệu năng của các mô hình khác nhau trong quá trình thử nghiệm, từ đó giúp người thiết kế lựa chọn cấu trúc và tinh chỉnh các siêu tham số (Hyperparameters) tối ưu nhất mà không gây rò rỉ dữ liệu kiểm thử.
  - id: KP3_3
    content: Vai trò đánh giá khả năng tổng quát hóa cuối cùng của tập Test set
    keypoint_weight: 0.3
    description: Tập Test set hoàn toàn bị cô lập trong suốt quá trình huấn luyện và chọn siêu tham số. Nó chỉ được sử dụng duy nhất một lần ở bước cuối cùng để đo lường khách quan khả năng tổng quát hóa (Generalization) của mô hình đã hoàn thiện trên dữ liệu thực tế ngoài đời.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong chuẩn bị đặc trưng dữ liệu (Feature Engineering) cho các biến danh mục (Categorical Variables), hãy phân biệt cơ chế hoạt động và trường hợp áp dụng hiệu quả giữa kỹ thuật Label Encoding và One-Hot Encoding.
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế hoạt động và rủi ro thứ tự giả định của Label Encoding
    keypoint_weight: 0.4
    description: Label Encoding chuyển đổi mỗi giá trị danh mục thành một số nguyên duy nhất (ví dụ: Đỏ -> 0, Xanh -> 1). Kỹ thuật này đơn giản, không làm tăng chiều dữ liệu nhưng có rủi ro là các thuật toán (như Hồi quy, KNN) sẽ tự nhận diện các con số này có mối quan hệ thứ tự lớn nhỏ (0 < 1), gây sai lệch logic mô hình. Chỉ nên dùng khi biến danh mục thực sự có tính thứ tự (Ordinal data, ví dụ: Tiểu học -> 0, Đại học -> 1).
  - id: KP4_2
    content: Cơ chế hoạt động giãn nở chiều dữ liệu của One-Hot Encoding
    keypoint_weight: 0.4
    description: One-Hot Encoding tạo ra thêm N cột nhị phân (với N là số lượng giá trị danh mục độc nhất), trong đó chỉ có duy nhất một cột mang giá trị 1 và các cột còn lại mang giá trị 0 cho mỗi dòng dữ liệu. Kỹ thuật này loại bỏ hoàn toàn ràng buộc thứ tự giả định, tối ưu cho các biến danh mục không có tính thứ tự (Nominal data).
  - id: KP4_3
    content: Điểm hạn chế về "Lời nguyền đa chiều" (Curse of Dimensionality)
    keypoint_weight: 0.2
    description: One-Hot Encoding sẽ làm phình to số lượng chiều dữ liệu (Sparse matrix) cực kỳ nhanh nếu biến danh mục có độ đa dạng giá trị cao (High cardinality, ví dụ: mã bưu chính, tên thành phố), làm chậm tốc độ huấn luyện và tốn RAM của các mô hình.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy trình bày nguyên lý hoạt động của kỹ thuật kiểm giá chéo K-Fold Cross-Validation. Kỹ thuật này giải quyết điểm hạn chế gì của phương pháp chia dữ liệu Train/Test thông thường (Hold-out method)?
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế phân chia và lặp vòng tròn tính điểm của K-Fold Cross-Validation
    keypoint_weight: 0.5
    description: Chia đều tập dữ liệu thành K phần con (Folds) có kích thước bằng nhau. Tiến trình huấn luyện lặp lại K lần: tại mỗi lần lặp, hệ thống chọn một Fold khác nhau làm tập kiểm thử (Validation fold) và dùng K-1 Folds còn lại làm tập huấn luyện (Training folds). Điểm hiệu năng cuối cùng của mô hình là giá trị trung bình cộng của các điểm đo lường ở cả K lần chạy.
  - id: KP5_2
    content: Giải quyết rủi ro sai lệch chọn mẫu (Sampling bias) của phương pháp Hold-out
    keypoint_weight: 0.5
    description: Phương pháp chia cắt dữ liệu cố định (Hold-out) dễ bị sai lệch nếu tập dữ liệu nhỏ hoặc phân phối nhãn không đều (may mắn bốc trúng tập Test dễ hoặc cực khó). K-Fold giải quyết triệt để vấn đề này bằng cách đảm bảo mọi dòng dữ liệu thô đều có cơ hội được xuất hiện trong tập huấn luyện và tập kiểm thử ít nhất một lần, giúp đánh giá hiệu năng mô hình ổn định và chính xác hơn.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong thuật toán cây quyết định (Decision Tree), thế nào là hiện tượng cây bị quá khớp (Overfitting)? Hãy nêu hai kỹ thuật cắt tỉa cây (Pruning techniques) bao gồm Pre-pruning và Post-pruning để kiểm soát độ phức tạp của cây.
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên nhân cây quyết định dễ bị Overfitting khi không giới hạn kích thước
    keypoint_weight: 0.4
    description: Nếu không có ràng buộc, cây quyết định sẽ tiếp tục phân nhánh liên tục cho đến khi mọi nút lá đều thuần khiết tuyệt đối hoặc không thể chia nhỏ được nữa. Điều này khiến cây có độ sâu quá mức, học thuộc lòng cả các chi tiết nhiễu ngẫu nhiên trong tập Train, dẫn đến Overfitting.
  - id: KP6_2
    content: Nguyên lý kiểm soát bằng chặn sớm từ đầu của Pre-pruning
    keypoint_weight: 0.3
    description: Pre-pruning (Cắt tỉa sớm) thực hiện đặt ra các rào cản chặn đứng quá trình phân nhánh của cây ngay trong khi huấn luyện nếu không thỏa mãn điều kiện cấu hình (ví dụ: giới hạn độ sâu tối đa max_depth, giới hạn số mẫu tối thiểu ở nút lá min_samples_leaf, hoặc độ tăng thông tin tối thiểu min_impurity_decrease).
  - id: KP6_3
    content: Nguyên lý gộp ngược sau khi huấn luyện của Post-pruning
    keypoint_weight: 0.3
    description: Post-pruning (Cắt tỉa sau) cho phép cây quyết định phát triển tự do đạt kích thước tối đa trước. Sau đó, thuật toán sẽ duyệt ngược từ dưới lên, phân tích và chủ động gộp các nút lá hoặc nhánh con không mang lại sự cải thiện hiệu năng thực tế trên tập Validation thành một nút lá lớn để đơn giản hóa mô hình.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi đo lường hiệu năng của mô hình hồi quy (Regression), hãy định nghĩa công thức toán học và ý nghĩa thực tế của chỉ số hệ số xác định R-squared ($R^2$). Điều gì xảy ra nếu mô hình dự báo của bạn có giá trị $R^2$ nhỏ hơn 0?
* **expected_key_points:**
  - id: KP7_1
    content: Công thức toán học và ý nghĩa tỉ lệ phương sai giải thích được của R-squared
    keypoint_weight: 0.5
    description: R-squared ($R^2 = 1 - (SS_{res} / SS_{tot})$) đo lường tỷ lệ phần trăm sự biến động (phương sai) của biến mục tiêu mà mô hình có khả năng giải thích và nắm bắt được dựa trên các biến độc lập đầu vào. Nó chạy trong khoảng từ 0 đến 1 đối với các mô hình thông thường.
  - id: KP7_2
    content: Định nghĩa mốc so sánh với mô hình cơ sở (Baseline model)
    keypoint_weight: 0.3
    description: Giá trị R-squared bằng 0 tương ứng với hiệu năng của một mô hình cơ sở (Baseline) cực kỳ đơn giản - luôn dự báo giá trị bằng số trung bình cộng (Mean) của biến mục tiêu trong mọi trường hợp.
  - id: KP7_3
    content: Hệ quả thực tế và ý nghĩa khi chỉ số R-squared âm ($R^2 < 0$)
    keypoint_weight: 0.2
    description: Giá trị $R^2 < 0$ chứng tỏ mô hình dự báo hoạt động cực kỳ kém, sai số dự báo của mô hình còn tệ hơn và lớn hơn cả việc sử dụng một đường nằm ngang lấy giá trị trung bình cộng của biến mục tiêu để dự báo trong mọi tình huống.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong các bài toán tối ưu hóa của học máy (như huấn luyện mạng nơ-ron hoặc hồi quy), thuật toán tối ưu Gradient Descent hoạt động dựa trên nguyên lý toán học nào? Hãy giải thích ý nghĩa của tham số Learning Rate (Tốc độ học) và hậu quả của việc chọn Learning Rate quá nhỏ hoặc quá lớn.
* **expected_key_points:**
  - id: KP8_1
    content: Nguyên lý tìm cực trị dựa trên đạo hàm ngược hướng của Gradient Descent
    keypoint_weight: 0.4
    description: Gradient Descent tìm kiếm giá trị tối thiểu của hàm mất mát bằng cách lặp đi lặp lại việc cập nhật các tham số (weights) theo hướng ngược lại với hướng của vectơ đạo hàm riêng (Gradient) tại điểm hiện tại: w = w - \alpha \cdot \nabla L(w). Vectơ gradient chỉ hướng dốc lên nhanh nhất, nên đi ngược hướng gradient giúp ta di chuyển dần về phía đáy thung lũng (điểm cực tiểu).
  - id: KP8_2
    content: Tác động hiệu năng khi cấu hình Learning Rate quá nhỏ
    keypoint_weight: 0.3
    description: Khi Learning Rate (\alpha) quá nhỏ, các bước di chuyển cập nhật trọng số sẽ cực kỳ ngắn. Mô hình mất rất nhiều thời gian tính toán và số lượng vòng lặp khổng lồ để hội tụ về điểm tối ưu, đồng thời dễ dàng bị mắc kẹt vĩnh viễn ở các điểm cực tiểu cục bộ nông (Local Minima) trên bề mặt hàm lỗi.
  - id: KP8_3
    content: Tác động hiệu năng khi cấu hình Learning Rate quá lớn
    keypoint_weight: 0.3
    description: Khi Learning Rate (\alpha) quá lớn, các bước nhảy trọng số sẽ quá dài. Điều này khiến thuật toán bị dao động mạnh quanh điểm tối ưu, liên tục nhảy qua nhảy lại giữa hai sườn dốc và không thể hội tụ (Overshooting), thậm chí làm hàm mất mát bị phân kỳ (Diverge) dẫn đến lỗi tính toán tràn số.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong mô hình Support Vector Machine (SVM) dành cho bài toán phân lớp, siêu phẳng biên cực đại (Maximum Margin Hyperplane) là gì? Hãy định nghĩa hàm toán học của khoảng cách lề (Margin) và phân biệt sự khác biệt về triết lý xử lý biên giữa Hard-margin SVM và Soft-margin SVM.
* **expected_key_points:**
  - id: KP9_1
    content: Định nghĩa hình học của siêu phẳng phân tách và các Vectơ hỗ trợ (Support Vectors)
    keypoint_weight: 0.4
    description: SVM tìm kiếm một siêu phẳng phân tách tuyến tính tối ưu nằm ở chính giữa hai lớp dữ liệu sao cho khoảng cách lề (Margin) từ siêu phẳng đó đến các điểm dữ liệu gần nhất của cả hai lớp (gọi là Support Vectors) đạt giá trị lớn nhất, nhằm tăng cường khả năng tổng quát hóa trên dữ liệu mới.
  - id: KP9_2
    content: Nguyên lý loại bỏ hoàn toàn sai số của Hard-margin SVM
    keypoint_weight: 0.3
    description: Hard-margin SVM áp dụng một ràng buộc cứng nhắc: yêu cầu tất cả các mẫu dữ liệu huấn luyện bắt buộc phải được phân loại chính xác tuyệt đối và không có bất kỳ điểm nào được phép vi phạm hoặc nằm lấn vào không gian của lề (Margin). Mô hình này chỉ khả thi khi dữ liệu phân tách tuyến tính hoàn hảo và rất nhạy cảm với nhiễu.
  - id: KP9_3
    content: Cơ chế nới lỏng ràng buộc bằng biến bù sai số (Slack Variables) của Soft-margin SVM
    keypoint_weight: 0.3
    description: Soft-margin SVM chấp nhận nới lỏng ràng buộc bằng cách đưa thêm các biến bù sai số (Slack Variables \xi_i) vào hàm mục tiêu tối ưu, cho phép một số mẫu dữ liệu bị phân loại sai hoặc nằm đè lên lề để đổi lấy một siêu phẳng có lề rộng hơn, ổn định hơn. Mức độ trừng phạt sai số được kiểm soát thông qua siêu tham số C.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong xử lý dữ liệu dạng chuỗi thời gian hoặc xử lý ngôn ngữ tự nhiên (NLP) với mạng nơ-ron hồi quy (Recurrent Neural Networks - RNN), hãy giải thích nguyên nhân bản chất toán học gây ra hiện tượng Triệt tiêu đạo hàm (Gradient Vanishing) khi thực hiện thuật toán Lan truyền ngược qua thời gian (BPTT).
* **expected_key_points:**
  - id: KP10_1
    content: Nguyên lý hoạt động chia sẻ trọng số theo thời gian của kiến trúc RNN
    keypoint_weight: 0.3
    description: RNN xử lý dữ liệu tuần tự bằng cách duy trì một trạng thái ẩn (Hidden state) cập nhật liên tục qua các bước thời gian. Điều cốt lõi là ma trận trọng số chuyển dịch trạng thái ẩn (W_{hh}) được chia sẻ chung và sử dụng lặp đi lặp lại ở tất cả các bước thời gian từ t=1 đến t=T.
  - id: KP10_2
    content: Phép nhân ma trận lũy thừa trong quy tắc chuỗi của Backpropagation Through Time (BPTT)
    keypoint_weight: 0.4
    description: Khi tính toán đạo hàm riêng của hàm mất mát ở bước thời gian muộn đối với các trọng số ở các bước thời gian rất sớm, thuật toán BPTT phải áp dụng quy tắc chuỗi liên tục qua các bước. Quá trình này sinh ra một chuỗi tích của các ma trận trọng số chuyển dịch trạng thái: \prod_{j=k+1}^{t} W_{hh}^T. Bản chất toán học của chuỗi tích này tương đương với phép nâng lũy thừa ma trận W_{hh}^{t-k}.
  - id: KP10_3
    content: Hệ quả suy biến đạo hàm theo hàm số mũ dựa trên giá trị trị riêng (Eigenvalues) của ma trận
    keypoint_weight: 0.3
    description: Nếu giá trị trị riêng lớn nhất (Largest Eigenvalue) của ma trận trọng số W_{hh}$ nhỏ hơn 1, khi số lượng bước thời gian tăng lên (chuỗi dài), phép nâng lũy thừa ma trận sẽ khiến các giá trị trong ma trận kết quả bị co rút và suy giảm cực nhanh theo hàm số mũ tiến sát về bằng 0. Đạo hàm bị triệt tiêu hoàn toàn khiến mạng RNN không thể học được các mối liên kết ngữ cảnh dài hạn (Long-term dependencies).