# Bộ Câu Hỏi Phỏng Vấn Business Analyst (Level 1)

* **Role:** Business Analyst
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong quản lý yêu cầu phần mềm, hãy phân biệt sự khác nhau cốt lõi về mặt mục đích và đối tượng độc giả giữa hai loại tài liệu: BRD (Business Requirement Document) và SRS (Software Requirement Specification).
* **expected_key_points:**
  - id: KP1_1
    content: Mục đích và đối tượng của tài liệu BRD
    keypoint_weight: 0.5
    description: BRD tập trung vào mục tiêu kinh doanh chiến lược cao cấp (Cái gì - What và Tại sao - Why). Đối tượng độc giả chính là khách hàng, quản lý cấp cao (Stakeholders) và PM; tài liệu sử dụng ngôn ngữ kinh doanh, không mang tính kỹ thuật.
  - id: KP1_2
    content: Mục đích và đối tượng của tài liệu SRS
    keypoint_weight: 0.5
    description: SRS tập trung vào chi tiết kỹ thuật hệ thống, cách thức phần mềm vận hành để đáp ứng BRD (Như thế nào - How). Đối tượng độc giả chính là đội ngũ phát triển (Developers) và kiểm thử (Testers); tài liệu sử dụng ngôn ngữ kỹ thuật, ca sử dụng (Use Cases), và các ràng buộc hệ thống.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt điểm khác nhau cơ bản giữa Functional Requirements (Yêu cầu chức năng) và Non-functional Requirements (Yêu cầu phi chức năng) của một hệ thống phần mềm. Nêu ví dụ minh họa cho từng loại.
* **expected_key_points:**
  - id: KP2_1
    content: Bản chất và ví dụ của Functional Requirements
    keypoint_weight: 0.5
    description: Là những yêu cầu định nghĩa trực tiếp các tính năng hành vi cụ thể mà hệ thống phần mềm bắt buộc phải thực hiện được cho người dùng (Hệ thống làm được gì). Ví dụ: Chức năng đăng nhập bằng OTP, chức năng thanh toán qua ví điện tử.
  - id: KP2_2
    content: Bản chất và ví dụ của Non-functional Requirements
    keypoint_weight: 0.5
    description: Là những yêu cầu quy định về đặc tính chất lượng, tiêu chuẩn vận hành và ràng buộc kỹ thuật của hệ thống (Hệ thống chạy mượt/an toàn ra sao). Ví dụ: Hệ thống phải chịu tải 10,000 người dùng đồng thời; thời gian phản hồi API phải dưới 2 giây; dữ liệu mật khẩu phải được mã hóa.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong mô hình Agile/Scrum, cấu trúc chuẩn của một "User Story" thường bao gồm những thành phần nào và mục đích của "Acceptance Criteria" (Tiêu chí nghiệm thu) là gì?
* **expected_key_points:**
  - id: KP3_1
    content: Cấu trúc 3 thành phần chuẩn của một User Story
    keypoint_weight: 0.5
    description: Viết theo format chuẩn: "As a [Role], I want to [Action], So that [Benefit]" (Với vai trò là..., Tôi muốn..., Để...).
  - id: KP3_2
    content: Mục đích cốt lõi của Acceptance Criteria
    keypoint_weight: 0.5
    description: Định nghĩa ranh giới và các điều kiện bắt buộc mà User Story phải thỏa mãn để được coi là hoàn thành (Done). Làm căn cứ để Developer viết code, Tester thiết kế test case và khách hàng nghiệm thu tính năng.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi tiếp nhận một dự án mới từ khách hàng, quy trình khơi gợi yêu cầu (Requirement Elicitation) của một BA thường diễn ra qua các bước logic nào để đảm bảo không bỏ sót thông tin?
* **expected_key_points:**
  - id: KP4_1
    content: Giai đoạn chuẩn bị nghiên cứu (Preparation)
    keypoint_weight: 0.3
    description: Xác định danh sách các bên liên quan (Stakeholders), nghiên cứu hệ thống hiện tại (As-is) và lựa chọn phương pháp khơi gợi phù hợp (Interview, Workshop, Survey).
  - id: KP4_2
    content: Giai đoạn thực hiện khơi gợi tương tác (Execution)
    keypoint_weight: 0.4
    description: Trực tiếp trao đổi, thảo luận hoặc quan sát người dùng để thu thập các nhu cầu, mong muốn và các bài toán khó khăn thực tế của họ.
  - id: KP4_3
    content: Giai đoạn xác nhận và kiểm chứng (Confirmation/Validation)
    keypoint_weight: 0.3
    description: Tổng hợp thông tin thu được, viết tài liệu sơ bộ và họp lại với khách hàng để rà soát, xác nhận tính chính xác và thống nhất lại những điểm hiểu lầm (Sign-off).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Kỹ thuật phân tích "S.M.A.R.T" được áp dụng như thế nào khi thiết lập các yêu cầu phần mềm để đảm bảo tính khả thi của dự án?
* **expected_key_points:**
  - id: KP5_1
    content: Giải thích ý nghĩa của S - M - A (Specific, Measurable, Actionable/Attainable)
    keypoint_weight: 0.5
    description: - Specific: Yêu cầu phải cụ thể, rõ ràng, không gây mơ hồ.
                 - Measurable: Yêu cầu phải đo lường được (bằng số liệu, chỉ số kỹ thuật).
                 - Actionable/Attainable: Yêu cầu phải có tính khả thi trong việc thực thi dựa trên nguồn lực hiện tại.
  - id: KP5_2
    content: Giải thích ý nghĩa của R - T (Relevant, Time-bound)
    keypoint_weight: 0.5
    description: - Relevant: Yêu cầu phải liên quan trực tiếp và phục vụ cho mục tiêu kinh doanh cốt lõi của dự án.
                 - Time-bound: Yêu cầu phải có giới hạn hoặc mốc thời gian hoàn thành rõ ràng.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong kỹ thuật mô hình hóa quy trình (Process Modeling), việc vẽ sơ đồ luồng công việc (Workflow/BPMN) mang lại lợi ích gì cho đội ngũ phát triển và khái niệm "Swimlane" (Làn bơi) dùng để biểu thị điều gì?
* **expected_key_points:**
  - id: KP6_1
    content: Lợi ích trực quan hóa quy trình nghiệp vụ hệ thống
    keypoint_weight: 0.5
    description: Giúp chuyển đổi các luồng nghiệp vụ chữ viết phức tạp thành sơ đồ hình ảnh trực quan, giúp Dev và Test hiểu rõ luồng đi của dữ liệu, các điểm rẽ nhánh điều kiện và thứ tự thực hiện các bước.
  - id: KP6_2
    content: Ý nghĩa phân định trách nhiệm của Swimlane
    keypoint_weight: 0.5
    description: Swimlane (các làn phân cách theo chiều ngang hoặc dọc) dùng để đại diện và phân định rõ ràng vai trò, phòng ban hoặc hệ thống nào chịu trách nhiệm thực hiện hành động cụ thể đó trong quy trình tổng thể.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giai đoạn kiểm thử nghiệm thu người dùng (User Acceptance Testing - UAT) đóng vai trò gì trong vòng đời dự án? BA có vai trò kỹ thuật gì trong giai đoạn này?
* **expected_key_points:**
  - id: KP7_1
    content: Mục đích xác nhận sản phẩm của giai đoạn UAT
    keypoint_weight: 0.5
    description: Là giai đoạn cuối cùng để người dùng cuối hoặc khách hàng trực tiếp kiểm thử sản phẩm thực tế nhằm xác nhận phần mềm chạy đúng theo nhu cầu nghiệp vụ thực tế, trước khi đồng ý nghiệm thu và deploy lên môi trường Production.
  - id: KP7_2
    content: Vai trò cầu nối hướng dẫn và quản lý phản hồi của BA
    keypoint_weight: 0.5
    description: BA đóng vai trò chuẩn bị kịch bản test nghiệm thu (UAT Test Cases/Scenarios), hỗ trợ hướng dẫn khách hàng test, và tiếp nhận các phản hồi về lỗi hoặc thay đổi (Change Requests) để phân loại, làm rõ với đội Dev.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Khi dự án đang trong giai đoạn phát triển (Development), khách hàng đột ngột đưa ra một yêu cầu thay đổi tính năng (Change Request) lớn. Hãy mô tả quy trình phân tích tác động (Impact Analysis) mà một BA cần thực hiện để xử lý tình huống này.
* **expected_key_points:**
  - id: KP8_1
    content: Đánh giá mức độ ảnh hưởng đến hệ thống và các yêu cầu hiện tại
    keypoint_weight: 0.4
    description: BA cần rà soát lại ma trận truy vết yêu cầu (Traceability Matrix) để xem tính năng thay đổi này sẽ làm ảnh hưởng, mâu thuẫn hay phá vỡ các chức năng cũ nào đang chạy ổn định của hệ thống.
  - id: KP8_2
    content: Phối hợp đánh giá tài nguyên với PM và Tech Lead
    keypoint_weight: 0.4
    description: Làm việc với Tech Lead để ước lượng chi phí viết lại code (Code refactoring) và làm việc với PM để tính toán lại tác động đến tiến độ dự án (Timeline), ngân sách (Budget) và nguồn lực con người.
  - id: KP8_3
    content: Đưa ra giải pháp lựa chọn và thương lượng với khách hàng
    keypoint_weight: 0.2
    description: Trình bày cho khách hàng các rủi ro, chi phí của việc thay đổi, từ đó đề xuất các phương án: làm ngay trong sprint hiện tại (nếu chịu tăng budget/timeline), hoặc dời sang phase sau của dự án (Backlog).

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong phân tích hệ thống kỹ thuật, sơ đồ Use Case Diagram (UML) và sơ đồ Data Flow Diagram (DFD) khác nhau như thế nào về mặt bản chất logic biểu diễn hệ thống?
* **expected_key_points:**
  - id: KP9_1
    content: Bản chất tương tác hành vi của Use Case Diagram
    keypoint_weight: 0.5
    description: Use Case Diagram tập trung biểu diễn các tương tác chức năng bên ngoài giữa các tác nhân (Actors - người dùng hoặc hệ thống khác) với các hành vi nghiệp vụ của hệ thống, không thể hiện thứ tự thời gian hay cách dòng dữ liệu di chuyển bên trong.
  - id: KP9_2
    content: Bản chất dòng chảy và biến đổi dữ liệu của DFD
    keypoint_weight: 0.5
    description: DFD tập trung biểu diễn kiến trúc luồng dữ liệu di chuyển xuyên suốt bên trong hệ thống (Dữ liệu đi từ đâu, qua tiến trình nào biến đổi, và lưu trữ vào kho dữ liệu nào - Data Stores). DFD không quan tâm đến giao diện người dùng hay hành vi của Actor.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Hãy giải thích khái niệm Ma trận truy vết yêu cầu (Requirements Traceability Matrix - RTM) và lý do tại sao cấu trúc này lại là công cụ sinh tử để kiểm soát phạm vi dự án (Scope Creep) khi dự án phình to?
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa cơ chế liên kết hai chiều của ma trận RTM
    keypoint_weight: 0.4
    description: RTM là bảng biểu dùng để liên kết theo hai chiều (Forward và Backward Tracking) từ Mục tiêu kinh doanh ban đầu -> Yêu cầu chi tiết chức năng -> Các task thiết kế/Dev code -> Kịch bản kiểm thử (Test Cases) tương ứng.
  - id: KP10_2
    content: Vai trò đảm bảo độ bao phủ yêu cầu (Requirement Coverage)
    keypoint_weight: 0.3
    description: Đảm bảo không có bất kỳ yêu cầu nào của khách hàng bị bỏ sót trong quá trình Dev code và kiểm thử, đồng thời kiểm tra xem mọi dòng code viết ra đều phục vụ cho một yêu cầu hợp lệ.
  - id: KP10_3
    content: Kiểm soát hiện tượng phình to phạm vi (Scope Creep)
    keypoint_weight: 0.3
    description: Khi dự án phình to, RTM giúp BA phát hiện ngay các tính năng "vô danh" do Dev tự ý thêm vào hoặc do khách hàng đưa vào mà không nằm trong phạm vi BRD ban đầu đã thỏa thuận, làm căn cứ từ chối hoặc tính thêm chi phí.