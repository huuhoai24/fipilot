# Bộ Câu Hỏi Phỏng Vấn Business Analyst (Level 3) - Data Analysis & SQL cho BA (3)

* **Role:** Business Analyst
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Bạn sử dụng SQL như thế nào trong công việc BA hàng ngày? Cho ví dụ query phức tạp bạn đã viết.
* **expected_key_points:**
  - id: KP1
    content: Ad-hoc data extraction
    keypoint_weight: 0.35
    description: Viết queries để trích xuất dữ liệu phục vụ analysis, reporting, và requirements validation.
  - id: KP2
    content: JOINs và aggregation
    keypoint_weight: 0.35
    description: Sử dụng INNER/LEFT JOIN nhiều bảng, GROUP BY, HAVING, window functions cho complex reporting.
  - id: KP3
    content: Data profiling và quality check
    keypoint_weight: 0.3
    description: Dùng SQL để kiểm tra data quality: NULL values, duplicates, outliers, referential integrity.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Phân biệt giữa quantitative và qualitative data analysis. Khi nào BA nên sử dụng loại nào?
* **expected_key_points:**
  - id: KP1
    content: Quantitative: số liệu, thống kê
    keypoint_weight: 0.35
    description: Phân tích dữ liệu số: revenue trends, conversion rates, user metrics. Dùng khi cần đo lường chính xác.
  - id: KP2
    content: Qualitative: phỏng vấn, survey mở
    keypoint_weight: 0.35
    description: Phân tích thông tin phi cấu trúc: interview notes, feedback, observation. Dùng khi cần hiểu 'tại sao'.
  - id: KP3
    content: Mixed methods approach
    keypoint_weight: 0.3
    description: Kết hợp cả hai: quantitative để xác định vấn đề, qualitative để hiểu nguyên nhân sâu xa.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích Data Dictionary và vai trò của nó trong quản lý yêu cầu. Bạn tạo Data Dictionary cho những dự án nào?
* **expected_key_points:**
  - id: KP1
    content: Định nghĩa và cấu trúc
    keypoint_weight: 0.4
    description: Tài liệu mô tả: field name, data type, length, format, valid values, business rules cho mỗi data element.
  - id: KP2
    content: Dùng cho system integration và migration
    keypoint_weight: 0.35
    description: Quan trọng khi tích hợp hệ thống, data migration, hoặc xây hệ thống mới cần thống nhất data definitions.
  - id: KP3
    content: Single source of truth
    keypoint_weight: 0.25
    description: Data Dictionary là tài liệu tham chiếu chung cho BA, Dev, QA, tránh hiểu sai data.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn cần phân tích dữ liệu khách hàng để xây dựng customer segmentation. Mô tả approach từ data đến actionable insights.
* **expected_key_points:**
  - id: KP1
    content: Data collection và preparation
    keypoint_weight: 0.25
    description: Thu thập demographics, transaction history, behavior data. Cleansing, handling missing values.
  - id: KP2
    content: Segmentation methodology
    keypoint_weight: 0.3
    description: RFM analysis (Recency, Frequency, Monetary), hoặc clustering algorithms nếu data đủ lớn.
  - id: KP3
    content: Segment profiling
    keypoint_weight: 0.25
    description: Mô tả đặc điểm từng segment, naming convention dễ hiểu cho business (VIP, At-risk, New).
  - id: KP4
    content: Actionable recommendations
    keypoint_weight: 0.2
    description: Đề xuất chiến lược marketing, pricing, service level khác nhau cho từng segment.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Mô tả cách bạn thiết kế data requirements cho một báo cáo BI (Business Intelligence). Các bước chính là gì?
* **expected_key_points:**
  - id: KP1
    content: Business questions trước tiên
    keypoint_weight: 0.3
    description: Xác định câu hỏi kinh doanh mà báo cáo cần trả lời, ai sử dụng, tần suất xem.
  - id: KP2
    content: Data source identification
    keypoint_weight: 0.25
    description: Map data elements với source systems, đánh giá data availability và quality.
  - id: KP3
    content: Dimension và Measure definition
    keypoint_weight: 0.25
    description: Định nghĩa dimensions (time, product, region) và measures (revenue, quantity) cho data model.
  - id: KP4
    content: Calculation logic và business rules
    keypoint_weight: 0.2
    description: Document rõ ràng formulas, filters, drill-down hierarchy, và exception handling.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn phát hiện data quality issue trong quá trình phân tích. Bạn xử lý và report vấn đề này như thế nào?
* **expected_key_points:**
  - id: KP1
    content: Issue identification và classification
    keypoint_weight: 0.3
    description: Phân loại: completeness, accuracy, consistency, timeliness. Đánh giá impact trên analysis results.
  - id: KP2
    content: Root cause investigation
    keypoint_weight: 0.25
    description: Trace lại source: data entry error, system bug, ETL failure, business rule change.
  - id: KP3
    content: Short-term mitigation
    keypoint_weight: 0.2
    description: Workaround cho analysis hiện tại: data imputation, exclusion rules, caveats trong report.
  - id: KP4
    content: Long-term data governance
    keypoint_weight: 0.25
    description: Đề xuất data quality rules, automated validation, data stewardship responsibilities.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn áp dụng A/B testing analysis trong vai trò BA như thế nào? Cho ví dụ scenario và cách đọc kết quả.
* **expected_key_points:**
  - id: KP1
    content: Hypothesis formulation
    keypoint_weight: 0.25
    description: Định nghĩa null/alternative hypothesis, primary metric, và minimum detectable effect.
  - id: KP2
    content: Sample size và test duration
    keypoint_weight: 0.25
    description: Tính sample size cần thiết dựa trên statistical power, traffic volume, và baseline conversion rate.
  - id: KP3
    content: Statistical significance
    keypoint_weight: 0.3
    description: Hiểu p-value, confidence interval, và khi nào kết quả đủ tin cậy để ra quyết định.
  - id: KP4
    content: Business interpretation
    keypoint_weight: 0.2
    description: Chuyển đổi kết quả thống kê thành business impact: revenue lift, cost savings projection.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế data strategy cho dự án chuyển đổi từ legacy monolithic database sang microservices architecture. BA cần deliver những gì?
* **expected_key_points:**
  - id: KP1
    content: Data domain decomposition
    keypoint_weight: 0.3
    description: Phân tích bounded contexts, xác định data ownership cho từng microservice, shared data strategy.
  - id: KP2
    content: Data migration plan
    keypoint_weight: 0.25
    description: Phasing strategy, data mapping, transformation rules, rollback plan, parallel run period.
  - id: KP3
    content: API contract definition
    keypoint_weight: 0.25
    description: Định nghĩa API specs cho data exchange giữa services, versioning strategy, backward compatibility.
  - id: KP4
    content: Data consistency patterns
    keypoint_weight: 0.2
    description: Eventual consistency vs strong consistency trade-offs, saga pattern cho distributed transactions.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Bạn cần xây dựng business requirements cho một Data Warehouse phục vụ enterprise reporting. Trình bày approach và key deliverables.
* **expected_key_points:**
  - id: KP1
    content: Kimball vs Inmon methodology selection
    keypoint_weight: 0.25
    description: Đánh giá bottom-up (dimensional modeling) vs top-down (normalized) dựa trên business needs.
  - id: KP2
    content: Subject area analysis và conformed dimensions
    keypoint_weight: 0.3
    description: Xác định subject areas (Sales, Finance, HR), thiết kế conformed dimensions cho cross-functional reporting.
  - id: KP3
    content: ETL requirements specification
    keypoint_weight: 0.25
    description: Document source-to-target mapping, transformation rules, data refresh frequency, error handling.
  - id: KP4
    content: Data governance và security requirements
    keypoint_weight: 0.2
    description: Access control matrix, data classification, GDPR/privacy compliance, audit logging.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích yêu cầu cho hệ thống Real-time Analytics Dashboard với 10,000+ concurrent users. Các non-functional requirements quan trọng nào cần xem xét?
* **expected_key_points:**
  - id: KP1
    content: Performance requirements
    keypoint_weight: 0.3
    description: Dashboard load time < 3s, data refresh < 5s, query response time SLA cho different complexity levels.
  - id: KP2
    content: Scalability và availability
    keypoint_weight: 0.25
    description: Horizontal scaling, 99.9% uptime SLA, disaster recovery, geographic distribution.
  - id: KP3
    content: Data freshness và consistency
    keypoint_weight: 0.25
    description: Định nghĩa acceptable data latency, stream processing vs batch, cache invalidation strategy.
  - id: KP4
    content: Security và multi-tenancy
    keypoint_weight: 0.2
    description: Row-level security, role-based access, data isolation giữa các tenants, audit trails.

