# Bộ Câu Hỏi Phỏng Vấn Business Analyst (Level 1)

* **Role:** Business Analyst
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong tài liệu đặc tả yêu cầu, hãy phân biệt điểm khác biệt cơ bản giữa Business Requirements (Yêu cầu kinh doanh) và User Requirements (Yêu cầu người dùng).
* **expected_key_points:**
  - id: KP1_1
    content: Bản chất chiến lược cao cấp của Business Requirements
    keypoint_weight: 0.5
    description: Là những mục tiêu, tầm nhìn chiến lược ở cấp độ tổ chức hoặc doanh nghiệp, giải thích lý do tại sao dự án được khởi tạo và lợi ích kinh doanh mong muốn đạt được (tối ưu hóa quy trình vận hành, tăng trưởng doanh thu).
  - id: KP1_2
    content: Bản chất tác vụ thực tế của User Requirements
    keypoint_weight: 0.5
    description: Là những nhu cầu, mong muốn cụ thể của một nhóm người dùng (User/Actor) khi tương tác với hệ thống phần mềm nhằm hoàn thành một tác vụ công việc hoặc mục tiêu hằng ngày của họ.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Hãy phân biệt điểm khác biệt về mặt logic nghiệp vụ giữa hai trạng thái kết thúc giao dịch: "Happy Path" (Luồng tối ưu) và "Exception Path" (Luồng ngoại lệ) khi BA thiết kế một Use Case.
* **expected_key_points:**
  - id: KP2_1
    content: Bản chất lý tưởng của Happy Path
    keypoint_weight: 0.5
    description: Là kịch bản/luồng đi lý tưởng nhất của quy trình nghiệp vụ, nơi người dùng thực hiện các thao tác hoàn toàn chính xác, không gặp bất kỳ lỗi kỹ thuật hay rào cản hệ thống nào và đạt được mục tiêu cuối cùng mượt mà.
  - id: KP2_2
    content: Bản chất xử lý lỗi của Exception Path
    keypoint_weight: 0.5
    description: Là kịch bản/luồng xử lý khi xảy ra các tình huống lỗi, sai sót logic hoặc vi phạm ràng buộc hệ thống khiến người dùng không thể hoàn thành mục tiêu (ví dụ: nhập sai mật khẩu quá số lần, hệ thống hết hàng), yêu cầu hệ thống phải đưa ra thông báo lỗi và hủy giao dịch an toàn.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Khi viết một tài liệu đặc tả (SRS/User Story), tại sao việc định nghĩa rõ ràng các "Business Rules" (Quy tắc nghiệp vụ) lại mang ý nghĩa bắt buộc? Nêu một ví dụ thực tế.
* **expected_key_points:**
  - id: KP3_1
    content: Bản chất định hướng chính sách và ràng buộc của Business Rules
    keypoint_weight: 0.5
    description: Quy tắc nghiệp vụ là những tuyên bố, chính sách, quy định hoặc hiến pháp hoạt động cốt lõi của doanh nghiệp mà hệ thống bắt buộc phải tuân thủ nghiêm ngặt, độc lập với logic giao diện phần mềm.
  - id: KP3_2
    content: Vai trò ngăn ngừa sai lệch logic kèm ví dụ minh họa
    keypoint_weight: 0.5
    description: Giúp đội ngũ phát triển xây dựng đúng các điều kiện kiểm tra dữ liệu, tránh làm sai lệch quy định vận hành thực tế. Ví dụ: "Khách hàng phải trên 18 tuổi mới được mở tài khoản tín dụng" hoặc "Đơn hàng trên 500,000 VND sẽ tự động được miễn phí vận chuyển".

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
* **Câu hỏi:** Kỹ thuật phân tích Mockup/Wireframe đóng vai trò gì trong việc xác thực yêu cầu (Requirement Validation) với khách hàng và giảm thiểu rủi ro cho đội lập trình?
* **expected_key_points:**
  - id: KP5_1
    content: Trực quan hóa giao diện tương tác giảm thiểu mơ hồ
    keypoint_weight: 0.5
    description: Mockup/Wireframe chuyển dịch các mô tả tính năng bằng chữ khô khan thành hình ảnh trực quan về bố cục, luồng đi của màn hình giao diện, giúp khách hàng dễ hình dung sản phẩm cuối cùng để xác nhận đúng nhu cầu của họ.
  - id: KP5_2
    content: Chốt sớm phạm vi thiết kế logic chặn lỗi Refactoring muộn
    keypoint_weight: 0.5
    description: Giúp phát hiện sớm các điểm thiếu sót, phi lý trong luồng trải nghiệm người dùng trước khi viết code, làm căn cứ rõ ràng cho Developer thiết kế giao diện và giảm thiểu tối đa chi phí sửa đổi code (Refactoring) ở giai đoạn cuối.

### Câu 6
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
    description: Swimlane (các làn phân cách dọc hoặc ngang) đại diện cho từng vai trò người dùng (Actor), phòng ban chức năng hoặc phân hệ công nghệ thông tin cụ thể, dùng để chỉ rõ ai/hệ thống nào chịu trách nhiệm thực hiện hành động đó trong quy trình tổng thể.

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
* **Câu hỏi:** Hãy giải thích khái niệm Ma trận truy vết yêu cầu (Requirements Traceability Matrix - RTM) và phân tích sâu cơ chế hoạt động của phép truy vết hai chiều (Forward và Backward Traceability).
* **expected_key_points:**
  - id: KP10_1
    content: Định nghĩa cơ chế liên kết xuyên suốt của ma trận RTM
    keypoint_weight: 0.4
    description: RTM là bảng biểu quản lý dùng để thiết lập mối quan hệ logic liên tục từ Mục tiêu kinh doanh ban đầu -> Yêu cầu chi tiết chức năng -> Tài liệu thiết kế/Module code -> Kịch bản kiểm thử (Test Cases) tương ứng.
  - id: KP10_2
    content: Cơ chế và mục đích của Forward Traceability (Truy vết tiến)
    keypoint_weight: 0.3
    description: Đi từ yêu cầu gốc đi dần về phía các sản phẩm đầu ra (Code, Test Cases). Mục đích nhằm đảm bảo 100% các yêu cầu của khách hàng đều được lập trình và kiểm thử đầy đủ, không bị bỏ sót bất kỳ hạng mục nào (Coverage Check).
  - id: KP10_3
    content: Cơ chế và mục đích của Backward Traceability (Truy vết ngược)
    keypoint_weight: 0.3
    description: Đi ngược từ một Test Case hoặc một chức năng phần mềm cụ thể quay trở về yêu cầu gốc ban đầu. Mục đích nhằm kiểm soát chặt chẽ hiện tượng phình to phạm vi (Scope Creep), đảm bảo mọi dòng code viết ra hoặc tác vụ phát triển đều có lý do chính đáng và phục vụ cho một mục tiêu kinh doanh hợp lệ đã ký kết.