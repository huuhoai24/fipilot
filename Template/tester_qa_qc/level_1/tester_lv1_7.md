# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1) - Tập Đề Test Strategy và SQL HAVING (7)

* **Role:** Tester
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt khái niệm "Test Policy" (Chính sách kiểm thử) và "Test Strategy" (Chiến lược kiểm thử) trong một tổ chức phát triển phần mềm.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa Test Policy
    keypoint_weight: 0.5
    description: Là tài liệu cấp cao nhất, định nghĩa các nguyên tắc, mục tiêu chất lượng và cam kết kiểm thử của toàn bộ công ty/tổ chức.
  - id: KP1_2
    content: Định nghĩa Test Strategy
    keypoint_weight: 0.5
    description: Là tài liệu chi tiết hơn, mô tả cách thức, phương pháp kiểm thử, công cụ, môi trường và tiêu chí đánh giá chất lượng cho một dự án cụ thể.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Thế nào là Ad-hoc Testing và nó khác biệt như thế nào so với Exploratory Testing?
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm Ad-hoc Testing
    keypoint_weight: 0.5
    description: Là kiểm thử ngẫu nhiên, không theo kế hoạch, không chuẩn bị trước, nhằm tìm nhanh các lỗi nghiêm trọng bằng cách tương tác tự do với ứng dụng.
  - id: KP2_2
    content: Điểm khác biệt với Exploratory Testing
    keypoint_weight: 0.5
    description: Exploratory Testing có tính cấu trúc hơn, kết hợp học hỏi hệ thống và ghi chép lại các kịch bản mới phát hiện, trong khi Ad-hoc hoàn toàn tự phát.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** JSON là gì? Viết cấu trúc cơ bản của một chuỗi JSON thể hiện thông tin của một sản phẩm gồm: mã sản phẩm (id), tên sản phẩm (name), và giá (price).
* **expected_key_points:**
  - id: KP3_1
    content: Khái niệm JSON
    keypoint_weight: 0.4
    description: JSON (JavaScript Object Notation) là định dạng trao đổi dữ liệu dạng văn bản nhẹ, dễ đọc viết và phân tích bởi máy tính.
  - id: KP3_2
    content: Viết chuỗi JSON chính xác
    keypoint_weight: 0.6
    description: Viết đúng định dạng: `{"id": 101, "name": "Iphone 13", "price": 799.99}`. Cặp key-value phải đặt trong nháy kép.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế các kịch bản kiểm thử cho tính năng bộ lọc nâng cao (Multi-filter) gồm các thuộc tính: Danh mục (Category), Khoảng giá (Price range) và Đánh giá (Rating) trên trang thương mại điện tử.
* **expected_key_points:**
  - id: KP4_1
    content: Kiểm thử lọc đơn lẻ và lọc kết hợp
    keypoint_weight: 0.5
    description: Kiểm tra chọn riêng lẻ từng bộ lọc hiển thị đúng sản phẩm; kiểm tra chọn kết hợp cả 3 bộ lọc để xem kết quả hiển thị có thỏa mãn đồng thời tất cả điều kiện lọc hay không.
  - id: KP4_2
    content: Kiểm thử trạng thái rỗng và reset bộ lọc
    keypoint_weight: 0.5
    description: Kiểm tra khi không có sản phẩm nào thỏa mãn điều kiện lọc (hiển thị thông báo phù hợp); kiểm tra nút 'Xóa bộ lọc' (Reset) đưa trang về trạng thái mặc định ban đầu.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết câu lệnh SQL sử dụng mệnh đề HAVING kết hợp với GROUP BY để tìm ra những nhóm sản phẩm (category_id) có tổng số lượng hàng tồn kho (quantity) lớn hơn 500.
* **expected_key_points:**
  - id: KP5_1
    content: Sử dụng HAVING chính xác
    keypoint_weight: 0.6
    description: Viết câu lệnh: `SELECT category_id, SUM(quantity) FROM products GROUP BY category_id HAVING SUM(quantity) > 500`.
  - id: KP5_2
    content: Phân biệt HAVING và WHERE
    keypoint_weight: 0.4
    description: HAVING dùng để lọc điều kiện sau khi dữ liệu đã gom nhóm (GROUP BY) còn WHERE lọc trước khi gom nhóm.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách sử dụng tab Performance trong Chrome DevTools để đo lường tốc độ tải trang và phát hiện các vấn đề làm chậm ứng dụng web.
* **expected_key_points:**
  - id: KP6_1
    content: Cách ghi lại hiệu năng trang
    keypoint_weight: 0.5
    description: Mở tab Performance -> nhấn nút Record (Ctrl+E) -> load lại trang web hoặc thực hiện thao tác trên UI -> nhấn Stop để xem báo cáo phân tích.
  - id: KP6_2
    content: Phân tích các chỉ số
    keypoint_weight: 0.5
    description: Phân tích thời gian dựng hình (rendering), scripting, các khoảng block luồng chính (Main Thread) và xác định tác nhân gây chậm (hình ảnh nặng, JS script chạy lâu).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết test case cho chức năng Đổi mật khẩu (Change Password) yêu cầu nhập mật khẩu cũ, mật khẩu mới và xác nhận mật khẩu mới.
* **expected_key_points:**
  - id: KP7_1
    content: Kiểm thử luồng đổi mật khẩu thành công
    keypoint_weight: 0.5
    description: Nhập đúng mật khẩu cũ, mật khẩu mới hợp lệ trùng với mật khẩu xác nhận -> đổi thành công, hệ thống yêu cầu đăng nhập lại bằng pass mới.
  - id: KP7_2
    content: Kiểm thử luồng lỗi và bảo mật
    keypoint_weight: 0.5
    description: Mật khẩu cũ nhập sai; mật khẩu mới trùng mật khẩu cũ; mật khẩu xác nhận không khớp mật khẩu mới; mật khẩu mới yếu/không thỏa mãn độ phức tạp quy định.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản kiểm thử cho hệ thống phân phối nội dung (CDN) để đảm bảo hình ảnh/video mới được cập nhật trên server gốc hiển thị ngay lập tức tới người dùng cuối (Cache Invalidation).
* **expected_key_points:**
  - id: KP8_1
    content: Kiểm chứng cơ chế xóa Cache (Cache Invalidation/Purge)
    keypoint_weight: 0.6
    description: Xác minh khi cập nhật ảnh mới, hệ thống tự động gửi lệnh Purge cache đến các CDN Edge Servers để xóa bản sao cũ, buộc CDN phải kéo dữ liệu mới từ origin server.
  - id: KP8_2
    content: Kiểm tra Cache headers của CDN response
    keypoint_weight: 0.4
    description: Đọc giá trị các Headers của API/ảnh như `X-Cache: HIT/MISS` hoặc `Age` để biết file được lấy từ CDN hay server gốc, đảm bảo người dùng nhận được file mới nhất.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích rủi ro và cách thiết kế kịch bản kiểm thử tính năng chuyển tiền liên ngân hàng 24/7 khi hệ thống của ngân hàng đích phản hồi chậm hoặc không phản hồi.
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế Timeout và Trạng thái chờ xử lý (Pending)
    keypoint_weight: 0.6
    description: Đảm bảo hệ thống giao dịch của ngân hàng gửi không tự ý báo thất bại ngay hoặc thành công ngay mà phải đưa giao dịch vào trạng thái Pending và chờ đối soát tự động.
  - id: KP9_2
    content: Xử lý bồi hoàn tiền (Refund/Rollback)
    keypoint_weight: 0.4
    description: If ngân hàng nhận phản hồi lỗi sau thời gian timeout, hệ thống ngân hàng gửi phải thực hiện rollback giao dịch và hoàn tiền an toàn về tài khoản nguồn.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Làm thế nào để kiểm thử tính nhất quan của dữ liệu (Data Integrity) trong hệ thống cơ sở dữ liệu phân tán (Distributed Database) sử dụng cơ chế Replication?
* **expected_key_points:**
  - id: KP10_1
    content: Đồng bộ hóa dữ liệu (Replication Delay)
    keypoint_weight: 0.5
    description: Kiểm tra độ trễ đồng bộ dữ liệu ghi (Write) từ Master Node sang các Slave Node (Read) trong điều kiện mạng bình thường và khi tải cao.
  - id: KP10_2
    content: Kiểm thử tính nhất quán cuối cùng (Eventual Consistency)
    keypoint_weight: 0.5
    description: Thực hiện cập nhật dữ liệu ở Master và truy vấn liên tục ở các Slave Node để xác định thời điểm dữ liệu ở tất cả các Node khớp nhau hoàn toàn.

