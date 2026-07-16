# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 2) - Tập Đề Diffusion Models và Vision Transformers (8)

* **Role:** AI Engineer
* **Level:** Level 2
* **Experience:** 1 - 3  năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Mô hình GAN (Generative Adversarial Network) là gì? Giải thích vai trò của Generator và Discriminator trong quá trình huấn luyện.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa GAN và hai thành phần
    keypoint_weight: 0.6
    description: Là kiến trúc học sâu gồm 2 mạng nơ-ron đối kháng nhau. Generator (Mạng sinh) cố gắng tạo ra ảnh giả giống ảnh thật từ vector nhiễu ngẫu nhiên. Discriminator (Mạng phân biệt) cố gắng phân biệt giữa ảnh thật lấy từ tập dữ liệu và ảnh giả do Generator sinh ra.
  - id: KP1_2
    content: Trò chơi minimax
    keypoint_weight: 0.4
    description: Huấn luyện song song theo cơ chế đối kháng (minimax game): Generator cố gắng tối đa hóa tỷ lệ lỗi của Discriminator, còn Discriminator cố gắng tối thiểu hóa tỷ lệ lỗi của chính mình.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Lớp Pooling trong mạng CNN là gì? Phân biệt Max Pooling và Average Pooling. Tại sao pooling giúp giảm tính toán?
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm và các loại Pooling
    keypoint_weight: 0.6
    description: Pooling là lớp lấy mẫu giảm chiều không gian của ma trận đặc trưng. Max Pooling giữ lại giá trị lớn nhất trong cửa sổ trượt (lấy đặc trưng nổi bật nhất). Average Pooling tính giá trị trung bình trong cửa sổ (lấy thông tin tổng quát).
  - id: KP2_2
    content: Lý do giảm tính toán
    keypoint_weight: 0.4
    description: Giảm kích thước không gian (width, height) của tensor đặc trưng, dẫn đến giảm số lượng tham số cần tính toán ở các lớp Fully Connected tiếp theo và giảm overfitting.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt hai phương pháp tối ưu siêu tham số: Grid Search và Random Search. Khi nào nên ưu tiên chọn Random Search?
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế Grid Search vs Random Search
    keypoint_weight: 0.5
    description: Grid Search thử nghiệm tất cả các tổ hợp siêu tham số được định nghĩa sẵn trong lưới (tốn thời gian). Random Search lựa chọn ngẫu nhiên các tổ hợp siêu tham số từ phân phối xác định.
  - id: KP3_2
    content: Ưu thế của Random Search
    keypoint_weight: 0.5
    description: Random Search hiệu quả hơn khi không gian tìm kiếm lớn và khi một số siêu tham số quan trọng hơn nhiều so với các siêu tham số khác (nó không bị lặp lại thử nghiệm trên các trục siêu tham số không quan trọng).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế hoạt động của mô hình khuếch tán (Diffusion Models - ví dụ Stable Diffusion) trong việc sinh hình ảnh chất lượng cao từ văn bản.
* **expected_key_points:**
  - id: KP4_1
    content: Quá trình Forward và Reverse Diffusion
    keypoint_weight: 0.6
    description: Forward process thêm nhiễu Gauss tuần tự vào ảnh thật cho đến khi biến thành nhiễu hoàn toàn. Reverse process huấn luyện một mạng nơ-ron (thường là U-Net) học cách loại bỏ nhiễu từng bước một để khôi phục lại ảnh sạch ban đầu.
  - id: KP4_2
    content: Cơ chế Latent Diffusion và Text Conditioning
    keypoint_weight: 0.4
    description: Stable Diffusion thực hiện quá trình khuếch tán trong không gian ẩn (latent space) của Autoencoder để giảm chi phí tính toán; sử dụng cơ chế Cross-Attention nhận vector text embedding từ CLIP để định hướng quá trình khử nhiễu theo prompt văn bản.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích kiến trúc Vision Transformer (ViT). Làm thế nào để đưa dữ liệu hình ảnh 2D vào đầu vào của một mạng Transformer vốn thiết kế cho dữ liệu chuỗi 1D?
* **expected_key_points:**
  - id: KP5_1
    content: Chia ảnh thành các Patches và chiếu tuyến tính (Linear Projection)
    keypoint_weight: 0.6
    description: Ảnh 2D kích thước $H 	imes W 	imes C$ được chia nhỏ thành một chuỗi các ô ảnh (patches) kích thước $P 	imes P$. Mỗi patch được trải phẳng (flatten) thành vector và đi qua một lớp Linear Projection để có kích thước vector embedding $D$ giống như tokens văn bản.
  - id: KP5_2
    content: Thêm CLS token và Position Embedding
    keypoint_weight: 0.4
    description: Thêm một token học được đặc biệt [class] (CLS token) vào đầu chuỗi patches; cộng thêm Position Embedding 1D học được vào chuỗi vectors để giữ thông tin vị trí không gian trước khi đưa vào Transformer Encoder.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh hai thuật toán tối ưu hóa Adam và AdamW. Tại sao AdamW được khuyến nghị sử dụng nhiều hơn Adam khi huấn luyện các mô hình lớn?
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế của Weight Decay trong Adam vs AdamW
    keypoint_weight: 0.6
    description: Trong Adam thông thường với L2 regularization, trọng số phạt L2 được cộng trực tiếp vào loss function, dẫn đến việc weight decay bị thay đổi bởi trung bình động của gradient (làm sai lệch hệ số decay). AdamW thực hiện tách biệt (decouple) weight decay bằng cách trừ trực tiếp một tỷ lệ trọng số hiện tại sau khi đã cập nhật gradient thích ứng.
  - id: KP6_2
    content: Hiệu quả thực tế
    keypoint_weight: 0.4
    description: AdamW giúp cải thiện khả năng tổng quát hóa của mô hình, giúp hội tụ ổn định hơn trên các mô hình lớn như Transformer có nhiều regularization.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy giải thích chỉ số đánh giá hệ thống tìm kiếm/xếp hạng NDCG (Normalized Discounted Cumulative Gain). Cách tính và ý nghĩa của nó.
* **expected_key_points:**
  - id: KP7_1
    content: Cách tính CG và DCG
    keypoint_weight: 0.6
    description: CG (Cumulative Gain) là tổng điểm độ liên quan của các kết quả tìm kiếm được đề xuất. DCG (Discounted CG) áp dụng hàm phạt logarit trên vị trí kết quả để ưu tiên các kết quả liên quan cao xuất hiện ở đầu trang tìm kiếm: $DCG = \sum \frac{rel_i}{\log_2(i+1)}$.
  - id: KP7_2
    content: Chuẩn hóa sang NDCG
    keypoint_weight: 0.4
    description: NDCG được tính bằng cách chia DCG thực tế cho IDCG (Ideal DCG - giá trị DCG tốt nhất có thể đạt được nếu xếp hạng hoàn hảo). NDCG có giá trị từ 0 đến 1, giúp so sánh hiệu quả xếp hạng giữa các truy vấn khác nhau.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong quá trình huấn luyện mô hình GAN lớn, hiện tượng Mode Collapse là gì? Hãy giải thích nguyên nhân và đề xuất ít nhất 2 phương pháp kỹ thuật để khắc phục.
* **expected_key_points:**
  - id: KP8_1
    content: Khái niệm và nguyên nhân Mode Collapse
    keypoint_weight: 0.5
    description: Xảy ra khi Generator chỉ tìm ra và sinh đi sinh lại một số lượng nhỏ các mẫu ảnh rất giống nhau (modes) mà Discriminator dễ tin là thật, thay vì học được toàn bộ phân phối dữ liệu đa dạng. Nguyên nhân do mất cân bằng tốc độ học giữa Generator và Discriminator.
  - id: KP8_2
    content: Các giải pháp kỹ thuật khắc phục
    keypoint_weight: 0.5
    description: Nêu được ít nhất 2 giải pháp: Sử dụng Wasserstein GAN (WGAN-GP) thay thế loss thông thường bằng earth mover's distance; áp dụng kỹ thuật Unrolled GANs; sử dụng nhiều Discriminators song song; hoặc thêm historical checkpoints.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống kiểm duyệt nội dung tự động (Content Moderation System) có khả năng lọc văn bản, hình ảnh, video độc hại (bạo lực, nhạy cảm) theo thời gian thực cho một mạng xã hội lớn.
* **expected_key_points:**
  - id: KP9_1
    content: Xử lý đa phương thức (Multimodal Moderation Pipeline)
    keypoint_weight: 0.5
    description: Thiết kế pipeline gồm 3 nhánh: Nhánh Text (mô hình BERT/LLM nhẹ phân loại nội dung), Nhánh Image (CNN/ViT phân loại ảnh nhạy cảm), Nhánh Video (trích xuất khung hình chính keyframes và dùng mô hình 3D-CNN hoặc CLIP để phân loại nhanh).
  - id: KP10_1
    content: Kiến trúc đáp ứng High Throughput và Low Latency
    keypoint_weight: 0.5
    description: Sử dụng mô hình nhỏ nhanh ở Layer 1 để lọc >90% nội dung an toàn rõ ràng (độ trễ < 10ms); các nội dung nghi ngờ chuyển lên Layer 2 dùng mô hình Multimodal nặng hơn; lưu cache kết quả băm ảnh (Perceptual Hashing) để phát hiện ảnh độc hại đã biết mà không cần chạy mô hình lại.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp phân loại văn bản đa nhãn (Multi-label Text Classification) với hàng ngàn nhãn phân cấp phức tạp (Hierarchical Multi-label Classification).
* **expected_key_points:**
  - id: KP10_2
    content: Xử lý phân cấp nhãn (Hierarchical Architecture)
    keypoint_weight: 0.5
    description: Thiết kế kiến trúc mô hình mạng nơ-ron phân cấp (ví dụ: huấn luyện các bộ phân loại độc lập ở mỗi nút cha trên cây phân cấp, hoặc sử dụng Graph CNN tích hợp cấu trúc quan hệ giữa các nhãn vào mô hình sinh embedding).
  - id: KP10_3
    content: Loss Function và giải quyết bài toán nhãn thưa
    keypoint_weight: 0.5
    description: Sử dụng Asymmetric Loss (ASL) hoặc Binary Cross-Entropy có trọng số để giải quyết tình trạng mất cân bằng nhãn nghiêm trọng (mỗi văn bản chỉ có vài nhãn trên tổng số hàng ngàn nhãn); áp dụng kỹ thuật thresholding động cho từng lớp nhãn thay vì dùng một ngưỡng cố định 0.5.

