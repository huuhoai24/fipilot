# Bộ Câu Hỏi Phỏng Vấn Business Analyst (Level 1)

* **Role:** Business Analyst
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong giai đoạn đầu thu thập yêu cầu, hãy phân biệt điểm khác biệt cốt lõi giữa hai khái niệm: "Nhu cầu của khách hàng" (Customer Wants/Needs) và "Yêu cầu phần mềm" (Software Requirements).
* **expected_key_points:**
  - id: KP1_1
    content: Bản chất thô, hướng bài toán kinh doanh của Nhu cầu khách hàng
    keypoint_weight: 0.5
    description: Là những mong muốn, nỗi đau hoặc bài toán kinh doanh thô ban đầu do khách hàng phát biểu bằng ngôn ngữ tự nhiên, thường mang tính trừu tượng, giải pháp chưa rõ ràng và đôi khi bị mâu thuẫn.
  - id: KP1_2
    content: Bản chất đặc tả logic, có thể thực thi của Yêu cầu phần mềm
    keypoint_weight: 0.5
    description: Là kết quả sau khi BA đã phân tích, làm mịn và chuyển hóa các nhu cầu thô thành các mô tả logic cụ thể, rõ ràng, có tính khả thi kỹ thuật để đội ngũ phát triển (Developer) có thể dựa vào đó lập trình.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Khi BA thực hiện phân tích tài liệu và viết đặc tả chức năng, một "User Scenario" (Kịch bản người dùng) khác gì so với một "Use Case" (Ca sử dụng)?
* **expected_key_points:**
  - id: KP2_1
    content: Bản chất kể chuyện, ngữ cảnh thực tế của User Scenario
    keypoint_weight: 0.5
    description: Scenario là một câu chuyện mô tả chi tiết ngữ cảnh thực tế về cách một người dùng cụ thể cố gắng hoàn thành mục tiêu trong đời sống (Ví dụ: Anh Nam mở app lúc 8h sáng khi đang đi xe buýt để đặt một ly cà phê).
  - id: KP2_2
    content: Bản chất cấu trúc hóa hệ thống, bao quát logic của Use Case
    keypoint_weight: 0.5
    description: Use Case là một tài liệu cấu trúc hóa, mô tả chuỗi tương tác logic toàn diện giữa Tác nhân (Actor) và Hệ thống để hoàn thành tác vụ, bao gồm cả luồng tối ưu (Happy Path) và các luồng lỗi (Exception Paths), không chứa chi tiết cá nhân hóa.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Trong quản lý dự án Agile/Scrum, một hạng mục trong Product Backlog (PBI) được coi là đáp ứng tiêu chuẩn "Ready" (Definition of Ready - DoR) khi nào?
* **expected_key_points:**
  - id: KP3_1
    content: Trạng thái thông tin rõ ràng và có tiêu chí nghiệm thu công khai
    keypoint_weight: 0.5
    description: Hạng mục đó phải có mô tả rõ ràng, không mơ hồ, và bắt buộc phải đi kèm bộ tiêu chí nghiệm thu công khai (Acceptance Criteria) để tất cả các bên cùng hiểu chung một logic.
  - id: KP3_2
    content: Sự sẵn sàng về mặt kỹ thuật cho Sprint Planning
    keypoint_weight: 0.5
    description: Hạng mục đã được đội ngũ phát triển (Development Team) rà soát, ước lượng được độ phức tạp (Estimation) và có kích thước đủ nhỏ để có thể hoàn thành trọn vẹn trong một Sprint mà không bị chặn bởi phụ thuộc bên ngoài.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy phân biệt điểm khác biệt cốt lõi về mặt cơ chế thu thập thông tin và ngữ cảnh áp dụng hiệu quả giữa hai kỹ thuật khơi gợi yêu cầu: Khảo sát diện rộng (Survey/Questionnaire) và Phỏng vấn sâu (Interview).
* **expected_key_points:**
  - id: KP4_1
    content: Cơ chế thu thập dữ liệu định lượng số đông của Survey
    keypoint_weight: 0.5
    description: Survey dùng bảng câu hỏi thiết kế sẵn để thu thập thông tin từ một lượng rất lớn đối tượng người dùng trong thời gian ngắn. Tối ưu cho việc lấy dữ liệu định lượng (Quantitative), thống kê xu hướng nhưng không thể đào sâu các lý do ẩn sau câu trả lời.
  - id: KP4_2
    content: Cơ chế tương tác trực tiếp định tính của Interview
    keypoint_weight: 0.5
    description: Interview là cuộc đối thoại trực tiếp (1-1 hoặc nhóm nhỏ), cho phép BA linh hoạt đặt câu hỏi đào sâu, quan sát phản ứng để thu thập dữ liệu định tính (Qualitative) sâu sắc, phù hợp khi cần làm việc với các Key Stakeholders để hiểu rõ quy trình ngầm phức tạp.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi thực hiện mô hình hóa quy trình (Process Modeling) bằng sơ đồ BPMN, hãy phân biệt sự khác nhau về mặt ngữ nghĩa và cách áp dụng giữa hai thành phần: "Pool" và "Lane" (Swimlane).
* **expected_key_points:**
  - id: KP5_1
    content: Bản chất ranh giới tổ chức độc lập của Pool
    keypoint_weight: 0.5
    description: Pool đại diện cho một thực thể kinh doanh hoặc một tổ chức độc lập hoàn toàn (ví dụ: Công ty Khách hàng và Công ty Vận chuyển). Giao tiếp giữa hai Pool bắt buộc phải sử dụng các luồng thông điệp (Message Flows) chứ không được dùng luồng tuần tự (Sequence Flows).
  - id: KP5_2
    content: Bản chất phân định chức năng nội bộ của Lane
    keypoint_weight: 0.5
    description: Lane là các nhánh phân chia nhỏ nằm bên trong một Pool, dùng để đại diện cho các vai trò (Roles), phòng ban chức năng hoặc phân hệ hệ thống cụ thể thuộc tổ chức đó (ví dụ: Nhân viên bán hàng, Kế toán). Các công việc trong cùng một Pool liên kết với nhau bằng luồng tuần tự qua các Lane.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Kỹ thuật phân tích Mockup/Wireframe đóng vai trò gì trong việc xác thực yêu cầu (Requirement Validation) với khách hàng và giảm thiểu rủi ro cho đội lập trình?
* **expected_key_points:**
  - id: KP6_1
    content: Trực quan hóa giao diện tương tác giảm thiểu mơ hồ
    keypoint_weight: 0.5
    description: Mockup/Wireframe chuyển dịch các mô tả tính năng bằng chữ khô khan thành hình ảnh trực quan về bố cục, luồng đi của màn hình giao diện, giúp khách hàng dễ hình dung sản phẩm cuối cùng để xác nhận đúng nhu cầu của họ.
  - id: KP6_2
    content: Chốt sớm phạm vi thiết kế logic chặn lỗi Refactoring muộn
    keypoint_weight: 0.5
    description: Giúp phát hiện sớm các điểm thiếu sót, phi lý trong luồng trải nghiệm người dùng trước khi viết code, làm căn cứ rõ ràng cho Developer thiết kế front-end và giảm thiểu tối đa chi phí sửa đổi code (Refactoring) ở giai đoạn cuối.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong quản lý yêu cầu phần mềm, tại sao một BA cần phải xác định các "Ràng buộc hệ thống" (System Constraints)? Hãy nêu hai ví dụ thực tế về ràng buộc công nghệ và ràng buộc kinh doanh.
* **expected_key_points:**
  - id: KP7_1
    content: Bản chất giới hạn biên không thể thay đổi của Ràng buộc
    keypoint_weight: 0.4
    description: Ràng buộc là những giới hạn kiến trúc định sẵn, bắt buộc hệ thống phải tuân thủ và đội ngũ dự án không có quyền thay đổi hay lựa chọn, trực tiếp ảnh hưởng đến giải pháp thiết kế phần mềm.
  - id: KP7_2
    content: Ví dụ thực tế về Ràng buộc công nghệ (Technical Constraint)
    keypoint_weight: 0.3
    description: Ví dụ: Hệ thống mới bắt buộc phải chạy trên nền tảng hạ tầng đám mây AWS hiện tại của tập đoàn; hoặc ứng dụng phải tích hợp tương thích với core database Oracle cũ có sẵn.
  - id: KP7_3
    content: Ví dụ thực tế về Ràng buộc kinh doanh (Business/Project Constraint)
    keypoint_weight: 0.3
    description: Ví dụ: Dự án bắt buộc phải nghiệm thu đưa vào vận hành trước ngày 31/12 để kịp mùa quyết toán thuế; hoặc tổng ngân sách phát triển tính năng không được vượt quá 500 triệu VND.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong giai đoạn nghiệm thu UAT, khách hàng từ chối ký biên bản nghiệm thu (Sign-off) với lý do phần mềm chạy đúng theo đặc tả SRS nhưng không giải quyết được bài toán vận hành thực tế do quy trình nghiệp vụ của họ vừa thay đổi. BA cần xử lý tình huống khủng hoảng này thế nào?
* **expected_key_points:**
  - id: KP8_1
    content: Sử dụng Baseline tài liệu đã phê duyệt làm điểm tựa pháp lý
    keypoint_weight: 0.3
    description: Lịch sự đối chiếu lại tài liệu SRS và kết quả kiểm thử đã được hai bên thống nhất ký duyệt làm ranh giới nghiệm thu, nhằm khẳng định đội dự án đã hoàn thành nghĩa vụ phát triển đúng theo cam kết hợp đồng giai đoạn đó.
  - id: KP8_2
    content: Khảo sát nhanh quy trình nghiệp vụ mới để phân tích khoảng cách (Gap Analysis)
    keypoint_weight: 0.4
    description: Đồng cảm với khó khăn của khách hàng, chủ động phối hợp ghi nhận quy trình vận hành mới thay đổi, thực hiện phân tích Gap để xác định rõ phần mềm hiện tại cần chỉnh sửa những gì và mức độ ảnh hưởng kiến trúc.
  - id: KP8_3
    content: Khởi tạo quy trình quản lý thay đổi chính thức (Change Management)
    keypoint_weight: 0.3
    description: Lập hồ sơ Yêu cầu thay đổi (Change Request), chuyển giao cho Project Manager (PM) để làm việc với khách hàng về mặt thủ tục hợp đồng, tính toán chi phí phát sinh và thời gian bàn giao (Phase/Sprint mới) thay vì sửa đổi tự phát phá vỡ phạm vi cũ.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Trong phân tích hệ thống hướng đối tượng, hãy so sánh sự khác biệt bản chất về mặt logic dòng điều khiển giữa sơ đồ Hoạt động (Activity Diagram) và sơ đồ Trạng thái (State Machine Diagram).
* **expected_key_points:**
  - id: KP9_1
    content: Bản chất luồng công việc tuần tự hành động của Activity Diagram
    keypoint_weight: 0.5
    description: Tập trung mô tả luồng công việc (Workflow) hoặc luồng xử lý logic tuần tự/song song của một quy trình hệ thống, thể hiện cách thức các Hành động (Actions) tiếp diễn nhau dựa trên các điểm quyết định; sơ đồ thiên về góc nhìn động của luồng xử lý tổng quan.
  - id: KP9_2
    content: Bản chất vòng đời biến đổi thực thể của State Machine Diagram
    keypoint_weight: 0.5
    description: Tập trung mô tả vòng đời của **một thực thể dữ liệu duy nhất** (ví dụ: Đơn hàng, Hóa đơn), thể hiện các Trạng thái tĩnh (States) của đối tượng đó và các Sự kiện (Events/Triggers) cụ thể kích hoạt sự chuyển dịch từ trạng thái này sang trạng thái khác (như Đơn hàng: Mới tạo -> Đang giao -> Đã nhận).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Hãy phân tích sâu cơ chế hoạt động của Ma trận truy vết yêu cầu (Requirements Traceability Matrix - RTM) trong việc kiểm soát rủi ro thiếu sót yêu cầu và chặn lỗi tự ý phát triển tính năng (Gold Plating).
* **expected_key_points:**
  - id: KP10_1
    content: Cơ chế liên kết bắc cầu xuyên suốt hai chiều của ma trận
    keypoint_weight: 0.4
    description: RTM thiết lập một ma trận liên kết logic chặt chẽ từ: Mục tiêu kinh doanh (Business Goal) -> Yêu cầu chức năng chi tiết -> Các thành phần thiết kế/Dev code -> Kịch bản kiểm thử (Test Cases).
  - id: KP10_2
    content: Quy trình và tác dụng kiểm soát thiếu sót của Forward Traceability
    keypoint_weight: 0.3
    description: Đi từ yêu cầu gốc tiến dần ra sản phẩm đầu ra để rà soát, đảm bảo 100% nhu cầu của khách hàng đều có module code xử lý tương ứng và được bao phủ đầy đủ bằng Test case, triệt tiêu rủi ro bỏ sót tính năng (Completeness check).
  - id: KP10_3
    content: Quy trình và tác dụng chặn tính năng tự phát của Backward Traceability
    keypoint_weight: 0.3
    description: Đi ngược từ một đoạn code hoặc một test case cụ thể quay về yêu cầu gốc. Giúp phát hiện lập tức hiện tượng Gold Plating (lập trình viên tự ý thêm tính năng ngoài phạm vi) hoặc các yêu cầu cài cắm thêm từ khách hàng mà không phục vụ cho mục tiêu kinh doanh ban đầu đã ký kết.