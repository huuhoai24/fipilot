# Bộ Câu Hỏi Phỏng Vấn Software Engineer (Level 1)

* **Role:** Software Engineer
* **Level:** Level 1
* **Experience:** 0 - 1 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Trong lập trình hướng đối tượng (OOP), bốn tính chất cốt lõi là gì? Hãy gọi tên chúng.
* **Đáp án mẫu:** Bốn tính chất cốt lõi của OOP bao gồm: Tính đóng gói (Encapsulation), Tính kế thừa (Inheritance), Tính đa hình (Polymorphism), và Tính trừu tượng (Abstraction).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Cấu trúc dữ liệu Stack (Ngăn xếp) và Queue (Hàng đợi) hoạt động theo cơ chế quản lý phần tử khác nhau như thế nào?
* **Đáp án mẫu:** - Stack hoạt động theo cơ chế LIFO (Last In, First Out) - phần tử nào vào sau cùng sẽ được lấy ra đầu tiên.
  - Queue hoạt động theo cơ chế FIFO (First In, First Out) - phần tử nào vào trước sẽ được lấy ra đầu tiên.

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Để kiểm tra xem một phần tử có tồn tại trong một danh sách đã được sắp xếp hay không, thuật toán Tìm kiếm nhị phân (Binary Search) có độ phức tạp thời gian (Time Complexity) ở trường hợp xấu nhất là bao nhiêu?
* **Đáp án mẫu:** Độ phức tạp thời gian ở trường hợp xấu nhất của thuật toán Tìm kiếm nhị phân là O(log n), trong đó n là số lượng phần tử của danh sách.

---

## CÂU HỎI TRUNG BÌNH (4 câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Trong thiết kế phần mềm, nguyên lý Single Responsibility Principle (SRP) thuộc hệ nguyên lý SOLID yêu cầu điều gì đối với một Class?
* **Đáp án mẫu:** Nguyên lý SRP yêu cầu một Class chỉ nên đảm nhận một trách nhiệm duy nhất và chỉ nên có một lý do duy nhất để thay đổi. Điều này giúp mã nguồn dễ bảo trì, kiểm thử và tách biệt các module logic rõ ràng hơn.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Khái niệm "Memory Leak" (Rò rỉ bộ nhớ) trong phát triển phần mềm là gì và tác hại của nó đối với ứng dụng nếu chạy lâu dài?
* **Đáp án mẫu:** Memory Leak là hiện tượng ứng dụng cấp phát vùng nhớ cho dữ liệu nhưng không giải phóng lại cho hệ điều hành khi dữ liệu đó không còn được sử dụng nữa. Tác hại là làm tiêu tốn bộ nhớ RAM theo thời gian, dẫn đến ứng dụng bị chậm, đơ hoặc bị hệ điều hành tắt do cạn kiệt bộ nhớ (OOM - Out Of Memory).

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Sự khác biệt về cách thức tổ chức vùng nhớ và hiệu năng truy cập phần tử giữa hai cấu trúc dữ liệu Array (Mảng) và Singly Linked List (Danh sách liên kết đơn) là gì?
* **Đáp án mẫu:** - Array lưu trữ các phần tử ở các ô nhớ liên tiếp nhau, cho phép truy cập ngẫu nhiên phần tử qua index với tốc độ O(1), nhưng việc chèn/xóa phần tử ở giữa mảng tốn O(n).
  - Linked List lưu trữ các phần tử ở các ô nhớ rải rác được liên kết qua con trỏ, việc truy cập phần tử tốn O(n) do phải duyệt tuần tự, nhưng việc chèn/xóa phần tử khi đã biết vị trí chỉ tốn O(1).

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Lập trình viên sử dụng kỹ thuật Unit Test (Kiểm thử đơn vị) nhằm mục đích gì trong pipeline phát triển phần mềm?
* **Đáp án mẫu:** Unit Test dùng để kiểm thử độc lập các đơn vị mã nguồn nhỏ nhất (thường là các hàm hoặc các phương thức của class) để đảm bảo chúng chạy đúng logic thiết kế ban đầu, giúp phát hiện lỗi sớm trước khi tích hợp hệ thống và tăng độ tự tin khi refactor code.

---

## CÂU HỎI KHÓ (3 câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Trong lập trình đồng thời (Concurrent Programming), hiện tượng Deadlock xảy ra khi nào? Nêu điều kiện cơ bản dẫn đến hiện tượng này.
* **Đáp án mẫu:** Deadlock xảy ra khi hai hoặc nhiều tiến trình/luồng (threads) bị treo vĩnh viễn vì mỗi bên đều đang nắm giữ một tài nguyên và chờ đợi để được cấp phát tài nguyên mà bên kia đang nắm giữ. Điều kiện cơ bản là có sự tranh chấp tài nguyên độc quyền (Mutual Exclusion) và xảy ra chu kỳ chờ đợi khép kín (Circular Wait).

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Kỹ thuật Lập trình động (Dynamic Programming) khác với kỹ thuật Chia để trị (Divide and Conquer) truyền thống ở điểm cốt lõi nào khi tối ưu bài toán?
* **Đáp án mẫu:** Cả hai đều chia bài toán lớn thành các bài toán con. Tuy nhiên, Chia để trị áp dụng khi các bài toán con độc lập nhau (như Merge Sort). Lập trình động áp dụng khi các bài toán con bị trùng lặp (Overlapping Subproblems); nó tối ưu bằng cách lưu lại kết quả của bài toán con đã giải (Memoization hoặc Tabulation) để tái sử dụng, tránh việc phải tính toán lại nhiều lần.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Khi thiết kế một hệ thống lớn, mẫu thiết kế (Design Pattern) mang tên "Observer Pattern" giải quyết bài toán giao tiếp giữa các đối tượng như thế nào?
* **Đáp án mẫu:** Observer Pattern định nghĩa một mối quan hệ phụ thuộc một-nhiều (one-to-many) giữa các đối tượng. Khi một đối tượng thay đổi trạng thái (Subject), tất cả các đối tượng phụ thuộc của nó (Observers) sẽ tự động nhận được thông báo và cập nhật thông tin một cách bất đồng bộ mà không cần các đối tượng phải liên kết quá chặt chẽ (loose coupling) với nhau.