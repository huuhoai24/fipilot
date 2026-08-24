# Automation Reliability

- **Flaky Tests**: kết quả không ổn định khi product không thay đổi
- **Explicit Wait**: chờ condition cụ thể với timeout
- **Implicit Wait**: global element lookup wait; có thể tạo timing khó đoán khi kết hợp waits khác
- **Synchronization**: đồng bộ với UI, network, animation, message hoặc backend state
- **Retry Mechanism**: chỉ dùng có kiểm soát để phân loại transient failures, không che defects
- **Stable Selectors**: role, accessible name hoặc dedicated test attributes có contract rõ
- Theo dõi flake rate, quarantine ngắn hạn và sửa root cause
