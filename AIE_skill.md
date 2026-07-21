# AI Engineer Knowledge Map
## Core Knowledge & Skills Frequently Evaluated in Technical Interviews
---

# 1. Python Programming

## 1.1 Python Fundamentals

- Variables
- Data Types
- Mutable vs Immutable
- Operators
- Type Conversion
- Input / Output
- Scope
- Modules
- Packages
- Virtual Environment
- PEP8

---

## 1.2 Data Structures

### List

- Indexing
- Slicing
- List Comprehension
- Nested List
- Copy vs Deep Copy
- Time Complexity

### Tuple

- Immutability
- Packing / Unpacking

### Dictionary

- Hash Table
- Collision
- Iteration
- Dictionary Comprehension
- Nested Dictionary

### Set

- Union
- Intersection
- Difference
- Membership Test

### Queue

- deque
- Queue module
- FIFO

### Stack

- list
- deque
- LIFO

---

## 1.3 Functions

- Arguments
- Keyword Arguments
- Default Arguments
- Variable-length Arguments (*args, **kwargs)
- Lambda
- Recursion
- First-class Function
- Higher-order Function
- Decorator
- Generator
- Iterator
- Yield

---

## 1.4 Object-Oriented Programming (OOP)

- Class
- Object
- Constructor
- Instance Variable
- Class Variable
- Encapsulation
- Inheritance
- Polymorphism
- Abstraction
- Method Overriding
- Method Overloading (Python Style)
- Static Method
- Class Method
- Property
- Magic Methods

---

## 1.5 Exception Handling

- try
- except
- finally
- else
- raise
- Custom Exception
- Logging

---

## 1.6 File Handling

- Text File
- CSV
- JSON
- Pickle
- YAML
- Context Manager (with)

---

## 1.7 Advanced Python

- Memory Management
- Garbage Collection
- GIL (Global Interpreter Lock)
- Multiprocessing
- Multithreading
- Asyncio
- Context Manager
- Dataclass
- Typing
- Profiling
- Performance Optimization

---

## 1.8 Common Enterprise Topics

- Package Management
- Dependency Management
- Requirements
- Virtual Environment
- Project Structure
- Logging
- Configuration Management
- Environment Variables

---

# 2. Mathematics for AI

---

## 2.1 Linear Algebra

- Vector
- Matrix
- Tensor
- Matrix Multiplication
- Dot Product
- Cross Product
- Transpose
- Inverse Matrix
- Rank
- Eigenvalue
- Eigenvector
- Orthogonality
- SVD

---

## 2.2 Calculus

- Derivative
- Partial Derivative
- Chain Rule
- Gradient
- Jacobian
- Hessian
- Optimization
- Critical Point

---

## 2.3 Probability

- Random Variable
- Probability Distribution
- Conditional Probability
- Bayes Theorem
- Likelihood
- Prior
- Posterior
- Independence

---

## 2.4 Statistics

- Mean
- Median
- Mode
- Variance
- Standard Deviation
- Covariance
- Correlation
- Confidence Interval
- Hypothesis Testing
- p-value
- Sampling

---

## 2.5 Optimization

- Gradient Descent
- SGD
- Mini-batch GD
- Adam
- RMSProp
- Learning Rate
- Local Minimum
- Global Minimum

---

# 3. Data Processing

---

## 3.1 NumPy

- ndarray
- Broadcasting
- Vectorization
- Indexing
- Reshape
- Axis
- Memory Layout

---

## 3.2 Pandas

- DataFrame
- Series
- Merge
- Join
- GroupBy
- Apply
- Missing Values
- Duplicate Handling
- Datetime
- Window Function

---

## 3.3 Data Cleaning

- Missing Data
- Outlier
- Duplicate
- Invalid Value
- Encoding
- Scaling
- Normalization
- Standardization

---

## 3.4 Feature Engineering

- Feature Selection
- Feature Extraction
- One-hot Encoding
- Label Encoding
- Polynomial Feature
- Interaction Feature

---

# 4. SQL

---

## SQL Fundamentals

- SELECT
- WHERE
- GROUP BY
- ORDER BY
- HAVING
- JOIN
- UNION
- CASE WHEN
- Subquery
- CTE
- Window Function

---

## Database Concepts

- Primary Key
- Foreign Key
- Index
- Transaction
- ACID
- Normalization
- Query Optimization

---

# 5. Machine Learning

---

## 5.1 ML Fundamentals

- Supervised Learning
- Unsupervised Learning
- Semi-supervised Learning
- Self-supervised Learning
- Reinforcement Learning

---

## 5.2 Data Splitting

- Train
- Validation
- Test
- Cross Validation
- Stratified Sampling

---

## 5.3 Bias & Variance

- Underfitting
- Overfitting
- Bias
- Variance
- Regularization

---

## 5.4 Common Algorithms

### Regression

- Linear Regression
- Ridge
- Lasso
- ElasticNet

### Classification

- Logistic Regression
- Decision Tree
- Random Forest
- SVM
- Naive Bayes
- KNN
- XGBoost
- LightGBM
- CatBoost

### Clustering

- KMeans
- DBSCAN
- Hierarchical Clustering

### Dimensionality Reduction

- PCA
- t-SNE
- UMAP

---

## 5.5 Evaluation Metrics

### Classification

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- PR-AUC
- Confusion Matrix

### Regression

- MAE
- MSE
- RMSE
- R²

### Clustering

- Silhouette Score

---

## 5.6 Common Enterprise Problems

- Data Leakage
- Class Imbalance
- Feature Leakage
- Data Drift
- Concept Drift
- Distribution Shift
- Label Noise

---

# 6. Deep Learning

---

## Neural Network Fundamentals

- Perceptron
- MLP
- Activation Function
- Loss Function
- Backpropagation
- Gradient Descent

---

## Common Layers

- Dense
- Convolution
- Pooling
- Batch Normalization
- Dropout
- Embedding

---

## CNN

- Convolution
- Padding
- Stride
- Receptive Field
- Feature Map

---

## RNN Family

- RNN
- LSTM
- GRU
- Sequence Modeling

---

## Transformer

- Self Attention
- Multi-head Attention
- Positional Encoding
- Encoder
- Decoder
- Cross Attention

---

## Optimization

- Learning Rate Scheduler
- Weight Initialization
- Gradient Clipping
- Mixed Precision

---

## Common Issues

- Vanishing Gradient
- Exploding Gradient
- Overfitting
- Underfitting

---

# 7. Computer Vision

---

## Image Fundamentals

- RGB
- HSV
- Grayscale
- Resolution
- Channel

---

## OpenCV

- Resize
- Crop
- Rotate
- Threshold
- Morphology
- Contour
- Histogram

---

## Tasks

- Image Classification
- Object Detection
- Semantic Segmentation
- Instance Segmentation
- OCR
- Pose Estimation

---

## Object Detection

- Bounding Box
- IoU
- NMS
- Anchor
- Anchor-free
- mAP
- Precision
- Recall

---

## Popular Models

- YOLO
- Faster R-CNN
- SSD
- RetinaNet
- DETR

---

## Data Annotation

- Label Quality
- Dataset Split
- Augmentation
- COCO Format
- YOLO Format

---

# 8. Natural Language Processing (NLP)

---

## Text Processing

- Tokenization
- Stopword
- Lemmatization
- Stemming
- N-gram

---

## Embedding

- Word2Vec
- FastText
- GloVe
- Sentence Embedding

---

## Transformer Models

- BERT
- RoBERTa
- T5
- Llama
- Gemma
- Qwen

---

## NLP Tasks

- Text Classification
- Named Entity Recognition
- Question Answering
- Summarization
- Translation

---

# 9. Large Language Models (LLMs)

---

## Fundamentals

- Token
- Context Window
- Prompt
- Completion
- Temperature
- Top-k
- Top-p

---

## Prompt Engineering

- Zero-shot
- One-shot
- Few-shot
- Chain-of-Thought
- Structured Output
- Prompt Template

---

## RAG

- Chunking
- Embedding
- Vector Database
- Similarity Search
- Retrieval
- Re-ranking

---

## Fine-tuning

- SFT
- LoRA
- QLoRA
- PEFT
- Instruction Tuning

---

## LLM Evaluation

- Hallucination
- Faithfulness
- Groundedness
- Relevance
- Semantic Similarity

---

## Common Enterprise Topics

- Prompt Versioning
- Context Management
- Cost Optimization
- Latency Optimization
- Guardrails
- Safety

---

# 10. MLOps

---

## Model Lifecycle

- Training
- Validation
- Deployment
- Monitoring
- Retraining

---

## Experiment Tracking

- MLflow
- Weights & Biases

---

## Model Registry

- Versioning
- Rollback
- Promotion

---

## Monitoring

- Latency
- Throughput
- Drift Detection
- Model Performance

---

# 11. AI Deployment

---

## API

- REST API
- FastAPI
- Flask
- Request
- Response

---

## Docker

- Dockerfile
- Image
- Container
- Volume
- Network

---

## Serving

- TorchServe
- Triton Inference Server
- ONNX Runtime
- TensorRT

---

## GPU

- CUDA
- cuDNN
- Mixed Precision
- Batch Inference

---

# 12. Software Engineering

---

## Git

- Branch
- Merge
- Rebase
- Pull Request
- Conflict Resolution

---

## Clean Code

- SOLID
- DRY
- KISS
- Naming Convention

---

## Design

- Modular Design
- Layered Architecture
- Dependency Injection

---

## Testing

- Unit Test
- Integration Test
- Mock
- CI/CD

---

# 13. Linux

---

## Fundamentals

- Shell
- Bash
- Permission
- Process
- SSH

---

## Common Commands

- ls
- cd
- grep
- find
- ps
- top
- chmod
- scp
- rsync

---

# 14. Cloud

---

## Storage

- Object Storage
- Blob Storage

---

## Compute

- VM
- Container
- Kubernetes

---

## AI Services

- GPU Instance
- Managed AI Platform

---

# 15. AI System Design

---

## Pipeline Design

- Data Collection
- Data Validation
- Data Processing
- Training
- Evaluation
- Deployment
- Monitoring

---

## Scalability

- Batch Inference
- Online Inference
- Queue
- Cache

---

## Reliability

- Retry
- Logging
- Monitoring
- Alerting

---

## Security

- Authentication
- Authorization
- API Key
- Secret Management

---

# 16. Communication & Engineering Practices

---

## Technical Communication

- Explain technical concepts clearly
- Design discussion
- Trade-off analysis
- Root Cause Analysis

---

## Collaboration

- Agile
- Scrum
- Code Review
- Documentation

---

## Debugging

- Error Analysis
- Log Analysis
- Performance Profiling
- Reproducibility

---

# 17. Frequently Evaluated Cross-cutting Topics

Các chủ đề dưới đây không thuộc riêng một kỹ năng nhưng xuất hiện rất thường xuyên trong phỏng vấn AI Engineer.

- Time Complexity
- Space Complexity
- Memory Usage
- CPU vs GPU
- Batch Size
- Learning Rate
- Epoch
- Iteration
- Random Seed
- Reproducibility
- Data Leakage
- Feature Leakage
- Class Imbalance
- Data Drift
- Concept Drift
- Experiment Tracking
- Model Versioning
- Hyperparameter Tuning
- Error Analysis
- Ablation Study
- Explainability (XAI)
- Model Interpretability
- Precision vs Recall Trade-off
- Offline Evaluation
- Online Evaluation
- A/B Testing
- Inference Optimization
- Quantization
- Pruning
- Distillation
- ONNX
- TensorRT
- Edge Deployment
- GPU Memory Optimization
- Distributed Training
- Mixed Precision Training
- Caching
- Rate Limiting
- API Design
- Logging
- Monitoring
- Observability
- Failure Recovery
- Production Debugging
- Security for AI Systems