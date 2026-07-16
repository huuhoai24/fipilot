# Bộ Câu Hỏi Phỏng Vấn Data Scientist (Level 1)

* **Role:** Data Scientist
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong lý thuyết xác suất và thống kê, hãy định nghĩa phân phối đa thức (Multinomial Distribution). Nêu một kịch bản ứng dụng thực tế của phân phối này trong các bài toán xử lý ngôn ngữ tự nhiên (NLP) cơ bản.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa bản chất mở rộng phép thử Bernoulli của phân phối đa thức
    keypoint_weight: 0.5
    description: Phân phối đa thức là sự tổng quát hóa của phân phối nhị thức (Binomial Distribution). Nó mô hình hóa xác suất của các tổ hợp kết quả khi thực hiện một chuỗi các phép thử độc lập, trong đó mỗi phép thử có thể dẫn đến nhiều hơn hai kết quả rời rạc có thể xảy ra (k kết quả với các xác suất tương ứng p_1, p_2, ..., p_k sao cho tổng bằng 1).
  - id: KP1_2
    content: Kịch bản ứng dụng mô hình hóa tần suất từ vựng (Bag-of-Words) trong NLP
    keypoint_weight: 0.5
    description: Được ứng dụng để mô hình hóa tần suất xuất hiện của các từ khóa trong một văn bản (mô hình Bag-of-Words). Mỗi phép thử là việc chọn ngẫu nhiên một từ trong từ điển (thủ kho văn bản), các kết quả rời rạc chính là các từ độc nhất trong bộ từ vựng, rất phổ biến làm nền tảng cho thuật toán Multinomial Naive Bayes để phân loại văn bản.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Kỹ thuật Mean Target Encoding (hoặc Target Encoding) thường được dùng để tiền xử lý biến danh mục (Categorical Features). Hãy giải thích cơ chế hoạt động và nêu một khuyết điểm lớn về mặt quá khớp (Overfitting) khi áp dụng kỹ thuật này lên các nhóm danh mục có kích thước mẫu quá nhỏ.
* **expected_key_points:**
  - id: KP2_1
    content: Cơ chế mã hóa danh mục dựa trên giá trị trung bình của biến mục tiêu
    keypoint_weight: 0.5
    description: Target Encoding chuyển đổi các giá trị chuỗi danh mục bằng cách tính toán giá trị trung bình (Mean) của biến mục tiêu ứng với chính nhóm danh mục đó trong tập dữ liệu huấn luyện.
  - id: KP2_2
    content: Rủi ro rò rỉ thông tin dữ liệu (Target Leakage) trên nhóm mẫu nhỏ
    keypoint_weight: 0.5
    description: Do sử dụng trực tiếp thông tin của biến mục tiêu để sinh đặc trưng, nếu một nhóm danh mục chỉ chứa rất ít mẫu (ví dụ 1-2 mẫu), giá trị mã hóa sẽ bị chi phối tuyệt đối bởi biến mục tiêu của các mẫu đó. Điều này gây rò rỉ dữ liệu (Target Leakage), làm mô hình học vẹt tập Train một cách hoàn hảo nhưng mất khả năng dự báo chính xác trên tập Test.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Khi xây dựng thuật toán Cây quyết định (Decision Tree) cho bài toán phân loại, cả hai chỉ số Gini Impurity (Độ tạp chất Gini) và Entropy đều được dùng để lựa chọn vết cắt tối ưu. Hãy so sánh sự khác biệt cơ bản về mặt công thức toán học và chi phí tính toán phần cứng giữa hai chỉ số này.
* **expected_key_points:**
  - id: KP3_1
    content: Khác biệt về cấu trúc hàm toán học (Bình phương vs Logarit)
    keypoint_weight: 0.5
    description: Gini Impurity được tính toán dựa trên tổng bình phương xác suất của các lớp nhãn: Gini = 1 - sum(p_i^2). Entropy được tính toán dựa trên hàm logarit tự nhiên hoặc logarit cơ số 2 của xác suất: Entropy = -sum(p_i * log(p_i)). Do đó đồ thị hàm Entropy có xu hướng phạt nặng hơn một chút ở các vùng dữ liệu có độ tạp chất cao.
  - id: KP3_2
    content: Khác biệt về chi phí tài nguyên xử lý phần cứng máy tính
    keypoint_weight: 0.5
    description: Gini Impurity chỉ yêu cầu các phép toán nhân bình phương cơ bản, giúp Database Engine tính toán cực nhanh. Entropy bắt buộc phải xử lý phép toán logarit phi tuyến phức tạp ở runtime, tiêu tốn nhiều chu kỳ xử lý của CPU hơn, làm chậm tốc độ phân nhánh của cây khi xử lý tập dữ liệu lớn chứa hàng triệu dòng.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong các bài toán giảm chiều dữ liệu (Dimensionality Reduction), hãy phân biệt sự khác biệt cốt lõi về triết lý toán học và mục đích sử dụng giữa hai kỹ thuật PCA (Principal Component Analysis) và t-SNE (t-Distributed Stochastic Neighbor Embedding).
* **expected_key_points:**
  - id: KP4_1
    content: Bản chất tuyến tính bảo toàn phương sai toàn cục của PCA
    keypoint_weight: 0.4
    description: PCA là một thuật toán tuyến tính (Linear), thực hiện chiếu dữ liệu sang không gian mới nhằm tối đa hóa phương sai của dữ liệu trên các trục tọa độ mới (Principal Components). Nó tập trung bảo toàn cấu trúc hình học toàn cục (Global Structure) của dữ liệu, tối ưu cho việc giảm chiều giảm tải tham số trước khi huấn luyện mô hình.
  - id: KP4_2
    content: Bản chất phi tuyến bảo toàn cấu trúc lân cận cục bộ của t-SNE
    keypoint_weight: 0.4
    description: t-SNE là thuật toán phi tuyến (Non-linear), chuyển đổi khoảng cách hình học thành các phân phối xác suất biểu thị độ tương đồng. Nó tập trung tuyệt đối vào việc bảo toàn cấu trúc lân cận cục bộ (Local Structure - giữ các điểm gần nhau ở không gian cao vẫn gần nhau ở không gian thấp), không quan tâm đến khoảng cách xa.
  - id: KP4_3
    content: Khác biệt về ngữ cảnh áp dụng thực tế
    keypoint_weight: 0.2
    description: PCA được dùng làm bước tiền xử lý nén đặc trưng (Feature extraction) cho pipeline học máy nhờ tốc độ nhanh và tính ổn định. t-SNE hầu như chỉ được sử dụng cho mục đích trực quan hóa dữ liệu (Data Visualization) trong không gian 2D hoặc 3D do chi phí tính toán cực cao và không có hàm ánh xạ kiểm thử mẫu mới.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy trình bày cơ chế hoạt động tối ưu hóa của giải thuật Stochastic Gradient Descent (SGD) khi được tích hợp thêm kỹ thuật phạt L1 Regularization (Lasso Penalty) vào hàm mất mát. Kỹ thuật này tạo ra đặc tính gì cho bộ trọng số?
* **expected_key_points:**
  - id: KP5_1
    content: Công thức tổng quát có thành phần phạt trị tuyệt đối trọng số
    keypoint_weight: 0.4
    description: Hàm mục tiêu tối ưu mới bằng sai số tính trên mẫu dữ liệu ngẫu nhiên cộng thêm thành phần phạt L1: L = Loss + lambda * sum(|w_i|). Thành phần này trừng phạt độ lớn của hệ số theo hàm bậc nhất tuyến tính.
  - id: KP5_2
    content: Cơ chế đạo hàm hằng số ép tuyệt đối trọng số về bằng 0
    keypoint_weight: 0.4
    description: Do đạo hàm của thành phần phạt L1 đối với trọng số mang giá trị hằng số không phụ thuộc vào độ lớn của w (bằng +lambda hoặc -lambda dựa trên dấu của w), tại mỗi bước cập nhật, trọng số luôn bị trừ đi một lượng cố định bất kể giá trị lớn hay nhỏ. Cơ chế này ép trực tiếp các hệ số trọng số của các biến không quan trọng về bằng 0 một cách tuyệt đối.
  - id: KP5_3
    content: Đặc tính tạo mô hình thưa thớt (Sparse Model) trích chọn đặc trưng
    keypoint_weight: 0.2
    description: Hệ quả của việc ép trọng số về 0 giúp tạo ra một mô hình thưa thớt (Sparse model), đóng vai trò như một cơ chế tự động trích chọn đặc trưng (Feature Selection), loại bỏ hoàn toàn các biến nhiễu ra khỏi mô hình để tối ưu tài nguyên tính toán.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi xây dựng mô hình hồi quy (Regression) trong doanh nghiệp, bài toán đôi khi yêu cầu dự báo một khoảng giá trị thay vì một số cụ thể. Hãy giải thích công thức logic hoạt động và ưu điểm của hàm mất mát Quantile Loss (Hồi quy phân vị).
* **expected_key_points:**
  - id: KP6_1
    content: Công thức toán học phân tách điều kiện dựa trên trọng số phân vị alpha
    keypoint_weight: 0.5
    description: Quantile Loss áp dụng hàm phạt sai số không đối xứng dựa trên tham số phân vị alpha định trước (nằm trong khoảng 0 đến 1). Công thức: L = alpha * (y - y_pred) nếu y >= y_pred, và (1 - alpha) * (y_pred - y) nếu y < y_pred.
  - id: KP6_2
    content: Khả năng ước lượng khoảng tin cậy và kiểm soát rủi ro không đối xứng
    keypoint_weight: 0.5
    description: Hàm mất mát này cho phép điều khiển mô hình dự báo chính xác một phân vị cụ thể của phân phối dữ liệu. Bằng cách huấn luyện hai mô hình riêng biệt với alpha thấp (ví dụ 0.1) và alpha cao (ví dụ 0.9), Data Scientist có thể xây dựng một khoảng dự báo tin cậy cho kết quả đầu ra, phục vụ kiểm soát rủi ro kinh doanh hằng ngày.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi đánh giá một mô hình phân loại đa lớp trên tập dữ liệu bị mất cân bằng nhãn nặng, tại sao chỉ số G-Mean (Geometric Mean) lại khách quan và toàn diện hơn chỉ số Accuracy? Hãy giải thích công thức tính chỉ số này.
* **expected_key_points:**
  - id: KP7_1
    content: Công thức tính trung bình nhân các độ chính xác cục bộ của G-Mean
    keypoint_weight: 0.5
    description: G-Mean được tính bằng căn bậc n của tích các chỉ số độ chính xác cục bộ (Sensitivity/Recall) của tất cả n lớp nhãn mục tiêu trong hệ thống: G-Mean = (Recall_1 * Recall_2 * ... * Recall_n)^(1/n).
  - id: KP7_2
    content: Cơ chế trừng phạt hiệu năng phân phối không đồng đều loại bỏ bias nhãn đa số
    keypoint_weight: 0.5
    description: Do sử dụng phép toán trung bình nhân, nếu mô hình hoạt động cực tốt ở lớp đa số nhưng lại thất bại hoàn toàn (Recall bằng 0) ở một lớp thiểu số hiếm, chỉ số G-Mean tổng thể sẽ lập tức bị kéo sụt giảm về 0 tuyệt đối. Điều này ép buộc mô hình phải cân bằng năng lực nhận diện trên tất cả các nhóm nhãn, loại bỏ sự đánh giá sai lệch của Accuracy.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong các mô hình xử lý ngôn ngữ tự nhiên (NLP) lớn dựa trên kiến trúc Transformer, tại sao kỹ thuật Layer Normalization lại được sử dụng thay thế cho Batch Normalization? Hãy giải thích sự khác biệt cốt lõi về không gian dữ liệu chuẩn hóa giữa hai kỹ thuật này.
* **expected_key_points:**
  - id: KP8_1
    content: Không gian chuẩn hóa theo trục lô của Batch Normalization và điểm yếu trong NLP
    keypoint_weight: 0.4
    description: Batch Normalization tính toán giá trị trung bình và phương sai trên toàn bộ các mẫu thuộc mini-batch cho từng đặc trưng độc lập. Trong dữ liệu văn bản NLP, các câu có độ dài rất khác nhau (Variable sequence lengths); việc tính toán theo cột lô sẽ bị sai lệch nghiêm trọng do các ký tự đệm (Padding tokens) hoặc khi kích thước lô quá nhỏ lúc suy luận (Inference).
  - id: KP8_2
    content: Không gian chuẩn hóa nội bộ của Layer Normalization độc lập với kích thước lô
    keypoint_weight: 0.4
    description: Layer Normalization thực hiện tính toán giá trị trung bình và phương sai dựa trên tất cả các đặc trưng đầu vào của duy nhất một mẫu dữ liệu (Single data instance) độc lập tại một bước thời gian. Tiến trình này hoàn toàn không phụ thuộc vào các mẫu khác trong mini-batch.
  - id: KP8_3
    content: Tính ổn định dòng gradient trong cả giai đoạn Train và Inference
    keypoint_weight: 0.2
    description: Nhờ tính toán độc lập nội bộ mẫu, Layer Normalization hoạt động nhất quán và ổn định hoàn hảo xuyên suốt cả hai giai đoạn Huấn luyện và Suy luận thời gian thực, kiểm soát tốt hiện tượng bùng nổ hoặc triệt tiêu gradient trong các mạng tuần tự sâu.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích nguyên lý hoạt động của giải thuật Mô phỏng luyện kim (Simulated Annealing) khi áp dụng vào bài toán tối ưu hóa siêu tham số tự động. Giải thích ý nghĩa toán học của tham số Nhiệt độ (Temperature) và cơ chế chấp nhận một nghiệm tệ hơn thông qua phân phối Boltzmann.
* **expected_key_points:**
  - id: KP9_1
    content: Nguyên lý mô phỏng quá trình nhiệt động học làm nguội kim loại vật lý
    keypoint_weight: 0.4
    description: Giải thuật mô phỏng lại quá trình luyện kim, bắt đầu từ một trạng thái siêu tham số ngẫu nhiên ở mức Nhiệt độ (Temperature - T) cực kỳ cao. Qua từng vòng lặp, hệ thống thực hiện một bước nhảy ngẫu nhiên sang tọa độ lân cận và hạ dần nhiệt độ theo một quy luật lịch trình (Cooling schedule).
  - id: KP9_2
    content: Cơ chế chấp nhận nghiệm tệ hơn dựa trên phân phối xác suất Boltzmann để thoát bẫy cục bộ
    keypoint_weight: 0.4
    description: Nếu vị trí mới cho điểm hiệu năng tốt hơn, hệ thống chấp nhận ngay. Nếu vị trí mới cho kết quả tệ hơn, giải thuật không từ chối ngay lập tức mà tính toán một xác suất chấp nhận dựa trên phân phối Boltzmann: P = exp(-Delta_E / T), trong đó Delta_E là độ suy giảm hiệu năng. Cơ chế nhảy vào nghiệm tệ này mang tính sống còn giúp thuật toán thực hiện chiến lược khám phá (Exploration) để thoát khỏi các bẫy cực trị cục bộ.
  - id: KP9_3
    content: Sự chuyển dịch hành vi từ khám phá sang khai thác (Exploration đến Exploitation)
    keypoint_weight: 0.2
    description: Ở giai đoạn đầu, T rất lớn khiến xác suất P cao, mô hình tự do nhảy qua các sườn dốc hàm lỗi. Ở giai đoạn cuối, T giảm dần về sát mốc 0 khiến xác suất P tiệm cận về 0; giải thuật hầu như chỉ chấp nhận các nghiệm tốt hơn, thu hẹp phạm vi để hội tụ chặt chẽ vào điểm cực trị tối ưu toàn cục (Exploitation).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong các bài toán học sâu phân đoạn hình ảnh (Image Segmentation) hoặc xử lý dữ liệu y tế, hiện tượng mất cân bằng số lượng pixel giữa vùng vật thể cần tìm (nhỏ) và vùng nền (chiếm đa số) rất nặng nề làm sập hàm Cross-Entropy. Hãy giải thích cấu trúc toán học và ưu điểm của hàm mất mát Dice Loss đối với bài toán này.
* **expected_key_points:**
  - id: KP10_1
    content: Công thức toán học dựa trên chỉ số tương đồng vùng giao (Sørensen-Dice coefficient)
    keypoint_weight: 0.4
    description: Dice Loss được tính toán dựa trên chỉ số đo lường tỷ lệ trùng nhau của hai vùng không gian: Dice Loss = 1 - (2 * |A intersect B|) / (|A| + |B|). Trong học sâu, công thức được biểu diễn qua tích các xác suất dự báo và nhãn thực tế trên từng pixel.
  - id: KP10_2
    content: Cơ chế loại bỏ sự chi phối của vùng tiêu cực nền khổng lồ (True Negatives elimination)
    keypoint_weight: 0.4
    description: Điểm cốt lõi của công thức Dice Loss là hoàn toàn không chứa thành phần True Negatives (số lượng pixel thuộc vùng nền dự báo đúng) trong cấu trúc tính toán mẫu số hay tử số. Hàm lỗi chỉ tập trung đo lường độ phủ trùng khớp trực tiếp giữa vùng mặt nạ thực tế và mặt nạ dự báo, loại bỏ hoàn toàn sự tràn ngập bias của vùng nền.
  - id: KP10_3
    content: Duy trì dòng gradient ổn định trên vùng vật thể kích thước siêu nhỏ
    keypoint_weight: 0.2
    description: Do loại bỏ được sự tràn ngập của vùng nền khổng lồ, Dice Loss ngăn chặn hiện tượng đồ thị gradient bị phẳng hóa về 0. Hệ thống duy trì dòng cập nhật trọng số mạnh mẽ kể cả khi vật thể mục tiêu chỉ chiếm một diện tích vài pixel trên bức ảnh lớn, tối ưu hóa vùng biên quyết định.