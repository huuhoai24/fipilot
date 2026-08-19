# Dimensionality Reduction

#### PCA

- Linear projections tối đa hóa variance
- Centering và scaling considerations
- Explained variance
- Components không luôn dễ diễn giải
- Fit chỉ trên training data

#### t-SNE

- Nonlinear visualization
- Bảo toàn local neighborhoods tốt hơn global geometry
- Perplexity và random seed sensitivity
- Không dùng khoảng cách giữa clusters như bằng chứng tuyệt đối
- Không phải default feature transform cho production

#### UMAP

- Nonlinear manifold-based embedding
- `n_neighbors`, `min_dist` và metric
- Thường dùng visualization hoặc downstream representation
- Stochastic và parameter-sensitive
- Global structure không được bảo toàn hoàn hảo
