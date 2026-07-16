# Bộ Câu Hỏi Phỏng Vấn Business Analyst (Level 3) - Security & Compliance Analysis (19)

* **Role:** Business Analyst
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Bạn incorporate security requirements vào functional specifications như thế nào? Cho ví dụ cho web application.
* **expected_key_points:**
  - id: KP1
    content: Authentication và authorization
    keypoint_weight: 0.4
    description: MFA requirements, role-based access control, session management, password policies.
  - id: KP2
    content: Data protection
    keypoint_weight: 0.35
    description: Encryption at rest/transit, data classification, PII handling, data masking in non-production.
  - id: KP3
    content: OWASP Top 10 awareness
    keypoint_weight: 0.25
    description: Injection prevention, XSS protection, broken authentication, sensitive data exposure requirements.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** GDPR ảnh hưởng thế nào đến data requirements cho ứng dụng serving EU customers?
* **expected_key_points:**
  - id: KP1
    content: Consent management requirements
    keypoint_weight: 0.4
    description: Explicit consent collection, granular consent options, consent withdrawal capability, consent audit trail.
  - id: KP2
    content: Data subject rights
    keypoint_weight: 0.35
    description: Right to access, rectification, erasure, portability, restriction of processing. System capability requirements.
  - id: KP3
    content: Data processing documentation
    keypoint_weight: 0.25
    description: Records of processing activities, DPA with processors, DPIA for high-risk processing, breach notification.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Bạn tạo access control matrix cho enterprise application. Mô tả approach và format.
* **expected_key_points:**
  - id: KP1
    content: RBAC (Role-Based Access Control)
    keypoint_weight: 0.4
    description: Define roles, map roles to permissions, minimize privilege principle, role hierarchy.
  - id: KP2
    content: Permission granularity
    keypoint_weight: 0.35
    description: CRUD permissions per data entity, field-level security, record-level security (row-level).
  - id: KP3
    content: Review và audit process
    keypoint_weight: 0.25
    description: Periodic access review, separation of duties validation, access certification campaigns.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn document security requirements cho mobile banking application. Mô tả threat model và mitigation requirements.
* **expected_key_points:**
  - id: KP1
    content: STRIDE threat model
    keypoint_weight: 0.3
    description: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege.
  - id: KP2
    content: Mobile-specific security requirements
    keypoint_weight: 0.25
    description: Secure storage, certificate pinning, jailbreak/root detection, biometric authentication, app shielding.
  - id: KP3
    content: Transaction security
    keypoint_weight: 0.25
    description: Transaction signing, OTP verification, device binding, geo-fencing, velocity checks.
  - id: KP4
    content: Incident response requirements
    keypoint_weight: 0.2
    description: Remote wipe capability, account freeze, fraud alert notifications, recovery procedures.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn phân tích compliance requirements cho hệ thống xử lý payment card data (PCI-DSS). BA deliverables?
* **expected_key_points:**
  - id: KP1
    content: Scope reduction analysis
    keypoint_weight: 0.3
    description: Identify cardholder data flows, minimize data touchpoints, tokenization strategy to reduce PCI scope.
  - id: KP2
    content: 12 PCI-DSS requirements mapping
    keypoint_weight: 0.25
    description: Map technical requirements per PCI domain: network security, access control, monitoring, testing, policy.
  - id: KP3
    content: Evidence collection requirements
    keypoint_weight: 0.25
    description: What evidence needed for audit: logs, configurations, policies, test results. Automated evidence collection.
  - id: KP4
    content: Continuous compliance monitoring
    keypoint_weight: 0.2
    description: File integrity monitoring, vulnerability scanning schedule, penetration testing requirements, log review.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Mô tả cách bạn conduct Privacy Impact Assessment (PIA) cho new data processing activity.
* **expected_key_points:**
  - id: KP1
    content: Data flow mapping
    keypoint_weight: 0.3
    description: Map personal data collection, processing, storage, sharing, deletion. Identify data controllers và processors.
  - id: KP2
    content: Risk assessment
    keypoint_weight: 0.25
    description: Identify privacy risks: unauthorized access, data breach, excessive collection, non-compliance, reputational.
  - id: KP3
    content: Mitigation measures
    keypoint_weight: 0.25
    description: Privacy enhancing technologies, data minimization, anonymization/pseudonymization, access controls.
  - id: KP4
    content: Documentation và approval
    keypoint_weight: 0.2
    description: PIA report structure, DPO review, management approval, periodic review schedule.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn thiết kế audit trail requirements cho financial system. Mô tả data capture và retention specifications.
* **expected_key_points:**
  - id: KP1
    content: What to log
    keypoint_weight: 0.3
    description: User actions, data changes (before/after values), login/logout, access attempts, system events, configuration changes.
  - id: KP2
    content: Log format và integrity
    keypoint_weight: 0.25
    description: Structured format (JSON), timestamp synchronization, tamper-proof storage, log signing.
  - id: KP3
    content: Retention và archival
    keypoint_weight: 0.25
    description: Retention periods per regulation, archival strategy, searchability, legal hold capability.
  - id: KP4
    content: Monitoring và alerting
    keypoint_weight: 0.2
    description: Real-time anomaly detection, privileged access monitoring, failed access attempts, alerting thresholds.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế Zero Trust Architecture requirements cho enterprise migration. BA deliverables và cross-team collaboration?
* **expected_key_points:**
  - id: KP1
    content: Zero Trust principles mapping to requirements
    keypoint_weight: 0.3
    description: Never trust, always verify. Micro-segmentation, least privilege, continuous authentication, device trust.
  - id: KP2
    content: Identity-centric security requirements
    keypoint_weight: 0.25
    description: Identity provider integration, conditional access policies, privileged access management, identity governance.
  - id: KP3
    content: Application-level requirements
    keypoint_weight: 0.25
    description: API gateway security, service mesh requirements, data classification-driven access, encryption everywhere.
  - id: KP4
    content: Phased implementation plan
    keypoint_weight: 0.2
    description: Priority assets first, quick wins (MFA everywhere), medium-term (micro-segmentation), long-term (full ZTA).

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Bạn cần xây dựng requirements cho SOC (Security Operations Center) platform. Mô tả use cases và automation requirements.
* **expected_key_points:**
  - id: KP1
    content: SIEM requirements
    keypoint_weight: 0.3
    description: Log sources, correlation rules, alert prioritization, dashboard requirements, retention policies.
  - id: KP2
    content: SOAR automation requirements
    keypoint_weight: 0.25
    description: Playbook design cho common incidents, automated enrichment, response actions, human approval gates.
  - id: KP3
    content: Threat intelligence integration
    keypoint_weight: 0.25
    description: IOC feeds, threat intelligence platform integration, automated blocking, threat hunting capabilities.
  - id: KP4
    content: Metrics và reporting
    keypoint_weight: 0.2
    description: MTTD, MTTR, false positive rate, alert volume trends, analyst productivity, compliance reporting.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích requirements cho Data Loss Prevention (DLP) program covering email, endpoint, cloud. BA approach cho enterprise-wide rollout?
* **expected_key_points:**
  - id: KP1
    content: Data classification scheme
    keypoint_weight: 0.3
    description: Classification levels (Public, Internal, Confidential, Restricted), classification criteria, labeling requirements.
  - id: KP2
    content: DLP policy requirements
    keypoint_weight: 0.25
    description: Content inspection rules, context-aware policies, action policies (block, encrypt, notify), exceptions management.
  - id: KP3
    content: Channel coverage requirements
    keypoint_weight: 0.25
    description: Email DLP, endpoint DLP (USB, print), cloud DLP (SaaS, IaaS), network DLP. Coverage priorities.
  - id: KP4
    content: Incident management workflow
    keypoint_weight: 0.2
    description: DLP incident triage, investigation workflow, false positive handling, policy violation reporting.

