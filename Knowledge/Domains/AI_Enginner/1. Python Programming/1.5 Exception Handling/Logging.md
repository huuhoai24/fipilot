# Logging

- Ghi exception với stack trace
- `logger.exception()` trong exception handler
- Log level phù hợp
- Không log secrets hoặc dữ liệu nhạy cảm
- Tránh vừa log vừa raise ở nhiều tầng gây duplicate logs
