from __future__ import annotations

from pathlib import Path

import docx
import pypdf


class DocumentService:
    def extract_text(self, file_path: str, filename: str | None = None) -> str:
        name = filename or Path(file_path).name
        suffix = Path(name).suffix.lower()

        if suffix == ".pdf":
            return self.extract_pdf_text(file_path)
        if suffix == ".docx":
            return self.extract_docx_text(file_path)

        raise ValueError("Only PDF and DOCX resumes are supported")

    def extract_pdf_text(self, file_path: str) -> str:
        return self.extract_pdf_text_direct(file_path)

    def extract_docx_text(self, file_path: str) -> str:
        return self.extract_docx_text_direct(file_path)

    def extract_pdf_text_direct(self, file_path: str) -> str:
        text = ""
        with open(file_path, "rb") as file:
            reader = pypdf.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()

    def extract_docx_text_direct(self, file_path: str) -> str:
        text_parts: list[str] = []
        document = docx.Document(file_path)
        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text.strip())
        for table in document.tables:
            for row in table.rows:
                cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if cells:
                    text_parts.append(" | ".join(dict.fromkeys(cells)))
        return "\n".join(text_parts)
