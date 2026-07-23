from __future__ import annotations


TECHNICAL_VOCABULARY: dict[str, tuple[str, ...]] = {
    "ai_engineer": (
        "AI Engineer",
        "machine learning",
        "deep learning",
        "PyTorch",
        "TensorFlow",
        "YOLO",
        "LLM",
        "RAG",
        "Vertex AI",
    ),
    "backend": (
        "Backend",
        "FastAPI",
        "Django",
        "Node.js",
        "REST API",
        "WebSocket",
        "PostgreSQL",
        "Redis",
        "microservices",
    ),
    "frontend": (
        "Frontend",
        "React",
        "TypeScript",
        "JavaScript",
        "Next.js",
        "Vue",
        "Web Audio API",
        "CSS",
    ),
    "data_engineer": (
        "Data Engineer",
        "Apache Spark",
        "Kafka",
        "Airflow",
        "BigQuery",
        "ETL",
        "data warehouse",
        "dbt",
    ),
    "devops": (
        "DevOps",
        "Docker",
        "Kubernetes",
        "Terraform",
        "Cloud Run",
        "CI/CD",
        "GitHub Actions",
        "observability",
    ),
}


def vocabulary_hotwords(
    profile: str,
    custom_hotwords: list[str] | None = None,
) -> str:
    normalized = profile.strip().lower().replace(" ", "_")
    profiles = (
        TECHNICAL_VOCABULARY.values()
        if normalized == "auto"
        else [TECHNICAL_VOCABULARY.get(normalized, ())]
    )
    values: list[str] = []
    seen: set[str] = set()
    for value in [
        *(item for group in profiles for item in group),
        *(custom_hotwords or []),
    ]:
        normalized_value = value.strip()
        key = normalized_value.casefold()
        if normalized_value and key not in seen:
            seen.add(key)
            values.append(normalized_value)
    return ", ".join(values)
