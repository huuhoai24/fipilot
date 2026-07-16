# Bộ Câu Hỏi Phỏng Vấn Data Scientist (Level 1)

* **Role:** Data Scientist
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Cả hai thuật toán K-Means và K-Medoids đều dùng để phân cụm dữ liệu phi giám sát dựa trên khoảng cách. Hãy phân biệt sự khác biệt cơ bản về cách xác định tọa độ của tâm cụm (Centroid vs Medoid) và giải thích tại sao K-Medoids lại có khả năng chống nhiễu ngoại lai (Outliers) tốt hơn K-Means.
* **expected_key_points:**
  - id: KP1_1
    content: Khác biệt bản chất trong cách tính tâm cụm (Mean vs Thực thể mẫu)
    keypoint_weight: 0.5
    description: Trong K-Means, tâm cụm (Centroid) được tính bằng giá trị trung bình cộng (Mean) tọa độ của tất cả các điểm trong cụm, do đó tọa độ này thường là một điểm ảo không tồn tại trong tập dữ liệu gốc. Trong K-Medoids, tâm cụm (Medoid) bắt buộc phải là một điểm dữ liệu thực tế có thật trong cụm, được chọn sao cho tổng khoảng cách từ nó đến tất cả các điểm khác trong cụm là nhỏ nhất.
  - id: KP1_2
    content: Cơ chế chống ngoại lai dựa trên hàm khoảng cách của K-Medoids
    keypoint_weight: 0.5
    description: Do K-Means dùng giá trị trung bình cộng, một vài điểm ngoại lai (Outliers) có giá trị cực biên sẽ kéo lệch vị trí tâm cụm ảo ra xa khỏi phân bổ số đông. K-Medoids dùng điểm thực tế tối thiểu hóa tổng khoảng cách (tương tự toán tử trung vị Median), giúp vị trí tâm cụm hoạt động ổn định và không bị chi phối bởi các điểm cực biên thưa thớt.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong tiền xử lý đặc trưng danh mục (Categorical Features), hãy giải thích cơ chế hoạt động của kỹ thuật Binary Encoding. Tại sao kỹ thuật này lại tối ưu hơn One-Hot Encoding khi xử lý các biến danh mục có độ đa dạng giá trị cao (High Cardinality)?
* **expected_key_points:**
  - id: KP2_1
    content: Cơ chế chuyển đổi tuần tự từ số nguyên sang chuỗi nhị phân
    keypoint_weight: 0.5
    description: Binary Encoding hoạt động qua các bước: đầu tiên chuyển đổi các chuỗi danh mục thành các số nguyên tuần tự (giống như Label Encoding), tiếp theo chuyển các số nguyên đó thành chuỗi nhị phân (0 và 1), cuối cùng tách các ký tự nhị phân này thành các cột đặc trưng độc lập.
  - id: KP2_2
    content: Giải quyết bài toán bùng nổ chiều dữ liệu bằng quy luật logarit
    keypoint_weight: 0.5
    description: Với biến danh mục có N lớp độc nhất, One-Hot Encoding yêu cầu tạo ra đúng N cột mới (gây phình to ma trận thưa). Binary Encoding tối ưu hơn vì nó kiểm soát số lượng cột tăng theo hàm logarit cơ số 2: số cột mới chỉ bằng log2(N). Ví dụ với 100 danh mục thành phố, One-Hot tốn 100 cột, trong khi Binary Encoding chỉ tốn 7 cột, giúp giảm chi phí bộ nhớ RAM đáng kể.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong lý thuyết xác suất và thống kê làm nền tảng cho khoa học dữ liệu, hãy định nghĩa phân phối Bernoulli (Bernoulli Distribution). Nêu công thức tính giá trị kỳ vọng (Expected Value) và phương sai (Variance) của một biến ngẫu nhiên tuân theo phân phối này.
* **expected_key_points:**
  - id: KP3_1
    content: Định nghĩa bản chất phép thử nhị phân của phân phối Bernoulli
    keypoint_weight: 0.5
    description: Phân phối Bernoulli là phân phối xác suất rời rạc của một biến ngẫu nhiên chỉ nhận hai giá trị đầu ra độc nhất: giá trị 1 (Thành công - Success) với xác suất p, và giá trị 0 (Thất bại - Failure) với xác suất 1-p. Thường dùng mô hình hóa cho các bài toán phân loại nhị phân như khách hàng rời bỏ hay ở lại.
  - id: KP3_2
    content: Công thức tính kỳ vọng và phương sai dựa trên tham số p
    keypoint_weight: 0.5
    description: Giá trị kỳ vọng (Mean) của phân phối Bernoulli bằng chính tham số p: E(X) = p. Phương sai (Variance) của phân phối được tính bằng tích số giữa xác suất thành công và thất bại: Var(X) = p*(1 - p).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong kỹ thuật trích chọn đặc trưng theo phương pháp lọc (Filter Method), chỉ số ANOVA F-value thường được áp dụng để đánh giá biến. Hãy giải thích nguyên lý toán học sử dụng chỉ số này để lọc ra các biến số đầu vào hữu ích cho bài toán phân loại nhị phân.
* **expected_key_points:**
  - id: KP4_1
    content: Nguyên lý tính toán tỷ lệ phương sai giữa các nhóm nhãn của ANOVA
    keypoint_weight: 0.5
    description: Chỉ số F-value tính toán tỷ lệ giữa phương sai của dữ liệu giữa các nhóm nhãn mục tiêu (Between-group variance) và phương sai nội bộ bên trong từng nhóm nhãn (Within-group variance). Giá trị F-value càng lớn chứng tỏ sự khác biệt về phân bổ giữa các nhóm càng rõ rệt.
  - id: KP4_2
    content: Tiêu chí toán học lựa chọn đặc trưng có năng lực phân tách
    keypoint_weight: 0.5
    description: Đối với một biến số đặc trưng liên tục, nếu giá trị F-value tính toán được đối với các nhóm nhãn mục tiêu càng lớn (tương ứng p-value càng nhỏ), chứng tỏ biến số đó chứa nhiều thông tin có năng lực phân tách mạnh mẽ giữa các lớp. Thuật toán lọc sẽ sắp xếp thứ tự và giữ lại các đặc trưng có F-value cao nhất để đưa vào huấn luyện mô hình.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thuật tối ưu hóa Mini-batch Gradient Descent hoạt động ra sao? Hãy phân tích sự đánh đổi về mặt hiệu năng tính toán phần cứng và độ ổn định của quỹ đạo hội tụ hàm mất mát khi ta tăng kích thước lô (Batch Size) từ nhỏ lên lớn.
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế chia nhỏ tập dữ liệu để tính toán gradient cục bộ
    keypoint_weight: 0.4
    description: Mini-batch Gradient Descent chia tập dữ liệu huấn luyện thành các gói nhỏ (Lô/Batches) có kích thước cố định để tính toán gradient của hàm mất mát và cập nhật trọng số mô hình tuần tự sau khi quét xong mỗi lô dữ liệu, thay vì dùng một mẫu độc lẻ hay toàn bộ tập dữ liệu.
  - id: KP5_2
    content: Tác động tối ưu hóa song song phần cứng của việc tăng Batch Size
    keypoint_weight: 0.3
    description: Khi tăng kích thước lô, hệ thống tận dụng tốt hơn năng lực tính toán song song vector hóa của phần cứng như GPU/TPU, giúp giảm số lượng bước cập nhật trọng số trong một Epoch và tăng tốc độ xử lý cơ học của tài nguyên xử lý dữ liệu lớn.
  - id: KP5_3
    content: Tác động phẳng hóa quỹ đạo hội tụ và rủi ro kẹt cực trị cục bộ khi lô quá lớn
    keypoint_weight: 0.3
    description: Kích thước lô quá lớn làm phẳng đường đi của gradient, quỹ đạo hội tụ ít biến động nhiễu hơn nhưng lại làm mất đi tính ngẫu biến của thuật toán. Việc thiếu nhiễu đồ thị khiến mô hình dễ bị mắc kẹt vĩnh viễn ở các bẫy điểm cực tiểu cục bộ nông (Local Minima) hoặc vùng yên ngựa, làm giảm khả năng tổng quát hóa so với kích thước lô vừa phải.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi xây dựng mô hình hồi quy (Regression) trong doanh nghiệp, bài toán đôi khi yêu cầu dự báo một khoảng giá trị thay vì một số cụ thể. Hãy giải thích công thức logic hoạt động và ưu điểm của hàm mất mát Quantile Loss (Hồi quy phân vị).
* **expected_key_points:**
  - id: KP6_1
    content: Công thức toán học phân tách điều kiện dựa trên trọng số phân vị alpha
    keypoint_weight: 0.5
    description: Quantile Loss áp dụng hàm phạt sai số không đối xứng dựa trên tham số phân vị alpha định trước (nằm trong khoảng 0 đến 1). Công thức: L = alpha * (y - y_pred) nếu y >= y_pred, và (alpha - 1) * (y - y_pred) nếu y < y_pred.
  - id: KP6_2
    content: Khả năng ước lượng khoảng tin cậy và kiểm soát rủi ro không đối xứng
    keypoint_weight: 0.5
    description: Hàm mất mát này cho phép điều khiển mô hình dự báo chính xác một phân vị cụ thể của phân phối dữ liệu (ví dụ phân vị 90%). Bằng cách huấn luyện hai mô hình riêng biệt với alpha thấp (ví dụ 0.1) và alpha cao (ví dụ 0.9), Data Scientist có thể xây dựng một khoảng dự báo tin cậy cho kết quả đầu ra, phục vụ kiểm soát rủi ro kinh doanh hằng ngày.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi đánh giá một mô hình phân loại trên tập dữ liệu bị mất cân bằng nhãn cực kỳ nghiêm trọng, tại sao đường cong Precision-Recall (PR Curve) lại được ưu tiên sử dụng thay thế hoàn toàn cho đường cong ROC Curve? Phân tích dựa trên sự tác động của nhãn tiêu cực đa số (True Negatives) lên các chỉ số cấu thành.
* **expected_key_points:**
  - id: KP7_1
    content: Thành phần cấu thành đường cong ROC và điểm yếu do chỉ số FPR nắm giữ
    keypoint_weight: 0.4
    description: ROC Curve biểu diễn TPR theo FPR. Chỉ số FPR được tính bằng FP / (TN + FP). Khi nhãn tiêu cực (Negative) chiếm đại đa số, giá trị TN cực kỳ khổng lồ, khiến mẫu số của FPR phình to, dẫn đến chỉ số FPR luôn giữ ở mức rất nhỏ sát 0 bất kể số lượng lỗi FP có biến động. ROC Curve sẽ cho kết quả đẹp một cách giả tạo.
  - id: KP7_2
    content: Cơ chế cô lập lớp thiểu số loại bỏ yếu tố TN của đường cong PR
    keypoint_weight: 0.4
    description: PR Curve biểu diễn Precision theo Recall (TPR). Công thức Precision = TP / (TP + FP) và Recall = TP / (TP + FN). Cả hai chỉ số này hoàn toàn không chứa thành phần TN (nhãn tiêu cực đa số) trong công thức tính toán, giúp tập trung hoàn toàn vào năng lực nhận diện lớp nhãn thiểu số quan trọng.
  - id: KP7_3
    content: Phản ánh trung thực hiệu năng mô hình trên tập dữ liệu lệch
    keypoint_weight: 0.2
    description: Do loại bỏ được sự chi phối của nhóm TN khổng lồ, PR Curve phản ánh cực kỳ nhạy cảm và trung thực các lỗi báo động giả (FP) phát sinh trên nhóm dữ liệu hiếm, giúp nhà khoa học dữ liệu đánh giá barem điểm chính xác hơn.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Kiến trúc Transformer đã tạo nên bước ngoặt lớn trong Deep Learning nhờ cơ chế Attention Mechanism (Self-Attention). Hãy giải thích bản chất toán học của quá trình tính toán ma trận Attention dựa trên ba thực thể đầu vào: Query (Q), Key (K), và Value (V).
* **expected_key_points:**
  - id: KP8_1
    content: Phép toán tích vô hướng ma trận đo lường độ tương đồng (Dot-product attention)
    keypoint_weight: 0.4
    description: Đầu tiên, thuật toán thực hiện phép nhân ma trận giữa Query (Q) và chuyển vị của Key (K): Q * K^T. Phép toán tích vô hướng này đo lường mức độ tương quan, độ tương đồng ngữ cảnh giữa từng từ khóa (token) đối với tất cả các từ còn lại trong chuỗi dữ liệu đầu vào.
  - id: KP8_2
    content: Công thức chuẩn hóa chống triệt tiêu đạo hàm kết hợp tầng Softmax
    keypoint_weight: 0.4
    description: Kết quả tích vô hướng được chia cho căn bậc hai của số chiều đặc trưng d_k để thu nhỏ miền giá trị, tránh việc rơi vào vùng bão hòa biên đạo hàm cực nhỏ của tầng tiếp theo. Sau đó, áp dụng hàm kích hoạt Softmax theo từng hàng để chuẩn hóa các giá trị thành một ma trận trọng số xác suất (Attention Weights) có tổng bằng 1. Công thức: Softmax( (Q*K^T) / sqrt(d_k) ).
  - id: KP8_3
    content: Phép tổ hợp tuyến tính trích xuất vector ngữ cảnh dựa trên ma trận Value (V)
    keypoint_weight: 0.2
    description: Cuối cùng, nhân ma trận trọng số xác suất thu được với ma trận Value (V) để thực hiện phép tổ hợp tuyến tính, trích xuất ra một vector embedding ngữ cảnh mới phong phú thông tin, giúp mô hình tập trung năng lượng vào các vùng thông tin quan trọng nhất của chuỗi.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích nguyên lý hoạt động của giải thuật Tối ưu hóa bầy đàn (Particle Swarm Optimization - PSO) khi áp dụng vào bài toán tối ưu hóa siêu tham số tự động. Giải thích ý nghĩa cơ chế cập nhật tọa độ cá thể dựa trên hai giá trị: pbest (Personal Best) và gbest (Global Best).
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế mã hóa không gian đa chiều và chấm điểm hàm thích nghi của PSO
    keypoint_weight: 0.4
    description: PSO mô phỏng hành vi xã hội của một đàn chim tìm kiếm thức ăn. Mỗi tổ hợp siêu tham số được coi là tọa độ của một hạt (Particle) di chuyển trong không gian đa chiều. Giải thuật khởi tạo một quần thể hạt ngẫu nhiên có vận tốc ban đầu, huấn luyện mô hình để tính điểm hiệu năng làm hàm thích nghi (Fitness) xác định độ tốt của vị trí hạt.
  - id: KP9_2
    content: Cơ chế cập nhật vận tốc dựa trên giá trị lịch sử cá nhân pbest
    keypoint_weight: 0.3
    description: pbest lưu trữ tọa độ vị trí cho điểm số Fitness cao nhất mà chính hạt đó từng tự đạt được trong lịch sử các bước lặp quá khứ. Thành phần toán học hướng về pbest đại diện cho xu hướng nhận thức độc lập của cá thể (Cognitive component).
  - id: KP9_3
    content: Cơ chế cập nhật vận tốc hướng đích dựa trên giá trị toàn cục gbest giúp cụm hội tụ
    keypoint_weight: 0.3
    description: gbest lưu trữ tọa độ vị trí tốt nhất tính trên toàn bộ tất cả các hạt trong bầy đàn từ đầu chương trình đến hiện tại. Thành phần toán học hướng về gbest đại diện cho xu hướng chia sẻ thông tin xã hội (Social component). Vectơ vận tộc mới của hạt là tổng hợp có trọng số ngẫu nhiên hướng về pbest và gbest, đẩy hạt di chuyển liên tục, cân bằng giữa khám phá vùng không gian mới và khai thác vùng tối ưu toàn cục.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Trong các bài toán học sâu phân loại hình ảnh hoặc phát hiện vật thể, hiện tượng mất cân bằng mẫu nghiêm trọng giữa lớp nền (Background) và vật thể cần tìm khiến hàm Cross-Entropy thông thường bị thất bại. Hãy giải thích công thức toán học và cơ chế trừng phạt động của hàm mất mát Focal Loss để giải quyết bài toán này.
* **expected_key_points:**
  - id: KP10_1
    content: Công thức toán học mở rộng tích hợp thành phần điều chỉnh (Modulating factor) của Focal Loss
    keypoint_weight: 0.4
    description: Focal Loss bổ sung một thành phần điều chỉnh động (Modulating factor) là (1 - p_t)^gamma vào công thức của hàm mất mát Cross-Entropy truyền thống. Công thức tổng quát: FL(p_t) = - (1 - p_t)^gamma * log(p_t), trong đó p_t là xác suất dự báo đúng nhãn thực tế của mô hình và gamma là siêu tham số điều khiển mức độ tập trung phạt.
  - id: KP10_2
    content: Cơ chế tự động giảm mạnh hình phạt đối với các mẫu dễ phân loại (Easy examples)
    keypoint_weight: 0.4
    description: Đối với các mẫu dữ liệu dễ phân loại (như lớp nền chiếm số đông), mô hình dự báo rất chính xác nên giá trị p_t tiến sát mốc 1. Khi đó, thành phần điều chỉnh (1 - p_t)^gamma sẽ tự động giảm sút tiệm cận về mức 0, làm triệt tiêu gần như hoàn toàn giá trị hàm loss phát sinh từ các mẫu dễ này, ngăn không cho chúng làm tràn ngập đồ thị gradient.
  - id: KP10_3
    content: Tập trung năng lượng tối ưu hóa vào các mẫu khó (Hard/Rare examples)
    keypoint_weight: 0.2
    description: Đối với các mẫu dữ liệu hiếm hoặc khó phân loại, giá trị p_t nhỏ (gần 0), khiến thành phần điều chỉnh (1 - p_t)^gamma tiến sát bằng 1. Hàm loss giữ nguyên giá trị phạt mạnh mẽ, ép buộc thuật toán Deep Learning tập trung toàn bộ tài nguyên cập nhật trọng số để giải quyết các mẫu khó, nâng cao năng lực ranh giới quyết định.