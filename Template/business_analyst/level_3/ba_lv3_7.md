# Bộ Câu Hỏi Phỏng Vấn Business Analyst (Level 3) - Business Rules & Decision Analysis (7)

* **Role:** Business Analyst
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Business Rule là gì? Bạn phân loại và document business rules như thế nào trong dự án?
* **expected_key_points:**
  - id: KP1
    content: Định nghĩa và phân loại
    keypoint_weight: 0.4
    description: Quy tắc kinh doanh kiểm soát hành vi hệ thống. Phân loại: constraint, computation, inference, action-enabling.
  - id: KP2
    content: Documentation format
    keypoint_weight: 0.35
    description: Structured natural language, decision tables, hoặc decision trees tùy complexity.
  - id: KP3
    content: Separation of concerns
    keypoint_weight: 0.25
    description: Business rules nên tách biệt khỏi process logic để dễ maintain và thay đổi.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt Decision Table, Decision Tree, và Decision Matrix. Ưu nhược điểm của mỗi loại.
* **expected_key_points:**
  - id: KP1
    content: Decision Table cho multiple conditions
    keypoint_weight: 0.35
    description: Bảng conditions → actions, phù hợp khi nhiều điều kiện kết hợp. Ưu: dễ verify completeness.
  - id: KP2
    content: Decision Tree cho sequential decisions
    keypoint_weight: 0.35
    description: Cây quyết định tuần tự, dễ visualize. Ưu: trực quan. Nhược: khó quản lý khi quá nhiều branches.
  - id: KP3
    content: Decision Matrix cho evaluation/scoring
    keypoint_weight: 0.3
    description: Ma trận đánh giá với criteria và weights. Dùng cho vendor selection, option comparison.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Bạn validate business rules với stakeholders như thế nào để đảm bảo tính chính xác?
* **expected_key_points:**
  - id: KP1
    content: Walkthrough sessions
    keypoint_weight: 0.4
    description: Review từng rule với business SMEs, dùng concrete examples/scenarios để verify logic.
  - id: KP2
    content: Test cases từ business rules
    keypoint_weight: 0.35
    description: Tạo test scenarios cover all combinations, boundary values, và edge cases.
  - id: KP3
    content: Version control và approval workflow
    keypoint_weight: 0.25
    description: Track changes, require formal sign-off từ rule owners khi thay đổi.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn thiết kế hệ thống business rules engine cho insurance claim processing. Mô tả các components và integration.
* **expected_key_points:**
  - id: KP1
    content: Rule categories cho claims
    keypoint_weight: 0.3
    description: Eligibility rules, coverage rules, fraud detection rules, payment calculation rules.
  - id: KP2
    content: Rule engine architecture
    keypoint_weight: 0.25
    description: Externalize rules từ application code, rule repository, versioning, rule execution engine.
  - id: KP3
    content: Rule testing và simulation
    keypoint_weight: 0.25
    description: Test environment cho business users chạy scenarios, impact analysis trước khi deploy rule changes.
  - id: KP4
    content: Audit và compliance
    keypoint_weight: 0.2
    description: Log mỗi rule execution, decision rationale, regulatory traceability.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn sẽ phân tích và document complex pricing logic cho một SaaS product với tiered pricing, discounts, và promotional offers. Approach?
* **expected_key_points:**
  - id: KP1
    content: Pricing model decomposition
    keypoint_weight: 0.3
    description: Base price → tier adjustments → volume discounts → promotional overlays → tax calculation. Document mỗi layer.
  - id: KP2
    content: Decision tables cho pricing rules
    keypoint_weight: 0.25
    description: Tạo decision tables cho mỗi pricing rule: conditions (user type, volume, contract), actions (rate, discount %).
  - id: KP3
    content: Edge cases và conflict resolution
    keypoint_weight: 0.25
    description: Khi nhiều discounts overlap, priority rules. Minimum price floors, maximum discount caps.
  - id: KP4
    content: Change management cho pricing
    keypoint_weight: 0.2
    description: Effective dates, grandfathering existing customers, notification requirements, audit trail.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Compliance requirements (GDPR, PCI-DSS) ảnh hưởng thế nào đến business analysis? Bạn incorporate compliance vào requirements như thế nào?
* **expected_key_points:**
  - id: KP1
    content: Compliance as non-functional requirements
    keypoint_weight: 0.3
    description: Map regulatory clauses thành technical/process requirements: data retention, encryption, access control.
  - id: KP2
    content: Privacy by design principles
    keypoint_weight: 0.25
    description: Data minimization, purpose limitation, consent management, right to erasure built into requirements.
  - id: KP3
    content: Compliance traceability
    keypoint_weight: 0.25
    description: Link mỗi requirement tới specific regulation clause, maintain mapping matrix.
  - id: KP4
    content: Impact on existing processes
    keypoint_weight: 0.2
    description: Gap analysis giữa current processes và compliance requirements, remediation plan.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn document exception handling rules cho hệ thống payment processing. Mô tả approach và các scenarios cần cover.
* **expected_key_points:**
  - id: KP1
    content: Exception taxonomy
    keypoint_weight: 0.3
    description: Phân loại: technical (timeout, connection failure), business (insufficient funds, fraud alert), regulatory (sanction list match).
  - id: KP2
    content: Retry và fallback logic
    keypoint_weight: 0.25
    description: Retry policy (count, interval, backoff), fallback payment method, manual override conditions.
  - id: KP3
    content: Notification và escalation rules
    keypoint_weight: 0.25
    description: Who gets notified at each exception level, SLA cho resolution, auto-escalation triggers.
  - id: KP4
    content: Reconciliation và audit
    keypoint_weight: 0.2
    description: Exception logging, daily reconciliation process, reporting cho operations team.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế một regulatory compliance monitoring system cho ngân hàng, tự động phát hiện vi phạm AML (Anti-Money Laundering). BA deliverables là gì?
* **expected_key_points:**
  - id: KP1
    content: AML rule specification
    keypoint_weight: 0.3
    description: Transaction monitoring rules: unusual patterns, threshold-based alerts, velocity checks, behavioral anomalies.
  - id: KP2
    content: Risk scoring model requirements
    keypoint_weight: 0.25
    description: Customer risk assessment: geography, transaction volume, PEP status, industry. Scoring methodology documentation.
  - id: KP3
    content: Case management workflow
    keypoint_weight: 0.25
    description: Alert triage → investigation → SAR filing workflow, với SLA, escalation, và documentation requirements.
  - id: KP4
    content: Regulatory reporting requirements
    keypoint_weight: 0.2
    description: CTR (Currency Transaction Report), SAR filing, regulatory exam support, data retention policies.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Xây dựng decision model cho automated underwriting trong bảo hiểm nhân thọ. Trình bày logic, data requirements, và edge cases.
* **expected_key_points:**
  - id: KP1
    content: Underwriting decision hierarchy
    keypoint_weight: 0.3
    description: Medical history assessment → lifestyle risk factors → financial evaluation → policy limits determination.
  - id: KP2
    content: Data integration requirements
    keypoint_weight: 0.25
    description: Medical Information Bureau, prescription databases, motor vehicle records, credit scores integration.
  - id: KP3
    content: Straight-through processing criteria
    keypoint_weight: 0.25
    description: Conditions cho auto-approve, auto-decline, và refer-to-human. Confidence thresholds.
  - id: KP4
    content: Explainability và fairness
    keypoint_weight: 0.2
    description: Regulatory requirement cho explainable decisions, bias testing, protected class considerations.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Bạn cần phân tích và document business rules cho hệ thống dynamic tax calculation hoạt động đa quốc gia (10+ countries). Approach?
* **expected_key_points:**
  - id: KP1
    content: Tax jurisdiction rule engine
    keypoint_weight: 0.3
    description: Xác định applicable tax rules based on: seller location, buyer location, product type, transaction type.
  - id: KP2
    content: Multi-country tax complexity
    keypoint_weight: 0.25
    description: VAT, GST, sales tax differences, withholding tax, tax treaties, reverse charge mechanism.
  - id: KP3
    content: Regulatory update management
    keypoint_weight: 0.25
    description: Process cho incorporting tax rate changes, new regulations, effective dates across jurisdictions.
  - id: KP4
    content: Reporting và audit requirements
    keypoint_weight: 0.2
    description: Country-specific tax reporting formats, audit trail cho tax calculations, compliance certificates.

