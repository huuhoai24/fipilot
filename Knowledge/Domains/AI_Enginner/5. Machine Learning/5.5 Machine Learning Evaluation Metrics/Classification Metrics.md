# Classification Metrics

#### Accuracy

- Tỷ lệ dự đoán đúng
- Có thể gây hiểu nhầm với class imbalance
- Phù hợp khi class/cost tương đối cân bằng

#### Precision

- `TP / (TP + FP)`
- Trong các predicted positives, bao nhiêu là đúng
- Quan trọng khi false positive tốn kém

#### Recall

- `TP / (TP + FN)`
- Trong các actual positives, bao nhiêu được phát hiện
- Quan trọng khi false negative tốn kém

#### F1-score

- Harmonic mean của precision và recall
- Bỏ qua true negatives
- Threshold-dependent
- Macro, micro và weighted variants

#### ROC-AUC

- Ranking quality qua TPR/FPR ở nhiều thresholds
- Có thể trông cao trong highly imbalanced datasets
- Không trực tiếp chọn operating threshold

#### PR-AUC

- Precision–recall trade-off qua thresholds
- Thường thông tin hơn khi positive class hiếm
- Baseline phụ thuộc prevalence

#### Confusion Matrix

- TP, FP, TN và FN
- Per-class matrix cho multiclass
- Cần xem counts và normalized views
