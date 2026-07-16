# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 3) - Tập Đề DeepSORT và Object Tracking (6)

* **Role:** AI Engineer
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt cơ chế học tương phản (Contrastive Learning) và mô hình tạo sinh (Generative Models). Nêu ví dụ tiêu biểu cho từng nhóm.
* **expected_key_points:**
  - id: KP1_1
    content: Bản chất Contrastive vs Generative
    keypoint_weight: 0.6
    description: Contrastive Learning học cách so sánh kéo gần cặp tương đồng và đẩy xa cặp khác biệt (như CLIP). Generative Models học phân phối dữ liệu gốc để sinh ra mẫu ảnh mới (như GAN, Diffusion).
  - id: KP1_2
    content: Ví dụ cụ thể
    keypoint_weight: 0.4
    description: Contrastive: CLIP, SimCLR. Generative: Stable Diffusion, StyleGAN, VAE.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt vai trò của lớp Max Pooling và Average Pooling trong mạng CNN. Tại sao pooling giúp giảm tính toán và tránh overfitting?
* **expected_key_points:**
  - id: KP2_1
    content: Max Pooling vs Average Pooling
    keypoint_weight: 0.5
    description: Max Pooling lấy giá trị lớn nhất trong cửa sổ trượt (trích xuất đặc trưng nổi bật nhất). Average Pooling lấy trung bình cộng (giữ thông tin nền mượt mà).
  - id: KP2_2
    content: Lý do giảm tính toán và overfitting
    keypoint_weight: 0.5
    description: Giảm kích thước không gian (spatial dimension) của ma trận đặc trưng, dẫn đến giảm số lượng tham số cần học ở các lớp fully connected tiếp theo.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích cơ chế hoạt động của 3 kỹ thuật tăng cường dữ liệu hình ảnh nâng cao: Mixup, CutMix, và Mosaic.
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế Mixup và CutMix
    keypoint_weight: 0.6
    description: Mixup hòa trộn tuyến tính hai ảnh và nhãn ngẫu nhiên theo tỷ lệ lambda. CutMix cắt một vùng ảnh A đè lên ảnh B và trộn nhãn tương ứng.
  - id: KP3_2
    content: Cơ chế Mosaic
    keypoint_weight: 0.4
    description: Mosaic ghép 4 ảnh huấn luyện khác nhau thành 1 ảnh duy nhất, giúp mô hình phát hiện cực tốt đối tượng nhỏ và cải thiện batch normalization.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích nguyên lý hoạt động của thuật toán theo dõi đối tượng đa mục tiêu DeepSORT. Hãy nêu vai trò của bộ lọc Kalman Filter và thuật toán Hungarian Algorithm trong quy trình này.
* **expected_key_points:**
  - id: KP4_1
    content: Vai trò của Kalman Filter (Dự đoán trạng thái)
    keypoint_weight: 0.5
    description: Dùng để dự đoán vị trí (bounding box) tiếp theo của đối tượng ở frame tiếp theo dựa trên vận tốc và quỹ đạo di chuyển lịch sử.
  - id: KP4_2
    content: Hungarian Algorithm và Deep Feature Association (So khớp)
    keypoint_weight: 0.5
    description: Hungarian Algorithm giải bài toán phân bổ tối ưu để so khớp giữa các bounding box thực tế phát hiện được và các vị trí dự đoán từ Kalman Filter. DeepSORT bổ sung đặc trưng vector (deep embeddings) trích xuất từ CNN để so khớp các đối tượng có ngoại hình giống nhau khi bị che khuất.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh hai kiến trúc Object Detection: YOLOv8 (Single-stage) và Faster R-CNN (Two-stage) về mặt tốc độ, độ chính xác và ứng dụng thực tế.
* **expected_key_points:**
  - id: KP5_1
    content: Kiến trúc Two-stage của Faster R-CNN
    keypoint_weight: 0.5
    description: Giai đoạn 1 đề xuất vùng chứa đối tượng (RPN), Giai đoạn 2 phân loại và tinh chỉnh box. Độ chính xác cao, đặc biệt với ảnh phức tạp, nhưng chạy chậm, khó đạt thời gian thực.
  - id: KP5_2
    content: Kiến trúc Single-stage của YOLOv8
    keypoint_weight: 0.5
    description: Dự đoán trực tiếp bounding box và class chỉ qua 1 lần forward pass. Tốc độ cực nhanh (thời gian thực >30 FPS), độ chính xác hiện nay tiệm cận các mô hình hai giai đoạn.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cơ chế hoạt động của mạng đối kháng tạo sinh GAN ứng dụng trong bài toán Tăng siêu phân giải hình ảnh (Super Resolution - ví dụ SRGAN).
* **expected_key_points:**
  - id: KP6_1
    content: Vai trò của Generator trong SRGAN
    keypoint_weight: 0.5
    description: Generator nhận đầu vào là ảnh chất lượng thấp (Low Resolution) và cố gắng sinh ra ảnh chi tiết chất lượng cao (High Resolution) trông tự nhiên nhất.
  - id: KP6_2
    content: Perceptual Loss và Discriminator
    keypoint_weight: 0.5
    description: Discriminator phân biệt ảnh do Generator sinh ra với ảnh chụp gốc sắc nét. Thay vì chỉ dùng loss pixel-level (MSE) làm ảnh bị mờ, SRGAN kết hợp Perceptual Loss (so sánh đặc trưng trích xuất từ mạng VGG) để giữ nguyên các chi tiết vân bề mặt sắc nét.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách tính và ý nghĩa của các chỉ số đánh giá mô hình Object Detection: IoU (Intersection over Union), mAP@0.5, và mAP@0.5:0.95.
* **expected_key_points:**
  - id: KP7_1
    content: Cách tính IoU
    keypoint_weight: 0.4
    description: IoU = Diện tích phần giao nhau / Diện tích phần hợp nhau của bounding box dự đoán và ground truth. Dùng làm ngưỡng để xác định một dự đoán là True Positive hay False Positive.
  - id: KP7_2
    content: Ý nghĩa mAP@0.5 và mAP@0.5:0.95
    keypoint_weight: 0.6
    description: mAP (mean Average Precision) tính trung bình độ chính xác trên tất cả các lớp. `@0.5` nghĩa là tính mAP khi đặt ngưỡng IoU cố định là 0.5. `@0.5:0.95` tính trung bình của các mAP tại các ngưỡng IoU chạy từ 0.5 đến 0.95 với bước nhảy 0.05 (đánh giá khả năng định vị hộp giới hạn khắt khe hơn).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống camera giám sát an ninh tự động phát hiện hành vi trộm cắp tại siêu thị thời gian thực sử dụng các kỹ thuật nhận diện hành động (Action Recognition) từ luồng video.
* **expected_key_points:**
  - id: KP8_1
    content: Pipeline xử lý video và trích xuất Pose/Spatio-Temporal Features
    keypoint_weight: 0.5
    description: Dùng mô hình Object Detection + Tracking để cắt riêng vùng ảnh của từng khách hàng -> Sử dụng mạng 3D-CNN (như I3D) hoặc kiến trúc SlowFast để trích xuất đặc trưng không-thời gian từ chuỗi khung hình liên tiếp; hoặc dùng mô hình ước lượng khung xương (Pose Estimation) trích xuất tọa độ khớp xương theo thời gian.
  - id: KP8_2
    content: Phân loại hành vi và cảnh báo
    keypoint_weight: 0.5
    description: Huấn luyện bộ phân loại (như LSTM hoặc Graph Convolutional Networks trên khớp xương ST-GCN) phân tích chuỗi chuyển động để nhận diện hành vi giấu đồ vào túi. Thiết lập ngưỡng tin cậy cao và kết nối hệ thống thông báo gửi cảnh báo về máy nhân viên kèm video bằng chứng.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp sinh hình ảnh sản phẩm quảng cáo tự động chất lượng cao dựa trên Stable Diffusion và ControlNet, đảm bảo giữ nguyên hình dạng và các chi tiết đặc trưng của sản phẩm gốc.
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế hoạt động của ControlNet trong sinh ảnh
    keypoint_weight: 0.5
    description: ControlNet đóng băng trọng số của Stable Diffusion và sao chép cấu trúc để huấn luyện riêng một nhánh điều khiển đầu vào bổ sung (như bản đồ nét biên Canny, bản đồ chiều sâu Depth Map, hoặc ảnh phân đoạn Segmentation) giúp ép mô hình sinh ảnh tuân thủ đúng bố cục sản phẩm gốc.
  - id: KP9_2
    content: Pipeline giữ chi tiết sản phẩm (Product Preserving Pipeline)
    keypoint_weight: 0.5
    description: Tách sản phẩm gốc ra khỏi nền -> Dùng ControlNet (nhập Canny/Depth map của sản phẩm) định hình bố cục -> Viết prompt mô tả bối cảnh xung quanh -> Sử dụng kỹ thuật Inpainting (chỉ vẽ lại vùng nền, khóa vùng sản phẩm gốc) kết hợp Blending để tạo bóng đổ tự nhiên.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp phân đoạn tự động các vùng tổn thương (ví dụ khối u) trên ảnh siêu âm chất lượng thấp, nhiều nhiễu, sử dụng mô hình Segment Anything Model (SAM) fine-tune.
* **expected_key_points:**
  - id: KP10_1
    content: Fine-tuning SAM trên dữ liệu y tế chuyên biệt
    keypoint_weight: 0.5
    description: Đóng băng Image Encoder (nặng) của SAM. Chỉ thực hiện fine-tune Prompt Encoder và Mask Decoder sử dụng tập dữ liệu ảnh siêu âm có gán nhãn khối u. Áp dụng LoRA lên các lớp attention của Mask Decoder để giảm overfitting.
  - id: KP10_2
    content: Xử lý prompt đầu vào khi chạy suy luận
    keypoint_weight: 0.5
    description: Thiết kế cơ chế sinh prompt tự động (bằng cách lấy bounding box từ một mô hình Object Detection phụ phát hiện khối u trước đó) gửi làm đầu vào cho SAM để thực hiện phân đoạn tự động không cần con người tương tác click chuột.

