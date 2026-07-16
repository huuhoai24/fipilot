# Bộ Câu Hỏi Phỏng Vấn Business Analyst (Level 3) - E-commerce & Payment Systems (16)

* **Role:** Business Analyst
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Bạn phân tích yêu cầu cho hệ thống thanh toán online. Các payment flow chính cần document là gì?
* **expected_key_points:**
  - id: KP1
    content: Payment lifecycle
    keypoint_weight: 0.4
    description: Authorization → Capture → Settlement → Reconciliation. Mỗi step có actors, data, và error handling riêng.
  - id: KP2
    content: Payment methods diversity
    keypoint_weight: 0.35
    description: Credit/debit card, e-wallet, bank transfer, COD, installment. Mỗi method có flow khác nhau.
  - id: KP3
    content: PCI-DSS compliance basics
    keypoint_weight: 0.25
    description: Tokenization, encryption, không store CVV, SAQ requirements, third-party payment gateway integration.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Shopping cart abandonment rate cao. Bạn sẽ phân tích vấn đề này bằng data nào và đề xuất gì?
* **expected_key_points:**
  - id: KP1
    content: Funnel analysis
    keypoint_weight: 0.4
    description: Analyze drop-off at each checkout step: cart → address → payment → confirmation. Identify highest drop-off.
  - id: KP2
    content: User behavior data
    keypoint_weight: 0.3
    description: Session recordings, heatmaps, exit survey responses, device/browser breakdown.
  - id: KP3
    content: Common solutions
    keypoint_weight: 0.3
    description: Guest checkout, progress indicator, save cart, multiple payment options, transparent pricing.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Mô tả yêu cầu cho tính năng Product Catalog management trong e-commerce platform.
* **expected_key_points:**
  - id: KP1
    content: Product data model
    keypoint_weight: 0.4
    description: SKU, variants (size, color), categories/subcategories, attributes, images, pricing, inventory status.
  - id: KP2
    content: Content management requirements
    keypoint_weight: 0.35
    description: Rich text description, SEO metadata, image management, bulk upload/update, localization.
  - id: KP3
    content: Search và filtering
    keypoint_weight: 0.25
    description: Faceted search, full-text search, sorting options, product recommendations integration.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn thiết kế requirements cho hệ thống Order Management xử lý multi-channel orders (web, mobile, marketplace). Các components chính?
* **expected_key_points:**
  - id: KP1
    content: Unified order lifecycle
    keypoint_weight: 0.3
    description: Order creation → payment verification → fulfillment → shipping → delivery → returns. Status tracking across channels.
  - id: KP2
    content: Inventory allocation logic
    keypoint_weight: 0.25
    description: Real-time inventory check, reservation mechanism, allocation priority rules, backorder handling.
  - id: KP3
    content: Split shipment và partial fulfillment
    keypoint_weight: 0.25
    description: Logic cho splitting orders across warehouses, partial delivery rules, customer notification.
  - id: KP4
    content: Returns và refund processing
    keypoint_weight: 0.2
    description: Return reasons, return window policies, refund methods, restocking logic, exchange workflow.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn phân tích yêu cầu cho Loyalty/Rewards program. Mô tả point system design và integration points.
* **expected_key_points:**
  - id: KP1
    content: Points earning rules
    keypoint_weight: 0.3
    description: Earn rate per spend, bonus events, product-specific multipliers, tier-based acceleration.
  - id: KP2
    content: Points redemption và expiry
    keypoint_weight: 0.25
    description: Redemption options (discount, products, experiences), minimum threshold, expiry policies, partial redemption.
  - id: KP3
    content: Tier management
    keypoint_weight: 0.25
    description: Tier levels, qualification criteria, benefits per tier, upgrade/downgrade logic, tier maintenance period.
  - id: KP4
    content: Integration với existing systems
    keypoint_weight: 0.2
    description: POS, e-commerce, CRM, accounting integration. Real-time points balance, cross-channel earning/redemption.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn document requirements cho fraud detection system trong e-commerce. Risk signals và decision logic?
* **expected_key_points:**
  - id: KP1
    content: Risk signal identification
    keypoint_weight: 0.3
    description: Velocity checks, address mismatch, device fingerprint, IP geolocation, purchase pattern anomalies.
  - id: KP2
    content: Risk scoring model requirements
    keypoint_weight: 0.25
    description: Weighted scoring model, threshold-based actions (auto-approve, review, block), dynamic thresholds.
  - id: KP3
    content: Manual review workflow
    keypoint_weight: 0.25
    description: Queue management, review SLA, escalation rules, decision tracking, analyst performance metrics.
  - id: KP4
    content: False positive management
    keypoint_weight: 0.2
    description: Customer friction balance, appeal process, whitelist management, model feedback loop.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn thiết kế promotion engine cho e-commerce platform. Mô tả requirements cho complex promotion scenarios.
* **expected_key_points:**
  - id: KP1
    content: Promotion types taxonomy
    keypoint_weight: 0.3
    description: Percentage discount, fixed amount, BOGO, bundle pricing, free shipping, tiered discount.
  - id: KP2
    content: Eligibility rules
    keypoint_weight: 0.25
    description: Customer segment, product category, minimum order, time window, channel-specific, usage limits.
  - id: KP3
    content: Stacking và conflict resolution
    keypoint_weight: 0.25
    description: Multiple promotions stacking rules, best-price guarantee, exclusive vs combinable, priority ordering.
  - id: KP4
    content: Reporting và analytics
    keypoint_weight: 0.2
    description: Promotion performance metrics: redemption rate, incremental revenue, margin impact, customer acquisition cost.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế requirements cho Marketplace platform kết nối sellers và buyers. BA deliverables cho two-sided marketplace?
* **expected_key_points:**
  - id: KP1
    content: Seller management requirements
    keypoint_weight: 0.3
    description: Seller onboarding, verification, product listing management, commission structure, payout schedule.
  - id: KP2
    content: Buyer experience requirements
    keypoint_weight: 0.25
    description: Multi-seller cart, combined checkout, delivery expectation management, review/rating system.
  - id: KP3
    content: Trust và safety requirements
    keypoint_weight: 0.25
    description: Dispute resolution workflow, escrow payment, seller rating algorithm, content moderation.
  - id: KP4
    content: Platform economics model
    keypoint_weight: 0.2
    description: Commission calculation, payment split, tax handling, refund policies, incentive programs.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích requirements cho subscription commerce platform với recurring billing, dunning management, và churn prevention.
* **expected_key_points:**
  - id: KP1
    content: Subscription lifecycle management
    keypoint_weight: 0.3
    description: Trial → active → paused → cancelled → reactivated. State transitions, triggers, và business rules.
  - id: KP2
    content: Recurring billing và dunning
    keypoint_weight: 0.25
    description: Payment retry logic, grace period, dunning email sequence, card update reminders, involuntary churn handling.
  - id: KP3
    content: Plan management flexibility
    keypoint_weight: 0.25
    description: Plan changes (upgrade/downgrade), proration logic, add-ons, metered billing, annual vs monthly.
  - id: KP4
    content: Churn prevention features
    keypoint_weight: 0.2
    description: Cancellation flow with save offers, pause option, feedback collection, win-back campaigns.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Bạn cần xây dựng requirements cho Cross-border E-commerce platform bán hàng tại 5 quốc gia ASEAN. Key considerations?
* **expected_key_points:**
  - id: KP1
    content: Multi-currency và pricing
    keypoint_weight: 0.3
    description: Currency conversion, local pricing strategy, payment method availability per country, exchange rate management.
  - id: KP2
    content: Logistics và customs
    keypoint_weight: 0.25
    description: Cross-border shipping, customs documentation, duties/taxes calculation, last-mile delivery partners per country.
  - id: KP3
    content: Regulatory compliance
    keypoint_weight: 0.25
    description: Consumer protection laws, data privacy (PDPA, etc.), product import restrictions, tax registration per country.
  - id: KP4
    content: Localization requirements
    keypoint_weight: 0.2
    description: Language, content adaptation, local customer support, payment methods (GrabPay, GCash, OVO, etc.).

