# Architecture Diagram Index

This index covers 95 evidence-backed diagrams. Statuses describe the checked-out source tree, not aspirational deployment state. `IMPLEMENTED OFFLINE` identifies evaluation-only behavior.

| # | Diagram | Category | Status | Standalone Mermaid |
|---:|---|---|---|---|
| 1 | [System Context](DIAGRAMS.md#1-system-context) | Architecture | IMPLEMENTED/PARTIAL | [source](diagrams/01-system-context.mmd) |
| 2 | [Container Architecture](DIAGRAMS.md#2-container-architecture) | Architecture | IMPLEMENTED/PARTIAL | [source](diagrams/02-container-architecture.mmd) |
| 3 | [Backend Components](DIAGRAMS.md#3-backend-components) | Architecture | IMPLEMENTED | [source](diagrams/03-backend-components.mmd) |
| 4 | [Frontend Architecture](DIAGRAMS.md#4-frontend-architecture) | Frontend | IMPLEMENTED/PARTIAL | [source](diagrams/04-frontend-architecture.mmd) |
| 5 | [Complete End-to-End Pipeline](DIAGRAMS.md#5-complete-end-to-end-pipeline) | Runtime | IMPLEMENTED/PARTIAL | [source](diagrams/05-end-to-end-pipeline.mmd) |
| 6 | [Resume Ingestion Pipeline](DIAGRAMS.md#6-resume-ingestion-pipeline) | Resume | IMPLEMENTED | [source](diagrams/06-resume-ingestion.mmd) |
| 7 | [OCR and Document Extraction Decision Tree](DIAGRAMS.md#7-ocr-and-document-extraction-decision-tree) | Resume | IMPLEMENTED | [source](diagrams/07-ocr-decision-tree.mmd) |
| 8 | [Candidate Profile Generation](DIAGRAMS.md#8-candidate-profile-generation) | Candidate | IMPLEMENTED/PARTIAL | [source](diagrams/08-candidate-profile-generation.mmd) |
| 9 | [Candidate Profile Data Model](DIAGRAMS.md#9-candidate-profile-data-model) | Data | IMPLEMENTED/PARTIAL | [source](diagrams/09-candidate-profile-data-model.mmd) |
| 10 | [Profile Readiness Pipeline](DIAGRAMS.md#10-profile-readiness-pipeline) | Candidate | IMPLEMENTED/PARTIAL | [source](diagrams/10-profile-readiness.mmd) |
| 11 | [Interview Plan Generation](DIAGRAMS.md#11-interview-plan-generation) | Interview | IMPLEMENTED | [source](diagrams/11-interview-plan-generation.mmd) |
| 12 | [Interview Plan Data Model](DIAGRAMS.md#12-interview-plan-data-model) | Data | IMPLEMENTED | [source](diagrams/12-interview-plan-data-model.mmd) |
| 13 | [Question Generation Pipeline](DIAGRAMS.md#13-question-generation-pipeline) | Question Generation | IMPLEMENTED | [source](diagrams/13-question-generation-pipeline.mmd) |
| 14 | [Question Generation Sequence](DIAGRAMS.md#14-question-generation-sequence) | Question Generation | IMPLEMENTED | [source](diagrams/14-question-generation-sequence.mmd) |
| 15 | [RAG Overview](DIAGRAMS.md#15-rag-overview) | RAG | IMPLEMENTED/PARTIAL | [source](diagrams/15-rag-overview.mmd) |
| 16 | [Knowledge Ingestion Pipeline](DIAGRAMS.md#16-knowledge-ingestion-pipeline) | RAG | IMPLEMENTED | [source](diagrams/16-knowledge-ingestion.mmd) |
| 17 | [Lexical Retrieval Pipeline](DIAGRAMS.md#17-lexical-retrieval-pipeline) | RAG | IMPLEMENTED | [source](diagrams/17-lexical-retrieval.mmd) |
| 18 | [Vector Retrieval Pipeline](DIAGRAMS.md#18-vector-retrieval-pipeline) | RAG | IMPLEMENTED | [source](diagrams/18-vector-retrieval.mmd) |
| 19 | [Retrieval Mode Comparison](DIAGRAMS.md#19-retrieval-mode-comparison) | RAG | IMPLEMENTED OFFLINE | [source](diagrams/19-retrieval-mode-comparison.mmd) |
| 20 | [RAG Query Construction](DIAGRAMS.md#20-rag-query-construction) | RAG | IMPLEMENTED | [source](diagrams/20-rag-query-construction.mmd) |
| 21 | [Context Assembly and Prompt Augmentation](DIAGRAMS.md#21-context-assembly-and-prompt-augmentation) | LLM | IMPLEMENTED | [source](diagrams/21-context-assembly.mmd) |
| 22 | [Prompt Architecture](DIAGRAMS.md#22-prompt-architecture) | LLM | IMPLEMENTED | [source](diagrams/22-prompt-architecture.mmd) |
| 23 | [Model and Provider Routing](DIAGRAMS.md#23-model-and-provider-routing) | LLM | IMPLEMENTED | [source](diagrams/23-model-provider-routing.mmd) |
| 24 | [Answer Submission Flow](DIAGRAMS.md#24-answer-submission-flow) | Interview | IMPLEMENTED | [source](diagrams/24-answer-submission-flow.mmd) |
| 25 | [Answer Evaluation Pipeline](DIAGRAMS.md#25-answer-evaluation-pipeline) | Evaluation | IMPLEMENTED | [source](diagrams/25-answer-evaluation-pipeline.mmd) |
| 26 | [Production Evaluation Rubric](DIAGRAMS.md#26-production-evaluation-rubric) | Evaluation | IMPLEMENTED | [source](diagrams/26-evaluation-rubric.mmd) |
| 27 | [Evaluation Framework Architecture](DIAGRAMS.md#27-evaluation-framework-architecture) | Evaluation | IMPLEMENTED OFFLINE | [source](diagrams/27-evaluation-framework.mmd) |
| 28 | [A B C RAG Ablation](DIAGRAMS.md#28-a-b-c-rag-ablation) | Evaluation | IMPLEMENTED OFFLINE | [source](diagrams/28-rag-abc-ablation.mmd) |
| 29 | [Grounding Evaluation Flow](DIAGRAMS.md#29-grounding-evaluation-flow) | Evaluation | IMPLEMENTED OFFLINE | [source](diagrams/29-grounding-evaluation.mmd) |
| 30 | [Knowledge Utilization Evaluation](DIAGRAMS.md#30-knowledge-utilization-evaluation) | Evaluation | IMPLEMENTED OFFLINE | [source](diagrams/30-knowledge-utilization.mmd) |
| 31 | [Interview Session State Machine](DIAGRAMS.md#31-interview-session-state-machine) | Interview | IMPLEMENTED/PARTIAL | [source](diagrams/31-interview-session-state-machine.mmd) |
| 32 | [Question Lifecycle State Machine](DIAGRAMS.md#32-question-lifecycle-state-machine) | Question Generation | IMPLEMENTED | [source](diagrams/32-question-lifecycle-state-machine.mmd) |
| 33 | [Complete Interview Sequence](DIAGRAMS.md#33-complete-interview-sequence) | Runtime | IMPLEMENTED/PARTIAL | [source](diagrams/33-interview-sequence.mmd) |
| 34 | [Database ER Model](DIAGRAMS.md#34-database-er-model) | Data | IMPLEMENTED | [source](diagrams/34-database-er.mmd) |
| 35 | [Data Ownership](DIAGRAMS.md#35-data-ownership) | Security | IMPLEMENTED/PARTIAL | [source](diagrams/35-data-ownership.mmd) |
| 36 | [Data Flow Diagram Level 0](DIAGRAMS.md#36-data-flow-diagram-level-0) | Data | IMPLEMENTED/PARTIAL | [source](diagrams/36-data-flow-level-0.mmd) |
| 37 | [Data Flow Diagram Level 1](DIAGRAMS.md#37-data-flow-diagram-level-1) | Data | IMPLEMENTED/PARTIAL | [source](diagrams/37-data-flow-level-1.mmd) |
| 38 | [Data Flow Diagram Level 2](DIAGRAMS.md#38-data-flow-diagram-level-2) | Data | IMPLEMENTED/PARTIAL | [source](diagrams/38-data-flow-level-2.mmd) |
| 39 | [API Architecture](DIAGRAMS.md#39-api-architecture) | API | IMPLEMENTED/PARTIAL | [source](diagrams/39-api-architecture.mmd) |
| 40 | [API Request Flow](DIAGRAMS.md#40-api-request-flow) | API | IMPLEMENTED | [source](diagrams/40-api-request-flow.mmd) |
| 41 | [Major Package Dependency Graph](DIAGRAMS.md#41-major-package-dependency-graph) | Architecture | IMPLEMENTED | [source](diagrams/41-dependency-graph.mmd) |
| 42 | [Layered Architecture](DIAGRAMS.md#42-layered-architecture) | Architecture | IMPLEMENTED/PARTIAL | [source](diagrams/42-layered-architecture.mmd) |
| 43 | [Configuration Flow](DIAGRAMS.md#43-configuration-flow) | Deployment | IMPLEMENTED | [source](diagrams/43-configuration-flow.mmd) |
| 44 | [Feature Flags and Experiment Configuration](DIAGRAMS.md#44-feature-flags-and-experiment-configuration) | Deployment | IMPLEMENTED/PARTIAL | [source](diagrams/44-feature-flags.mmd) |
| 45 | [Error Handling Flow](DIAGRAMS.md#45-error-handling-flow) | Reliability | IMPLEMENTED/PARTIAL | [source](diagrams/45-error-handling.mmd) |
| 46 | [LLM Failure and Retry](DIAGRAMS.md#46-llm-failure-and-retry) | Reliability | IMPLEMENTED/PARTIAL | [source](diagrams/46-llm-failure-retry.mmd) |
| 47 | [Structured Output Validation](DIAGRAMS.md#47-structured-output-validation) | LLM | IMPLEMENTED | [source](diagrams/47-structured-output-validation.mmd) |
| 48 | [Observability Architecture](DIAGRAMS.md#48-observability-architecture) | Performance | IMPLEMENTED/PARTIAL | [source](diagrams/48-observability-architecture.mmd) |
| 49 | [Runtime Latency Breakdown](DIAGRAMS.md#49-runtime-latency-breakdown) | Performance | IMPLEMENTED/PARTIAL | [source](diagrams/49-latency-breakdown.mmd) |
| 50 | [Performance Evaluation Pipeline](DIAGRAMS.md#50-performance-evaluation-pipeline) | Performance | IMPLEMENTED OFFLINE | [source](diagrams/50-performance-evaluation.mmd) |
| 51 | [Cache Architecture](DIAGRAMS.md#51-cache-architecture) | Reliability | IMPLEMENTED/PARTIAL | [source](diagrams/51-cache-architecture.mmd) |
| 52 | [Security and Trust Boundaries](DIAGRAMS.md#52-security-and-trust-boundaries) | Security | IMPLEMENTED/PARTIAL | [source](diagrams/52-security-trust-boundaries.mmd) |
| 53 | [Resume Data Privacy Flow](DIAGRAMS.md#53-resume-data-privacy-flow) | Security | IMPLEMENTED/PARTIAL | [source](diagrams/53-resume-data-privacy.mmd) |
| 54 | [Deployment Architecture](DIAGRAMS.md#54-deployment-architecture) | Deployment | IMPLEMENTED CONFIG/UNKNOWN LIVE | [source](diagrams/54-deployment-architecture.mmd) |
| 55 | [Local Development Architecture](DIAGRAMS.md#55-local-development-architecture) | Deployment | IMPLEMENTED | [source](diagrams/55-local-development.mmd) |
| 56 | [CI and CD Availability](DIAGRAMS.md#56-ci-and-cd-availability) | Testing | SPEC-PENDING/PARTIAL | [source](diagrams/56-ci-cd-pipeline.mmd) |
| 57 | [Test Architecture](DIAGRAMS.md#57-test-architecture) | Testing | IMPLEMENTED/PARTIAL | [source](diagrams/57-test-architecture.mmd) |
| 58 | [Test Coverage Map](DIAGRAMS.md#58-test-coverage-map) | Testing | IMPLEMENTED/PARTIAL | [source](diagrams/58-test-coverage-map.mmd) |
| 59 | [Current UX Flow](DIAGRAMS.md#59-current-ux-flow) | Frontend | IMPLEMENTED/PARTIAL | [source](diagrams/59-ux-flow.mmd) |
| 60 | [Candidate User Journey](DIAGRAMS.md#60-candidate-user-journey) | Frontend | IMPLEMENTED/PARTIAL | [source](diagrams/60-user-journey.mmd) |
| 61 | [Double-click and Idempotency Flow](DIAGRAMS.md#61-double-click-and-idempotency-flow) | Reliability | IMPLEMENTED/PARTIAL | [source](diagrams/61-double-click-idempotency.mmd) |
| 62 | [Concurrent Request Flow](DIAGRAMS.md#62-concurrent-request-flow) | Reliability | IMPLEMENTED/PARTIAL | [source](diagrams/62-concurrent-requests.mmd) |
| 63 | [Interview Completion Flow](DIAGRAMS.md#63-interview-completion-flow) | Interview | IMPLEMENTED/PARTIAL | [source](diagrams/63-interview-completion.mmd) |
| 64 | [Report Generation Pipeline](DIAGRAMS.md#64-report-generation-pipeline) | Interview | IMPLEMENTED/PARTIAL | [source](diagrams/64-report-generation.mmd) |
| 65 | [Interview Report Data Model](DIAGRAMS.md#65-interview-report-data-model) | Data | IMPLEMENTED | [source](diagrams/65-report-data-model.mmd) |
| 66 | [Core Domain Model](DIAGRAMS.md#66-core-domain-model) | Data | IMPLEMENTED/PARTIAL | [source](diagrams/66-domain-model.mmd) |
| 67 | [Core Implementation Classes](DIAGRAMS.md#67-core-implementation-classes) | Architecture | IMPLEMENTED | [source](diagrams/67-core-class-diagram.mmd) |
| 68 | [Service Call Graph](DIAGRAMS.md#68-service-call-graph) | Architecture | IMPLEMENTED/PARTIAL | [source](diagrams/68-service-call-graph.mmd) |
| 69 | [LLM Call Graph](DIAGRAMS.md#69-llm-call-graph) | LLM | IMPLEMENTED | [source](diagrams/69-llm-call-graph.mmd) |
| 70 | [Embedding Call Graph](DIAGRAMS.md#70-embedding-call-graph) | RAG | IMPLEMENTED/PARTIAL | [source](diagrams/70-embedding-call-graph.mmd) |
| 71 | [Storage Architecture](DIAGRAMS.md#71-storage-architecture) | Data | IMPLEMENTED/PARTIAL | [source](diagrams/71-storage-architecture.mmd) |
| 72 | [Resume File Lifecycle](DIAGRAMS.md#72-resume-file-lifecycle) | Resume | IMPLEMENTED | [source](diagrams/72-resume-file-lifecycle.mmd) |
| 73 | [Knowledge Chunk Data Model](DIAGRAMS.md#73-knowledge-chunk-data-model) | Data | IMPLEMENTED | [source](diagrams/73-knowledge-chunk-data-model.mmd) |
| 74 | [Retrieval Sequence](DIAGRAMS.md#74-retrieval-sequence) | RAG | IMPLEMENTED/PARTIAL | [source](diagrams/74-retrieval-sequence.mmd) |
| 75 | [RAG Failure Flow](DIAGRAMS.md#75-rag-failure-flow) | Reliability | IMPLEMENTED/PARTIAL | [source](diagrams/75-rag-failure-flow.mmd) |
| 76 | [End-to-End Data Transformation](DIAGRAMS.md#76-end-to-end-data-transformation) | Data | IMPLEMENTED/PARTIAL | [source](diagrams/76-data-transformation.mmd) |
| 77 | [Schema Transformation Map](DIAGRAMS.md#77-schema-transformation-map) | Data | IMPLEMENTED/PARTIAL | [source](diagrams/77-schema-transformations.mmd) |
| 78 | [Interview Plan to Question Traceability](DIAGRAMS.md#78-interview-plan-to-question-traceability) | Question Generation | IMPLEMENTED/PARTIAL | [source](diagrams/78-plan-question-traceability.mmd) |
| 79 | [Question to Evaluation Traceability](DIAGRAMS.md#79-question-to-evaluation-traceability) | Evaluation | IMPLEMENTED | [source](diagrams/79-question-evaluation-traceability.mmd) |
| 80 | [End-to-End Traceability](DIAGRAMS.md#80-end-to-end-traceability) | Data | IMPLEMENTED/PARTIAL | [source](diagrams/80-end-to-end-traceability.mmd) |
| 81 | [Implementation Status Map](DIAGRAMS.md#81-implementation-status-map) | Architecture | IMPLEMENTED/PARTIAL/SPEC-PENDING/UNKNOWN | [source](diagrams/81-implementation-status-map.mmd) |
| 82 | [Architecture Gap Map](DIAGRAMS.md#82-architecture-gap-map) | Architecture | PARTIAL/SPEC-PENDING | [source](diagrams/82-architecture-gaps.mmd) |
| 83 | [Current versus Target Pipeline](DIAGRAMS.md#83-current-versus-target-pipeline) | Architecture | IMPLEMENTED/SPEC-PENDING | [source](diagrams/83-current-vs-target.mmd) |
| 84 | [Successful Interview Critical Path](DIAGRAMS.md#84-successful-interview-critical-path) | Runtime | IMPLEMENTED/PARTIAL | [source](diagrams/84-critical-path.mmd) |
| 85 | [Failure Domain Map](DIAGRAMS.md#85-failure-domain-map) | Reliability | IMPLEMENTED/PARTIAL | [source](diagrams/85-failure-domains.mmd) |
| 86 | [Single Question Latency Trace](DIAGRAMS.md#86-single-question-latency-trace) | Performance | IMPLEMENTED/PARTIAL | [source](diagrams/86-single-question-latency.mmd) |
| 87 | [Evaluation Execution Sequence](DIAGRAMS.md#87-evaluation-execution-sequence) | Evaluation | IMPLEMENTED OFFLINE | [source](diagrams/87-evaluation-execution.mmd) |
| 88 | [Evaluation Data Model](DIAGRAMS.md#88-evaluation-data-model) | Data | IMPLEMENTED OFFLINE | [source](diagrams/88-evaluation-data-model.mmd) |
| 89 | [RAG Ablation Isolation Controls](DIAGRAMS.md#89-rag-ablation-isolation-controls) | Evaluation | IMPLEMENTED OFFLINE | [source](diagrams/89-rag-ablation-isolation.mmd) |
| 90 | [Metric Dependency Graph](DIAGRAMS.md#90-metric-dependency-graph) | Evaluation | IMPLEMENTED OFFLINE | [source](diagrams/90-metric-dependency-graph.mmd) |
| 91 | [Authentication and Ownership Flow](DIAGRAMS.md#91-authentication-and-ownership-flow) | Security | IMPLEMENTED | [source](diagrams/91-authentication-flow.mmd) |
| 92 | [Voice Interview Sequence](DIAGRAMS.md#92-voice-interview-sequence) | Runtime | IMPLEMENTED/PARTIAL | [source](diagrams/92-voice-interview-sequence.mmd) |
| 93 | [Speech Processing Pipeline](DIAGRAMS.md#93-speech-processing-pipeline) | Runtime | IMPLEMENTED | [source](diagrams/93-speech-processing-pipeline.mmd) |
| 94 | [Voice Session State Machine](DIAGRAMS.md#94-voice-session-state-machine) | Runtime | IMPLEMENTED | [source](diagrams/94-voice-state-machine.mmd) |
| 95 | [Voice WebSocket Event Contract](DIAGRAMS.md#95-voice-websocket-event-contract) | API | IMPLEMENTED | [source](diagrams/95-voice-event-contract.mmd) |
