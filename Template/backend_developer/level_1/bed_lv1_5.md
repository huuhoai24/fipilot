# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 1)

* **Role:** Backend Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong ngôn ngữ lập trình Backend, hãy phân biệt sự khác nhau cốt lõi về mặt quản lý bộ nhớ và hiệu năng giữa hai vùng nhớ: Stack và Heap.
* **expected_key_points:**
  - id: KP1_1
    content: Cơ chế cấp phát và giải phóng (Allocation & Vòng đời)
    keypoint_weight: 0.5
    description: Vùng nhớ Stack được quản lý tự động bởi CPU theo cơ chế LIFO (Last In First Out), dữ liệu tự giải phóng khi hàm kết thúc. Vùng nhớ Heap được cấp phát động (Dynamic Allocation), vòng đời do lập trình viên quản lý trực tiếp hoặc thông qua Garbage Collector giải phóng muộn.
  - id: KP1_2
    content: Loại dữ liệu lưu trữ và Tốc độ truy cập
    keypoint_weight: 0.5
    description: Stack lưu trữ các biến cục bộ (Local variables) và tham số hàm, dung lượng nhỏ, tốc độ truy cập cực nhanh. Heap lưu trữ các đối tượng phức tạp (Objects/Reference types), dung lượng lớn có thể co giãn, tốc độ truy cập chậm hơn do phải phân giải địa chỉ con trỏ.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong thiết kế cơ sở dữ liệu quan hệ, việc thiết lập trường khóa ngoại (Foreign Key) đóng vai trò logic gì và đảm bảo tính chất nào của dữ liệu?
* **expected_key_points:**
  - id: KP2_1
    content: Định nghĩa mối quan hệ logic giữa các bảng (Table Relationships)
    keypoint_weight: 0.5
    description: Khóa ngoại là một trường (hoặc tập hợp trường) trong một bảng dữ liệu trỏ đến trường khóa chính (Primary Key) của một bảng khác, nhằm thiết lập và ràng buộc mối quan hệ (1-n, n-n) giữa hai thực thể.
  - id: KP2_2
    content: Đảm bảo tính toàn vẹn tham chiếu (Referential Integrity)
    keypoint_weight: 0.5
    description: Ngăn chặn việc thêm các bản ghi có giá trị khóa ngoại không tồn tại ở bảng gốc, hoặc ngăn chặn việc xóa/sửa dữ liệu ở bảng gốc khi đang có bảng khác tham chiếu đến (trừ khi cấu hình CASCADE), giữ dữ liệu luôn đồng bộ thống nhất.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Giao thức mạng TCP (Transmission Control Protocol) và UDP (User Datagram Protocol) khác nhau như thế nào về cơ chế bắt tay kết nối và độ tin cậy?
* **expected_key_points:**
  - id: KP3_1
    content: Cơ chế hướng kết nối và tính tin cậy của TCP (Connection-oriented)
    keypoint_weight: 0.5
    description: TCP bắt buộc phải thiết lập kết nối trước khi truyền dữ liệu thông qua quá trình bắt tay 3 bước (3-way handshake). TCP đảm bảo dữ liệu truyền đi không bị mất mát, đúng thứ tự và có cơ chế kiểm soát lỗi/luồng (Reliable).
  - id: KP3_2
    content: Cơ chế không kết nối và tốc độ của UDP (Connectionless)
    keypoint_weight: 0.5
    description: UDP truyền dữ liệu trực tiếp mà không cần thiết lập kết nối trước (Connectionless). UDP không đảm bảo dữ liệu đến đích hay đúng thứ tự, đổi lại tốc độ truyền tải cực nhanh và tốn ít tài nguyên đường truyền, phù hợp cho streaming, gaming.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy phân biệt điểm khác biệt cốt lõi về mặt chức năng tính toán giữa hai kỹ thuật phân trang dữ liệu ở phía Database: Off-set Pagination và Cursor-based Pagination (Keyset Pagination).
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế nhảy cóc của Off-set Pagination và khuyết điểm hiệu năng
    keypoint_weight: 0.5
    description: Off-set sử dụng mệnh đề `LIMIT X OFFSET Y`. Database Engine bắt buộc phải quét và sắp xếp tuần tự toàn bộ $Y$ bản ghi trước đó rồi mới lấy ra $X$ bản ghi tiếp theo. Khi dữ liệu lớn ($Y$ lớn), tốc độ truy vấn sẽ tụt dốc nghiêm trọng và gặp lỗi lệch trang khi dữ liệu bị thêm/xóa đồng thời.
  - id: KP4_2
    content: Cơ chế trỏ chỉ mục của Cursor-based Pagination và ưu điểm
    keypoint_weight: 0.5
    description: Cursor-based sử dụng một con trỏ (thường là ID hoặc Timestamp của bản ghi cuối cùng của trang trước) kết hợp mệnh đề `WHERE ID > Cursor LIMIT X`. Database tìm thẳng đến vị trí con trỏ thông qua Index mà không cần quét lại dữ liệu cũ, giúp hiệu năng ổn định $O(1)$ bất kể độ sâu của trang và không bị trùng lặp dữ liệu.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong kiến trúc thiết kế API, cơ chế Cross-Origin Resource Sharing (CORS) là gì? Lỗi "CORS Error" ở trình duyệt xảy ra do nguyên nhân gì từ phía Backend?
* **expected_key_points:**
  - id: KP5_1
    content: Bản chất chính sách bảo mật CORS của trình duyệt
    keypoint_weight: 0.4
    description: CORS là cơ chế bảo mật dựa trên HTTP-header của trình duyệt nhằm cho phép hoặc ngăn chặn một trang web từ một nguồn (Origin - Protocol + Domain + Port) này được quyền truy cập tài nguyên của một nguồn khác.
  - id: KP5_2
    content: Nguyên nhân Backend thiếu cấu hình Response Header phù hợp
    keypoint_weight: 0.6
    description: Lỗi xảy ra khi mã Frontend gửi một request API lên Server ở domain khác, nhưng trong phản hồi trả về (HTTP Response), phía Backend không đính kèm hoặc cấu hình sai header `Access-Control-Allow-Origin` chứa domain của Frontend đó để cấp quyền truy cập.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy giải thích hiện tượng "N+1 Query Problem" thường gặp khi sử dụng các thư viện ánh xạ thực thể ORM (như Hibernate, Entity Framework, Sequelize) và nêu một giải pháp khắc phục.
* **expected_key_points:**
  - id: KP6_1
    content: Cơ chế phát sinh câu lệnh truy vấn lặp vòng lặp (Loop Query)
    keypoint_weight: 0.5
    description: Xảy ra khi ORM thực hiện 1 câu lệnh SQL ban đầu để lấy ra danh sách $N$ bản ghi cha, sau đó chạy thêm $N$ câu lệnh SQL độc lập bên trong vòng lặp để lấy dữ liệu liên quan của từng bản ghi con, gây quá tải và làm chậm Database (tổng cộng $N+1$ câu lệnh).
  - id: KP6_2
    content: Giải pháp gộp câu lệnh sử dụng Eager Loading (JOIN/In-clause)
    keypoint_weight: 0.5
    description: Cấu hình cho bộ ORM sử dụng chiến lược Eager Loading bằng cách ép sử dụng phép toán `JOIN` hoặc mệnh đề `IN` ngay trong câu lệnh đầu tiên để gom toàn bộ dữ liệu cha và con về trong 1 hoặc 2 câu lệnh SQL duy nhất.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi ứng dụng Backend cần xử lý đồng thời nhiều tác vụ I/O nặng (như gọi API bên thứ ba, đọc file dữ liệu lớn), mô hình Async/Await (Asynchronous Programming) tối ưu hóa tài nguyên hệ thống tốt hơn mô hình Multi-threading truyền thống như thế nào?
* **expected_key_points:**
  - id: KP7_1
    content: Khuyết điểm thắt nút cổ chai tốn RAM của Multi-threading truyền thống
    keypoint_weight: 0.5
    description: Mô hình truyền thống gán mỗi Request cho một Thread vật lý quản lý. Khi gặp tác vụ đợi I/O, Thread đó bị khóa cứng (Blocking), treo luồng lãng phí tài nguyên RAM/CPU và làm giới hạn dung lượng chịu tải của hệ thống.
  - id: KP7_2
    content: Cơ chế không chặn luồng (Non-blocking) nhờ Event Loop của Async/Await
    keypoint_weight: 0.5
    description: Async/Await sử dụng cơ chế Non-blocking I/O kết hợp hàng đợi sự kiện (Event Loop). Khi gặp tác vụ đợi I/O, luồng xử lý chính lập tức giải phóng để đi phục vụ request khác. Khi I/O hoàn thành, một sự kiện được bắn ngược lại để chạy tiếp callback, giúp 1 luồng đơn có thể xử lý hàng vạn kết nối đồng thời.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong kiến trúc vi dịch vụ (Microservices), lỗi nghẽn mạch hệ thống dây chuyền "Cascading Failure" là gì? Kỹ thuật "Circuit Breaker Pattern" hoạt động dựa trên ba trạng thái nào để bảo vệ hệ thống?
* **expected_key_points:**
  - id: KP8_1
    content: Bản chất lỗi sập dây chuyền (Cascading Failure)
    keypoint_weight: 0.4
    description: Xảy ra khi một dịch vụ nội bộ phía sau bị sập hoặc phản hồi quá chậm, làm nghẽn luồng và phình to tài nguyên chờ của các dịch vụ gọi nó ở phía trước, tạo thành hiệu ứng sụp đổ dây chuyền lan rộng khắp toàn bộ hệ thống.
  - id: KP8_2
    content: Ba trạng thái hoạt động: Closed, Open, và Half-Open
    keypoint_weight: 0.6
    description: - **Closed (Đóng mạch):** Trạng thái bình thường, request đi qua bình thường. Nếu tỷ lệ lỗi vượt ngưỡng, mạch chuyển sang Open.
                 - **Open (Ngắt mạch):** Chặn đứng và từ chối gọi tới service lỗi ngay lập tức, trả về lỗi nhanh (Fail-fast) để giải phóng tài nguyên. Sau một thời gian, mạch tự chuyển sang Half-Open.
                 - **Half-Open (Nửa đóng nửa mở):** Cho phép một lượng nhỏ request thử nghiệm đi qua. Nếu thành công, mạch quay về Closed (phục hồi); nếu tiếp tục lỗi, mạch lập tức quay lại Open.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích nguyên lý hoạt động kỹ thuật của kiến trúc lưu trữ dữ liệu "Log-Structured Merge-Tree" (LSM-Tree) và lý do tại sao nó đạt thông lượng ghi (Write Throughput) vượt trội hoàn toàn so với kiến trúc B-Tree trong các hệ thống Big Data.
* **expected_key_points:**
  - id: KP9_1
    content: Cơ chế ghi tuần tự thay vì ghi ngẫu nhiên (Sequential vs Random Writes)
    keypoint_weight: 0.4
    description: B-Tree thực hiện cập nhật dữ liệu trực tiếp trên các trang đĩa tại các vị trí rải rác, dẫn đến việc phải thực hiện các phép toán ghi ngẫu nhiên (Random Writes) rất chậm. LSM-Tree chuyển đổi mọi thao tác ghi thành phép ghi tuần tự nối đuôi liên tục (Sequential Writes) vào bộ nhớ nền, tăng tốc độ ghi lên hàng trăm lần.
  - id: KP9_2
    content: Quy trình ghi thông qua cấu trúc MemTable và SSTable
    keypoint_weight: 0.4
    description: Dữ liệu mới ghi vào sẽ được nạp trực tiếp vào một cấu trúc dữ liệu cây trên bộ nhớ RAM gọi là MemTable (đồng thời ghi vào file Log WAL để phòng sự cố). Khi MemTable đầy, nó sẽ được đóng băng và ghi súc (Flush) tuần tự xuống ổ đĩa cứng thành các file tĩnh đã sắp xếp thứ tự gọi là SSTable (Sorted String Table).
  - id: KP9_3
    content: Tiến trình dọn dẹp chạy ngầm Compaction
    keypoint_weight: 0.2
    description: Do dữ liệu được ghi nối đuôi liên tục nên sẽ tồn tại nhiều phiên bản cũ của cùng một key dữ liệu nằm rải rác trên các file SSTable. LSM-Tree sử dụng một tiến trình chạy ngầm gọi là Compaction để liên tục gộp, loại bỏ dữ liệu trùng lặp hoặc đã xóa và sắp xếp lại các file SSTable theo các phân tầng (Levels).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Khi triển khai kiến trúc Caching phân tán trên cụm nhiều server Redis, hãy phân tích nguyên lý hoạt động kỹ thuật của thuật toán định tuyến "Consistent Hashing" (Băm nhất quán) và giải pháp xử lý lỗi phân bổ không đều (Hotspot) của thuật toán này.
* **expected_key_points:**
  - id: KP10_1
    content: Lỗi mất dấu dữ liệu hàng loạt của phép toán băm Modulo truyền thống
    keypoint_weight: 0.4
    description: Phép toán băm Modulo truyền thống `$h(key) \pmod N$` phụ thuộc vào tổng số node $N$. Khi ta thêm hoặc bớt một node ($N$ thay đổi), vị trí băm của hầu hết các key cũ bị xáo trộn hoàn toàn, gây ra hiện tượng sập Cache Miss hàng loạt trên diện rộng.
  - id: KP10_2
    content: Nguyên lý ánh xạ không gian khóa lên vòng tròn logic (Hash Ring)
    keypoint_weight: 0.4
    description: Consistent Hashing băm cả Key dữ liệu lẫn Địa chỉ các Node về một không gian số thực lớn nằm trên một vòng tròn logic (Hash Ring). Vị trí lưu trữ của Key được xác định bằng cách chạy theo chiều kim đồng hồ từ điểm băm của key cho đến khi gặp Node đầu tiên. Khi thêm/bớt node, hệ thống chỉ cần chuyển dịch một phần nhỏ lượng dữ liệu nằm sát cạnh node đó mà không ảnh hưởng phần còn lại.
  - id: KP10_3
    content: Kỹ thuật sử dụng Node ảo (Virtual Nodes / Vnodes) để cân bằng tải
    keypoint_weight: 0.2
    description: Nếu cụm chỉ có ít node vật lý, chúng dễ phân bổ lệch trên vòng tròn, gây ra hiện tượng một server gánh quá nhiều dữ liệu (Hotspot Node). Thuật toán giải quyết bằng cách tạo ra nhiều Node ảo (Virtual Nodes) đại diện cho một node vật lý băm rải rác khắp vòng tròn để chia đều dữ liệu đầu vào.