# Bộ Câu Hỏi Phỏng Vấn Data Scientist (Level 1)

* **Role:** Data Scientist
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Hàm kích hoạt Leaky ReLU là gì và nó giải quyết điểm hạn chế chí tử nào của hàm ReLU truyền thống trong quá trình huấn luyện mạng nơ-ron?
* **expected_key_points:**
  - id: KP1_1
    content: Nguyên lý toán học và cấu trúc của hàm Leaky ReLU
    keypoint_weight: 0.5
    description: Leaky ReLU giữ nguyên giá trị dương của đầu vào (y = x nếu x > 0), nhưng thay vì ép giá trị bằng 0 tuyệt đối khi đầu vào âm như ReLU, nó cho phép một dòng rò rỉ nhỏ bằng cách nhân với một hệ số alpha rất bé (y = alpha * x với alpha thường bằng 0.01).
  - id: KP1_2
    content: Khắc phục hiện tượng chết nơ-ron (Dying ReLU Problem)
    keypoint_weight: 0.5
    description: Khi nơ-ron rơi vào vùng giá trị âm, đạo hàm của ReLU bằng 0 khiến các trọng số không được cập nhật và nơ-ron bị chết vĩnh viễn. Leaky ReLU có đạo hàm vùng âm bằng alpha (khác 0), đảm bảo gradient vẫn tiếp tục lan truyền ngược, duy trì khả năng học của nơ-ron.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong giai đoạn tiền xử lý dữ liệu danh mục (Categorical Features), khi gặp một biến có quá nhiều giá trị khuyết thiếu (Missing Values) nhưng vẫn mang ý nghĩa logic nghiệp vụ, bạn xử lý ra sao mà không cần dùng đến kỹ thuật gán giá trị (Imputation) hay xóa bỏ dòng dữ liệu?
* **expected_key_points:**
  - id: KP2_1
    content: Cơ chế tạo lớp nhãn khuyết thiếu độc lập (Missing Category)
    keypoint_weight: 0.5
    description: Thay vì gán giá trị trung bình hay giá trị phổ biến, ta coi phần dữ liệu khuyết thiếu là một nhóm danh mục hoàn toàn hợp lệ và đặt tên cho nó (ví dụ: "Unknown" hoặc "Missing").
  - id: KP2_2
    content: Bảo toàn thông tin logic và cấu trúc của mô hình
    keypoint_weight: 0.5
    description: Việc chuyển đổi này giúp bảo toàn toàn bộ kích thước mẫu của tập dữ liệu huấn luyện, đồng thời cho phép các thuật toán học máy (như cây quyết định) tự động học xem hành vi khuyết thiếu thông tin đó có mối tương quan đặc thù nào với biến mục tiêu hay không.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong lý thuyết thống kê, hãy định nghĩa phân phối Poisson (Poisson Distribution). Nêu một kịch bản thực tế trong doanh nghiệp có thể áp dụng phân phối này để mô hình hóa bài toán.
* **expected_key_points:**
  - id: KP3_1
    content: Định nghĩa bản chất toán học đếm sự kiện của phân phối Poisson
    keypoint_weight: 0.5
    description: Phân phối Poisson là phân phối xác suất rời rạc đo lường xác suất xảy ra của một số lượng sự kiện nhất định trong một khoảng thời gian hoặc không gian cố định, với điều kiện các sự kiện này xảy ra độc lập và với một tỷ lệ trung bình lambda biết trước.
  - id: KP3_2
    content: Kịch bản ứng dụng thực tế phù hợp
    keypoint_weight: 0.5
    description: Ví dụ mô hình hóa số lượng khách hàng truy cập vào trang web e-commerce hằng giờ, số lượng cuộc gọi đến tổng đài chăm sóc khách hàng trong một phút, hoặc số lượng giao dịch lỗi phát sinh hệ thống trong ngày.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong kỹ thuật trích chọn đặc trưng (Feature Selection), hãy phân biệt sự khác biệt cốt lõi về giả định phân phối và loại mối quan hệ dữ liệu giữa hệ số tương quan Pearson và hệ số tương quan hạng Spearman.
* **expected_key_points:**
  - id: KP4_1
    content: Giả định phân phối chuẩn và quan hệ tuyến tính của hệ số Pearson
    keypoint_weight: 0.5
    description: Hệ số Pearson yêu cầu các biến số phải tuân theo phân phối chuẩn và chỉ đo lường mối quan hệ tuyến tính thẳng giữa hai biến. Nó cực kỳ nhạy cảm với các giá trị ngoại lai.
  - id: KP4_2
    content: Tính toán phi tham số dựa trên thứ hạng hạng của hệ số Spearman
    keypoint_weight: 0.5
    description: Hệ số Spearman là một kiểm định phi tham số, tính toán hệ số tương quan dựa trên thứ hạng (Ranks) của dữ liệu thay vì giá trị vật lý thô. Nó đo lường mối quan hệ đơn điệu (Monotonic relationship), không yêu cầu dữ liệu tuân theo phân phối chuẩn và có khả năng chống chịu ngoại lai rất tốt.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy trình bày cơ chế hoạt động tối ưu hóa của giải thuật Batch Gradient Descent khi được tích hợp thêm kỹ thuật phạt L2 Regularization (Ridge Penalty) vào hàm mất mát.
* **expected_key_points:**
  - id: KP5_1
    content: Công thức tổng quát có thành phần phạt bình phương trọng số
    keypoint_weight: 0.5
    description: Hàm mục tiêu mới bằng tổng sai số của toàn bộ tập dữ liệu huấn luyện cộng thêm thành phần phạt L2: L = Loss + lambda * sum(w_i^2). Thành phần phạt này trừng phạt các mô hình có trọng số phình to quá mức.
  - id: KP5_2
    content: Cơ chế co rút trọng số (Weight Decay) qua từng bước lặp
    keypoint_weight: 0.5
    description: Khi tính đạo hàm, thành phần phạt L2 sinh ra hằng số tỷ lệ thuận với chính trọng số hiện tại. Trong công thức cập nhật, trọng số cũ sẽ bị nhân bớt đi một hệ số nhỏ hơn 1 trước khi trừ đi gradient của loss thô, ép các trọng số thu nhỏ đồng đều tiệm cận về sát mức 0 để chống Overfitting.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong các bài toán hồi quy (Regression) chứa nhiều nhiễu ngoại lai, hàm mất mát Log-Cosh Loss thường đem lại độ ổn định cao. Hãy giải thích công thức logic hoạt động và ưu điểm hình học của Log-Cosh Loss so với MSE và MAE.
* **expected_key_points:**
  - id: KP6_1
    content: Công thức toán học hàm logarit-cos-hyperbolic của Log-Cosh Loss
    keypoint_weight: 0.5
    description: Log-Cosh Loss tính toán giá trị dựa trên logarit tự nhiên của hàm cos hyperbolic của sai số dự báo: L(y, y_pred) = log(cosh(y_pred - y)).
  - id: KP6_2
    content: Ưu điểm hình học mượt mà và khả vi trơn tru tại điểm gốc
    keypoint_weight: 0.5
    description: Với sai số nhỏ, Log-Cosh hoạt động tương tự như một nửa của hàm bình phương MSE, giúp đồ thị mượt mà. Với sai số lớn do ngoại lai, đồ thị tiệm cận thành một đường thẳng tuyến tính tương tự như hàm MAE, giúp chống phóng đại sai số biên. Điểm vượt trội của nó so với MAE là khả vi liên tục (trơn tru) tại điểm sai số bằng 0, giúp Gradient Descent không bị dao động nhiễu vòng quanh đáy.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi đánh giá một mô hình phân loại đa lớp trên tập dữ liệu bị mất cân bằng nhãn nặng, tại sao chỉ số G-Mean (Geometric Mean) lại khách quan hơn chỉ số Accuracy? Hãy giải thích công thức tính chỉ số này.
* **expected_key_points:**
  - id: KP7_1
    content: Công thức tính trung bình nhân các độ chính xác cục bộ của G-Mean
    keypoint_weight: 0.5
    description: G-Mean được tính bằng căn bậc n của tích các chỉ số độ chính xác cục bộ (Sensitivity/Recall) của tất cả n lớp nhãn mục tiêu trong hệ thống: G-Mean = (Recall_1 * Recall_2 * ... * Recall_n)^(1/n).
  - id: KP7_2
    content: Cơ chế trừng phạt hiệu năng phân phối không đồng đều
    keypoint_weight: 0.5
    description: Do sử dụng phép nhân (trung bình nhân), nếu mô hình hoạt động cực tốt ở lớp đa số nhưng lại thất bại hoàn toàn (Recall bằng 0) ở một lớp thiểu số rare, chỉ số G-Mean tổng thể sẽ lập tức bị kéo sụt giảm về 0 tuyệt đối. Điều này ép buộc mô hình phải cân bằng năng lực nhận diện trên tất cả các nhóm nhãn, loại bỏ sự đánh giá sai lệch của Accuracy.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong các mô hình xử lý ngôn ngữ tự nhiên (NLP) lớn dựa trên kiến trúc Transformer, tại sao kỹ thuật Layer Normalization lại được sử dụng thay thế cho Batch Normalization? Hãy giải thích sự khác biệt cốt lõi về không gian chuẩn hóa giữa hai kỹ thuật này.
* **expected_key_points:**
  - id: KP8_1
    content: Không gian chuẩn hóa theo trục lô của Batch Normalization và điểm yếu trong NLP
    keypoint_weight: 0.4
    description: Batch Normalization tính toán giá trị trung bình và phương sai trên toàn bộ các mẫu thuộc mini-batch cho từng đặc trưng độc