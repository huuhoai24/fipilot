# Pickle

- Python-specific object serialization
- `pickle.dump()`, `load()`, `dumps()`, `loads()`
- Không bảo đảm tương thích lâu dài giữa mọi environment/version
- Không dùng để trao đổi dữ liệu độc lập ngôn ngữ
- Không load pickle từ nguồn không tin cậy vì có thể thực thi mã độc
