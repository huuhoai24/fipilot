# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2) - Tập Đề Advanced DB và Data Integrity (16)

* **Role:** Backend Developer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích vai trò của các ràng buộc (Constraints) trong cơ sở dữ liệu quan hệ: NOT NULL, UNIQUE, CHECK, và FOREIGN KEY.
* **expected_key_points:**
  - id: KP1_1
    content: NOT NULL và UNIQUE
    keypoint_weight: 0.5
    description: NOT NULL bắt buộc cột dữ liệu phải có giá trị. UNIQUE đảm bảo giá trị trong cột không được trùng lặp trên tất cả các dòng của bảng.
  - id: KP1_2
    content: CHECK và FOREIGN KEY
    keypoint_weight: 0.5
    description: CHECK kiểm tra điều kiện logic của giá trị trước khi lưu (ví dụ: tuổi > 18). FOREIGN KEY liên kết khóa ngoại đảm bảo tính toàn vẹn tham chiếu.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Lệnh ROLLBACK trong SQL hoạt động như thế nào? Nêu một kịch bản ứng dụng Backend cần thực thi ROLLBACK.
* **expected_key_points:**
  - id: KP2_1
    content: Nguyên lý hoạt động của ROLLBACK
    keypoint_weight: 0.5
    description: ROLLBACK hoàn trả toàn bộ cơ sở dữ liệu về trạng thái trước khi transaction bắt đầu, hủy bỏ tất cả các thay đổi chưa được commit.
  - id: KP2_2
    content: Kịch bản ứng dụng thực tế
    keypoint_weight: 0.5
    description: Trong thanh toán chuyển tiền: trừ tiền ví người gửi thành công nhưng cộng tiền ví người nhận bị lỗi -> bắt buộc gọi ROLLBACK để trả lại tiền cho ví người gửi.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa hai kiểu dữ liệu lưu trữ thời gian: TIMESTAMP và DATETIME trong CSDL quan hệ.
* **expected_key_points:**
  - id: KP3_1
    content: Kiểu dữ liệu DATETIME
    keypoint_weight: 0.5
    description: DATETIME lưu trữ ngày giờ cố định độc lập với múi giờ (Timezone), giá trị lưu thế nào thì hiển thị y nguyên như thế.
  - id: KP3_2
    content: Kiểu dữ liệu TIMESTAMP
    keypoint_weight: 0.5
    description: TIMESTAMP tự động chuyển đổi sang múi giờ UTC khi lưu và chuyển ngược lại múi giờ hiện tại của client khi đọc, chiếm ít dung lượng hơn DATETIME.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm Transactions và cách triển khai Giao dịch lồng nhau (Nested Transactions / Savepoints) trong CSDL quan hệ.
* **expected_key_points:**
  - id: KP4_1
    content: Khái niệm Savepoints
    keypoint_weight: 0.5
    description: Savepoint cho phép chia một transaction lớn thành các mốc nhỏ; ta có thể rollback về một mốc xác định mà không cần hủy bỏ toàn bộ transaction chính.
  - id: KP4_2
    content: Kịch bản sử dụng Savepoints
    keypoint_weight: 0.5
    description: Khi xử lý một đơn hàng có nhiều sản phẩm: nếu 1 sản phẩm phụ bị lỗi ghi, ta rollback riêng sản phẩm đó về Savepoint và tiếp tục thực hiện hoàn thành đơn hàng với các sản phẩm chính còn lại.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích tác động của việc không cấu hình chỉ mục (Index) trên các cột Khóa ngoại (Foreign Key) khi thực hiện xóa hoặc cập nhật bản ghi cha.
* **expected_key_points:**
  - id: KP5_1
    content: Nguyên nhân gây chậm khi xóa/sửa bản ghi cha
    keypoint_weight: 0.5
    description: Khi xóa bản ghi cha, DB phải quét bảng con để kiểm tra ràng buộc khóa ngoại; nếu không có index trên cột khóa ngoại ở bảng con, DB sẽ phải quét toàn bộ bảng con (Full Table Scan).
  - id: KP5_2
    content: Gây lỗi khóa chặn diện rộng (Table Locking)
    keypoint_weight: 0.5
    description: Quét toàn bộ bảng con làm khóa nhiều dòng dữ liệu, dẫn đến cản trở các giao dịch chèn/xóa khác chạy song song trên bảng con, gây chậm hệ thống nặng nề.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế hoạt động của Soft Delete (Xóa mềm) so với Hard Delete (Xóa cứng). Khi thiết kế database, bạn cần lưu ý điều gì khi dùng Soft Delete kết hợp ràng buộc UNIQUE?
* **expected_key_points:**
  - id: KP6_1
    content: Bản chất Soft Delete vs Hard Delete
    keypoint_weight: 0.5
    description: Hard Delete xóa hoàn toàn bản ghi khỏi ổ đĩa. Soft Delete chỉ cập nhật trạng thái ẩn (ví dụ: `is_deleted = true` hoặc `deleted_at = timestamp`).
  - id: KP6_2
    content: Xử lý xung đột ràng buộc UNIQUE
    keypoint_weight: 0.5
    description: Nếu có trường UNIQUE (như email): khi user xóa mềm tài khoản, email đó vẫn tồn tại trong DB, làm user mới không đăng ký được email đó. Giải pháp: Thêm trường `deleted_at` vào tổ hợp UNIQUE index `(email, deleted_at)`.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là lỗi mất mát cập nhật (Lost Update) trong xử lý đồng thời CSDL? Làm thế nào để giải quyết lỗi này bằng câu lệnh UPDATE nguyên tử?
* **expected_key_points:**
  - id: KP7_1
    content: Cơ chế phát sinh lỗi Lost Update
    keypoint_weight: 0.5
    description: Xảy ra khi hai transaction đọc cùng một dữ liệu -> cùng thay đổi cục bộ -> transaction A ghi đè kết quả lên DB -> transaction B tiếp tục ghi đè kết quả của nó, làm mất bản cập nhật của A.
  - id: KP7_2
    content: Sử dụng câu lệnh UPDATE nguyên tử (Atomic Update)
    keypoint_weight: 0.5
    description: Không đọc về code xử lý; thực hiện tính toán trực tiếp trong câu lệnh SQL: `UPDATE products SET quantity = quantity - 1 WHERE id = :id AND quantity >= 1`.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế cơ sở dữ liệu và luồng nghiệp vụ xử lý chuyển tiền giữa các tài khoản ngân hàng, đảm bảo tính nhất quán tuyệt đối về tiền tệ và không bao giờ bị lệch tổng số tiền hệ thống.
* **expected_key_points:**
  - id: KP8_1
    content: Sử dụng ACID Transaction và Khóa bi quan
    keypoint_weight: 0.5
    description: Bọc toàn bộ luồng chuyển tiền trong một Transaction; thực hiện khóa dòng tài khoản nguồn và đích bằng `SELECT ... FOR UPDATE` theo thứ tự ID tăng dần để tránh deadlock.
  - id: KP8_2
    content: Thiết kế bảng Nhật ký giao dịch (Double-Entry Bookkeeping)
    keypoint_weight: 0.5
    description: Áp dụng nguyên lý kế toán kép: mọi giao dịch phải ghi nhận đồng thời vào bảng nhật ký (Ledger): một dòng ghi nợ (- tiền tài khoản A) và một dòng ghi có (+ tiền tài khoản B), tổng nợ và có của giao dịch luôn bằng 0.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp phục hồi dữ liệu và kiểm tra tính toàn vẹn của cơ sở dữ liệu sau sự cố sập nguồn đột ngột (Crash Recovery) sử dụng Write-Ahead Log (WAL) và Checkpointing.
* **expected_key_points:**
  - id: KP9_1
    content: Nguyên lý hoạt động của Checkpoint trong DB
    keypoint_weight: 0.5
    description: Checkpoint định kỳ đồng bộ toàn bộ dữ liệu dơ (dirty data blocks) từ bộ nhớ RAM xuống ổ đĩa cứng và ghi nhận mốc thời gian an toàn vào file log.
  - id: KP9_2
    content: Quy trình chạy Redo và Undo sau Crash
    keypoint_weight: 0.5
    description: Sau sự cố: CSDL đọc log từ mốc checkpoint gần nhất; chạy lại (Redo) tất cả các thay đổi của transaction đã commit; hoàn trả (Undo) các thay đổi của transaction chưa kịp commit về trạng thái cũ.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp phân tách cơ sở dữ liệu đọc/ghi động sử dụng Hibernate / Spring routing DataSource để tự động định tuyến các câu query SELECT sang Replica và INSERT/UPDATE sang Master.
* **expected_key_points:**
  - id: KP10_1
    content: Thiết lập Dynamic Routing DataSource
    keypoint_weight: 0.5
    description: Cấu hình một lớp Router DataSource kế thừa `AbstractRoutingDataSource`; ghi đè hàm xác định khóa kết nối hiện tại dựa trên ngữ cảnh giao dịch (Transaction Context).
  - id: KP10_2
    content: Định tuyến dựa trên trạng thái Read-Only
    keypoint_weight: 0.5
    description: Sử dụng annotation `@Transactional(readOnly = true)` để đánh dấu giao dịch chỉ đọc -> Router tự động chọn kết nối từ Replica pool; ngược lại chọn kết nối từ Master pool.

