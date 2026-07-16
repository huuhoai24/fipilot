# Bộ Câu Hỏi Phỏng Vấn Full Stack Developer (Level 1) - Tập Đề Mới (11)

* **Role:** Full Stack Developer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong CSS, `position: sticky` hoạt động như thế nào và sự khác biệt của nó với `fixed`?
* **expected_key_points:**
  - id: KP1_1
    content: Cơ chế của sticky
    keypoint_weight: 0.5
    description: Phần tử hoạt động như `relative` cho đến khi nó đạt đến ngưỡng scroll chỉ định, sau đó nó "dính" lại giống như `fixed` trong container chứa nó.
  - id: KP1_2
    content: Sự khác biệt với fixed
    keypoint_weight: 0.5
    description: `fixed` dính vào viewport (toàn màn hình), còn `sticky` chỉ dính trong phạm vi phần tử cha bao quanh nó.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Sự khác biệt giữa `let` và `const` trong JavaScript là gì? Khi nào nên ưu tiên dùng cái nào?
* **expected_key_points:**
  - id: KP2_1
    content: Khả năng gán lại
    keypoint_weight: 0.5
    description: `let` cho phép gán lại giá trị mới. `const` yêu cầu khởi tạo ngay và không cho phép gán lại biến sau đó.
  - id: KP2_2
    content: Quy tắc sử dụng
    keypoint_weight: 0.5
    description: Ưu tiên `const` mặc định để tăng tính an toàn, chỉ dùng `let` khi biết chắc chắn giá trị của biến sẽ thay đổi trong tương lai.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Mục đích của thẻ `<head>` trong tài liệu HTML là gì?
* **expected_key_points:**
  - id: KP3_1
    content: Chứa metadata
    keypoint_weight: 0.5
    description: Chứa các thông tin về trang như tiêu đề (title), bộ mã hóa ký tự (charset), mô tả (description) và các đường dẫn external (CSS, scripts).
  - id: KP3_2
    content: Không hiển thị nội dung
    keypoint_weight: 0.5
    description: Nội dung trong `<head>` không hiển thị trực tiếp trên trình duyệt mà phục vụ trình duyệt, công cụ tìm kiếm và các thư viện hỗ trợ.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong React, sự khác biệt giữa `useEffect` và `useLayoutEffect` là gì?
* **expected_key_points:**
  - id: KP4_1
    content: Thời điểm thực thi
    keypoint_weight: 0.5
    description: `useEffect` chạy bất đồng bộ sau khi render. `useLayoutEffect` chạy đồng bộ ngay sau khi DOM được cập nhật nhưng trước khi trình duyệt vẽ lại (paint).
  - id: KP4_2
    content: Khi nào dùng useLayoutEffect
    keypoint_weight: 0.5
    description: Dùng khi cần đo đạc DOM hoặc thay đổi DOM trực tiếp mà không muốn người dùng thấy hiện tượng "nháy" (flickering) giao diện.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích hiện tượng SQL Injection và cách khắc phục.
* **expected_key_points:**
  - id: KP5_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Kẻ tấn công chèn mã SQL độc hại vào input của người dùng để đánh lừa ứng dụng thực thi các câu lệnh không mong muốn trên DB.
  - id: KP5_2
    content: Cách khắc phục
    keypoint_weight: 0.5
    description: Luôn sử dụng "Prepared Statements" (Parameterized Queries) để tách biệt dữ liệu khỏi câu lệnh SQL gốc.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong HTTP, `301 Moved Permanently` và `302 Found` khác nhau như thế nào về mặt SEO?
* **expected_key_points:**
  - id: KP6_1
    content: 301 (Di chuyển vĩnh viễn)
    keypoint_weight: 0.5
    description: Báo hiệu cho các công cụ tìm kiếm chuyển quyền lợi SEO (link equity) từ URL cũ sang URL mới vĩnh viễn.
  - id: KP6_2
    content: 302 (Di chuyển tạm thời)
    keypoint_weight: 0.5
    description: Báo hiệu cho công cụ tìm kiếm rằng URL cũ vẫn sẽ được dùng lại trong tương lai, không chuyển quyền lợi SEO vĩnh viễn.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Tại sao nên dùng `async/await` thay cho `.then()` trong việc xử lý Promise?
* **expected_key_points:**
  - id: KP7_1
    content: Tính dễ đọc (Readability)
    keypoint_weight: 0.5
    description: Làm cho code bất đồng bộ trông giống như code đồng bộ tuần tự, dễ hiểu và dễ theo dõi luồng xử lý.
  - id: KP7_2
    content: Quản lý lỗi
    keypoint_weight: 0.5
    description: Cho phép sử dụng `try/catch` chuẩn để bắt lỗi cho cả logic đồng bộ và bất đồng bộ, thay vì phải xử lý `.catch()` ở từng tầng.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Giải thích khái niệm "Event Delegation" và tại sao nó lại tối ưu hiệu năng?
* **expected_key_points:**
  - id: KP8_1
    content: Định nghĩa
    keypoint_weight: 0.5
    description: Thay vì gán event listener cho từng phần tử con, ta gán một listener duy nhất vào phần tử cha và tận dụng "Event Bubbling" để xử lý sự kiện cho các con.
  - id: KP8_2
    content: Lợi ích
    keypoint_weight: 0.5
    description: Giảm đáng kể số lượng event listener trong bộ nhớ và không cần gán lại listener khi thêm các phần tử con mới vào DOM.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Cơ chế "Database Transaction Isolation Levels" - Mức Read Uncommitted gây ra lỗi gì?
* **expected_key_points:**
  - id: KP9_1
    content: Định nghĩa Read Uncommitted
    keypoint_weight: 0.5
    description: Mức thấp nhất, cho phép đọc dữ liệu đang thay đổi của giao dịch khác dù giao dịch đó chưa hoàn tất (commit).
  - id: KP9_2
    content: Lỗi Dirty Read
    keypoint_weight: 0.5
    description: Dẫn đến "Dirty Read": ứng dụng đọc phải dữ liệu rác (nếu giao dịch kia rollback thì dữ liệu đã đọc là sai lệch hoàn toàn).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Khái niệm "Hydration" và lý do tại sao nó là điểm yếu về hiệu năng (Performance) trong các SSR Framework?
* **expected_key_points:**
  - id: KP10_1
    content: Bản chất Hydration
    keypoint_weight: 0.5
    description: Sau khi server gửi HTML tĩnh, trình duyệt phải tải toàn bộ Bundle JS và chạy lại để "gắn" lại các event handler và state.
  - id: KP10_2
    content: Vấn đề hiệu năng
    keypoint_weight: 0.5
    description: Quá trình này khóa Main Thread của trình duyệt. Nếu Bundle JS lớn, người dùng không thể tương tác với trang (TTI - Time to Interactive) dù trang đã hiển thị nội dung.