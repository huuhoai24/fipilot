# Bộ Câu Hỏi Phỏng Vấn Web Developer (Level 1) - Tập Đề Mới (15)

* **Role:** Web Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, `position: absolute` và `position: fixed` khác nhau như thế nào?
* **expected_key_points:**
  - id: KP1_1
    content: Hệ quy chiếu định vị
    keypoint_weight: 0.5
    description: `absolute` định vị dựa trên phần tử cha gần nhất có `position` khác `static`. `fixed` định vị trực tiếp dựa trên viewport (cửa sổ trình duyệt).
  - id: KP1_2
    content: Hành vi khi cuộn trang
    keypoint_weight: 0.5
    description: Phần tử `absolute` sẽ cuộn theo nội dung trang. Phần tử `fixed` sẽ đứng yên tại vị trí đó bất chấp người dùng cuộn trang.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** JavaScript `Arrow Function` khác gì với `Regular Function` (hàm truyền thống)?
* **expected_key_points:**
  - id: KP2_1
    content: Cơ chế của `this`
    keypoint_weight: 0.6
    description: Arrow function không có `this` riêng, nó kế thừa `this` từ phạm vi (scope) bao quanh nó (lexical scoping). Regular function có `this` riêng tùy vào cách gọi hàm.
  - id: KP2_2
    content: Cú pháp và đối tượng `arguments`
    keypoint_weight: 0.4
    description: Arrow function có cú pháp ngắn gọn hơn và không có đối tượng `arguments` cục bộ bên trong.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Thẻ `<meta charset="UTF-8">` trong HTML dùng để làm gì?
* **expected_key_points:**
  - id: KP3_1
    content: Thiết lập bảng mã ký tự
    keypoint_weight: 0.5
    description: Khai báo cho trình duyệt biết trang web sử dụng bảng mã UTF-8 để hiển thị các ký tự văn bản.
  - id: KP3_2
    content: Tầm quan trọng
    keypoint_weight: 0.5
    description: Giúp hiển thị chính xác các ký tự đặc biệt, các ngôn ngữ đa dạng (tiếng Việt, tiếng Nhật, emoji) mà không bị lỗi font (mojibake).

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `Map` và `Object` trong JavaScript và khi nào nên dùng `Map`?
* **expected_key_points:**
  - id: KP4_1
    content: Khả năng hỗ trợ Key
    keypoint_weight: 0.5
    description: `Object` chỉ hỗ trợ key là string/symbol. `Map` cho phép key là bất kỳ giá trị nào (object, function, number).
  - id: KP4_2
    content: Khi nào dùng Map
    keypoint_weight: 0.5
    description: Dùng `Map` khi cần lưu trữ key không phải là string, cần duy trì thứ tự chèn phần tử, hoặc cần lấy kích thước (size) của collection thường xuyên.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm "Bất đồng bộ" (Asynchronous) trong JavaScript và tại sao nó cần thiết trong Web?
* **expected_key_points:**
  - id: KP5_1
    content: Định nghĩa bất đồng bộ
    keypoint_weight: 0.5
    description: Khả năng thực hiện các tác vụ tốn thời gian (như gọi API, xử lý file) mà không làm "treo" luồng thực thi chính (main thread).
  - id: KP5_2
    content: Tại sao cần thiết
    keypoint_weight: 0.5
    description: Giúp trang web vẫn phản hồi tương tác người dùng (scroll, click) trong lúc đang chờ dữ liệu từ máy chủ trả về, cải thiện trải nghiệm người dùng.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cách `Event Loop` của JavaScript xử lý mã đồng bộ và bất đồng bộ.
* **expected_key_points:**
  - id: KP6_1
    content: Call Stack
    keypoint_weight: 0.5
    description: Nơi thực thi mã đồng bộ. Khi một tác vụ bất đồng bộ được gọi, nó được đẩy sang Web APIs/Node APIs để xử lý.
  - id: KP6_2
    content: Callback Queue và Vòng lặp
    keypoint_weight: 0.5
    description: Khi tác vụ API xong, callback được đẩy vào Queue. Event Loop kiểm tra nếu Stack rỗng thì đẩy callback từ Queue vào Stack để thực thi.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `PUT` và `PATCH` khi cập nhật dữ liệu trong REST API?
* **expected_key_points:**
  - id: KP7_1
    content: PUT (Thay thế toàn phần)
    keypoint_weight: 0.5
    description: Gửi toàn bộ đối tượng để thay thế hoàn toàn tài nguyên cũ.
  - id: KP7_2
    content: PATCH (Cập nhật một phần)
    keypoint_weight: 0.5
    description: Chỉ gửi những trường dữ liệu cần thay đổi, tài nguyên cũ giữ lại các trường không được đề cập.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Hiện tượng "Memory Leak" do việc không dọn dẹp các biến tham chiếu từ Closure xảy ra như thế nào?
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất closure
    keypoint_weight: 0.5
    description: Closure giữ lại liên kết với scope của hàm cha. Nếu hàm cha có các đối tượng lớn và closure tồn tại dài hạn, các đối tượng này không bao giờ được GC (Garbage Collector) dọn dẹp.
  - id: KP8_2
    content: Cách khắc phục
    keypoint_weight: 0.5
    description: Gán biến lớn bằng `null` khi không dùng nữa hoặc tránh sử dụng closure trong các vòng lặp tạo hàm lớn.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích "Hydration" và tại sao nó có thể là nút thắt cổ chai về hiệu năng trong React SSR (Server Side Rendering)?
* **expected_key_points:**
  - id: KP9_1
    content: Quá trình Hydration
    keypoint_weight: 0.5
    description: Quá trình trình duyệt "gắn" JavaScript (event listeners, state) vào HTML tĩnh được server gửi xuống.
  - id: KP9_2
    content: Vấn đề hiệu năng
    keypoint_weight: 0.5
    description: Việc chạy JS để hydrate tốn nhiều CPU, khóa luồng chính (Main Thread), khiến người dùng không tương tác được với trang web dù đã nhìn thấy nội dung.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** "Optimistic UI Updates" là gì và làm thế nào để xử lý lỗi khi cập nhật giao diện kiểu này?
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Cập nhật giao diện ngay lập tức như thể yêu cầu đã thành công, tạo cảm giác phản hồi tức thì cho người dùng.
  - id: KP10_2
    content: Xử lý lỗi
    keypoint_weight: 0.5
    description: Nếu server trả về lỗi, ứng dụng phải tự động "rollback" (hoàn tác) về trạng thái cũ và thông báo lỗi cho người dùng.