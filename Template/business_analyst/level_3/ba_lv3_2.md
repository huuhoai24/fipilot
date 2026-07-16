# Bộ Câu Hỏi Phỏng Vấn Business Analyst (Level 3) - Process Improvement & Lean Six Sigma (2)

* **Role:** Business Analyst
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt Value-Added, Non-Value-Added, và Business-Value-Added activities trong process analysis. Cho ví dụ cụ thể.
* **expected_key_points:**
  - id: KP1
    content: Value-Added (VA)
    keypoint_weight: 0.35
    description: Hoạt động trực tiếp tạo giá trị cho khách hàng, khách hàng sẵn sàng trả tiền. VD: sản xuất, tư vấn.
  - id: KP2
    content: Non-Value-Added (NVA)
    keypoint_weight: 0.35
    description: Hoạt động lãng phí, không tạo giá trị. VD: chờ phê duyệt không cần thiết, rework.
  - id: KP3
    content: Business-Value-Added (BVA)
    keypoint_weight: 0.3
    description: Không trực tiếp tạo giá trị cho khách hàng nhưng cần thiết cho hoạt động doanh nghiệp. VD: compliance, audit.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** RACI matrix là gì? Bạn đã sử dụng nó trong dự án thực tế nào?
* **expected_key_points:**
  - id: KP1
    content: Responsible, Accountable, Consulted, Informed
    keypoint_weight: 0.4
    description: R: người thực hiện, A: người chịu trách nhiệm cuối cùng, C: được tham vấn, I: được thông báo.
  - id: KP2
    content: Ứng dụng trong cross-functional projects
    keypoint_weight: 0.35
    description: Dùng khi nhiều phòng ban tham gia, tránh overlap trách nhiệm và communication gaps.
  - id: KP3
    content: Quy tắc: mỗi task chỉ 1 Accountable
    keypoint_weight: 0.25
    description: Đảm bảo mỗi task có đúng 1 người Accountable để tránh diffusion of responsibility.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Bạn hiểu thế nào về DMAIC trong Six Sigma? Vai trò của BA trong mỗi phase?
* **expected_key_points:**
  - id: KP1
    content: Define, Measure, Analyze, Improve, Control
    keypoint_weight: 0.4
    description: 5 phases cải tiến quy trình: xác định vấn đề, đo lường, phân tích nguyên nhân, cải tiến, kiểm soát.
  - id: KP2
    content: BA trong Define và Analyze
    keypoint_weight: 0.35
    description: BA đóng vai trò chính trong thu thập VOC, tạo process map, root cause analysis.
  - id: KP3
    content: Data-driven decision making
    keypoint_weight: 0.25
    description: Mỗi phase yêu cầu dữ liệu định lượng để ra quyết định, BA hỗ trợ data collection và analysis.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn được yêu cầu thực hiện process mining trên dữ liệu event log từ hệ thống SAP. Mô tả approach và các insight mong đợi.
* **expected_key_points:**
  - id: KP1
    content: Extract event log từ SAP
    keypoint_weight: 0.25
    description: Xác định relevant tables (BKPF, EKKO, VBAK), extract Case ID, Activity, Timestamp, Resource.
  - id: KP2
    content: Process discovery và conformance checking
    keypoint_weight: 0.3
    description: Dùng tool (Celonis, Disco) để tự động tạo process model, so sánh với intended process.
  - id: KP3
    content: Variant analysis và bottleneck detection
    keypoint_weight: 0.25
    description: Phân tích các process variants, xác định bottleneck qua waiting time analysis.
  - id: KP4
    content: Actionable recommendations
    keypoint_weight: 0.2
    description: Đề xuất cải tiến dựa trên data: loại bỏ rework loops, tự động hóa manual steps.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Thiết kế một KPI dashboard cho C-level management. Bạn sẽ chọn những metrics nào và tại sao?
* **expected_key_points:**
  - id: KP1
    content: Balanced Scorecard framework
    keypoint_weight: 0.3
    description: Sử dụng 4 perspectives: Financial, Customer, Internal Process, Learning & Growth.
  - id: KP2
    content: Leading vs Lagging indicators
    keypoint_weight: 0.25
    description: Kết hợp leading indicators (pipeline value, NPS trend) với lagging (revenue, profit margin).
  - id: KP3
    content: Data visualization best practices
    keypoint_weight: 0.25
    description: Chọn chart type phù hợp, progressive disclosure, drill-down capability.
  - id: KP4
    content: Real-time vs periodic refresh
    keypoint_weight: 0.2
    description: Xác định metrics nào cần real-time (operational) vs monthly/quarterly (strategic).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn áp dụng Value Stream Mapping (VSM) để cải tiến quy trình order fulfillment. Mô tả các bước và deliverables.
* **expected_key_points:**
  - id: KP1
    content: Current State Map
    keypoint_weight: 0.3
    description: Vẽ VSM hiện tại: process steps, inventory levels, cycle time, lead time, information flow.
  - id: KP2
    content: Identify 7 wastes (Muda)
    keypoint_weight: 0.25
    description: Phát hiện Transportation, Inventory, Motion, Waiting, Overproduction, Overprocessing, Defects.
  - id: KP3
    content: Future State Map với kaizen bursts
    keypoint_weight: 0.25
    description: Thiết kế quy trình tương lai với cải tiến cụ thể, takt time calculation.
  - id: KP4
    content: Implementation plan với metrics
    keypoint_weight: 0.2
    description: Tạo action plan với responsible person, timeline, và success metrics cho mỗi kaizen.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn sẽ thực hiện Root Cause Analysis cho vấn đề 'tỷ lệ khách hàng rời bỏ tăng 20%'. Trình bày phương pháp.
* **expected_key_points:**
  - id: KP1
    content: Fishbone diagram (Ishikawa)
    keypoint_weight: 0.3
    description: Phân tích theo 6M: Man, Machine, Method, Material, Measurement, Mother Nature.
  - id: KP2
    content: 5 Whys analysis
    keypoint_weight: 0.25
    description: Đặt câu hỏi 'Tại sao' liên tiếp để đi sâu từ symptom đến root cause.
  - id: KP3
    content: Data analysis hỗ trợ
    keypoint_weight: 0.25
    description: Phân tích cohort churn, correlation analysis với các yếu tố: pricing, service quality, competitor.
  - id: KP4
    content: Prioritize causes và action plan
    keypoint_weight: 0.2
    description: Dùng Pareto principle để focus vào 20% nguyên nhân gây 80% vấn đề.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế một Continuous Improvement Framework cho tổ chức 500+ nhân viên. Bao gồm governance, methodology, và technology enablers.
* **expected_key_points:**
  - id: KP1
    content: Governance structure
    keypoint_weight: 0.3
    description: Process Excellence Council, dedicated CI team, process owners network, reporting cadence.
  - id: KP2
    content: Methodology selection và adaptation
    keypoint_weight: 0.25
    description: Kết hợp Lean và Six Sigma, scaled cho organization size, training curriculum (Yellow/Green/Black Belt).
  - id: KP3
    content: Technology stack cho CI
    keypoint_weight: 0.25
    description: Process mining tools, BPM suites, collaboration platforms, idea management system.
  - id: KP4
    content: Change management và culture
    keypoint_weight: 0.2
    description: Embedding CI mindset, recognition programs, knowledge sharing, CI maturity model.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích và đề xuất giải pháp cho vấn đề: 'Lead time của quy trình procure-to-pay là 45 ngày, mục tiêu giảm xuống 15 ngày'. Approach end-to-end.
* **expected_key_points:**
  - id: KP1
    content: End-to-end process mapping với timing
    keypoint_weight: 0.25
    description: Map toàn bộ P2P process: requisition → approval → PO → goods receipt → invoice → payment, đo thời gian mỗi step.
  - id: KP2
    content: Bottleneck analysis và automation opportunities
    keypoint_weight: 0.3
    description: Xác định steps chiếm nhiều thời gian nhất, đánh giá khả năng RPA/workflow automation.
  - id: KP3
    content: Policy và approval matrix redesign
    keypoint_weight: 0.25
    description: Đề xuất thay đổi approval thresholds, parallel approvals, auto-approval cho low-value POs.
  - id: KP4
    content: Implementation phased approach
    keypoint_weight: 0.2
    description: Quick wins (tháng 1-2), medium-term improvements (tháng 3-6), long-term automation (tháng 6-12).

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Bạn cần xây dựng một Business Process Architecture cho công ty fintech startup đang scale. Mô tả approach và các layers.
* **expected_key_points:**
  - id: KP1
    content: Process architecture layers
    keypoint_weight: 0.3
    description: Strategic processes (governance), Core processes (value chain), Supporting processes (HR, IT, Finance).
  - id: KP2
    content: Process decomposition hierarchy
    keypoint_weight: 0.25
    description: Level 0 (value chain) → Level 1 (process groups) → Level 2 (processes) → Level 3 (sub-processes).
  - id: KP3
    content: Alignment với business capabilities
    keypoint_weight: 0.25
    description: Map processes với business capability model, xác định gaps và redundancies.
  - id: KP4
    content: Scalability considerations cho fintech
    keypoint_weight: 0.2
    description: Regulatory compliance processes, API-first design, automated monitoring, audit trails.

