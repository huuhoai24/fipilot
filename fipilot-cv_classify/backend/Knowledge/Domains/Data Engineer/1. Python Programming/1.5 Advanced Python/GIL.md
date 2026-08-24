# GIL

- Global Interpreter Lock trong CPython
- Ảnh hưởng đến CPU-bound Python threads
- I/O-bound threads vẫn có thể hữu ích
- GIL không làm mọi thao tác thread-safe
- Chọn multiprocessing hoặc native/vectorized code cho CPU-bound workloads
