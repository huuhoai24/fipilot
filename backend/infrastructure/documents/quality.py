from __future__ import annotations

import re
import unicodedata
from enum import Enum


class TextQuality(str, Enum):
    NORMAL = "normal"
    SPARSE = "sparse"
    IMAGE_ONLY = "image_only"
    UNUSABLE = "unusable"


def normalize_extracted_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text or "").replace("\x00", "")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in normalized.splitlines()]
    return "\n".join(line for line in lines if line).strip()


def classify_text_quality(page_texts: list[str]) -> TextQuality:
    if not page_texts:
        return TextQuality.UNUSABLE
    meaningful = sum(sum(character.isalnum() for character in text) for text in page_texts)
    if meaningful == 0:
        return TextQuality.IMAGE_ONLY
    nonblank_pages = sum(bool(normalize_extracted_text(text)) for text in page_texts)
    if meaningful < 50 or nonblank_pages < max(1, len(page_texts) // 2):
        return TextQuality.SPARSE
    return TextQuality.NORMAL
