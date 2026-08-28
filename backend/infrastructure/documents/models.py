from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class DocumentExtractionStatus(str, Enum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    FAILED = "failed"


class DocumentPage(BaseModel):
    page_number: int = Field(ge=1)
    text: str = ""
    extraction_method: str
    warnings: list[str] = Field(default_factory=list)


class DocumentTable(BaseModel):
    page_number: int | None = None
    rows: list[list[str]] = Field(default_factory=list)


class DocumentExtractionResult(BaseModel):
    text: str
    source_type: str
    page_count: int | None = None
    character_count: int = Field(ge=0)
    extraction_method: str
    status: DocumentExtractionStatus
    is_partial: bool = False
    warnings: list[str] = Field(default_factory=list)
    pages: list[DocumentPage] = Field(default_factory=list)
    tables: list[DocumentTable] = Field(default_factory=list)


class DocumentProcessingError(ValueError):
    def __init__(self, code: str, safe_message: str, *, status_code: int, warnings: list[str] | None = None) -> None:
        super().__init__(safe_message)
        self.code = code
        self.safe_message = safe_message
        self.status_code = status_code
        self.warnings = warnings or []
