import argparse
import re
from pathlib import Path
from typing import Dict, Tuple

import pymupdf


def _validate_pdf_path(pdf_path: str | Path) -> Path:
    path = Path(pdf_path)
    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a .pdf file: {path}")
    return path


def _extract_lines(pdf_path: str | Path) -> list[str]:
    path = _validate_pdf_path(pdf_path)
    lines: list[str] = []

    try:
        with pymupdf.open(path) as document:
            for page in document:
                # Sorted text order handles normal single- and multi-column text PDFs
                # without rendering pages to images or loading a layout model.
                for raw_line in page.get_text("text", sort=True).splitlines():
                    normalized = re.sub(r"\s+", " ", raw_line).strip()
                    if normalized:
                        lines.append(normalized)
    except pymupdf.FileDataError as error:
        raise ValueError("The uploaded PDF is malformed or corrupted") from error

    if not lines:
        raise ValueError(
            "No text layer found in the PDF. The file may require OCR before extraction."
        )
    return lines


def extract_indexed_text_from_pdf(
    pdf_path: str | Path,
) -> Tuple[str, Dict[int, str]]:
    """Return LLM-ready lines and their stable evidence indexes."""
    index_map = dict(enumerate(_extract_lines(pdf_path)))
    indexed_text = "\n".join(f"[{index}]: {text}" for index, text in index_map.items())
    return indexed_text, index_map


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """Extract page-ordered text from a PDF for use as LLM context."""
    return "\n".join(_extract_lines(pdf_path))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract text from a PDF using PyMuPDF for LLM input."
    )
    parser.add_argument("pdf", type=Path, help="Path to the input PDF")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Optional output .txt file; prints to stdout when omitted",
    )
    args = parser.parse_args()

    text = extract_text_from_pdf(args.pdf)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
        print(f"Extracted text written to: {args.output}")
    else:
        print(text)


if __name__ == "__main__":
    main()
