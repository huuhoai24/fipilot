# Bộ Câu Hỏi Phỏng Vấn Cloud Engineer (Level 3)

* **Vai trò:** Cloud Engineer
* **Level:** Level 3
* **Kinh nghiệm:** 3 - 5+ năm kinh nghiệm
* **Kỳ vọng:** thiết kế hệ thống, quản trị rủi ro, mentor, đảm bảo reliability và scalability

---

## CÂU HỎI DỄ (3 câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trước khi dẫn dắt xây dựng một dịch vụ cloud có khả năng mở rộng, bạn thường đánh giá những rủi ro kiến trúc nào?
* **Đáp án mẫu:** Câu trả lời mạnh nên bao gồm scalability, reliability, data consistency, security, observability, operational complexity, năng lực team, chi phí và rủi ro migration.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Bạn mentor một teammate ít kinh nghiệm hơn đang làm về hạ tầng cloud, networking, IAM, scalability, observability và kiểm soát chi phí như thế nào?
* **Đáp án mẫu:** Ứng viên nên nêu cách đặt context, pair hoặc review, đặt câu hỏi gợi mở, chia sẻ pattern, feedback cụ thể và vẫn để teammate sở hữu solution.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Dấu hiệu nào cho thấy một solution trong hệ AWS, Azure, GCP, VPC, IAM, load balancer, autoscaling đang trở nên khó bảo trì?
* **Đáp án mẫu:** Các dấu hiệu gồm logic trùng lặp, boundary không rõ, test dễ vỡ, regression thường xuyên, delivery chậm, coupling ẩn, observability kém hoặc knowledge tập trung vào một người.

---

## CÂU HỎI TRUNG BÌNH (4 câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy thiết kế high-level approach để scale một dịch vụ cloud có khả năng mở rộng khi usage tăng 10 lần.
* **Đáp án mẫu:** Câu trả lời nên nói về xác định bottleneck, horizontal scaling, caching, async processing, database/index strategy, observability, load test và rollout theo phase.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn sẽ đưa một thay đổi kỹ thuật lớn vào hệ thống mà không làm gián đoạn delivery như thế nào?
* **Đáp án mẫu:** Nên có migration plan, compatibility layer, feature flag, rollout tăng dần, test, monitoring, rollback plan, tài liệu và giao tiếp stakeholder.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn định nghĩa success metrics cho một dự án liên quan tới hạ tầng cloud, networking, IAM, scalability, observability và kiểm soát chi phí như thế nào?
* **Đáp án mẫu:** Ứng viên nên nêu cả metric kỹ thuật và business như latency, error rate, uptime, defect, user adoption, throughput, cost hoặc delivery predictability tùy vai trò.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi thiết kế một dịch vụ cloud có khả năng mở rộng, bạn tiếp cận security và privacy như thế nào?
* **Đáp án mẫu:** Câu trả lời mạnh nên có least privilege, input validation, quản lý secret an toàn, audit/logging, data minimization, encryption khi cần, review dependency và tránh lộ dữ liệu nhạy cảm.

---

## CÂU HỎI KHÓ (3 câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Hai senior engineer bất đồng hướng thiết kế cho một dịch vụ cloud có khả năng mở rộng. Bạn sẽ dẫn dắt việc ra quyết định thế nào?
* **Đáp án mẫu:** Ứng viên nên frame quyết định quanh requirement, constraint, trade-off, thử nghiệm nhỏ, RFC/design review, mức độ reversible và timeline; thể hiện khả năng điều phối thay vì áp đặt.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Bạn xử lý một legacy system liên quan tới hạ tầng cloud, networking, IAM, scalability, observability và kiểm soát chi phí vừa business-critical vừa rủi ro khi sửa như thế nào?
* **Đáp án mẫu:** Câu trả lời nên có characterization test, observability, thay đổi nhỏ có rollback, strangler pattern hoặc thay thế từng phần, tài liệu và thống nhất rủi ro với stakeholder.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Bạn chuẩn bị một dịch vụ cloud có khả năng mở rộng để một team khác có thể ownership lâu dài như thế nào?
* **Đáp án mẫu:** Nên có boundary rõ, tài liệu, runbook, dashboard, alert, test, hướng dẫn deploy, mô hình ownership, known limitations và buổi handover/training.
