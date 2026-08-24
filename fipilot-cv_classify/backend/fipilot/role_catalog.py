"""Canonical interview roles shared by resume matching and knowledge retrieval."""

ROLE_CATALOG = (
    {
        "id": "ai-engineer",
        "title": "AI Engineer",
        "knowledge_domain": "AI_Enginner",
        "keywords": (
            "ai engineer", "artificial intelligence", "machine learning", "deep learning",
            "generative ai", "llm", "large language model", "computer vision", "nlp",
            "pytorch", "tensorflow", "transformers", "rag", "embedding", "inference",
            "model training", "scikit-learn", "opencv", "yolo",
        ),
    },
    {
        "id": "backend-developer",
        "title": "Backend Developer",
        "knowledge_domain": "Backend Developer",
        "keywords": (
            "backend engineer", "backend developer", "back-end", "fastapi", "django",
            "flask", "spring boot", "node.js", "nestjs", "express", "rest api", "graphql",
            "postgresql", "mysql", "mongodb", "redis", "database", "microservice",
            "message queue", "kafka", "rabbitmq", "sqlalchemy",
        ),
    },
    {
        "id": "business-analyst",
        "title": "Business Analyst",
        "knowledge_domain": "Business Analyst",
        "keywords": (
            "business analyst", "business analysis", "requirements gathering",
            "requirement analysis", "business requirement document", "brd", "frd",
            "user story", "use case", "acceptance criteria", "bpmn", "uml",
            "stakeholder analysis", "gap analysis", "process modeling",
        ),
    },
    {
        "id": "data-engineer",
        "title": "Data Engineer",
        "knowledge_domain": "Data Engineer",
        "keywords": (
            "data engineer", "data engineering", "etl", "elt", "data pipeline",
            "data warehouse", "data lake", "apache airflow", "airflow", "apache spark",
            "spark", "hadoop", "dbt", "snowflake", "bigquery", "databricks",
        ),
    },
    {
        "id": "data-scientist",
        "title": "Data Scientist",
        "knowledge_domain": "Data Scientist",
        "keywords": (
            "data scientist", "data science", "statistics", "statistical modeling",
            "hypothesis testing", "feature engineering", "predictive modeling", "regression",
            "classification", "time series", "experiment design", "a/b testing", "pandas",
            "numpy", "scikit-learn",
        ),
    },
    {
        "id": "devops-engineer",
        "title": "DevOps Engineer",
        "knowledge_domain": "DevOps Engineer",
        "keywords": (
            "devops engineer", "devops", "ci/cd", "docker", "kubernetes", "terraform",
            "ansible", "jenkins", "github actions", "gitlab ci", "helm", "prometheus",
            "grafana", "azure devops", "infrastructure as code",
        ),
    },
    {
        "id": "full-stack-developer",
        "title": "Full Stack Developer",
        "knowledge_domain": "Full stack Developer",
        "keywords": (
            "full stack developer", "full-stack developer", "full stack", "full-stack",
            "mern", "mean stack", "react", "next.js", "node.js", "express",
            "frontend and backend", "end-to-end web",
        ),
    },
    {
        "id": "software-engineer",
        "title": "Software Engineer",
        "knowledge_domain": "Software Engineer",
        "keywords": (
            "software engineer", "software engineering", "data structures", "algorithms",
            "system design", "design patterns", "object-oriented", "distributed systems",
            "unit testing", "integration testing", "git", "java", "c++", "golang", "rust",
        ),
    },
    {
        "id": "tester-qa-qc",
        "title": "Tester QA QC",
        "knowledge_domain": "Tester_QA_QC",
        "keywords": (
            "tester", "qa engineer", "qc engineer", "quality assurance", "quality control",
            "manual testing", "automation testing", "selenium", "playwright", "cypress",
            "test case", "test plan", "regression testing", "performance testing", "postman",
        ),
    },
    {
        "id": "web-developer",
        "title": "Web Developer",
        "knowledge_domain": "Web Developer",
        "keywords": (
            "web developer", "web development", "frontend developer", "front-end",
            "html", "css", "javascript", "typescript", "responsive design",
            "web accessibility", "react", "angular", "vue", "php", "laravel", "wordpress",
        ),
    },
)


def role_definition(role: str) -> dict | None:
    normalized = "".join(character.casefold() for character in role if character.isalnum())
    for item in ROLE_CATALOG:
        aliases = (item["id"], item["title"], item["knowledge_domain"])
        if normalized in {
            "".join(character.casefold() for character in alias if character.isalnum())
            for alias in aliases
        }:
            return item
    return None


def knowledge_domain_for_role(role: str) -> str | None:
    definition = role_definition(role)
    return definition["knowledge_domain"] if definition is not None else None
