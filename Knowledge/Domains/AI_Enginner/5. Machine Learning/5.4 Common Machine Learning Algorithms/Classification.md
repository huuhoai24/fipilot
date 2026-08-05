# Classification

#### Logistic Regression

- Linear decision function và probability qua sigmoid/softmax
- Log-loss
- Regularization
- Threshold
- Coefficient interpretation với điều kiện phù hợp

#### Decision Tree

- Recursive feature splits
- Classification/regression criteria
- Depth, leaf size và pruning
- Nonlinear interactions
- Overfitting risk

#### Random Forest

- Bagging trees
- Feature subsampling
- Out-of-bag estimate ở mức khái niệm
- Giảm variance
- Memory và inference cost

#### SVM

- Maximum-margin classifier
- Linear và kernel SVM
- `C`, kernel parameters và scaling
- Training cost với dataset lớn
- Probability calibration không mặc định

#### Naive Bayes

- Conditional independence assumption
- Gaussian, Multinomial và Bernoulli variants
- Hiệu quả với một số text/count features
- Fast baseline

#### KNN

- Instance-based prediction
- Distance metric
- `k`
- Scaling quan trọng
- Prediction cost và curse of dimensionality

#### XGBoost

- Gradient-boosted decision trees
- Regularized objective
- Learning rate, depth, estimators, subsampling
- Missing values
- Strong tabular baseline

#### LightGBM

- Gradient boosting với histogram-based training
- Leaf-wise growth
- Categorical support tùy API/config
- Tốc độ và memory tốt cho nhiều tabular workloads
- Overfitting control

#### CatBoost

- Gradient boosting
- Native handling cho categorical features
- Ordered target statistics để giảm leakage theo thiết kế
- Strong default cho categorical-heavy data
