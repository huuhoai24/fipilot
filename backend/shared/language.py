"""Language helpers shared by interview services."""


def normalize_language(language: str | None) -> str:
    value = (language or "vi").strip().lower()
    return value if value in {"vi", "en"} else "vi"

