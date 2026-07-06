# Bộ Câu Hỏi Phỏng Vấn Tester (Level 1)

* **Role:** Tester (QA/QC)
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt sự khác nhau cốt lõi giữa Kiểm thử chức năng (Functional Testing) và Kiểm thử phi chức năng (Non-functional Testing).
* **Đáp án mẫu:** - Kiểm thử chức năng: Kiểm tra xem hệ thống có hoạt động đúng theo yêu cầu nghiệp vụ đề ra hay không (hệ thống làm gì). Ví dụ: Kiểm tra tính năng đăng nhập, thanh toán.
  - Kiểm thử phi chức năng: Kiểm tra các đặc tính vận hành của hệ thống dưới các điều kiện cụ thể (hệ thống chạy như thế nào). Ví dụ: Kiểm tra hiệu năng (Performance), độ bảo mật (Security), độ tin cậy.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Một Test Case (Trường hợp kiểm thử) tiêu chuẩn thường bao gồm những thông tin cơ bản nào?
* **Đáp án mẫu:** Một Test Case tiêu chuẩn bao gồm: ID, Tên test case, Điều kiện tiên quyết (Pre-conditions), Các bước thực hiện (Steps), Dữ liệu kiểm thử (Test Data), Kết quả mong đợi (Expected Result) và Kết quả thực tế (Actual Result).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Sự khác biệt giữa Regression Testing (Kiểm thử hồi quy) và Re-testing (Kiểm thử lại) là gì?
* **Đáp án mẫu:** - Re-testing: Kiểm thử lại chính xác kịch bản lỗi trước đó sau khi lập trình viên báo đã sửa xong nhằm xác nhận lỗi đã được khắc phục.
  - Regression Testing: Kiểm thử lại các tính năng cũ không liên quan xung quanh khu vực vừa sửa đổi để đảm bảo code mới không làm hỏng hoặc gây lỗi cho các tính năng đang chạy ổn định.

---

## CÂU HỎI TRUNG BÌNH (4 câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Kỹ thuật thiết kế test case "Phân vùng tương đương" (Equivalence Partitioning) và "Phân tích giá trị biên" (Boundary Value Analysis) hoạt động như thế nào?
* **Đáp án mẫu:** - Phân vùng tương đương: Chia dữ liệu đầu vào thành các nhóm (vùng) có tính chất giống nhau, đại diện cho dữ liệu hợp lệ và không hợp lệ, rồi chọn một giá trị đại diện trong mỗi vùng để test.
  - Phân tích giá trị biên: Tập trung kiểm thử tại các điểm biên (giá trị tối thiểu, tối đa và các giá trị ngay sát biên) của các vùng tương đương, vì đây là nơi lập trình viên dễ viết sai điều kiện logic nhất.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Vòng đời của một lỗi phần mềm (Bug Life Cycle) diễn ra qua các trạng thái cơ bản nào từ khi phát hiện đến khi đóng lỗi?
* **Đáp án mẫu:** Quy trình gồm các trạng thái: **New** (Phát hiện lỗi) -> **Assigned** (Giao cho Developer sửa) -> **Open/In Progress** (Đang sửa) -> **Fixed** (Đã sửa xong và chuyển cho Tester) -> **Pending Test/Ready for Test** -> **Verified/Passed** (Tester xác nhận đã hết lỗi) -> **Closed** (Đóng lỗi). Nếu test lại vẫn lỗi thì chuyển thành **Reopened**.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong kiểm thử API, các mã trạng thái HTTP Response Code (HTTP Status Code) nhóm 2xx, 4xx, và 5xx đại diện cho điều gì?
* **Đáp án mẫu:** - 2xx (ví dụ 200 OK): Yêu cầu được xử lý thành công.
  - 4xx (ví dụ 404 Not Found, 401 Unauthorized): Lỗi từ phía Client (gửi sai định dạng, sai URL hoặc thiếu quyền truy cập).
  - 5xx (ví dụ 500 Internal Server Error): Lỗi phát sinh từ phía Server mặc dù request của client hợp lệ.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt giữa Khói kiểm thử (Smoke Testing) và Kiểm thử độ tỉnh táo (Sanity Testing) nằm ở thời điểm và mục đích áp dụng nào?
* **Đáp án mẫu:** - Smoke Testing: Thực hiện trên các bản build ban đầu hoặc build lớn để kiểm tra xem các chức năng cốt lõi nhất có hoạt động không, nhằm quyết định có tiếp tục nhận bản build để test chi tiết hay từ chối.
  - Sanity Testing: Thực hiện trên bản build nhỏ (chứa các cập nhật hoặc sửa lỗi nhỏ) để xác thực nhanh xem chức năng cụ thể đó hoạt động đúng logic hay không mà không cần test toàn bộ hệ thống.

---

## CÂU HỎI KHÓ (3 câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong Agile/Scrum, một định nghĩa hoàn thành "Definition of Done" (DoD) có vai trò gì đối với một Tester, và tại sao nó lại khác với Tiêu chí nghiệm thu (Acceptance Criteria)?
* **Đáp án mẫu:** - Định nghĩa hoàn thành (DoD): Là một checklist chung áp dụng cho **tất cả** các User Story trong Sprint (ví dụ: đã code xong, đã review, đã chạy test case pass 100%, đã deploy lên staging) để đảm bảo chất lượng tổng thể.
  - Acceptance Criteria: Là các điều kiện nghiệm thu riêng biệt mang tính nghiệp vụ được thiết lập cụ thể cho **từng** User Story riêng lẻ để kiểm tra tính năng đó có chạy đúng yêu cầu khách hàng hay không.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Khi kiểm thử phần mềm dựa trên kiến trúc Microservices, tại sao Integration Testing (Kiểm thử tích hợp) lại phức tạp hơn so với kiến trúc Monolith (Khối tập trung)? Tester cần chú ý điều gì?
* **Đáp án mẫu:** Phức tạp hơn vì các service nằm độc lập, giao tiếp với nhau qua mạng bằng API hoặc Message Broker thay vì gọi hàm nội bộ. Lỗi có thể xảy ra do mất kết nối mạng, độ trễ hoặc không đồng nhất về phiên bản API giữa các service. Tester cần chú ý kiểm thử các kịch bản lỗi mạng, timeout, tính toàn vẹn dữ liệu (Data consistency) và sử dụng Mock Service khi cần thiết.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Khi phát hiện một lỗi không thể tái hiện lại một cách liên tục (Intermittent/Flaky Bug), bạn sẽ xử lý và báo cáo lỗi này như thế nào để hỗ trợ Developer tốt nhất?
* **Đáp án mẫu:** Quy trình xử lý: 
  1. Thử nghiệm lại nhiều lần, thay đổi các biến số môi trường (trình duyệt, bộ nhớ, tốc độ mạng, dữ liệu test) để tìm ra quy luật hoặc điều kiện kích hoạt lỗi.
  2. Thu thập tối đa bằng chứng: Quay video màn hình, chụp ảnh log của trình duyệt (Console log, Network tab), log phía máy chủ (Server log) tại thời điểm xảy ra lỗi.
  3. Khi báo cáo (Log bug), ghi rõ mức độ tần suất xuất hiện (ví dụ: xuất hiện 2/10 lần), liệt kê chi tiết mọi thông tin môi trường và đính kèm đầy đủ file log để Developer khoanh vùng tìm nguyên nhân.