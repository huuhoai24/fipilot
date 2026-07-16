# Bộ Câu Hỏi Phỏng Vấn Business Analyst (Level 3) - Financial Analysis & Business Case (9)

* **Role:** Business Analyst
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích NPV (Net Present Value) và IRR (Internal Rate of Return) trong ngữ cảnh business case. Khi nào dùng cái nào?
* **expected_key_points:**
  - id: KP1
    content: NPV: giá trị hiện tại ròng
    keypoint_weight: 0.4
    description: Tổng giá trị hiện tại của cash flows trừ initial investment. NPV > 0 → dự án có lợi. Dùng khi so sánh dự án khác quy mô.
  - id: KP2
    content: IRR: tỷ suất hoàn vốn nội bộ
    keypoint_weight: 0.35
    description: Discount rate tại đó NPV = 0. So sánh với cost of capital. Dùng khi cần percentage return.
  - id: KP3
    content: Limitations và best practice
    keypoint_weight: 0.25
    description: IRR có thể misleading khi cash flows irregular. Nên dùng cả hai kết hợp để ra quyết định.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Bạn estimate effort cho requirements gathering phase bằng phương pháp nào? Giải thích approach.
* **expected_key_points:**
  - id: KP1
    content: Analogous estimation
    keypoint_weight: 0.35
    description: Dựa trên dữ liệu từ dự án tương tự trước đây, adjust cho complexity và scope differences.
  - id: KP2
    content: Work Breakdown Structure
    keypoint_weight: 0.35
    description: Phân rã BA activities: elicitation, analysis, documentation, review, approval. Estimate cho từng work package.
  - id: KP3
    content: Buffer và contingency
    keypoint_weight: 0.3
    description: Thêm contingency 15-25% cho unknowns, stakeholder availability, và rework cycles.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** TCO (Total Cost of Ownership) bao gồm những thành phần nào? Cho ví dụ TCO cho hệ thống SaaS.
* **expected_key_points:**
  - id: KP1
    content: Direct costs
    keypoint_weight: 0.4
    description: Licensing/subscription fees, implementation, customization, data migration, hardware (nếu on-premise).
  - id: KP2
    content: Indirect costs
    keypoint_weight: 0.35
    description: Training, change management, productivity loss during transition, ongoing support, upgrade costs.
  - id: KP3
    content: Hidden costs thường bị bỏ qua
    keypoint_weight: 0.25
    description: Integration maintenance, data storage growth, compliance audits, vendor management overhead.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn build business case cho dự án RPA (Robotic Process Automation) tự động hóa 10 processes. Mô tả methodology tính ROI.
* **expected_key_points:**
  - id: KP1
    content: Process assessment và selection
    keypoint_weight: 0.25
    description: Đánh giá complexity, volume, error rate, suitability cho automation. Prioritize bằng automation readiness score.
  - id: KP2
    content: Cost analysis: current vs automated
    keypoint_weight: 0.3
    description: FTE cost (salary, benefits, overhead) × time spent per process vs RPA development + licensing + maintenance cost.
  - id: KP3
    content: Benefit quantification
    keypoint_weight: 0.25
    description: Time savings, error reduction, 24/7 availability, compliance improvement, employee satisfaction.
  - id: KP4
    content: Payback period calculation
    keypoint_weight: 0.2
    description: Total investment / monthly savings. Typical RPA payback: 6-18 months. Include ramp-up period.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn phân tích make vs buy decision cho một business intelligence platform. Trình bày framework và criteria.
* **expected_key_points:**
  - id: KP1
    content: Strategic alignment assessment
    keypoint_weight: 0.25
    description: BI là core competency hay commodity? Custom analytics needs vs standard reporting?
  - id: KP2
    content: 5-year TCO comparison
    keypoint_weight: 0.3
    description: Build: dev team, infrastructure, ongoing maintenance. Buy: license, implementation partner, customization, upgrades.
  - id: KP3
    content: Time-to-value analysis
    keypoint_weight: 0.25
    description: Build: 12-18 months. Buy: 3-6 months. Opportunity cost of delayed insights.
  - id: KP4
    content: Risk matrix
    keypoint_weight: 0.2
    description: Build risks: scope creep, talent retention. Buy risks: vendor lock-in, feature gaps, data security.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn cần thuyết phục CFO approve budget cho dự án data governance. Data governance không có direct revenue impact. Approach?
* **expected_key_points:**
  - id: KP1
    content: Cost of poor data quality
    keypoint_weight: 0.3
    description: Quantify: rework costs, wrong decisions, regulatory fines, customer churn due to bad data.
  - id: KP2
    content: Risk mitigation value
    keypoint_weight: 0.25
    description: GDPR fines (up to 4% revenue), audit failures, reputational damage probability × impact.
  - id: KP3
    content: Enablement value
    keypoint_weight: 0.25
    description: Data governance enables: better analytics, faster reporting, AI/ML readiness, M&A due diligence.
  - id: KP4
    content: Phased investment approach
    keypoint_weight: 0.2
    description: Start small, demonstrate value, expand. Year 1: critical data domains. Year 2-3: enterprise-wide.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn cần estimate project size bằng Function Point Analysis (FPA). Giải thích methodology và khi nào áp dụng.
* **expected_key_points:**
  - id: KP1
    content: Function Point components
    keypoint_weight: 0.3
    description: EI (External Inputs), EO (External Outputs), EQ (External Queries), ILF (Internal Logical Files), EIF (External Interface Files).
  - id: KP2
    content: Complexity assessment
    keypoint_weight: 0.25
    description: Đánh giá low/average/high complexity cho mỗi component dựa trên data elements và file types referenced.
  - id: KP3
    content: Adjustment factors
    keypoint_weight: 0.25
    description: 14 General System Characteristics: data communications, performance, reusability, etc. Adjust ±35%.
  - id: KP4
    content: FPA to effort conversion
    keypoint_weight: 0.2
    description: Industry benchmarks: hours per FP varies by technology, team experience, và methodology (8-20 hrs/FP).

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Xây dựng một Financial Model cho dự án SaaS product launch dự kiến break-even trong 18 tháng. Trình bày assumptions và key metrics.
* **expected_key_points:**
  - id: KP1
    content: Revenue model assumptions
    keypoint_weight: 0.3
    description: Pricing tiers, expected conversion rates, churn rate, expansion revenue, average contract value (ACV).
  - id: KP2
    content: Cost structure
    keypoint_weight: 0.25
    description: CAC (Customer Acquisition Cost), COGS, R&D, G&A. Variable vs fixed costs. Unit economics.
  - id: KP3
    content: Key SaaS metrics projection
    keypoint_weight: 0.25
    description: MRR/ARR growth, LTV/CAC ratio (target >3x), gross margin (target >70%), burn rate, runway.
  - id: KP4
    content: Sensitivity analysis
    keypoint_weight: 0.2
    description: What-if scenarios: churn rate ±2%, pricing ±20%, sales cycle ±30 days impact on break-even.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Bạn cần build investment thesis cho C-level presentation để justify $2M technology modernization program. Trình bày structure và persuasion techniques.
* **expected_key_points:**
  - id: KP1
    content: Strategic narrative
    keypoint_weight: 0.3
    description: Market pressure, competitive threat, technical debt cost, opportunity cost of inaction. Data-backed urgency.
  - id: KP2
    content: Financial projections với scenarios
    keypoint_weight: 0.25
    description: Conservative, moderate, optimistic scenarios. 3-5 year projections. Sensitivity on key assumptions.
  - id: KP3
    content: Risk-adjusted returns
    keypoint_weight: 0.25
    description: Monte Carlo simulation for key variables, expected value calculation, downside protection strategies.
  - id: KP4
    content: Implementation governance
    keypoint_weight: 0.2
    description: Stage-gate approach, kill criteria, quarterly business review cadence, executive dashboard.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích portfolio prioritization cho 15 dự án đang cạnh tranh cùng budget. Bạn sẽ dùng framework gì và present kết quả thế nào?
* **expected_key_points:**
  - id: KP1
    content: Portfolio scoring model
    keypoint_weight: 0.3
    description: Multi-criteria: strategic alignment, financial return, risk, resource requirements, dependencies, urgency.
  - id: KP2
    content: Constraint-based optimization
    keypoint_weight: 0.25
    description: Budget constraint, resource constraint, dependency sequencing, mandatory vs discretionary projects.
  - id: KP3
    content: Visualization và communication
    keypoint_weight: 0.25
    description: Portfolio bubble chart (value vs risk vs size), Gantt view cho sequencing, investment mix pie chart.
  - id: KP4
    content: Dynamic reprioritization process
    keypoint_weight: 0.2
    description: Quarterly review triggers, criteria for adding/removing projects, opportunity cost assessment.

