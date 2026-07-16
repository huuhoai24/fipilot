# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 5) - Tập Đề Distributed Caching và Locks (4)

* **Role:** Backend Developer
* **Level:** Level 5
* **Experience:** Trên 8 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích sự khác nhau về bản chất, cơ chế hoạt động và trường hợp áp dụng tối ưu giữa hai mô hình caching: Cache-Aside pattern và Read-Through/Write-Through pattern.
* **expected_key_points:**
  - id: KP1_1
    content: Cơ chế Cache-Aside pattern
    keypoint_weight: 0.5
    description: Ứng dụng trực tiếp quản lý cache: tự kiểm tra cache, nếu cache miss thì đọc từ DB rồi tự cập nhật vào cache. DB và Cache độc lập nhau.
  - id: KP1_2
    content: Cơ chế Read/Write-Through pattern
    keypoint_weight: 0.5
    description: Ứng dụng coi thư viện Caching là nguồn dữ liệu duy nhất. Khi đọc/ghi, Cache Provider tự động đồng bộ hóa xuống DB phía sau, mã nguồn ứng dụng gọn hơn.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Hiện tượng Xuyên thủng Cache (Cache Penetration) là gì? Hãy thiết kế giải pháp ngăn chặn nó bằng cách sử dụng cấu trúc dữ liệu Bloom Filter.
* **expected_key_points:**
  - id: KP2_1
    content: Bản chất Cache Penetration
    keypoint_weight: 0.5
    description: Xảy ra khi người dùng liên tục truy vấn các key không hề tồn tại trong cả cache và cơ sở dữ liệu (ví dụ: bị tấn công dò quét), bắt hệ thống phải truy vấn DB liên tục.
  - id: KP2_2
    content: Ngăn chặn bằng Bloom Filter
    keypoint_weight: 0.5
    description: Thiết lập Bloom Filter lưu trữ toàn bộ tập hợp keys hợp lệ trên RAM. Khi có request, kiểm tra nhanh qua Bloom Filter; nếu xác định key không tồn tại, từ chối ngay lập tức không truy vấn DB.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh sự khác nhau về cơ chế đồng thuận, khả năng chịu lỗi mạng và hiệu năng giữa khóa phân tán (Distributed Lock) sử dụng Redis (Redlock) và ZooKeeper.
* **expected_key_points:**
  - id: KP3_1
    content: Distributed Lock bằng Redis vs ZooKeeper
    keypoint_weight: 0.6
    description: Redis Redlock dựa trên tính toán thời gian hết hạn (TTL) và đồng thuận đa số node (AP). ZooKeeper sử dụng các Ephemeral Nodes kết hợp Watcher (CP), tự động xóa khóa khi client mất kết nối.
  - id: KP3_2
    content: So sánh Hiệu năng và An toàn
    keypoint_weight: 0.4
    description: Redis có hiệu năng và throughput cực cao nhưng có khả năng bị tranh chấp khóa do lệch giờ hệ thống. ZooKeeper đảm bảo an toàn tuyệt đối nhưng độ trễ ghi cao hơn.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích các chiến lược thu hồi bộ nhớ của Redis (Eviction Policies): LRU (Least Recently Used) và LFU (Least Frequently Used). Trong trường hợp nào bạn chọn chiến lược nào?
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế LRU vs LFU trong Redis
    keypoint_weight: 0.5
    description: LRU loại bỏ các keys lâu nhất không được truy cập (dựa trên mốc thời gian). LFU loại bỏ các keys có tần suất truy cập ít nhất (dựa trên bộ đếm tần suất).
  - id: KP4_2
    content: Kịch bản áp dụng thực tế
    keypoint_weight: 0.5
    description: Chọn LRU cho các ứng dụng có tính mùa vụ cao (các sản phẩm mới hot thay thế sản phẩm cũ). Chọn LFU khi muốn bảo vệ các dữ liệu tĩnh quan trọng luôn được truy cập đều đặn không bị trôi đi.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế giải pháp đồng bộ hóa dữ liệu cache và cơ sở dữ liệu chính để tránh hiện tượng rò rỉ dữ liệu cũ (Stale Cache) khi có nhiều luồng cập nhật đồng thời.
* **expected_key_points:**
  - id: KP5_1
    content: Chiến lược Xóa Cache thay vì Cập nhật Cache
    keypoint_weight: 0.5
    description: Khi update DB, thực hiện xóa key trong cache thay vì ghi đè giá trị mới. Ghi đè dễ dẫn đến mâu thuẫn trạng thái do thứ tự chạy của các threads bị lệch.
  - id: KP5_2
    content: Kỹ thuật Xóa kép (Cache Aside Double Delete)
    keypoint_weight: 0.5
    description: Luồng cập nhật: Xóa cache -> Update DB -> Chờ 500ms (để các transaction khác kịp commit) -> Xóa cache lần hai, triệt tiêu hoàn toàn khả năng ghi đè dữ liệu cũ.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân tích hiện tượng Tuyết lở cache (Cache Avalanche) và Tháo chạy cache (Cache Stampede). Thiết kế giải pháp khắc phục bằng cách sử dụng thuật toán Probabilistic Early Expiration (XFetch).
* **expected_key_points:**
  - id: KP6_1
    content: Bản chất Cache Avalanche vs Cache Stampede
    keypoint_weight: 0.5
    description: Cache Avalanche xảy ra khi hàng loạt key hết hạn cùng lúc làm sập DB. Cache Stampede xảy ra khi một key cực hot hết hạn, hàng ngàn request đồng thời đổ vào DB để tính toán lại giá trị đó.
  - id: KP6_2
    content: Khắc phục bằng thuật toán XFetch
    keypoint_weight: 0.5
    description: Tính toán xác suất hết hạn sớm ngẫu nhiên dựa trên thời gian đọc và hệ số beta: nếu xác suất đạt -> cho phép 1 luồng chạy ngầm tính lại dữ liệu trước khi key thực sự hết hạn, tránh nghẽn DB.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích nguyên lý hoạt động của thuật toán Redlock dùng để tạo khóa phân tán an toàn trên cụm Redis gồm nhiều master nodes độc lập.
* **expected_key_points:**
  - id: KP7_1
    content: Các bước thực hiện của Redlock
    keypoint_weight: 0.6
    description: Lấy thời gian hiện tại -> Gửi yêu cầu acquire lock kèm TTL ngắn đến tất cả N master nodes -> Tính thời gian thực hiện; nếu acquire thành công trên ít nhất (N/2 + 1) nodes và tổng thời gian nhỏ hơn TTL thì lock thành công.
  - id: KP7_2
    content: Cơ chế Giải phóng khóa (Unlock)
    keypoint_weight: 0.4
    description: Gửi lệnh giải phóng khóa tới tất cả các nodes trong cụm, bất kể node đó có báo acquire thành công trước đó hay không để tránh sót khóa.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống khóa phân tán chịu lỗi cao (Highly Available Distributed Lock Manager) hỗ trợ hàng triệu lượt khóa/mở khóa mỗi giây với độ trễ cực thấp (<1ms) và đảm bảo an toàn tuyệt đối khi xảy ra lỗi mạng phân mảnh.
* **expected_key_points:**
  - id: KP8_1
    content: Cơ chế lưu trữ trạng thái khóa trên RAM và Phân mảnh
    keypoint_weight: 0.5
    description: Sử dụng cụm Redis Cluster phân mảnh khóa theo Hash Slot để chia tải; sử dụng thuật toán đồng thuận Raft để quản lý metadata trạng thái.
  - id: KP8_2
    content: Cơ chế Fencing Token phòng ngừa Network Partition
    keypoint_weight: 0.5
    description: Mỗi lượt cấp khóa trả về một số hiệu tăng dần duy nhất (fencing token). Khi ứng dụng ghi xuống DB, DB kiểm tra token; nếu nhận token cũ hơn token hiện tại (do thread cũ bị lag mạng gửi lên), DB sẽ từ chối ghi.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế hệ thống Cache phân tán đa tầng (Multi-tier Caching: L1 Local Cache + L2 Redis Cache) cho ứng dụng tin tức lớn phục vụ hàng chục triệu người dùng hoạt động đồng thời, đảm bảo tính nhất quán dữ liệu cao giữa các tầng cache.
* **expected_key_points:**
  - id: KP9_1
    content: Thiết kế L1 Local Cache và L2 Redis Cache
    keypoint_weight: 0.5
    description: L1 Cache nằm trên bộ nhớ RAM của từng instance ứng dụng (như Guava/Caffeine), truy xuất trễ 0ms. L2 Cache nằm trên cụm Redis dùng chung cho toàn hệ thống.
  - id: KP9_2
    content: Đồng bộ hóa nhất quán qua cơ chế Pub/Sub
    keypoint_weight: 0.5
    description: Khi có cập nhật dữ liệu: sửa L2 Redis -> gửi thông báo qua Redis Pub/Sub hoặc Kafka -> tất cả các instances nhận thông báo và tự động xóa key tương ứng trong L1 Cache cục bộ của mình.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kiến trúc hệ thống phục vụ dữ liệu cấu hình động (Configuration Management System) có tính sẵn sàng cao, hỗ trợ đẩy cập nhật tức thời (real-time push) tới hàng ngàn microservices mà không làm quá tải cơ sở dữ liệu chính.
* **expected_key_points:**
  - id: KP10_1
    content: Kiến trúc lưu trữ cấu hình và phân phối
    keypoint_weight: 0.5
    description: Lưu trữ cấu hình trong DB quan hệ (PostgreSQL); đồng bộ và lập chỉ mục sang cụm etcd/ZooKeeper chuyên biệt cho dữ liệu cấu hình.
  - id: KP10_2
    content: Cơ chế Watcher và Long Polling
    keypoint_weight: 0.5
    description: Các microservices thiết lập kết nối Watcher (gRPC streaming) tới etcd để nhận thông báo đẩy tức thời khi cấu hình thay đổi; kết hợp fallback sang cơ chế Long Polling để tự động lấy lại cấu hình khi mất kết nối.

