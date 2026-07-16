from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "Template"


ROLES = {
    "Software_Engineer": {
        "title": "Software Engineer",
        "focus": "thiết kế phần mềm, cấu trúc dữ liệu, thuật toán, debug và testing",
        "stack": "Git, HTTP, SQL, REST API, unit test, CI/CD",
        "artifact": "một module ứng dụng dễ bảo trì",
    },
    "Backend_Developer": {
        "title": "Backend Developer",
        "focus": "thiết kế API, cơ sở dữ liệu, xác thực, caching và xử lý bất đồng bộ",
        "stack": "Node.js, Java, Python, PostgreSQL, Redis, Docker",
        "artifact": "một dịch vụ backend chạy ổn định trên production",
    },
    "Frontend_Developer": {
        "title": "Frontend Developer",
        "focus": "thiết kế component, quản lý state, accessibility, hiệu năng và tích hợp API",
        "stack": "HTML, CSS, JavaScript, TypeScript, React, Vite",
        "artifact": "một giao diện web responsive cho người dùng cuối",
    },
    "Fullstack_Developer": {
        "title": "Fullstack Developer",
        "focus": "frontend, backend, hợp đồng API, thiết kế database và deployment",
        "stack": "React, Node.js, SQL/NoSQL, REST API, Docker",
        "artifact": "một tính năng web hoàn chỉnh từ UI đến backend",
    },
    "Web_Developer": {
        "title": "Web Developer",
        "focus": "nền tảng web, hành vi trình duyệt, responsive UI, form và gọi API",
        "stack": "HTML, CSS, JavaScript, REST API, kiến thức SEO cơ bản",
        "artifact": "một tính năng website đáng tin cậy",
    },
    "Mobile_Developer": {
        "title": "Mobile Developer",
        "focus": "UI mobile, navigation, offline handling, hiệu năng app và tích hợp API",
        "stack": "Android, iOS, React Native, Flutter, SQLite, push notification",
        "artifact": "một tính năng ứng dụng mobile",
    },
    "DevOps_Engineer": {
        "title": "DevOps Engineer",
        "focus": "CI/CD, container, hạ tầng, monitoring và độ tin cậy deployment",
        "stack": "Linux, Docker, Kubernetes, GitHub Actions, Terraform, Prometheus",
        "artifact": "một pipeline triển khai đáng tin cậy",
    },
    "Cloud_Engineer": {
        "title": "Cloud Engineer",
        "focus": "hạ tầng cloud, networking, IAM, scalability, observability và kiểm soát chi phí",
        "stack": "AWS, Azure, GCP, VPC, IAM, load balancer, autoscaling",
        "artifact": "một dịch vụ cloud có khả năng mở rộng",
    },
    "Data_Engineer": {
        "title": "Data Engineer",
        "focus": "data pipeline, ETL/ELT, batch processing, orchestration và data quality",
        "stack": "SQL, Python, Spark, Airflow, Kafka, dbt, data warehouse",
        "artifact": "một pipeline dữ liệu đáng tin cậy",
    },
    "Data_Scientist": {
        "title": "Data Scientist",
        "focus": "phân tích thống kê, feature engineering, đánh giá mô hình và experimentation",
        "stack": "Python, Pandas, scikit-learn, SQL, notebook, visualization",
        "artifact": "một dự án phân tích dự đoán",
    },
    "AI_Engineer": {
        "title": "AI Engineer",
        "focus": "tích hợp LLM, RAG, prompt design, evaluation, model serving và safety",
        "stack": "Python, embeddings, vector database, LangChain/LlamaIndex, FastAPI",
        "artifact": "một ứng dụng có tích hợp AI",
    },
    "QA_Automation_Engineer": {
        "title": "QA Automation Engineer",
        "focus": "test strategy, automation, regression testing, API testing và tích hợp CI",
        "stack": "Playwright, Selenium, Postman, pytest, Jest, CI/CD",
        "artifact": "một bộ test tự động",
    },
    "Tester": {
        "title": "Tester",
        "focus": "test case, bug report, exploratory testing, regression và acceptance criteria",
        "stack": "Jira, TestRail, Postman, browser devtools, SQL cơ bản",
        "artifact": "một test plan rõ ràng",
    },
    "Business_Analyst": {
        "title": "Business Analyst",
        "focus": "phân tích yêu cầu, giao tiếp stakeholder, process mapping và user story",
        "stack": "BRD, SRS, BPMN, user story, acceptance criteria, Jira",
        "artifact": "một bộ yêu cầu đã được xác thực",
    },
    "Cybersecurity_Analyst": {
        "title": "Cybersecurity Analyst",
        "focus": "threat modeling, vulnerability assessment, incident response và access control",
        "stack": "SIEM, OWASP, IAM, network logs, vulnerability scanner, EDR",
        "artifact": "một báo cáo đánh giá bảo mật",
    },
    "Database_Administrator": {
        "title": "Database Administrator",
        "focus": "vận hành database, backup, replication, query tuning và availability",
        "stack": "PostgreSQL, MySQL, SQL Server, index, replication, backup/restore",
        "artifact": "một môi trường database ổn định",
    },
}


LEVELS = {
    1: {
        "name": "Level 1",
        "experience": "0 - 1 năm kinh nghiệm",
        "expectation": "nắm khái niệm cơ bản, làm được nhiệm vụ nhỏ và giao tiếp rõ ràng",
    },
    2: {
        "name": "Level 2",
        "experience": "1 - 3 năm kinh nghiệm",
        "expectation": "biết cân nhắc trade-off, debug thực tế, hiểu production và có tinh thần ownership",
    },
    3: {
        "name": "Level 3",
        "experience": "3 - 5+ năm kinh nghiệm",
        "expectation": "thiết kế hệ thống, quản trị rủi ro, mentor, đảm bảo reliability và scalability",
    },
}


def question_bank(role, level):
    title = role["title"]
    focus = role["focus"]
    stack = role["stack"]
    artifact = role["artifact"]

    if level == 1:
        return [
            (
                "Dễ",
                f"Theo bạn, trách nhiệm chính của một {title} trong team phần mềm là gì?",
                f"Câu trả lời tốt nên nêu được việc hiểu yêu cầu được giao, đóng góp vào {artifact}, làm việc cẩn thận, báo sớm blocker, tuân thủ tiêu chuẩn của team và có tinh thần học hỏi.",
            ),
            (
                "Dễ",
                f"Bạn đã từng dùng công cụ hoặc công nghệ nào trong nhóm sau: {stack}?",
                "Ứng viên nên nói đúng công cụ mình đã dùng, mô tả một việc cụ thể đã làm với công cụ đó, ví dụ xây feature nhỏ, viết query, test endpoint hoặc cấu hình workflow đơn giản.",
            ),
            (
                "Dễ",
                f"Trước khi bàn giao {artifact}, bạn kiểm tra công việc của mình như thế nào?",
                "Câu trả lời nên có đọc lại yêu cầu, test luồng chính và edge case đơn giản, kiểm tra log hoặc output, nhờ review khi cần và ghi chú giả định quan trọng.",
            ),
            (
                "Trung bình",
                f"Hãy kể một bug hoặc vấn đề bạn từng gặp khi làm việc với {focus}. Bạn đã điều tra như thế nào?",
                "Ứng viên nên trình bày quy trình debug: tái hiện lỗi, khoanh vùng nguyên nhân, xem log/dữ liệu, đặt giả thuyết, thử fix và xác minh lại kết quả.",
            ),
            (
                "Trung bình",
                "Khi nhận một task chưa rõ yêu cầu, bạn sẽ hỏi những câu gì trước khi bắt đầu?",
                "Câu trả lời tốt nên hỏi về behavior mong muốn, input/output, acceptance criteria, edge case, deadline, dependency, constraint và cách đo task đã hoàn thành.",
            ),
            (
                "Trung bình",
                f"Trong công việc {title}, khác nhau giữa cách vá tạm và cách sửa đúng gốc là gì?",
                "Cách sửa đúng gốc xử lý nguyên nhân chính, có test, dễ bảo trì và ít tạo side effect. Cách vá tạm có thể dùng trong tình huống khẩn cấp nhưng cần ghi rõ rủi ro và kế hoạch xử lý tiếp theo.",
            ),
            (
                "Trung bình",
                "Bạn sẽ giải thích một vấn đề kỹ thuật cho teammate không chuyên kỹ thuật như thế nào?",
                "Ứng viên nên dùng ngôn ngữ đơn giản, tập trung vào impact, tránh jargon không cần thiết, dùng ví dụ hoặc sơ đồ và trình bày các lựa chọn kèm trade-off.",
            ),
            (
                "Khó",
                "Nếu bạn nhận hai task cùng deadline, bạn quyết định làm task nào trước như thế nào?",
                "Câu trả lời nên ưu tiên theo business impact, độ khẩn cấp, dependency, rủi ro và effort; đồng thời trao đổi sớm với lead/stakeholder thay vì im lặng trễ deadline.",
            ),
            (
                "Khó",
                "Nếu solution chạy đúng ở local nhưng fail ở môi trường chung, bạn xử lý thế nào?",
                "Ứng viên nên so sánh environment variable, version dependency, dữ liệu, log, build step, permission và config; sau đó đưa bằng chứng khi nhờ hỗ trợ.",
            ),
            (
                "Khó",
                "Nếu sau khi release bạn phát hiện phần mình làm gây regression, bạn sẽ làm gì?",
                "Câu trả lời tốt là minh bạch: báo team, hỗ trợ tái hiện lỗi, rollback hoặc hotfix nếu cần, thêm test ngăn tái diễn và ghi lại root cause ngắn gọn.",
            ),
        ]

    if level == 2:
        return [
            (
                "Dễ",
                f"Khi nhận một task {title} cỡ vừa, bạn chia nhỏ công việc trước khi implement như thế nào?",
                "Câu trả lời nên có review yêu cầu, xác định dependency, định nghĩa interface hoặc acceptance criteria, chia deliverable nhỏ, ước lượng rủi ro và lên kế hoạch test.",
            ),
            (
                "Dễ",
                f"Với {artifact}, bạn sẽ thêm những quality check nào trước khi đưa vào production?",
                "Ứng viên nên nhắc tới automated test, code review, lint/static check, validation edge case, logging/monitoring khi phù hợp và kế hoạch rollback.",
            ),
            (
                "Dễ",
                f"Theo bạn phần nào trong {focus} dễ phát sinh lỗi nhất, và bạn giảm lỗi bằng cách nào?",
                "Câu trả lời mạnh sẽ chỉ ra một khu vực rủi ro thực tế và đưa biện pháp cụ thể như validation, contract rõ ràng, test, observability, checklist review hoặc default an toàn.",
            ),
            (
                "Trung bình",
                "Hãy kể một lần bạn cải thiện performance, reliability hoặc maintainability trong công việc.",
                "Ứng viên nên nêu bối cảnh, vấn đề đo được hoặc quan sát được, hành động đã làm, trade-off đã cân nhắc và kết quả sau thay đổi.",
            ),
            (
                "Trung bình",
                "Bạn quyết định reuse solution có sẵn hay tự build mới dựa trên tiêu chí nào?",
                "Câu trả lời nên cân nhắc độ phù hợp yêu cầu, chi phí bảo trì, mức quen thuộc của team, security, scalability, license, thời gian delivery và khả năng mở rộng sau này.",
            ),
            (
                "Trung bình",
                f"Bạn sẽ thiết kế error handling cho {artifact} như thế nào?",
                "Nên có phân loại lỗi, message có ý nghĩa, logging, retry/fallback khi phù hợp, behavior an toàn cho user và tránh lộ thông tin nhạy cảm.",
            ),
            (
                "Trung bình",
                f"Khi review công việc của teammate liên quan tới {focus}, bạn tập trung vào điểm gì?",
                "Câu trả lời nên bao gồm correctness, readability, test coverage, edge case, security, performance và mức độ bám yêu cầu; feedback nên dựa trên bằng chứng và mang tính xây dựng.",
            ),
            (
                "Khó",
                f"Một sự cố production xuất hiện sau release liên quan tới {artifact}. Bạn sẽ xử lý incident như thế nào?",
                "Ứng viên nên đánh giá impact, mitigate hoặc rollback, xem log/metric, giao tiếp với team, phân tích root cause, đưa fix lâu dài và rút kinh nghiệm sau incident.",
            ),
            (
                "Khó",
                f"Bạn cân bằng tốc độ delivery và technical debt trong dự án dùng {stack} như thế nào?",
                "Câu trả lời tốt phân biệt debt chấp nhận được ngắn hạn với debt rủi ro, ghi lại trade-off, đặt tiêu chí cleanup, thêm test quanh vùng rủi ro và trao đổi impact với stakeholder.",
            ),
            (
                "Khó",
                "Nếu stakeholder yêu cầu một feature xung đột với kiến trúc hiện tại, bạn phản hồi thế nào?",
                "Ứng viên nên làm rõ nhu cầu business, đưa các phương án, giải thích cost/risk, đề xuất delivery theo phase nếu cần và tránh từ chối mà không có lựa chọn thay thế.",
            ),
        ]

    return [
        (
            "Dễ",
            f"Trước khi dẫn dắt xây dựng {artifact}, bạn thường đánh giá những rủi ro kiến trúc nào?",
            "Câu trả lời mạnh nên bao gồm scalability, reliability, data consistency, security, observability, operational complexity, năng lực team, chi phí và rủi ro migration.",
        ),
        (
            "Dễ",
            f"Bạn mentor một teammate ít kinh nghiệm hơn đang làm về {focus} như thế nào?",
            "Ứng viên nên nêu cách đặt context, pair hoặc review, đặt câu hỏi gợi mở, chia sẻ pattern, feedback cụ thể và vẫn để teammate sở hữu solution.",
        ),
        (
            "Dễ",
            f"Dấu hiệu nào cho thấy một solution trong hệ {stack} đang trở nên khó bảo trì?",
            "Các dấu hiệu gồm logic trùng lặp, boundary không rõ, test dễ vỡ, regression thường xuyên, delivery chậm, coupling ẩn, observability kém hoặc knowledge tập trung vào một người.",
        ),
        (
            "Trung bình",
            f"Hãy thiết kế high-level approach để scale {artifact} khi usage tăng 10 lần.",
            "Câu trả lời nên nói về xác định bottleneck, horizontal scaling, caching, async processing, database/index strategy, observability, load test và rollout theo phase.",
        ),
        (
            "Trung bình",
            "Bạn sẽ đưa một thay đổi kỹ thuật lớn vào hệ thống mà không làm gián đoạn delivery như thế nào?",
            "Nên có migration plan, compatibility layer, feature flag, rollout tăng dần, test, monitoring, rollback plan, tài liệu và giao tiếp stakeholder.",
        ),
        (
            "Trung bình",
            f"Bạn định nghĩa success metrics cho một dự án liên quan tới {focus} như thế nào?",
            "Ứng viên nên nêu cả metric kỹ thuật và business như latency, error rate, uptime, defect, user adoption, throughput, cost hoặc delivery predictability tùy vai trò.",
        ),
        (
            "Trung bình",
            f"Khi thiết kế {artifact}, bạn tiếp cận security và privacy như thế nào?",
            "Câu trả lời mạnh nên có least privilege, input validation, quản lý secret an toàn, audit/logging, data minimization, encryption khi cần, review dependency và tránh lộ dữ liệu nhạy cảm.",
        ),
        (
            "Khó",
            f"Hai senior engineer bất đồng hướng thiết kế cho {artifact}. Bạn sẽ dẫn dắt việc ra quyết định thế nào?",
            "Ứng viên nên frame quyết định quanh requirement, constraint, trade-off, thử nghiệm nhỏ, RFC/design review, mức độ reversible và timeline; thể hiện khả năng điều phối thay vì áp đặt.",
        ),
        (
            "Khó",
            f"Bạn xử lý một legacy system liên quan tới {focus} vừa business-critical vừa rủi ro khi sửa như thế nào?",
            "Câu trả lời nên có characterization test, observability, thay đổi nhỏ có rollback, strangler pattern hoặc thay thế từng phần, tài liệu và thống nhất rủi ro với stakeholder.",
        ),
        (
            "Khó",
            f"Bạn chuẩn bị {artifact} để một team khác có thể ownership lâu dài như thế nào?",
            "Nên có boundary rõ, tài liệu, runbook, dashboard, alert, test, hướng dẫn deploy, mô hình ownership, known limitations và buổi handover/training.",
        ),
    ]


def render_template(role, level):
    level_info = LEVELS[level]
    title = role["title"]
    questions = question_bank(role, level)
    lines = [
        f"# Bộ Câu Hỏi Phỏng Vấn {title} ({level_info['name']})",
        "",
        f"* **Vai trò:** {title}",
        f"* **Level:** {level_info['name']}",
        f"* **Kinh nghiệm:** {level_info['experience']}",
        f"* **Kỳ vọng:** {level_info['expectation']}",
        "",
        "---",
        "",
        "## CÂU HỎI DỄ (3 câu)",
        "",
    ]
    section_by_index = {
        4: ["---", "", "## CÂU HỎI TRUNG BÌNH (4 câu)", ""],
        8: ["---", "", "## CÂU HỎI KHÓ (3 câu)", ""],
    }
    for idx, (difficulty, question, answer) in enumerate(questions, start=1):
        if idx in section_by_index:
            lines.extend(section_by_index[idx])
        lines.extend(
            [
                f"### Câu {idx}",
                f"* **Độ khó:** {difficulty}",
                f"* **Câu hỏi:** {question}",
                f"* **Đáp án mẫu:** {answer}",
                "",
            ]
        )
    return "\n".join(lines).strip() + "\n"


def main():
    TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for slug, role in ROLES.items():
        for level in (1, 2, 3):
            path = TEMPLATE_DIR / f"{slug}_lv{level}.md"
            path.write_text(render_template(role, level), encoding="utf-8")
            written.append(path.name)
    print(f"Wrote {len(written)} Vietnamese IT templates")
    for name in written:
        print(f"+ {name}")


if __name__ == "__main__":
    main()
