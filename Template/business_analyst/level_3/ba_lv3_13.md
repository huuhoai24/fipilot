# Bộ Câu Hỏi Phỏng Vấn Business Analyst (Level 3) - Modeling & Documentation Standards (13)

* **Role:** Business Analyst
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh UML Use Case Diagram, Activity Diagram, và State Machine Diagram. Khi nào BA dùng từng loại?
* **expected_key_points:**
  - id: KP1
    content: Use Case Diagram: functional scope
    keypoint_weight: 0.35
    description: Mô tả actors và use cases, thể hiện functional boundaries của hệ thống. Dùng trong discovery phase.
  - id: KP2
    content: Activity Diagram: process flow
    keypoint_weight: 0.35
    description: Mô tả workflow với decisions, parallel activities, swimlanes. Dùng cho business process modeling.
  - id: KP3
    content: State Machine: object lifecycle
    keypoint_weight: 0.3
    description: Mô tả trạng thái và transitions của một entity (order, ticket). Dùng khi entity có complex lifecycle.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Bạn dùng ERD (Entity-Relationship Diagram) trong BA work. Giải thích cardinality và khi nào tạo ERD.
* **expected_key_points:**
  - id: KP1
    content: Entities, Attributes, Relationships
    keypoint_weight: 0.35
    description: Entities: business objects. Attributes: properties. Relationships: associations between entities.
  - id: KP2
    content: Cardinality notation
    keypoint_weight: 0.35
    description: 1:1, 1:N, M:N relationships. Chen vs Crow's foot notation. Mandatory vs optional participation.
  - id: KP3
    content: Khi nào BA tạo ERD
    keypoint_weight: 0.3
    description: Data-heavy projects, database design input, data migration, integration mapping, reporting requirements.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Bạn maintain một shared documentation repository cho BA team. Best practices để đảm bảo quality và accessibility.
* **expected_key_points:**
  - id: KP1
    content: Template standardization
    keypoint_weight: 0.4
    description: Chuẩn hóa templates: BRD, FRS, Use Case, Meeting Notes. Consistent formatting, naming conventions.
  - id: KP2
    content: Version control và review process
    keypoint_weight: 0.35
    description: Document versioning, mandatory peer review, change tracking, approval workflows.
  - id: KP3
    content: Searchability và organization
    keypoint_weight: 0.25
    description: Logical folder structure, tagging system, search-friendly naming, index/catalog document.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn cần model một complex business process spanning 5 departments với 20+ activities. Approach để manage complexity?
* **expected_key_points:**
  - id: KP1
    content: Hierarchical decomposition
    keypoint_weight: 0.3
    description: Level 0: end-to-end overview. Level 1: department-level sub-processes. Level 2: detailed activities.
  - id: KP2
    content: BPMN Collaboration Diagram
    keypoint_weight: 0.25
    description: Sử dụng pools cho departments, message flows cho inter-department communication.
  - id: KP3
    content: Process metrics annotation
    keypoint_weight: 0.25
    description: Annotate cycle time, wait time, handoff points, automation opportunities trên diagram.
  - id: KP4
    content: Stakeholder-specific views
    keypoint_weight: 0.2
    description: Tạo different views cho different audiences: executive summary, operational detail, technical implementation.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Mô tả cách bạn tạo một comprehensive Data Model cho CRM system, từ conceptual đến logical.
* **expected_key_points:**
  - id: KP1
    content: Conceptual data model
    keypoint_weight: 0.3
    description: High-level entities và relationships: Customer, Contact, Account, Opportunity, Product, Activity.
  - id: KP2
    content: Logical data model
    keypoint_weight: 0.25
    description: Detailed attributes, data types, constraints, normalization. Bridge tables cho M:N relationships.
  - id: KP3
    content: Business rules embedded in model
    keypoint_weight: 0.25
    description: Constraints reflecting business rules: customer status transitions, account hierarchy rules, territory mapping.
  - id: KP4
    content: Validation với stakeholders
    keypoint_weight: 0.2
    description: Walkthrough scenarios using data model, verify all business processes can be supported.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn document system interfaces cho integration project. Mô tả Interface Specification Document structure.
* **expected_key_points:**
  - id: KP1
    content: Interface overview và context
    keypoint_weight: 0.25
    description: Source/target systems, integration purpose, business trigger, frequency, direction (uni/bi-directional).
  - id: KP2
    content: Data mapping specification
    keypoint_weight: 0.3
    description: Source field → target field mapping, transformations, default values, mandatory/optional fields.
  - id: KP3
    content: Error handling và recovery
    keypoint_weight: 0.25
    description: Error codes, retry logic, dead letter queue, manual intervention procedures, notification rules.
  - id: KP4
    content: SLA và monitoring
    keypoint_weight: 0.2
    description: Response time, throughput, availability SLA, health check endpoints, alerting thresholds.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn sử dụng BPMN 2.0 để model một approval workflow có parallel reviews và escalation. Mô tả các elements sử dụng.
* **expected_key_points:**
  - id: KP1
    content: Gateways: Parallel, Exclusive, Inclusive
    keypoint_weight: 0.3
    description: Parallel gateway cho simultaneous reviews, Exclusive cho routing decisions, Inclusive cho conditional parallel.
  - id: KP2
    content: Timer events cho escalation
    keypoint_weight: 0.25
    description: Boundary timer events trên approval tasks, trigger escalation khi timeout, non-interrupting reminders.
  - id: KP3
    content: Subprocess và call activities
    keypoint_weight: 0.25
    description: Embed reusable approval subprocess, call activity cho shared review process across workflows.
  - id: KP4
    content: Error và compensation events
    keypoint_weight: 0.2
    description: Error boundary events cho failed approvals, compensation handlers cho rollback nếu cần.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế một Requirements Management Framework cho enterprise program với 10+ projects sharing common components. Tools, processes, và governance.
* **expected_key_points:**
  - id: KP1
    content: Centralized requirements repository
    keypoint_weight: 0.3
    description: Tool selection (Jira, Azure DevOps, DOORS), shared taxonomy, cross-project traceability, reuse library.
  - id: KP2
    content: Requirements governance model
    keypoint_weight: 0.25
    description: Ownership model, change approval process, baseline management, dependency tracking across projects.
  - id: KP3
    content: Quality assurance process
    keypoint_weight: 0.25
    description: Requirements quality metrics, peer review cadence, completeness checklists, ambiguity detection.
  - id: KP4
    content: Reporting và visibility
    keypoint_weight: 0.2
    description: Requirements status dashboard, coverage metrics, dependency matrix, risk-based requirements views.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Bạn cần tạo một Living Documentation system cho Agile product development. Mô tả architecture và maintenance strategy.
* **expected_key_points:**
  - id: KP1
    content: Executable specifications
    keypoint_weight: 0.3
    description: BDD specs as living docs (Cucumber/SpecFlow), auto-generated from test execution results.
  - id: KP2
    content: Documentation as code
    keypoint_weight: 0.25
    description: Docs trong version control, markdown-based, CI/CD pipeline build docs, review cùng code.
  - id: KP3
    content: Architecture Decision Records (ADR)
    keypoint_weight: 0.25
    description: Template: context, decision, consequences. Track technical decisions, easy to find rationale.
  - id: KP4
    content: Maintenance strategy
    keypoint_weight: 0.2
    description: Documentation health metrics, stale content detection, documentation DoD, responsibility matrix.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích và propose một Enterprise-wide Modeling Standard combining TOGAF, BPMN, UML, và ArchiMate cho tổ chức đa quốc gia.
* **expected_key_points:**
  - id: KP1
    content: Modeling language mapping
    keypoint_weight: 0.3
    description: TOGAF ADM phases → applicable modeling languages. ArchiMate cho EA views, BPMN cho processes, UML cho systems.
  - id: KP2
    content: Viewpoint architecture
    keypoint_weight: 0.25
    description: Define standard viewpoints cho different stakeholders: strategy, business, application, technology layers.
  - id: KP3
    content: Tool integration strategy
    keypoint_weight: 0.25
    description: Central repository, model exchange formats (XMI, BPMN XML), tool interoperability requirements.
  - id: KP4
    content: Adoption và training
    keypoint_weight: 0.2
    description: Phased rollout, center of excellence, template library, coaching program, maturity assessment.

