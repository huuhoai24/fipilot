from __future__ import annotations

from typing import Protocol


class OCREngine(Protocol):
    def recognize(self, image_bytes: bytes) -> str: ...


class RapidOCREngine:
    """Lazy local OCR adapter; model loading occurs only on an OCR path."""

    def __init__(self) -> None:
        self._engine = None

    @property
    def engine(self):
        if self._engine is None:
            from rapidocr import RapidOCR

            self._engine = RapidOCR()
        return self._engine

    def recognize(self, image_bytes: bytes) -> str:
        try:
            output = self.engine(image_bytes)
            texts = getattr(output, "txts", None)
            if texts is not None:
                return "\n".join(str(text) for text in texts if str(text).strip())
            if isinstance(output, tuple) and output:
                rows = output[0] or []
                return "\n".join(str(row[1]) for row in rows if len(row) > 1 and str(row[1]).strip())
        except Exception:
            return ""
        return ""
