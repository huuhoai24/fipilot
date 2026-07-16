# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2) - Tập Đề Concurrency và Thread Safety (13)

* **Role:** Backend Developer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích khái niệm Race Condition (Tranh chấp luồng). Cho ví dụ thực tế trong lập trình backend.
* **expected_key_points:**
  - id: KP1_1
    content: Định nghĩa Race Condition
    keypoint_weight: 0.5
    description: Xảy ra khi nhiều luồng thực thi (threads) đồng thời truy cập và sửa đổi một vùng nhớ dùng chung mà không có cơ chế đồng bộ, kết quả cuối cùng phụ thuộc vào thứ tự chạy của các luồng.
  - id: KP1_2
    content: Ví dụ thực tế cụ thể
    keypoint_weight: 0.5
    description: Luồng A và B cùng đọc số dư tài khoản = 100$, cùng thực hiện cộng 10$ -> cả hai luồng cùng ghi đè giá trị 110$ thay vì 120$.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Thế nào là một đoạn mã an toàn luồng (Thread-safe)? Trình bày 2 phương pháp cơ bản để đạt được tính an toàn luồng trong lập trình.
* **expected_key_points:**
  - id: KP2_1
    content: Khái niệm Thread-safe
    keypoint_weight: 0.5
    description: Là tính chất của đoạn code đảm bảo chạy đúng và nhất quán dữ liệu ngay cả khi có nhiều luồng cùng gọi thực thi đồng thời.
  - id: KP2_2
    content: Các phương pháp đạt Thread-safe
    keypoint_weight: 0.5
    description: Sử dụng biến bất biến (Immutable objects); sử dụng cơ chế đồng bộ hóa (synchronization/locks) để chặn truy cập đồng thời hoặc dùng biến cục bộ (ThreadLocal).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau giữa Process (Tiến trình) và Thread (Luồng) về mặt chia sẻ tài nguyên bộ nhớ.
* **expected_key_points:**
  - id: KP3_1
    content: Đặc trưng Process
    keypoint_weight: 0.5
    description: Process là một chương trình đang thực thi, sở hữu một vùng không gian địa chỉ bộ nhớ độc lập; giao tiếp giữa các process tốn nhiều chi phí (IPC).
  - id: KP3_2
    content: Đặc trưng Thread
    keypoint_weight: 0.5
    description: Thread là đơn vị xử lý nhỏ nhất bên trong Process. Các threads trong cùng một process chia sẻ chung bộ nhớ (Heap) nhưng có Stack riêng biệt, giao tiếp rất nhanh.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt sự khác nhau giữa hai cơ chế khóa: Pessimistic Lock (Khóa bi quan) và Optimistic Lock (Khóa lạc quan) ở cấp độ mã nguồn ứng dụng.
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế hoạt động khóa bi quan
    keypoint_weight: 0.5
    description: Sử dụng lệnh đồng bộ cứng (như `synchronized` trong Java hoặc Mutex lock) để chặn đứng mọi luồng khác khi 1 luồng đang truy cập tài nguyên.
  - id: KP4_2
    content: Cơ chế hoạt động khóa lạc quan
    keypoint_weight: 0.5
    description: Không dùng lệnh khóa; sử dụng cơ chế CAS (Compare-And-Swap) hoặc kiểm tra phiên bản trước khi ghi dữ liệu; nếu phát hiện bị đổi thì retry.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là lỗi nghẽn khóa (Deadlock) giữa các luồng chạy song song? Chỉ ra 4 điều kiện cần để xảy ra Deadlock.
* **expected_key_points:**
  - id: KP5_1
    content: Bản chất lỗi Deadlock luồng
    keypoint_weight: 0.5
    description: Xảy ra khi hai hoặc nhiều luồng bị treo vô tận vì mỗi luồng đang chờ đợi giải phóng khóa từ tài nguyên mà luồng kia đang nắm giữ.
  - id: KP5_2
    content: 4 điều kiện xảy ra Deadlock
    keypoint_weight: 0.5
    description: Mutual Exclusion (loại trừ lẫn nhau), Hold and Wait (giữ và chờ), No Preemption (không cướp đoạt), và Circular Wait (chờ đợi vòng tròn).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích sự khác nhau về luồng xử lý và hiệu năng giữa kiến trúc Blocking I/O và Non-blocking I/O (Asynchronous I/O).
* **expected_key_points:**
  - id: KP6_1
    content: Mô hình Blocking I/O
    keypoint_weight: 0.5
    description: Luồng hiện tại sẽ bị treo (blocked) để đợi kết quả trả về từ ổ đĩa hoặc kết nối mạng mạng, lãng phí tài nguyên CPU của server.
  - id: KP6_2
    content: Mô hình Non-blocking I/O
    keypoint_weight: 0.5
    description: Luồng gửi yêu cầu I/O rồi tiếp tục thực hiện công việc khác ngay lập tức; khi I/O hoàn thành, hệ thống sẽ gọi lại thông qua Callback/Event Loop (như Node.js).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trình bày vai trò và cách thiết lập các thông số cơ bản của Thread Pool (core pool size, max pool size, queue capacity) trong một ứng dụng Backend xử lý nhiều requests.
* **expected_key_points:**
  - id: KP7_1
    content: Khái niệm và thông số Thread Pool
    keypoint_weight: 0.6
    description: Thread Pool quản lý một tập các luồng tái sử dụng để tránh chi phí tạo/hủy luồng liên tục. `corePoolSize` là số luồng luôn duy trì. `maxPoolSize` là số luồng tối đa khi hàng đợi bị đầy.
  - id: KP7_2
    content: Vai trò của Hàng đợi công việc (Task Queue)
    keypoint_weight: 0.4
    description: Khi số lượng request vượt quá `corePoolSize`, các request mới được đưa vào hàng đợi (`queueCapacity`) chờ xử lý; cấu hình quá nhỏ gây lỗi từ chối tác vụ (RejectedExecution).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp an toàn luồng cho một bộ đếm số lượng xem bài viết (Page View Counter) thời gian thực chịu tải 100,000 requests mỗi giây mà không làm nghẽn hiệu năng của server.
* **expected_key_points:**
  - id: KP8_1
    content: Tránh đồng bộ hóa thô bạo (Synchronized)
    keypoint_weight: 0.5
    description: Không dùng các lệnh khóa chặn (`synchronized`) trên toàn bộ hàm vì sẽ biến đa luồng thành tuần tự, làm giảm vọt throughput của hệ thống.
  - id: KP8_2
    content: Sử dụng Atomic Variables và Redis
    keypoint_weight: 0.5
    description: Sử dụng các biến nguyên tử (như `AtomicLong` dựa trên phần cứng CAS) hoặc đẩy luồng đếm vào bộ đệm Redis bằng lệnh tăng nguyên tử `INCR`, định kỳ ghi đồng bộ xuống DB.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế một bộ đệm lưu trữ dữ liệu trong bộ nhớ (In-memory Cache) thủ công hỗ trợ tự động xóa key hết hạn (TTL) và an toàn luồng khi có hàng nghìn luồng đọc/ghi đồng thời.
* **expected_key_points:**
  - id: KP9_1
    content: Sử dụng ConcurrentHashMap và Read-Write Locks
    keypoint_weight: 0.5
    description: Sử dụng cấu trúc dữ liệu `ConcurrentHashMap` (Java) hoặc cơ chế khóa đọc-ghi phân tách (`ReentrantReadWriteLock`) để cho phép nhiều luồng đọc đồng thời nhưng khóa khi ghi.
  - id: KP9_2
    content: Cơ chế dọn dẹp key hết hạn chạy ngầm
    keypoint_weight: 0.5
    description: Khởi động một luồng chạy ngầm định kỳ (Daemon Thread) quét ngẫu nhiên các keys để xóa key hết hạn dựa trên TTL, kết hợp xóa lười (lazy delete) khi key được truy cập.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp phân phối công việc bất đồng bộ cho cụm ứng dụng Backend, giải quyết hiện tượng sập server do rò rỉ bộ nhớ (Memory Leak) khi tích hợp luồng xử lý chạy ngầm.
* **expected_key_points:**
  - id: KP10_1
    content: Nguyên nhân rò rỉ bộ nhớ đa luồng
    keypoint_weight: 0.5
    description: Do giữ lại các tham chiếu đến đối tượng trong biến ThreadLocal mà không gọi hàm `remove()` sau khi xử lý xong, làm Garbage Collector không thể thu hồi bộ nhớ.
  - id: KP10_2
    content: Giải pháp giải phóng tài nguyên triệt để
    keypoint_weight: 0.5
    description: Bắt buộc đặt lệnh dọn dẹp tài nguyên trong khối `finally { threadLocal.remove(); }`; cấu hình timeout cho các luồng xử lý bất đồng bộ để tránh treo luồng vô hạn.

