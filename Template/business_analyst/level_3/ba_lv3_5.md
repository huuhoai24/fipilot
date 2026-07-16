# Bộ Câu Hỏi Phỏng Vấn Business Analyst (Level 3) - Enterprise Architecture & Integration (5)

* **Role:** Business Analyst
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích sự khác biệt giữa Enterprise Architecture (EA) và Solution Architecture. BA tương tác với mỗi vai trò như thế nào?
* **expected_key_points:**
  - id: KP1
    content: EA: big picture toàn tổ chức
    keypoint_weight: 0.35
    description: EA định nghĩa blueprint tổng thể: business, data, application, technology architecture cho toàn công ty.
  - id: KP2
    content: SA: solution-level design
    keypoint_weight: 0.35
    description: SA thiết kế kiến trúc cho 1 solution/project cụ thể, tuân thủ EA guidelines.
  - id: KP3
    content: BA bridge giữa business và architecture
    keypoint_weight: 0.3
    description: BA cung cấp business requirements cho SA, và validate solution design với business stakeholders.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** API là gì theo góc nhìn BA? Bạn document API requirements như thế nào?
* **expected_key_points:**
  - id: KP1
    content: API as integration contract
    keypoint_weight: 0.4
    description: Application Programming Interface - hợp đồng giao tiếp giữa các hệ thống, BA định nghĩa business logic phía sau.
  - id: KP2
    content: API specification elements
    keypoint_weight: 0.35
    description: Endpoints, request/response format, authentication, error codes, rate limits, data validation rules.
  - id: KP3
    content: Consumer-driven approach
    keypoint_weight: 0.25
    description: BA thu thập use cases từ API consumers, đảm bảo API design phục vụ đúng business needs.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Bạn hiểu thế nào về middleware/ESB trong enterprise integration? Vai trò BA khi dự án có integration component.
* **expected_key_points:**
  - id: KP1
    content: ESB as integration hub
    keypoint_weight: 0.35
    description: Enterprise Service Bus kết nối nhiều hệ thống, cung cấp message routing, transformation, protocol conversion.
  - id: KP2
    content: BA define integration requirements
    keypoint_weight: 0.35
    description: BA xác định data mapping, transformation rules, error handling, SLA cho mỗi integration flow.
  - id: KP3
    content: Monitoring và alerting requirements
    keypoint_weight: 0.3
    description: BA define business-level monitoring: transaction success rate, data freshness, escalation procedures.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn phân tích yêu cầu cho việc tích hợp 5 hệ thống legacy với một platform mới. Mô tả approach từ discovery đến delivery.
* **expected_key_points:**
  - id: KP1
    content: System landscape analysis
    keypoint_weight: 0.25
    description: Map tất cả systems, data flows, dependencies. Tạo context diagram và integration matrix.
  - id: KP2
    content: Integration pattern selection
    keypoint_weight: 0.3
    description: Đánh giá point-to-point vs hub-spoke, sync vs async, batch vs real-time cho từng integration.
  - id: KP3
    content: Data mapping và transformation spec
    keypoint_weight: 0.25
    description: Chi tiết source-to-target mapping, business rules cho data transformation, exception handling.
  - id: KP4
    content: Testing strategy cho integration
    keypoint_weight: 0.2
    description: Unit test per integration, end-to-end testing, performance testing, failover testing.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn tham gia dự án Cloud Migration. Vai trò BA trong việc đánh giá ứng dụng nào nên migrate và phương pháp nào (6Rs)?
* **expected_key_points:**
  - id: KP1
    content: 6Rs: Rehost, Replatform, Refactor, Repurchase, Retire, Retain
    keypoint_weight: 0.3
    description: Đánh giá từng ứng dụng theo complexity, business criticality, technical debt để chọn strategy.
  - id: KP2
    content: Business impact assessment
    keypoint_weight: 0.25
    description: Phân tích downtime tolerance, user impact, compliance requirements cho migration planning.
  - id: KP3
    content: Cost-benefit analysis per application
    keypoint_weight: 0.25
    description: TCO comparison: on-premise vs cloud, including licensing, infrastructure, operational costs.
  - id: KP4
    content: Migration wave planning
    keypoint_weight: 0.2
    description: Grouping applications by dependency, risk level, business priority cho phased migration.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Mô tả cách bạn document một complex workflow khi có nhiều hệ thống tham gia (cross-system workflow).
* **expected_key_points:**
  - id: KP1
    content: Swimlane diagram
    keypoint_weight: 0.3
    description: Sử dụng BPMN collaboration diagram với swimlanes cho mỗi system/actor, thể hiện message flows.
  - id: KP2
    content: Sequence diagram cho system interactions
    keypoint_weight: 0.25
    description: UML sequence diagram chi tiết thứ tự gọi giữa các systems, sync/async calls.
  - id: KP3
    content: Error handling và compensation flows
    keypoint_weight: 0.25
    description: Document exception paths, retry logic, rollback procedures, manual intervention points.
  - id: KP4
    content: State diagram cho entity lifecycle
    keypoint_weight: 0.2
    description: Track trạng thái entity (order, ticket) qua các hệ thống, transitions và triggers.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn đánh giá vendor solution thông qua RFP process. Mô tả các bước từ requirement gathering đến vendor selection.
* **expected_key_points:**
  - id: KP1
    content: Requirements elicitation và RFP creation
    keypoint_weight: 0.3
    description: Thu thập functional/non-functional requirements, tạo RFP document với evaluation criteria và weightings.
  - id: KP2
    content: Vendor evaluation matrix
    keypoint_weight: 0.25
    description: Scoring model: functionality fit, cost, vendor stability, implementation timeline, references.
  - id: KP3
    content: Demo và proof of concept
    keypoint_weight: 0.25
    description: Tổ chức scripted demo với real business scenarios, POC cho critical/risky features.
  - id: KP4
    content: Contract negotiation inputs
    keypoint_weight: 0.2
    description: BA provide SLA requirements, customization scope, data ownership, exit strategy clauses.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế Integration Architecture cho hệ thống omnichannel retail: POS, e-commerce, mobile app, warehouse, CRM. Trình bày requirements và considerations.
* **expected_key_points:**
  - id: KP1
    content: Real-time inventory synchronization
    keypoint_weight: 0.25
    description: Event-driven architecture cho stock updates across channels, conflict resolution cho concurrent orders.
  - id: KP2
    content: Customer 360 data integration
    keypoint_weight: 0.3
    description: Unified customer profile across channels, identity resolution, preference sync, GDPR compliance.
  - id: KP3
    content: Order management orchestration
    keypoint_weight: 0.25
    description: Distributed order management: routing logic, split shipments, returns across channels, status tracking.
  - id: KP4
    content: Scalability cho peak periods
    keypoint_weight: 0.2
    description: Black Friday/sale events capacity planning, auto-scaling requirements, graceful degradation strategy.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Bạn cần phân tích requirements cho việc triển khai Event-Driven Architecture (EDA) thay thế traditional batch processing. Trình bày trade-offs và deliverables.
* **expected_key_points:**
  - id: KP1
    content: Event identification và design
    keypoint_weight: 0.3
    description: Domain events analysis, event schema design, event catalog, versioning strategy.
  - id: KP2
    content: Eventual consistency implications
    keypoint_weight: 0.25
    description: Giải thích cho business stakeholders về data consistency trade-offs, compensation mechanisms.
  - id: KP3
    content: Event sourcing và CQRS patterns
    keypoint_weight: 0.25
    description: Khi nào áp dụng event sourcing, CQRS cho read/write separation, replay capability.
  - id: KP4
    content: Monitoring và observability requirements
    keypoint_weight: 0.2
    description: Event flow tracing, dead letter queues, alerting on event processing failures, business metrics dashboards.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Bạn phải xây dựng Technology Evaluation Framework cho tổ chức khi cần chọn giữa Salesforce, SAP, và custom-built CRM. BA approach như thế nào?
* **expected_key_points:**
  - id: KP1
    content: Fit-gap analysis methodology
    keypoint_weight: 0.3
    description: Map business requirements vs each platform capabilities, quantify gaps, estimate customization effort.
  - id: KP2
    content: Total Cost of Ownership comparison
    keypoint_weight: 0.25
    description: Licensing, implementation, customization, training, ongoing maintenance, opportunity cost for 5-year horizon.
  - id: KP3
    content: Integration ecosystem assessment
    keypoint_weight: 0.25
    description: Đánh giá khả năng integrate với existing landscape, API maturity, marketplace/connectors availability.
  - id: KP4
    content: Change management và adoption risk
    keypoint_weight: 0.2
    description: User adoption difficulty, training requirements, organizational change impact, vendor support quality.

