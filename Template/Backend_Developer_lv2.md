# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2)

* **Vai trò:** Backend Developer
* **Level:** Level 2
* **Kinh nghiệm:** 1 - 3 năm kinh nghiệm
* **Kỳ vọng:** biết cân nhắc trade-off, debug thực tế, hiểu production và có tinh thần ownership

---

## CÂU HỎI DỄ (3 câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Khi nhận một task Backend Developer cỡ vừa, bạn chia nhỏ công việc trước khi implement như thế nào?
* **Đáp án mẫu:** Câu trả lời nên có review yêu cầu, xác định dependency, định nghĩa interface hoặc acceptance criteria, chia deliverable nhỏ, ước lượng rủi ro và lên kế hoạch test.

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Với một dịch vụ backend chạy ổn định trên production, bạn sẽ thêm những quality check nào trước khi đưa vào production?
* **Đáp án mẫu:** Ứng viên nên nhắc tới automated test, code review, lint/static check, validation edge case, logging/monitoring khi phù hợp và kế hoạch rollback.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Theo bạn phần nào trong thiết kế API, cơ sở dữ liệu, xác thực, caching và xử lý bất đồng bộ dễ phát sinh lỗi nhất, và bạn giảm lỗi bằng cách nào?
* **Đáp án mẫu:** Câu trả lời mạnh sẽ chỉ ra một khu vực rủi ro thực tế và đưa biện pháp cụ thể như validation, contract rõ ràng, test, observability, checklist review hoặc default an toàn.

---

## CÂU HỎI TRUNG BÌNH (4 câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Hãy kể một lần bạn cải thiện performance, reliability hoặc maintainability trong công việc.
* **Đáp án mẫu:** Ứng viên nên nêu bối cảnh, vấn đề đo được hoặc quan sát được, hành động đã làm, trade-off đã cân nhắc và kết quả sau thay đổi.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn quyết định reuse solution có sẵn hay tự build mới dựa trên tiêu chí nào?
* **Đáp án mẫu:** Câu trả lời nên cân nhắc độ phù hợp yêu cầu, chi phí bảo trì, mức quen thuộc của team, security, scalability, license, thời gian delivery và khả năng mở rộng sau này.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Bạn sẽ thiết kế error handling cho một dịch vụ backend chạy ổn định trên production như thế nào?
* **Đáp án mẫu:** Nên có phân loại lỗi, message có ý nghĩa, logging, retry/fallback khi phù hợp, behavior an toàn cho user và tránh lộ thông tin nhạy cảm.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Khi review công việc của teammate liên quan tới thiết kế API, cơ sở dữ liệu, xác thực, caching và xử lý bất đồng bộ, bạn tập trung vào điểm gì?
* **Đáp án mẫu:** Câu trả lời nên bao gồm correctness, readability, test coverage, edge case, security, performance và mức độ bám yêu cầu; feedback nên dựa trên bằng chứng và mang tính xây dựng.

---

## CÂU HỎI KHÓ (3 câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Một sự cố production xuất hiện sau release liên quan tới một dịch vụ backend chạy ổn định trên production. Bạn sẽ xử lý incident như thế nào?
* **Đáp án mẫu:** Ứng viên nên đánh giá impact, mitigate hoặc rollback, xem log/metric, giao tiếp với team, phân tích root cause, đưa fix lâu dài và rút kinh nghiệm sau incident.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Bạn cân bằng tốc độ delivery và technical debt trong dự án dùng Node.js, Java, Python, PostgreSQL, Redis, Docker như thế nào?
* **Đáp án mẫu:** Câu trả lời tốt phân biệt debt chấp nhận được ngắn hạn với debt rủi ro, ghi lại trade-off, đặt tiêu chí cleanup, thêm test quanh vùng rủi ro và trao đổi impact với stakeholder.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Nếu stakeholder yêu cầu một feature xung đột với kiến trúc hiện tại, bạn phản hồi thế nào?
* **Đáp án mẫu:** Ứng viên nên làm rõ nhu cầu business, đưa các phương án, giải thích cost/risk, đề xuất delivery theo phase nếu cần và tránh từ chối mà không có lựa chọn thay thế.
