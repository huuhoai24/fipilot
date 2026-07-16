# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 2) - Tập Đề Computer Vision và Vector DB (4)

* **Role:** AI Engineer
* **Level:** Level 2
* **Experience:** 1 - 3  năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Hiện tượng Overfitting là gì? Hãy nêu 3 kỹ thuật giảm thiểu Overfitting phổ biến khi huấn luyện mô hình Deep Learning.
* **expected_key_points:**
  - id: KP1_1
    content: Bản chất hiện tượng Overfitting
    keypoint_weight: 0.4
    description: Là hiện tượng mô hình học quá tốt các đặc trưng của tập train bao gồm cả nhiễu, dẫn đến việc mất khả năng tổng quát hóa trên dữ liệu mới (đầu ra tập validation tệ).
  - id: KP1_2
    content: Kỹ thuật giảm thiểu Overfitting
    keypoint_weight: 0.6
    description: Nêu được ít nhất 3 kỹ thuật: Dropout (tắt nơ-ron ngẫu nhiên), Data Augmentation (tăng cường dữ liệu), Early Stopping (dừng sớm), Weight Decay (L2 regularization), hoặc Batch Normalization.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh sự khác nhau giữa hai bài toán Object Detection (Phát hiện đối tượng) và Semantic Segmentation (Phân đoạn ngữ nghĩa) trong Computer Vision.
* **expected_key_points:**
  - id: KP2_1
    content: Đầu ra của Object Detection
    keypoint_weight: 0.5
    description: Xác định nhãn đối tượng và vị trí của chúng thông qua các hộp giới hạn (Bounding Boxes) hình chữ nhật.
  - id: KP2_2
    content: Đầu ra của Semantic Segmentation
    keypoint_weight: 0.5
    description: Phân loại ở cấp độ pixel (pixel-level classification), tức là gắn mỗi pixel trong ảnh vào một nhãn lớp đối tượng cụ thể.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Vector Embedding là gì? Hãy trình bày cách tính và sự khác nhau giữa hai độ đo khoảng cách: Euclidean Distance (L2) và Cosine Similarity.
* **expected_key_points:**
  - id: KP3_1
    content: Khái niệm Vector Embedding
    keypoint_weight: 0.4
    description: Là phương pháp biểu diễn dữ liệu phi cấu trúc (văn bản, hình ảnh) dưới dạng các vector số thực mật độ cao trong không gian đa chiều, giữ được ngữ nghĩa liên quan.
  - id: KP3_2
    content: Khoảng cách Euclidean vs Cosine
    keypoint_weight: 0.6
    description: Euclidean đo khoảng cách đường thẳng trực tiếp giữa 2 điểm đầu mút vector. Cosine đo góc giữa 2 vector, không phụ thuộc vào độ dài (magnitude) của vector, thường dùng so khớp ngữ nghĩa.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích nguyên lý hoạt động của mô hình YOLO (You Only Look Once) trong bài toán Object Detection và vai trò của thuật toán Non-Maximum Suppression (NMS).
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế Single-shot của YOLO
    keypoint_weight: 0.5
    description: YOLO coi Object Detection là bài toán hồi quy duy nhất, chia ảnh thành lưới ô (grid cells). Mỗi ô dự đoán đồng thời các bounding boxes, độ tin cậy (confidence) và xác suất lớp (class probabilities) chỉ qua 1 lần forward pass.
  - id: KP4_2
    content: Vai trò của NMS (Non-Maximum Suppression)
    keypoint_weight: 0.5
    description: Loại bỏ các bounding boxes trùng lặp đè lên cùng một đối tượng bằng cách giữ lại box có confidence cao nhất và xóa các box xung quanh có độ giao nhau (IoU - Intersection over Union) lớn hơn ngưỡng quy định.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày nguyên lý hoạt động của Contrastive Learning so với Masked Language Modeling. Cho ví dụ cụ thể về ứng dụng của mô hình CLIP (Contrastive Language-Image Pre-training).
* **expected_key_points:**
  - id: KP5_1
    content: Contrastive Learning vs Masked Language Modeling
    keypoint_weight: 0.5
    description: Masked Language Modeling che từ và bắt mô hình đoán. Contrastive Learning huấn luyện mô hình bằng cách kéo biểu diễn vector của các cặp mẫu tương đồng (positive pairs) lại gần nhau và đẩy các cặp khác biệt (negative pairs) ra xa trong không gian embedding.
  - id: KP5_2
    content: Ứng dụng của mô hình CLIP
    keypoint_weight: 0.5
    description: CLIP được huấn luyện trên cặp ảnh-văn bản tương ứng, sử dụng Text Encoder và Image Encoder để tối ưu hóa độ tương đồng của cặp đúng, giúp mô hình hiểu được ngữ nghĩa chéo giữa văn bản và hình ảnh (ứng dụng Zero-shot Classification).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt sự khác nhau giữa kiến trúc mạng U-Net và Mask R-CNN trong bài toán Image Segmentation.
* **expected_key_points:**
  - id: KP6_1
    content: Đặc trưng kiến trúc U-Net
    keypoint_weight: 0.5
    description: U-Net dùng cho Semantic Segmentation (phân đoạn ngữ nghĩa chung). Thiết kế đối xứng Encoder-Decoder dạng chữ U kết hợp skip connections để truyền thông tin không gian trực tiếp, rất phổ biến trong y tế.
  - id: KP6_2
    content: Đặc trưng kiến trúc Mask R-CNN
    keypoint_weight: 0.5
    description: Mask R-CNN dùng cho Instance Segmentation (phân đoạn cá thể). Mở rộng từ Faster R-CNN bằng cách thêm một nhánh song song để dự đoán mặt nạ phân đoạn (binary mask) trên mỗi vùng đề xuất đối tượng (RoI).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Vector Database là gì? Giải thích cơ chế hoạt động của thuật toán tìm kiếm lân cận gần đúng ANN (Approximate Nearest Neighbors) như HNSW (Hierarchical Navigable Small World).
* **expected_key_points:**
  - id: KP7_1
    content: Vai trò của Vector Database
    keypoint_weight: 0.4
    description: Là cơ sở dữ liệu tối ưu hóa riêng cho việc lưu trữ, quản lý và truy vấn cực nhanh các vector embedding đa chiều.
  - id: KP7_2
    content: Cơ chế của thuật toán HNSW
    keypoint_weight: 0.6
    description: Xây dựng cấu trúc đồ thị nhiều tầng (hierarchical graph). Các tầng trên có liên kết thưa giúp tìm kiếm nhanh khoảng cách lớn (skip-list style), các tầng dưới có liên kết dày giúp tinh chỉnh kết quả cục bộ, giảm độ phức tạp tìm kiếm từ $O(N)$ xuống $O(\log N)$.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trình bày cách bạn tối ưu hóa một mô hình Computer Vision (như ResNet hoặc YOLO) bằng NVIDIA TensorRT để deploy suy luận thời gian thực lên thiết bị Edge NVIDIA Jetson.
* **expected_key_points:**
  - id: KP8_1
    content: Các cơ chế tối ưu của TensorRT
    keypoint_weight: 0.5
    description: Thực hiện Layer & Tensor Fusion (gộp các lớp dọc/ngang), Kernel Tuning (chọn thuật toán nhân ma trận tốt nhất cho GPU cụ thể), lượng tử hóa mô hình sang FP16/INT8, và tối ưu hóa Dynamic Memory để giảm VRAM.
  - id: KP8_2
    content: Quy trình chuyển đổi mô hình
    keypoint_weight: 0.5
    description: Xuất mô hình PyTorch sang định dạng ONNX -> Cấu hình TensorRT builder (thiết lập precision, calibration dataset cho INT8) -> Build Engine file tương thích trực tiếp với kiến trúc GPU của Jetson.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp xây dựng hệ thống OCR tự động đọc và trích xuất thông tin hóa đơn (Invoice Information Extraction) từ ảnh chụp điện thoại chênh góc và mờ.
* **expected_key_points:**
  - id: KP9_1
    content: Pipeline xử lý ảnh và trích xuất OCR
    keypoint_weight: 0.5
    description: Tiền xử lý ảnh (xoay, khử nhiễu, phối cảnh phẳng) -> Dùng mô hình Text Detection (như DBNet) xác định vùng chữ -> Dùng OCR Engine (như Tesseract, EasyOCR, hoặc PaddleOCR) đọc text thuần.
  - id: KP9_2
    content: Trích xuất thông tin ngữ nghĩa (Information Extraction)
    keypoint_weight: 0.5
    description: Sử dụng mô hình ngôn ngữ kết hợp thông tin không gian (như LayoutLM) để phân loại các thực thể key-value (tên cửa hàng, tổng tiền, ngày tháng) dựa trên cả đặc trưng chữ, tọa độ hộp giới hạn (bounding boxes) và ảnh.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống phát hiện bất thường (Anomaly Detection) cho thiết bị cảm biến IoT trong nhà máy công nghiệp sử dụng mô hình Auto-encoder.
* **expected_key_points:**
  - id: KP10_1
    content: Nguyên lý huấn luyện Auto-encoder phát hiện bất thường
    keypoint_weight: 0.5
    description: Huấn luyện Auto-encoder chỉ sử dụng dữ liệu chạy bình thường (normal data) để mạng học cách mã hóa (encode) và tái lập (decode/reconstruct) dữ liệu bình thường một cách hoàn hảo nhất.
  - id: KP10_2
    content: Xác định bất thường dựa trên Reconstruction Error
    keypoint_weight: 0.5
    description: Khi nhận dữ liệu bất thường (anomaly), Auto-encoder sẽ không thể tái lập tốt dẫn đến sai số tái lập (Reconstruction Error) rất cao. Đặt ngưỡng threshold trên sai số này để phân loại bất thường và gửi cảnh báo.

