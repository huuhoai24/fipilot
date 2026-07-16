# Bộ Câu Hỏi Phỏng Vấn Backend Developer (Level 2) - Tập Đề Clean Architecture và DDD Basics (19)

* **Role:** Backend Developer
* **Level:** Level 2
* **Experience:** 1 - 3 năm kinh nghiệm

---

## CÂU HỎI DỄ (3 câu - Trọng số: 0.15 / câu)

### Câu 1
* **Độ khó:** Dễ
* **Câu hỏi:** Clean Architecture là gì? Nêu tên các lớp (layers) cơ bản cấu thành nên Clean Architecture.
* **expected_key_points:**
  - id: KP1_1
    content: Khái niệm Clean Architecture
    keypoint_weight: 0.5
    description: Là kiến trúc thiết kế phần mềm tập trung vào việc tách biệt mã nguồn thành các lớp độc lập, đặt lớp nghiệp vụ cốt lõi làm trung tâm không phụ thuộc vào framework bên ngoài.
  - id: KP1_2
    content: Các lớp cơ bản trong Clean Architecture
    keypoint_weight: 0.5
    description: Entities (Nghiệp vụ cốt lõi doanh nghiệp), Use Cases (Luồng xử lý nghiệp vụ ứng dụng), Interface Adapters (Controllers, Gateways, Presenters), và Frameworks & Drivers (Web, DB, Devices).

### Câu 2
* **Độ khó:** Dễ
* **Câu hỏi:** Giải thích quy tắc phụ thuộc (Dependency Rule) trong Clean Architecture. Chiều phụ thuộc giữa các lớp phải đi như thế nào?
* **expected_key_points:**
  - id: KP2_1
    content: Nguyên lý chiều phụ thuộc hướng tâm
    keypoint_weight: 0.6
    description: Chiều phụ thuộc bắt buộc chỉ được trỏ từ các lớp bên ngoài (Frameworks, Web, DB) hướng vào các lớp bên trong (Use Cases, Entities).
  - id: KP2_2
    content: Sự độc lập của tầng nghiệp vụ
    keypoint_weight: 0.4
    description: Các lớp bên trong (Entities, Use Cases) hoàn toàn không được biết bất kỳ thông tin gì về mã nguồn của các lớp bên ngoài (ví dụ: use case không chứa cú pháp SQL hay framework web).

### Câu 3
* **Độ khó:** Dễ
* **Câu hỏi:** Domain-Driven Design (DDD) là gì? Phân biệt sự khác nhau giữa hai khái niệm: Ubiquitous Language (Ngôn ngữ chung) và Bounded Context.
* **expected_key_points:**
  - id: KP3_1
    content: Khái niệm Ubiquitous Language
    keypoint_weight: 0.5
    description: Là bộ từ vựng và ngôn ngữ chung thống nhất được sử dụng bởi cả lập trình viên và chuyên gia nghiệp vụ (Domain Experts) để tránh hiểu nhầm.
  - id: KP3_2
    content: Khái niệm Bounded Context
    keypoint_weight: 0.5
    description: Là một ranh giới logic bao quanh một phân vùng nghiệp vụ xác định; trong ranh giới đó, các từ vựng của ngôn ngữ chung mang một ngữ nghĩa duy nhất và chính xác.

---

## CÂU HỎI TRUNG BÌNH (4 câu - Trọng số: 0.1 / câu)

### Câu 4
* **Độ khó:** Trung bình
* **Câu hỏi:** Phân biệt sự khác nhau giữa Entity (Thực thể) và Value Object trong Domain-Driven Design (DDD). Cho ví dụ thực tế.
* **expected_key_points:**
  - id: KP4_1
    content: Bản chất Entity vs Value Object
    keypoint_weight: 0.6
    description: Entity được định nghĩa bởi một định danh duy nhất (Identity) không đổi theo thời gian. Value Object không có định danh, được định nghĩa hoàn toàn bởi các thuộc tính của nó và mang tính bất biến (immutable).
  - id: KP4_2
    content: Ví dụ thực tế minh họa
    keypoint_weight: 0.4
    description: Người dùng (User) là Entity vì có ID không đổi; Địa chỉ nhà (Address) gồm đường, quận, thành phố là Value Object vì nếu đổi đường ta tạo Address mới.

### Câu 5
* **Độ khó:** Trung bình
* **Câu hỏi:** Giải thích khái niệm Aggregate và Aggregate Root trong Domain-Driven Design (DDD). Tại sao việc cập nhật dữ liệu phải đi qua Aggregate Root?
* **expected_key_points:**
  - id: KP5_1
    content: Khái niệm Aggregate và Aggregate Root
    keypoint_weight: 0.5
    description: Aggregate là một nhóm các đối tượng (Entities/Value Objects) liên kết chặt chẽ với nhau. Aggregate Root là Entity duy nhất làm cổng giao tiếp đại diện cho cả nhóm đó từ bên ngoài.
  - id: KP5_2
    content: Bảo vệ tính toàn vẹn dữ liệu (Invariants)
    keypoint_weight: 0.5
    description: Ngăn không cho code bên ngoài thay đổi trực tiếp các đối tượng con bên trong; mọi cập nhật phải gọi hàm của Aggregate Root để đảm bảo kiểm tra logic toàn vẹn của cả nhóm.

### Câu 6
* **Độ khó:** Trung bình
* **Câu hỏi:** Làm thế nào để áp dụng nguyên lý Dependency Inversion Principle (DIP) để tách biệt tầng Use Case nghiệp vụ khỏi cơ sở dữ liệu quan hệ cụ thể trong Clean Architecture?
* **expected_key_points:**
  - id: KP6_1
    content: Định nghĩa Interface ở tầng Use Case
    keypoint_weight: 0.5
    description: Tầng Use Case định nghĩa một interface cổng giao tiếp (ví dụ: `UserRepository` interface) khai báo các phương thức đọc ghi cần thiết.
  - id: KP6_2
    content: Triển khai Concrete Class ở tầng Infrastructure
    keypoint_weight: 0.5
    description: Tầng ngoài (Infrastructure) viết lớp triển khai cụ thể (`SqlUserRepository` implement `UserRepository` sử dụng JPA/ORM); dùng DI framework để tiêm class này vào Use Case.

### Câu 7
* **Độ khó:** Trung bình
* **Câu hỏi:** Thế nào là khái niệm DTO (Data Transfer Object) và Domain Model? Tại sao chúng ta cần chuyển đổi giữa chúng tại biên của các tầng kiến trúc?
* **expected_key_points:**
  - id: KP7_1
    content: Đặc trưng DTO vs Domain Model
    keypoint_weight: 0.5
    description: DTO là đối tượng thuần túy chứa dữ liệu để truyền tải qua mạng (giữa Client và API). Domain Model chứa cả dữ liệu và các quy tắc nghiệp vụ logic thực tế.
  - id: KP7_2
    content: Lý do cần chuyển đổi (Mapping)
    keypoint_weight: 0.5
    description: Để bảo vệ mô hình nghiệp vụ cốt lõi không bị ảnh hưởng bởi sự thay đổi giao diện API; tránh việc để lộ các thông tin nội bộ của hệ thống ra ngoài mạng.

---

## CÂU HỎI KHÓ (3 câu - Trọng số: 0.05 / câu)

### Câu 8
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế cấu trúc thư mục dự án Backend (Package Structure) áp dụng kiến trúc Clean Architecture kết hợp các nguyên lý DDD cho phân hệ quản lý tài khoản người dùng.
* **expected_key_points:**
  - id: KP8_1
    content: Thiết kế tầng Domain và Application
    keypoint_weight: 0.5
    description: Tầng Domain (`domain/`): chứa Entities (User), Value Objects, và interfaces repositories. Tầng Application (`application/`): chứa Use Cases (RegisterUserUseCase) xử lý nghiệp vụ ứng dụng.
  - id: KP8_2
    content: Thiết kế tầng Adapters và Infrastructure
    keypoint_weight: 0.5
    description: Tầng Adapters (`adapters/`): chứa REST Controllers, DTOs và Serializers. Tầng Infrastructure (`infrastructure/`): chứa cấu hình DB, cấu hình ORM, gọi API bên thứ ba.

### Câu 9
* **Độ khó:** Khó
* **Câu hỏi:** Thiết kế giải pháp giao tiếp bất đồng bộ giữa các Bounded Contexts khác nhau (ví dụ: Context Đặt hàng và Context Vận chuyển) sử dụng Event-Driven Architecture và Domain Events.
* **expected_key_points:**
  - id: KP9_1
    content: Định nghĩa và xuất bản Domain Event
    keypoint_weight: 0.5
    description: Khi đặt hàng thành công, Context Đặt hàng tạo sự kiện `OrderCreatedEvent` -> xuất bản sự kiện này ra Message Broker (Kafka) ngay trong luồng transaction.
  - id: KP9_2
    content: Tiêu thụ sự kiện an toàn ở Bounded Context khác
    keypoint_weight: 0.5
    description: Context Vận chuyển lắng nghe sự kiện từ Kafka -> tự động khởi tạo đơn giao hàng mới trong DB của nó, đảm bảo tính liên kết lỏng (loose coupling) hoàn hảo giữa 2 contexts.

### Câu 10
* **Độ khó:** Khó
* **Câu hỏi:** Phân tích tác động và thiết kế giải pháp khắc phục hiện tượng rò rỉ khái niệm nghiệp vụ (Anemic Domain Model) trong phát triển phần mềm nghiệp vụ lớn.
* **expected_key_points:**
  - id: KP10_1
    content: Anemic Domain Model là gì
    keypoint_weight: 0.5
    description: Là hiện tượng các lớp Domain Model chỉ chứa các thuộc tính getter/setter thuần túy (không chứa hành vi logic), toàn bộ logic xử lý bị đẩy sang lớp Service dồn ứ.
  - id: KP10_2
    content: Refactor sang Rich Domain Model
    keypoint_weight: 0.5
    description: Di chuyển các hàm kiểm tra logic, thay đổi trạng thái của thực thể trực tiếp vào bên trong lớp Model đó; lớp Service chỉ đóng vai trò điều phối gọi hàm, tuân thủ đúng OOP.

