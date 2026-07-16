# Bộ Câu Hỏi Phỏng Vấn Business Analyst (Level 3) - Agile & Product Management (4)

* **Role:** Business Analyst
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** So sánh User Story, Use Case, và Job Story. Khi nào BA nên dùng format nào?
* **expected_key_points:**
  - id: KP1
    content: User Story format và context
    keypoint_weight: 0.35
    description: As a [user], I want [goal], so that [reason]. Dùng trong Agile, focus vào user value.
  - id: KP2
    content: Use Case chi tiết hơn
    keypoint_weight: 0.35
    description: Mô tả luồng chính, alternative flows, exceptions. Dùng khi cần chi tiết interaction system-user.
  - id: KP3
    content: Job Story cho innovation
    keypoint_weight: 0.3
    description: When [situation], I want to [motivation], so I can [expected outcome]. Focus vào context, giảm bias persona.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** INVEST criteria cho User Stories là gì? Bạn áp dụng nó thế nào khi refine backlog?
* **expected_key_points:**
  - id: KP1
    content: Independent, Negotiable, Valuable
    keypoint_weight: 0.4
    description: Story không phụ thuộc lẫn nhau, scope có thể thương lượng, và phải tạo giá trị cho user.
  - id: KP2
    content: Estimable, Small, Testable
    keypoint_weight: 0.35
    description: Dev có thể estimate effort, đủ nhỏ để hoàn thành trong 1 sprint, có acceptance criteria rõ ràng.
  - id: KP3
    content: Thực hành story splitting
    keypoint_weight: 0.25
    description: Khi story quá lớn, chia theo workflow steps, data variations, hoặc business rules.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Definition of Ready (DoR) vs Definition of Done (DoD) - phân biệt và cho ví dụ checklist cụ thể.
* **expected_key_points:**
  - id: KP1
    content: DoR: tiêu chí để story vào sprint
    keypoint_weight: 0.4
    description: Acceptance criteria clear, dependencies identified, UX mockup approved, technical approach discussed.
  - id: KP2
    content: DoD: tiêu chí hoàn thành story
    keypoint_weight: 0.35
    description: Code reviewed, unit tests passed, UAT completed, documentation updated, deployed to staging.
  - id: KP3
    content: Team ownership và evolution
    keypoint_weight: 0.25
    description: DoR/DoD do team quyết định, review và cải tiến qua retrospectives.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn quản lý Product Backlog với 200+ items. Mô tả framework ưu tiên và cách bạn maintain backlog health.
* **expected_key_points:**
  - id: KP1
    content: Prioritization frameworks
    keypoint_weight: 0.3
    description: WSJF (Weighted Shortest Job First), RICE (Reach, Impact, Confidence, Effort), hoặc value vs effort matrix.
  - id: KP2
    content: Backlog grooming cadence
    keypoint_weight: 0.25
    description: Regular refinement sessions, story mapping workshops, quarterly theme review.
  - id: KP3
    content: Backlog hygiene practices
    keypoint_weight: 0.25
    description: Archive stale items, merge duplicates, maintain consistent estimation, clear acceptance criteria.
  - id: KP4
    content: Stakeholder alignment
    keypoint_weight: 0.2
    description: Sprint review feedback loop, roadmap communication, managing expectations on delivery timeline.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Mô tả cách bạn tạo một Product Roadmap cho 12 tháng. Các yếu tố nào cần cân nhắc?
* **expected_key_points:**
  - id: KP1
    content: Strategic themes và objectives
    keypoint_weight: 0.3
    description: Align roadmap với business strategy, OKRs, market trends, và competitive landscape.
  - id: KP2
    content: Now-Next-Later format
    keypoint_weight: 0.25
    description: Tránh commit dates cụ thể, dùng time horizons để thể hiện độ tin cậy giảm dần.
  - id: KP3
    content: Dependencies và constraints
    keypoint_weight: 0.25
    description: Technical dependencies, resource constraints, regulatory deadlines, third-party integrations.
  - id: KP4
    content: Review và adaptation cadence
    keypoint_weight: 0.2
    description: Quarterly review, adjust based on market feedback, team velocity, và changing priorities.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn làm việc trong SAFe (Scaled Agile Framework). Vai trò BA khác gì so với Scrum thuần túy? Mô tả ceremony tham gia.
* **expected_key_points:**
  - id: KP1
    content: PI Planning participation
    keypoint_weight: 0.3
    description: BA contribute vào Program Increment planning, break features thành stories, identify dependencies across teams.
  - id: KP2
    content: BA trong ART (Agile Release Train)
    keypoint_weight: 0.25
    description: Làm việc với multiple teams, maintain shared backlog, ensure architectural runway.
  - id: KP3
    content: Enabler stories và NFRs
    keypoint_weight: 0.25
    description: BA viết enabler stories cho technical debt, infrastructure, và non-functional requirements.
  - id: KP4
    content: Solution Intent document
    keypoint_weight: 0.2
    description: Maintain living document mô tả current và intended solution, evolve through set-based design.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn cần viết acceptance criteria cho một feature phức tạp: 'Dynamic pricing engine'. Sử dụng BDD format và cho ví dụ.
* **expected_key_points:**
  - id: KP1
    content: Given-When-Then format
    keypoint_weight: 0.3
    description: Viết scenarios cụ thể: Given [context], When [action], Then [expected result] cho happy và edge cases.
  - id: KP2
    content: Boundary conditions
    keypoint_weight: 0.25
    description: Cover minimum/maximum price limits, time-based rules, competitor price matching thresholds.
  - id: KP3
    content: Integration scenarios
    keypoint_weight: 0.25
    description: Scenarios cho real-time price updates, inventory sync, và fallback khi external data unavailable.
  - id: KP4
    content: Performance acceptance criteria
    keypoint_weight: 0.2
    description: Price calculation latency < 200ms, batch repricing throughput, và accuracy tolerance.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Bạn được yêu cầu chuyển đổi tổ chức từ Waterfall sang Agile cho team 50 người. Trình bày transition plan và vai trò BA trong quá trình này.
* **expected_key_points:**
  - id: KP1
    content: Assessment và readiness evaluation
    keypoint_weight: 0.25
    description: Đánh giá current maturity, organizational culture, pain points, stakeholder willingness to change.
  - id: KP2
    content: Phased transition approach
    keypoint_weight: 0.3
    description: Pilot team → expand → scale. BA chuyển từ viết BRD sang user stories, từ gatekeeper sang facilitator.
  - id: KP3
    content: BA role evolution
    keypoint_weight: 0.25
    description: Từ document-centric sang conversation-centric, từ requirements analyst sang product thinking mindset.
  - id: KP4
    content: Metrics để đo transition success
    keypoint_weight: 0.2
    description: Team velocity trend, cycle time reduction, stakeholder satisfaction, defect escape rate.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế một Product Analytics Framework cho ứng dụng SaaS B2B. Bạn sẽ track những gì và tại sao?
* **expected_key_points:**
  - id: KP1
    content: Pirate Metrics (AARRR)
    keypoint_weight: 0.25
    description: Acquisition, Activation, Retention, Revenue, Referral - framework cho SaaS lifecycle metrics.
  - id: KP2
    content: Feature adoption và usage analytics
    keypoint_weight: 0.3
    description: Track feature discovery, activation rate, frequency of use, time-to-value cho key features.
  - id: KP3
    content: Cohort analysis và churn prediction
    keypoint_weight: 0.25
    description: Phân tích retention by cohort, identify churn indicators, expansion revenue signals.
  - id: KP4
    content: Data-driven product decisions
    keypoint_weight: 0.2
    description: Kết nối analytics với roadmap decisions, A/B test results, feature deprecation criteria.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Bạn cần đánh giá và chọn giữa 3 giải pháp: Build in-house, Buy COTS package, hoặc Outsource phát triển. Trình bày decision framework.
* **expected_key_points:**
  - id: KP1
    content: Multi-criteria evaluation matrix
    keypoint_weight: 0.3
    description: Criteria: TCO, time-to-market, customization needs, vendor risk, IP ownership, strategic importance.
  - id: KP2
    content: Build: khi nào phù hợp
    keypoint_weight: 0.2
    description: Core differentiator, unique requirements, long-term control needed, có internal capability.
  - id: KP3
    content: Buy: COTS evaluation process
    keypoint_weight: 0.25
    description: RFP/RFI process, vendor demo, fit-gap analysis, reference check, contract negotiation.
  - id: KP4
    content: Risk analysis cho mỗi option
    keypoint_weight: 0.25
    description: Build: timeline/budget overrun. Buy: vendor lock-in, customization limits. Outsource: quality, knowledge transfer.

