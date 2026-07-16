# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1) - Tập Đề Test Environment và SQL JOIN 3 bảng (8)

* **Role:** Tester
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Môi trường kiểm thử (Test Environment) là gì và tại sao nó cần được thiết lập độc lập với môi trường phát triển (Development Environment)?
* **expected_key_points:**
  - id: KP1_1
    content: Khái niệm Test Environment
    keypoint_weight: 0.5
    description: Là tập hợp phần cứng, phần mềm, mạng, dữ liệu và các cấu hình hệ thống được chuẩn bị để Tester thực thi các ca kiểm thử.
  - id: KP1_2
    content: Sự cần thiết của tính độc lập
    keypoint_weight: 0.5
    description: Tránh việc Developer đang sửa code làm thay đổi tính năng giữa chừng, đảm bảo dữ liệu test không bị nhiễu và kết quả kiểm thử được ổn định, chính xác.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Thế nào là kiểm thử chấp nhận người dùng (UAT - User Acceptance Testing) và ai là người thực hiện chính?
* **expected_key_points:**
  - id: KP2_1
    content: Mục đích của UAT
    keypoint_weight: 0.5
    description: Là giai đoạn kiểm thử cuối cùng trước khi bàn giao hệ thống, nhằm xác minh phần mềm đáp ứng đúng nhu cầu nghiệp vụ thực tế của người dùng.
  - id: KP2_2
    content: Đối tượng thực hiện chính
    keypoint_weight: 0.5
    description: Thực hiện bởi khách hàng, người dùng cuối (end-users) hoặc đại diện nghiệp vụ (Product Owner/Business Analyst), dưới sự hỗ trợ kỹ thuật của Tester.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trình bày cách kiểm tra phiên bản (version) hiện tại của một ứng dụng di động đang cài đặt và cách dọn dẹp bộ nhớ đệm (Cache/Data) của ứng dụng đó trên điện thoại Android/iOS.
* **expected_key_points:**
  - id: KP3_1
    content: Xem phiên bản ứng dụng
    keypoint_weight: 0.4
    description: Vào Cài đặt hệ thống (Settings) -> Quản lý ứng dụng -> chọn App và xem thông số phiên bản (Version); hoặc xem trực tiếp trong màn hình Settings nội bộ của App.
  - id: KP3_2
    content: Xóa bộ nhớ đệm (Cache)
    keypoint_weight: 0.6
    description: Trên Android: Cài đặt -> Ứng dụng -> Chọn App -> Lưu trữ -> chọn Xóa bộ nhớ đệm (Clear Cache). Trên iOS: gỡ cài đặt app cài lại, hoặc dùng tính năng dọn dẹp nội bộ app.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế các test case cơ bản cho tính năng đăng nhập ứng dụng thông qua dịch vụ bên thứ ba (Google OAuth / Facebook Single Sign-On).
* **expected_key_points:**
  - id: KP4_1
    content: Kiểm thử luồng đăng nhập thành công
    keypoint_weight: 0.5
    description: Chọn đăng nhập Google/Facebook -> hiển thị pop-up nhập thông tin -> cấp quyền thành công -> đăng nhập hệ thống và tạo tài khoản liên kết tự động.
  - id: KP4_2
    content: Kiểm thử hủy cấp quyền và bảo mật
    keypoint_weight: 0.5
    description: Kiểm tra nhấn Hủy (Cancel) giữa chừng; kiểm tra khi token đăng nhập Google/Facebook hết hạn; kiểm tra trường hợp tài khoản Google/Facebook bị khóa.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Viết câu lệnh SQL kết hợp 3 bảng sử dụng JOIN để lấy thông tin chi tiết: Mã đơn hàng (order_id), Tên khách hàng (customer_name), và Tên sản phẩm (product_name). Bảng liên kết gồm: Orders, Order_Details, Customers, Products.
* **expected_key_points:**
  - id: KP5_1
    content: Cú pháp kết hợp JOIN nhiều bảng chính xác
    keypoint_weight: 0.6
    description: Sử dụng nhiều mệnh đề JOIN liên tiếp (ví dụ: `FROM Orders JOIN Customers ON ... JOIN Order_Details ON ... JOIN Products ON ...`).
  - id: KP5_2
    content: Ràng buộc khóa ngoại hợp lý
    keypoint_weight: 0.4
    description: Đảm bảo các điều kiện ON trỏ đúng khóa chính và khóa ngoại của các bảng tương ứng.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế các test case cho tính năng xuất dữ liệu (Export) danh sách khách hàng ra file Excel (.xlsx) hỗ trợ dữ liệu lớn và font chữ tiếng Việt.
* **expected_key_points:**
  - id: KP6_1
    content: Kiểm tra định dạng và dữ liệu xuất ra
    keypoint_weight: 0.5
    description: Xác minh file tải về mở được bằng Microsoft Excel, hiển thị đúng các cột dữ liệu, không bị lỗi font chữ tiếng Việt (UTF-8), đúng định dạng số/ngày tháng.
  - id: KP6_2
    content: Kiểm thử hiệu năng xuất dữ liệu lớn
    keypoint_weight: 0.5
    description: Test xuất file với dữ liệu lớn (hàng chục ngàn dòng) xem có bị timeout API, tràn bộ nhớ server hoặc đơ trình duyệt client không.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt sự khác nhau giữa Re-testing (Kiểm thử lại) và Regression Testing (Kiểm thử hồi quy) về định nghĩa và phạm vi áp dụng.
* **expected_key_points:**
  - id: KP7_1
    content: Bản chất Re-testing
    keypoint_weight: 0.5
    description: Thực hiện kiểm thử lại chính xác kịch bản bị lỗi trước đó để xác minh xem bug cụ thể đó đã được sửa hoàn toàn hay chưa (chỉ tập trung vào test case fail).
  - id: KP7_2
    content: Bản chất Regression Testing
    keypoint_weight: 0.5
    description: Kiểm thử các vùng chức năng không đổi xung quanh bản sửa lỗi để đảm bảo việc sửa lỗi không vô tình làm hỏng các tính năng hoạt động ổn định trước đó.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế kịch bản kiểm thử cho hệ thống gợi ý sản phẩm (Recommendation System) dựa trên hành vi người dùng bằng thuật toán học máy hoặc phân tích lịch sử mua sắm.
* **expected_key_points:**
  - id: KP8_1
    content: Kiểm thử tính liên quan của gợi ý (Recommendation Relevance)
    keypoint_weight: 0.6
    description: Tạo lịch sử mua sắm giả lập cho User A (ví dụ mua đồ công nghệ) -> kiểm tra xem danh sách sản phẩm gợi ý hiển thị trên trang chủ có liên quan đến đồ công nghệ hay không.
  - id: KP8_2
    content: Kiểm thử biên và trường hợp đặc biệt
    keypoint_weight: 0.4
    description: Kiểm thử với User hoàn toàn mới (Cold Start - kiểm tra xem hệ thống hiển thị sản phẩm phổ biến/mặc định) và kiểm tra tốc độ phản hồi API gợi ý.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích nguyên nhân và cách kiểm thử lỗi memory leak (rò rỉ bộ nhớ) của ứng dụng web chạy liên tục trên trình duyệt trong nhiều ngày (Long-running test).
* **expected_key_points:**
  - id: KP9_1
    content: Nguyên nhân rò rỉ bộ nhớ ở Client-side
    keypoint_weight: 0.5
    description: Do các biến toàn cục không giải phóng, các bộ lắng nghe sự kiện (event listeners) không bị xóa khi hủy component, hoặc sử dụng thư viện bên thứ ba không giải phóng bộ nhớ.
  - id: KP9_2
    content: Phương pháp kiểm thử và phát hiện
    keypoint_weight: 0.5
    description: Dùng tab Memory trong DevTools chụp ảnh heap snapshot tại các mốc thời gian; thực hiện lặp đi lặp lại một hành động rồi so sánh các snapshot; nếu dung lượng Heap tăng đều và không giảm sau Garbage Collection thì có leak.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Kiểm thử bảo mật: Phát hiện lỗi SQL Injection dạng Blind SQL Injection bằng cách kiểm tra phản hồi thời gian (Time-based blind SQLi).
* **expected_key_points:**
  - id: KP10_1
    content: Khái niệm Time-based Blind SQL Injection
    keypoint_weight: 0.5
    description: Là kỹ thuật tấn công khi database không hiển thị lỗi trực tiếp ra màn hình, kẻ tấn công chèn các câu lệnh (như `sleep(5)`) để nhận biết kết quả đúng/sai dựa vào thời gian phản hồi của server.
  - id: KP10_2
    content: Cách thức kiểm thử thủ công
    keypoint_weight: 0.5
    description: Nhập chuỗi payload SQL Injection kèm hàm tạo độ trễ (ví dụ: `1' AND sleep(10)--`) vào ô input. Nếu trang web phản hồi chậm hơn đúng 10 giây so với bình thường, hệ thống dính lỗ hổng.

