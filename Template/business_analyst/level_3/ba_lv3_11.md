# Bộ Câu Hỏi Phỏng Vấn Business Analyst (Level 3) - Testing & Quality Assurance cho BA (11)

* **Role:** Business Analyst
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** BA tham gia vào testing ở mức độ nào? Phân biệt vai trò BA và QA trong việc đảm bảo chất lượng yêu cầu.
* **expected_key_points:**
  - id: KP1
    content: BA: requirements validation
    keypoint_weight: 0.4
    description: BA validate rằng requirements đúng và đủ, viết acceptance criteria, tham gia UAT.
  - id: KP2
    content: QA: implementation verification
    keypoint_weight: 0.35
    description: QA verify rằng implementation đúng theo requirements, viết test cases chi tiết, thực hiện testing.
  - id: KP3
    content: Collaboration points
    keypoint_weight: 0.25
    description: BA review test cases, clarify requirements cho QA, participate in defect triage.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Acceptance Criteria viết theo format nào? Cho ví dụ cho feature 'Online Payment'.
* **expected_key_points:**
  - id: KP1
    content: Given-When-Then (BDD format)
    keypoint_weight: 0.4
    description: Given: preconditions. When: action. Then: expected result. Chuẩn hóa, dễ automate.
  - id: KP2
    content: Rule-based format
    keypoint_weight: 0.3
    description: Checklist of conditions: payment success, failure handling, timeout, receipt generation.
  - id: KP3
    content: Measurable và testable
    keypoint_weight: 0.3
    description: Mỗi AC phải verify được, không ambiguous, không subjective.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Bạn phân biệt Verification và Validation trong software development. Tại sao cả hai đều quan trọng?
* **expected_key_points:**
  - id: KP1
    content: Verification: Are we building it right?
    keypoint_weight: 0.4
    description: Kiểm tra sản phẩm đúng theo specification: code review, unit test, static analysis.
  - id: KP2
    content: Validation: Are we building the right thing?
    keypoint_weight: 0.35
    description: Kiểm tra sản phẩm đáp ứng nhu cầu user: UAT, beta testing, usability testing.
  - id: KP3
    content: BA focus on validation
    keypoint_weight: 0.25
    description: BA đảm bảo validation qua requirements traceability, UAT coordination, user feedback loops.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn phát hiện nhiều defects trong UAT bắt nguồn từ requirements ambiguity. Bạn sẽ cải thiện requirements quality như thế nào?
* **expected_key_points:**
  - id: KP1
    content: Requirements quality metrics
    keypoint_weight: 0.25
    description: Track defects attributed to requirements: ambiguity, incompleteness, inconsistency. Trend analysis.
  - id: KP2
    content: Peer review process
    keypoint_weight: 0.3
    description: Formal requirements inspection checklist, cross-functional review sessions, external reviewer rotation.
  - id: KP3
    content: Requirements testing techniques
    keypoint_weight: 0.25
    description: Test case derivation from requirements trước khi code, identify testability issues early.
  - id: KP4
    content: Continuous improvement
    keypoint_weight: 0.2
    description: Root cause analysis cho requirements defects, update templates/checklists, share lessons learned.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn tham gia defect triage meeting. Mô tả quy trình classification và prioritization defects.
* **expected_key_points:**
  - id: KP1
    content: Severity vs Priority classification
    keypoint_weight: 0.3
    description: Severity: technical impact (Critical, Major, Minor, Cosmetic). Priority: business urgency (P1-P4).
  - id: KP2
    content: BA role trong triage
    keypoint_weight: 0.25
    description: Validate defect against requirements, confirm expected behavior, assess business impact.
  - id: KP3
    content: Resolution categories
    keypoint_weight: 0.25
    description: Fix, Won't Fix, By Design, Duplicate, Deferred. Decision criteria cho mỗi category.
  - id: KP4
    content: Defect trend analysis
    keypoint_weight: 0.2
    description: Track defect density by module, root cause distribution, find-fix ratio, regression defect rate.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Mô tả cách bạn viết test scenarios cho non-functional requirements: performance, security, usability.
* **expected_key_points:**
  - id: KP1
    content: Performance test scenarios
    keypoint_weight: 0.3
    description: Load testing: concurrent users, response time SLA. Stress testing: breaking point. Endurance: sustained load.
  - id: KP2
    content: Security test scenarios
    keypoint_weight: 0.25
    description: Authentication bypass, authorization escalation, SQL injection, XSS, data encryption verification.
  - id: KP3
    content: Usability test scenarios
    keypoint_weight: 0.25
    description: Task completion rate, learnability, error recovery, accessibility compliance, multi-device testing.
  - id: KP4
    content: Acceptance criteria cho NFRs
    keypoint_weight: 0.2
    description: Quantifiable thresholds: 95th percentile response < 2s, OWASP Top 10 compliance, SUS score > 68.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn implement test automation strategy cho regression testing. BA contribute gì vào process này?
* **expected_key_points:**
  - id: KP1
    content: Test case selection cho automation
    keypoint_weight: 0.3
    description: BA identify high-priority business scenarios, frequently executed flows, và stable features cho automation.
  - id: KP2
    content: Test data management
    keypoint_weight: 0.25
    description: BA define representative test data sets, edge cases data, và data refresh requirements.
  - id: KP3
    content: Automation-friendly acceptance criteria
    keypoint_weight: 0.25
    description: Viết AC structured, unambiguous, với clear expected results dễ assert programmatically.
  - id: KP4
    content: ROI assessment
    keypoint_weight: 0.2
    description: BA calculate automation ROI: manual testing effort saved vs automation development/maintenance cost.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế end-to-end testing strategy cho hệ thống microservices với 20+ services, bao gồm contract testing. BA deliverables là gì?
* **expected_key_points:**
  - id: KP1
    content: Testing pyramid cho microservices
    keypoint_weight: 0.3
    description: Unit → Integration → Contract → E2E. BA focus vào defining business scenarios cho contract và E2E layers.
  - id: KP2
    content: Consumer-driven contract testing
    keypoint_weight: 0.25
    description: BA define consumer expectations cho API contracts, Pact-style contracts từ business perspective.
  - id: KP3
    content: Test environment strategy
    keypoint_weight: 0.25
    description: Environment topology, service virtualization, test data isolation, deployment pipeline integration.
  - id: KP4
    content: Chaos engineering requirements
    keypoint_weight: 0.2
    description: BA define business-critical resilience scenarios: service failure, network partition, data inconsistency.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Bạn cần establish Quality Gates cho CI/CD pipeline từ góc nhìn business requirements. Mô tả approach.
* **expected_key_points:**
  - id: KP1
    content: Quality gate criteria definition
    keypoint_weight: 0.3
    description: Code coverage thresholds, zero critical defects, performance regression limits, security scan pass.
  - id: KP2
    content: Business validation gates
    keypoint_weight: 0.25
    description: Feature toggle validation, A/B test setup verification, regulatory compliance checks.
  - id: KP3
    content: Automated vs manual gates
    keypoint_weight: 0.25
    description: Which checks can be automated, which require human review (UX review, legal review).
  - id: KP4
    content: Metrics và continuous improvement
    keypoint_weight: 0.2
    description: Gate pass/fail rates, false positive rates, pipeline speed, escaped defect tracking.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích requirements cho hệ thống Data Validation Framework xử lý 1M+ records/ngày với complex business rules. BA approach?
* **expected_key_points:**
  - id: KP1
    content: Validation rule specification
    keypoint_weight: 0.3
    description: Categorize rules: format, range, referential integrity, cross-field, temporal, aggregate. Priority levels.
  - id: KP2
    content: Error handling và remediation workflows
    keypoint_weight: 0.25
    description: Auto-correct vs reject vs quarantine logic. Business user interface cho exception management.
  - id: KP3
    content: Performance requirements
    keypoint_weight: 0.25
    description: Throughput SLA, batch vs streaming validation, parallel processing requirements.
  - id: KP4
    content: Reporting và monitoring
    keypoint_weight: 0.2
    description: Data quality scorecards, trend dashboards, alerting on quality degradation, audit trails.

