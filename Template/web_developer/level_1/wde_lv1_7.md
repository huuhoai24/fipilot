# Bộ Câu Hỏi Phỏng Vấn Web Developer (Level 1) - Tập Đề Mới (18)

* **Role:** Web Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, thuộc tính `overflow: hidden` có tác dụng gì và tại sao nó lại được dùng để giải quyết vấn đề "clearfix"?
* **expected_key_points:**
  - id: KP1_1
    content: Cơ chế ẩn nội dung thừa
    keypoint_weight: 0.6
    description: `overflow: hidden` ẩn đi bất kỳ nội dung nào vượt quá giới hạn của vùng chứa (container).
  - id: KP1_2
    content: Giải quyết vấn đề float (clearfix)
    keypoint_weight: 0.4
    description: Nó tạo ra một "block formatting context" (BFC), khiến container tự động bao bọc các phần tử con đang sử dụng `float` mà không bị sập (collapsed height).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Trong JavaScript, sự khác biệt giữa `slice()` và `splice()` khi thao tác với mảng là gì?
* **expected_key_points:**
  - id: KP2_1
    content: Tính bất biến (Immutability)
    keypoint_weight: 0.5
    description: `slice()` trả về một mảng mới (không thay đổi mảng gốc). `splice()` thay đổi trực tiếp mảng gốc.
  - id: KP2_2
    content: Mục đích sử dụng
    keypoint_weight: 0.5
    description: `slice()` dùng để copy một phần mảng. `splice()` dùng để chèn, xóa hoặc thay thế các phần tử trong mảng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Thẻ `<noscript>` trong HTML dùng để làm gì và khi nào nó xuất hiện?
* **expected_key_points:**
  - id: KP3_1
    content: Nội dung dự phòng
    keypoint_weight: 0.5
    description: Chứa nội dung sẽ hiển thị cho người dùng khi trình duyệt của họ đã tắt JavaScript hoặc không hỗ trợ JavaScript.
  - id: KP3_2
    content: Tính năng fallback
    keypoint_weight: 0.5
    description: Cung cấp thông báo hướng dẫn hoặc nội dung thay thế để đảm bảo ứng dụng vẫn có giá trị cơ bản cho người dùng.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm "Hoisting" trong JavaScript và sự khác biệt giữa `var` và `let/const` trong trường hợp này?
* **expected_key_points:**
  - id: KP4_1
    content: Định nghĩa Hoisting
    keypoint_weight: 0.5
    description: Là cơ chế JavaScript đưa các khai báo lên đầu scope. `var` được khởi tạo là `undefined`.
  - id: KP4_2
    content: Temporal Dead Zone (TDZ)
    keypoint_weight: 0.5
    description: `let/const` cũng được hoist nhưng không được khởi tạo, dẫn đến lỗi `ReferenceError` nếu truy cập trước dòng khai báo.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, sự khác biệt giữa `useMemo` và `React.memo` là gì?
* **expected_key_points:**
  - id: KP5_1
    content: useMemo
    keypoint_weight: 0.5
    description: Là một Hook dùng để ghi nhớ kết quả của một phép tính toán phức tạp giữa các lần render.
  - id: KP5_2
    content: React.memo
    keypoint_weight: 0.5
    description: Là một Higher-Order Component (HOC) dùng để ghi nhớ (memoize) toàn bộ component, ngăn chặn re-render nếu props không thay đổi.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa `INNER JOIN` và `LEFT JOIN` trong truy vấn SQL?
* **expected_key_points:**
  - id: KP6_1
    content: INNER JOIN
    keypoint_weight: 0.5
    description: Chỉ trả về các hàng có dữ liệu khớp (matching) ở cả hai bảng được join.
  - id: KP6_2
    content: LEFT JOIN
    keypoint_weight: 0.5
    description: Trả về tất cả các hàng từ bảng bên trái, và các hàng khớp từ bảng bên phải. Nếu không khớp ở bảng phải, trả về NULL.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích mục đích của `Content Security Policy` (CSP) trong HTTP headers.
* **expected_key_points:**
  - id: KP7_1
    content: Chống tấn công XSS
    keypoint_weight: 0.5
    description: CSP giúp quản trị viên kiểm soát những nguồn nào (domain) được phép nạp script, style hoặc images, ngăn chặn việc chạy mã độc từ nguồn không tin cậy.
  - id: KP7_2
    content: Cơ chế thực thi
    keypoint_weight: 0.5
    description: Trình duyệt sẽ dựa vào header `Content-Security-Policy` để từ chối bất kỳ hành động nào vi phạm chính sách đã thiết lập.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích hiện tượng "Memory Leak" do không dọn dẹp `setTimeout` hoặc `setInterval` trong các SPA (Single Page Application).
* **expected_key_points:**
  - id: KP8_1
    content: Cơ chế giữ tham chiếu
    keypoint_weight: 0.5
    description: `setInterval` tạo một tham chiếu đến hàm callback và scope của component. Nếu không `clearInterval`, timer vẫn chạy ngầm giữ lại scope của component đó trong bộ nhớ.
  - id: KP8_2
    content: Hậu quả
    keypoint_weight: 0.5
    description: Component không thể được giải phóng (GC - Garbage Collected) dẫn đến tích lũy bộ nhớ bị chiếm dụng dần theo thời gian.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Sự khác biệt giữa "Concurrency" và "Parallelism" trong lập trình backend?
* **expected_key_points:**
  - id: KP9_1
    content: Concurrency
    keypoint_weight: 0.5
    description: Khả năng xử lý nhiều công việc bằng cách chia nhỏ và chuyển đổi qua lại giữa chúng (context switching) trên một luồng.
  - id: KP9_2
    content: Parallelism
    keypoint_weight: 0.5
    description: Thực hiện nhiều công việc cùng lúc thực sự trên nhiều lõi CPU, đòi hỏi phần cứng hỗ trợ.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** "Optimistic UI Updates" là gì và tại sao nó được coi là kỹ thuật cải thiện UX mạnh mẽ?
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Cập nhật giao diện ngay lập tức dựa trên dữ liệu phía client trước khi server xác nhận thành công.
  - id: KP10_2
    content: Lợi ích và rủi ro
    keypoint_weight: 0.5
    description: UX mượt mà (cảm giác không độ trễ), nhưng yêu cầu logic xử lý rollback (hoàn tác) nếu request gửi lên server thất bại.