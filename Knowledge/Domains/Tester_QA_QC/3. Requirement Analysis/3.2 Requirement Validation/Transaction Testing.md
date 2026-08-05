# Transaction Testing

- **ACID**: atomicity, consistency, isolation và durability
- **Commit**: changes được xác nhận và trở nên persistent theo transaction semantics
- **Rollback**: hủy changes chưa commit hoặc phục hồi sau lỗi
- **Isolation Levels**: trade-off giữa anomalies và concurrency
- **Locking**: row/table locks, blocking và timeout
- Kiểm tra lost update, dirty read, non-repeatable read, phantom và deadlock khi phù hợp
