# Partitions and Shuffle

- Partition là đơn vị parallelism
- Shuffle di chuyển data giữa executors
- Join, group và repartition có thể gây shuffle
- Data skew tạo stragglers
- Partition count ảnh hưởng overhead và utilization
