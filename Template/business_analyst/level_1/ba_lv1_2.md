# Bộ Câu Hỏi Phỏng Vấn Business Analyst (Level 1)

* **Role:** Business Analyst
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong mô hình Agile/Scrum, một "User Story" thường được viết theo cấu trúc chuẩn nào? Hãy giải thích ý nghĩa và mục đích sử dụng cốt lõi của thành phần "Acceptance Criteria" (Tiêu chí nghiệm thu) đi kèm với User Story đó.
* **expected_key_points:**
  - id: KP1_1
    content: Cấu trúc ba thành phần của một User Story
    keypoint_weight: 0.4
    description: Phải nêu rõ cấu trúc định dạng chuẩn: "As a [Role], I want to [Action], So that [Benefit/Value]" (Với vai trò là..., Tôi muốn..., Để...).
  - id: KP1_2
    content: Định nghĩa ranh giới hoàn thành tính năng của Acceptance Criteria
    keypoint_weight: 0.3
    description: Acceptance Criteria quy định các điều kiện logic, tiêu chuẩn bắt buộc mà tính năng phải đáp ứng để được coi là hoàn thành (Done), giúp ngăn chặn việc phình to phạm vi yêu cầu (Scope Creep).
  - id: KP1_3
    content: Làm căn cứ kỹ thuật cho đội ngũ Development và Testing
    keypoint_weight: 0.3
    description: Cung cấp tiêu chuẩn rõ ràng giúp lập trình viên (Developer) viết code chính xác và giúp kiểm thử viên (Tester) thiết kế kịch bản kiểm thử (Test Cases), đồng thời làm cơ sở nghiệm thu cuối cùng với khách hàng.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt sự khác nhau cốt lõi về mặt mục đích sử dụng và đối tượng độc giả hướng tới của hai loại tài liệu: BRD (Business Requirement Document) và SRS (Software Requirement Specification).
* **expected_key_points:**
  - id: KP2_1
    content: Bản chất kinh doanh chiến lược của tài liệu BRD
    keypoint_weight: 0.5
    description: BRD tập trung vào mục tiêu, nhu cầu kinh doanh và kỳ vọng của doanh nghiệp (Cái gì - What và Tại sao - Why). Đối tượng độc giả chính là khách hàng, nhà đầu tư, ban quản lý cấp cao (Stakeholders) và Quản trị dự án (PM); tài liệu sử dụng ngôn ngữ kinh doanh phi kỹ thuật.
  - id: KP2_2
    content: Bản chất đặc tả kỹ thuật hệ thống của tài liệu SRS
    keypoint_weight: 0.5
    description: SRS tập trung vào chi tiết chức năng, phi chức năng và giao diện của phần mềm cần xây dựng để đáp ứng mục tiêu kinh doanh (Như thế nào - How). Đối tượng độc giả chính là đội ngũ phát triển (Developers) và kiểm thử (Testers); tài liệu sử dụng ngôn ngữ kỹ thuật logic, các ca sử dụng (Use Cases) và sơ đồ luồng.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy định nghĩa thế nào là Functional Requirements (Yêu cầu chức năng) và Non-functional Requirements (Yêu cầu phi chức năng). Nêu một ví dụ thực tế cho mỗi loại.
* **expected_key_points:**
  - id: KP3_1
    content: Khái niệm hành vi hệ thống của Functional Requirements
    keypoint_weight: 0.5
    description: Định nghĩa trực tiếp những tính năng, hành động xử lý cụ thể mà hệ thống phần mềm phải thực hiện cho người dùng (Hệ thống làm được gì). Ví dụ: Chức năng gửi mã OTP qua SMS, chức năng xuất báo cáo file Excel.
  - id: KP3_2
    content: Khái niệm đặc tính vận hành của Non-functional Requirements
    keypoint_weight: 0.5
    description: Quy định các tiêu chuẩn chất lượng, ràng buộc kỹ thuật và môi trường vận hành của hệ thống (Hệ thống hoạt động tốt ra sao). Ví dụ: Hệ thống phải phản hồi request dưới 1.5 giây; dữ liệu thẻ tín dụng phải được mã hóa chuẩn mã AES-256; hệ thống đạt tính sẵn sàng 99.9%.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi bắt đầu một dự án phần mềm mới, quy trình khơi gợi yêu cầu (Requirement Elicitation) của một BA thường diễn ra qua những giai đoạn logic nào để đảm bảo thu thập đầy đủ thông tin?
* **expected_key_points:**
  - id: KP4_1
    content: Giai đoạn chuẩn bị lập kế hoạch (Preparation)
    keypoint_weight: 0.3
    description: Xác định các bên liên quan (Stakeholders) cần làm việc, tìm hiểu tổng quan về nghiệp vụ hiện tại (As-is), và lựa chọn phương pháp khơi gợi phù hợp (Phỏng vấn - Interview, Thảo luận nhóm - Workshop, Khảo sát - Survey).
  - id: KP4_2
    content: Giai đoạn tương tác thu thập thông tin (Execution)
    keypoint_weight: 0.4
    description: Trực tiếp tiến hành trao đổi, đặt câu hỏi hoặc quan sát người dùng thao tác để ghi nhận các nhu cầu, mong muốn thô, và những rào cản nghiệp vụ họ đang gặp phải.
  - id: KP4_3
    content: Giai đoạn tổng hợp và xác nhận lại (Confirmation/Validation)
    keypoint_weight: 0.3
    description: Phân tích thông tin thu được, chuyển hóa thành tài liệu sơ bộ và tổ chức họp rà soát với khách hàng nhằm đính chính các điểm hiểu lầm, thống nhất phạm vi và ký biên bản xác nhận (Sign-off).

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong mô hình hóa quy trình nghiệp vụ (Process Modeling), việc xây dựng sơ đồ luồng công việc (Workflow/BPMN) đem lại lợi ích gì? Thành phần "Swimlane" (Làn bơi) trong sơ đồ dùng để biểu thị nội dung gì?
* **expected_key_points:**
  - id: KP5_1
    content: Lợi ích trực quan hóa và đồng nhất tư duy luồng nghiệp vụ
    keypoint_weight: 0.5
    description: Biến đổi các quy trình nghiệp vụ dài dòng bằng chữ thành sơ đồ hình ảnh trực quan, giúp tất cả các bên (Khách hàng, Dev, Test) hiểu chung một cách vận hành của hệ thống, nhận diện rõ các điểm rẽ nhánh điều kiện và luồng dữ liệu.
  - id: KP5_2
    content: Ý nghĩa phân định trách nhiệm thao tác của Swimlane
    keypoint_weight: 0.5
    description: Swimlane (các làn phân cách dọc hoặc ngang) đại diện cho từng vai trò người dùng (Actor), phòng ban chức năng hoặc hệ thống công nghệ thông tin cụ thể, dùng để chỉ rõ ai/hệ thống nào chịu trách nhiệm thực hiện hành động đó trong quy trình tổng thể.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Kỹ thuật phân tích tiêu chuẩn "S.M.A.R.T" được một Business Analyst áp dụng như thế nào khi thiết lập và viết các yêu cầu phần mềm?
* **expected_key_points:**
  - id: KP6_1
    content: Ý nghĩa các chữ cái S - M - A (Specific, Measurable, Achievable)
    keypoint_weight: 0.5
    description: - Specific: Yêu cầu phải rõ ràng, cụ thể, đơn nghĩa.
                 - Measurable: Yêu cầu phải đo lường được bằng các chỉ số kỹ thuật hoặc tiêu chí nghiệm thu định lượng.
                 - Achievable/Attainable: Yêu cầu phải có tính khả thi, nằm trong năng lực kỹ thuật và nguồn lực dự án.
  - id: KP6_2
    content: Ý nghĩa các chữ cái R - T (Relevant, Time-bound)
    keypoint_weight: 0.5
    description: - Relevant: Yêu cầu phải thực tế và đóng góp trực tiếp vào mục tiêu kinh doanh cốt lõi của sản phẩm.
                 - Time-bound: Yêu cầu phải xác định rõ mốc thời gian hoặc phạm vi sprint/phase cần hoàn thành.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Giai đoạn Kiểm thử nghiệm thu người dùng (User Acceptance Testing - UAT) đóng vai trò gì trong vòng đời phát triển phần mềm và trách nhiệm của BA trong giai đoạn này là gì?
* **expected_key_points:**
  - id: KP7_1
    content: Mục đích xác nhận tính sẵn sàng của sản phẩm trong giai đoạn UAT
    keypoint_weight: 0.5
    description: UAT là bước kiểm thử cuối cùng do người dùng cuối hoặc đại diện khách hàng thực hiện nhằm xác định phần mềm đã chạy đúng và đủ theo các kịch bản nghiệp vụ thực tế hay chưa, làm cơ sở để đồng ý đưa hệ thống lên môi trường thật (Go-live).
  - id: KP7_2
    content: Vai trò cầu nối hướng dẫn và quản lý lỗi nghiệm thu của BA
    keypoint_weight: 0.5
    description: BA chịu trách nhiệm thiết lập bộ kịch bản kiểm thử nghiệm thu (UAT Test Scenarios), hướng dẫn và hỗ trợ người dùng thực hiện test, thu thập và phân loại các phản hồi về lỗi phát sinh hoặc yêu cầu thay đổi (Change Requests) để chuyển giao về cho đội Dev.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Khi dự án đang trong giai đoạn lập trình (Development), khách hàng đột ngột yêu cầu thay đổi một tính năng lớn (Change Request). Hãy trình bày quy trình phân tích tác động (Impact Analysis) mà một BA cần thực hiện để xử lý tình huống này.
* **expected_key_points:**
  - id: KP8_1
    content: Rà soát liên kết ma trận truy vết yêu cầu (Traceability Matrix)
    keypoint_weight: 0.4
    description: BA sử dụng ma trận truy vết để kiểm tra xem việc thay đổi tính năng này sẽ tác động dây chuyền, gây mâu thuẫn logic hoặc làm ảnh hưởng trực tiếp đến những yêu cầu nghiệp vụ, ca sử dụng hay chức năng nào hiện tại hệ thống đang xây dựng.
  - id: KP8_2
    content: Phối hợp đánh giá tài nguyên và rủi ro kỹ thuật (Triple Constraints)
    keypoint_weight: 0.4
    description: Làm việc với Tech Lead để ước lượng công sức viết lại code/kiến trúc dữ liệu, phối hợp với Project Manager (PM) để tính toán lại mức độ ảnh hưởng đến tiến độ (Timeline), chi phí tài chính (Budget) và chất lượng chung của dự án.
  - id: KP8_3
    content: Đàm phán phương án triển khai với khách hàng
    keypoint_weight: 0.2
    description: Trình bày báo cáo Impact Analysis một cách khách quan cho khách hàng, đưa ra các đề xuất lựa chọn: Chấp nhận dời ngày Go-live/Tăng chi phí để làm ngay, hoặc đưa yêu cầu thay đổi này vào danh sách Product Backlog để xử lý ở giai đoạn sau (Phase sau).

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong phân tích và thiết kế hệ thống, sơ đồ Use Case Diagram (UML) và sơ đồ Data Flow Diagram (DFD) khác nhau như thế nào về mặt bản chất logic biểu diễn?
* **expected_key_points:**
  - id: KP9_1
    content: Bản chất biểu diễn tương tác chức năng của Use Case Diagram
    keypoint_weight: 0.5
    description: Use Case Diagram tiếp cận theo hướng hành vi hệ thống, tập trung mô tả mối quan hệ tương tác giữa các tác nhân bên ngoài (Actors - người dùng hoặc hệ thống ngoại vi) với các tính năng chức năng của hệ thống; sơ đồ không thể hiện thứ tự thời gian hay cách thức dữ liệu dịch chuyển.
  - id: KP9_2
    content: Bản chất biểu diễn dòng chảy và biến đổi thông tin của DFD
    keypoint_weight: 0.5
    description: DFD tiếp cận theo hướng cấu trúc dữ liệu, tập trung mô tả cách thức thông tin di chuyển xuyên suốt qua các tiến trình xử lý bên trong (Processes), nguồn gốc dữ liệu đi/đến (External Entities) và các kho lưu trữ dữ liệu tĩnh (Data Stores). DFD không thể hiện giao diện hay hành vi tương tác của Actor.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Hãy giải thích khái niệm Ma trận truy vết yêu cầu (Requirements Traceability Matrix - RTM) và lý do tại sao cấu trúc này lại là công cụ sống còn để kiểm soát hiện tượng phình to phạm vi dự án (Scope Creep)?
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa cơ chế liên kết hai chiều của ma trận RTM
    keypoint_weight: 0.4
    description: RTM là một bảng biểu kỹ thuật dùng để thiết lập mối liên kết theo cả hai chiều (Forward và Backward) từ: Mục tiêu kinh doanh ban đầu -> Yêu cầu chức năng chi tiết -> Các tác vụ thiết kế/lập trình -> Kịch bản kiểm thử (Test Cases) tương ứng.
  - id: KP10_2
    content: Đảm bảo độ bao phủ toàn vẹn của yêu cầu (Requirement Coverage)
    keypoint_weight: 0.3
    description: Giúp BA và QA/Tester kiểm tra một cách hệ thống xem mọi yêu cầu ban đầu của khách hàng đã được lập trình và kiểm thử đầy đủ hay chưa, đảm bảo không có tính năng nào bị bỏ sót trong sản phẩm cuối cùng.
  - id: KP10_3
    content: Đánh chặn hiện tượng phình to phạm vi tự phát (Scope Creep Control)
    keypoint_weight: 0.3
    description: Khi dự án phình to, RTM giúp phát hiện lập tức các đoạn code dư thừa, các tính năng do Developer tự ý thêm vào (Gold Plating) hoặc do khách hàng cài cắm thêm mà không được chứng minh là phục vụ cho một mục tiêu kinh doanh hợp lệ nào trong thỏa thuận phạm vi ban đầu.