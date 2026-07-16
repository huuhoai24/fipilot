# Bộ Câu Hỏi Phỏng Vấn Business Analyst (Level 3) - Healthcare & Regulated Industries (17)

* **Role:** Business Analyst
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** HL7 và FHIR standards trong healthcare IT là gì? BA cần hiểu ở mức nào?
* **expected_key_points:**
  - id: KP1
    content: HL7 v2 messaging standard
    keypoint_weight: 0.35
    description: Standard cho healthcare data exchange: ADT, ORM, ORU messages. Pipe-delimited format, point-to-point integration.
  - id: KP2
    content: FHIR (Fast Healthcare Interoperability Resources)
    keypoint_weight: 0.35
    description: Modern RESTful API standard, JSON/XML resources (Patient, Observation, MedicationRequest), easier integration.
  - id: KP3
    content: BA knowledge requirements
    keypoint_weight: 0.3
    description: Hiểu data elements, use cases, mapping giữa clinical workflow và technical standards. Không cần code.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** HIPAA compliance ảnh hưởng thế nào đến requirements gathering trong dự án healthcare?
* **expected_key_points:**
  - id: KP1
    content: PHI (Protected Health Information)
    keypoint_weight: 0.4
    description: Xác định data elements thuộc PHI, minimum necessary principle, de-identification requirements.
  - id: KP2
    content: Security Rule requirements
    keypoint_weight: 0.35
    description: Access controls, audit logging, encryption at rest/transit, backup/recovery, breach notification.
  - id: KP3
    content: Impact trên BA activities
    keypoint_weight: 0.25
    description: NDA requirements, screen sharing restrictions, test data anonymization, documentation security classification.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Clinical workflow trong bệnh viện khác gì business workflow thông thường? BA cần adjust approach thế nào?
* **expected_key_points:**
  - id: KP1
    content: Patient safety priority
    keypoint_weight: 0.4
    description: Mọi quyết định design phải xem xét patient safety. Error prevention, clinical decision support, alert fatigue.
  - id: KP2
    content: Interdisciplinary stakeholders
    keypoint_weight: 0.35
    description: Doctors, nurses, pharmacists, lab techs, admin staff - mỗi nhóm có workflow và terminology riêng.
  - id: KP3
    content: Regulatory constraints
    keypoint_weight: 0.25
    description: FDA regulations cho medical devices/software, clinical validation requirements, audit trail obligations.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn phân tích yêu cầu cho Electronic Health Record (EHR) system. Mô tả key modules và integration requirements.
* **expected_key_points:**
  - id: KP1
    content: Core EHR modules
    keypoint_weight: 0.3
    description: Patient demographics, clinical documentation, order entry (CPOE), medication management, lab results, imaging.
  - id: KP2
    content: Interoperability requirements
    keypoint_weight: 0.25
    description: HL7/FHIR interfaces với lab systems, pharmacy, billing, insurance, health information exchange (HIE).
  - id: KP3
    content: Clinical Decision Support (CDS)
    keypoint_weight: 0.25
    description: Drug interaction alerts, allergy checking, clinical guidelines integration, evidence-based recommendations.
  - id: KP4
    content: Usability cho clinical users
    keypoint_weight: 0.2
    description: Minimize clicks, voice input support, mobile rounding, customizable views per specialty, offline capability.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn document requirements cho telemedicine platform. Key features và regulatory considerations?
* **expected_key_points:**
  - id: KP1
    content: Video consultation requirements
    keypoint_weight: 0.25
    description: HD video/audio, screen sharing, file exchange, waiting room, multi-party calls, bandwidth adaptive.
  - id: KP2
    content: Clinical documentation integration
    keypoint_weight: 0.3
    description: Visit notes, prescriptions, referrals, lab orders integrated với EHR. Templates per specialty.
  - id: KP3
    content: Regulatory compliance
    keypoint_weight: 0.25
    description: State licensing, informed consent, prescription rules, recording consent, data residency requirements.
  - id: KP4
    content: Patient experience
    keypoint_weight: 0.2
    description: Easy scheduling, reminders, device compatibility, accessibility, technical support, post-visit survey.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** BA role trong Clinical Trial Management System (CTMS). Mô tả requirements và stakeholders.
* **expected_key_points:**
  - id: KP1
    content: Study protocol management
    keypoint_weight: 0.3
    description: Protocol design, site selection, enrollment tracking, visit schedules, randomization requirements.
  - id: KP2
    content: Regulatory submissions
    keypoint_weight: 0.25
    description: FDA/EMA submission workflows, document management, audit trail, 21 CFR Part 11 compliance.
  - id: KP3
    content: Data collection và monitoring
    keypoint_weight: 0.25
    description: Electronic Data Capture (EDC), query management, source data verification, safety reporting.
  - id: KP4
    content: Multi-stakeholder coordination
    keypoint_weight: 0.2
    description: Sponsor, CRO, sites, IRB, regulatory agencies - different views và access levels needed.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn phân tích requirements cho Patient Portal tích hợp với hệ thống bệnh viện. Mô tả features và security considerations.
* **expected_key_points:**
  - id: KP1
    content: Patient-facing features
    keypoint_weight: 0.3
    description: Appointment scheduling, lab results viewing, medication list, billing/payment, secure messaging with providers.
  - id: KP2
    content: Identity verification và authentication
    keypoint_weight: 0.25
    description: Patient identity proofing, MFA, proxy access (parents, caregivers), password recovery.
  - id: KP3
    content: EHR integration requirements
    keypoint_weight: 0.25
    description: Real-time data sync, FHIR APIs, patient-mediated data exchange, consent management.
  - id: KP4
    content: Accessibility và multilingual
    keypoint_weight: 0.2
    description: WCAG compliance, health literacy considerations, multilingual support, elderly-friendly design.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế requirements cho AI-powered Medical Imaging Analysis system (radiology AI). BA approach cho regulated medical software?
* **expected_key_points:**
  - id: KP1
    content: FDA SaMD (Software as Medical Device) classification
    keypoint_weight: 0.3
    description: Determine classification level, intended use statement, indications for use, risk categorization.
  - id: KP2
    content: Clinical validation requirements
    keypoint_weight: 0.25
    description: Performance benchmarks: sensitivity, specificity, AUC. Clinical trial design, ground truth establishment.
  - id: KP3
    content: Workflow integration requirements
    keypoint_weight: 0.25
    description: DICOM integration, PACS workflow, radiologist review/override, report generation, worklist prioritization.
  - id: KP4
    content: Post-market surveillance
    keypoint_weight: 0.2
    description: Ongoing performance monitoring, adverse event reporting, model drift detection, retraining requirements.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích requirements cho Healthcare Data Warehouse phục vụ population health management. BA deliverables?
* **expected_key_points:**
  - id: KP1
    content: Data integration across care continuum
    keypoint_weight: 0.3
    description: EHR, claims, pharmacy, labs, social determinants. Data harmonization, terminology mapping (ICD-10, SNOMED, LOINC).
  - id: KP2
    content: Population health analytics requirements
    keypoint_weight: 0.25
    description: Risk stratification, care gap identification, chronic disease management, predictive models for readmission.
  - id: KP3
    content: Privacy-preserving analytics
    keypoint_weight: 0.25
    description: De-identification, aggregation rules, minimum cell size, consent management, data governance policies.
  - id: KP4
    content: Reporting requirements
    keypoint_weight: 0.2
    description: Quality measures (HEDIS, MIPS), regulatory reporting, payer contracts, executive dashboards.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Bạn cần xây dựng requirements cho interoperable health information exchange (HIE) platform kết nối 50+ facilities. End-to-end approach?
* **expected_key_points:**
  - id: KP1
    content: Trust framework requirements
    keypoint_weight: 0.3
    description: Participant agreements, data sharing policies, consent management, identity federation, certificate management.
  - id: KP2
    content: Technical interoperability
    keypoint_weight: 0.25
    description: FHIR R4 APIs, Consolidated CDA documents, Direct messaging, query-based exchange, event notifications.
  - id: KP3
    content: Data governance và quality
    keypoint_weight: 0.25
    description: Master Patient Index (MPI), record matching algorithms, data quality standards, duplicate management.
  - id: KP4
    content: Sustainability model
    keypoint_weight: 0.2
    description: Funding model, value proposition per participant type, operational governance, technology evolution plan.

