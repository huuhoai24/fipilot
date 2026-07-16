# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2) - Tập Đề Caching Concepts và Redis Basics (5)

* **Role:** Backend Developer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Caching là gì? Giải thích vai trò của Caching trong việc cải thiện hiệu năng và giảm tải cho cơ sở dữ liệu chính.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa Caching và tốc độ đọc
    keypoint_weight: 0.5
    description: Caching là việc lưu trữ tạm thời dữ liệu thường xuyên truy cập vào bộ nhớ tốc độ cao (như RAM) để trả kết quả cực nhanh cho client mà không cần tính toán lại.
  - id: KP1_2
    content: Giảm tải cho Database
    keypoint_weight: 0.5
    description: Tránh việc DB chính phải chạy các câu query nặng lặp đi lặp lại nhiều lần, giúp duy trì độ ổn định cho DB và tiết kiệm tài nguyên CPU/IOPS.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày các kiểu dữ liệu cơ bản trong Redis (String, List, Set, Hash, Sorted Set) và một ví dụ ứng dụng thực tế cho mỗi loại.
* **expected_key_points:**
  - id: KP2_1
    content: Các kiểu dữ liệu cơ bản
    keypoint_weight: 0.6
    description: String (chuỗi/số), List (mảng tuần tự), Set (tập hợp không trùng lặp), Hash (cấu trúc key-value lồng), Sorted Set (tập hợp có sắp xếp theo điểm số).
  - id: KP2_2
    content: Ví dụ thực tế tương ứng
    keypoint_weight: 0.4
    description: String dùng lưu session, List dùng lưu tin nhắn chat, Set dùng lọc IP duy nhất, Hash lưu thông tin profile user, Sorted Set làm bảng xếp hạng Leaderboard.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích ý nghĩa của tham số TTL (Time-To-Live) khi thiết lập cache. Tại sao không nên đặt TTL vô hạn cho tất cả các keys?
* **expected_key_points:**
  - id: KP3_1
    content: Ý nghĩa của TTL
    keypoint_weight: 0.5
    description: TTL quy định thời gian tồn tại tối đa của dữ liệu trong cache; sau khoảng thời gian này cache sẽ tự động bị xóa bỏ.
  - id: KP3_2
    content: Nguy cơ khi đặt TTL vô hạn
    keypoint_weight: 0.5
    description: Làm cạn kiệt bộ nhớ RAM của server cache (Out of memory); đồng thời làm dữ liệu bị stale (lỗi thời) do không được cập nhật khi DB chính thay đổi.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích cơ chế hoạt động của chiến lược Cache-Aside (Lazy Loading). Trình bày luồng xử lý khi Đọc và khi Ghi dữ liệu.
* **expected_key_points:**
  - id: KP4_1
    content: Luồng Đọc dữ liệu (Read flow)
    keypoint_weight: 0.5
    description: Ứng dụng tìm dữ liệu trong cache -> nếu có (cache hit) trả về luôn; nếu không có (cache miss) đọc dữ liệu từ DB -> cập nhật dữ liệu vào cache -> trả về cho client.
  - id: KP4_2
    content: Luồng Ghi dữ liệu (Write flow)
    keypoint_weight: 0.5
    description: Ứng dụng cập nhật dữ liệu vào DB trước -> xóa key tương ứng trong cache để đảm bảo request tiếp theo sẽ đọc dữ liệu mới từ DB.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích hiện tượng Cache Penetration (Bộ đệm bị xuyên thủng). Làm thế nào để giải quyết vấn đề này?
* **expected_key_points:**
  - id: KP5_1
    content: Bản chất Cache Penetration
    keypoint_weight: 0.5
    description: Xảy ra khi client liên tục truy vấn các keys không tồn tại trong cả Cache và DB, khiến mọi request đều đi thẳng xuống DB gây quá tải.
  - id: KP5_2
    content: Giải pháp khắc phục
    keypoint_weight: 0.5
    description: Lưu các giá trị rỗng/null vào cache với TTL ngắn cho các key không tồn tại hoặc sử dụng cấu trúc dữ liệu Bloom Filter để lọc nhanh keys hợp lệ từ RAM.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là lỗi Cache Avalanche (Cache bị sập đổ hàng loạt)? Thiết kế giải pháp ngăn chặn hiện tượng này.
* **expected_key_points:**
  - id: KP6_1
    content: Nguyên nhân Cache Avalanche
    keypoint_weight: 0.5
    description: Xảy ra khi một lượng lớn keys trong cache hết hạn đồng thời tại cùng một thời điểm, hoặc khi hệ thống cache bị sập, khiến toàn bộ traffic đổ dồn xuống DB cùng lúc.
  - id: KP6_2
    content: Thiết kế giải pháp khắc phục
    keypoint_weight: 0.5
    description: Cộng thêm một khoảng thời gian ngẫu nhiên (random jitter) vào TTL của từng key để phân tán thời gian hết hạn; thiết lập cụm cache dự phòng (Redis Sentinel/Cluster).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày cách sử dụng Redis làm bộ lưu trữ Session (Session Store) cho cụm ứng dụng Backend chạy sau Load Balancer. Tại sao giải pháp này tối ưu hơn lưu session trong bộ nhớ máy chủ?
* **expected_key_points:**
  - id: KP7_1
    content: Thiết kế Session Store trên Redis
    keypoint_weight: 0.6
    description: Mỗi khi user đăng nhập, backend tạo session ID -> lưu thông tin user vào Redis dưới key là session ID -> trả session ID về client trong cookie.
  - id: KP7_2
    content: Tối ưu hóa hơn lưu RAM cục bộ
    keypoint_weight: 0.4
    description: Lưu RAM cục bộ làm các server không chia sẻ trạng thái được (yêu cầu sticky session). Lưu Redis giúp scale ngang ứng dụng thoải mái vì mọi instance đều đọc chung dữ liệu.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp đồng bộ dữ liệu giữa Cache và Cơ sở dữ liệu chính nhằm hạn chế tối đa hiện tượng dữ liệu không nhất quán (Stale Cache) trong hệ thống cập nhật liên tục.
* **expected_key_points:**
  - id: KP8_1
    content: Xóa cache thay vì cập nhật cache
    keypoint_weight: 0.5
    description: Khi update dữ liệu, xóa key cache thay vì ghi đè giá trị mới để tránh lỗi đua tranh luồng (race conditions) làm ghi đè dữ liệu cũ vào cache.
  - id: KP8_2
    content: Kỹ thuật Xóa kép (Cache Aside Double Delete)
    keypoint_weight: 0.5
    description: Chạy luồng: Xóa cache lần 1 -> Cập nhật DB chính -> Chờ 500ms (để các transaction DB đồng bộ xong) -> Xóa cache lần 2 để dọn sạch dữ liệu cũ còn sót.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống khóa phân tán (Distributed Lock) sử dụng Redis để ngăn chặn tình trạng ghi đè hoặc xung đột tài nguyên khi có nhiều instances ứng dụng cùng xử lý một đơn hàng.
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế khóa bằng lệnh SETNX
    keypoint_weight: 0.5
    description: Sử dụng lệnh `SET key value NX PX milliseconds` để acquire lock nguyên tử (atomic) kèm giá trị định danh duy nhất của thread và thiết lập TTL cho khóa tránh deadlock.
  - id: KP9_2
    content: Cơ chế giải phóng khóa an toàn
    keypoint_weight: 0.5
    description: Giải phóng khóa sử dụng Lua script để kiểm tra giá trị định danh của thread hiện tại trùng khớp với giá trị lưu trong khóa trước khi xóa, tránh việc xóa nhầm khóa của thread khác.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích cơ chế giải phóng bộ nhớ của Redis khi bị đầy (Eviction Policies) bao gồm LRU, LFU. Trong trường hợp nào bạn sẽ lựa chọn cấu hình chính sách nào?
* **expected_key_points:**
  - id: KP10_1
    content: Nguyên lý hoạt động của LRU và LFU
    keypoint_weight: 0.6
    description: LRU (Least Recently Used) loại bỏ các keys lâu nhất không được truy cập. LFU (Least Frequently Used) loại bỏ các keys có tần suất truy cập ít nhất.
  - id: KP10_2
    content: Lựa chọn chính sách phù hợp
    keypoint_weight: 0.4
    description: Chọn LRU cho dữ liệu có tính chất hot-topic thay đổi theo thời gian. Chọn LFU cho dữ liệu tĩnh có độ hot ổn định. Cấu hình `volatile-lru/lfu` để chỉ xóa các key có cài TTL.

