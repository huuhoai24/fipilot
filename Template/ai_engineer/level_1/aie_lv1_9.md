# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 1)

* **Role:** AI Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong Machine Learning, hãy giải thích hiện tượng Data Leakage (Rò rỉ dữ liệu) là gì và nêu một ví dụ thực tế về cách nó xảy ra trong quá trình tiền xử lý dữ liệu.
* **expected_key_points:**
  - id: KP1_1
    content: Bản chất hiện tượng Data Leakage
    keypoint_weight: 0.5
    description: Là hiện tượng thông tin từ tập dữ liệu kiểm thử (Test/Validation set) vô tình bị trộn lẫn hoặc sử dụng trong quá trình huấn luyện mô hình (Training set), khiến mô hình có độ chính xác ảo cực cao lúc train nhưng tệ khi deploy thực tế.
  - id: KP1_2
    content: Ví dụ thực tế trong tiền xử lý dữ liệu (Scaling/Imputation)
    keypoint_weight: 0.5
    description: Thực hiện tính toán các giá trị thống kê như Mean, Standard Deviation hoặc MinMaxScaler trên toàn bộ Dataset trước khi thực hiện chia tách tập Train/Test, dẫn đến việc tập Train chứa thông tin phân phối của tập Test.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Tại sao người ta thường ưu tiên sử dụng hàm kích hoạt phi tuyến tính ReLU (Rectified Linear Unit) thay cho Sigmoid trong các tầng ẩn (Hidden Layers) của mạng nơ-ron sâu?
* **expected_key_points:**
  - id: KP2_1
    content: Khắc phục hiện tượng Triệt tiêu Đạo hàm (Vanishing Gradient)
    keypoint_weight: 0.5
    description: Hàm Sigmoid bị bão hòa ở hai đầu khiến đạo hàm tiến về sát 0 khi giá trị đầu vào lớn, gây triệt tiêu gradient ở mạng sâu. ReLU có đạo hàm bằng 1 cố định với mọi giá trị đầu vào dương, giữ cho dòng đạo hàm không bị suy giảm.
  - id: KP2_2
    content: Tối ưu hóa hiệu năng tính toán (Computational Efficiency)
    keypoint_weight: 0.5
    description: ReLU chỉ sử dụng phép toán so sánh đơn giản `max(0, x)` thay vì các phép toán lũy thừa phức tạp `e^-x` như Sigmoid, giúp tăng tốc độ tính toán Forward và Backward đáng kể.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Khi huấn luyện mô hình học máy, siêu tham số Batch Size (Kích thước lô) là gì? Phân biệt điểm khác nhau cơ bản giữa Mini-batch Gradient Descent và Stochastic Gradient Descent (SGD).
* **expected_key_points:**
  - id: KP3_1
    content: Định nghĩa siêu tham số Batch Size
    keypoint_weight: 0.4
    description: Batch Size quy định số lượng mẫu dữ liệu được nạp vào mạng để tính toán loss và cập nhật trọng số trong một bước lặp (Iteration).
  - id: KP3_2
    content: Điểm khác biệt về số lượng mẫu trong mỗi bước cập nhật
    keypoint_weight: 0.6
    description: Stochastic Gradient Descent (SGD) thực hiện cập nhật trọng số sau khi duyệt qua từng mẫu dữ liệu đơn lẻ (Batch Size = 1). Mini-batch Gradient Descent thực hiện cập nhật trọng số sau khi duyệt qua một nhóm mẫu (thường là 32, 64, 128).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong mạng nơ-ron tích chập (CNN), phép toán Receptive Field (Vùng cảm nhận) mang ý nghĩa gì? Kỹ thuật Dilated Convolution (Tích chập giãn khoảng) giúp mở rộng Receptive Field như thế nào?
* **expected_key_points:**
  - id: KP4_1
    content: Ý nghĩa logic của Receptive Field
    keypoint_weight: 0.5
    description: Receptive Field là vùng không gian trên ảnh đầu vào mà một neuron cụ thể ở tầng sâu có thể "nhìn thấy" và trích xuất đặc trưng. Tầng càng sâu thì Receptive Field càng lớn.
  - id: KP4_2
    content: Cơ chế chèn khoảng trống của Dilated Convolution
    keypoint_weight: 0.5
    description: Dilated Convolution chèn các khoảng trống (lỗ hổng) giữa các phần tử của bộ lọc (Kernel) dựa trên siêu tham số dilation rate, giúp mở rộng Receptive Field lớn hơn mà không làm tăng số lượng tham số cần tính toán.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Đối với các bài toán mất cân bằng dữ liệu nghiêm trọng, tại sao kỹ thuật Focal Loss lại vượt trội hơn hàm mất mát Standard Cross-Entropy thông thường trong việc huấn luyện mô hình phân loại?
* **expected_key_points:**
  - id: KP5_1
    content: Giảm trọng số của các mẫu dễ phân loại (Easy Examples)
    keypoint_weight: 0.5
    description: Focal Loss bổ sung một hệ số điều chế toán học $\left(1 - p_t\right)^\gamma$ vào hàm Cross-Entropy để chủ động giảm bớt đóng góp loss từ các mẫu dễ phân loại mà mô hình đã tự tin đoán đúng.
  - id: KP5_2
    content: Tập trung Gradient vào các mẫu khó (Hard/Rare Examples)
    keypoint_weight: 0.5
    description: Ép mạng nơ-ron tập trung cập nhật trọng số dựa trên các mẫu khó hoặc các lớp thiểu số (Minority classes) vốn có ít dữ liệu, ngăn chặn việc mô hình bị thao túng bởi các mẫu dễ thuộc lớp đa số.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Thuật toán tối ưu Gradient Descent tích hợp cơ chế Momentum (Quán tính) hoạt động dựa trên nguyên lý gì và nó giúp giải quyết lỗi dao động ở các vùng địa hình yên ngựa (Saddle Points) ra sao?
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế tích lũy vận tốc gradient từ quá khứ
    keypoint_weight: 0.5
    description: Momentum tính toán trung bình trượt lũy thừa của các gradient trước đó để tạo ra một véc-tơ vận tốc, mô phỏng một quả cầu lăn xuống dốc tích tụ động năng.
  - id: KP6_2
    content: Triệt tiêu dao động ngang và tăng tốc hướng đích
    keypoint_weight: 0.5
    description: Tại các vùng yên ngựa hoặc thung lũng dẹt, Momentum giúp triệt tiêu các dao động qua lại theo chiều ngang (vùng có gradient đổi chiều liên tục) và cộng dồn gia tốc theo chiều dọc để đẩy mô hình tiến nhanh về đích.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy phân biệt sự khác nhau về mặt cơ chế hoạt động kỹ thuật giữa hai phương pháp chuẩn hóa dữ liệu: Layer Normalization và Batch Normalization trong Deep Learning.
* **expected_key_points:**
  - id: KP7_1
    content: Cơ chế tính toán theo chiều Batch (Batch Normalization)
    keypoint_weight: 0.5
    description: Batch Normalization tính toán Mean và Variance dựa trên toàn bộ các mẫu dữ liệu trong một mini-batch cho từng thuộc tính/kênh độc lập. Phương pháp này phụ thuộc vào kích thước Batch Size.
  - id: KP7_2
    content: Cơ chế tính toán theo chiều thuộc tính (Layer Normalization)
    keypoint_weight: 0.5
    description: Layer Normalization tính toán Mean và Variance dựa trên tất cả các thuộc tính/siêu tính năng của một mẫu duy nhất trong tầng đó. Phương pháp này hoàn toàn độc lập với Batch Size, rất phù hợp cho mạng RNN hoặc Transformer.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong kiến trúc Transformer, tại sao người ta bắt buộc phải sử dụng kỹ thuật Positional Encoding (Mã hóa vị trí)? Hãy giải thích cơ chế toán học của hàm hình sin/cosin được dùng cho kỹ thuật này.
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất bất biến tuần tự của cơ chế Self-Attention
    keypoint_weight: 0.4
    description: Phép toán Self-Attention xử lý tất cả các từ trong câu cùng một lúc một cách song song, không có cấu trúc tuần tự thời gian như RNN, khiến mô hình coi câu như một tập hợp từ không thứ tự (Bag-of-words). Do đó cần Positional Encoding để nhúng thông tin thứ tự từ.
  - id: KP8_2
    content: Cơ chế hàm sóng Sin và Cosin đa tần số
    keypoint_weight: 0.4
    description: Sử dụng các hàm sóng sin và cosin với tần số khác nhau trên các chiều kích thước của vector nhúng: $PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d_{model}}}\right)$ và $PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d_{model}}}\right)$.
  - id: KP8_3
    content: Khả năng mở rộng chiều dài chuỗi và khoảng cách tương đối
    keypoint_weight: 0.2
    description: Hàm lượng giác cho phép mô hình dễ dàng học và biểu diễn mối quan hệ khoảng cách tương đối giữa các từ (vì $PE_{pos+k}$ có thể biểu diễn dưới dạng biến đổi tuyến tính của $PE_{pos}$), đồng thời cho phép mô hình mở rộng mượt mà với các câu có độ dài lớn hơn lúc train.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong huấn luyện mạng sinh GAN, hàm mất mát Earth Mover's Distance (EMD) trong kiến trúc Wasserstein GAN (WGAN) cải tiến điểm nghẽn gì của khoảng cách Jensen-Shannon (JS) trong Vanilla GAN?
* **expected_key_points:**
  - id: KP9_1
    content: Lỗi triệt tiêu Gradient của khoảng cách JS khi hai phân phối tách rời
    keypoint_weight: 0.4
    description: Trong Vanilla GAN, nếu phân phối của ảnh giả và ảnh thật hoàn toàn không chồng lấn lên nhau trong không gian hình học, khoảng cách JS sẽ trả về giá trị hằng số $\log 2$, dẫn đến đạo hàm gradient bằng 0 tuyệt đối, khiến Generator không thể học.
  - id: KP9_2
    content: Đồ thị khoảng cách liên tục mượt mà của Wasserstein Distance (EMD)
    keypoint_weight: 0.4
    description: EMD đo lượng công năng tối thiểu để biến đổi phân phối này thành phân phối kia. Khoảng cách này cung cấp một hàm đo lường liên tục có đạo hàm dốc mượt mà ở mọi nơi, cung cấp gradient chất lượng cho Generator học ngay cả khi hai phân phối nằm xa nhau.
  - id: KP9_3
    content: Cơ chế ép Lipschitz Continuity qua Gradient Penalty
    keypoint_weight: 0.2
    description: Để đảm bảo hàm tối ưu Wasserstein có nghĩa, mạng Critic phải thỏa mãn ràng buộc K-Lipschitz. Kỹ thuật WGAN-GP thực thi điều này bằng cách phạt trực tiếp vào hàm loss nếu độ lớn của gradient chuẩn (L2 norm) của Critic sai lệch khỏi giá trị 1.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích cơ chế toán học và sự đánh đổi tài nguyên của kỹ thuật nơ-ron bổ trợ LoRA (Low-Rank Adaptation) khi tinh chỉnh mô hình ngôn ngữ lớn (LLM). Tại sao nó không làm tăng độ trễ (Latency) lúc Inference?
* **expected_key_points:**
  - id: KP10_1
    content: Nguyên lý phân rã ma trận hạng thấp (Low-Rank Decomposition)
    keypoint_weight: 0.4
    description: LoRA đóng băng ma trận trọng số gốc $W_0 \in \mathbb{R}^{d \times k}$ và biểu diễn phần thay đổi trọng số $\Delta W$ bằng tích của hai ma trận hạng thấp $B \in \mathbb{R}^{d \times r}$ và $A \in \mathbb{R}^{r \times k}$ với tham số hạng $r \ll d$. Chỉ có $A$ và $B$ là được cập nhật trọng số.
  - id: KP10_2
    content: Tiết kiệm bộ nhớ VRAM và tài nguyên huấn luyện
    keypoint_weight: 0.4
    description: Giảm số lượng tham số cần lưu trữ trạng thái tối ưu (Optimizer States như Adam) đi hàng nghìn lần, giúp giảm thiểu đáng kể dung lượng bộ nhớ VRAM yêu cầu, cho phép huấn luyện mô hình lớn trên phần cứng GPU phổ thông.
  - id: KP10_3
    content: Cơ chế cộng gộp trọng số (Weight Merging) triệt tiêu Latency
    keypoint_weight: 0.2
    description: Tại thời điểm triển khai hệ thống (Deployment), ta có thể thực hiện phép toán cộng trực tiếp ma trận LoRA vào ma trận gốc: $W = W_0 + B \cdot A$. Trọng số được tích hợp thẳng vào kiến trúc cũ, giúp mô hình chạy Inference với cấu trúc gốc mà không tốn thêm bất kỳ chi phí tính toán nhánh song song nào.