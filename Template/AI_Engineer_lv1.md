# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 1)

* **Role:** AI Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong các bài toán Phân loại (Classification), ma trận nhầm lẫn Confusion Matrix dùng để làm gì? Nêu tên các thành phần cốt lõi trong ma trận này.
* **Đáp án mẫu:** Confusion Matrix dùng để trực quan hóa và đánh giá chi tiết hiệu năng của mô hình phân loại. Các thành phần cốt lõi gồm: True Positive (TP), True Negative (TN), False Positive (FP), và False Negative (FN).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Kỹ thuật Regularization (như L1 và L2) được thêm vào hàm mất mát (Loss function) nhằm mục đích gì? Sự khác biệt chính về mặt kết quả giữa L1 và L2 là gì?
* **Đáp án mẫu:** Mục đích nhằm phạt các trọng số có giá trị quá lớn để giảm thiểu hiện tượng Overfitting. Khác biệt: L1 (Lasso) có xu hướng đưa các trọng số không quan trọng về bằng 0 (tạo ra ma trận thưa), trong khi L2 (Ridge) chỉ thu nhỏ trọng số về gần 0 chứ không triệt tiêu hoàn toàn.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Khi xây dựng một mạng nơ-ron truyền thẳng (Feedforward Neural Network), kỷ thuật Khởi tạo trọng số (Weight Initialization) như Xavier hay He có vai trò gì?
* **Đáp án mẫu:** Kỹ thuật này giúp thiết lập các giá trị trọng số ban đầu một cách tối ưu dựa trên số lượng nơ-ron đầu vào và đầu ra của lớp đó, ngăn chặn hiện tượng bùng nổ đạo hàm (Exploding Gradient) hoặc biến mất đạo hàm (Vanishing Gradient) ngay khi mạng bắt đầu huấn luyện.

---

## CÂU HỎI TRUNG BÌNH (4 câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thuật toán tối ưu Stochastic Gradient Descent (SGD) khác với Batch Gradient Descent truyền thống như thế nào về cách cập nhật trọng số?
* **Đáp án mẫu:** Batch Gradient Descent tính toán đạo hàm trên toàn bộ tập dữ liệu rồi mới cập nhật trọng số một lần per epoch (chậm và tốn tài nguyên). SGD cập nhật trọng số ngay sau khi tính toán đạo hàm của từng mẫu dữ liệu đơn lẻ (nhanh hơn nhưng đồ thị loss sẽ dao động mạnh hơn).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong xử lý ngôn ngữ tự nhiên (NLP) với mô hình Bag-of-Words, chỉ số TF-IDF (Term Frequency - Inverse Document Frequency) giải quyết nhược điểm gì của việc chỉ đếm tần suất xuất hiện của từ (Word Count)?
* **Đáp án mẫu:** Word Count thường đánh giá cao các từ xuất hiện nhiều nhưng ít mang giá trị phân loại (nhũ "and", "the", "là", "bởi vì"). TF-IDF giải quyết bằng cách hạ thấp trọng số của các từ xuất hiện phổ biến ở tất cả các văn bản, đồng thời làm nổi bật các từ đặc trưng chỉ xuất hiện ở một vài văn bản cụ thể.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Kỹ thuật K-Fold Cross-Validation hoạt động như thế nào và tại sao nó lại giúp đánh giá mô hình khách quan hơn cách chia Train/Test thông thường?
* **Đáp án mẫu:** Hoạt động bằng cách chia dữ liệu thành K phần bằng nhau; mô hình sẽ được huấn luyện K lần, mỗi lần dùng K-1 phần để Train và 1 phần còn lại để Validate. Kết quả cuối cùng là trung bình cộng của K lần thử nghiệm, giúp đảm bảo mọi phần dữ liệu đều được dùng để huấn luyện và kiểm thử, giảm thiểu sự sai lệch do việc chia dữ liệu ngẫu nhiên một lần gây ra.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong mạng nơ-ron tích chập (CNN), khái niệm "Stride" và "Padding" ảnh hưởng như thế nào đến kích thước của ma trận đặc trưng (Feature Map) đầu ra?
* **Đáp án mẫu:** Stride là bước nhảy của bộ lọc khi trượt trên ảnh (Stride càng lớn thì kích thước đầu ra càng giảm). Padding là việc thêm các giá trị (thường là số 0) vào viền xung quanh ảnh đầu vào, giúp bảo toàn kích thước không gian của ma trận đầu ra và tránh mất thông tin ở các cạnh ảnh.

---

## CÂU HỎI KHÓ (3 câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong kiến trúc Transformer, tại sao lại cần sử dụng cơ chế mã hóa vị trí (Positional Encoding) cho các vectơ từ đầu vào?
* **Đáp án mẫu:** Vì kiến trúc Transformer xử lý toàn bộ các từ trong câu song song cùng một lúc (không tuần tự như RNN). Do đó, mô hình không có khái niệm về thứ tự trước sau của các từ. Positional Encoding thêm thông tin về vị trí hình học của từ vào vectơ embedding để mạng hiểu được cấu trúc cú pháp ngữ cảnh dựa trên thứ tự từ.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Khi triển khai một hệ thống RAG (Retrieval-Augmented Generation) cơ bản kết hợp với Large Language Model (LLM), quy trình xử lý từ câu hỏi của người dùng cho đến khi trả ra câu trả lời cuối cùng diễn ra như thế nào?
* **Đáp án mẫu:** Quy trình gồm 3 bước cốt lõi: 
  1. Câu hỏi của người dùng được chuyển thành vectơ embedding.
  2. Hệ thống tìm kiếm (Retrieval) thực hiện so sánh độ tương đồng vectơ để lấy ra các đoạn văn bản chứa thông tin liên quan nhất từ cơ sở dữ liệu tri thức (Vector DB).
  3. Câu hỏi gốc cùng với các đoạn văn bản bổ trợ này được gộp chung vào một prompt (gọi là Context) rồi gửi cho LLM để mô hình tổng hợp và tạo ra câu trả lời chính xác.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Hiện tượng sụp đổ chế độ (Mode Collapse) trong mạng sinh đối kháng (GAN) là gì và biểu hiện của nó trên thực tế như thế nào?
* **Đáp án mẫu:** Mode Collapse là hiện tượng mạng sinh (Generator) tìm ra một vài phân phối dữ liệu đánh lừa được mạng phân biệt (Discriminator) tốt nhất và liên tục chỉ sinh ra một hoặc một nhóm nhỏ các mẫu tương tự nhau, thay vì sinh ra dữ liệu đa dạng phong phú từ toàn bộ không gian phân phối đích (ví dụ: mô hình sinh ảnh khuôn mặt nhưng chỉ sinh ra duy nhất một khuôn mặt giống nhau ở mọi lượt huấn luyện).