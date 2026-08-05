# GIL (Global Interpreter Lock)

- Một thread thực thi Python bytecode tại một thời điểm trong CPython truyền thống
- I/O-bound so với CPU-bound
- Native extensions có thể release GIL
- GIL không tự bảo đảm thread safety cho application logic
