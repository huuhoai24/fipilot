# M3 Duplicate Analysis

Near matches are retained. Group IDs are correlation metadata, not deletion instructions.

Exact groups: **673**; near groups: **6**.

## Strategy

- Exact: SHA-256 over normalized chunk content.
- Near: local candidate generation over token postings; max unigram/trigram Jaccard at threshold `0.85`.
- Candidate pairs evaluated: `30244`.

## Exact group sample

- `exact_fbd6cc1b156faa1f`: 2 chunks; domains=['AI_Engineer', 'Data_Scientist']; paths=['Knowledge/Domains/AI_Enginner/5. Machine Learning/5.5 Machine Learning Evaluation Metrics/Regression Metrics.md', 'Knowledge/Domains/Data Scientist/6. Machine Learning/Model Evaluation/Regression Metrics.md']
- `exact_4043533f810efa09`: 3 chunks; domains=['Backend_Developer', 'Full_Stack_Developer', 'Software_Engineer']; paths=['Knowledge/Domains/Backend Developer/4. Networking/4.1 Networking Fundamentals/TCP_IP Model.md', 'Knowledge/Domains/Full stack Developer/6. Networking/6.2 Networking Fundamentals/TCP_IP Model.md', 'Knowledge/Domains/Software Engineer/6. Networking/6.1 Networking Fundamentals/TCP_IP Model.md']
- `exact_357192a79dd27b5e`: 3 chunks; domains=['Backend_Developer', 'Full_Stack_Developer', 'Software_Engineer']; paths=['Knowledge/Domains/Backend Developer/1. Computer Science Fundamentals/1.2 Object-Oriented Programming (OOP)/Aggregation.md', 'Knowledge/Domains/Full stack Developer/1. Computer Science Fundamentals/1.2 Object-Oriented Programming/Aggregation.md', 'Knowledge/Domains/Software Engineer/1. Computer Science Fundamentals/1.2 Object-Oriented Programming/Aggregation.md']
- `exact_4e08207e6649d727`: 2 chunks; domains=['Data_Engineer', 'Data_Scientist']; paths=['Knowledge/Domains/Data Engineer/2. SQL/2.1 SQL Fundamentals/DISTINCT.md', 'Knowledge/Domains/Data Scientist/3. SQL/SQL Fundamentals/DISTINCT.md']
- `exact_195c1cc75d4a86f5`: 2 chunks; domains=['Backend_Developer', 'DevOps_Engineer']; paths=['Knowledge/Domains/Backend Developer/23. Version Control/23.2 Collaboration/Daily Stand-up.md', 'Knowledge/Domains/DevOps Engineer/18. Software Engineering Practices/Agile/Daily Stand-up.md']
- `exact_f90e021f7360bea2`: 2 chunks; domains=['AI_Engineer', 'Data_Scientist']; paths=['Knowledge/Domains/AI_Enginner/13. Linux/13.2 Common Linux Commands/`top`.md', 'Knowledge/Domains/Data Scientist/13. Linux/Common Commands/`top`.md']
- `exact_4b0f402c0d29e8a8`: 2 chunks; domains=['AI_Engineer', 'Data_Scientist']; paths=['Knowledge/Domains/AI_Enginner/13. Linux/13.2 Common Linux Commands/`ps`.md', 'Knowledge/Domains/Data Scientist/13. Linux/Common Commands/`ps`.md']
- `exact_5e37ed85ac3ec4c5`: 2 chunks; domains=['Backend_Developer', 'Software_Engineer']; paths=['Knowledge/Domains/Backend Developer/10. Concurrency & Parallelism/10.2 Synchronization/Lock.md', 'Knowledge/Domains/Software Engineer/8. Concurrency/8.2 Synchronization/Lock.md']
- `exact_938f53ccadbb21ef`: 2 chunks; domains=['Backend_Developer', 'Software_Engineer']; paths=['Knowledge/Domains/Backend Developer/15. Security/15.2 Cryptography/TLS.md', 'Knowledge/Domains/Software Engineer/9. Security/9.2 Cryptography/TLS.md']
- `exact_596ecaf68747d510`: 2 chunks; domains=['Backend_Developer', 'DevOps_Engineer']; paths=['Knowledge/Domains/Backend Developer/19. Docker/19.1 Docker Fundamentals/Images.md', 'Knowledge/Domains/DevOps Engineer/6. Containerization/Docker Fundamentals/Images.md']
- `exact_f8c78cde0fc3c2a8`: 3 chunks; domains=['Backend_Developer', 'Full_Stack_Developer', 'Software_Engineer']; paths=['Knowledge/Domains/Backend Developer/1. Computer Science Fundamentals/1.3 Functional Programming/First-class Functions.md', 'Knowledge/Domains/Full stack Developer/1. Computer Science Fundamentals/1.3 Functional Programming/First-class Functions.md', 'Knowledge/Domains/Software Engineer/1. Computer Science Fundamentals/1.3 Functional Programming/First-class Functions.md']
- `exact_b9dbc177e7b39323`: 2 chunks; domains=['Data_Engineer', 'Data_Scientist']; paths=['Knowledge/Domains/Data Engineer/1. Python Programming/1.3 Functions/`_args`.md', 'Knowledge/Domains/Data Scientist/1. Python Programming/1.3 Functions/`_args`.md']
- `exact_36e15270e9e68723`: 3 chunks; domains=['Backend_Developer', 'Full_Stack_Developer', 'Software_Engineer']; paths=['Knowledge/Domains/Backend Developer/4. Networking/4.1 Networking Fundamentals/IP Address.md', 'Knowledge/Domains/Full stack Developer/6. Networking/6.2 Networking Fundamentals/IP Address.md', 'Knowledge/Domains/Software Engineer/6. Networking/6.1 Networking Fundamentals/IP Address.md']
- `exact_c47f7d7f2f4493e8`: 2 chunks; domains=['Backend_Developer', 'Software_Engineer']; paths=['Knowledge/Domains/Backend Developer/16. Testing/16.1 Testing Fundamentals/Test Pyramid.md', 'Knowledge/Domains/Software Engineer/10. Testing/10.1 Testing Fundamentals/Test Pyramid.md']
- `exact_58c6c224c77ab1d3`: 2 chunks; domains=['AI_Engineer', 'Data_Scientist']; paths=['Knowledge/Domains/AI_Enginner/6. Deep Learning/6.5 Transformer/Practical Concerns.md', 'Knowledge/Domains/Data Scientist/7. Deep Learning/Transformer/Practical Concerns.md']
- `exact_ef10a684eaee125d`: 3 chunks; domains=['Backend_Developer', 'Full_Stack_Developer', 'Software_Engineer']; paths=['Knowledge/Domains/Backend Developer/1. Computer Science Fundamentals/1.5 Algorithms/Searching.md', 'Knowledge/Domains/Full stack Developer/1. Computer Science Fundamentals/1.5 Algorithms/Searching.md', 'Knowledge/Domains/Software Engineer/1. Computer Science Fundamentals/1.5 Algorithms/Searching.md']
- `exact_2beb3ee9478ff8ee`: 2 chunks; domains=['Data_Engineer', 'Data_Scientist']; paths=['Knowledge/Domains/Data Engineer/2. SQL/2.4 Advanced SQL/UNION.md', 'Knowledge/Domains/Data Scientist/3. SQL/Advanced SQL/UNION.md']
- `exact_b8551e386763edce`: 2 chunks; domains=['AI_Engineer', 'Data_Scientist']; paths=['Knowledge/Domains/AI_Enginner/3. Data Processing/3.4 Feature Engineering/Label Encoding.md', 'Knowledge/Domains/Data Scientist/4. Data Analysis/Feature Engineering/Label Encoding.md']
- `exact_8afcbf418bd6d3a7`: 2 chunks; domains=['AI_Engineer', 'Data_Scientist']; paths=['Knowledge/Domains/AI_Enginner/12. Software Engineering/12.2 Clean Code/Function and Module Quality.md', 'Knowledge/Domains/Data Scientist/12. Software Engineering/Clean Code/Function and Module Quality.md']
- `exact_fa1e2398dccb5503`: 2 chunks; domains=['Data_Engineer', 'Data_Scientist']; paths=['Knowledge/Domains/Data Engineer/2. SQL/2.5 Window Functions/ROW_NUMBER.md', 'Knowledge/Domains/Data Scientist/3. SQL/Window Functions/ROW_NUMBER.md']
- `exact_dfe13301e912bf89`: 2 chunks; domains=['AI_Engineer', 'Data_Scientist']; paths=['Knowledge/Domains/AI_Enginner/6. Deep Learning/6.5 Transformer/Decoder.md', 'Knowledge/Domains/Data Scientist/7. Deep Learning/Transformer/Decoder.md']
- `exact_76503845da8ad7e2`: 2 chunks; domains=['AI_Engineer', 'Data_Scientist']; paths=['Knowledge/Domains/AI_Enginner/5. Machine Learning/5.6 Common Enterprise Machine Learning Problems/Class Imbalance.md', 'Knowledge/Domains/Data Scientist/6. Machine Learning/Common Problems/Class Imbalance.md']
- `exact_a08625377356bacd`: 2 chunks; domains=['AI_Engineer', 'Data_Scientist']; paths=['Knowledge/Domains/AI_Enginner/10. MLOps/10.2 Experiment Tracking/MLflow.md', 'Knowledge/Domains/Data Scientist/11. MLOps (Fundamental)/Experiment Tracking/MLflow.md']
- `exact_9ae6a0648c1e41cd`: 2 chunks; domains=['Data_Engineer', 'Data_Scientist']; paths=['Knowledge/Domains/Data Engineer/2. SQL/2.4 Advanced SQL/Window Function.md', 'Knowledge/Domains/Data Scientist/3. SQL/Advanced SQL/Window Function.md']
- `exact_ac08cf12581dc6f3`: 2 chunks; domains=['AI_Engineer', 'Data_Scientist']; paths=['Knowledge/Domains/AI_Enginner/2. Mathematics for AI/2.4 Statistics/Median.md', 'Knowledge/Domains/Data Scientist/2. Mathematics/2.4 Statistics/Median.md']

## Near group sample

- `near_33a59d4dfcca68a8`: 2 chunks; domains=['Full_Stack_Developer', 'Software_Engineer']; paths=['Knowledge/Domains/Full stack Developer/Frequently Evaluated Cross-cutting Topics/Frequently Evaluated Cross-cutting Topics/Computer Science Fundamentals.md', 'Knowledge/Domains/Software Engineer/Frequently Evaluated Senior Software Engineer Topics/Frequently Evaluated Cross-cutting Topics/Computer Science Fundamentals.md']
- `near_b9a71ed120bdbbeb`: 3 chunks; domains=['Backend_Developer', 'Software_Engineer']; paths=['Knowledge/Domains/Backend Developer/10. Concurrency & Parallelism/10.3 Common Problems/Deadlock.md', 'Knowledge/Domains/Backend Developer/3. Operating Systems/3.1 Operating System Fundamentals/Deadlock.md', 'Knowledge/Domains/Software Engineer/8. Concurrency/8.3 Concurrency Problems/Deadlock.md']
- `near_7d4f95a57f72ccc1`: 4 chunks; domains=['Data_Engineer', 'DevOps_Engineer', 'Full_Stack_Developer', 'Software_Engineer']; paths=['Knowledge/Levels/Data_Engineer/Senior.md', 'Knowledge/Levels/DevOps_Engineer/Senior.md', 'Knowledge/Levels/Full_Stack_Developer/Senior.md', 'Knowledge/Levels/Software_Engineer/Senior.md']
- `near_c03251d99aa15fa2`: 2 chunks; domains=['Full_Stack_Developer', 'Software_Engineer']; paths=['Knowledge/Domains/Full stack Developer/8. Performance Optimization/8.3 System Performance/Load Balancing.md', 'Knowledge/Domains/Software Engineer/4. System Design/4.1 Scalability/Load Balancing.md']
- `near_0ba06f5effe7315d`: 2 chunks; domains=['AI_Engineer', 'Data_Scientist']; paths=['Knowledge/Levels/AI_Engineer/Middle.md', 'Knowledge/Levels/Data_Scientist/Middle.md']
- `near_ea45d64d231e6236`: 2 chunks; domains=['Software_Engineer']; paths=['Knowledge/Domains/Software Engineer/14. Software Engineering Practices/14.4 Collaboration/Collaborative Development.md', 'Knowledge/Domains/Software Engineer/8. Concurrency/8.1 Concurrency Fundamentals/Asynchronous Execution.md']

Complete group membership is stored in `evaluation/m3/generated/duplicate_analysis.json`.
