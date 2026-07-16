# Bộ Câu Hỏi Phỏng Vấn Business Analyst (Level 3) - Phân tích Yêu cầu & Quản lý Stakeholder (1)

* **Role:** Business Analyst
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Với kinh nghiệm 4-5 năm, bạn phân biệt thế nào giữa Business Requirements Document (BRD) và Functional Requirements Specification (FRS)? Cho ví dụ cụ thể.
* **expected_key_points:**
  - id: KP1
    content: BRD mô tả mục tiêu kinh doanh
    keypoint_weight: 0.35
    description: BRD tập trung vào WHY - lý do kinh doanh, mục tiêu chiến lược, và phạm vi dự án ở mức cao.
  - id: KP2
    content: FRS mô tả hành vi hệ thống chi tiết
    keypoint_weight: 0.35
    description: FRS tập trung vào HOW - các chức năng cụ thể, luồng xử lý, và quy tắc nghiệp vụ.
  - id: KP3
    content: Mối quan hệ và thứ tự tạo
    keypoint_weight: 0.3
    description: BRD được tạo trước, FRS được dẫn xuất từ BRD và chi tiết hóa từng yêu cầu kinh doanh.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Bạn đã sử dụng kỹ thuật nào để quản lý Stakeholder có mâu thuẫn lợi ích? Mô tả quy trình cụ thể.
* **expected_key_points:**
  - id: KP1
    content: Stakeholder mapping và power-interest grid
    keypoint_weight: 0.4
    description: Phân loại stakeholder theo mức độ ảnh hưởng và quan tâm để xác định chiến lược giao tiếp phù hợp.
  - id: KP2
    content: Kỹ thuật negotiation và facilitation
    keypoint_weight: 0.35
    description: Sử dụng workshop, mediation session để tìm điểm chung và giải quyết xung đột.
  - id: KP3
    content: Escalation path rõ ràng
    keypoint_weight: 0.25
    description: Thiết lập quy trình leo thang khi không thể giải quyết ở cấp BA, có decision log.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Traceability Matrix là gì? Bạn áp dụng nó như thế nào trong quản lý yêu cầu?
* **expected_key_points:**
  - id: KP1
    content: Ma trận theo dõi yêu cầu
    keypoint_weight: 0.4
    description: Công cụ liên kết yêu cầu kinh doanh → yêu cầu chức năng → test case → deliverable.
  - id: KP2
    content: Forward và backward traceability
    keypoint_weight: 0.35
    description: Forward: từ yêu cầu đến implementation. Backward: từ deliverable ngược về yêu cầu gốc.
  - id: KP3
    content: Quản lý thay đổi và impact analysis
    keypoint_weight: 0.25
    description: Khi yêu cầu thay đổi, dùng traceability matrix để đánh giá phạm vi ảnh hưởng nhanh chóng.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn xử lý thế nào khi Product Owner thay đổi yêu cầu giữa sprint trong môi trường Agile? Đưa ra framework quyết định.
* **expected_key_points:**
  - id: KP1
    content: Đánh giá impact trên sprint goal
    keypoint_weight: 0.3
    description: Phân tích xem thay đổi có ảnh hưởng đến sprint goal hiện tại hay không, ước lượng effort.
  - id: KP2
    content: Change request process trong Agile
    keypoint_weight: 0.3
    description: Nếu nhỏ, thêm vào sprint; nếu lớn, đưa vào backlog và reprioritize cho sprint sau.
  - id: KP3
    content: Trade-off analysis
    keypoint_weight: 0.2
    description: Trình bày rõ cái gì phải bỏ nếu thêm yêu cầu mới, dùng velocity làm căn cứ.
  - id: KP4
    content: Communication với team
    keypoint_weight: 0.2
    description: Thông báo kịp thời cho dev team, QA về thay đổi, cập nhật acceptance criteria.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Mô tả cách bạn thiết kế một quy trình UAT (User Acceptance Testing) từ đầu đến cuối cho hệ thống ERP.
* **expected_key_points:**
  - id: KP1
    content: Xây dựng UAT plan và test scenarios
    keypoint_weight: 0.3
    description: Tạo kịch bản test dựa trên business process, bao gồm happy path và edge cases.
  - id: KP2
    content: Lựa chọn và đào tạo UAT testers
    keypoint_weight: 0.25
    description: Chọn end-users đại diện cho từng phòng ban, training về cách test và report bug.
  - id: KP3
    content: Entry/Exit criteria rõ ràng
    keypoint_weight: 0.25
    description: Định nghĩa điều kiện bắt đầu UAT và tiêu chí chấp nhận để go-live.
  - id: KP4
    content: Defect tracking và sign-off
    keypoint_weight: 0.2
    description: Quy trình log bug, phân loại severity, và lấy sign-off từ business owner.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn phân tích gap analysis giữa hệ thống hiện tại (AS-IS) và hệ thống mong muốn (TO-BE) như thế nào? Cho ví dụ thực tế.
* **expected_key_points:**
  - id: KP1
    content: Mô hình hóa AS-IS process
    keypoint_weight: 0.3
    description: Document quy trình hiện tại bằng BPMN hoặc flowchart, xác định pain points và bottleneck.
  - id: KP2
    content: Thiết kế TO-BE với cải tiến
    keypoint_weight: 0.3
    description: Đề xuất quy trình tương lai dựa trên best practice, automation opportunities, và business goals.
  - id: KP3
    content: Gap identification và prioritization
    keypoint_weight: 0.25
    description: Liệt kê các gap, phân loại theo impact và effort, tạo roadmap triển khai.
  - id: KP4
    content: Risk assessment cho từng gap
    keypoint_weight: 0.15
    description: Đánh giá rủi ro kỹ thuật và tổ chức khi bridge mỗi gap.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn sử dụng Data Flow Diagram (DFD) trong ngữ cảnh nào? So sánh DFD Level 0 và Level 1.
* **expected_key_points:**
  - id: KP1
    content: Context diagram (Level 0)
    keypoint_weight: 0.3
    description: Mô tả hệ thống như một process duy nhất, thể hiện external entities và data flows chính.
  - id: KP2
    content: Decomposition sang Level 1
    keypoint_weight: 0.3
    description: Phân rã process chính thành các sub-processes, chi tiết hóa data stores và transformations.
  - id: KP3
    content: Ngữ cảnh sử dụng
    keypoint_weight: 0.2
    description: Dùng khi cần hiểu luồng dữ liệu trong hệ thống, đặc biệt cho data migration hoặc integration.
  - id: KP4
    content: Balancing giữa các levels
    keypoint_weight: 0.2
    description: Đảm bảo inputs/outputs ở level cao phải match với chi tiết ở level thấp hơn.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Bạn được giao phân tích yêu cầu cho việc tích hợp hệ thống CRM với ERP, bao gồm data synchronization real-time. Hãy trình bày approach và các deliverables chính.
* **expected_key_points:**
  - id: KP1
    content: Integration architecture analysis
    keypoint_weight: 0.3
    description: Phân tích API-based vs middleware (ESB), đánh giá data mapping giữa CRM entities và ERP modules.
  - id: KP2
    content: Data governance và quality rules
    keypoint_weight: 0.25
    description: Định nghĩa master data, conflict resolution rules, data validation khi sync giữa 2 hệ thống.
  - id: KP3
    content: Non-functional requirements cho real-time sync
    keypoint_weight: 0.25
    description: Latency SLA, throughput, error handling, retry mechanism, và monitoring requirements.
  - id: KP4
    content: Deliverables: Integration spec, data mapping doc, SLA definition
    keypoint_weight: 0.2
    description: Tạo integration specification document, data mapping matrix, và SLA agreement.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế một Decision Model using DMN (Decision Model and Notation) cho quy trình phê duyệt khoản vay ngân hàng. Giải thích cấu trúc và logic.
* **expected_key_points:**
  - id: KP1
    content: Decision Requirements Diagram (DRD)
    keypoint_weight: 0.3
    description: Vẽ DRD thể hiện các decisions, input data, knowledge sources và dependencies giữa chúng.
  - id: KP2
    content: Decision tables với business rules
    keypoint_weight: 0.3
    description: Tạo decision tables cho từng decision node: credit score ranges, income ratios, collateral valuation.
  - id: KP3
    content: Hit policy và completeness check
    keypoint_weight: 0.2
    description: Chọn hit policy phù hợp (Unique, First, Priority), kiểm tra đủ các combinations.
  - id: KP4
    content: Integration với BPMN process
    keypoint_weight: 0.2
    description: Liên kết DMN decision với business rule task trong BPMN loan approval workflow.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Bạn phải thực hiện một Business Case cho dự án chuyển đổi số (Digital Transformation) với ngân sách 5 tỷ VNĐ. Trình bày cấu trúc và phương pháp tính toán.
* **expected_key_points:**
  - id: KP1
    content: Cost-Benefit Analysis chi tiết
    keypoint_weight: 0.3
    description: Phân tích TCO (Total Cost of Ownership), tangible/intangible benefits, payback period, NPV, IRR.
  - id: KP2
    content: Risk quantification và sensitivity analysis
    keypoint_weight: 0.25
    description: Lượng hóa rủi ro, tạo scenarios (best/worst/most likely), Monte Carlo simulation nếu cần.
  - id: KP3
    content: Strategic alignment và KPIs
    keypoint_weight: 0.25
    description: Liên kết business case với chiến lược công ty, định nghĩa KPIs đo lường thành công sau triển khai.
  - id: KP4
    content: Phased implementation roadmap
    keypoint_weight: 0.2
    description: Đề xuất triển khai theo phases với milestones, gate reviews, và criteria cho mỗi phase.

