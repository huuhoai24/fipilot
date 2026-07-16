# Bộ Câu Hỏi Phỏng Vấn AI Engineer (Level 2) - Tập Đề Bi-LSTM CRF và NLP (14)

* **Role:** AI Engineer
* **Level:** Level 2
* **Experience:** 1 - 3  năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Thế nào là bài toán Trích xuất thực thể liên kết (Named Entity Recognition - NER)? Hãy nêu 3 loại thực thể phổ biến nhất thường được trích xuất.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa bài toán NER
    keypoint_weight: 0.5
    description: Là bài toán con của NLP nhằm xác định và phân loại các từ hoặc cụm từ trong văn bản vào các nhóm thực thể đã định nghĩa trước.
  - id: KP1_2
    content: 3 thực thể phổ biến
    keypoint_weight: 0.5
    description: Nêu đúng ít nhất 3 thực thể: PERSON (Tên người), ORGANIZATION (Tên tổ chức), LOCATION/GPE (Địa điểm/Địa lý), hoặc DATE/TIME (Thời gian).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt kỹ thuật Tokenization ở cấp độ Từ (Word-level) và cấp độ Từ con (Subword-level). Tại sao các mô hình NLP hiện đại đều chọn Subword?
* **expected_key_points:**
  - id: KP2_1
    content: Word-level vs Subword-level Tokenization
    keypoint_weight: 0.5
    description: Word-level chia câu trực tiếp theo khoảng trắng hoặc từ điển từ ghép. Subword-level chia nhỏ từ thành các phần từ con quen thuộc (ví dụ 'unhappiness' thành ['un', 'happi', 'ness']).
  - id: KP2_2
    content: Lý do lựa chọn Subword
    keypoint_weight: 0.5
    description: Tránh lỗi Từ ngoài từ điển (OOV), kiểm soát kích thước từ điển của mô hình không bị quá lớn, và giúp mô hình hiểu được cấu trúc ngữ pháp từ các tiền tố/hậu tố.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy giải thích chỉ số TF-IDF (Term Frequency - Inverse Document Frequency). Nó đo lường điều gì và có ưu điểm gì so với Bag-of-Words thông thường?
* **expected_key_points:**
  - id: KP3_1
    content: Công thức và ý nghĩa TF-IDF
    keypoint_weight: 0.6
    description: TF-IDF = TF * IDF. TF đo tần suất xuất hiện của từ trong tài liệu. IDF giảm trọng số của các từ xuất hiện quá phổ biến ở mọi tài liệu (như 'and', 'the', 'thì', 'là').
  - id: KP3_2
    content: Ưu điểm so với Bag-of-Words
    keypoint_weight: 0.4
    description: Bag-of-Words chỉ đếm tần suất đơn thuần. TF-IDF làm nổi bật các từ mang tính đặc trưng, chứa nhiều thông tin đại diện cho nội dung của tài liệu đó hơn.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cấu trúc và nguyên lý hoạt động của kiến trúc lai Bi-LSTM kết hợp với lớp CRF (Conditional Random Fields) trong bài toán NER.
* **expected_key_points:**
  - id: KP4_1
    content: Vai trò của lớp Bi-LSTM
    keypoint_weight: 0.5
    description: Sử dụng mạng LSTM hai chiều để học đặc trưng ngữ cảnh của từng từ từ cả phía trước và phía sau câu, tạo ra vector embedding chất lượng cho mỗi token.
  - id: KP4_2
    content: Vai trò của lớp CRF
    keypoint_weight: 0.5
    description: CRF học các ràng buộc tuần tự giữa các nhãn (ví dụ nhãn I-PER bắt buộc phải đứng sau B-PER, không thể đứng sau B-LOC). CRF tính toán phân phối xác suất chung của toàn bộ chuỗi nhãn thay vì dự đoán độc lập từng từ.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** So sánh sự khác nhau giữa mô hình ngôn ngữ lớn LLaMA, Mistral và Qwen về cơ chế chú ý Grouped-Query Attention (GQA). GQA giải quyết vấn đề gì của Multi-Query Attention (MQA)?
* **expected_key_points:**
  - id: KP5_1
    content: Cơ chế hoạt động của GQA
    keypoint_weight: 0.5
    description: GQA chia các Query heads thành các nhóm (groups). Mỗi nhóm Query heads sẽ dùng chung một cặp Key và Value head duy nhất. GQA nằm giữa Multi-Head Attention (mỗi Q có một K, V) và Multi-Query Attention (tất cả Q dùng chung 1 K, V).
  - id: KP5_2
    content: Vấn đề GQA giải quyết
    keypoint_weight: 0.5
    description: MQA tiết kiệm dung lượng KV Cache lưu trên RAM nhưng làm giảm độ chính xác đáng kể. GQA đạt được sự cân bằng tối ưu: giảm mạnh dung lượng KV Cache lưu trữ (tăng tốc độ suy luận) mà không làm suy giảm độ chính xác của mô hình.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế Beam Search trong quá trình sinh chữ (Decoding) của LLM. So sánh ưu nhược điểm với Greedy Search.
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên lý hoạt động của Beam Search
    keypoint_weight: 0.5
    description: Tại mỗi bước sinh từ, thay vì chỉ chọn từ có xác suất cao nhất (Greedy Search), Beam Search duy trì $B$ chuỗi con có xác suất tích lũy cao nhất (gọi là beam width $B$).
  - id: KP6_2
    content: So sánh ưu nhược điểm với Greedy Search
    keypoint_weight: 0.5
    description: Greedy Search chạy nhanh nhất nhưng dễ rơi vào tối ưu cục bộ và sinh câu lặp lại. Beam Search cho kết quả câu mượt mà, chất lượng cao hơn nhưng tốn tài nguyên tính toán hơn (gấp $B$ lần).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách giải quyết bài toán Dịch máy (Machine Translation) sử dụng kiến trúc Seq2Seq kết hợp cơ chế Attention. Hãy mô tả chi tiết quá trình huấn luyện sử dụng kỹ thuật Teacher Forcing.
* **expected_key_points:**
  - id: KP7_1
    content: Kiến trúc Seq2Seq với Attention
    keypoint_weight: 0.5
    description: Encoder nhận câu gốc -> sinh hidden states. Attention tính trọng số tương quan giữa trạng thái của Decoder và tất cả hidden states của Encoder. Decoder sử dụng ngữ cảnh chú ý này để sinh câu dịch từng từ.
  - id: KP7_2
    content: Kỹ thuật Teacher Forcing
    keypoint_weight: 0.5
    description: Trong quá trình huấn luyện, thay vì sử dụng từ dự đoán của Decoder ở bước $t-1$ làm đầu vào cho bước $t$ (có thể sai dây chuyền), ta đưa trực tiếp từ mục tiêu thực tế (ground truth) làm đầu vào cho bước $t$. Giúp mô hình hội tụ nhanh hơn.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống trích xuất thông tin bệnh án y khoa tiếng Việt phi cấu trúc (như triệu chứng, chẩn đoán, thuốc điều trị) từ văn bản bác sĩ gõ tự do.
* **expected_key_points:**
  - id: KP8_1
    content: Huấn luyện mô hình NER chuyên biệt
    keypoint_weight: 0.5
    description: Sử dụng PhoBERT hoặc ViBERT làm backbone; fine-tune trên tập dữ liệu bệnh án y khoa được gán nhãn theo định dạng BIO. Kết hợp CRF hoặc softmax lớp cuối để dự đoán thực thể.
  - id: KP8_2
    content: Chuẩn hóa thực thể y khoa (Entity Normalization/Linking)
    keypoint_weight: 0.5
    description: Xây dựng pipeline so khớp các thực thể trích xuất được với từ điển chuẩn quốc tế (như ICD-10 cho bệnh lý, RxNorm cho tên thuốc) bằng cách sử dụng vector embedding và thuật toán so khớp mờ để giải quyết lỗi chính tả viết tắt của bác sĩ.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp dịch thuật tài liệu pháp lý chuyên ngành tự động hỗ trợ 50 ngôn ngữ, tối ưu hóa bộ nhớ dịch thuật (Translation Memory) để đảm bảo tính nhất quán của thuật ngữ pháp lý.
* **expected_key_points:**
  - id: KP9_1
    content: Kiến trúc dịch máy kết hợp thuật ngữ (Terminology-constrained Translation)
    keypoint_weight: 0.5
    description: Sử dụng mô hình dịch thuật đa ngôn ngữ (như NLLB-200) fine-tune trên văn bản pháp luật. Tích hợp cơ chế ràng buộc thuật ngữ (Lexicon constraint): chèn trực tiếp các cặp thuật ngữ pháp lý chuẩn vào prompt hoặc ma trận attention để bắt mô hình dịch đúng từ quy định.
  - id: KP9_2
    content: Tích hợp Translation Memory (TM)
    keypoint_weight: 0.5
    description: Thiết lập Vector DB lưu trữ các câu pháp lý đã được dịch chuẩn bởi chuyên gia. Khi có tài liệu mới, truy vấn câu tương đồng từ TM; nếu độ tương đồng > 90%, lấy trực tiếp bản dịch cũ; ngược lại mới gửi qua mô hình dịch máy.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống tóm tắt tài liệu văn bản dài (Long-document Summarization - ví dụ báo cáo nghiên cứu 100 trang) vượt quá giới hạn cửa sổ ngữ cảnh của các mô hình LLM thông thường.
* **expected_key_points:**
  - id: KP10_1
    content: Chiến lược tóm tắt phân cấp (Hierarchical/MapReduce Summarization)
    keypoint_weight: 0.6
    description: Chia tài liệu thành các chương/mục nhỏ -> Giai đoạn Map: gửi từng phần qua LLM để sinh tóm tắt cục bộ -> Giai đoạn Reduce: ghép các bản tóm tắt cục bộ lại và tóm tắt một lần nữa để có kết quả tổng quan cuối cùng.
  - id: KP10_2
    content: Lưu trữ trạng thái ngữ cảnh (Memory-based/Incremental Summarization)
    keypoint_weight: 0.4
    description: Sử dụng cơ chế cập nhật nháp (incremental): đọc chương 1 -> tóm tắt -> dùng tóm tắt chương 1 làm ngữ cảnh đầu vào khi đọc và tóm tắt chương 2, đảm bảo luồng thông tin không bị ngắt quãng.

