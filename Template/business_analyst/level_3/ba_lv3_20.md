# Bộ Câu Hỏi Phỏng Vấn Business Analyst (Level 3) - Emerging Technologies & Innovation (20)

* **Role:** Business Analyst
* **Level:** Level 3
* **Experience:** 4 - 5 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.1 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** BA cần hiểu blockchain ở mức nào? Khi nào blockchain là giải pháp phù hợp cho business problem?
* **expected_key_points:**
  - id: KP1
    content: Blockchain fundamentals cho BA
    keypoint_weight: 0.35
    description: Distributed ledger, immutability, consensus mechanism, smart contracts. Hiểu concepts, không cần code.
  - id: KP2
    content: Decision framework: khi nào dùng blockchain
    keypoint_weight: 0.35
    description: Multiple untrusted parties, need for shared truth, audit trail critical, intermediary elimination beneficial.
  - id: KP3
    content: Khi nào KHÔNG nên dùng blockchain
    keypoint_weight: 0.3
    description: Single organization, trusted parties, high transaction speed needed, data privacy paramount, simple database suffices.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Bạn hiểu thế nào về Data Mesh architecture? So sánh với traditional centralized Data Warehouse approach.
* **expected_key_points:**
  - id: KP1
    content: Data Mesh principles
    keypoint_weight: 0.4
    description: Domain-oriented ownership, data as a product, self-serve data platform, federated computational governance.
  - id: KP2
    content: vs Centralized Data Warehouse
    keypoint_weight: 0.35
    description: DW: central team owns all data. Data Mesh: domain teams own their data products. Trade-offs in consistency vs autonomy.
  - id: KP3
    content: BA implications
    keypoint_weight: 0.25
    description: BA works with domain teams to define data products, data contracts, quality SLAs, discovery mechanisms.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Edge Computing vs Cloud Computing: BA cần biết gì khi phân tích requirements cho IoT solutions?
* **expected_key_points:**
  - id: KP1
    content: Edge Computing use cases
    keypoint_weight: 0.35
    description: Low latency requirements, bandwidth constraints, offline operation, data sovereignty. VD: manufacturing, autonomous vehicles.
  - id: KP2
    content: Cloud vs Edge decision criteria
    keypoint_weight: 0.35
    description: Latency requirements, data volume, connectivity reliability, processing complexity, cost model.
  - id: KP3
    content: Hybrid architecture requirements
    keypoint_weight: 0.3
    description: What processes at edge vs cloud, data sync strategy, device management, security at edge.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn phân tích requirements cho AI-powered Customer Service platform (AI + Human agents). Approach và considerations?
* **expected_key_points:**
  - id: KP1
    content: AI-human handoff requirements
    keypoint_weight: 0.3
    description: Handoff triggers, context transfer, sentiment-based escalation, agent assistance mode vs full automation.
  - id: KP2
    content: AI model requirements
    keypoint_weight: 0.25
    description: Intent classification accuracy targets, entity extraction, multi-language support, continuous learning.
  - id: KP3
    content: Agent experience requirements
    keypoint_weight: 0.25
    description: AI-suggested responses, customer context display, knowledge base search, performance analytics.
  - id: KP4
    content: Quality assurance requirements
    keypoint_weight: 0.2
    description: Conversation quality scoring, AI accuracy monitoring, customer satisfaction tracking, compliance auditing.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn cần assess feasibility của GraphQL vs REST API cho new platform development. BA analysis approach?
* **expected_key_points:**
  - id: KP1
    content: Use case analysis
    keypoint_weight: 0.3
    description: REST: simple CRUD, caching important, well-defined resources. GraphQL: complex queries, mobile apps, multiple consumers.
  - id: KP2
    content: Developer experience và ecosystem
    keypoint_weight: 0.25
    description: Team familiarity, tooling availability, documentation standards, learning curve assessment.
  - id: KP3
    content: Performance và scalability trade-offs
    keypoint_weight: 0.25
    description: REST: HTTP caching, simpler scaling. GraphQL: reduce over-fetching, n+1 query problem, complexity.
  - id: KP4
    content: Decision recommendation format
    keypoint_weight: 0.2
    description: Pros/cons matrix, POC results, team input, recommended approach with rationale, migration path if switching.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn document requirements cho event-driven notification system serving 1M+ users. Architecture considerations cho BA?
* **expected_key_points:**
  - id: KP1
    content: Notification channels và preferences
    keypoint_weight: 0.3
    description: Push notification, email, SMS, in-app. User preference management, opt-in/opt-out, frequency controls.
  - id: KP2
    content: Event triggers và content templates
    keypoint_weight: 0.25
    description: Business event catalog, template management with variables, personalization rules, A/B testing.
  - id: KP3
    content: Delivery reliability requirements
    keypoint_weight: 0.25
    description: Delivery SLA per channel, retry logic, fallback channels, delivery tracking, bounce handling.
  - id: KP4
    content: Scalability và performance
    keypoint_weight: 0.2
    description: Peak load handling, queue management, rate limiting per provider, batching strategy.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn evaluate Composable Architecture approach cho digital commerce platform. BA assessment framework?
* **expected_key_points:**
  - id: KP1
    content: Composable commerce concepts
    keypoint_weight: 0.3
    description: MACH architecture (Microservices, API-first, Cloud-native, Headless). Best-of-breed vs suite approach.
  - id: KP2
    content: Vendor selection per capability
    keypoint_weight: 0.25
    description: CMS, commerce engine, search, personalization, payments as separate best-of-breed selections.
  - id: KP3
    content: Integration complexity assessment
    keypoint_weight: 0.25
    description: API contracts, event-driven integration, data consistency challenges, vendor dependency risks.
  - id: KP4
    content: Build vs buy per component
    keypoint_weight: 0.2
    description: Decision matrix: strategic differentiation, market availability, customization needs, total cost.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.1 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế requirements cho Generative AI integration vào enterprise knowledge management. Governance, use cases, và risk mitigation?
* **expected_key_points:**
  - id: KP1
    content: Use case identification và prioritization
    keypoint_weight: 0.25
    description: Document search/summarization, Q&A over internal docs, content generation, code assistance. ROI per use case.
  - id: KP2
    content: Data governance cho AI
    keypoint_weight: 0.3
    description: Training data sourcing, PII handling, data quality for RAG, hallucination mitigation, source attribution.
  - id: KP3
    content: Responsible AI requirements
    keypoint_weight: 0.25
    description: Content moderation, bias detection, human review workflows, transparency, usage policies.
  - id: KP4
    content: Integration architecture
    keypoint_weight: 0.2
    description: API integration with LLM providers, vector database for embeddings, caching strategy, cost management.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Bạn phân tích requirements cho Multi-cloud Strategy implementation. BA considerations cho workload placement decisions?
* **expected_key_points:**
  - id: KP1
    content: Workload assessment framework
    keypoint_weight: 0.3
    description: Performance requirements, data residency, cost optimization, vendor capabilities, compliance requirements per workload.
  - id: KP2
    content: Portability và interoperability requirements
    keypoint_weight: 0.25
    description: Container orchestration, IaC standards, API abstraction layers, data portability, avoiding vendor lock-in.
  - id: KP3
    content: Operational requirements
    keypoint_weight: 0.25
    description: Unified monitoring, centralized logging, cost management across clouds, security policy consistency.
  - id: KP4
    content: Disaster recovery và business continuity
    keypoint_weight: 0.2
    description: Cross-cloud DR, RTO/RPO requirements, failover automation, regular DR testing requirements.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích và propose requirements cho Digital Identity platform (SSI - Self-Sovereign Identity) cho financial services. BA end-to-end approach?
* **expected_key_points:**
  - id: KP1
    content: SSI concepts và architecture
    keypoint_weight: 0.3
    description: Decentralized identifiers (DIDs), verifiable credentials, identity wallets, trust registries.
  - id: KP2
    content: KYC/AML use case requirements
    keypoint_weight: 0.25
    description: Identity verification workflow, credential issuance, credential verification, regulatory compliance mapping.
  - id: KP3
    content: Interoperability standards
    keypoint_weight: 0.25
    description: W3C standards compliance, cross-platform wallet compatibility, trust framework governance.
  - id: KP4
    content: User experience requirements
    keypoint_weight: 0.2
    description: Onboarding flow, credential management, consent management, recovery mechanisms, accessibility.

