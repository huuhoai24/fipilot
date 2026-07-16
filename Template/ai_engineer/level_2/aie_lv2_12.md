# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 2) - Tập Đề Quantization và Model Deployment (12)

* **Role:** AI Engineer
* **Level:** Level 2
* **Experience:** 1 - 3  năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Cắt tỉa mô hình (Model Pruning) là gì? Hãy nêu lợi ích và thách thức khi triển khai mô hình đã qua cắt tỉa lên phần cứng suy luận thực tế.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa và lợi ích của Pruning
    keypoint_weight: 0.5
    description: Là kỹ thuật loại bỏ bớt các trọng số/kết nối không quan trọng (gần 0) để giảm dung lượng file mô hình và tăng tốc độ tính toán.
  - id: KP1_2
    content: Thách thức khi deploy thực tế
    keypoint_weight: 0.5
    description: Cắt tỉa không cấu trúc (unstructured pruning) tạo ra các ma trận thưa. Hầu hết GPU thông thường không tối ưu được phép toán nhân ma trận thưa, nên thực tế không tăng được tốc độ suy luận trừ khi sử dụng phần cứng chuyên biệt hoặc cắt tỉa có cấu trúc (structured pruning).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh sự khác nhau về mục đích sử dụng và kiến trúc giữa Triton Inference Server và các framework web thông thường như Flask/FastAPI khi xây dựng dịch vụ phục vụ mô hình AI (Model Serving).
* **expected_key_points:**
  - id: KP2_1
    content: Hạn chế của Flask/FastAPI cho Model Serving
    keypoint_weight: 0.5
    description: Flask/FastAPI thiết kế cho web thông thường, không hỗ trợ tối ưu hóa GPU, thiếu các cơ chế gom lô động (dynamic batching) và quản lý hàng đợi suy luận hiệu quả dưới tải cao.
  - id: KP2_2
    content: Ưu thế của Triton Inference Server
    keypoint_weight: 0.5
    description: Triton là máy chủ suy luận chuyên dụng, hỗ trợ chạy song song nhiều mô hình (model concurrency), tự động gom lô động (dynamic batching), quản lý tối ưu VRAM GPU, hỗ trợ giao thức gRPC/HTTP và đa dạng backend (TensorRT, ONNX, PyTorch).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt hiện tượng lệch dữ liệu Data Drift và Concept Drift trong quá trình vận hành mô hình AI thực tế. Cho ví dụ minh họa từng loại.
* **expected_key_points:**
  - id: KP3_1
    content: Đặc trưng và ví dụ Data Drift
    keypoint_weight: 0.5
    description: Xảy ra khi phân phối của dữ liệu đầu vào $P(X)$ thay đổi theo thời gian nhưng mối quan hệ với nhãn không đổi. Ví dụ: Khách hàng sử dụng app chuyển tiền từ giới trẻ sang người lớn tuổi (phân phối tuổi đầu vào thay đổi).
  - id: KP3_2
    content: Đặc trưng và ví dụ Concept Drift
    keypoint_weight: 0.5
    description: Xảy ra khi mối quan hệ giữa đặc trưng đầu vào và nhãn thực tế $P(Y|X)$ thay đổi. Ví dụ: Hành vi quỵt nợ thay đổi sau khi có luật tài chính mới, khiến các tiêu chí chấm điểm tín dụng trước đây không còn chính xác.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích kỹ thuật Lượng tử hóa mô hình (Model Quantization) từ FP32 sang INT8. Phân biệt sự khác nhau giữa Lượng tử hóa đối xứng (Symmetric Quantization) và không đối xứng (Asymmetric Quantization).
* **expected_key_points:**
  - id: KP4_1
    content: Nguyên lý lượng tử hóa FP32 sang INT8
    keypoint_weight: 0.5
    description: Ánh xạ dải giá trị số thực FP32 sang dải số nguyên INT8 ([-128, 127] hoặc [0, 255]) sử dụng một hệ số tỷ lệ (scale factor $S$) và điểm không (zero-point $Z$): $q = \text{clip}(\text{round}(x/S) + Z)$.
  - id: KP4_2
    content: Symmetric vs Asymmetric Quantization
    keypoint_weight: 0.5
    description: Lượng tử hóa đối xứng ánh xạ điểm 0 của số thực trùng đúng với điểm 0 của số nguyên (zero-point $Z = 0$, dải giá trị đối xứng qua 0). Lượng tử hóa không đối xứng cho phép dịch chuyển điểm không ($Z \neq 0$), tối ưu hơn khi dải giá trị số thực bị lệch nhiều về một phía (như sau hàm kích hoạt ReLU).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh các định dạng mô hình phổ biến khi deploy: ONNX, TensorRT, và PyTorch JIT (TorchScript). Trong trường hợp nào bạn sẽ chọn ONNX làm định dạng trung gian?
* **expected_key_points:**
  - id: KP5_1
    content: Đặc trưng từng định dạng
    keypoint_weight: 0.6
    description: ONNX là định dạng mở trung lập giữa các framework. TensorRT tối ưu hóa riêng biệt cho phần cứng GPU NVIDIA để đạt hiệu năng cực đại. TorchScript cho phép chạy mô hình PyTorch trong môi trường C++ không cần Python runtime.
  - id: KP5_2
    content: Khi nào chọn ONNX làm trung gian
    keypoint_weight: 0.4
    description: Chọn ONNX khi cần chuyển mô hình từ framework này sang framework khác (ví dụ PyTorch sang TensorFlow/TensorRT), hoặc khi deploy trên các phần cứng không phải NVIDIA (như CPU Intel qua OpenVINO, thiết bị Edge di động).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế một pipeline tự động kiểm định chất lượng mô hình (Model Validation) trước khi chính thức deploy lên môi trường Production.
* **expected_key_points:**
  - id: KP6_1
    content: Các bài kiểm tra chất lượng kỹ thuật
    keypoint_weight: 0.5
    description: Kiểm tra hiệu năng độ chính xác trên tập test ẩn (Golden Dataset); chạy bài test khả năng chịu tải (Load test) để đo thời gian phản hồi (latency) và lượng tài nguyên RAM/VRAM tiêu thụ.
  - id: KP6_2
    content: Bài kiểm tra chức năng hệ thống
    keypoint_weight: 0.5
    description: Kiểm tra tính tương thích ngược của API (schema validation), chạy các ca kiểm thử biên (boundary/extreme inputs) và kiểm tra lỗi logic hệ thống để đảm bảo mô hình không crash.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Làm thế nào để xử lý bài toán mất cân bằng dữ liệu nghiêm trọng bằng cách kết hợp tham số class_weight và Focal Loss? Viết công thức toán học của Focal Loss và giải thích ý nghĩa các tham số.
* **expected_key_points:**
  - id: KP7_1
    content: Kết hợp class_weight và loss
    keypoint_weight: 0.4
    description: Sử dụng class_weight phạt nặng hơn sai số ở lớp thiểu số. Dùng Focal Loss tự động điều chỉnh trọng số dựa trên độ khó của mẫu dữ liệu.
  - id: KP7_2
    content: Công thức và ý nghĩa Focal Loss
    keypoint_weight: 0.6
    description: Công thức: $FL(p_t) = -\alpha_t (1 - p_t)^\gamma \log(p_t)$. Tham số $\alpha$ kiểm soát sự mất cân bằng giữa các lớp. Tham số $\gamma$ (focusing parameter) điều chỉnh tốc độ giảm trọng số của các mẫu dễ phân loại, bắt mô hình tập trung học các mẫu khó phân loại.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống phục vụ suy luận LLM lớn sử dụng framework vLLM. Giải thích cách vLLM giải quyết vấn đề phân mảnh bộ nhớ KV Cache bằng thuật toán PagedAttention.
* **expected_key_points:**
  - id: KP8_1
    content: Vấn đề phân mảnh bộ nhớ KV Cache
    keypoint_weight: 0.4
    description: Trong sinh chữ tự hồi quy, KV Cache lưu trữ các key/value vectors của các tokens trước đó. Bộ nhớ này tăng dần và có độ dài động. Việc cấp phát bộ nhớ liên tục gây ra phân mảnh bộ nhớ vật lý nghiêm trọng và lãng phí VRAM.
  - id: KP8_2
    content: Giải pháp PagedAttention của vLLM
    keypoint_weight: 0.6
    description: PagedAttention chia bộ nhớ KV Cache thành các trang (pages) vật lý không liên tục tương tự như phân trang bộ nhớ của hệ điều hành. Sử dụng một bảng trang (page table) để ánh xạ các vị trí ảo của tokens vào các trang vật lý trên VRAM, cho phép chia sẻ KV Cache giữa các luồng (ví dụ khi sinh đa luồng cho cùng một prompt), giúp tăng batch size lên gấp nhiều lần.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp deploy một mô hình học sâu phát hiện sự cố giao thông thời gian thực từ camera đường phố lên thiết bị nhúng NVIDIA Jetson Nano. Hãy thiết kế tối ưu hóa phần cứng và phần mềm.
* **expected_key_points:**
  - id: KP9_1
    content: Tối ưu hóa mô hình và pipeline dữ liệu
    keypoint_weight: 0.5
    description: Sử dụng mô hình Object Detection nhẹ (như YOLOv8-nano) lượng tử hóa sang INT8. Xây dựng pipeline xử lý camera bằng GStreamer kết hợp DeepStream SDK để giải mã video bằng phần cứng (NVDEC) trực tiếp trên GPU mà không đi qua CPU.
  - id: KP9_2
    content: Tối ưu hóa tài nguyên phần cứng Jetson
    keypoint_weight: 0.5
    description: Thiết lập cấu hình swap memory, tắt giao diện đồ họa (GUI) của hệ điều hành để tiết kiệm RAM, cấu hình quạt tản nhiệt chạy công suất tối đa và thiết lập chế độ năng lượng cao nhất (nvpmodel -m 0).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống Học liên hợp (Federated Learning) để huấn luyện mô hình gõ phím thông minh trên hàng triệu thiết bị di động của người dùng mà vẫn đảm bảo tính bảo mật và riêng tư dữ liệu tuyệt đối.
* **expected_key_points:**
  - id: KP10_1
    content: Quy trình huấn luyện cục bộ (Client-side Training)
    keypoint_weight: 0.5
    description: Điện thoại tải mô hình gốc về -> Tự động train cục bộ trên thiết bị bằng dữ liệu gõ phím thực tế khi điện thoại ở trạng thái rảnh rỗi (đang sạc, có Wifi) -> Chỉ gửi cập nhật trọng số (gradients/weights) về máy chủ.
  - id: KP10_2
    content: Cơ chế gộp và bảo mật (Server-side Aggregation)
    keypoint_weight: 0.5
    description: Server sử dụng thuật toán FedAvg để gộp các trọng số cập nhật từ hàng ngàn thiết bị; áp dụng cơ chế Secure Aggregation (mã hóa đa bên) để server không thể đọc được trọng số của từng thiết bị riêng lẻ, và thêm nhiễu Differential Privacy để chống tấn công dịch ngược dữ liệu.

